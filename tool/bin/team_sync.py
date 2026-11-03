#!/usr/bin/env python3
"""Upload approved WAL candidates and install the latest shared revision.

Usage: team_sync.py sync --allow approved-ids.txt
       team_sync.py pull | status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg
import wal
import wal_team

HEX = re.compile(r"^[0-9a-f]{64}$")
NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*\.md$")


def team_root() -> Path:
    return cfg.runtime_dir() / "team"


def settings(server: str | None) -> tuple[str, str]:
    url = (server or os.environ.get("AI_SKILLS_TEAM_URL") or cfg.get("team.url") or "").rstrip("/")
    token = os.environ.get("AI_SKILLS_TEAM_TOKEN", "")
    parsed = urlsplit(url)
    if not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path:
        raise ValueError("configure a server origin in AI_SKILLS_TEAM_URL or team.url")
    if parsed.scheme != "https" and not (parsed.scheme == "http" and parsed.hostname in
                                            ("localhost", "127.0.0.1", "::1")):
        raise ValueError("team sync requires HTTPS except for local loopback testing")
    if len(token) < 32:
        raise ValueError("AI_SKILLS_TEAM_TOKEN must contain at least 32 characters")
    return url, token


def request(url: str, token: str, path: str, payload: dict | None = None) -> bytes:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = Request(url + path, data=body,
                  headers={"Authorization": "Bearer " + token,
                           "Content-Type": "application/json"},
                  method="POST" if body is not None else "GET")
    with urlopen(req, timeout=30) as response:
        return response.read(2 * 1024 * 1024 + 1)


def upload(url: str, token: str, source: Path, allow_file: Path, root: Path) -> int:
    allowed = {line.strip() for line in allow_file.read_text(encoding="utf-8").splitlines()
               if line.strip() and not line.lstrip().startswith("#")}
    if not allowed:
        raise ValueError("allow-list is empty")
    records = wal_team.candidates(source, allowed)  # validates all selected events before network I/O
    root.mkdir(parents=True, exist_ok=True)
    acknowledged = set()
    for offset in range(0, len(records), 200):
        chunk = records[offset:offset + 200]
        reply = json.loads(request(url, token, "/v1/candidates",
                                   {"schema": 1, "candidates": chunk}))
        expected = {r["candidate_id"] for r in chunk}
        if set(reply.get("accepted", [])) != expected:
            raise ValueError("server receipt did not acknowledge the submitted candidates")
        acknowledged.update(expected)
        receipt = root / "receipts.jsonl"
        with receipt.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"candidate_ids": sorted(expected),
                                 "published_revision": reply.get("published_revision")}) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
    return len(acknowledged)


def validate_manifest(manifest: dict) -> tuple[str | None, dict[str, str]]:
    if not isinstance(manifest, dict) or manifest.get("schema") != 1:
        raise ValueError("invalid team manifest")
    revision, files = manifest.get("revision"), manifest.get("files")
    if revision is None and files == {}:
        return None, {}
    if not isinstance(revision, str) or not HEX.fullmatch(revision) or not isinstance(files, dict) or not files:
        raise ValueError("invalid team revision")
    for name, digest in files.items():
        if not isinstance(name, str) or not NAME.fullmatch(name) or name.startswith("_") or \
                not isinstance(digest, str) or not HEX.fullmatch(digest):
            raise ValueError("unsafe team manifest path or hash")
    return revision, files


def installed_revision(root: Path) -> str | None:
    try:
        return (root / "current").read_text(encoding="ascii").strip() or None
    except FileNotFoundError:
        return None


def revision_digest(files: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name, body in sorted(files.items()):
        digest.update(name.encode("utf-8") + b"\0" + body + b"\0")
    return digest.hexdigest()


def pull(url: str, token: str, root: Path) -> str | None:
    manifest = json.loads(request(url, token, "/v1/manifest"))
    revision, files = validate_manifest(manifest)
    if revision is None:
        return revision
    revisions = root / "revisions"
    revisions.mkdir(parents=True, exist_ok=True)
    target = revisions / revision
    if not target.exists():
        staging = Path(tempfile.mkdtemp(prefix=".download-", dir=revisions))
        try:
            downloaded = {}
            for name, digest in files.items():
                body = request(url, token, "/v1/files/" + revision + "/" + quote(name))
                if len(body) > 2 * 1024 * 1024 or hashlib.sha256(body).hexdigest() != digest:
                    raise ValueError("team download hash mismatch: " + name)
                body.decode("utf-8")
                (staging / name).write_bytes(body)
                downloaded[name] = body
            if revision_digest(downloaded) != revision:
                raise ValueError("team revision digest mismatch")
            (staging / "manifest.json").write_text(json.dumps(manifest, sort_keys=True) + "\n",
                                                   encoding="utf-8")
            staging.replace(target)
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    else:
        installed = {}
        for name, digest in files.items():
            if not (target / name).is_file() or hashlib.sha256((target / name).read_bytes()).hexdigest() != digest:
                raise ValueError("installed team revision is corrupt: " + name)
            installed[name] = (target / name).read_bytes()
        if revision_digest(installed) != revision:
            raise ValueError("installed team revision digest mismatch")
    pointer = root / "current.tmp"
    pointer.write_text(revision + "\n", encoding="ascii")
    pointer.replace(root / "current")
    return revision


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verb", choices=("sync", "pull", "status"))
    parser.add_argument("--allow", type=Path, help="reviewed WAL event IDs, one per line")
    parser.add_argument("--server", help="server origin; defaults to AI_SKILLS_TEAM_URL")
    parser.add_argument("--source", type=Path, default=wal.root())
    args = parser.parse_args(argv)
    root = team_root()
    try:
        if args.verb == "status":
            revision = installed_revision(root)
            print("installed revision: " + (revision or "none"))
            print("team copy: " + str(root / "revisions" / revision) if revision else "team copy: none")
            return 0
        url, token = settings(args.server)
        if args.verb == "sync":
            if not args.allow:
                raise ValueError("sync requires --allow with reviewed WAL event IDs")
            print("server acknowledged %d candidate(s); publication is separate" %
                  upload(url, token, args.source, args.allow, root))
        before = installed_revision(root)
        after = pull(url, token, root)
        print("team revision: %s%s" % (after or "not published yet",
                                        " (installed)" if after and after != before else ""))
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print("team sync failed: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
