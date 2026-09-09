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
import sys
import tempfile
import unittest
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import capture     # noqa: E402
import cfg         # noqa: E402
import distill     # noqa: E402
import json_merge  # noqa: E402
import procs       # noqa: E402


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


class TestLiveness(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
