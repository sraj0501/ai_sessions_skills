#!/usr/bin/env python3
"""One distillation pass: turn the capture queue into knowledge-base entries.

Runs the first available writer backend (devin, claude, codex, copilot,
opencode, cursor-agent) as an isolated agent session inside the knowledge-base
directory, verifies that every queued signature ended up documented, then
commits.

No shell is involved: the backend is invoked as an argv list, so quoting works
identically on Windows, macOS and Linux.

    distill.py            # write whatever is queued
    AI_SKILLS_WRITER=claude distill.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg      # noqa: E402
import kb       # noqa: E402
import procs    # noqa: E402

SIG_RE = re.compile(r"<!--\s*sig:\s*([0-9a-f]{6,40})\s*-->")


def log(runtime: Path, message: str) -> None:
    line = "[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), message)
    with (runtime / "distill.log").open("a", encoding="utf-8") as fh:
        fh.write(line)


def read_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def write_records(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records),
                    encoding="utf-8")


def build_prompt(kb: Path, runtime: Path, count: int) -> Path:
    template = (cfg.TOOL_ROOT / "prompts" / "DISTILL_PROMPT.md").read_text(encoding="utf-8")
    existing = sorted(p.name for p in kb.glob("*.md"))
    prompt = runtime / "prompt.md"
    prompt.write_text(
        template
        + "\n## This run\n\n"
        + "- Knowledge-base directory (your working directory): `%s`\n" % kb
        + "- Batch file: `.runtime/batch.jsonl` (%d records)\n" % count
        + "- Knowledge-base files that already exist:\n"
        + "".join("  - `%s`\n" % name for name in existing)
        + "\nProcess every record in the batch file, then reply with one line:\n"
        + "`distilled: <n> new entries, <n> merged, <n> skipped`.\n",
        encoding="utf-8")
    return prompt


def run_backend(backend: dict, prompt: Path, kb: Path, timeout: int, runtime: Path) -> int:
    text = prompt.read_text(encoding="utf-8")
    argv = [backend["bin"]] + [a.replace("{prompt_text}", text) for a in backend["args"]]
    env = {"AI_SKILLS_DISTILLER": "1", "AI_SKILLS_CAPTURE_OFF": "1"}
    stdin_data = text if backend.get("prompt") == "stdin" else None

    merged = dict(os.environ)
    merged.update(env)
    try:
        done = subprocess.run(
            argv, cwd=str(kb), env=merged, timeout=timeout,
            input=stdin_data, capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        log(runtime, "timeout after %ds, writer killed" % timeout)
        return 124
    except FileNotFoundError:
        log(runtime, "writer binary vanished: %s" % backend["bin"])
        return 127

    tail = "\n".join((done.stdout or "").strip().splitlines()[-5:])
    if tail:
        log(runtime, "writer output: " + tail.replace("\n", " | "))
    if done.returncode != 0:
        err = "\n".join((done.stderr or "").strip().splitlines()[-3:])
        if err:
            log(runtime, "writer stderr: " + err.replace("\n", " | "))
    return done.returncode


# --------------------------------------------------------------------------- #
# text mode: Python owns the knowledge base, the model only writes prose
# --------------------------------------------------------------------------- #
FENCE_ONLY = re.compile(r"^```[a-zA-Z]*\s*$")
SKIP_RE = re.compile(r"^\s*SKIP\s*:\s*(.+)$", re.MULTILINE)
SECTION_LINE = re.compile(r"^\s*SECTION\s*:\s*(.+)$", re.MULTILINE)


def entry_prompt(record: dict, existing_sections: list[str] | None = None) -> str:
    template = (cfg.TOOL_ROOT / "prompts" / "ENTRY_PROMPT.md").read_text(encoding="utf-8")
    lines = [template, "\n## Now document this command\n",
             "Command: `%s`" % record.get("command", "")]
    if existing_sections:
        lines.append("\nThe file already has these sections. Reuse one of them "
                     "**exactly** if the command fits; only invent a new name if none do:\n"
                     + "\n".join("- %s" % s for s in existing_sections))
    subcmds = record.get("subcommands") or []
    lines.append("Binary: `%s`%s" % (record.get("binary", ""),
                                     (", subcommands: `%s`" % " ".join(subcmds)) if subcmds else ""))
    full = record.get("full_command") or ""
    if full and full != record.get("command"):
        lines.append("It was part of this command line: `%s`" % full)
    if record.get("ok") is False:
        lines.append("This command FAILED when it was run. Document it anyway and "
                     "note the likely failure mode.")
    lines.append("\nOutput the entry now, starting with the SECTION: line.")
    return "\n".join(lines)


ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def run_http(backend: dict, prompt: str, timeout: int, runtime: Path) -> str | None:
    """Generate over Ollama's HTTP API.

    Deliberately not `ollama run`: that streams through a terminal renderer
    which re-wraps long lines with cursor-movement escapes, so piped output
    cannot be reconstructed reliably. The API returns the text verbatim.
    """
    body = json.dumps({
        "model": backend.get("model") or "",
        "prompt": prompt,
        "stream": False,
        "options": backend.get("options") or {},
    }).encode("utf-8")
    request = urllib.request.Request(backend["url"], data=body,
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8")).get("response") or ""
    except Exception as exc:
        log(runtime, "model request failed (%s): %s" % (backend["url"], exc))
        return None


def run_text(backend: dict, prompt: str, timeout: int, runtime: Path) -> str | None:
    """One text-in/text-out generation. No tools, no file access, no cwd needs."""
    if backend.get("url"):
        return run_http(backend, prompt, timeout, runtime)
    argv = [backend["bin"]] + [a.replace("{prompt_text}", prompt) for a in backend["args"]]
    env = dict(os.environ)
    env.update({"AI_SKILLS_DISTILLER": "1", "AI_SKILLS_CAPTURE_OFF": "1"})
    stdin_data = prompt if backend.get("prompt") == "stdin" else None
    try:
        done = subprocess.run(argv, env=env, timeout=timeout, input=stdin_data,
                              capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        log(runtime, "model timed out after %ds" % timeout)
        return None
    except FileNotFoundError:
        log(runtime, "model binary vanished: %s" % backend["bin"])
        return None
    if done.returncode != 0:
        err = "\n".join((done.stderr or "").strip().splitlines()[-2:])
        log(runtime, "model exited %d: %s" % (done.returncode, err.replace("\n", " | ")))
        return None
    return ANSI.sub("", done.stdout or "")


def parse_entry(text: str) -> tuple[str, str] | tuple[None, str]:
    """Model output -> (section, entry markdown), or (None, skip reason).

    Tolerates the things small models do: wrapping the whole answer in a code
    fence, emitting a sig comment, adding chatter before the heading.
    """
    body = (text or "").strip()
    if not body:
        return None, "empty response"

    lines = body.splitlines()
    if lines and FENCE_ONLY.match(lines[0]):           # whole answer fenced
        closing = next((i for i in range(len(lines) - 1, 0, -1)
                        if lines[i].strip() == "```"), None)
        if closing:
            lines = lines[1:closing]

    heading_at = next((i for i, line in enumerate(lines) if line.startswith("### ")), None)
    if heading_at is None:
        found = SKIP_RE.search(body)
        return None, (found.group(1).strip() if found else "no entry heading in response")

    section = "Other"
    found = SECTION_LINE.search("\n".join(lines[:heading_at]) or "")
    if found:
        section = found.group(1).strip().strip("<>").strip()

    kept = [line for line in lines[heading_at:] if not kb.SIG_RE.search(line)]
    entry = "\n".join(kept).strip()
    if "```" not in entry:
        return None, "response had no command block"
    return section, entry


def document_record(kb_dir: Path, runtime: Path, record: dict, backend: dict,
                    timeout: int) -> str:
    """Place one record into the knowledge base. Returns what happened."""
    sig = record.get("sig") or ""
    binary = str(record.get("binary") or "")
    subcmds = list(record.get("subcommands") or [])

    filename, title = kb.route(record)
    path = kb_dir / filename
    is_new_file = not path.exists()

    known_sections: list[str] = []
    if not is_new_file:
        text = path.read_text(encoding="utf-8", errors="replace")
        match = kb.find_match(kb.parse(text), binary, subcmds)
        if match:
            kb.add_sig(path, sig, match.heading)
            return "merged"
        known_sections = kb.sections(text)

    raw = run_text(backend, entry_prompt(record, known_sections), timeout, runtime)
    if raw is None:
        # The model was unreachable or errored. That is not a verdict about the
        # record, so leave it undocumented and let the batch retry.
        return "failed"

    section, entry = parse_entry(raw)
    if section is None:
        kb.note_skipped(kb_dir, sig, record.get("command", ""), entry)
        return "skipped"

    head, rest = entry.split("\n", 1) if "\n" in entry else (entry, "")
    kb.insert_entry(path, title, section, "%s\n<!-- sig: %s -->\n%s" % (head, sig, rest))
    if is_new_file:
        kb.ensure_readme_row(kb_dir, filename, title)
    return "new"


def distill_text(kb_dir: Path, runtime: Path, records: list[dict], backend: dict,
                 timeout: int) -> tuple[int, list[dict]]:
    """Document every record. Returns (documented count, records still missing)."""
    done_sigs = kb.documented_sigs(kb_dir)
    tally = {"new": 0, "merged": 0, "skipped": 0, "duplicate": 0, "failed": 0}
    failed = []
    for record in records:
        if record.get("sig") in done_sigs:
            tally["duplicate"] += 1
            continue
        try:
            outcome = document_record(kb_dir, runtime, record, backend, timeout)
        except Exception as exc:                      # never lose the batch to one bad record
            log(runtime, "record %s errored: %s" % (record.get("sig"), exc))
            outcome = "failed"
        tally[outcome] += 1
        if outcome == "failed":
            failed.append(record)
        else:
            done_sigs.add(record.get("sig"))
    log(runtime, "distilled: %(new)d new, %(merged)d merged, %(skipped)d skipped, "
                 "%(duplicate)d already known, %(failed)d failed" % tally)
    return sum(tally.values()) - tally["failed"], failed


def undocumented(kb_dir: Path, records: list[dict]) -> int:
    docs = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                     for p in kb_dir.glob("*.md"))
    have = set(SIG_RE.findall(docs))
    return sum(1 for r in records if r.get("sig") not in have)


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True)


def dirty_paths(repo: Path) -> set[str]:
    """Every path with uncommitted content, staged or not, tracked or not.

    NUL-separated so paths with spaces or non-ASCII survive intact; gitignored
    files (notably `.runtime/`) stay excluded.
    """
    done = git(repo, "status", "--porcelain", "-z", "--untracked-files=all")
    if done.returncode != 0:
        return set()
    fields = (done.stdout or "").split("\0")
    paths, i = set(), 0
    while i < len(fields):
        entry, i = fields[i], i + 1
        if len(entry) < 4:
            continue
        status, path = entry[:2], entry[3:]
        paths.add(path)
        if "R" in status or "C" in status:   # rename/copy: source follows as its own field
            if i < len(fields):
                paths.add(fields[i])
                i += 1
    return paths


def commit(repo: Path, runtime: Path, count: int, backend_name: str,
           preexisting: set[str] | None = None) -> None:
    """Commit only what the writer changed.

    Anything already dirty before the writer ran is the user's work in progress
    and is left alone. A path dirty on both sides is genuinely ambiguous — the
    two edits are interleaved in one file — so it is reported and skipped rather
    than guessed at.
    """
    if cfg.get("auto_commit", True) is not True:
        return
    if git(repo, "rev-parse", "--git-dir").returncode != 0:
        return

    preexisting = set() if preexisting is None else preexisting
    now = dirty_paths(repo)
    ours = sorted(now - preexisting)
    entangled = sorted(now & preexisting)

    if entangled:
        shown = ", ".join(entangled[:5]) + (" ..." if len(entangled) > 5 else "")
        log(runtime, "left %d pre-existing change(s) uncommitted: %s" % (len(entangled), shown))
    if not ours:
        log(runtime, "nothing of ours to commit")
        return

    git(repo, "add", "--", *ours)
    # --only commits exactly these paths, so anything the user had staged stays staged.
    done = git(repo, "commit", "-q", "--only",
               "-m", "docs: document %d captured action(s)" % count,
               "-m", "Written automatically by the ai-session-skills writer (%s)." % backend_name,
               "--", *ours)
    if done.returncode != 0:
        err = "\n".join((done.stderr or done.stdout or "").strip().splitlines()[-2:])
        log(runtime, "commit failed: " + (err.replace("\n", " | ") or "unknown error"))
        return
    log(runtime, "committed %d action(s) across %d file(s)" % (count, len(ours)))

    if cfg.get("auto_push", False) is True and git(repo, "remote", "get-url", "origin").returncode == 0:
        if git(repo, "push", "-q").returncode == 0:
            log(runtime, "pushed to origin")


def main() -> int:
    kb_dir, runtime = cfg.kb_dir(), cfg.runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "failed").mkdir(exist_ok=True)

    pending, batch = runtime / "pending.jsonl", runtime / "batch.jsonl"
    attempts_file = runtime / "batch.attempts"
    timeout = int(cfg.get("distill.timeout_seconds", 900) or 900)
    max_attempts = int(cfg.get("distill.max_attempts", 3) or 3)
    max_records = int(cfg.get("distill.max_batch_records", 40) or 40)

    mode = "text" if str(cfg.get("writer.mode", "text")).lower() == "text" else "agent"
    backend = cfg.writer_backend(mode)
    if not backend:
        log(runtime, "no %s writer backend available (checked writer.prefer%s)"
            % (mode, "_text" if mode == "text" else ""))
        return 0

    lock = procs.DirLock(runtime / "distill.lock", stale_after=timeout * 2)
    if not lock.acquire():
        return 0
    try:
        # Carry over a previously failed batch, then take newly pending records.
        records = read_records(batch)
        queued = read_records(pending)
        take = max(0, max_records - len(records))
        records += queued[:take]
        leftover = queued[take:]
        if not records:
            batch.unlink(missing_ok=True)
            return 0
        write_records(batch, records)
        write_records(pending, leftover)

        attempt = 1
        try:
            attempt = int(attempts_file.read_text().strip()) + 1
        except Exception:
            pass
        attempts_file.write_text(str(attempt), encoding="utf-8")
        log(runtime, "distilling %d record(s), attempt %d, backend %s"
            % (len(records), attempt, backend["name"]))

        preexisting = dirty_paths(kb_dir)   # the user's work in progress; not ours to commit

        if mode == "text":
            per_record = int(cfg.get("distill.model_timeout_seconds", 180) or 180)
            distill_text(kb_dir, runtime, records, backend, per_record)
            status = 0
        else:
            prompt = build_prompt(kb_dir, runtime, len(records))
            status = run_backend(backend, prompt, kb_dir, timeout, runtime)

        # Same safety net in both modes: every sig must have landed in some .md.
        missing = undocumented(kb_dir, records) if status == 0 else None
        if status == 0:
            log(runtime, "writer finished; undocumented signatures: %d" % missing)

        if status != 0 or missing:
            log(runtime, "distillation incomplete (exit=%s undocumented=%s)"
                % (status, "n/a" if missing is None else missing))
            if attempt >= max_attempts:
                stamp = time.strftime("%Y%m%d-%H%M%S")
                batch.replace(runtime / "failed" / ("batch-%s.jsonl" % stamp))
                attempts_file.unlink(missing_ok=True)
                subprocess.run(procs.python_argv(cfg.TOOL_ROOT / "bin" / "sync_seen.py"),
                               capture_output=True)
                log(runtime, "gave up after %d attempts; batch parked in "
                             "failed/batch-%s.jsonl and signatures released" % (attempt, stamp))
            return 0

        batch.unlink(missing_ok=True)
        attempts_file.unlink(missing_ok=True)
        subprocess.run(procs.python_argv(cfg.TOOL_ROOT / "bin" / "sync_seen.py"),
                       capture_output=True)
        commit(kb_dir, runtime, len(records), backend["name"], preexisting)
        log(runtime, "done")
        return 0
    finally:
        lock.release()


if __name__ == "__main__":
    raise SystemExit(main())
