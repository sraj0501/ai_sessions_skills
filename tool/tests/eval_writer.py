#!/usr/bin/env python3
"""Score the writer's output quality, so prompt changes can be compared.

Runs a fixed set of representative records through the real text-mode
pipeline into a throwaway knowledge base, then grades every entry against
checks that need no judge model:

  format      parses back into a well-formed entry
  heading     names the task, not the command (no binary name, no flags)
  concise     "what"/"why" stay within the length budget
  grounded    every flag mentioned appears in the captured command
  clean       no absolute personal paths, no leaked tokens

`grounded` is the accuracy proxy: small models invent plausible flags, and
that is the failure that quietly poisons a reference manual.

    python3 tool/tests/eval_writer.py                  # default backend
    python3 tool/tests/eval_writer.py --backend devin  # cloud comparison
    python3 tool/tests/eval_writer.py --verbose
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import cfg      # noqa: E402
import distill  # noqa: E402
import kb       # noqa: E402

# (binary, subcommands, command, concrete details the entry ought to mention)
CASES = [
    ("git", ["merge"], "git merge --no-ff --no-edit upstream/staging", ["upstream/staging"]),
    ("git", ["log"], "git --no-pager log --oneline -20 --graph", ["20"]),
    ("docker", ["compose", "up"], "docker compose up -d --build", ["build"]),
    ("npm", ["run"], "npm run test -- --coverage", ["coverage"]),
    ("rg", [], "rg -n --glob '*.ts' -C 2 useEffect", ["*.ts", ".ts", "typescript"]),
    ("kubectl", ["get"], "kubectl get pods -n prod -o wide", ["prod"]),
    ("sed", [], "sed -i '' 's/foo/bar/g' README.md", ["README.md", "readme"]),
    ("curl", [], "curl -fsSL -H 'Accept: application/json' https://api.example.com/v1/status",
     ["json"]),
]

FLAG_RE = re.compile(r"(?<![\w-])(--?[A-Za-z][\w-]*)")
SECRETISH = re.compile(r"/Users/[^\s`)]+|ghp_[A-Za-z0-9]+|Bearer\s+[A-Za-z0-9._-]{8,}")
WORD_BUDGET = 45


def records():
    for n, (binary, subcmds, command, wanted) in enumerate(CASES):
        yield {"sig": "%012d" % n, "binary": binary, "subcommands": subcmds,
               "command": command, "full_command": command, "tool": "exec",
               "ok": True, "kind": "shell", "harness": "eval", "_wanted": wanted}


def expand_flags(command: str) -> set[str]:
    """Flags in a command, with bundled short flags split out.

    `curl -fsSL` really does use -f, -s, -S and -L, so an entry explaining
    them individually is grounded, not inventing.
    """
    flags = set(FLAG_RE.findall(command))
    for flag in list(flags):
        if not flag.startswith("--") and len(flag) > 2:
            flags.update("-" + ch for ch in flag[1:])
    return flags


def bullet(entry_text: str, label: str) -> str:
    found = re.search(r"^-\s+\*\*%s:?\*\*\s*(.+)$" % label, entry_text, re.M | re.I)
    return found.group(1).strip() if found else ""


def grade(record: dict, entry: kb.Entry, text: str) -> dict:
    heading = entry.heading
    binary = record["binary"]
    what, why = bullet(text, "What it does"), bullet(text, "Why")

    # heading should name the task, not restate the command
    head_low = heading.lower()
    heading_ok = (not head_low.startswith(binary)
                  and "--" not in heading
                  and not re.search(r"`[^`]+`", heading)
                  and len(heading.split()) >= 3)

    concise = bool(what) and bool(why) and len(what.split()) <= WORD_BUDGET \
        and len(why.split()) <= WORD_BUDGET

    # every flag the entry claims must exist in the captured command
    claimed = set(FLAG_RE.findall(text)) - {"-"}
    invented = sorted(claimed - expand_flags(record["command"]))

    # a good entry names the concrete thing acted on, not just the verb
    prose = " ".join([heading, what, why]).lower()
    specific = any(want.lower() in prose for want in record.get("_wanted", []))

    return {
        "format": bool(entry.commands) and bool(what),
        "heading": heading_ok,
        "concise": concise,
        "grounded": not invented,
        "specific": specific,
        "clean": not SECRETISH.search(text),
        "invented": invented,
        "heading_text": heading,
        "lines": len(text.strip().splitlines()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", default=None, help="force a writer backend")
    parser.add_argument("--limit", type=int, default=len(CASES))
    parser.add_argument("--verbose", action="store_true")
    opts = parser.parse_args()

    if opts.backend:
        import os
        os.environ["AI_SKILLS_WRITER"] = opts.backend
    backend = cfg.writer_backend("text")
    if not backend:
        print("no text backend available")
        return 1

    tmp = Path(tempfile.mkdtemp(prefix="kbeval-"))
    runtime = tmp / ".runtime"
    runtime.mkdir()
    print("backend: %s  model: %s" % (backend["name"], backend.get("model") or "-"))
    print("kb:      %s\n" % tmp)

    checks = ["format", "heading", "concise", "grounded", "specific", "clean"]
    totals = dict.fromkeys(checks, 0)
    scored = 0
    started = time.time()

    for record in list(records())[:opts.limit]:
        outcome = distill.document_record(tmp, runtime, record, backend, 180)
        path = tmp / kb.route(record)[0]
        entry = next((e for e in kb.parse(path.read_text(encoding="utf-8"))
                      if record["sig"] in e.sigs), None) if path.exists() else None
        if entry is None:
            print("  %-9s %-12s -> %s (no entry)" % (record["binary"], outcome, "FAIL"))
            scored += 1
            continue
        text = "\n".join(path.read_text(encoding="utf-8").splitlines()[entry.start:entry.end])
        result = grade(record, entry, text)
        scored += 1
        for key in checks:
            totals[key] += bool(result[key])
        flags = "".join("." if result[k] else "X" for k in checks)
        print("  %-9s %s  %s" % (record["binary"], flags, result["heading_text"][:58]))
        if opts.verbose and result["invented"]:
            print("            invented flags: %s" % ", ".join(result["invented"]))
        if opts.verbose:
            print("            " + text.replace("\n", "\n            ")[:900])

    elapsed = time.time() - started
    print("\n  checks: %s" % " ".join(checks))
    print("  score : %s" % "  ".join("%s %d/%d" % (k, totals[k], scored) for k in checks))
    print("  total : %d/%d  (%.0f%%)  in %.0fs"
          % (sum(totals.values()), scored * len(checks),
             100.0 * sum(totals.values()) / max(1, scored * len(checks)), elapsed))
    shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
