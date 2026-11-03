#!/usr/bin/env python3
"""Immutable local evidence log for reusable command knowledge.

Each event is one atomically published, checksummed JSON file. The queue and
Markdown knowledge base are derived views; neither is needed to inspect the log.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
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
    if setting:
        base = cfg.config_path().parent if cfg.config_path() else cfg.TOOL_ROOT
        return (base / str(setting)).expanduser().resolve()
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
    directory = root() / "events" / now.strftime("%Y-%m-%d")
    directory.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(directory.parent, 0o700)
        os.chmod(directory, 0o700)
    name = now.strftime("%H%M%S.%f") + "-" + event_id + ".json"
    fd, temporary = tempfile.mkstemp(prefix=".event-", dir=directory)
    try:
        if os.name != "nt":
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as fh:
            fh.write(canonical(envelope) + b"\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(temporary, directory / name)
        if os.name != "nt":
            dir_fd = os.open(directory, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return event


def read(path: Path) -> dict:
    envelope = json.loads(path.read_text(encoding="utf-8"))
    event = envelope["event"]
    if event.get("schema") != SCHEMA:
        raise ValueError("unsupported WAL schema: " + str(event.get("schema")))
    if hashlib.sha256(canonical(event)).hexdigest() != envelope.get("sha256"):
        raise ValueError("checksum mismatch: " + str(path))
    if not event.get("event_id") or not event.get("machine_id"):
        raise ValueError("missing event identity: " + str(path))
    return event


def events(directory: Path | None = None):
    base = directory or root()
    for path in sorted((base / "events").glob("*/*.json")):
        yield read(path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verb", choices=("inspect", "verify"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args(argv)
    try:
        found = list(events(args.root))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
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
