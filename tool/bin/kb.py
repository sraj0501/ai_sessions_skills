#!/usr/bin/env python3
"""Deterministic knowledge-base mechanics.

Everything the writer model used to be trusted with — routing a record to a
file, deciding whether an action is already documented, placing an entry under
the right heading, keeping `sig` comments intact — happens here instead, in
plain Python.

That leaves the model one job: turn a single record into a few lines of prose.
A small local model can do that; none of it requires tool use, file access or
multi-step planning.

    kb.py route '{"binary": "git", "subcommands": ["merge"]}'
    kb.py sigs                     # every documented signature
"""

from __future__ import annotations

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
SHELL_BINS = {
    "rg", "grep", "sed", "awk", "find", "ls", "cat", "head", "tail", "jq", "yq",
    "curl", "wget", "xargs", "chmod", "chown", "sort", "uniq", "wc", "cut", "tr",
    "echo", "printf", "mkdir", "rm", "cp", "mv", "ln", "tar", "zip", "unzip",
    "ssh", "scp", "rsync", "df", "du", "ps", "kill", "pkill", "stat", "touch",
    "diff", "tee", "which", "env", "date", "sleep", "openssl", "base64", "shasum",
    "md5sum", "seq", "basename", "dirname", "realpath", "readlink", "file",
    "watch", "xxd", "column", "nl", "rev", "shuf", "split", "tree", "lsof",
    "netstat", "ping", "dig", "host", "nc", "sudo", "open", "pbcopy", "pbpaste",
    "bash", "sh", "zsh", "fish", "dash", "source", "time", "timeout",
}
AGENT_BINS = {"devin", "claude", "codex", "copilot", "opencode", "cursor-agent", "aider"}
# Agent tools with no shell equivalent — these alone belong in agent-tools.md.
AGENT_ONLY = {"edit", "write", "apply_patch", "notebook_edit", "multiedit", "str_replace"}

ROUTES: list[tuple[set[str], str, str]] = [
    ({"git", "jj", "hg", "svn"}, "git.md", "Git"),
    ({"gh", "glab"}, "github-cli.md", "GitHub CLI"),
    ({"docker", "docker-compose", "podman", "nerdctl"}, "docker.md", "Docker"),
    ({"kubectl", "helm", "k9s", "kustomize", "minikube"}, "kubernetes.md", "Kubernetes"),
    ({"npm", "npx", "yarn", "pnpm", "bun", "node", "tsc", "vitest", "jest",
      "eslint", "prettier"}, "node.md", "Node"),
    ({"python", "python3", "py", "pip", "pip3", "uv", "poetry", "pytest", "ruff",
      "mypy", "black", "flake8"}, "python.md", "Python"),
    ({"psql", "mysql", "sqlite3", "redis-cli", "influx", "mongosh"}, "database.md", "Databases"),
    ({"az", "aws", "gcloud", "terraform", "pulumi"}, "cloud.md", "Cloud"),
    (SHELL_BINS, "shell.md", "Shell"),
    (AGENT_BINS, "agent-tools.md", "Agent tools"),
]


def route(record: dict) -> tuple[str, str]:
    """(filename, human title) for a record. Never guesses a new name twice."""
    binary = str(record.get("binary") or "").lower()
    tool = str(record.get("tool") or "").lower()
    if binary in AGENT_ONLY or (not binary and tool in AGENT_ONLY):
        return "agent-tools.md", "Agent tools"
    for bins, filename, title in ROUTES:
        if binary in bins:
            return filename, title
    safe = re.sub(r"[^a-z0-9._-]", "-", binary).strip("-") or "misc"
    return "%s.md" % safe, binary or "Misc"


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


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 0
    if argv[0] == "route":
        print("\t".join(route(json.loads(argv[1]))))
    elif argv[0] == "sigs":
        for sig in sorted(documented_sigs(cfg.kb_dir())):
            print(sig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
