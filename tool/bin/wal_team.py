#!/usr/bin/env python3
"""Explicit, reviewable transfer of sanitized command candidates between machines.

Export requires an allow-list of WAL event IDs. The resulting bundle contains
no raw payload, result, task text, or playback. Common secret and absolute
path patterns are rejected; review the bundle
before sending it. Ingest is idempotent and never publishes Markdown.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capture
import cfg
import distill
import wal
import wal_rebuild

SCHEMA = 1
SENSITIVE = re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key|authorization|bearer|private[_-]?key|AKIA[0-9A-Z]{16})")
ABS_PATH = re.compile(r"(?i)(?:[A-Z]:[\\/]|(?:^|[\s='\"])/[^\s]+|://)")


def candidates(source: Path, allowed: set[str]) -> list[dict]:
    selected = []
    found = set()
    for event in wal.events(source):
        if event["event_id"] not in allowed:
            continue
        found.add(event["event_id"])
        for record in capture.records_from_payload(event["payload"], event["harness"]):
            command = record["command"]
            if SENSITIVE.search(command) or ABS_PATH.search(command):
                raise ValueError("sensitive command rejected: " + event["event_id"])
            selected.append({"schema": SCHEMA, "machine_id": event["machine_id"],
                             "event_id": event["event_id"], "candidate_id":
                             hashlib.sha256((event["machine_id"] + ":" +
                                             event["event_id"] + ":" + record["sig"]).encode()).hexdigest(),
                             "sig": record["sig"], "kind": record["kind"],
                             "binary": record["binary"], "subcommands": record["subcommands"],
                             "command": command, "normalizer_version": 1})
    missing = allowed - found
    if missing:
        raise ValueError("unknown event ID(s): " + ", ".join(sorted(missing)))
    return selected


def export(source: Path, allow_file: Path, output: Path) -> int:
    if output.exists():
        raise ValueError("bundle already exists")
    allowed = {line.strip() for line in allow_file.read_text(encoding="utf-8").splitlines()
               if line.strip() and not line.startswith("#")}
    if not allowed:
        raise ValueError("allow-list is empty")
    records = candidates(source, allowed)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"schema": SCHEMA, "candidates": records},
                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(records)


def ingest(bundle: Path, inbox: Path) -> tuple[int, int]:
    data = json.loads(bundle.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA or not isinstance(data.get("candidates"), list):
        raise ValueError("unsupported bundle")
    validated = []
    for record in data["candidates"]:
        if record.get("schema") != SCHEMA or not all(record.get(k) for k in
            ("machine_id", "event_id", "candidate_id", "sig", "binary", "command")):
            raise ValueError("invalid candidate")
        if SENSITIVE.search(record["command"]) or ABS_PATH.search(record["command"]):
            raise ValueError("sensitive command rejected")
        expected = hashlib.sha256((record["machine_id"] + ":" + record["event_id"] +
                                   ":" + record["sig"]).encode()).hexdigest()
        if record["candidate_id"] != expected:
            raise ValueError("candidate identity mismatch")
        validated.append(record)
    inbox.mkdir(parents=True, exist_ok=True)
    added = 0
    for record in validated:
        path = inbox / (record["candidate_id"] + ".json")
        if path.exists():
            if json.loads(path.read_text(encoding="utf-8")) != record:
                raise ValueError("conflicting candidate: " + record["candidate_id"])
            continue
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        added += 1
    return added, len(validated) - added


def report(inbox: Path) -> str:
    groups = {}
    for path in sorted(inbox.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        groups.setdefault(record["sig"], []).append(record)
    lines = ["# Team candidate review", "",
             "Signature equality is a first pass. Review meaning and command variants before publishing.", ""]
    for sig, records in sorted(groups.items()):
        lines += ["## %s — %s" % (sig, records[0]["binary"]), ""]
        for record in records:
            lines.append("- `%s` — %s / %s" % (record["command"].replace("`", "'"),
                                               record["machine_id"], record["event_id"]))
        lines.append("")
    return "\n".join(lines)


def propose(inbox: Path, output: Path, writer: str) -> int:
    """One central processor drafts a fresh KB; a human reviews before Git publish."""
    if output.exists():
        raise ValueError("proposal output already exists")
    records = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(inbox.glob("*.json"))]
    variants = {}
    for item in records:
        commands = variants.setdefault(item["sig"], [])
        if item["command"] not in commands:
            commands.append(item["command"])
    backend = cfg.writer_backend("text") if writer == "model" else None
    if writer == "model" and not backend:
        raise ValueError("no text model backend available")
    output.mkdir(parents=True)
    runtime = output / ".runtime"
    runtime.mkdir()
    seen = set()
    manifest = []
    for item in records:
        record = {**item, "full_command": item["command"], "ok": True,
                  "wal_event_id": item["event_id"],
                  "wal_machine_id": item["machine_id"],
                  "team_variants": variants[item["sig"]]}
        outcome = "duplicate"
        if record["sig"] not in seen:
            outcome = (wal_rebuild.stub_write(output, record) if writer == "stub" else
                       distill.document_record(output, runtime, record, backend,
                                               int(cfg.get("distill.model_timeout_seconds", 180))))
            if outcome == "failed":
                raise RuntimeError("writer failed on " + item["candidate_id"])
            seen.add(record["sig"])
        manifest.append({"candidate_id": item["candidate_id"], "sig": item["sig"],
                         "outcome": outcome})
    (output / "team-manifest.json").write_text(json.dumps({"schema": 1, "writer": writer,
                                                 "candidates": manifest}, indent=2) + "\n",
                                                encoding="utf-8")
    return len(records)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="verb", required=True)
    exp = sub.add_parser("export")
    exp.add_argument("--source", type=Path, default=wal.root())
    exp.add_argument("--allow", type=Path, required=True)
    exp.add_argument("--output", type=Path, required=True)
    inc = sub.add_parser("ingest")
    inc.add_argument("--bundle", type=Path, required=True)
    inc.add_argument("--inbox", type=Path, required=True)
    rep = sub.add_parser("report")
    rep.add_argument("--inbox", type=Path, required=True)
    draft = sub.add_parser("propose")
    draft.add_argument("--inbox", type=Path, required=True)
    draft.add_argument("--output", type=Path, required=True)
    draft.add_argument("--writer", choices=("stub", "model"), default="stub")
    args = parser.parse_args(argv)
    try:
        if args.verb == "export":
            print("exported %d candidate(s); review the bundle before sending" %
                  export(args.source, args.allow, args.output))
        elif args.verb == "ingest":
            added, duplicate = ingest(args.bundle, args.inbox)
            print("ingested %d; %d retry duplicate(s)" % (added, duplicate))
        elif args.verb == "propose":
            print("drafted %d candidate(s) for review" %
                  propose(args.inbox, args.output, args.writer))
        else:
            print(report(args.inbox))
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
