"""Bounded, typed operations shared by every session-skills MCP client."""
from __future__ import annotations

import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

import cfg
import procs

BIN = Path(__file__).resolve().parent
MAX_OUTPUT = 4000


def _tool(name: str, description: str, properties: dict, required: list[str],
          read_only: bool = False, destructive: bool = False) -> dict:
    return {"name": name, "description": description,
            "inputSchema": {"type": "object", "properties": properties,
                            "required": required, "additionalProperties": False},
            "annotations": {"readOnlyHint": read_only, "destructiveHint": destructive}}


S = lambda description: {"type": "string", "description": description}
I = lambda description: {"type": "integer", "minimum": 1, "description": description}
B = lambda description: {"type": "boolean", "description": description}

TOOLS = [
    _tool("inspect_session_skills", "Check pipeline health, recent activity, or command routes. Results are bounded.",
          {"view": {"type": "string", "enum": ["doctor", "activity", "routes", "signatures", "wal", "wal_verify"]},
           "limit": I("Recent activity lines, maximum 50")}, ["view"], True),
    _tool("control_capture_pipeline", "Check, start, stop, or restart automatic command capture; distill queued records.",
          {"action": {"type": "string", "enum": ["status", "start", "stop", "restart", "distill", "sync_seen", "compact_wal"]},
           "reason": S("Reason for stopping capture")}, ["action"]),
    _tool("record_resolution_playback", "Start, annotate, stop, finalize, or migrate a resolution playback.",
          {"action": {"type": "string", "enum": ["status", "start", "note", "stop", "finalize", "migrate"]},
           "title": S("Issue title for start"),
           "kind": {"type": "string", "enum": ["intent", "observation", "decision", "outcome"]},
           "text": S("Factual note text"), "session": S("Harness session ID when bound"),
           "harness": S("Harness name for start")}, ["action"]),
    _tool("generate_playback_reasoning", "Reconstruct missing reasoning for one playback. Returns a job ID. Existing reasoning is skipped unless overwrite is explicitly true.",
          {"id": S("Playback ID"), "model": S("Answer model ID"),
           "ollama_cloud": B("Use Ollama Cloud and OLLAMA_API_KEY from private environment"),
           "start": I("First step"), "end": I("Last step"),
           "overwrite": B("Explicitly replace existing reconstructed reasoning in prompts")}, ["id", "model"]),
    _tool("manage_runtime_backup", "Create, verify, or restore a private runtime ZIP. Restore requires a new target directory.",
          {"action": {"type": "string", "enum": ["backup", "verify", "restore"]},
           "archive": S("Archive path for verify or restore"),
           "target": S("New directory for restore"),
           "output_dir": S("Private archive directory for backup")}, ["action"]),
    _tool("manage_command_knowledge", "Inspect or change routes, capture commands, and propose or apply reviewed topic consolidation.",
          {"action": {"type": "string", "enum": ["routes", "route", "merge", "capture", "organize_propose", "organize_select", "organize_apply"]},
           "binary": S("Binary for route"), "file": S("Destination topic Markdown filename"),
           "source": S("Source topic Markdown filename for merge"),
           "sources": {"type": "array", "items": {"type": "string"},
                       "minItems": 1, "maxItems": 30,
                       "description": "Reviewed source filenames for organize_select"},
           "command": S("One command to capture"),
           "proposal": S("New proposal JSON path for organize_propose, reviewed JSON path for organize_apply"),
           "output": S("New filtered proposal JSON path for organize_select"),
           "approved_sha": S("Reviewed proposal SHA256 for organize_apply"),
           "max_entries": I("Maximum entries in a source topic file, default 5")}, ["action"], destructive=True),
    _tool("manage_shared_knowledge", "Inspect, pull, or sync a reviewed team knowledge revision. Sync needs an allowlist file of reviewed WAL event IDs.",
          {"action": {"type": "string", "enum": ["status", "pull", "sync"]},
           "allow_file": S("Path to reviewed WAL event ID allowlist for sync")}, ["action"]),
    _tool("review_knowledge_proposal", "Diff or promote a reviewed WAL reconstruction proposal; promotion requires its exact SHA256 digest.",
          {"action": {"type": "string", "enum": ["diff", "promote", "rebuild"]},
           "current": S("Current knowledge directory for diff/promote"),
           "proposal": S("Proposal directory for diff/promote"),
           "approved_sha": S("Reviewed SHA256 digest for promote"),
           "output": S("New proposal directory for rebuild"),
           "writer": {"type": "string", "enum": ["stub", "model"]}}, ["action"], destructive=True),
    _tool("manage_team_server", "Inspect, report, draft, or publish a central team knowledge revision. Publishing requires a reviewed SHA256 digest.",
          {"action": {"type": "string", "enum": ["status", "report", "propose", "publish"]},
           "root": S("Private central data directory"),
           "output": S("New proposal directory for propose"),
           "proposal": S("Reviewed proposal directory for publish"),
           "writer": {"type": "string", "enum": ["stub", "model"]},
           "approved_sha": S("Reviewed SHA256 digest for publish")}, ["action", "root"], destructive=True),
    _tool("manage_team_bundle", "Export reviewed WAL candidates, ingest a bundle, report an inbox, or draft a proposal.",
          {"action": {"type": "string", "enum": ["export", "ingest", "report", "propose"]},
           "allow_file": S("Reviewed WAL event ID allowlist for export"),
           "output": S("New bundle or proposal path"),
           "bundle": S("Bundle path for ingest"),
           "inbox": S("Private inbox directory for ingest, report, or propose"),
           "writer": {"type": "string", "enum": ["stub", "model"]}}, ["action"], destructive=True),
    _tool("session_skills_job_status", "Read the bounded result of a background MCP operation.",
          {"job_id": S("Job ID returned by an operation")}, ["job_id"], True),
]


def _string(args: dict, key: str, required: bool = False, max_len: int = 1000) -> str:
    value = args.get(key, "")
    if not isinstance(value, str) or len(value) > max_len or (required and not value.strip()):
        raise ValueError(f"{key} must be a {'nonempty ' if required else ''}string of at most {max_len} characters")
    return value.strip()


def _int(args: dict, key: str, default: int, maximum: int = 100000) -> int:
    value = args.get(key, default)
    if type(value) is not int or not 1 <= value <= maximum:
        raise ValueError(f"{key} must be an integer from 1 to {maximum}")
    return value


def _bool(args: dict, key: str) -> bool:
    value = args.get(key, False)
    if type(value) is not bool:
        raise ValueError(f"{key} must be a boolean")
    return value


def _path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _run(script: str, *args: str, background: bool = False) -> dict:
    argv = procs.python_argv(BIN / script, *args)
    if background:
        return _job(argv)
    done = procs.run(argv, cwd=cfg.TOOL_ROOT.parent, text=True, capture_output=True,
                     encoding="utf-8", errors="replace", timeout=30)
    output = ((done.stdout or "") + (done.stderr or "")).strip()
    return {"ok": done.returncode == 0, "exit_code": done.returncode,
            "output": output[:MAX_OUTPUT], "truncated": len(output) > MAX_OUTPUT}


def _job(argv: list[str]) -> dict:
    folder = cfg.runtime_dir() / "mcp_jobs"
    folder.mkdir(parents=True, exist_ok=True)
    ident = uuid.uuid4().hex
    request = folder / f"{ident}.json"
    request.write_text(json.dumps({"argv": argv, "status": "running"}), encoding="utf-8")
    pid = procs.spawn_detached(procs.python_argv(BIN / "mcp_job.py", ident),
                               cwd=cfg.TOOL_ROOT.parent)
    if pid is None:
        request.unlink(missing_ok=True)
        raise RuntimeError("could not launch background job")
    return {"job_id": ident, "status": "running"}


def job_status(ident: str) -> dict:
    if not isinstance(ident, str) or len(ident) != 32 or any(c not in "0123456789abcdef" for c in ident):
        raise ValueError("invalid job ID")
    path = cfg.runtime_dir() / "mcp_jobs" / f"{ident}.json"
    for attempt in range(4):
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
            break
        except FileNotFoundError as exc:
            raise ValueError("job not found") from exc
        except (PermissionError, json.JSONDecodeError):
            if attempt == 3:
                raise
            time.sleep(0.025)
    return {key: state[key] for key in ("status", "exit_code", "output", "truncated") if key in state} | {"job_id": ident}


def call(name: str, a: dict) -> dict:
    if not isinstance(a, dict):
        raise ValueError("arguments must be an object")
    schema = next((t["inputSchema"] for t in TOOLS if t["name"] == name), None)
    if schema is None:
        raise ValueError("unknown operation")
    extra = set(a) - set(schema["properties"])
    if extra:
        raise ValueError("unknown argument: " + sorted(extra)[0])
    for key in schema["required"]:
        if key not in a:
            raise ValueError("missing argument: " + key)
    if name == "session_skills_job_status":
        return job_status(_string(a, "job_id", True, 32))
    if name == "inspect_session_skills":
        view = _string(a, "view", True)
        if view == "doctor": return _run("doctor.py")
        if view == "routes": return _run("kb.py", "routes")
        if view == "signatures": return _run("kb.py", "sigs")
        if view == "activity": return _run("log.py", "--lines", str(_int(a, "limit", 20, 50)))
        if view == "wal": return _run("wal.py", "inspect", "--limit", str(_int(a, "limit", 20, 50)))
        if view == "wal_verify": return _run("wal.py", "verify")
    if name == "control_capture_pipeline":
        action = _string(a, "action", True)
        if action in ("status", "start", "restart"):
            return _run("session.py", action)
        if action == "stop": return _run("session.py", "stop", _string(a, "reason"))
        if action == "distill": return _run("distill.py", background=True)
        if action == "sync_seen": return _run("sync_seen.py")
        if action == "compact_wal": return _run("wal.py", "compact", background=True)
    if name == "record_resolution_playback":
        action = _string(a, "action", True)
        argv = [action]
        if action == "start":
            argv.append(_string(a, "title", True, 200))
        elif action == "note":
            kind = _string(a, "kind", True)
            if kind not in ("intent", "observation", "decision", "outcome"):
                raise ValueError("kind must be intent, observation, decision, or outcome")
            argv += [kind, _string(a, "text", True, 2000)]
        elif action not in ("status", "stop", "finalize", "migrate"):
            raise ValueError("invalid playback action")
        session = _string(a, "session", max_len=200)
        harness = _string(a, "harness", max_len=80)
        if session: argv += ["--session", session]
        if harness and action == "start": argv += ["--harness", harness]
        return _run("playback.py", *argv, background=action == "finalize")
    if name == "generate_playback_reasoning":
        ident = _string(a, "id", True, 200)
        model = _string(a, "model", True, 200)
        argv = ["--id", ident, "--model", model]
        if _bool(a, "ollama_cloud"): argv.append("--ollama-cloud")
        if "start" in a: argv += ["--start", str(_int(a, "start", 1))]
        if "end" in a: argv += ["--end", str(_int(a, "end", 1))]
        if _bool(a, "overwrite"): argv.append("--overwrite")
        return _run("playback_reason.py", *argv, background=True)
    if name == "manage_runtime_backup":
        action = _string(a, "action", True)
        if action == "backup":
            output = _string(a, "output_dir", max_len=1000)
            return _run("runtime_backup.py", "backup", *(["--output-dir", str(_path(output))] if output else []), background=True)
        archive = _string(a, "archive", True, 1000)
        if action == "verify": return _run("runtime_backup.py", "verify", str(_path(archive)), background=True)
        if action == "restore":
            target = _string(a, "target", True, 1000)
            return _run("runtime_backup.py", "restore", str(_path(archive)), "--target", str(_path(target)), background=True)
    if name == "manage_command_knowledge":
        action = _string(a, "action", True)
        if action == "routes": return _run("kb.py", "routes")
        if action == "route": return _run("kb.py", "route", _string(a, "binary", True, 100), _string(a, "file", True, 150))
        if action == "merge": return _run("kb.py", "merge", _string(a, "source", True, 150), _string(a, "file", True, 150), background=True)
        if action == "capture": return _run("capture.py", "--command", _string(a, "command", True, 2000), "--harness", "mcp")
        if action == "organize_propose":
            proposal = str(_path(_string(a, "proposal", True, 1000)))
            source = _string(a, "source", max_len=150)
            return _run("knowledge_organize.py", "propose", "--proposal", proposal,
                        "--max-entries", str(_int(a, "max_entries", 5, 20)),
                        *(["--source", source] if source else []), background=True)
        if action == "organize_apply":
            proposal = str(_path(_string(a, "proposal", True, 1000)))
            return _run("knowledge_organize.py", "apply", "--proposal", proposal,
                        "--approved-sha", _digest(a), background=True)
        if action == "organize_select":
            proposal = str(_path(_string(a, "proposal", True, 1000)))
            output = str(_path(_string(a, "output", True, 1000)))
            sources = a.get("sources")
            if not isinstance(sources, list) or not 1 <= len(sources) <= 30 or \
                    any(not isinstance(source, str) or not source.strip() or
                        len(source) > 150 for source in sources):
                raise ValueError("sources must be 1 to 30 topic filenames")
            return _run("knowledge_organize.py", "select", "--proposal", proposal,
                        "--output", output,
                        *(part for source in sources for part in ("--source", source)),
                        background=False)
    if name == "manage_shared_knowledge":
        action = _string(a, "action", True)
        if action == "status": return _run("team_sync.py", "status")
        if action == "pull": return _run("team_sync.py", "pull", background=True)
        if action == "sync":
            allow = _string(a, "allow_file", True, 1000)
            return _run("team_sync.py", "sync", "--allow", str(_path(allow)), background=True)
    if name == "review_knowledge_proposal":
        action = _string(a, "action", True)
        if action == "rebuild":
            output = _string(a, "output", True, 1000)
            writer = _string(a, "writer") or "stub"
            if writer not in ("stub", "model"):
                raise ValueError("writer must be stub or model")
            return _run("wal_rebuild.py", "--output", str(_path(output)), "--writer", writer, background=True)
        current = _string(a, "current", True, 1000)
        proposal = _string(a, "proposal", True, 1000)
        argv = [action, "--current", str(_path(current)), "--proposal", str(_path(proposal))]
        if action == "diff": return _run("wal_review.py", *argv)
        if action == "promote":
            digest = _string(a, "approved_sha", True, 64)
            if len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
                raise ValueError("approved_sha must be a SHA256 hex digest")
            return _run("wal_review.py", *argv, "--approved-sha", digest, background=True)
    if name == "manage_team_server":
        action = _string(a, "action", True)
        root = str(_path(_string(a, "root", True, 1000)))
        if action in ("status", "report"):
            return _run("team_server.py", action, "--root", root)
        if action == "propose":
            output = str(_path(_string(a, "output", True, 1000)))
            writer = _string(a, "writer") or "model"
            if writer not in ("stub", "model"): raise ValueError("invalid writer")
            return _run("team_server.py", "propose", "--root", root, "--output", output,
                        "--writer", writer, background=True)
        if action == "publish":
            proposal = str(_path(_string(a, "proposal", True, 1000)))
            digest = _digest(a)
            return _run("team_server.py", "publish", "--root", root, "--proposal",
                        proposal, "--approved-sha", digest, background=True)
    if name == "manage_team_bundle":
        action = _string(a, "action", True)
        if action == "export":
            allow = str(_path(_string(a, "allow_file", True, 1000)))
            output = str(_path(_string(a, "output", True, 1000)))
            return _run("wal_team.py", "export", "--allow", allow, "--output", output, background=True)
        inbox = str(_path(_string(a, "inbox", True, 1000)))
        if action == "report": return _run("wal_team.py", "report", "--inbox", inbox)
        if action == "ingest":
            bundle = str(_path(_string(a, "bundle", True, 1000)))
            return _run("wal_team.py", "ingest", "--inbox", inbox, "--bundle", bundle, background=True)
        if action == "propose":
            output = str(_path(_string(a, "output", True, 1000)))
            writer = _string(a, "writer") or "stub"
            if writer not in ("stub", "model"): raise ValueError("invalid writer")
            return _run("wal_team.py", "propose", "--inbox", inbox, "--output", output,
                        "--writer", writer, background=True)
    raise ValueError("invalid action")


def _digest(a: dict) -> str:
    digest = _string(a, "approved_sha", True, 64)
    if len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
        raise ValueError("approved_sha must be a SHA256 hex digest")
    return digest
