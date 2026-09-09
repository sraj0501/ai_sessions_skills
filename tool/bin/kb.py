#!/usr/bin/env python3
"""Deterministic knowledge-base mechanics.

Everything the writer model used to be trusted with — routing a record to a
file, deciding whether an action is already documented, placing an entry under
the right heading, keeping `sig` comments intact — happens here instead, in
plain Python.

That leaves the model one job: turn a single record into a few lines of prose.
A small local model can do that; none of it requires tool use, file access or
multi-step planning.

    kb.py routes                     # where each binary is filed, and why
    kb.py route <binary> <file.md>   # correct a decision, permanently
    kb.py merge <from.md> <to.md>    # move entries, signatures intact
    kb.py sigs                       # every documented signature
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capture  # noqa: E402
import cfg      # noqa: E402

SIG_RE = re.compile(r"<!--\s*sig:\s*([0-9a-f]{6,40})\s*-->")
HEADING_RE = re.compile(r"^###\s+(.*?)\s*$")
SECTION_RE = re.compile(r"^##\s+(?!#)(.*?)\s*$")
FENCE_RE = re.compile(r"^```")

DEFAULT_SECTION = "Other"
SKIPPED_FILE = "_skipped.md"

# --------------------------------------------------------------------------- #
# routing: binary -> file
# --------------------------------------------------------------------------- #
# There is no table of known commands. A fixed list always lags what is
# actually run: `grep.md` and `timeout.md` exist in this repo because those
# binaries were seen before anyone thought to add them to the list. Instead the
# knowledge base is its own routing table, and anything genuinely new is
# classified once by the model and remembered.
ROUTES_FILE = ".routes.json"
BINARY_RE = re.compile(r"^[a-z0-9][a-z0-9._+-]*$")


def safe_filename(name: str) -> str:
    """A markdown filename that cannot escape the knowledge base.

    Applied to every route, including ones a model proposes, so a suggested
    path can never traverse or land outside the directory.
    """
    stem = re.sub(r"[^a-z0-9._-]", "-", str(name or "").lower().strip())
    stem = stem[:-3] if stem.endswith(".md") else stem
    stem = stem.strip("-.") or "misc"
    return "%s.md" % stem


def title_of(kb: Path, filename: str) -> str:
    """The `# Heading` of a knowledge-base file, for reuse and for prompts."""
    path = kb / filename
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return filename[:-3].replace("-", " ").title()


def binary_index(kb: Path) -> dict[str, str]:
    """Which file already documents each binary, derived from the entries.

    This is what makes routing self-correcting: once `git status` lives in
    git.md, every other git command follows it without anyone maintaining a
    list.
    """
    index: dict[str, str] = {}
    for path in sorted(kb.glob("*.md")):
        if path.name in (SKIPPED_FILE, "README.md"):
            continue
        for entry in parse(path.read_text(encoding="utf-8", errors="replace")):
            action = action_of(entry)
            # Command blocks contain prose fragments and placeholders too, so
            # only plausible binary names are allowed to define a route.
            if action and BINARY_RE.match(action[0]) and action[0] not in index:
                index[action[0]] = path.name
    return index


def load_routes(kb: Path) -> dict[str, str]:
    """Remembered decisions, so a binary is classified at most once."""
    try:
        data = json.loads((kb / ROUTES_FILE).read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in data.items()} if isinstance(data, dict) else {}
    except Exception:
        return {}


def remember_route(kb: Path, binary: str, filename: str) -> None:
    if not binary or not BINARY_RE.match(binary):
        return
    routes = load_routes(kb)
    if routes.get(binary) == filename:
        return
    routes[binary] = filename
    (kb / ROUTES_FILE).write_text(json.dumps(dict(sorted(routes.items())), indent=2) + "\n",
                                  encoding="utf-8")


def known_route(record: dict, kb: Path) -> tuple[str, str] | None:
    """Where this binary already belongs, or None if it has never been seen."""
    binary = str(record.get("binary") or "").lower()
    if not binary:
        return None
    filename = binary_index(kb).get(binary) or load_routes(kb).get(binary)
    return (filename, title_of(kb, filename)) if filename else None


def fallback_route(record: dict) -> tuple[str, str]:
    """Last resort when no classifier is available: a file of its own."""
    binary = str(record.get("binary") or "").lower()
    filename = safe_filename(binary)
    return filename, (binary or "Misc")


# --------------------------------------------------------------------------- #
# entry parsing
# --------------------------------------------------------------------------- #
class Entry:
    """One `###` block: its heading, sig comments, command lines and extent."""

    def __init__(self, heading: str, section: str, start: int, end: int,
                 sigs: list[str], commands: list[str], sig_end: int):
        self.heading = heading
        self.section = section
        self.start = start          # index of the '### ' line
        self.end = end              # exclusive
        self.sigs = sigs
        self.commands = commands
        self.sig_end = sig_end      # index after the last sig line (insert point)

    def __repr__(self) -> str:      # pragma: no cover - debugging aid
        return "<Entry %r sigs=%d>" % (self.heading, len(self.sigs))


def parse(text: str) -> list[Entry]:
    """Every `###` entry in a knowledge-base file, in document order."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if HEADING_RE.match(line)]
    entries = []
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        section = DEFAULT_SECTION
        for i in range(start - 1, -1, -1):
            found = SECTION_RE.match(lines[i])
            if found:
                section = found.group(1)
                break
        sigs, sig_end = [], start + 1
        for i in range(start + 1, end):
            if SIG_RE.search(lines[i]):
                sigs.append(SIG_RE.search(lines[i]).group(1))
                sig_end = i + 1
            elif lines[i].strip():
                break
        entries.append(Entry(HEADING_RE.match(lines[start]).group(1), section,
                             start, end, sigs, _fenced(lines[start:end]), sig_end))
    return entries


def _fenced(block: list[str]) -> list[str]:
    """Command lines inside the first fenced code block of an entry."""
    out, inside = [], False
    for line in block:
        if FENCE_RE.match(line.strip()):
            if inside:
                break
            inside = True
            continue
        if inside and line.strip():
            out.append(line.strip())
    return out


def action_of(entry: Entry) -> tuple[str, tuple[str, ...]] | None:
    """(binary, subcommands) an entry documents, derived from its command block."""
    for line in entry.commands:
        for tokens in capture.tokenize(line):
            result = capture.signature(tokens)
            if result:
                return result[1], tuple(result[2])
    return None


def find_match(entries: list[Entry], binary: str, subcmds: list[str]) -> Entry | None:
    """An existing entry for the same binary + subcommands, if any.

    A different mix of flags on the same action is a variant, not a new entry,
    so it merges into the entry already documenting it.
    """
    want = (binary.lower(), tuple(subcmds))
    for entry in entries:
        if action_of(entry) == want:
            return entry
    return None


def canonical_section(name: str, existing: list[str]) -> str:
    """Snap a proposed section onto an existing one when it means the same.

    Models coin "Stashing and cleanup" next to "Stashing and saving work".
    Case-insensitive equality catches most of it; close matching catches the
    rest without blocking a genuinely new group.
    """
    name = (name or "").strip().strip("#").strip() or DEFAULT_SECTION
    for section in existing:
        if section.lower() == name.lower():
            return section
    close = difflib.get_close_matches(name.lower(), [s.lower() for s in existing],
                                      n=1, cutoff=0.82)
    if close:
        return next(s for s in existing if s.lower() == close[0])
    return name


def render_entry(fields: dict, sig: str) -> str:
    """Build the markdown for an entry from validated fields.

    The model supplies prose only; layout, ordering, fencing and the sig
    comment are produced here, so no model can emit a malformed entry.
    """
    commands = [c.rstrip() for c in fields.get("commands") or [] if c.strip()]
    lines = ["### %s" % fields["heading"].strip(),
             "<!-- sig: %s -->" % sig,
             "",
             "```bash",
             *commands,
             "```",
             ""]
    for label, key in (("What it does", "what"), ("Why", "why"),
                       ("Example", "example"), ("Notes", "notes")):
        value = " ".join(str(fields.get(key) or "").split())
        if value:
            lines.append("- **%s:** %s" % (label, value))
    return "\n".join(lines)


def sections(text: str) -> list[str]:
    """Existing `##` group headings, in document order, deduplicated."""
    out = []
    for line in text.splitlines():
        found = SECTION_RE.match(line)
        if found and found.group(1) not in out:
            out.append(found.group(1))
    return out


def documented_sigs(kb: Path) -> set[str]:
    sigs: set[str] = set()
    for path in sorted(kb.glob("*.md")):
        sigs.update(SIG_RE.findall(path.read_text(encoding="utf-8", errors="replace")))
    return sigs


# --------------------------------------------------------------------------- #
# mutation
# --------------------------------------------------------------------------- #
FILE_HEADER = ("# %s\n\n"
               "> Auto-maintained by the ai_session_skills background writer. One `###` entry\n"
               "> per distinct action. `sig` comments are dedupe keys — never delete them.\n")


def _write(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")


def add_sig(path: Path, sig: str, heading: str) -> bool:
    """Attach another signature to the entry with this heading."""
    lines = path.read_text(encoding="utf-8").splitlines()
    for entry in parse("\n".join(lines)):
        if entry.heading == heading:
            if sig in entry.sigs:
                return False
            lines.insert(entry.sig_end, "<!-- sig: %s -->" % sig)
            _write(path, lines)
            return True
    return False


def insert_entry(path: Path, title: str, section: str, body: str) -> None:
    """Place a rendered entry at the end of its section, creating both if absent."""
    if not path.exists():
        path.write_text(FILE_HEADER % title, encoding="utf-8")
    lines = path.read_text(encoding="utf-8").splitlines()

    target = None
    for i, line in enumerate(lines):
        found = SECTION_RE.match(line)
        if found and found.group(1).strip().lower() == section.strip().lower():
            target = i
            break

    block = body.rstrip("\n").splitlines()
    if target is None:
        lines += ["", "## %s" % section, ""] + block
    else:
        end = len(lines)
        for i in range(target + 1, len(lines)):
            if SECTION_RE.match(lines[i]):
                end = i
                break
        while end > target + 1 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = [""] + block
    _write(path, lines)


def note_skipped(kb: Path, sig: str, command: str, reason: str) -> None:
    path = kb / SKIPPED_FILE
    if not path.exists():
        path.write_text("# Skipped\n\n> Actions judged too trivial or "
                        "non-reusable to document as knowledge-base entries.\n",
                        encoding="utf-8")
    with path.open("a", encoding="utf-8") as fh:
        fh.write("\n### %s\n<!-- sig: %s -->\n\n%s\n" % (command.strip()[:100], sig, reason.strip()))


def ensure_readme_row(kb: Path, filename: str, title: str) -> None:
    """Add a row for a newly created file to the README table, if there is one."""
    readme = kb / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    if "(%s)" % filename in text or "`%s`" % filename in text:
        return
    lines = text.splitlines()
    last = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and filename.rsplit(".", 1)[0] not in line:
            last = i
    if last is None:
        return
    lines.insert(last + 1, "| [`%s`](%s) | %s |" % (filename, filename, title))
    readme.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")


def merge_file(kb: Path, source: str, dest: str) -> int:
    """Move every entry from one file into another, signatures intact.

    Used to undo a bad routing decision after the fact: the entries move, the
    `sig` comments come with them, so nothing is re-documented.
    """
    src, dst = kb / safe_filename(source), kb / safe_filename(dest)
    if not src.exists() or src == dst:
        return 0
    lines = src.read_text(encoding="utf-8", errors="replace").splitlines()
    entries = parse("\n".join(lines))
    title = title_of(kb, dst.name)
    for entry in entries:
        insert_entry(dst, title, entry.section,
                     "\n".join(lines[entry.start:entry.end]).strip())
    src.unlink()
    for binary, filename in load_routes(kb).items():
        if filename == src.name:
            remember_route(kb, binary, dst.name)
    for entry in entries:
        action = action_of(entry)
        if action:
            remember_route(kb, action[0], dst.name)
    readme = kb / "README.md"
    if readme.exists():
        kept = [ln for ln in readme.read_text(encoding="utf-8").splitlines()
                if src.name not in ln]
        readme.write_text("\n".join(kept).rstrip("\n") + "\n", encoding="utf-8")
    return len(entries)


def main(argv: list[str]) -> int:
    kb = cfg.kb_dir()
    if not argv:
        print(__doc__)
        return 0
    verb = argv[0]
    if verb == "routes":
        index, saved = binary_index(kb), load_routes(kb)
        for binary in sorted(set(index) | set(saved)):
            where = index.get(binary) or saved[binary]
            print("%-18s %-24s %s" % (binary, where,
                                      "from entries" if binary in index else "remembered"))
    elif verb == "route" and len(argv) >= 3:
        remember_route(kb, argv[1].lower(), safe_filename(argv[2]))
        print("%s -> %s (future entries; use `merge` to move existing ones)"
              % (argv[1], safe_filename(argv[2])))
    elif verb == "merge" and len(argv) >= 3:
        moved = merge_file(kb, argv[1], argv[2])
        print("moved %d entr%s: %s -> %s"
              % (moved, "y" if moved == 1 else "ies", argv[1], argv[2]))
    elif verb == "sigs":
        for sig in sorted(documented_sigs(kb)):
            print(sig)
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
