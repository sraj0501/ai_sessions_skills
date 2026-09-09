"""Exercise Windows hook shims, detached watcher and real local model in isolation.

Run explicitly with: python tool/tests/smoke_windows.py
Requires the configured local writer. Never commits or changes the real KB.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import cfg
import capture
import kb


def main():
    if os.name != "nt":
        raise SystemExit("This integration check requires Windows")
    with tempfile.TemporaryDirectory(prefix="skills-windows-") as tmp:
        root = Path(tmp)
        config = cfg.load()
        config.update(auto_commit=False, auto_push=False)
        config["watcher"].update(poll_seconds=1, quiet_seconds=1, idle_exit_seconds=300)
        path = root / "config.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        env = dict(os.environ, AI_SKILLS_KB=str(root), AI_SKILLS_CONFIG=str(path))
        for key in ("AI_SKILLS_DISTILLER", "AI_SKILLS_CAPTURE_OFF"):
            env.pop(key, None)
        command = "git log --oneline -5"
        payload = {"hook_event_name": "PostToolUse", "tool_name": "Bash",
                   "tool_input": {"command": command}, "tool_response": {"exit_code": 0}}
        sig = capture.records_from_payload(payload, "codex")[0]["sig"]

        def run(script, *args, input=None):
            return subprocess.run([os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c",
                                   str(BIN / script), *args], env=env, input=input,
                                  capture_output=True, text=True, timeout=20, check=True)

        try:
            run("hook-session.cmd", "start", "codex")
            run("hook-capture.cmd", "codex", input=json.dumps(payload))
            run("hook-session.cmd", "end", "codex")
            deadline = time.monotonic() + 240
            while time.monotonic() < deadline:
                entries = [entry for file in root.glob("*.md")
                           for entry in kb.parse(file.read_text(encoding="utf-8"))
                           if sig in entry.sigs]
                if entries:
                    print("PASS: Windows hooks -> capture -> watcher -> local model -> entry")
                    print("Entry:", entries[0].heading)
                    run("hook-capture.cmd", "codex", input=json.dumps(payload))
                    log = (root / ".runtime" / "session.log").read_text(encoding="utf-8")
                    assert any("known" in line and sig in line for line in log.splitlines()), log
                    print("PASS: repeated hook event deduplicated")
                    return 0
                time.sleep(1)
            for name in ("watcher.log", "session.log"):
                file = root / ".runtime" / name
                if file.exists():
                    print(file.read_text(encoding="utf-8"))
            raise AssertionError("No documented entry within 240 seconds")
        finally:
            subprocess.run([sys.executable, str(BIN / "session.py"), "stop"],
                           env=env, capture_output=True, timeout=30, check=True)


if __name__ == "__main__":
    raise SystemExit(main())
