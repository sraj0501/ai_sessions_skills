#!/usr/bin/env python3
"""One distillation pass: turn the capture queue into knowledge-base entries.

Runs the first available writer backend (devin, claude, codex, copilot,
opencode, cursor-agent) as an isolated agent session inside the knowledge-base
directory, verifies that every queued signature ended up documented, then
commits.

No shell is involved: the backend is invoked as an argv list, so quoting works
identically on Windows, macOS and Linux.

    distill.py            # write whatever is queued
    AI_SKILLS_WRITER=claude distill.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg      # noqa: E402
import procs    # noqa: E402

SIG_RE = re.compile(r"<!--\s*sig:\s*([0-9a-f]{6,40})\s*-->")


def log(runtime: Path, message: str) -> None:
    line = "[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), message)
    with (runtime / "distill.log").open("a", encoding="utf-8") as fh:
        fh.write(line)


def read_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def write_records(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records),
                    encoding="utf-8")


def build_prompt(kb: Path, runtime: Path, count: int) -> Path:
    template = (cfg.TOOL_ROOT / "prompts" / "DISTILL_PROMPT.md").read_text(encoding="utf-8")
    existing = sorted(p.name for p in kb.glob("*.md"))
    prompt = runtime / "prompt.md"
    prompt.write_text(
        template
        + "\n## This run\n\n"
        + "- Knowledge-base directory (your working directory): `%s`\n" % kb
        + "- Batch file: `.runtime/batch.jsonl` (%d records)\n" % count
        + "- Knowledge-base files that already exist:\n"
        + "".join("  - `%s`\n" % name for name in existing)
        + "\nProcess every record in the batch file, then reply with one line:\n"
        + "`distilled: <n> new entries, <n> merged, <n> skipped`.\n",
        encoding="utf-8")
    return prompt


def run_backend(backend: dict, prompt: Path, kb: Path, timeout: int, runtime: Path) -> int:
    text = prompt.read_text(encoding="utf-8")
    argv = [backend["bin"]] + [a.replace("{prompt_text}", text) for a in backend["args"]]
    env = {"AI_SKILLS_DISTILLER": "1", "AI_SKILLS_CAPTURE_OFF": "1"}
    stdin_data = text if backend.get("prompt") == "stdin" else None

    merged = dict(os.environ)
    merged.update(env)
    try:
        done = subprocess.run(
            argv, cwd=str(kb), env=merged, timeout=timeout,
            input=stdin_data, capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        log(runtime, "timeout after %ds, writer killed" % timeout)
        return 124
    except FileNotFoundError:
        log(runtime, "writer binary vanished: %s" % backend["bin"])
        return 127

    tail = "\n".join((done.stdout or "").strip().splitlines()[-5:])
    if tail:
        log(runtime, "writer output: " + tail.replace("\n", " | "))
    if done.returncode != 0:
        err = "\n".join((done.stderr or "").strip().splitlines()[-3:])
        if err:
            log(runtime, "writer stderr: " + err.replace("\n", " | "))
    return done.returncode


def undocumented(kb: Path, records: list[dict]) -> int:
    docs = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in kb.glob("*.md"))
    have = set(SIG_RE.findall(docs))
    return sum(1 for r in records if r.get("sig") not in have)


def git(kb: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(kb), capture_output=True, text=True)


def dirty_paths(kb: Path) -> set[str]:
    """Every path with uncommitted content, staged or not, tracked or not.

    NUL-separated so paths with spaces or non-ASCII survive intact; gitignored
    files (notably `.runtime/`) stay excluded.
    """
    done = git(kb, "status", "--porcelain", "-z", "--untracked-files=all")
    if done.returncode != 0:
        return set()
    fields = (done.stdout or "").split("\0")
    paths, i = set(), 0
    while i < len(fields):
        entry, i = fields[i], i + 1
        if len(entry) < 4:
            continue
        status, path = entry[:2], entry[3:]
        paths.add(path)
        if "R" in status or "C" in status:   # rename/copy: source follows as its own field
            if i < len(fields):
                paths.add(fields[i])
                i += 1
    return paths


def commit(kb: Path, runtime: Path, count: int, backend_name: str,
           preexisting: set[str] | None = None) -> None:
    """Commit only what the writer changed.

    Anything already dirty before the writer ran is the user's work in progress
    and is left alone. A path dirty on both sides is genuinely ambiguous — the
    two edits are interleaved in one file — so it is reported and skipped rather
    than guessed at.
    """
    if cfg.get("auto_commit", True) is not True:
        return
    if git(kb, "rev-parse", "--git-dir").returncode != 0:
        return

    preexisting = set() if preexisting is None else preexisting
    now = dirty_paths(kb)
    ours = sorted(now - preexisting)
    entangled = sorted(now & preexisting)

    if entangled:
        shown = ", ".join(entangled[:5]) + (" ..." if len(entangled) > 5 else "")
        log(runtime, "left %d pre-existing change(s) uncommitted: %s" % (len(entangled), shown))
    if not ours:
        log(runtime, "nothing of ours to commit")
        return

    git(kb, "add", "--", *ours)
    # --only commits exactly these paths, so anything the user had staged stays staged.
    done = git(kb, "commit", "-q", "--only",
               "-m", "docs: document %d captured action(s)" % count,
               "-m", "Written automatically by the ai-session-skills writer (%s)." % backend_name,
               "--", *ours)
    if done.returncode != 0:
        err = "\n".join((done.stderr or done.stdout or "").strip().splitlines()[-2:])
        log(runtime, "commit failed: " + (err.replace("\n", " | ") or "unknown error"))
        return
    log(runtime, "committed %d action(s) across %d file(s)" % (count, len(ours)))

    if cfg.get("auto_push", False) is True and git(kb, "remote", "get-url", "origin").returncode == 0:
        if git(kb, "push", "-q").returncode == 0:
            log(runtime, "pushed to origin")


def main() -> int:
    kb, runtime = cfg.kb_dir(), cfg.runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "failed").mkdir(exist_ok=True)

    pending, batch = runtime / "pending.jsonl", runtime / "batch.jsonl"
    attempts_file = runtime / "batch.attempts"
    timeout = int(cfg.get("distill.timeout_seconds", 900) or 900)
    max_attempts = int(cfg.get("distill.max_attempts", 3) or 3)
    max_records = int(cfg.get("distill.max_batch_records", 40) or 40)

    backend = cfg.writer_backend()
    if not backend:
        log(runtime, "no writer backend available "
                     "(install devin, claude, codex, copilot, opencode or cursor-agent)")
        return 0

    lock = procs.DirLock(runtime / "distill.lock", stale_after=timeout * 2)
    if not lock.acquire():
        return 0
    try:
        # Carry over a previously failed batch, then take newly pending records.
        records = read_records(batch)
        queued = read_records(pending)
        take = max(0, max_records - len(records))
        records += queued[:take]
        leftover = queued[take:]
        if not records:
            batch.unlink(missing_ok=True)
            return 0
        write_records(batch, records)
        write_records(pending, leftover)

        attempt = 1
        try:
            attempt = int(attempts_file.read_text().strip()) + 1
        except Exception:
            pass
        attempts_file.write_text(str(attempt), encoding="utf-8")
        log(runtime, "distilling %d record(s), attempt %d, backend %s"
            % (len(records), attempt, backend["name"]))

        prompt = build_prompt(kb, runtime, len(records))
        preexisting = dirty_paths(kb)   # the user's work in progress; not ours to commit
        status = run_backend(backend, prompt, kb, timeout, runtime)

        missing = undocumented(kb, records) if status == 0 else None
        if status == 0:
            log(runtime, "writer finished; undocumented signatures: %d" % missing)

        if status != 0 or missing:
            log(runtime, "distillation incomplete (exit=%s undocumented=%s)"
                % (status, "n/a" if missing is None else missing))
            if attempt >= max_attempts:
                stamp = time.strftime("%Y%m%d-%H%M%S")
                batch.replace(runtime / "failed" / ("batch-%s.jsonl" % stamp))
                attempts_file.unlink(missing_ok=True)
                subprocess.run(procs.python_argv(cfg.TOOL_ROOT / "bin" / "sync_seen.py"),
                               capture_output=True)
                log(runtime, "gave up after %d attempts; batch parked in "
                             "failed/batch-%s.jsonl and signatures released" % (attempt, stamp))
            return 0

        batch.unlink(missing_ok=True)
        attempts_file.unlink(missing_ok=True)
        subprocess.run(procs.python_argv(cfg.TOOL_ROOT / "bin" / "sync_seen.py"),
                       capture_output=True)
        commit(kb, runtime, len(records), backend["name"], preexisting)
        log(runtime, "done")
        return 0
    finally:
        lock.release()


if __name__ == "__main__":
    raise SystemExit(main())
