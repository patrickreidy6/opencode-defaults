import contextlib
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import publish_opencode_version as publisher
from tests.test_baseline import cli_env


class PublishVersionTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.remote = self.root / "remote"
        self.author = self.root / "author"
        self.git(self.root, "init", "--bare", "-b", "main", str(self.remote))
        self.git(self.root, "clone", str(self.remote), str(self.author))
        self.git(self.author, "config", "user.name", "Fixture")
        self.git(self.author, "config", "user.email", "fixture@example.invalid")
        self.git(self.author, "config", "commit.gpgSign", "false")
        (self.author / "baseline.json").write_bytes(b'{"opencode": "2.2.7"}\n')
        (self.author / "notes.md").write_bytes(b"original\n")
        self.git(self.author, "add", "baseline.json", "notes.md")
        self.git(self.author, "commit", "-m", "initial")
        self.git(self.author, "push", "origin", "main")
        self.base = self.git(self.remote, "rev-parse", "main")
        self.enter_patch(mock.patch.object(publisher, "PUBLISH_URLS", {str(self.remote)}))
        env = cli_env(self.root, "2.3.2", isolate=False)
        self.enter_patch(mock.patch.dict(os.environ, {**env, "GIT_ALLOW_PROTOCOL": "file"}))

    def enter_patch(self, patch):
        patch.start()
        self.addCleanup(patch.stop)

    def git(self, cwd, *args):
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                              text=True, check=True).stdout.strip()

    def publish(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            publisher.publish(self.author)
        return output.getvalue()

    def assert_published_pin(self, parent):
        tip = self.git(self.remote, "rev-parse", "main")
        self.assertEqual(self.git(self.remote, "rev-list", "--parents", "-1", tip), f"{tip} {parent}")
        self.assertEqual(self.git(self.remote, "diff", "--name-only", parent, tip), "baseline.json")
        self.assertEqual(self.git(self.remote, "show", "main:baseline.json"), '{"opencode": "2.3.2"}')
        return tip

    def test_publishes_only_pin_and_repeat_reports_same_revision(self):
        notes = self.author / "notes.md"
        notes.write_bytes(b"staged edit\n")
        self.git(self.author, "add", "notes.md")
        notes.write_bytes(b"unstaged edit\n")
        (self.author / "private.md").write_bytes(b"untracked\n")
        self.git(self.author, "tag", "-a", "local-tag", "-m", "local tag")
        self.git(self.author, "config", "push.followTags", "true")
        before = self.git(self.author, "status", "--porcelain")

        first = self.publish()
        tip = self.assert_published_pin(self.base)
        self.assertIn(f"Published OpenCode 2.3.2 on main at {tip}", first)
        self.assertEqual(self.git(self.author, "rev-parse", "HEAD"), tip)
        self.assertEqual(self.git(self.author, "status", "--porcelain"), before)
        self.assertEqual(self.git(self.author, "show", ":notes.md"), "staged edit")
        self.assertEqual(notes.read_bytes(), b"unstaged edit\n")
        self.assertEqual((self.author / "private.md").read_bytes(), b"untracked\n")
        self.assertEqual(self.git(self.remote, "tag", "--list"), "")
        self.assertIn(f"Already published OpenCode 2.3.2 on main at {tip}", self.publish())
        self.assertEqual(self.git(self.remote, "rev-parse", "main"), tip)
        self.assertEqual(self.git(self.author, "status", "--porcelain"), before)

    def test_unpublished_commits_and_conflicting_pin_edits_stay_local(self):
        (self.author / "notes.md").write_bytes(b"local history\n")
        self.git(self.author, "commit", "-am", "unpublished")
        local_tip = self.git(self.author, "rev-parse", "HEAD")
        pin = self.author / "baseline.json"
        pin.write_bytes(b'{"opencode": "9.0.0"}\n')
        self.git(self.author, "add", "baseline.json")
        pin.write_bytes(b'{"opencode": "9.0.1"}\n')
        before = self.git(self.author, "status", "--porcelain")

        message = self.publish()
        tip = self.assert_published_pin(self.base)
        self.assertIn(tip, message)
        self.assertIn("author checkout", message)
        self.assertIn(f"Already published OpenCode 2.3.2 on main at {tip}", self.publish())
        self.assertEqual(self.git(self.author, "rev-parse", "HEAD"), local_tip)
        self.assertEqual(self.git(self.author, "status", "--porcelain"), before)
        self.assertEqual(self.git(self.author, "show", ":baseline.json"), '{"opencode": "9.0.0"}')
        self.assertEqual(pin.read_bytes(), b'{"opencode": "9.0.1"}\n')

    def test_rejected_push_preserves_checkout_and_retry_uses_new_public_parent(self):
        (self.author / "notes.md").write_bytes(b"staged while publishing\n")
        self.git(self.author, "add", "notes.md")
        before = self.git(self.author, "status", "--porcelain")
        worktrees = self.git(self.author, "worktree", "list", "--porcelain")
        prepare = publisher.prepare_pin
        other = self.root / "other"
        self.git(self.root, "clone", str(self.remote), str(other))

        def advance_main(repo, parent, version):
            candidate = prepare(repo, parent, version)
            (other / "public.md").write_bytes(b"independent public commit\n")
            self.git(other, "add", "public.md")
            self.git(other, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                     "-c", "commit.gpgSign=false", "commit", "-m", "concurrent change")
            self.git(other, "push", "origin", "main")
            return candidate

        output = io.StringIO()
        with contextlib.redirect_stdout(output), mock.patch.object(publisher, "prepare_pin", advance_main):
            with self.assertRaisesRegex(publisher.PublishError, "push failed"):
                publisher.publish(self.author)
        self.assertEqual(output.getvalue(), "")
        public_tip = self.git(other, "rev-parse", "HEAD")
        self.assertEqual(self.git(self.remote, "rev-parse", "main"), public_tip)
        self.assertEqual(self.git(self.remote, "show", "main:baseline.json"), '{"opencode": "2.2.7"}')
        self.assertEqual(self.git(self.author, "rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git(self.author, "status", "--porcelain"), before)
        self.assertEqual(self.git(self.author, "worktree", "list", "--porcelain"), worktrees)
        message = self.publish()
        self.assertIn(self.assert_published_pin(public_tip), message)

    def test_unrecognized_version_or_wrong_push_destination_stops_publication(self):
        with mock.patch.object(publisher.install, "probe_opencode_version", return_value=("ok", "unknown")):
            with self.assertRaisesRegex(publisher.PublishError, "release version"):
                self.publish()
        self.git(self.author, "config", "--add", "remote.origin.pushurl", str(self.remote))
        self.git(self.author, "config", "--add", "remote.origin.pushurl", str(self.root / "elsewhere"))
        with self.assertRaisesRegex(publisher.PublishError, "destinations"):
            self.publish()
        self.assertEqual(self.git(self.remote, "rev-parse", "main"), self.base)


if __name__ == "__main__":
    unittest.main()
