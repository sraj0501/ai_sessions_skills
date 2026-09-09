#!/usr/bin/env python3
"""Idempotently merge (or remove) our entries in a harness settings file.

Importable:

    json_merge.apply(path, patch, markers)   -> created / updated / unchanged
    json_merge.remove(path, markers)         -> updated / unchanged / missing

Or from a shell:

    json_merge.py --file ~/.claude/settings.json --marker /path/to/tool < patch.json
    json_merge.py --file ~/.claude/settings.json --marker /path/to/tool --remove --prune

Every hook entry we install embeds the tool's absolute path, so the markers
identify exactly our own entries. Install purges anything carrying a marker
before merging the patch, which makes re-running safe and makes uninstall a
pure subtraction. Other tools' settings are never touched.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


def purge(node, markers: list[str]):
    """Drop any list item whose serialised form mentions one of the markers."""
    if isinstance(node, dict):
        return {k: purge(v, markers) for k, v in node.items()}
    if isinstance(node, list):
        kept = []
        for item in node:
            blob = json.dumps(item)
            if any(m and json.dumps(m)[1:-1] in blob for m in markers):
                continue
            kept.append(purge(item, markers))
        return kept
    return node


def prune_empty(node):
    """Remove keys whose value became an empty list/dict after purging."""
    if not isinstance(node, dict):
        return node
    out = {}
    for key, value in node.items():
        value = prune_empty(value)
        if value in ({}, []):
            continue
        out[key] = value
    return out


def deep_merge(base, patch):
    if isinstance(base, dict) and isinstance(patch, dict):
        out = dict(base)
        for key, value in patch.items():
            out[key] = deep_merge(base.get(key), value) if key in base else value
        return out
    if isinstance(base, list) and isinstance(patch, list):
        return base + patch
    return patch


def _load(path: Path) -> tuple[str, dict]:
    if not path.is_file():
        return "", {}
    original = path.read_text(encoding="utf-8")
    if not original.strip():
        return original, {}
    return original, json.loads(original)


def _save(path: Path, original: str, result) -> str:
    rendered = json.dumps(result, indent=2) + "\n"
    if original == rendered:
        return "unchanged"
    path.parent.mkdir(parents=True, exist_ok=True)
    if original:
        shutil.copy2(path, path.with_suffix(path.suffix + ".ai-skills.bak"))
    path.write_text(rendered, encoding="utf-8")
    return "updated" if original else "created"


def apply(path: Path, patch: dict, markers: list[str]) -> str:
    original, data = _load(Path(path))
    return _save(Path(path), original, deep_merge(purge(data, markers), patch))


def remove(path: Path, markers: list[str], prune: bool = True) -> str:
    path = Path(path)
    if not path.is_file():
        return "missing"
    original, data = _load(path)
    cleaned = purge(data, markers)
    return _save(path, original, prune_empty(cleaned) if prune else cleaned)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--marker", required=True, action="append",
                    help="repeatable; identifies our own entries")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--prune", action="store_true")
    args = ap.parse_args()
    path = Path(args.file).expanduser()
    try:
        if args.remove:
            print(remove(path, args.marker, args.prune))
        else:
            print(apply(path, json.loads(sys.stdin.read() or "{}"), args.marker))
    except json.JSONDecodeError as exc:
        print("invalid JSON in %s: %s" % (path, exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
