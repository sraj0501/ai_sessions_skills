#!/usr/bin/env python3
"""Rebuild a proposed knowledge base from local WAL evidence, in a new directory."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capture
import cfg
import distill
import kb
import wal

NORMALIZER_VERSION = 1


def candidates(source: Path):
    """Regenerate candidates from exact events, including formerly skipped ones."""
    for event in wal.events(source):
        for record in capture.records_from_payload(event["payload"], event["harness"]):
            record.update(wal_event_id=event["event_id"],
                          wal_machine_id=event["machine_id"],
                          normalizer_version=NORMALIZER_VERSION,
                          wal_evidence={k: event.get(k) for k in
                                        ("cwd", "project", "session", "command", "output",
                                         "exit_code", "task_context", "visible_evaluation")})
            yield record


def stub_write(output: Path, record: dict) -> str:
    """Deterministic fixture writer; no model or network needed."""
    filename, title = kb.known_route(record, output) or kb.fallback_route(record)
    path = output / filename
    fields = {
        "heading": " ".join([record["binary"], *record.get("subcommands", [])]),
        "commands": record.get("team_variants") or [record["command"]],
        "what": "Deterministic replay fixture; replace with a model review.",
        "why": "Evidence: %s/%s" % (record["wal_machine_id"], record["wal_event_id"]),
    }
    kb.insert_entry(path, title, "Captured actions", kb.render_entry(fields, record["sig"]))
    return "new"


def rebuild(source: Path, output: Path, writer: str = "stub") -> dict:
    source = source.resolve()
    output = output.resolve()
    if output.exists():
        raise ValueError("output already exists: " + str(output))
    if output == source or source in output.parents:
        raise ValueError("output must be separate from the WAL")
    backend = None
    if writer == "model":
        backend = cfg.writer_backend("text")
        if not backend:
            raise ValueError("no text model backend available")
    records = list(candidates(source))  # validate entire WAL before writing
    evidence_by_sig = {}
    commands_by_sig = {}
    for record in records:
        evidence_by_sig.setdefault(record["sig"], []).append(record["wal_evidence"])
        commands = commands_by_sig.setdefault(record["sig"], [])
        if record["command"] not in commands:
            commands.append(record["command"])
    output.mkdir(parents=True)
    runtime = output / ".runtime"
    runtime.mkdir()
    seen = set()
    provenance = []
    prompt_path = cfg.TOOL_ROOT / "prompts" / "ENTRY_PROMPT.md"
    prompt_sha = hashlib.sha256(prompt_path.read_bytes()).hexdigest() if writer == "model" else None
    for record in records:
        sig = record["sig"]
        outcome = "duplicate"
        if sig not in seen:
            record["wal_evidence"] = evidence_by_sig[sig]
            record["team_variants"] = commands_by_sig[sig]
            outcome = (stub_write(output, record) if writer == "stub" else
                       distill.document_record(output, runtime, record, backend,
                                               int(cfg.get("distill.model_timeout_seconds", 180))))
            if outcome == "failed":
                raise RuntimeError("model failed on WAL event " + record["wal_event_id"])
            seen.add(sig)
        provenance.append({"machine_id": record["wal_machine_id"],
                           "event_id": record["wal_event_id"], "sig": sig,
                           "normalizer_version": NORMALIZER_VERSION,
                           "writer": writer, "model": backend.get("model") if backend else None,
                           "backend": backend.get("name") if backend else None,
                           "prompt_sha256": prompt_sha, "outcome": outcome})
    manifest = {"schema": 1, "source": str(source), "writer": writer,
                "records": provenance}
    (output / "rebuild-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n",
                                                   encoding="utf-8")
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=wal.root())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--writer", choices=("stub", "model"), default="stub")
    args = parser.parse_args(argv)
    try:
        manifest = rebuild(args.source, args.output, args.writer)
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("rebuilt %d candidate(s) in %s" % (len(manifest["records"]), args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
