"""Search documented entries: python tool/bin/search.py git branch"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg
import kb


def search(root: Path, query: str, topic: str = "") -> list[dict]:
    terms = query.casefold().split()
    if not terms:
        return []
    matches = []
    for path in sorted(root.glob("*.md")):
        if path.name.startswith("_") or path.name == "README.md":
            continue
        if topic and topic.casefold() not in path.stem.casefold():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for entry in kb.parse("\n".join(lines)):
            body = "\n".join(lines[entry.start:entry.end])
            searchable = (path.stem + "\n" + body).casefold()
            if all(term in searchable for term in terms):
                score = sum(3 * (term in entry.heading.casefold()) +
                            2 * (term in " ".join(entry.commands).casefold()) for term in terms)
                matches.append(dict(path=path, line=entry.start + 1, heading=entry.heading,
                                    commands=entry.commands, body=body, score=score))
    return sorted(matches, key=lambda item: (-item["score"], str(item["path"]), item["line"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--topic", default="", help="filter by topic filename")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--full", action="store_true", help="show complete matching entries")
    args = parser.parse_args()
    matches = search(cfg.kb_dir(), " ".join(args.keywords), args.topic)
    for match in matches[:max(0, args.limit)]:
        print("%s:%s - %s" % (match["path"], match["line"], match["heading"]))
        print(match["body"] if args.full else "\n".join("  " + cmd for cmd in match["commands"]))
        print()
    print("%d matching entries; showing %d." % (len(matches), min(len(matches), max(0, args.limit))))


if __name__ == "__main__":
    main()
