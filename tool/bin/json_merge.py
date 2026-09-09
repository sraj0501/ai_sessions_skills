#!/usr/bin/env python3
"""Idempotently merge (or remove) our entries in a harness settings file.

    json_merge.py --file ~/.claude/settings.json --marker /path/to/tool < patch.json
    json_merge.py --file ~/.claude/settings.json --marker /path/to/tool --remove

Every hook entry we install embeds the tool's absolute path, so the marker
identifies exactly our own entries. Install purges anything carrying the marker
before merging the patch, which makes re-running the installer safe and makes
uninstall a pure subtraction. Other tools' settings are never touched.

Prints one of: created / updated / unchanged / missing.
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
            if any(m and m in blob for m in markers):
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


def merge(base, patch):
    if isinstance(base, dict) and isinstance(patch, dict):
        out = dict(base)
        for key, value in patch.items():
            out[key] = merge(base.get(key), value) if key in base else value
        return out
    if isinstance(base, list) and isinstance(patch, list):
        return base + patch
    return patch


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--marker", required=True, action="append",
                    help="repeatable; identifies our own entries (e.g. old and new tool paths)")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--prune", action="store_true",
                    help="drop keys left empty after removal (use with --remove)")
    args = ap.parse_args()

    path = Path(args.file).expanduser()
    original = ""
    data: dict = {}
    if path.is_file():
        original = path.read_text(encoding="utf-8")
        try:
            data = json.loads(original) if original.strip() else {}
        except json.JSONDecodeError as exc:
            print("invalid JSON in %s: %s" % (path, exc), file=sys.stderr)
            return 1
    elif args.remove:
        print("missing")
        return 0

    cleaned = purge(data, args.marker)
    if args.remove:
        result = prune_empty(cleaned) if args.prune else cleaned
    else:
        patch = json.loads(sys.stdin.read() or "{}")
        result = merge(cleaned, patch)

    rendered = json.dumps(result, indent=2) + "\n"
    if original == rendered:
        print("unchanged")
        return 0

    path.parent.mkdir(parents=True, exist_ok=True)
    if original:
        shutil.copy2(path, path.with_suffix(path.suffix + ".ai-skills.bak"))
    path.write_text(rendered, encoding="utf-8")
    print("updated" if original else "created")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
