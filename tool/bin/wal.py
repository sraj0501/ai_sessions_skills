#!/usr/bin/env python3
"""Immutable local evidence log for reusable command knowledge.

New events live in one durable SQLite file per UTC day. Older checksummed JSON
events remain readable. The queue and Markdown knowledge base are derived views.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import hashlib
import json
import os
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg

SCHEMA = 1


def root() -> Path:
    override = os.environ.get("AI_SKILLS_WAL")
    if override:
        return Path(override).expanduser().resolve()
    setting = cfg.get("wal_dir")
    if setting is not None:
        if not isinstance(setting, str) or not setting.strip():
            raise ValueError("wal_dir must be a non-empty path string")
        base = cfg.config_path().parent if cfg.config_path() else cfg.TOOL_ROOT
        return (base / setting).expanduser().resolve()
    return cfg.runtime_dir() / "wal"


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def machine_id() -> str:
    path = root() / "machine-id"
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(path.parent, 0o700)
    try:
        return path.read_text(encoding="ascii").strip()
    except FileNotFoundError:
        value = str(uuid.uuid4())
        try:
            with path.open("x", encoding="ascii") as fh:
                if os.name != "nt":
                    os.chmod(path, 0o600)
                fh.write(value)
                fh.flush()
                os.fsync(fh.fileno())
        except FileExistsError:
            return path.read_text(encoding="ascii").strip()
        return value


def append(payload: dict, harness: str, source: str = "hook") -> dict:
    """Publish evidence durably before normalization and deduplication."""
    if not isinstance(payload, dict):
        raise ValueError("WAL payload must be an object")
    import capture  # local import avoids an import cycle
    now = datetime.now(timezone.utc)
    event_id = uuid.uuid4().hex
    args = capture._as_dict(capture._first(payload, capture.TOOL_INPUT_KEYS)) or payload
    command = capture._first(args, capture.COMMAND_KEYS)
    cwd = capture._first(payload, capture.CWD_KEYS)
    if cwd is None:
        cwd = next((os.environ[v] for v in capture.CWD_ENV if os.environ.get(v)), None)
    session = capture._first(payload, capture.SESSION_KEYS)
    event = {
        "schema": SCHEMA, "machine_id": machine_id(), "event_id": event_id,
        "timestamp": now.isoformat(), "harness": harness, "source": source,
        "session": session, "cwd": cwd,
        "project": Path(str(cwd)).name if cwd else None,
        "tool": capture._first(payload, capture.TOOL_NAME_KEYS),
        "command": command,
        "output": capture._first(payload, ("tool_response", "toolResponse", "tool_result",
                                                    "toolResult", "result", "output", "response",
                                                    "stdout")),
        "exit_code": capture._first(payload, ("exit_code", "exitCode", "status_code")),
        "task_context": capture._first(payload, ("task", "issue", "user_request", "context")),
        "visible_evaluation": capture._first(payload, ("evaluation", "agent_note", "decision")),
        "payload": payload,
    }
    envelope = {"event": event, "sha256": hashlib.sha256(canonical(event)).hexdigest()}
    directory = root() / "events"
    directory.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(directory, 0o700)
    database = directory / (now.strftime("%Y-%m-%d") + ".sqlite3")
    with closing(sqlite3.connect(database, timeout=30)) as db:
        db.execute("PRAGMA synchronous=FULL")
        with db:
            db.execute("CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, "
                       "timestamp TEXT NOT NULL, envelope BLOB NOT NULL)")
            db.execute("INSERT INTO events VALUES (?, ?, ?)",
                       (event_id, event["timestamp"], canonical(envelope)))
    if os.name != "nt":
        os.chmod(database, 0o600)
    return event


def _verified(envelope: dict, location: str) -> dict:
    event = envelope["event"]
    if event.get("schema") != SCHEMA:
        raise ValueError("unsupported WAL schema: " + str(event.get("schema")))
    if hashlib.sha256(canonical(event)).hexdigest() != envelope.get("sha256"):
        raise ValueError("checksum mismatch: " + location)
    if not event.get("event_id") or not event.get("machine_id"):
        raise ValueError("missing event identity: " + location)
    return event


def read(path: Path) -> dict:
    return _verified(json.loads(path.read_text(encoding="utf-8")), str(path))


def compact(directory: Path | None = None) -> int:
    """Move verified legacy JSON events into daily databases, safe to retry."""
    folder = (directory or root()) / "events"
    paths = sorted(folder.glob("*/*.json"))
    records = [(path, read(path)) for path in paths]  # validate before changing anything
    for path, event in records:
        database = folder / (path.parent.name + ".sqlite3")
        raw = canonical({"event": event, "sha256": hashlib.sha256(canonical(event)).hexdigest()})
        with closing(sqlite3.connect(database, timeout=30)) as db:
            db.execute("PRAGMA synchronous=FULL")
            with db:
                db.execute("CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, "
                           "timestamp TEXT NOT NULL, envelope BLOB NOT NULL)")
                existing = db.execute("SELECT envelope FROM events WHERE event_id = ?",
                                      (event["event_id"],)).fetchone()
                if existing is not None and json.loads(existing[0]) != json.loads(raw):
                    raise ValueError("conflicting WAL event: " + event["event_id"])
                if existing is None:
                    db.execute("INSERT INTO events VALUES (?, ?, ?)",
                               (event["event_id"], event["timestamp"], raw))
        if os.name != "nt":
            os.chmod(database, 0o600)
        path.unlink()
    for day in sorted({path.parent for path in paths}):
        if not any(day.iterdir()):
            day.rmdir()
    return len(records)


def events(directory: Path | None = None):
    base = directory or root()
    folder = base / "events"
    days = sorted({p.stem for p in folder.glob("*.sqlite3")} |
                  {p.name for p in folder.iterdir() if p.is_dir()}) if folder.exists() else []
    for day in days:
        found = []
        database = folder / (day + ".sqlite3")
        if database.exists():
            with closing(sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                for (raw,) in db.execute("SELECT envelope FROM events ORDER BY timestamp, event_id"):
                    found.append(_verified(json.loads(raw), str(database)))
        for path in sorted((folder / day).glob("*.json")):
            found.append(read(path))
        unique = {}
        for item in found:
            key = (item["machine_id"], item["event_id"])
            if key in unique and unique[key] != item:
                raise ValueError("conflicting WAL event: " + item["event_id"])
            unique[key] = item
        yield from sorted(unique.values(), key=lambda item: (item["timestamp"], item["event_id"]))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verb", choices=("inspect", "verify", "compact"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.verb == "compact":
            print("compacted %d legacy WAL event(s)" % compact(args.root))
            return 0
        found = list(events(args.root))
    except (ValueError, OSError, sqlite3.DatabaseError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.verb == "verify":
        print("verified %d WAL event(s)" % len(found))
    else:
        for event in found[-args.limit:]:
            print(json.dumps({k: event.get(k) for k in ("timestamp", "machine_id", "event_id",
                                                          "harness", "session", "command", "exit_code")},
                             ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
