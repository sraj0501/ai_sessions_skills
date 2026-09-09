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
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg      # noqa: E402
import kb       # noqa: E402
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
    template = template.replace(".runtime/", runtime.as_posix().rstrip("/") + "/")
    existing = sorted(p.name for p in kb.glob("*.md"))
    prompt = runtime / "prompt.md"
    prompt.write_text(
        template
        + "\n## This run\n\n"
        + "- Knowledge-base directory (your working directory): `%s`\n" % kb
        + "- Batch file: `%s` (%d records)\n" % ((runtime / "batch.jsonl").as_posix(), count)
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
        done = procs.run(
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


# --------------------------------------------------------------------------- #
# text mode: Python owns the knowledge base, the model only writes prose
# --------------------------------------------------------------------------- #
FENCE_ONLY = re.compile(r"^```[a-zA-Z]*\s*$")
SKIP_RE = re.compile(r"^\s*SKIP\s*:\s*(.+)$", re.MULTILINE)
SECTION_LINE = re.compile(r"^\s*SECTION\s*:\s*(.+)$", re.MULTILINE)


def entry_prompt(record: dict, existing_sections: list[str] | None = None) -> str:
    template = (cfg.TOOL_ROOT / "prompts" / "ENTRY_PROMPT.md").read_text(encoding="utf-8")
    lines = [template, "\n## Now document this command\n",
             "Command: `%s`" % record.get("command", "")]
    if existing_sections:
        lines.append("\nUse one of these existing `section` values **exactly** if the "
                     "command fits; only invent a new one if none do:\n"
                     + "\n".join("- %s" % s for s in existing_sections))
    subcmds = record.get("subcommands") or []
    lines.append("Binary: `%s`%s" % (record.get("binary", ""),
                                     (", subcommands: `%s`" % " ".join(subcmds)) if subcmds else ""))
    full = record.get("full_command") or ""
    if full and full != record.get("command"):
        lines.append("It was part of this command line: `%s`" % full)
    if record.get("ok") is False:
        lines.append("This command FAILED when it was run. Document it anyway and "
                     "note the likely failure mode.")
    lines.append("\nReply with the JSON object now.")
    return "\n".join(lines)


ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
JSON_BLOCK = re.compile(r"\{.*\}", re.S)

# The output contract. Sent to Ollama as `format`, which constrains decoding so
# the reply cannot be anything else; other backends are asked for the same
# shape in the prompt and validated on arrival.
ENTRY_SCHEMA = {
    "type": "object",
    "properties": {
        "worth_documenting": {"type": "boolean"},
        "skip_reason": {"type": "string"},
        "section": {"type": "string"},
        "heading": {"type": "string"},
        "commands": {"type": "array", "items": {"type": "string"}},
        "what": {"type": "string"},
        "why": {"type": "string"},
        "example": {"type": "string"},
        "notes": {"type": "string"},
    },
    "required": ["worth_documenting", "section", "heading", "commands",
                 "what", "why", "example"],
}
REQUIRED_PROSE = ("heading", "what", "why")

# `kind` is answered before `file`, and under constrained decoding the model
# must pick one of the three. Judging what a tool *is* turns out to be much
# more reliable than picking a filename, where a small model just reaches for
# the largest existing bucket -- so Python uses `kind` to police the choice.
ROUTE_KINDS = ("same-ecosystem", "generic-plumbing", "new-technology")
ROUTE_SCHEMA = {
    "type": "object",
    "properties": {
        "kind": {"type": "string", "enum": list(ROUTE_KINDS)},
        "file": {"type": "string"},
        "title": {"type": "string"},
    },
    "required": ["kind", "file", "title"],
}


def route_prompt(record: dict, choices: list[tuple[str, str, list[str]]]) -> str:
    """Ask which file a never-before-seen command belongs in.

    Each candidate is shown with the commands it already documents: concrete
    evidence beats a title, and it is what makes `pnpm` land beside `npm`.
    """
    listing = "\n".join(
        "- `%s` — %s%s" % (name, title,
                           (" (documents: %s)" % ", ".join(bins[:8])) if bins else "")
        for name, title, bins in choices)
    return (
        "You organise a personal command reference. Each file covers one "
        "technology or family of tools.\n\n"
        "A command was run that the reference does not cover yet:\n\n"
        "    binary:  %s\n    command: %s\n\n"
        "%s\n\n"
        "First decide what kind of tool this is:\n\n"
        "- `same-ecosystem` — a listed file already covers this tool, or "
        "another tool from the same language, runtime or platform. An "
        "ecosystem includes its package managers, test runners, linters and "
        "build tools, which belong with their language rather than with "
        "similar tools from other ecosystems.\n"
        "- `generic-plumbing` — general-purpose Unix work that is tied to no "
        "particular technology: searching, editing, archiving, piping, "
        "permissions, process and file management.\n"
        "- `new-technology` — a specific technology the reference does not "
        "cover yet. A database client, an operating-system package manager, "
        "an init or service system, or an infrastructure tool is always this, "
        "never `generic-plumbing`, even when no listed file fits.\n\n"
        "Then choose `file`:\n\n"
        "- `same-ecosystem` -> the existing file for that ecosystem.\n"
        "- `generic-plumbing` -> the listed general shell/utilities file.\n"
        "- `new-technology` -> a NEW filename, named for the family rather "
        "than this one binary, so related tools can join it later.\n\n"
        "Reply with JSON: {\"kind\": \"...\", \"file\": \"<name>.md\", "
        "\"title\": \"<Heading>\"}. `file` is short and lowercase; `title` is "
        "a human heading of one to three words, never a command line.\n"
        % (record.get("binary", ""), record.get("command", ""),
           ("Existing files:\n" + listing) if listing else "The reference is empty."))


def classify(record: dict, kb_dir: Path, backend: dict, timeout: int,
             runtime: Path) -> tuple[str, str] | None:
    """Decide a home for an unknown binary. Returns None if the model cannot."""
    by_file: dict[str, list[str]] = {}
    for known_binary, filename in sorted(kb.binary_index(kb_dir).items()):
        by_file.setdefault(filename, []).append(known_binary)
    choices = sorted((name, kb.title_of(kb_dir, name), by_file.get(name, []))
                     for name in (p.name for p in kb_dir.glob("*.md"))
                     if name not in (kb.SKIPPED_FILE, "README.md"))
    raw = run_text(backend, route_prompt(record, choices), timeout, runtime, ROUTE_SCHEMA)
    if not raw:
        return None
    found = JSON_BLOCK.search(raw)
    if not found:
        return None
    try:
        reply = json.loads(found.group(0))
    except Exception:
        return None
    # The model suggests; Python decides the actual path.
    if not str(reply.get("file") or "").strip():
        return None
    filename = kb.safe_filename(reply["file"])
    title = " ".join(str(reply.get("title") or "").split())

    # Models sometimes echo the category name back as the filename.
    if filename[:-3] in ROUTE_KINDS:
        filename = kb.safe_filename(title or record.get("binary", ""))

    # Hold it to its own judgement. Saying "this is a technology nothing here
    # covers" and then filing it in the general shell bucket is the failure
    # small models fall into, so that answer is overridden rather than trusted.
    if reply.get("kind") == "new-technology" and (kb_dir / filename).exists():
        derived = kb.safe_filename(title or record.get("binary", ""))
        if not (kb_dir / derived).exists():
            filename = derived

    if (kb_dir / filename).exists():
        # An existing file keeps its own heading: this is choosing a
        # destination, not renaming one.
        return filename, kb.title_of(kb_dir, filename)
    if not title or len(title.split()) > 4 or title.startswith("-") or " -" in title:
        title = kb.title_of(kb_dir, filename)   # a command line is not a title
    return filename, title[:60]


def run_http(backend: dict, prompt: str, timeout: int, runtime: Path,
             schema: dict | None = None) -> str | None:
    """Generate over Ollama's HTTP API.

    Deliberately not `ollama run`: that streams through a terminal renderer
    which re-wraps long lines with cursor-movement escapes, so piped output
    cannot be reconstructed reliably. The API returns the text verbatim.
    """
    payload = {
        "model": backend.get("model") or "",
        "prompt": prompt,
        "stream": False,
        "options": backend.get("options") or {},
    }
    if backend.get("think") is not None:
        # Reasoning models otherwise spend most of their tokens (and time)
        # thinking. Filling a fixed template does not need it.
        payload["think"] = backend["think"]
    if schema:
        # Constrained decoding: the sampler can only emit tokens that keep the
        # output a valid instance of this schema, so format compliance stops
        # depending on how well the model follows instructions.
        payload["format"] = schema
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(backend["url"], data=body,
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            reply = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        log(runtime, "model request failed (%s): %s" % (backend["url"], exc))
        return None

    text = reply.get("response") or ""
    if reply.get("done_reason") == "length" and not text.strip():
        # A reasoning model can burn the whole token budget thinking and emit
        # nothing visible; that is a configuration fault, not a bad record.
        log(runtime, "model hit its token limit before answering "
                     "(raise or remove options.num_predict, or set think=false)")
        return None
    return text


def run_text(backend: dict, prompt: str, timeout: int, runtime: Path,
             schema: dict | None = None) -> str | None:
    """One text-in/text-out generation. No tools, no file access, no cwd needs."""
    if backend.get("url"):
        return run_http(backend, prompt, timeout, runtime, schema)

    mode = backend.get("prompt", "stdin")
    prompt_file = runtime / "entry-prompt.md"
    if mode == "file":                       # some CLIs refuse a prompt on stdin
        prompt_file.write_text(prompt, encoding="utf-8")
    argv = [backend["bin"]] + [a.replace("{prompt_text}", prompt)
                                .replace("{prompt_file}", str(prompt_file))
                               for a in backend["args"]]
    env = dict(os.environ)
    env.update({"AI_SKILLS_DISTILLER": "1", "AI_SKILLS_CAPTURE_OFF": "1"})
    stdin_data = prompt if mode == "stdin" else None
    try:
        done = procs.run(argv, env=env, timeout=timeout, input=stdin_data,
                              capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        log(runtime, "model timed out after %ds" % timeout)
        return None
    except FileNotFoundError:
        log(runtime, "model binary vanished: %s" % backend["bin"])
        return None
    if done.returncode != 0:
        err = "\n".join((done.stderr or "").strip().splitlines()[-2:])
        log(runtime, "model exited %d: %s" % (done.returncode, err.replace("\n", " | ")))
        return None
    return ANSI.sub("", done.stdout or "")


def parse_fields(text: str, command: str) -> tuple[dict | None, str, str]:
    """Model output -> (fields, reason, status).

    status is "ok", "skip" (the model judged the command not worth an entry)
    or "malformed" (the reply was not usable). The caller must not treat those
    last two alike: a skip is a verdict, malformed output is worth retrying
    under a schema.

    Enforces what a schema cannot express: prose is clean, no stray sigs.
    """
    body = (text or "").strip()
    if not body:
        return None, "empty response", "malformed"

    found = JSON_BLOCK.search(body)             # tolerate chatter or a fence around it
    if not found:
        return None, "response was not JSON", "malformed"
    try:
        fields = json.loads(found.group(0))
    except Exception as exc:
        return None, "unparseable JSON (%s)" % exc, "malformed"
    if not isinstance(fields, dict):
        return None, "JSON was not an object", "malformed"

    if fields.get("worth_documenting") is False:
        return None, str(fields.get("skip_reason") or "not worth documenting").strip(), "skip"

    for key in REQUIRED_PROSE:
        if not str(fields.get(key) or "").strip():
            return None, "missing required field: %s" % key, "malformed"

    # Signatures are ours; a model must never supply or influence one.
    for key in ("heading", "what", "why", "example", "notes"):
        if key in fields and isinstance(fields[key], str):
            fields[key] = kb.SIG_RE.sub("", fields[key]).strip()

    heading = " ".join(str(fields["heading"]).split()).strip(" .#`")
    if not heading:
        return None, "empty heading", "malformed"
    fields["heading"] = heading

    commands = [c for c in (fields.get("commands") or []) if str(c).strip()]
    fields["commands"] = [str(c).strip() for c in commands] or [command]
    return fields, "", "ok"


def document_record(kb_dir: Path, runtime: Path, record: dict, backend: dict,
                    timeout: int) -> str:
    """Place one record into the knowledge base. Returns what happened."""
    sig = record.get("sig") or ""
    binary = str(record.get("binary") or "").lower()
    subcmds = list(record.get("subcommands") or [])

    # Where does this belong? What the knowledge base already documents wins;
    # only a genuinely new binary costs a classification call, and the answer
    # is remembered so it is never asked twice.
    target = kb.known_route(record, kb_dir)
    if target is None:
        target = classify(record, kb_dir, backend, timeout, runtime) \
            or kb.fallback_route(record)
        kb.remember_route(kb_dir, binary, target[0])
        cfg.session_log("routed", sig, binary, "-> %s" % target[0], "writer")
    filename, title = target

    path = kb_dir / filename
    is_new_file = not path.exists()

    known_sections: list[str] = []
    if not is_new_file:
        text = path.read_text(encoding="utf-8", errors="replace")
        match = kb.find_match(kb.parse(text), binary, subcmds)
        if match:
            kb.add_sig(path, sig, match.heading)
            return "merged"
        known_sections = kb.sections(text)

    command = record.get("command", "")
    prompt = entry_prompt(record, known_sections)

    # Ask unconstrained first: forcing tokens to satisfy a grammar measurably
    # costs prose quality. Only if the reply is unusable is the schema applied,
    # which makes a well-formed answer the worst case instead of the norm.
    raw = run_text(backend, prompt, timeout, runtime)
    if raw is None:
        # The model was unreachable or errored. That is not a verdict about the
        # record, so leave it undocumented and let the batch retry.
        return "failed"

    fields, reason, status = parse_fields(raw, command)
    if status == "malformed" and ENTRY_SCHEMA and backend.get("url"):
        log(runtime, "reply unusable (%s); retrying under the schema" % reason)
        retry = run_text(backend, prompt, timeout, runtime, ENTRY_SCHEMA)
        if retry is None:
            return "failed"
        fields, reason, status = parse_fields(retry, command)

    if fields is None:
        kb.note_skipped(kb_dir, sig, command, reason)
        return "skipped"

    section = kb.canonical_section(fields.get("section", ""), known_sections)
    kb.insert_entry(path, title, section, kb.render_entry(fields, sig))
    if is_new_file:
        kb.ensure_readme_row(kb_dir, filename, title)
    return "new"


def distill_text(kb_dir: Path, runtime: Path, records: list[dict], backend: dict,
                 timeout: int) -> tuple[int, list[dict]]:
    """Document every record. Returns (documented count, records still missing)."""
    done_sigs = kb.documented_sigs(kb_dir)
    tally = {"new": 0, "merged": 0, "skipped": 0, "duplicate": 0, "failed": 0}
    failed = []
    for record in records:
        if record.get("sig") in done_sigs:
            tally["duplicate"] += 1
            continue
        try:
            outcome = document_record(kb_dir, runtime, record, backend, timeout)
        except Exception as exc:                      # never lose the batch to one bad record
            log(runtime, "record %s errored: %s" % (record.get("sig"), exc))
            outcome = "failed"
        tally[outcome] += 1
        cfg.session_log({"new": "documented", "merged": "merged",
                         "skipped": "not-useful", "failed": "write-fail"}[outcome],
                        record.get("sig", ""), record.get("binary", ""),
                        record.get("command", ""), "writer")
        if outcome == "failed":
            failed.append(record)
        else:
            done_sigs.add(record.get("sig"))
    log(runtime, "distilled: %(new)d new, %(merged)d merged, %(skipped)d skipped, "
                 "%(duplicate)d already known, %(failed)d failed" % tally)
    return sum(tally.values()) - tally["failed"], failed


def undocumented(kb_dir: Path, records: list[dict]) -> int:
    docs = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                     for p in kb_dir.glob("*.md"))
    have = set(SIG_RE.findall(docs))
    return sum(1 for r in records if r.get("sig") not in have)


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return procs.run(["git", *args], cwd=str(repo), capture_output=True, text=True)


def dirty_paths(repo: Path) -> set[str]:
    """Every path with uncommitted content, staged or not, tracked or not.

    NUL-separated so paths with spaces or non-ASCII survive intact; gitignored
    files (notably `.runtime/`) stay excluded.
    """
    done = git(repo, "status", "--porcelain", "-z", "--untracked-files=all")
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


def commit(repo: Path, runtime: Path, count: int, backend_name: str,
           preexisting: set[str] | None = None) -> None:
    """Commit only what the writer changed.

    Anything already dirty before the writer ran is the user's work in progress
    and is left alone. A path dirty on both sides is genuinely ambiguous — the
    two edits are interleaved in one file — so it is reported and skipped rather
    than guessed at.
    """
    if cfg.get("auto_commit", True) is not True:
        return
    root = git(repo, "rev-parse", "--show-toplevel")
    if root.returncode != 0:
        return
    # Porcelain status paths are relative to the Git root, even when the
    # knowledge base is a subdirectory. Stage/commit from the same root.
    repo = Path(root.stdout.strip())

    preexisting = set() if preexisting is None else preexisting
    now = dirty_paths(repo)
    ours = sorted(now - preexisting)
    entangled = sorted(now & preexisting)

    if entangled:
        shown = ", ".join(entangled[:5]) + (" ..." if len(entangled) > 5 else "")
        log(runtime, "left %d pre-existing change(s) uncommitted: %s" % (len(entangled), shown))
    if not ours:
        log(runtime, "nothing of ours to commit")
        return

    git(repo, "add", "--", *ours)
    # --only commits exactly these paths, so anything the user had staged stays staged.
    done = git(repo, "commit", "-q", "--only",
               "-m", "docs: document %d captured action(s)" % count,
               "-m", "Written automatically by the ai-session-skills writer (%s)." % backend_name,
               "--", *ours)
    if done.returncode != 0:
        err = "\n".join((done.stderr or done.stdout or "").strip().splitlines()[-2:])
        log(runtime, "commit failed: " + (err.replace("\n", " | ") or "unknown error"))
        return
    log(runtime, "committed %d action(s) across %d file(s)" % (count, len(ours)))

    if cfg.get("auto_push", False) is True and git(repo, "remote", "get-url", "origin").returncode == 0:
        if git(repo, "push", "-q").returncode == 0:
            log(runtime, "pushed to origin")


def main() -> int:
    kb_dir, runtime = cfg.kb_dir(), cfg.runtime_dir()
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "failed").mkdir(exist_ok=True)

    pending, batch = runtime / "pending.jsonl", runtime / "batch.jsonl"
    attempts_file = runtime / "batch.attempts"
    timeout = int(cfg.get("distill.timeout_seconds", 900) or 900)
    max_attempts = int(cfg.get("distill.max_attempts", 3) or 3)
    max_records = int(cfg.get("distill.max_batch_records", 40) or 40)

    if cfg.is_paused():
        log(runtime, "paused; not writing (resume with session.py resume)")
        return 0

    mode = "text" if str(cfg.get("writer.mode", "text")).lower() == "text" else "agent"
    backend = cfg.writer_backend(mode)
    if not backend:
        log(runtime, "no %s writer backend available (checked writer.prefer%s)"
            % (mode, "_text" if mode == "text" else ""))
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

        preexisting = dirty_paths(kb_dir)   # the user's work in progress; not ours to commit

        if mode == "text":
            per_record = int(cfg.get("distill.model_timeout_seconds", 180) or 180)
            distill_text(kb_dir, runtime, records, backend, per_record)
            status = 0
        else:
            prompt = build_prompt(kb_dir, runtime, len(records))
            status = run_backend(backend, prompt, kb_dir, timeout, runtime)

        # Same safety net in both modes: every sig must have landed in some .md.
        missing = undocumented(kb_dir, records) if status == 0 else None
        if status == 0:
            log(runtime, "writer finished; undocumented signatures: %d" % missing)

        if status != 0 or missing:
            log(runtime, "distillation incomplete (exit=%s undocumented=%s)"
                % (status, "n/a" if missing is None else missing))
            if attempt >= max_attempts:
                stamp = time.strftime("%Y%m%d-%H%M%S")
                batch.replace(runtime / "failed" / ("batch-%s.jsonl" % stamp))
                attempts_file.unlink(missing_ok=True)
                procs.run(procs.python_argv(cfg.TOOL_ROOT / "bin" / "sync_seen.py"),
                               capture_output=True)
                log(runtime, "gave up after %d attempts; batch parked in "
                             "failed/batch-%s.jsonl and signatures released" % (attempt, stamp))
            return 0

        batch.unlink(missing_ok=True)
        attempts_file.unlink(missing_ok=True)
        procs.run(procs.python_argv(cfg.TOOL_ROOT / "bin" / "sync_seen.py"),
                       capture_output=True)
        commit(kb_dir, runtime, len(records), backend["name"], preexisting)
        log(runtime, "done")
        return 0
    finally:
        lock.release()


if __name__ == "__main__":
    raise SystemExit(main())
