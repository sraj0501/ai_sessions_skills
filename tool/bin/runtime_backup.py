#!/usr/bin/env python3
"""Create, verify, and restore compressed backups of durable local runtime data."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cfg

SCHEMA = 1
SKIP_FILES = {"heartbeat", "watcher.alive", "watcher.pid", "session.log",
              "watcher.log", "distill.log"}
SKIP_SUFFIXES = (".log", ".pid")
REBUILDABLE_DATABASES = ("knowledge-vectors.sqlite3", "text-index.sqlite3",
                         "vector-index.sqlite3")


def _durable_files(runtime: Path) -> list[tuple[Path, str]]:
    if not runtime.is_dir():
        raise ValueError(f"runtime directory does not exist: {runtime}")
    files = []
    for path in sorted(runtime.rglob("*")):
        if "mcp_jobs" in path.relative_to(runtime).parts:
            continue
        if path.is_symlink():
            raise ValueError(f"runtime contains a symbolic link: {path}")
        if (not path.is_file() or path.name in SKIP_FILES or path.name.endswith(SKIP_SUFFIXES)
                or any(path.name.startswith(name) for name in REBUILDABLE_DATABASES)):
            continue
        files.append((path, path.relative_to(runtime).as_posix()))
    return files


def _safe_name(value: str) -> bool:
    path = PurePosixPath(value)
    return (value == path.as_posix() and not path.is_absolute()
            and len(path.parts) > 0 and all(part not in ("", ".", "..") for part in path.parts)
            and "\\" not in value and ":" not in value)


def backup(runtime: Path, output_dir: Path) -> Path:
    runtime = runtime.resolve()
    output_dir = output_dir.resolve()
    if output_dir == runtime or runtime in output_dir.parents:
        raise ValueError("backup destination must be outside the runtime directory")
    files = _durable_files(runtime)
    output_dir.mkdir(parents=True, exist_ok=True)
    name = datetime.now(timezone.utc).strftime("runtime-%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex[:8] + ".zip"
    archive = output_dir / name
    temp = output_dir / (name + ".tmp")
    manifest = {"schema": SCHEMA, "created_utc": datetime.now(timezone.utc).isoformat(),
                "files": {}}
    try:
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=9,
                             allowZip64=True) as zf:
            for source, relative in files:
                digest = hashlib.sha256()
                size = 0
                with source.open("rb") as reader, zf.open("runtime/" + relative, "w") as writer:
                    while chunk := reader.read(1024 * 1024):
                        writer.write(chunk)
                        digest.update(chunk)
                        size += len(chunk)
                manifest["files"][relative] = {"sha256": digest.hexdigest(), "size": size}
            zf.writestr("manifest.json", json.dumps(manifest, sort_keys=True, indent=2))
        verify(temp)
        temp.replace(archive)
    finally:
        temp.unlink(missing_ok=True)
    return archive


def _manifest(zf: zipfile.ZipFile) -> dict:
    try:
        manifest = json.loads(zf.read("manifest.json"))
    except (KeyError, json.JSONDecodeError) as exc:
        raise ValueError("backup manifest is missing or invalid") from exc
    files = manifest.get("files")
    if manifest.get("schema") != SCHEMA or not isinstance(files, dict):
        raise ValueError("unsupported backup manifest")
    if not all(_safe_name(name) and isinstance(info, dict)
               and isinstance(info.get("size"), int) and info["size"] >= 0
               and isinstance(info.get("sha256"), str) and len(info["sha256"]) == 64
               for name, info in files.items()):
        raise ValueError("unsafe backup manifest")
    expected = {"manifest.json"} | {"runtime/" + name for name in files}
    names = zf.namelist()
    if len(names) != len(set(names)) or set(names) != expected:
        raise ValueError("backup has unexpected or duplicate files")
    return manifest


def verify(archive: Path) -> dict:
    with zipfile.ZipFile(archive, "r") as zf:
        manifest = _manifest(zf)
        for relative, info in manifest["files"].items():
            digest = hashlib.sha256()
            size = 0
            with zf.open("runtime/" + relative) as reader:
                while chunk := reader.read(1024 * 1024):
                    digest.update(chunk)
                    size += len(chunk)
            if size != info["size"] or digest.hexdigest() != info["sha256"]:
                raise ValueError(f"backup integrity check failed: {relative}")
        return manifest


def restore(archive: Path, target: Path) -> Path:
    target = target.resolve()
    if target.exists():
        raise ValueError(f"restore target already exists: {target}")
    manifest = verify(archive)
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.parent / (target.name + "-restore-" + uuid.uuid4().hex[:8])
    staging.mkdir()
    try:
        with zipfile.ZipFile(archive, "r") as zf:
            for relative in manifest["files"]:
                destination = staging.joinpath(*PurePosixPath(relative).parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                with zf.open("runtime/" + relative) as reader, destination.open("xb") as writer:
                    shutil.copyfileobj(reader, writer)
        for state_file in list((staging / "playback").glob("*/state.json")) + [
                staging / "playback" / "active.json"]:
            if not state_file.is_file():
                continue
            state = json.loads(state_file.read_text(encoding="utf-8"))
            ident = state.get("id")
            if (isinstance(ident, str) and _safe_name(ident)
                    and len(PurePosixPath(ident).parts) == 1
                    and (staging / "playback" / ident / "playback.md").is_file()):
                state["output"] = str(target / "playback" / ident / "playback.md")
                state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        staging.replace(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("backup", help="compress durable runtime data")
    create.add_argument("--runtime", type=Path, default=cfg.runtime_dir())
    create.add_argument("--output-dir", type=Path,
                        default=cfg.runtime_dir().parent / "backups")
    check = commands.add_parser("verify", help="check archive hashes")
    check.add_argument("archive", type=Path)
    recover = commands.add_parser("restore", help="restore into a new directory")
    recover.add_argument("archive", type=Path)
    recover.add_argument("--target", type=Path, default=cfg.runtime_dir())
    args = parser.parse_args()
    try:
        if args.command == "backup":
            archive = backup(args.runtime, args.output_dir)
            print(f"backup: {archive} ({archive.stat().st_size} bytes)")
        elif args.command == "verify":
            manifest = verify(args.archive)
            print(f"verified {len(manifest['files'])} files in {args.archive}")
        else:
            print(f"restored: {restore(args.archive, args.target)}")
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
