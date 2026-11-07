#!/usr/bin/env python3
"""Propose model-guided topic consolidation, then apply a reviewed proposal.

The model sees one small source file at a time. Proposals never edit knowledge.
Apply requires the printed digest and verifies that every affected file is still
identical to the reviewed version before making a compressed local backup.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg
import distill
import kb
import procs
import sync_seen


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def proposal_hash(data: dict) -> str:
    body = {key: value for key, value in data.items() if key != "sha256"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"))
                          .encode("utf-8")).hexdigest()


def select(data: dict, sources: set[str]) -> dict:
    """Create a separately digestible proposal containing reviewed moves only."""
    if data.get("schema") != 1 or data.get("sha256") != proposal_hash(data):
        raise ValueError("input proposal digest is invalid")
    moves = [move for move in data["moves"] if move["source"] in sources]
    if not moves or len(moves) != len(sources):
        raise ValueError("select at least one source from the proposal")
    result = {**data, "moves": moves}
    result["sha256"] = proposal_hash(result)
    return result


def propose(kb_dir: Path, runtime: Path, backend: dict, max_entries: int = 5,
            sources: set[str] | None = None, progress: bool = False) -> dict:
    """Recommend only whole-file moves agreed on by every entry in that file."""
    moves = []
    for path in sorted(kb_dir.glob("*.md")):
        if path.name in ("README.md", kb.SKIPPED_FILE):
            continue
        if sources is not None and path.name not in sources:
            continue
        entries = kb.parse(path.read_text(encoding="utf-8", errors="replace"))
        if not entries or len(entries) > max_entries or any(not e.sigs or not e.commands
                                                              for e in entries):
            continue
        if progress:
            print("Checking %s (%d entries)..." % (path.name, len(entries)),
                  file=sys.stderr, flush=True)
        destinations = []
        for entry in entries:
            action = kb.action_of(entry)
            if not action:
                break
            record = {"binary": action[0], "command": entry.commands[0],
                      "subcommands": list(action[1])}
            choice = distill.classify(record, kb_dir, backend,
                                     int(cfg.get("distill.model_timeout_seconds", 180)),
                                     runtime, excluded={path.name})
            if not choice or choice[0] == path.name or not (kb_dir / choice[0]).is_file():
                break
            destinations.append(choice[0])
        if len(destinations) != len(entries) or len(set(destinations)) != 1:
            continue
        destination = kb_dir / destinations[0]
        if any(kb.find_match(kb.parse(destination.read_text(encoding="utf-8")),
                             *kb.action_of(entry)) for entry in entries):
            continue
        moves.append({"source": path.name, "destination": destination.name,
                      "entries": len(entries), "source_sha256": file_hash(path),
                      "destination_sha256": file_hash(destination),
                      "examples": [entry.commands[0] for entry in entries]})
    # A destination must remain in place during this run; avoid chained moves.
    sources = {move["source"] for move in moves}
    moves = [move for move in moves if move["destination"] not in sources]
    data = {"schema": 1, "moves": moves,
            "index_sha256": file_hash(kb_dir / "README.md"),
            "routes_sha256": file_hash(kb_dir / kb.ROUTES_FILE)}
    data["sha256"] = proposal_hash(data)
    return data


def apply(kb_dir: Path, runtime: Path, data: dict, approved_sha: str) -> tuple[int, Path]:
    if data.get("schema") != 1 or data.get("sha256") != proposal_hash(data) or \
            approved_sha != data["sha256"]:
        raise ValueError("proposal digest differs from the reviewed digest")
    moves = data.get("moves")
    if not isinstance(moves, list) or not moves:
        raise ValueError("proposal has no moves")
    if file_hash(kb_dir / "README.md") != data.get("index_sha256") or \
            file_hash(kb_dir / kb.ROUTES_FILE) != data.get("routes_sha256"):
        raise ValueError("knowledge index or routes changed since proposal")
    sources = set()
    for move in moves:
        source, destination = move["source"], move["destination"]
        if (kb.safe_filename(source) != source or kb.safe_filename(destination) != destination
                or source == destination or source in sources):
            raise ValueError("invalid or repeated file in proposal")
        sources.add(source)
        if not (kb_dir / source).is_file() or not (kb_dir / destination).is_file():
            raise ValueError("source or destination file is missing")
        if file_hash(kb_dir / source) != move["source_sha256"] or \
                file_hash(kb_dir / destination) != move["destination_sha256"]:
            raise ValueError("knowledge changed since proposal; generate a new proposal")
    if any(move["destination"] in sources for move in moves):
        raise ValueError("chained moves are not supported")
    lock = procs.DirLock(runtime / "distill.lock", stale_after=1800)
    if not lock.acquire():
        raise ValueError("knowledge writer is active; retry after it finishes")
    try:
        # Preflight again after obtaining the writer lock, closing the gap
        # between review and backup if a writer finished in that interval.
        if file_hash(kb_dir / "README.md") != data["index_sha256"] or \
                file_hash(kb_dir / kb.ROUTES_FILE) != data["routes_sha256"] or \
                any(file_hash(kb_dir / move["source"]) != move["source_sha256"] or
                    file_hash(kb_dir / move["destination"]) != move["destination_sha256"]
                    for move in moves):
            raise ValueError("knowledge changed since proposal; generate a new proposal")
        backup = runtime / ("knowledge-before-organize-%s.zip" % time.strftime("%Y%m%d-%H%M%S"))
        with zipfile.ZipFile(backup, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in sorted(sources | {m["destination"] for m in moves} |
                               {"README.md", kb.ROUTES_FILE}):
                path = kb_dir / name
                if path.is_file():
                    archive.write(path, name)
        before_sigs = kb.documented_sigs(kb_dir)
        count = sum(kb.merge_file(kb_dir, move["source"], move["destination"])
                    for move in moves)
        if kb.documented_sigs(kb_dir) != before_sigs:
            raise RuntimeError("signature set changed; restore affected files from " + str(backup))
        sync_seen.main()
        return count, backup
    finally:
        lock.release()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verb", choices=("propose", "select", "apply"))
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--output", type=Path,
                        help="New proposal JSON path for select")
    parser.add_argument("--approved-sha", default="")
    parser.add_argument("--max-entries", type=int, default=5)
    parser.add_argument("--source", action="append", default=[],
                        help="Only inspect this source filename; repeat for several files")
    args = parser.parse_args(argv)
    kb_dir, runtime = cfg.kb_dir(), cfg.runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)
    try:
        if args.verb == "propose":
            if args.proposal.exists() or args.max_entries < 1:
                raise ValueError("proposal must be a new path and max-entries must be positive")
            backend = cfg.writer_backend("text")
            if not backend:
                raise ValueError("no text writer is available")
            sources = {kb.safe_filename(name) for name in args.source}
            if any(not (kb_dir / name).is_file() for name in sources):
                raise ValueError("a requested source file does not exist")
            data = propose(kb_dir, runtime, backend, args.max_entries,
                           sources or None, progress=True)
            args.proposal.parent.mkdir(parents=True, exist_ok=True)
            args.proposal.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            print("proposed %d moves; review %s; SHA256 %s" %
                  (len(data["moves"]), args.proposal, data["sha256"]))
        elif args.verb == "select":
            if not args.source or not args.output or args.output.exists():
                raise ValueError("select requires --source and a new --output path")
            data = select(json.loads(args.proposal.read_text(encoding="utf-8")),
                          {kb.safe_filename(name) for name in args.source})
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            print("selected %d moves; review %s; SHA256 %s" %
                  (len(data["moves"]), args.output, data["sha256"]))
        else:
            data = json.loads(args.proposal.read_text(encoding="utf-8"))
            count, backup = apply(kb_dir, runtime, data, args.approved_sha)
            print("moved %d entries; compressed backup: %s" % (count, backup))
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
