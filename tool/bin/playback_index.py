"""Model-free, incremental text index of exact local playback events."""
from __future__ import annotations

import json
import hashlib
import re
import sqlite3
import uuid
from contextlib import closing
from pathlib import Path

import playback_query
from playback_worker import _action, _result

VERSION = 3

MAX_COMMAND = 900
MAX_RESULT_LINE = 180


def _short(value: str, limit: int) -> str:
    value = value.strip()
    return value if len(value) <= limit else value[:limit].rstrip() + " [full text in recording]"


def _command(payload: dict) -> str:
    label, action = _action(payload)
    if action.startswith("*** Begin Patch"):
        lines = [line for line in action.splitlines()
                 if line.startswith(("*** Add File:", "*** Update File:", "*** Delete File:",
                                     "+", "-")) and line not in ("++", "--")]
        action = "\n".join(lines)
    return f"{label}: {_short(action, MAX_COMMAND)}"


def _observed(payload: dict) -> str:
    result = _result(payload)
    if result == "Not recorded":
        return result
    lines = [line.strip() for line in result.splitlines() if line.strip()]
    signals = [line for line in lines if re.search(
        r"(?i)\b(error|failed|failure|warning|passed|success|ok|tests? run|ran \d+ tests?|exit code|"
        r"not found|refused|timeout|modified|created|deleted)\b", line)]
    selected = signals[:3] if signals else lines[:2]
    if len(lines) > len(selected):
        selected.append(f"[{len(lines) - len(selected)} other output lines in recording]")
    return " | ".join(_short(line, MAX_RESULT_LINE) for line in selected)


def _text(event: dict, number: int, next_action: str = "",
          reasoning: str = "") -> str:
    if event.get("type") == "note":
        return f"Step {number}. {event.get('kind', 'note')}: {event.get('text', '')}"
    payload = event.get("payload") or {}
    return (f"Step {number}. {_command(payload)}\n"
            f"Observed: {_observed(payload)}\n"
            f"Inference: {reasoning or 'Not recorded'}\n"
            f"Next recorded action: {next_action or 'None recorded'}")


def reasoning_file(folder: Path) -> Path:
    return folder / "reasoning.json"


def load_reasoning(folder: Path) -> dict:
    path = reasoning_file(folder)
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("invalid playback reasoning file")
    return data


def save_reasoning(folder: Path, data: dict) -> None:
    path = reasoning_file(folder)
    temp = folder / ("reasoning-" + uuid.uuid4().hex + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)


def evidence_digest(event: dict, next_action: str) -> str:
    payload = event.get("payload") or {}
    source = _command(payload) + "\n" + _observed(payload) + "\n" + next_action
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def tool_steps(ident: str) -> list[dict]:
    """Return compact tool evidence with recorded/generated reasoning status."""
    _, folder = playback_query._recording(ident)
    paths = sorted((folder / "events").glob("*.json"))
    events = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    generated = load_reasoning(folder)
    result = []
    for number, (path, event) in enumerate(zip(paths, events), 1):
        if event.get("type") != "tool":
            continue
        following = events[number:]
        next_tool = next((item for item in following if item.get("type") == "tool"), None)
        next_action = _short(_command(next_tool.get("payload") or {}), 220) if next_tool else ""
        until_next = following[:following.index(next_tool) if next_tool else len(following)]
        notes = [item for item in until_next if item.get("type") == "note"
                 and item.get("kind") in ("observation", "decision")]
        note_numbers = [number + offset + 1 for offset, item in enumerate(until_next)
                        if item in notes]
        recorded = "; ".join(_short(str(item.get("text", "")), 280) for item in notes)
        digest = evidence_digest(event, next_action)
        saved = generated.get(path.name, {})
        reconstructed = (saved.get("text", "") if isinstance(saved, dict)
                         and saved.get("digest") == digest else "")
        result.append({"number": number, "event_id": path.name, "event": event,
                       "next_action": next_action, "recorded": recorded,
                       "generated": reconstructed, "digest": digest,
                       "note_numbers": note_numbers})
    return result


def _excerpt(value: str, limit: int = 2400, focus: str = "") -> str:
    if len(value) <= limit:
        return value
    words = sorted(set(re.findall(r"[a-z0-9_./:-]{4,}", focus.lower())), key=len, reverse=True)
    location = next((value.lower().find(word) for word in words
                     if value.lower().find(word) >= 0), -1)
    if location >= limit // 2:
        begin = max(0, location - limit // 3)
        end = min(len(value), begin + limit)
        return (f"[... {begin} earlier characters omitted ...]\n" + value[begin:end]
                + f"\n[... {len(value) - end} later characters omitted; exact event remains on disk ...]")
    head = limit * 2 // 3
    tail = limit - head
    return (value[:head] + f"\n[... {len(value) - limit} characters omitted; exact event remains on disk ...]\n"
            + value[-tail:])


def indexed_steps(ident: str) -> list[tuple[int, str]]:
    """Refresh changed steps and return their text; cache never replaces evidence."""
    _, folder = playback_query._recording(ident)
    paths = sorted((folder / "events").glob("*.json"))
    database = folder / "text-index.sqlite3"
    with closing(sqlite3.connect(database, timeout=30)) as db:
        db.execute("CREATE TABLE IF NOT EXISTS steps (number INTEGER PRIMARY KEY, source TEXT NOT NULL, "
                   "mtime_ns INTEGER NOT NULL, size INTEGER NOT NULL, version INTEGER NOT NULL, text TEXT NOT NULL)")
        events = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
        by_number = {item["number"]: item for item in tool_steps(ident)}
        superseded = {note: item["number"] for item in by_number.values()
                      if item["generated"] for note in item["note_numbers"]}
        for number, (path, event) in enumerate(zip(paths, events), 1):
            stat = path.stat()
            old = db.execute("SELECT source, mtime_ns, size, version, text FROM steps WHERE number=?",
                             (number,)).fetchone()
            tool = by_number.get(number)
            next_action = tool["next_action"] if tool else ""
            reasoning = (("Reconstructed later: " + tool["generated"] if tool["generated"]
                          else tool["recorded"]) if tool else "")
            signature = (path.name, stat.st_mtime_ns, stat.st_size, VERSION)
            step_text = (f"Step {number}. Recorded note superseded by later reconstructed "
                         f"inference for step {superseded[number]}." if number in superseded
                         else _text(event, number, next_action, reasoning))
            if old != (*signature, step_text):
                db.execute("INSERT OR REPLACE INTO steps VALUES (?, ?, ?, ?, ?, ?)",
                           (number, *signature, step_text))
        db.execute("DELETE FROM steps WHERE number > ?", (len(paths),))
        db.commit()
        return db.execute("SELECT number, text FROM steps ORDER BY number").fetchall()


def relevant_steps(steps: list[tuple[int, str]], question: str, limit: int = 5,
                   title: str = ""
                   ) -> list[tuple[int, str]]:
    """Select question-matching steps locally; preserve timeline order in prompt."""
    words = set(re.findall(r"[a-z0-9_./:-]{3,}", question.lower()))
    stop = {"the", "and", "for", "with", "from", "what", "which", "where", "when",
            "were", "this", "that", "about", "steps", "step", "playback", "recorded",
            "issue", "fixed", "fix", "resolution", "resolved", "problem", "how", "did"}
    words -= stop
    if not words and title:
        words = set(re.findall(r"[a-z0-9_./:-]{3,}", title.lower())) - stop
        words -= {"use", "using", "rather", "than", "values", "skills", "sessions", "ai"}
        changes = [item for item in steps if
                   ("*** Update File:" in item[1][:200] and
                    "tool/bin/" in item[1][:300].lower().replace("\\", "/")) or
                   item[1].lower().startswith(f"step {item[0]}. outcome")]
        def score(item: tuple[int, str]) -> tuple[int, int]:
            content = item[1][:1800].lower()
            return (sum(min(content.count(word), 3) for word in words), -item[0])
        selected = sorted(changes, key=score, reverse=True)[:max(0, limit - 1)]
        checks = [item for item in steps if item not in selected and
                  ("tests passed" in item[1].lower() or
                   (re.search(r"Ran \d+ tests?", item[1]) and
                    re.search(r"(?:^|\| )OK(?:\s|$)", item[1]))) and
                  not re.search(r"(?m)^(?:FAILED|ERROR)", item[1])]
        if checks:
            selected.append(max(checks, key=score))
        if selected:
            return sorted(selected[:limit], key=lambda item: item[0])
    ranked = sorted(steps, key=lambda item: (-sum(min(item[1].lower().count(w), 5)
                                                    for w in words), item[0]))
    return sorted(ranked[:limit], key=lambda item: item[0])


def excerpt(value: str, limit: int = 2400, focus: str = "") -> str:
    return _excerpt(value, limit, focus)


def compact_timeline(ident: str, start: int = 1, limit: int = 5) -> dict:
    """The bounded playback view passed to a chat model; raw events stay on disk."""
    if type(start) is not int or start < 1:
        raise ValueError("start must be a positive step number")
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("limit must be an integer from 1 to 20")
    steps = indexed_steps(ident)
    page = steps[start - 1:start - 1 + limit]
    return {"total_steps": len(steps), "steps": [
        {"step": number, "text": excerpt(value, limit=1200)} for number, value in page],
        "next_start": start + len(page) if start + len(page) <= len(steps) else None}
