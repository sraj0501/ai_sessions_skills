"""Search documented entries: python tool/bin/search.py git branch"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg
import kb
import team_sync
import vector_cache


def entries(root: Path, topic: str = "") -> list[dict]:
    """Read all entries for semantic retrieval, retaining exact source lines."""
    matches = []
    for path in sorted(root.glob("*.md")):
        if path.name.startswith("_") or path.name == "README.md":
            continue
        if topic and topic.casefold() not in path.stem.casefold():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for entry in kb.parse("\n".join(lines)):
            matches.append(dict(path=path, line=entry.start + 1, heading=entry.heading,
                                commands=entry.commands,
                                body="\n".join(lines[entry.start:entry.end])))
    return matches


def _team_paths(root: Path) -> list[Path]:
    team = team_sync.team_root()
    revision = team_sync.installed_revision(team)
    return ([team / "revisions" / revision] if revision else []) + [root]


def entries_with_team(root: Path, topic: str = "") -> list[dict]:
    seen = set()
    results = []
    for path in _team_paths(root):
        for item in entries(path, topic):
            sigs = tuple(kb.SIG_RE.findall(item["body"]))
            key = sigs[0] if sigs else (item["heading"], tuple(item["commands"]))
            if key not in seen:
                seen.add(key)
                results.append(item)
    return results


def semantic_search_with_team(root: Path, query: str, topic: str = "",
                              limit: int = 5) -> list[dict]:
    """Required embeddings with keyword ranking for exact command matches."""
    candidates = entries_with_team(root, topic)
    if not candidates:
        return []
    keyed = {f"{item['path'].resolve()}:{item['line']}": item for item in candidates}
    words = [word for word in query.casefold().split() if word not in
             {"how", "what", "where", "when", "why", "the", "and", "for", "with",
              "can", "you", "does", "this", "that", "from"}]
    def lexical_score(key: str) -> tuple[int, int]:
        item = keyed[key]
        heading = item["heading"].casefold()
        commands = " ".join(item["commands"]).casefold()
        body = item["body"].casefold()
        coverage = sum(word in (heading + " " + commands + " " + body)
                       for word in words)
        score = sum(3 * (word in heading) + 2 * (word in commands) +
                    (word in body) for word in words)
        return coverage, score
    lexical = sorted((key for key in keyed if words and
                      lexical_score(key)[0] >= min(2, len(words))),
                     key=lambda key: (tuple(-value for value in lexical_score(key)), key))
    records = [(key, item["path"].stem + "\n" + item["heading"] + "\n" +
                "\n".join(item["commands"]) + "\n" +
                kb.SIG_RE.sub("", item["body"]))
               for key, item in keyed.items()]
    ranked = vector_cache.rank(cfg.runtime_dir() / "knowledge-vectors.sqlite3",
                               records, query, limit, lexical)
    return [keyed[key] for key in ranked]


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


def search_with_team(root: Path, query: str, topic: str = "") -> list[dict]:
    """Search the installed shared revision and local entries, preferring shared duplicates."""
    team = team_sync.team_root()
    revision = team_sync.installed_revision(team)
    paths = ([team / "revisions" / revision] if revision else []) + [root]
    seen = set()
    results = []
    for path in paths:
        for match in search(path, query, topic):
            sigs = tuple(kb.SIG_RE.findall(match["body"]))
            key = sigs[0] if sigs else (match["heading"], tuple(match["commands"]))
            if key not in seen:
                seen.add(key)
                results.append(match)
    return sorted(results, key=lambda item: (-item["score"], str(item["path"]), item["line"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--topic", default="", help="filter by topic filename")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--full", action="store_true", help="show complete matching entries")
    args = parser.parse_args()
    matches = search_with_team(cfg.kb_dir(), " ".join(args.keywords), args.topic)
    for match in matches[:max(0, args.limit)]:
        print("%s:%s - %s" % (match["path"], match["line"], match["heading"]))
        print(match["body"] if args.full else "\n".join("  " + cmd for cmd in match["commands"]))
        print()
    print("%d matching entries; showing %d." % (len(matches), min(len(matches), max(0, args.limit))))


if __name__ == "__main__":
    main()
