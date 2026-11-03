#!/usr/bin/env python3
"""Authenticated candidate intake and reviewed, versioned team publications.

Put this service behind an HTTPS reverse proxy. Set AI_SKILLS_TEAM_TOKEN in the
server environment; never place the token in a checked-in config file.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
import threading
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wal_review
import wal_team

MAX_BODY = 2 * 1024 * 1024
NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*\.md$")


def manifest_for(proposal: Path) -> tuple[dict, dict[str, bytes]]:
    files = wal_review.files(proposal)
    if not files:
        raise ValueError("proposal has no Markdown files")
    for name, body in files.items():
        if not NAME.fullmatch(name) or name.startswith("_") or len(body) > MAX_BODY or b"\x00" in body:
            raise ValueError("invalid publication file: " + name)
        body.decode("utf-8")
    hashes = {name: hashlib.sha256(body).hexdigest() for name, body in files.items()}
    revision = wal_review.digest(proposal)
    return {"schema": 1, "revision": revision, "files": hashes}, files


def publish(root: Path, proposal: Path, approved_sha: str) -> str:
    manifest, files = manifest_for(proposal)
    if approved_sha != manifest["revision"]:
        raise ValueError("proposal digest changed; review it again")
    revision = manifest["revision"]
    target = root / "revisions" / revision
    if not target.exists():
        target.mkdir(parents=True)
        for name, body in files.items():
            (target / name).write_bytes(body)
        (target / "manifest.json").write_text(json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8")
    else:
        stored = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
        if stored != manifest:
            raise ValueError("stored revision conflict")
    pointer = root / "current.tmp"
    pointer.write_text(revision + "\n", encoding="ascii")
    pointer.replace(root / "current")
    return revision


def current_manifest(root: Path) -> dict:
    try:
        revision = (root / "current").read_text(encoding="ascii").strip()
        return json.loads((root / "revisions" / revision / "manifest.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"schema": 1, "revision": None, "files": {}}


def handler_for(root: Path, token: str | dict[str, str]):
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def _reply(self, code: int, data: dict | bytes, content_type="application/json"):
            body = data if isinstance(data, bytes) else json.dumps(data).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _authorized(self) -> str | None:
            actual = self.headers.get("Authorization", "")
            if isinstance(token, dict):
                for machine, secret in token.items():
                    if hmac.compare_digest(actual, "Bearer " + secret):
                        return machine
            elif hmac.compare_digest(actual, "Bearer " + token):
                return "*"
            self._reply(401, {"error": "unauthorized"})
            return None

        def do_POST(self):
            machine = self._authorized()
            if machine is None:
                return
            if urlsplit(self.path).path != "/v1/candidates":
                self._reply(404, {"error": "not found"})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size <= 0 or size > MAX_BODY:
                    raise ValueError("invalid request size")
                data = json.loads(self.rfile.read(size))
                if machine != "*" and any(r.get("machine_id") != machine
                                           for r in wal_team.validate_bundle(data)):
                    raise ValueError("candidate machine ID does not match token")
                with lock:
                    added, duplicates = wal_team.ingest_data(data, root / "inbox")
                self._reply(200, {"schema": 1, "accepted": [r["candidate_id"] for r in data["candidates"]],
                                  "added": added, "duplicates": duplicates,
                                  "published_revision": current_manifest(root)["revision"]})
            except (ValueError, KeyError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
                self._reply(400, {"error": str(exc)})

        def do_GET(self):
            if self._authorized() is None:
                return
            path = urlsplit(self.path).path
            if path == "/v1/manifest":
                self._reply(200, current_manifest(root))
                return
            parts = path.split("/")
            if len(parts) == 5 and parts[:3] == ["", "v1", "files"]:
                _, _, _, revision, name = parts
                try:
                    manifest = json.loads((root / "revisions" / revision / "manifest.json").read_text(encoding="utf-8")) \
                        if re.fullmatch(r"[0-9a-f]{64}", revision) else {}
                except FileNotFoundError:
                    manifest = {}
                if manifest.get("revision") == revision and name in manifest.get("files", {}):
                    self._reply(200, (root / "revisions" / revision / name).read_bytes(),
                                "text/markdown; charset=utf-8")
                    return
            self._reply(404, {"error": "not found"})

    return Handler


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verb", choices=("serve", "report", "propose", "publish", "status"))
    parser.add_argument("--root", type=Path, required=True, help="private central data directory")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--proposal", type=Path)
    parser.add_argument("--writer", choices=("model", "stub"), default="model")
    parser.add_argument("--approved-sha")
    args = parser.parse_args(argv)
    try:
        if args.verb == "serve":
            if os.environ.get("AI_SKILLS_TEAM_TOKENS"):
                token = json.loads(os.environ["AI_SKILLS_TEAM_TOKENS"])
                if not isinstance(token, dict) or not token or any(
                        not isinstance(k, str) or not k or not isinstance(v, str) or len(v) < 32
                        for k, v in token.items()) or len(set(token.values())) != len(token):
                    raise ValueError("AI_SKILLS_TEAM_TOKENS must map machine IDs to 32+ character tokens")
            else:
                token = os.environ.get("AI_SKILLS_TEAM_TOKEN", "")
                if len(token) < 32:
                    raise ValueError("AI_SKILLS_TEAM_TOKEN must contain at least 32 characters")
            if args.host not in ("127.0.0.1", "localhost", "::1"):
                raise ValueError("bind to loopback and put an HTTPS proxy in front of the server")
            server = ThreadingHTTPServer((args.host, args.port), handler_for(args.root, token))
            print("team sync server listening on %s:%d" % server.server_address, flush=True)
            server.serve_forever()
        elif args.verb == "report":
            print(wal_team.report(args.root / "inbox"))
        elif args.verb == "propose":
            if not args.output:
                raise ValueError("--output is required")
            print("drafted %d candidates" % wal_team.propose(args.root / "inbox", args.output, args.writer))
        elif args.verb == "publish":
            if not args.proposal or not args.approved_sha:
                raise ValueError("--proposal and --approved-sha are required")
            print("published revision " + publish(args.root, args.proposal, args.approved_sha))
        else:
            print(json.dumps({"inbox": len(list((args.root / "inbox").glob("*.json"))),
                              "publication": current_manifest(args.root)}, indent=2))
    except (ValueError, OSError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
