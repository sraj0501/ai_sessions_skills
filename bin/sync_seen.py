#!/usr/bin/env python3
"""Rebuild `.runtime/seen.txt` from the documented signatures on disk.

`seen.txt` is only a cache: the source of truth is the `<!-- sig: ... -->`
markers inside the knowledge-base markdown files, plus whatever is still
queued in `.runtime/pending.jsonl` / `.runtime/batch.jsonl`.

Rebuilding keeps dedupe correct if seen.txt is deleted, and drops signatures
whose entries were removed from the docs by hand (so they get re-documented).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / ".runtime"
SIG_RE = re.compile(r"<!--\s*sig:\s*([0-9a-f]{6,40})\s*-->")


def documented_sigs() -> set[str]:
    sigs: set[str] = set()
    for md in sorted(ROOT.glob("*.md")):
        sigs.update(SIG_RE.findall(md.read_text(encoding="utf-8", errors="replace")))
    return sigs


def queued_sigs() -> set[str]:
    sigs: set[str] = set()
    for name in ("pending.jsonl", "batch.jsonl"):
        path = RUNTIME / name
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                sig = json.loads(line).get("sig")
            except Exception:
                continue
            if sig:
                sigs.add(sig)
    return sigs


def main() -> int:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    sigs = documented_sigs() | queued_sigs()
    (RUNTIME / "seen.txt").write_text("".join(s + "\n" for s in sorted(sigs)), encoding="utf-8")
    print("seen.txt rebuilt: %d signatures" % len(sigs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
