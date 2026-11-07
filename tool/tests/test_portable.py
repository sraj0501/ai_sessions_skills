#!/usr/bin/env python3
"""Portability and behaviour tests. No dependencies, no network, no agents.

    python3 tool/tests/test_portable.py

Path resolution and backend rendering are pure functions of (platform, env,
home), so Windows and Linux layouts are verified from any machine — including
macOS, where they cannot be exercised directly.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import capture     # noqa: E402
import cfg         # noqa: E402
import distill     # noqa: E402
import json_merge  # noqa: E402
import kb          # noqa: E402
import knowledge_organize  # noqa: E402
import procs       # noqa: E402
import search as knowledge_search

ENTRY = """### Check what changed before committing
<!-- sig: aaaaaaaaaaaa -->

```bash
git --no-pager diff --staged
```

- **What it does:** Shows staged changes.
"""


class TestUserConfigDir(unittest.TestCase):
    def test_windows_uses_appdata(self):
        got = cfg.user_config_dir("win32", {"APPDATA": r"C:\Users\me\AppData\Roaming"},
                                  Path(r"C:\Users\me"))
        self.assertEqual(str(got), r"C:\Users\me\AppData\Roaming")

    def test_windows_falls_back_to_home(self):
        got = cfg.user_config_dir("win32", {}, Path("/home/me"))
        self.assertEqual(got, Path("/home/me/AppData/Roaming"))

    def test_linux_honours_xdg(self):
        got = cfg.user_config_dir("linux", {"XDG_CONFIG_HOME": "/home/me/.xdg"},
                                  Path("/home/me"))
        self.assertEqual(got, Path("/home/me/.xdg"))

    def test_linux_default_is_dot_config(self):
        self.assertEqual(cfg.user_config_dir("linux", {}, Path("/home/me")),
                         Path("/home/me/.config"))

    def test_macos_default_is_dot_config(self):
        self.assertEqual(cfg.user_config_dir("darwin", {}, Path("/Users/me")),
                         Path("/Users/me/.config"))


class TestHarnessLayout(unittest.TestCase):
    """Devin follows the platform convention; the dot-dir harnesses do not."""

    def layout(self, platform, env=None, home=None):
        return cfg.harness_layout(platform, env or {}, home or Path("/home/me"),
                                  exists=lambda p: False)

    def test_linux_devin_under_xdg(self):
        got = self.layout("linux")
        self.assertEqual(got["devin"]["hooks"], Path("/home/me/.config/devin/config.json"))
        self.assertEqual(got["opencode"]["plugin"],
                         Path("/home/me/.config/opencode/plugin/ai-session-skills.js"))

    def test_linux_respects_xdg_override(self):
        got = self.layout("linux", {"XDG_CONFIG_HOME": "/home/me/.xdg"})
        self.assertEqual(got["devin"]["hooks"], Path("/home/me/.xdg/devin/config.json"))

    def test_windows_devin_under_appdata(self):
        got = self.layout("win32", {"APPDATA": "/c/Users/me/AppData/Roaming"},
                          Path("/c/Users/me"))
        self.assertEqual(got["devin"]["hooks"],
                         Path("/c/Users/me/AppData/Roaming/devin/config.json"))

    def test_dot_dirs_are_home_relative_on_every_platform(self):
        for platform in ("win32", "darwin", "linux"):
            got = self.layout(platform, {"APPDATA": "/appdata"}, Path("/home/me"))
            self.assertEqual(got["claude"]["hooks"], Path("/home/me/.claude/settings.json"),
                             platform)
            self.assertEqual(got["codex"]["hooks"], Path("/home/me/.codex/hooks.json"), platform)
            self.assertEqual(got["copilot"]["hooks"],
                             Path("/home/me/.copilot/hooks/ai-session-skills.json"), platform)
            self.assertEqual(got["cursor"]["hooks"], Path("/home/me/.cursor/hooks.json"), platform)

    def test_windows_prefers_existing_opencode_dir(self):
        existing = Path("/home/me/.config/opencode")
        got = cfg.harness_layout("win32", {"APPDATA": "/appdata"}, Path("/home/me"),
                                 exists=lambda p: p == existing)
        self.assertEqual(got["opencode"]["dir"], existing)

    def test_every_harness_has_a_skill_destination(self):
        got = self.layout("linux")
        for harness, spec in got.items():
            self.assertTrue(str(spec["skill"]).endswith(".md"), harness)
            self.assertIn(spec["style"], ("devin", "claude", "plain"), harness)


class TestPrimaryHooks(unittest.TestCase):
    def test_codex_captures_all_tool_names_on_windows_with_history_fallback_enabled(self):
        sys.path.insert(0, str(BIN.parent))
        import install
        with patch.object(install.cfg, "IS_WINDOWS", True), \
                patch.object(install.cfg, "get", return_value=True):
            groups = install.codex_patch()["hooks"]["PostToolUse"]
        self.assertEqual(len(groups), 1)
        self.assertNotIn("matcher", groups[0])
        self.assertIn("capture", groups[0]["hooks"][0]["command"])

    def test_claude_covers_powershell_and_failed_commands(self):
        sys.path.insert(0, str(BIN.parent))
        import install
        hooks = install.claude_patch()["hooks"]
        for event in ("PostToolUse", "PostToolUseFailure"):
            self.assertIn("PowerShell", hooks[event][0]["matcher"])
            self.assertIn("exec_command", hooks[event][0]["matcher"])

    def test_nested_exit_code_marks_failed_shell_command(self):
        rows = capture.records_from_payload({
            "tool_name": "exec_command", "tool_input": {"command": "git status"},
            "tool_response": {"exit_code": 1, "output": "fatal"},
        }, "codex")
        self.assertEqual(len(rows), 1)
        self.assertFalse(rows[0]["ok"])

    @unittest.skipUnless(os.name == "nt", "Windows GUI interpreter probe")
    def test_windows_hook_command_receives_stdin_without_console(self):
        sys.path.insert(0, str(BIN.parent))
        import install
        import wal
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, AI_SKILLS_KB=tmp)
            env.pop("AI_SKILLS_CAPTURE_OFF", None)
            payload = {"tool_name": "exec_command", "tool_input": {"command": "echo hook-probe"},
                       "tool_response": {"exit_code": 0, "output": "hook-probe"}}
            done = subprocess.run(install.hook_cmd("capture", "codex"),
                                  input=json.dumps(payload), capture_output=True,
                                  text=True, shell=True, env=env, timeout=15)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertEqual(done.stdout, "")
            events = list(wal.events(Path(tmp) / ".runtime" / "wal"))
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["payload"], payload)


class TestHookLauncher(unittest.TestCase):
    def test_launcher_extension_matches_platform(self):
        suffix = ".cmd" if os.name == "nt" else ".sh"
        for kind in ("capture", "session"):
            launcher = cfg.hook_launcher(kind)
            self.assertTrue(str(launcher).endswith(suffix))
            self.assertTrue(launcher.is_file(), "%s missing" % launcher)

    def test_both_platform_shims_are_shipped(self):
        for name in ("hook-capture.sh", "hook-capture.cmd",
                     "hook-session.sh", "hook-session.cmd"):
            self.assertTrue((BIN / name).is_file(), name)


class TestWriterBackend(unittest.TestCase):
    def test_placeholders_are_rendered_and_empty_model_dropped(self):
        spec = {
            "prefer": ["fake"],
            "backends": {"fake": {"bin": sys.executable, "model": "",
                                  "args": ["-m", "{model}", "--cd", "{kb}", "{prompt_text}"],
                                  "prompt": "arg"}},
        }
        original = cfg.load
        cfg.load = lambda: {**original(), "writer": spec}
        try:
            got = cfg.writer_backend()
        finally:
            cfg.load = original
        self.assertIsNotNone(got)
        self.assertNotIn("{model}", got["args"])
        self.assertNotIn("-m", got["args"])          # flag dropped with its empty value
        self.assertIn(str(cfg.kb_dir()), got["args"])
        self.assertIn("{prompt_text}", got["args"])  # substituted at run time

    def test_no_backend_when_binary_missing(self):
        spec = {"prefer": ["nope"],
                "backends": {"nope": {"bin": "definitely-not-installed-xyz", "args": []}}}
        original = cfg.load
        cfg.load = lambda: {**original(), "writer": spec}
        try:
            self.assertIsNone(cfg.writer_backend())
        finally:
            cfg.load = original

    def test_shipped_backends_declare_a_prompt_mode(self):
        for name, spec in cfg.DEFAULTS["writer"]["backends"].items():
            self.assertIn(spec.get("prompt"), ("file", "arg", "stdin"), name)
            if spec["prompt"] == "arg":
                self.assertIn("{prompt_text}", spec["args"], name)
            if spec["prompt"] == "file":
                self.assertIn("{prompt_file}", spec["args"], name)


class TestSignatures(unittest.TestCase):
    def sig(self, command):
        return [s for s, _b, _sc, _seg in capture.sig_of_command(command)]

    def test_same_action_different_values_collapses(self):
        self.assertEqual(self.sig('git commit -m "fix a"'), self.sig('git commit -m "fix b"'))
        self.assertEqual(self.sig("npm install lodash"), self.sig("npm install express"))
        self.assertEqual(self.sig("brew services restart postgresql@16"),
                         self.sig("brew services restart redis"))

    def test_names_do_not_leak_into_signatures(self):
        """A service/release/pod/package name must not create a new action."""
        self.assertEqual(self.sig("systemctl status sshd"), self.sig("systemctl status httpd"))
        self.assertEqual(self.sig("helm upgrade api ./chart"), self.sig("helm upgrade web ./chart"))
        self.assertEqual(self.sig("kubectl logs pod-abc"), self.sig("kubectl logs pod-xyz"))
        self.assertEqual(self.sig("dnf install ripgrep"), self.sig("dnf install jq"))

    def test_real_subcommands_still_split(self):
        self.assertNotEqual(self.sig("systemctl status sshd"), self.sig("systemctl restart sshd"))
        self.assertNotEqual(self.sig("helm repo add x https://y"), self.sig("helm repo update"))
        self.assertNotEqual(self.sig("kubectl get pods"), self.sig("kubectl get svc"))
        self.assertNotEqual(self.sig("az boards work-item show"), self.sig("az boards query"))

    def test_distinct_actions_stay_distinct(self):
        self.assertNotEqual(self.sig("npm run test"), self.sig("npm run build"))
        self.assertNotEqual(self.sig("git --no-pager diff"), self.sig("git --no-pager log"))
        self.assertNotEqual(self.sig("git stash push"), self.sig("git stash pop"))

    def test_pipelines_yield_one_signature_per_segment(self):
        self.assertEqual(len(self.sig("cat f.json | python3 -m json.tool")), 2)
        self.assertEqual(len(self.sig("git fetch upstream && git merge upstream/staging")), 2)

    def test_quoted_separators_do_not_split(self):
        self.assertEqual(len(self.sig('git commit -m "a; b && c"')), 1)

    def test_trivial_commands_are_ignored(self):
        self.assertEqual(self.sig("echo hello"), [])
        self.assertEqual(self.sig("cd /tmp"), [])


class TestPayloadNormalisation(unittest.TestCase):
    """One code path must absorb every harness's payload shape."""

    CASES = {
        "devin": {"tool_name": "exec", "tool_input": {"command": "terraform apply"},
                  "tool_response": {"success": True}},
        "claude": {"hook_event_name": "PostToolUse", "tool_name": "Bash", "cwd": "/repo",
                   "tool_input": {"command": "helm upgrade api ./chart"},
                   "tool_response": {"stdout": "ok"}},
        "codex": {"tool_name": "Bash", "tool_input": {"command": "cargo build --release"},
                  "tool_response": {"success": True}},
        "copilot-camel": {"sessionId": "x", "cwd": "/repo", "toolName": "bash",
                          "toolArgs": {"command": "aws s3 ls s3://b"},
                          "toolResult": {"resultType": "success"}},
        "copilot-snake": {"tool_name": "bash", "tool_input": {"command": "gcloud auth login"},
                          "tool_result": {"result_type": "success"}},
        "opencode": {"tool_name": "bash", "tool_input": {"command": "bun test --coverage"},
                     "tool_response": {"success": True}},
        "cursor-shell": {"command": "pnpm dlx prisma migrate dev", "exit_code": 0},
        "cursor-tool": {"tool_name": "Shell",
                        "tool_input": {"command": "kubectl rollout restart deploy/api"}},
    }

    def test_every_shape_produces_a_shell_record(self):
        for name, payload in self.CASES.items():
            records = capture.records_from_payload(payload, name)
            self.assertEqual(len(records), 1, name)
            self.assertEqual(records[0]["kind"], "shell", name)
            self.assertTrue(records[0]["sig"], name)
            self.assertTrue(records[0]["ok"], name)

    def test_string_encoded_arguments_are_parsed(self):
        records = capture.records_from_payload(
            {"toolName": "bash", "toolArgs": json.dumps({"command": "docker ps -a"})}, "copilot")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["binary"], "docker")

    def test_failure_shapes_are_detected(self):
        for payload in (
            {"tool_name": "Bash", "tool_input": {"command": "psql -c 'select 1'"},
             "tool_response": {"is_error": True}},
            {"hook_event_name": "PostToolUseFailure", "tool_name": "Bash",
             "tool_input": {"command": "psql -c 'select 2'"}},
            {"tool_name": "bash", "tool_input": {"command": "psql -c 'select 3'"},
             "exit_code": 1},
        ):
            records = capture.records_from_payload(payload, "test")
            self.assertEqual(len(records), 1)
            self.assertFalse(records[0]["ok"], payload)

    def test_search_tools_become_ripgrep(self):
        claude = capture.records_from_payload(
            {"tool_name": "Grep", "tool_input": {"pattern": "TODO", "glob": "*.go",
                                                 "-i": True, "-C": 2}}, "claude")[0]
        self.assertEqual(claude["binary"], "rg")
        self.assertIn("-i", claude["command"])
        self.assertIn("-C", claude["command"])
        devin = capture.records_from_payload(
            {"tool_name": "grep", "tool_input": {"pattern": "TODO", "glob_pattern": "*.go",
                                                 "case_insensitive": True,
                                                 "context_lines": 2}}, "devin")[0]
        self.assertEqual(claude["sig"], devin["sig"],
                         "same search in two harnesses must be one action")

    def test_edit_tools_are_documented_once_per_kind(self):
        a = capture.records_from_payload({"tool_name": "Write",
                                          "tool_input": {"file_path": "/a"}}, "claude")[0]
        b = capture.records_from_payload({"tool_name": "write",
                                          "tool_input": {"file_path": "/b"}}, "devin")[0]
        self.assertEqual(a["sig"], b["sig"])
        self.assertEqual(a["kind"], "agent-tool")

    def test_unknown_payload_is_ignored_not_crashed(self):
        self.assertEqual(capture.records_from_payload({}, "x"), [])
        self.assertEqual(capture.records_from_payload({"tool_name": "WebFetch",
                                                       "tool_input": {"url": "http://x"}}, "x"), [])


class TestJsonMerge(unittest.TestCase):
    def test_windows_paths_do_not_duplicate_hooks_on_reinstall(self):
        marker = r"D:\repo\tool"
        payload = {"hooks": {"PostToolUse": [{"hooks": [
            {"command": marker + r"\bin\hook-capture.cmd codex"}]}]}}
        json_merge.apply(self.path, payload, [marker])
        self.assertEqual(json_merge.apply(self.path, payload, [marker]), "unchanged")
        self.assertEqual(json.loads(self.path.read_text()), payload)
        json_merge.remove(self.path, [marker])
        self.assertEqual(json.loads(self.path.read_text()), {})

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = Path(self.dir) / "settings.json"

    def test_merge_preserves_foreign_settings_and_is_idempotent(self):
        self.path.write_text(json.dumps({
            "theme": "dark",
            "hooks": {"PostToolUse": [{"hooks": [{"command": "/other/tool/x.sh"}]}]},
        }, indent=2) + "\n", encoding="utf-8")
        patch = {"hooks": {"PostToolUse": [{"hooks": [{"command": "/my/tool/bin/c.sh"}]}]}}

        self.assertEqual(json_merge.apply(self.path, patch, ["/my/tool"]), "updated")
        first = self.path.read_text()
        self.assertEqual(json_merge.apply(self.path, patch, ["/my/tool"]), "unchanged")
        self.assertEqual(self.path.read_text(), first)

        data = json.loads(first)
        self.assertEqual(data["theme"], "dark")
        commands = [h["command"] for group in data["hooks"]["PostToolUse"]
                    for h in group["hooks"]]
        self.assertIn("/other/tool/x.sh", commands)
        self.assertEqual(sum(1 for c in commands if c.startswith("/my/tool")), 1)

    def test_remove_is_pure_subtraction(self):
        self.path.write_text(json.dumps({
            "theme": "dark",
            "hooks": {"PostToolUse": [{"hooks": [{"command": "/my/tool/bin/c.sh"}]}]},
        }, indent=2) + "\n", encoding="utf-8")
        self.assertEqual(json_merge.remove(self.path, ["/my/tool"]), "updated")
        data = json.loads(self.path.read_text())
        self.assertEqual(data, {"theme": "dark"})

    def test_legacy_marker_purges_old_layout(self):
        self.path.write_text(json.dumps({
            "hooks": {"PostToolUse": [{"hooks": [{"command": "/repo/bin/old-hook.sh"}]}]},
        }, indent=2) + "\n", encoding="utf-8")
        patch = {"hooks": {"PostToolUse": [{"hooks": [{"command": "/repo/tool/bin/new.sh"}]}]}}
        json_merge.apply(self.path, patch, ["/repo/tool", "/repo"])
        commands = [h["command"] for group in
                    json.loads(self.path.read_text())["hooks"]["PostToolUse"]
                    for h in group["hooks"]]
        self.assertEqual(commands, ["/repo/tool/bin/new.sh"])

    def test_missing_file_reports_missing_on_remove(self):
        self.assertEqual(json_merge.remove(Path(self.dir) / "nope.json", ["/x"]), "missing")


class TestLocking(unittest.TestCase):
    def test_lock_is_exclusive_and_releasable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lock"
            first, second = procs.DirLock(path), procs.DirLock(path)
            self.assertTrue(first.acquire())
            self.assertFalse(second.acquire())
            first.release()
            self.assertTrue(second.acquire())
            second.release()

    def test_stale_lock_is_reclaimed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lock"
            path.mkdir()
            os.utime(path, (0, 0))                    # ancient
            self.assertTrue(procs.DirLock(path, stale_after=60).acquire())


class TestBackgroundLaunch(unittest.TestCase):
    def test_windows_helpers_request_no_console(self):
        with patch.object(procs, "IS_WINDOWS", True), patch.object(procs.subprocess, "run") as run:
            procs.run(["tasklist"], capture_output=True)
            self.assertTrue(run.call_args.kwargs["creationflags"] & 0x08000000)

    def test_posix_helpers_do_not_receive_windows_flags(self):
        with patch.object(procs, "IS_WINDOWS", False), patch.object(procs.subprocess, "run") as run:
            procs.run(["git", "status"], capture_output=True)
            self.assertNotIn("creationflags", run.call_args.kwargs)

    @unittest.skipUnless(os.name == "nt", "Windows console regression")
    def test_real_helper_has_no_console_and_preserves_piped_input(self):
        done = procs.run([sys.executable, "-c",
                          "import ctypes, sys; print(ctypes.windll.kernel32.GetConsoleWindow()); "
                          "print(sys.stdin.read())"],
                         input="hook payload", capture_output=True, text=True, check=True)
        self.assertEqual(done.stdout.splitlines(), ["0", "hook payload"])

    @unittest.skipUnless(os.name == "nt", "Windows detached regression")
    def test_detached_process_has_no_console(self):
        import time
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "console.txt"
            pid = procs.spawn_detached([sys.executable, "-c",
                "import ctypes, pathlib, sys; pathlib.Path(sys.argv[1]).write_text("
                "str(ctypes.windll.kernel32.GetConsoleWindow()))", str(output)])
            self.assertIsNotNone(pid)
            deadline = time.monotonic() + 10
            while not output.exists() and time.monotonic() < deadline:
                time.sleep(0.05)
            self.assertEqual(output.read_text(), "0")


class TestLiveness(unittest.TestCase):
    def test_tasklist_access_failure_does_not_report_a_dead_process(self):
        with patch.object(procs, "IS_WINDOWS", True), patch.object(procs.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 1, "", "Access denied")
            self.assertTrue(procs.pid_alive(12345))

    def test_dead_pid_is_not_alive(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            (runtime / "watcher.pid").write_text("999999")
            self.assertFalse(procs.watcher_alive(runtime))

    def test_missing_pidfile_is_not_alive(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(procs.watcher_alive(Path(tmp)))

    def test_own_pid_with_fresh_touch_is_alive(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            (runtime / "watcher.pid").write_text(str(os.getpid()))
            (runtime / "watcher.alive").touch()
            self.assertTrue(procs.watcher_alive(runtime))


class TestCommitScope(unittest.TestCase):
    """The writer commits its own output and never the user's work in progress."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kb = Path(self.tmp.name)
        self.runtime = self.kb / ".runtime"
        self.runtime.mkdir()
        for args in (("init", "-q", "-b", "main"),
                     ("config", "user.email", "test@example.com"),
                     ("config", "user.name", "Test"),
                     ("config", "commit.gpgsign", "false")):
            distill.git(self.kb, *args)
        (self.kb / ".gitignore").write_text(".runtime/\n", encoding="utf-8")
        (self.kb / "git.md").write_text("# git\n", encoding="utf-8")
        distill.git(self.kb, "add", "-A")
        distill.git(self.kb, "commit", "-q", "-m", "seed")

        self.real_get = distill.cfg.get
        distill.cfg.get = lambda key, default=None: {
            "auto_commit": True, "auto_push": False}.get(key, default)

    def tearDown(self):
        distill.cfg.get = self.real_get
        self.tmp.cleanup()

    def head_files(self):
        done = distill.git(self.kb, "diff-tree", "--no-commit-id",
                           "--name-only", "-r", "-z", "HEAD")
        return sorted(p for p in done.stdout.split("\0") if p)

    def head_subject(self):
        return distill.git(self.kb, "log", "-1", "--format=%s").stdout.strip()

    def write(self, name, text):
        (self.kb / name).write_text(text, encoding="utf-8")

    def test_gitignored_runtime_is_never_dirty(self):
        (self.runtime / "pending.jsonl").write_text("noise\n", encoding="utf-8")
        self.assertEqual(distill.dirty_paths(self.kb), set())

    def test_nested_knowledge_folder_commits_with_root_relative_paths(self):
        nested = self.kb / "knowledge"
        nested.mkdir()
        self.write("README.md", "user work\n")
        before = distill.dirty_paths(nested)
        (nested / "shell.md").write_text("# Shell\n")
        distill.commit(nested, self.runtime, 1, "test", before)
        self.assertEqual(self.head_files(), ["knowledge/shell.md"])
        self.assertIn("README.md", distill.dirty_paths(self.kb))

    def test_preexisting_work_is_left_uncommitted(self):
        self.write("README.md", "user work in progress\n")     # user, before the writer
        before = distill.dirty_paths(self.kb)
        self.write("shell.md", "# shell\n")                    # writer's output
        distill.commit(self.kb, self.runtime, 1, "test", before)
        self.assertEqual(self.head_files(), ["shell.md"])
        self.assertIn("README.md", distill.dirty_paths(self.kb))

    def test_entangled_file_is_skipped_not_guessed(self):
        self.write("git.md", "# git\nuser edit\n")
        before = distill.dirty_paths(self.kb)
        self.write("git.md", "# git\nuser edit\nwriter edit\n")
        distill.commit(self.kb, self.runtime, 1, "test", before)
        self.assertEqual(self.head_subject(), "seed")          # nothing committed
        self.assertIn("git.md", distill.dirty_paths(self.kb))
        self.assertIn("left 1 pre-existing change",
                      (self.runtime / "distill.log").read_text(encoding="utf-8"))

    def test_user_staged_work_stays_staged(self):
        self.write("README.md", "staged user work\n")
        distill.git(self.kb, "add", "README.md")
        before = distill.dirty_paths(self.kb)
        self.write("shell.md", "# shell\n")
        distill.commit(self.kb, self.runtime, 1, "test", before)
        self.assertEqual(self.head_files(), ["shell.md"])
        staged = distill.git(self.kb, "diff", "--cached", "--name-only").stdout.split()
        self.assertEqual(staged, ["README.md"])

    def test_paths_with_spaces_survive(self):
        before = distill.dirty_paths(self.kb)
        self.write("my notes.md", "# notes\n")
        distill.commit(self.kb, self.runtime, 1, "test", before)
        self.assertEqual(self.head_files(), ["my notes.md"])

    def test_deletion_by_writer_is_committed(self):
        before = distill.dirty_paths(self.kb)
        (self.kb / "git.md").unlink()
        distill.commit(self.kb, self.runtime, 1, "test", before)
        self.assertEqual(self.head_files(), ["git.md"])
        self.assertEqual(distill.dirty_paths(self.kb), set())

    def test_nothing_of_ours_makes_no_commit(self):
        self.write("README.md", "only user work\n")
        before = distill.dirty_paths(self.kb)
        distill.commit(self.kb, self.runtime, 1, "test", before)
        self.assertEqual(self.head_subject(), "seed")

    def test_auto_commit_off_is_respected(self):
        distill.cfg.get = lambda key, default=None: {
            "auto_commit": False, "auto_push": False}.get(key, default)
        before = distill.dirty_paths(self.kb)
        self.write("shell.md", "# shell\n")
        distill.commit(self.kb, self.runtime, 1, "test", before)
        self.assertEqual(self.head_subject(), "seed")

    def test_non_repo_is_a_no_op(self):
        with tempfile.TemporaryDirectory() as plain:
            distill.commit(Path(plain), self.runtime, 1, "test", set())


class TestRouting(unittest.TestCase):
    """The knowledge base is its own routing table; there is no fixed list."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kb = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def document(self, filename, title, command, sig="aaaaaaaaaaaa"):
        kb.insert_entry(self.kb / filename, title, "Group",
                        kb.render_entry({"heading": "Do the thing",
                                         "commands": [command], "what": "x",
                                         "why": "y"}, sig))

    def test_an_existing_entry_routes_its_whole_binary(self):
        """Once `git status` is filed, every git command follows it."""
        self.document("git.md", "Git", "git status --short")
        got = kb.known_route({"binary": "git"}, self.kb)
        self.assertEqual(got, ("git.md", "Git"))

    def test_a_binary_the_list_never_knew_still_routes(self):
        """This is the case a hardcoded table cannot cover."""
        self.document("package-managers.md", "Package managers", "dnf install -y ripgrep")
        self.assertEqual(kb.known_route({"binary": "dnf"}, self.kb)[0],
                         "package-managers.md")

    def test_unknown_binary_has_no_route_yet(self):
        self.assertIsNone(kb.known_route({"binary": "nixos-rebuild"}, self.kb))

    def test_remembered_decisions_survive_before_any_entry_exists(self):
        kb.remember_route(self.kb, "nixos-rebuild", "nix.md")
        self.assertEqual(kb.known_route({"binary": "nixos-rebuild"}, self.kb)[0], "nix.md")

    def test_entries_win_over_a_stale_remembered_route(self):
        kb.remember_route(self.kb, "git", "wrong.md")
        self.document("git.md", "Git", "git status --short")
        self.assertEqual(kb.known_route({"binary": "git"}, self.kb)[0], "git.md")

    def test_title_is_read_back_from_the_file(self):
        self.document("kubernetes.md", "Kubernetes", "kubectl get pods")
        self.assertEqual(kb.known_route({"binary": "kubectl"}, self.kb)[1], "Kubernetes")

    def test_skipped_and_readme_never_become_routes(self):
        kb.note_skipped(self.kb, "bbbbbbbbbbbb", "date", "trivial")
        self.assertNotIn("date", kb.binary_index(self.kb))

    def test_filename_cannot_escape_the_knowledge_base(self):
        """Model-proposed names are sanitised, so they cannot traverse."""
        for hostile in ("../../etc/passwd", "/etc/shadow", "a/b/c", "..",
                        "....//....//x.md"):
            name = kb.safe_filename(hostile)
            self.assertNotIn("/", name, hostile)
            self.assertEqual(Path("/kb", name).resolve().parent, Path("/kb").resolve(), hostile)
        self.assertEqual(kb.safe_filename(""), "misc.md")
        self.assertEqual(kb.safe_filename("Shell.md"), "shell.md")
        self.assertEqual(kb.safe_filename("package managers"), "package-managers.md")

    def test_fallback_is_a_file_of_its_own(self):
        self.assertEqual(kb.fallback_route({"binary": "cargo"})[0], "cargo.md")

    def test_merge_moves_entries_and_repoints_routing(self):
        """A wrong decision must be correctable after the fact."""
        self.document("shell.md", "Shell", "rg -n foo", sig="111111111111")
        self.document("grep.md", "Grep", "grep -rn foo .", sig="222222222222")
        moved = kb.merge_file(self.kb, "grep.md", "shell.md")
        self.assertEqual(moved, 1)
        self.assertFalse((self.kb / "grep.md").exists())
        text = (self.kb / "shell.md").read_text()
        self.assertIn("222222222222", text, "signatures must survive the move")
        self.assertIn("111111111111", text)
        self.assertEqual(kb.known_route({"binary": "grep"}, self.kb)[0], "shell.md")

    def test_merge_is_a_no_op_for_a_missing_file(self):
        self.assertEqual(kb.merge_file(self.kb, "nope.md", "shell.md"), 0)

    def test_a_correction_outlives_the_classifier(self):
        kb.remember_route(self.kb, "dnf", "package-managers.md")
        self.assertEqual(kb.known_route({"binary": "dnf"}, self.kb)[0],
                         "package-managers.md")

    def test_exact_action_is_found_across_topic_files(self):
        self.document("utilities.md", "Utilities", "grep -rn foo .")
        found = kb.find_action(self.kb, "grep", [])
        self.assertEqual(found[0].name, "utilities.md")

    def test_new_action_asks_model_even_when_binary_has_route(self):
        self.document("old.md", "Old", "grep -rn foo .")
        record = {"binary": "grep", "subcommands": [], "command": "grep -n bar .",
                  "sig": "bbbbbbbbbbbb"}
        with patch.object(distill, "classify", return_value=("shell.md", "Shell")) as route, \
             patch.object(distill, "run_text", return_value=json.dumps({
                 "worth_documenting": True, "heading": "Find lines", "what": "Finds text",
                 "why": "Inspect a file", "section": "Searching"})):
            result = distill.document_record(self.kb, self.kb, record,
                                            {"name": "test"}, 1)
        self.assertEqual(result, "merged")  # same binary and subcommands across files
        route.assert_not_called()

    def test_route_failure_does_not_create_a_binary_file(self):
        record = {"binary": "raretool", "subcommands": ["run"],
                  "command": "raretool run", "sig": "bbbbbbbbbbbb"}
        with patch.object(distill, "classify", return_value=None):
            self.assertEqual(distill.document_record(self.kb, self.kb, record,
                                                    {"name": "test"}, 1), "failed")
        self.assertFalse((self.kb / "raretool.md").exists())

    def test_model_can_change_prior_route_for_new_action(self):
        self.document("old.md", "Old", "grep -rn foo .")
        record = {"binary": "grep", "subcommands": ["special"],
                  "command": "grep special bar", "sig": "bbbbbbbbbbbb"}
        answer = {"worth_documenting": True, "heading": "Special search",
                  "what": "Searches", "why": "Inspect text", "section": "Searching"}
        with patch.object(distill, "classify", return_value=("shell.md", "Shell")) as route, \
             patch.object(distill, "run_text", return_value=json.dumps(answer)):
            result = distill.document_record(self.kb, self.kb, record,
                                            {"name": "test"}, 1)
        self.assertEqual(result, "new")
        route.assert_called_once()
        self.assertTrue((self.kb / "shell.md").exists())

    def test_consolidation_apply_preserves_signatures_and_backs_up(self):
        self.document("shell.md", "Shell", "rg foo", sig="111111111111")
        self.document("grep.md", "Grep", "grep foo", sig="222222222222")
        runtime = self.kb / ".runtime"
        runtime.mkdir()
        data = {"schema": 1, "moves": [{"source": "grep.md", "destination": "shell.md",
                "entries": 1, "source_sha256": knowledge_organize.file_hash(self.kb / "grep.md"),
                "destination_sha256": knowledge_organize.file_hash(self.kb / "shell.md")}],
                "index_sha256": "", "routes_sha256": ""}
        data["sha256"] = knowledge_organize.proposal_hash(data)
        with patch.object(knowledge_organize.sync_seen, "main", return_value=0):
            count, backup = knowledge_organize.apply(self.kb, runtime, data, data["sha256"])
        self.assertEqual(count, 1)
        self.assertTrue(backup.exists())
        self.assertIn("222222222222", (self.kb / "shell.md").read_text())
        self.assertFalse((self.kb / "grep.md").exists())

    def test_consolidation_proposal_uses_model_choice(self):
        self.document("shell.md", "Shell", "rg foo", sig="111111111111")
        self.document("tool-a.md", "Tool A", "tool-a foo", sig="222222222222")
        runtime = self.kb / ".runtime"
        runtime.mkdir()
        with patch.object(distill, "classify", return_value=("shell.md", "Shell")) as choose:
            proposal = knowledge_organize.propose(self.kb, runtime, {"name": "test"})
        self.assertEqual(proposal["moves"][0]["source"], "tool-a.md")
        self.assertEqual(proposal["moves"][0]["destination"], "shell.md")
        self.assertEqual(proposal["moves"][0]["examples"], ["tool-a foo"])
        self.assertEqual(choose.call_args.kwargs["excluded"], {"tool-a.md"})

    def test_consolidation_rejects_changed_source(self):
        self.document("shell.md", "Shell", "rg foo", sig="111111111111")
        self.document("tool-a.md", "Tool A", "tool-a foo", sig="222222222222")
        runtime = self.kb / ".runtime"
        runtime.mkdir()
        with patch.object(distill, "classify", return_value=("shell.md", "Shell")):
            proposal = knowledge_organize.propose(self.kb, runtime, {"name": "test"})
        (self.kb / "tool-a.md").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "knowledge changed"):
            knowledge_organize.apply(self.kb, runtime, proposal, proposal["sha256"])

    def test_consolidation_select_rehashes_reviewed_subset(self):
        data = {"schema": 1, "moves": [{"source": "a.md"}, {"source": "b.md"}],
                "index_sha256": "x", "routes_sha256": "y"}
        data["sha256"] = knowledge_organize.proposal_hash(data)
        selected = knowledge_organize.select(data, {"b.md"})
        self.assertEqual([move["source"] for move in selected["moves"]], ["b.md"])
        self.assertNotEqual(selected["sha256"], data["sha256"])
        with self.assertRaises(ValueError):
            knowledge_organize.select(data, {"missing.md"})


class TestEntryParsing(unittest.TestCase):
    def test_parses_heading_sigs_and_commands(self):
        entries = kb.parse("## Committing\n\n" + ENTRY)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].heading, "Check what changed before committing")
        self.assertEqual(entries[0].sigs, ["aaaaaaaaaaaa"])
        self.assertEqual(entries[0].commands, ["git --no-pager diff --staged"])
        self.assertEqual(entries[0].section, "Committing")

    def test_multiple_sigs_on_one_entry(self):
        text = ENTRY.replace("<!-- sig: aaaaaaaaaaaa -->",
                             "<!-- sig: aaaaaaaaaaaa -->\n<!-- sig: bbbbbbbbbbbb -->")
        self.assertEqual(kb.parse(text)[0].sigs, ["aaaaaaaaaaaa", "bbbbbbbbbbbb"])

    def test_action_is_derived_from_the_command_block(self):
        self.assertEqual(kb.action_of(kb.parse(ENTRY)[0]), ("git", ("diff",)))

    def test_same_action_different_flags_is_a_match(self):
        """This is what stops a second entry being written for a variant."""
        entries = kb.parse(ENTRY)
        self.assertIsNotNone(kb.find_match(entries, "git", ["diff"]))

    def test_different_subcommand_is_not_a_match(self):
        self.assertIsNone(kb.find_match(kb.parse(ENTRY), "git", ["merge"]))


class TestKbMutation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.path = self.dir / "git.md"

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_sig_appends_and_is_idempotent(self):
        self.path.write_text("## Committing\n\n" + ENTRY, encoding="utf-8")
        head = "Check what changed before committing"
        self.assertTrue(kb.add_sig(self.path, "cccccccccccc", head))
        self.assertFalse(kb.add_sig(self.path, "cccccccccccc", head))
        entry = kb.parse(self.path.read_text())[0]
        self.assertEqual(entry.sigs, ["aaaaaaaaaaaa", "cccccccccccc"])
        self.assertIn("git --no-pager diff --staged", self.path.read_text())

    def test_insert_creates_file_with_header(self):
        kb.insert_entry(self.path, "Git", "Committing", ENTRY)
        text = self.path.read_text()
        self.assertTrue(text.startswith("# Git"))
        self.assertIn("## Committing", text)
        self.assertEqual(len(kb.parse(text)), 1)

    def test_insert_reuses_an_existing_section(self):
        kb.insert_entry(self.path, "Git", "Committing", ENTRY)
        kb.insert_entry(self.path, "Git", "Committing",
                        ENTRY.replace("aaaaaaaaaaaa", "dddddddddddd")
                             .replace("Check what changed", "Stage everything"))
        text = self.path.read_text()
        self.assertEqual(text.count("## Committing"), 1)
        self.assertEqual(len(kb.parse(text)), 2)

    def test_insert_preserves_earlier_entries(self):
        kb.insert_entry(self.path, "Git", "Committing", ENTRY)
        kb.insert_entry(self.path, "Git", "Branching",
                        ENTRY.replace("aaaaaaaaaaaa", "eeeeeeeeeeee"))
        self.assertIn("aaaaaaaaaaaa", self.path.read_text())
        self.assertIn("## Branching", self.path.read_text())

    def test_skipped_file_records_the_sig(self):
        kb.note_skipped(self.dir, "ffffffffffff", "date", "prints the time")
        self.assertIn("ffffffffffff", kb.documented_sigs(self.dir))

    def test_documented_sigs_spans_every_file(self):
        kb.insert_entry(self.path, "Git", "Committing", ENTRY)
        kb.insert_entry(self.dir / "node.md", "Node", "Builds",
                        ENTRY.replace("aaaaaaaaaaaa", "999999999999"))
        self.assertEqual(kb.documented_sigs(self.dir), {"aaaaaaaaaaaa", "999999999999"})


class TestModelResponseParsing(unittest.TestCase):
    """The model is untrusted output: every shape it emits must be handled."""

    GOOD = json.dumps({
        "worth_documenting": True, "skip_reason": "",
        "section": "Inspecting state", "heading": "Show the log compactly",
        "commands": ["git log --oneline -10"],
        "what": "Prints ten commits, one line each.",
        "why": "Fast overview.", "example": "git log --oneline -10", "notes": "",
    })

    def test_clean_response(self):
        fields, _, _status = distill.parse_fields(self.GOOD, "git log")
        self.assertEqual(fields["section"], "Inspecting state")
        self.assertEqual(fields["heading"], "Show the log compactly")

    def test_answer_wrapped_in_a_fence_or_chatter(self):
        for wrapped in ("```json\n" + self.GOOD + "\n```",
                        "Sure! Here is the JSON:\n\n" + self.GOOD,
                        self.GOOD + "\n\nLet me know if you need more."):
            fields, reason, _status = distill.parse_fields(wrapped, "git log")
            self.assertIsNotNone(fields, reason)
            self.assertEqual(fields["heading"], "Show the log compactly")

    def test_model_emitted_sig_is_stripped(self):
        """Python owns signatures; a hallucinated one must never survive."""
        polluted = self.GOOD.replace("Show the log compactly",
                                     "Show the log <!-- sig: deadbeefcafe -->")
        fields, _, _status = distill.parse_fields(polluted, "git log")
        self.assertNotIn("deadbeefcafe", json.dumps(fields))

    def test_skip_verdict_is_distinguished_from_malformed(self):
        """A verdict must not be retried, and garbage must not be recorded."""
        payload = json.dumps({"worth_documenting": False,
                              "skip_reason": "just prints the date"})
        fields, reason, status = distill.parse_fields(payload, "date")
        self.assertIsNone(fields)
        self.assertEqual(reason, "just prints the date")
        self.assertEqual(status, "skip")

        _f, _r, status = distill.parse_fields("I cannot help", "date")
        self.assertEqual(status, "malformed")

    def test_empty_commands_fall_back_to_the_captured_command(self):
        payload = json.loads(self.GOOD)
        payload["commands"] = []
        fields, _, _status = distill.parse_fields(json.dumps(payload), "git log --oneline")
        self.assertEqual(fields["commands"], ["git log --oneline"])

    def test_garbage_is_rejected_not_written(self):
        missing = json.loads(self.GOOD)
        missing["what"] = ""
        for junk in ("", "   ", "I cannot help with that.",
                     "{not json at all}", "[1,2,3]", json.dumps(missing)):
            fields, reason, _status = distill.parse_fields(junk, "cmd")
            self.assertIsNone(fields, junk)
            self.assertTrue(reason)


class TestDeterministicRendering(unittest.TestCase):
    """Layout comes from Python, so the model cannot produce a malformed entry."""

    FIELDS = {"heading": "Show the log compactly",
              "commands": ["git log --oneline -10", "git log --graph"],
              "what": "Prints ten commits.", "why": "Fast overview.",
              "example": "git log --oneline -10", "notes": "Needs --no-pager in CI."}

    def test_renders_a_parseable_entry(self):
        text = kb.render_entry(self.FIELDS, "abcdef123456")
        entry = kb.parse(text)[0]
        self.assertEqual(entry.heading, "Show the log compactly")
        self.assertEqual(entry.sigs, ["abcdef123456"])
        self.assertEqual(entry.commands, ["git log --oneline -10", "git log --graph"])

    def test_blank_notes_omits_the_bullet(self):
        text = kb.render_entry({**self.FIELDS, "notes": "  "}, "abcdef123456")
        self.assertNotIn("**Notes:**", text)

    def test_multiline_prose_is_flattened(self):
        text = kb.render_entry({**self.FIELDS, "what": "One.\n\nTwo."}, "abcdef123456")
        self.assertIn("- **What it does:** One. Two.", text)
        self.assertEqual(len(kb.parse(text)), 1)


class TestSectionCanonicalisation(unittest.TestCase):
    def test_exact_and_case_insensitive_match_reuse(self):
        self.assertEqual(kb.canonical_section("branching", ["Branching"]), "Branching")

    def test_near_duplicate_snaps_to_existing(self):
        for proposed in ("Remote and syncing", "Remotes and syncing.", "remotes  and syncing"):
            self.assertEqual(kb.canonical_section(proposed, ["Remotes and syncing"]),
                             "Remotes and syncing", proposed)

    def test_genuinely_new_section_is_kept(self):
        self.assertEqual(kb.canonical_section("Containers", ["Branching"]), "Containers")

    def test_related_but_differently_worded_sections_are_not_merged(self):
        """Deliberate: matching is conservative, so distinct groups survive.

        "Stashing and cleanup" vs "Stashing and saving work" scores ~0.59, well
        under the cutoff. Lowering it to catch this would also merge unrelated
        groups, so the prompt (which lists existing sections) is what prevents
        the duplicate, not the fuzzy match.
        """
        got = kb.canonical_section("Stashing and cleanup", ["Stashing and saving work"])
        self.assertEqual(got, "Stashing and cleanup")

    def test_empty_falls_back_to_default(self):
        self.assertEqual(kb.canonical_section("", []), kb.DEFAULT_SECTION)


class TestPauseSwitchAndLog(unittest.TestCase):
    """The user-facing on/off switch and the activity log."""

    def setUp(self):
        self.watcher_mock = patch.object(capture, "ensure_watcher")
        self.watcher_mock.start()
        self.addCleanup(self.watcher_mock.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.kb = Path(self.tmp.name)
        self.real_runtime = cfg.runtime_dir
        cfg.runtime_dir = lambda: self.kb / ".runtime"

    def tearDown(self):
        cfg.runtime_dir = self.real_runtime
        os.environ.pop("AI_SKILLS_CAPTURE_OFF", None)
        self.tmp.cleanup()

    def log_text(self):
        path = cfg.runtime_dir() / cfg.SESSION_LOG
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def test_pause_is_persistent_and_reversible(self):
        self.assertFalse(cfg.is_paused())
        cfg.set_paused(True, "testing")
        self.assertTrue(cfg.is_paused())
        self.assertIn("testing", (cfg.runtime_dir() / cfg.PAUSE_FILE).read_text())
        cfg.set_paused(False)
        self.assertFalse(cfg.is_paused())

    def test_resume_when_not_paused_is_harmless(self):
        cfg.set_paused(False)
        self.assertFalse(cfg.is_paused())

    def test_env_switch_is_process_local(self):
        """AI_SKILLS_CAPTURE_OFF stops this shell without pausing globally."""
        os.environ["AI_SKILLS_CAPTURE_OFF"] = "1"
        self.assertTrue(cfg.capture_off())
        self.assertFalse(cfg.is_paused(), "one shell must not pause every harness")

    def test_paused_stops_capture(self):
        cfg.set_paused(True)
        self.assertTrue(cfg.capture_off())

    def test_log_records_a_decision_per_line(self):
        cfg.session_log("new", "abc123abc123", "git", "git status --short", "devin")
        cfg.session_log("known", "abc123abc123", "git", "git status --short", "devin")
        lines = self.log_text().strip().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("new", lines[0])
        self.assertIn("known", lines[1])
        self.assertIn("git status --short", lines[0])

    def test_log_flattens_newlines_so_one_action_is_one_line(self):
        cfg.session_log("new", "abc123abc123", "sh", "line one\nline two", "devin")
        self.assertEqual(len(self.log_text().strip().splitlines()), 1)

    def test_log_never_raises(self):
        """It runs inside the agent tool loop; failure must be silent."""
        cfg.runtime_dir = lambda: Path("/definitely/not/writable/xyz")
        cfg.session_log("new", "x", "y", "z")     # must not raise

    def test_enqueue_logs_new_then_known(self):
        record = {"sig": "aabbccddeeff", "binary": "git", "command": "git status",
                  "harness": "devin", "kind": "shell", "tool": "exec"}
        self.assertEqual(capture.enqueue([dict(record)]), 1)
        self.assertEqual(capture.enqueue([dict(record)]), 0, "second time is a duplicate")
        text = self.log_text()
        self.assertIn("new", text)
        self.assertIn("known", text)

    def test_new_knowledge_base_ignores_private_runtime_files(self):
        """A separate KB must protect raw evidence, archives, and .env files."""
        sys.path.insert(0, str(BIN.parent))
        import install
        install.ensure_gitignore(self.kb)
        body = (self.kb / ".gitignore").read_text()
        for line in (".runtime/", "backups/", "playbacks/", ".env", ".env.*",
                     "!.env.example"):
            self.assertIn(line, body.splitlines())

    def test_existing_gitignore_is_extended_not_replaced(self):
        sys.path.insert(0, str(BIN.parent))
        import install
        (self.kb / ".gitignore").write_text("secrets.env\n", encoding="utf-8")
        install.ensure_gitignore(self.kb)
        body = (self.kb / ".gitignore").read_text()
        self.assertIn("secrets.env", body)
        self.assertIn(".runtime/", body)
        install.ensure_gitignore(self.kb)          # idempotent
        self.assertEqual(body, (self.kb / ".gitignore").read_text())

    def test_repeat_within_one_command_line_is_marked(self):
        record = {"sig": "112233445566", "binary": "tail", "command": "tail -5",
                  "harness": "devin", "kind": "shell", "tool": "exec"}
        capture.enqueue([dict(record), dict(record)])
        self.assertIn("repeat", self.log_text())


class TestSessionVerbs(unittest.TestCase):
    """The start/stop surface, driven exactly as a person or a hook would."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kb = Path(self.tmp.name)

    def tearDown(self):
        self.run_session("stop")
        self.tmp.cleanup()

    def run_session(self, *args):
        env = dict(os.environ, AI_SKILLS_KB=str(self.kb))
        env.pop("AI_SKILLS_CAPTURE_OFF", None)
        return subprocess.run([sys.executable, str(BIN / "session.py"), *args],
                              capture_output=True, text=True, env=env)

    def paused(self):
        return (self.kb / ".runtime" / "paused").exists()

    def test_stop_and_start_round_trip(self):
        self.assertEqual(self.run_session("stop", "testing").returncode, 0)
        self.assertTrue(self.paused())
        self.run_session("start")
        self.assertFalse(self.paused())

    def test_restart_replaces_the_watcher_and_stop_releases_it(self):
        self.assertEqual(self.run_session("start").returncode, 0)
        pidfile = self.kb / ".runtime" / "watcher.pid"
        first = int(pidfile.read_text())
        done = self.run_session("restart")
        self.assertEqual(done.returncode, 0, done.stderr)
        second = int(pidfile.read_text())
        self.assertNotEqual(first, second)
        self.assertFalse(procs.pid_alive(first))
        self.assertTrue(procs.pid_alive(second))
        self.assertEqual(self.run_session("stop").returncode, 0)
        self.assertFalse(procs.pid_alive(second))

    def test_aliases_all_work(self):
        for stop_word in ("stop", "pause", "off"):
            self.run_session(stop_word)
            self.assertTrue(self.paused(), stop_word)
            self.run_session("start")
        for start_word in ("start", "resume", "on"):
            self.run_session("stop")
            self.run_session(start_word)
            self.assertFalse(self.paused(), start_word)

    def test_a_typo_is_loud_rather_than_a_silent_no_op(self):
        """`stop` used to do nothing at all and still exit 0."""
        done = self.run_session("nonsense")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("unknown action", done.stderr)

    def test_stop_records_its_reason(self):
        self.run_session("stop", "reviewing", "a", "client", "repo")
        self.assertIn("reviewing a client repo",
                      (self.kb / ".runtime" / "paused").read_text())

    def test_hook_verbs_are_silent_and_never_fail(self):
        for verb in ("hook-start", "hook-end"):
            done = self.run_session(verb, "devin")
            self.assertEqual(done.returncode, 0, verb)
            self.assertEqual(done.stdout.strip(), "", verb)

    def test_a_legacy_shim_cannot_silently_restart_capture(self):
        """Old shims call `start <harness>`; that must stay a hook verb."""
        self.run_session("stop")
        self.run_session("start", "devin")
        self.assertTrue(self.paused())

    def test_status_reports_both_states(self):
        self.assertIn("on", self.run_session("status").stdout)
        self.run_session("stop")
        self.assertIn("PAUSED", self.run_session("status").stdout)


class TestHttpBackend(unittest.TestCase):
    """Regressions from wiring up local models."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.runtime = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def reply(self, payload):
        class FakeResponse:
            def read(inner):
                return json.dumps(payload).encode()

            def __enter__(inner):
                return inner

            def __exit__(inner, *a):
                return False
        return FakeResponse()

    def run_with(self, payload):
        real = distill.urllib.request.urlopen
        distill.urllib.request.urlopen = lambda *a, **k: self.reply(payload)
        try:
            return distill.run_http({"url": "http://x/api/generate", "model": "m"},
                                    "prompt", 5, self.runtime)
        finally:
            distill.urllib.request.urlopen = real

    def test_normal_reply_is_returned(self):
        self.assertEqual(self.run_with({"response": "hello", "done_reason": "stop"}), "hello")

    def test_token_limit_with_no_output_is_a_failure_not_a_verdict(self):
        """A thinking model can burn the whole budget and emit nothing."""
        got = self.run_with({"response": "", "done_reason": "length"})
        self.assertIsNone(got)
        self.assertIn("token limit", (self.runtime / "distill.log").read_text())

    def test_shipped_ollama_backend_has_no_output_cap(self):
        spec = cfg.DEFAULTS["writer"]["text_backends"]["ollama"]
        self.assertNotIn("num_predict", spec["options"],
                         "a token cap truncates reasoning models before they answer")
        self.assertEqual(spec["options"]["temperature"], 0)

    def test_text_backend_defers_prompt_file_substitution(self):
        """Each call writes its own prompt, so cfg must not bake in one path."""
        spec = {"prefer_text": ["fake"],
                "text_backends": {"fake": {"bin": sys.executable, "model": "m",
                                           "args": ["--prompt-file", "{prompt_file}"],
                                           "prompt": "file"}}}
        original = cfg.load
        cfg.load = lambda: {**original(), "writer": spec}
        try:
            got = cfg.writer_backend("text")
        finally:
            cfg.load = original
        self.assertIn("{prompt_file}", got["args"])


class TestTextModeDistillation(unittest.TestCase):
    """The whole text-mode loop, with a stub model instead of a real one."""

    RESPONSE = json.dumps({
        "worth_documenting": True, "section": "Inspecting state",
        "heading": "Show the log compactly", "commands": ["git log --oneline -10"],
        "what": "Prints ten commits.", "why": "Fast overview.",
        "example": "git log --oneline -10", "notes": "",
    })

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.runtime = self.dir / ".runtime"
        self.runtime.mkdir()
        self.real_run = distill.run_text
        self.real_choices = distill.route_choices
        distill.route_choices = lambda record, root, runtime, excluded=None: [
            (filename, kb.title_of(root, filename), []) for filename in
            ([kb.known_route(record, root)[0]] if kb.known_route(record, root) else [])]
        self.calls = []
        # Routing is a separate concern with its own tests; pin it here so
        # these tests count only the calls that write entries.
        for binary, filename in (("git", "git.md"), ("date", "shell.md")):
            kb.remember_route(self.dir, binary, filename)

    def tearDown(self):
        distill.run_text = self.real_run
        distill.route_choices = self.real_choices
        self.tmp.cleanup()

    def stub(self, reply):
        def fake(_backend, prompt, _timeout, _runtime, _schema=None):
            self.calls.append(prompt)
            if "organise a personal command reference" in prompt:
                filename = "git.md" if "binary:  git" in prompt else "shell.md"
                return json.dumps({"kind": "same-ecosystem", "file": filename,
                                   "title": filename[:-3].title(), "confidence": "clear"})
            return reply
        distill.run_text = fake

    def record(self, sig, binary, subcmds, command):
        return {"sig": sig, "binary": binary, "subcommands": subcmds,
                "command": command, "full_command": command, "tool": "exec", "ok": True}

    def test_documents_and_routes(self):
        self.stub(self.RESPONSE)
        distill.distill_text(self.dir, self.runtime,
                             [self.record("a1a1a1a1a1a1", "git", ["log"], "git log --oneline")],
                             {"name": "stub"}, 10)
        self.assertIn("a1a1a1a1a1a1", (self.dir / "git.md").read_text())

    def test_second_variant_merges_without_calling_the_model(self):
        self.stub(self.RESPONSE)
        first = self.record("b1b1b1b1b1b1", "git", ["log"], "git log --oneline")
        second = self.record("c1c1c1c1c1c1", "git", ["log"], "git log --oneline -20 --graph")
        distill.distill_text(self.dir, self.runtime, [first], {"name": "stub"}, 10)
        self.assertEqual(len(self.calls), 2)
        distill.distill_text(self.dir, self.runtime, [second], {"name": "stub"}, 10)
        self.assertEqual(len(self.calls), 2, "merge must not consult the model")
        text = (self.dir / "git.md").read_text()
        self.assertIn("c1c1c1c1c1c1", text)
        self.assertEqual(len(kb.parse(text)), 1, "a variant must not create a second entry")

    def test_already_documented_sig_is_untouched(self):
        self.stub(self.RESPONSE)
        rec = self.record("d1d1d1d1d1d1", "git", ["log"], "git log")
        distill.distill_text(self.dir, self.runtime, [rec], {"name": "stub"}, 10)
        before = (self.dir / "git.md").read_text()
        distill.distill_text(self.dir, self.runtime, [rec], {"name": "stub"}, 10)
        self.assertEqual((self.dir / "git.md").read_text(), before)

    def test_model_outage_is_not_recorded_as_skipped(self):
        """A dead model must leave the record for retry, not bury it in _skipped."""
        self.stub(None)
        rec = self.record("e1e1e1e1e1e1", "git", ["log"], "git log")
        done, failed = distill.distill_text(self.dir, self.runtime, [rec], {"name": "stub"}, 10)
        self.assertEqual(done, 0)
        self.assertEqual(failed, [rec])
        self.assertFalse((self.dir / kb.SKIPPED_FILE).exists())
        self.assertNotIn("e1e1e1e1e1e1", kb.documented_sigs(self.dir))

    def test_skip_verdict_is_recorded_so_it_never_returns(self):
        self.stub(json.dumps({"worth_documenting": False,
                              "skip_reason": "just prints the date"}))
        rec = self.record("f1f1f1f1f1f1", "date", [], "date")
        _done, failed = distill.distill_text(self.dir, self.runtime, [rec], {"name": "stub"}, 10)
        self.assertEqual(failed, [])
        self.assertIn("f1f1f1f1f1f1", kb.documented_sigs(self.dir))

    def test_malformed_reply_is_retried_under_the_schema(self):
        """Structure is guaranteed by falling back to constrained decoding."""
        attempts = []

        def fake(_backend, _prompt, _timeout, _runtime, schema=None):
            attempts.append(schema)
            if "organise a personal command reference" in _prompt:
                return json.dumps({"kind": "same-ecosystem", "file": "git.md",
                                   "title": "Git", "confidence": "clear"})
            return "sorry, no idea" if schema is None else self.RESPONSE
        distill.run_text = fake

        rec = self.record("9a9a9a9a9a9a", "git", ["log"], "git log")
        distill.distill_text(self.dir, self.runtime, [rec],
                             {"name": "stub", "url": "http://x"}, 10)
        self.assertEqual(len(attempts), 3, "route, then entry and one retry")
        self.assertIsNone(attempts[1], "first entry attempt is unconstrained")
        self.assertIsNotNone(attempts[2], "retry supplies the schema")
        self.assertIn("9a9a9a9a9a9a", (self.dir / "git.md").read_text())

    def test_skip_verdict_is_not_retried(self):
        attempts = []

        def fake(_backend, _prompt, _timeout, _runtime, schema=None):
            attempts.append(schema)
            if "organise a personal command reference" in _prompt:
                return json.dumps({"kind": "same-ecosystem", "file": "shell.md",
                                   "title": "Shell", "confidence": "clear"})
            return json.dumps({"worth_documenting": False, "skip_reason": "trivial"})
        distill.run_text = fake

        rec = self.record("8b8b8b8b8b8b", "date", [], "date")
        distill.distill_text(self.dir, self.runtime, [rec],
                             {"name": "stub", "url": "http://x"}, 10)
        self.assertEqual(len(attempts), 2, "a verdict must not trigger a retry")

    def test_unknown_binary_is_classified_for_each_new_action(self):
        prompts = []

        def fake(_backend, prompt, _timeout, _runtime, _schema=None):
            prompts.append(prompt)
            if "organise a personal command reference" in prompt:
                return json.dumps({"file": "package-managers.md",
                                   "title": "Package managers", "kind": "new-technology",
                                   "confidence": "clear"})
            return self.RESPONSE
        distill.run_text = fake

        first = self.record("c0c0c0c0c0c0", "dnf", ["install"], "dnf install -y rg")
        distill.distill_text(self.dir, self.runtime, [first], {"name": "stub"}, 10)
        self.assertTrue((self.dir / "package-managers.md").exists(),
                        "the model chose the file, not a hardcoded table")
        routing = [p for p in prompts if "organise a personal" in p]
        self.assertEqual(len(routing), 1)

        second = self.record("d0d0d0d0d0d0", "dnf", ["remove"], "dnf remove -y rg")
        distill.distill_text(self.dir, self.runtime, [second], {"name": "stub"}, 10)
        routing = [p for p in prompts if "organise a personal" in p]
        self.assertEqual(len(routing), 2, "a new action gets a fresh routing decision")
        self.assertIn("d0d0d0d0d0d0", (self.dir / "package-managers.md").read_text())

    def test_classifier_choice_is_sanitised(self):
        """A proposed path must not escape the knowledge base."""
        def fake(_backend, prompt, _timeout, _runtime, _schema=None):
            if "organise a personal command reference" in prompt:
                return json.dumps({"file": "../../etc/passwd", "title": "Nope",
                                   "kind": "new-technology", "confidence": "clear"})
            return self.RESPONSE
        distill.run_text = fake

        rec = self.record("e0e0e0e0e0e0", "weird", [], "weird --run")
        distill.distill_text(self.dir, self.runtime, [rec], {"name": "stub"}, 10)
        written = [p.name for p in self.dir.glob("*.md")]
        self.assertTrue(written)
        for name in written:
            self.assertNotIn("/", name)
        self.assertFalse((self.dir.parent / "etc").exists())

    def test_unreachable_classifier_keeps_record_for_retry(self):
        def fake(_backend, prompt, _timeout, _runtime, _schema=None):
            if "organise a personal command reference" in prompt:
                return None          # classifier unavailable
            return self.RESPONSE
        distill.run_text = fake

        rec = self.record("f0f0f0f0f0f0", "cargo", ["build"], "cargo build --release")
        _done, failed = distill.distill_text(self.dir, self.runtime, [rec],
                                             {"name": "stub"}, 10)
        self.assertEqual(failed, [rec])
        self.assertFalse((self.dir / "cargo.md").exists())

    def test_existing_sections_are_offered_to_the_model(self):
        self.stub(self.RESPONSE)
        distill.distill_text(self.dir, self.runtime,
                             [self.record("aaaa1111aaaa", "git", ["log"], "git log")],
                             {"name": "stub"}, 10)
        distill.distill_text(self.dir, self.runtime,
                             [self.record("bbbb2222bbbb", "git", ["merge"], "git merge main")],
                             {"name": "stub"}, 10)
        self.assertIn("Inspecting state", self.calls[-1],
                      "the model must see existing sections to avoid inventing near-duplicates")


class TestKnowledgeLayout(unittest.TestCase):
    def test_agent_prompt_uses_separate_runtime_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            knowledge, runtime = root / "knowledge", root / ".runtime"
            knowledge.mkdir()
            runtime.mkdir()
            prompt = distill.build_prompt(knowledge, runtime, 1).read_text(encoding="utf-8")
            self.assertIn((runtime / "batch.jsonl").as_posix(), prompt)
            self.assertNotIn("`.runtime/batch.jsonl`", prompt)

    def test_runtime_setting_is_relative_to_config(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(cfg, "get", return_value=".runtime"), \
                patch.object(cfg, "config_path", return_value=Path.cwd() / "config.json"):
            self.assertEqual(cfg.runtime_dir(), Path.cwd() / ".runtime")

    def test_explicit_kb_override_keeps_runtime_isolated(self):
        with patch.dict(os.environ, {"AI_SKILLS_KB": str(Path.cwd() / "isolated")}):
            self.assertEqual(cfg.runtime_dir(), Path.cwd() / "isolated" / ".runtime")

    def test_keyword_search_matches_whole_entries_and_filters_topics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "git.md").write_text(ENTRY, encoding="utf-8")
            (root / "_skipped.md").write_text(ENTRY, encoding="utf-8")
            results = knowledge_search.search(root, "git staged")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["path"].name, "git.md")
            self.assertEqual(knowledge_search.search(root, "git missingword"), [])
            self.assertEqual(knowledge_search.search(root, "git", "docker"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
