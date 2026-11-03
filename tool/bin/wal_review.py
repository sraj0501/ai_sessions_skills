#!/usr/bin/env python3
"""Compare a WAL rebuild with current knowledge; promote only an approved digest."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import shutil
import sys
import uuid
from pathlib import Path


def files(directory: Path) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(directory.glob("*.md"))}


def digest(directory: Path) -> str:
    hash_ = hashlib.sha256()
    for name, data in files(directory).items():
        hash_.update(name.encode("utf-8") + b"\0" + data + b"\0")
    return hash_.hexdigest()


def diff(current: Path, proposal: Path) -> str:
    before, after = files(current), files(proposal)
    lines = []
    # Promotion overlays proposal files; unrelated current files are retained.
    for name in sorted(after):
        left = before.get(name, b"").decode("utf-8", errors="replace").splitlines(True)
        right = after.get(name, b"").decode("utf-8", errors="replace").splitlines(True)
        lines.extend(difflib.unified_diff(left, right, fromfile="current/" + name,
                                          tofile="proposal/" + name))
    return "".join(lines)


def promote(current: Path, proposal: Path, approved_sha: str) -> Path:
    if not current.is_dir() or not proposal.is_dir():
        raise ValueError("current and proposal must be directories")
    actual = digest(proposal)
    if approved_sha != actual:
        raise ValueError("proposal digest changed; review the diff again")
    new = files(proposal)
    if not new:
        raise ValueError("proposal has no Markdown files")
    if current.resolve() == proposal.resolve():
        raise ValueError("proposal and current are the same directory")
    backup = current / ".runtime" / "revisions" / uuid.uuid4().hex
    backup.mkdir(parents=True)
    for name in new:
        existing = current / name
        if existing.exists():
            shutil.copy2(existing, backup / name)
    for name, content in new.items():
        temp = current / ("." + name + ".wal-new")
        temp.write_bytes(content)
        temp.replace(current / name)
    (backup / "promotion.json").write_text(json.dumps({"proposal": str(proposal.resolve()),
                            "sha256": actual, "files": sorted(new)}, indent=2) + "\n",
                                           encoding="utf-8")
    return backup


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verb", choices=("diff", "promote"))
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--approved-sha")
    args = parser.parse_args(argv)
    try:
        if args.verb == "diff":
            print("proposal SHA256: " + digest(args.proposal))
            print(diff(args.current, args.proposal), end="")
        else:
            if not args.approved_sha:
                raise ValueError("promote requires --approved-sha from a reviewed diff")
            print("promoted; previous files backed up at " +
                  str(promote(args.current, args.proposal, args.approved_sha)))
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
