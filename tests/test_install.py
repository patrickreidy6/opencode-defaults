import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from install import merge_settings

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL_PY = REPO_ROOT / "install.py"
SUPERPOWERS_PACKAGE = "superpowers@git+https://github.com/obra/superpowers.git"
PINNED_SUPERPOWERS = SUPERPOWERS_PACKAGE + "#22f0b463e7a5e579904dd6211a520321035526f7"


class InstallHarnessTests(unittest.TestCase):
    def run_installer(
        self, *args: str, env: dict[str, str] | None = None, repo_root: Path = REPO_ROOT
    ) -> subprocess.CompletedProcess[str]:
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            [sys.executable, str(repo_root / "install.py"), *args],
            cwd=repo_root,
            env=merged_env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_dry_run_makes_no_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "opencode-dest"
            res = self.run_installer("--destination", str(dest), "--dry-run")
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertFalse(dest.exists())

    def test_xdg_config_home_default_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            xdg = Path(tmp) / "xdg"
            res = self.run_installer(env={"XDG_CONFIG_HOME": str(xdg)})
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertTrue((xdg / "opencode" / "opencode.json").is_file())
            self.assertTrue((xdg / "opencode" / "AGENTS.md").is_file())

    def test_refuses_when_opencode_jsonc_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            (dest / "opencode.jsonc").write_text("{}\n", encoding="utf-8")
            res = self.run_installer("--destination", str(dest))
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("opencode.jsonc", res.stderr + res.stdout)

    def test_merges_config_unions_arrays_cleans_legacy_v1_and_backs_up(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            existing_cfg = {
                "small_model": "openai/old-small",
                "experimental": {"openTelemetry": True, "todo": True},
                "plugins": [
                    "superpowers@git+https://github.com/obra/superpowers.git",
                    "local-custom-plugin",
                ],
                "instructions": ["~/custom-rules.md"],
                "providers": {"openrouter": {"settings": {"apiKey": "{env:OPENROUTER_API_KEY}"}}},
                "mcp": {
                    "context7": {"type": "remote", "url": "https://mcp.context7.com/mcp", "enabled": True},
                    "gmail": {"type": "remote", "url": "https://gmailmcp.googleapis.com/mcp/v1", "enabled": True},
                    "servers": {
                        "playwright": {"type": "local", "command": ["npx", "@playwright/mcp"]}
                    },
                },
            }
            (dest / "opencode.json").write_text(json.dumps(existing_cfg, indent=2), encoding="utf-8")
            (dest / "service.json").write_text('{"port":28894}\n', encoding="utf-8")
            (dest / "commands").mkdir()
            (dest / "commands" / "add-notes.md").write_text("keep me\n", encoding="utf-8")
            (dest / "AGENTS.md").write_text("# Personal workflow\nPointer to pr7\n", encoding="utf-8")

            res = self.run_installer("--destination", str(dest))
            self.assertEqual(res.returncode, 0, res.stderr)

            merged = json.loads((dest / "opencode.json").read_text(encoding="utf-8"))
            self.assertEqual(merged["$schema"], "https://opencode.ai/config.json")
            self.assertEqual(merged["model"], "openai/gpt-6-astra")
            self.assertEqual(merged["agents"]["title"]["model"], "openai/gpt-6.1-sol#medium")
            self.assertEqual(merged["agents"]["explore"]["model"], "openai/gpt-6-astra#medium")
            self.assertEqual(merged["agents"]["general"]["model"], "openai/gpt-6-astra#high")
            self.assertNotIn("small_model", merged)
            self.assertEqual(merged["experimental"], {"todo": True})

            self.assertEqual(
                merged["plugins"],
                [
                    PINNED_SUPERPOWERS,
                    "local-custom-plugin",
                ],
            )
            self.assertEqual(
                merged["instructions"],
                [
                    "~/.config/opencode/AGENTS.local.md",
                    "~/custom-rules.md",
                ],
            )
            self.assertIn("openrouter", merged["providers"])
            self.assertNotIn("context7", merged["mcp"])
            self.assertNotIn("gmail", merged["mcp"])
            self.assertIn("context7", merged["mcp"]["servers"])
            self.assertIn("playwright", merged["mcp"]["servers"])

            # Custom non-pr4 AGENTS.md migrated to AGENTS.local.md and backed up
            self.assertEqual(
                (dest / "AGENTS.local.md").read_text(encoding="utf-8"),
                "# Personal workflow\nPointer to pr7\n",
            )
            self.assertIn("# Personal OpenCode Defaults", (dest / "AGENTS.md").read_text(encoding="utf-8"))

            # Unrelated files untouched
            self.assertEqual((dest / "service.json").read_text(encoding="utf-8"), '{"port":28894}\n')
            self.assertEqual((dest / "commands" / "add-notes.md").read_text(encoding="utf-8"), "keep me\n")

            # Backup created for overwritten opencode.json and AGENTS.md
            backups = list((dest / "backups").glob("harness-*"))
            self.assertEqual(len(backups), 1)
            self.assertTrue((backups[0] / "opencode.json").is_file())
            self.assertTrue((backups[0] / "AGENTS.md").is_file())

            # Skills deployed
            for skill_name in (
                "writer",
                "frontend-design",
                "data-preferences",
                "project-setup",
                "skill-authoring",
                "naming-files",
                "naming-directories",
                "socratic-tutor",
            ):
                self.assertTrue((dest / "skills" / skill_name / "SKILL.md").is_file(), skill_name)
            self.assertTrue((dest / "skills" / "socratic-tutor" / "LICENSE.md").is_file())
            self.assertTrue(
                (dest / "skills" / "frontend-design" / "references" / "ui-preferences.md").is_file()
            )
            self.assertTrue(
                (dest / "skills" / "project-setup" / "references" / "preferred-devtools.md").is_file()
            )
            self.assertEqual(
                (dest / "skills" / "project-setup" / "SKILL.md").read_bytes(),
                (REPO_ROOT / ".opencode" / "skills" / "project-setup" / "SKILL.md").read_bytes(),
            )
            self.assertEqual(
                (dest / "skills" / "project-setup" / "references" / "preferred-devtools.md").read_bytes(),
                (REPO_ROOT / ".opencode" / "skills" / "project-setup" / "references" / "preferred-devtools.md").read_bytes(),
            )

            # Second run is idempotent and preserves AGENTS.local.md
            res2 = self.run_installer("--destination", str(dest))
            self.assertEqual(res2.returncode, 0, res2.stderr)
            self.assertEqual(
                (dest / "AGENTS.local.md").read_text(encoding="utf-8"),
                "# Personal workflow\nPointer to pr7\n",
            )
            merged2 = json.loads((dest / "opencode.json").read_text(encoding="utf-8"))
            self.assertEqual(merged2["plugins"], merged["plugins"])
            self.assertEqual(merged2["instructions"], merged["instructions"])
            self.assertEqual(
                (dest / "skills" / "project-setup" / "SKILL.md").read_bytes(),
                (REPO_ROOT / ".opencode" / "skills" / "project-setup" / "SKILL.md").read_bytes(),
            )
            self.assertEqual(
                (dest / "skills" / "project-setup" / "references" / "preferred-devtools.md").read_bytes(),
                (REPO_ROOT / ".opencode" / "skills" / "project-setup" / "references" / "preferred-devtools.md").read_bytes(),
            )

    def test_commands_install_back_up_and_preserve_local_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "source"
            commands = repo / "global" / "commands"
            commands.mkdir(parents=True)
            shutil.copy2(INSTALL_PY, repo / "install.py")
            (repo / "global" / "opencode.json").write_text("{}\n", encoding="utf-8")
            (repo / "global" / "AGENTS.md").write_text("# Test defaults\n", encoding="utf-8")
            payloads = {
                "xm-review.md": b"---\ndescription: Review\n---\nReview $ARGUMENTS.\n",
                "xm-plan.md": b"---\ndescription: Plan\n---\nPlan $ARGUMENTS.\n",
            }
            for name, content in payloads.items():
                (commands / name).write_bytes(content)
            (commands / "notes.txt").write_text("not a command", encoding="utf-8")
            (commands / "directory.md").mkdir()

            dest = Path(tmp) / "destination"
            (dest / "commands").mkdir(parents=True)
            old_command = b"Previous managed command\n"
            local_command = b"Unrelated local command\n"
            (dest / "commands" / "xm-review.md").write_bytes(old_command)
            (dest / "commands" / "add-notes.md").write_bytes(local_command)

            preview = self.run_installer("--destination", str(dest), "--dry-run", repo_root=repo)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertIn(str(dest / "commands" / "xm-plan.md"), preview.stdout)
            self.assertFalse((dest / "opencode.json").exists())
            self.assertFalse((dest / "backups").exists())
            self.assertEqual((dest / "commands" / "xm-review.md").read_bytes(), old_command)
            self.assertFalse((dest / "commands" / "xm-plan.md").exists())

            installed = self.run_installer("--destination", str(dest), repo_root=repo)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            self.assertEqual(
                {p.name for p in (dest / "commands").iterdir()},
                {"xm-review.md", "xm-plan.md", "add-notes.md"},
            )
            for name, content in payloads.items():
                self.assertEqual((dest / "commands" / name).read_bytes(), content)
            self.assertEqual((dest / "commands" / "add-notes.md").read_bytes(), local_command)
            backups = list((dest / "backups").glob("harness-*/commands/xm-review.md"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), old_command)

            repeated = self.run_installer("--destination", str(dest), repo_root=repo)
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            for name, content in payloads.items():
                self.assertEqual((dest / "commands" / name).read_bytes(), content)
            self.assertEqual((dest / "commands" / "add-notes.md").read_bytes(), local_command)

    def test_superpowers_pin_converges_on_fresh_installs_and_migrations(self) -> None:
        old_pin = SUPERPOWERS_PACKAGE + "#" + "1" * 40
        cases = {
            "fresh": None,
            "other_plugins_only": [],
            "floating": [SUPERPOWERS_PACKAGE],
            "old_pin": [old_pin],
            "multiple": [SUPERPOWERS_PACKAGE, old_pin, PINNED_SUPERPOWERS, SUPERPOWERS_PACKAGE + "#main"],
            "already_pinned": [PINNED_SUPERPOWERS],
        }
        unrelated = [
            "local-first",
            "superpowers-helper",
            "superpowers@git+https://github.com/example/superpowers.git#custom",
            "superpowers@git+https://github.com/obra/superpowers.git-extra",
            {"package": "local-last", "options": {"enabled": True}},
            "-superpowers",
        ]
        for name, previous in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                dest = Path(tmp)
                config_path = dest / "opencode.json"
                original = None
                if previous is not None:
                    existing = {"plugins": [unrelated[0], *previous, *unrelated[1:]]}
                    original = (json.dumps(existing, indent=2) + "\n").encode("utf-8")
                    config_path.write_bytes(original)

                preview = self.run_installer("--destination", str(dest), "--dry-run")
                self.assertEqual(preview.returncode, 0, preview.stderr)
                self.assertEqual(sorted(p.name for p in dest.iterdir()), [] if original is None else ["opencode.json"])
                if original is not None:
                    self.assertEqual(config_path.read_bytes(), original)

                result = self.run_installer("--destination", str(dest))
                self.assertEqual(result.returncode, 0, result.stderr)
                expected = [PINNED_SUPERPOWERS, *(unrelated if previous is not None else [])]
                installed = json.loads(config_path.read_text(encoding="utf-8"))
                self.assertEqual(installed["plugins"], expected)
                if original is not None:
                    backups = list((dest / "backups").glob("harness-*/opencode.json"))
                    self.assertEqual(len(backups), 1)
                    self.assertEqual(backups[0].read_bytes(), original)

                repeated = self.run_installer("--destination", str(dest))
                self.assertEqual(repeated.returncode, 0, repeated.stderr)
                self.assertEqual(json.loads(config_path.read_text(encoding="utf-8")), installed)

    def test_next_superpowers_pin_replaces_current_pin(self) -> None:
        next_pin = SUPERPOWERS_PACKAGE + "#" + "2" * 40
        current = {"plugins": [PINNED_SUPERPOWERS, "custom-plugin"]}
        incoming = {"plugins": [next_pin]}

        merged = merge_settings(current, incoming)

        self.assertEqual(merged["plugins"], [next_pin, "custom-plugin"])
        self.assertEqual(current, {"plugins": [PINNED_SUPERPOWERS, "custom-plugin"]})
        self.assertEqual(incoming, {"plugins": [next_pin]})

    def test_superpowers_reference_is_preserved_without_incoming_managed_plugin(self) -> None:
        current = {"plugins": [SUPERPOWERS_PACKAGE], "instructions": [SUPERPOWERS_PACKAGE]}
        incoming = {"plugins": ["custom-plugin"], "instructions": ["custom-rules.md"]}

        merged = merge_settings(current, incoming)

        self.assertEqual(merged["plugins"], ["custom-plugin", SUPERPOWERS_PACKAGE])
        self.assertEqual(merged["instructions"], ["custom-rules.md", SUPERPOWERS_PACKAGE])

    def test_wrappers_ps1_and_sh(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ps_dest = Path(tmp) / "ps-dest"
            ps_whatif = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(REPO_ROOT / "install.ps1"),
                    "-Destination",
                    str(ps_dest),
                    "-WhatIf",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(ps_whatif.returncode, 0, ps_whatif.stderr)
            self.assertFalse(ps_dest.exists())

            ps_run = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(REPO_ROOT / "install.ps1"),
                    "-Destination",
                    str(ps_dest),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(ps_run.returncode, 0, ps_run.stderr)
            self.assertTrue((ps_dest / "opencode.json").is_file())

            sh_exe = shutil.which("sh") or r"C:\Program Files\Git\bin\sh.exe"
            if Path(sh_exe).exists():
                sh_dest = Path(tmp) / "sh-dest"
                sh_run = subprocess.run(
                    [sh_exe, "./install.sh", "--destination", sh_dest.as_posix()],
                    cwd=REPO_ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(sh_run.returncode, 0, sh_run.stderr)
                self.assertTrue((sh_dest / "opencode.json").is_file())

    def test_bom_tolerance_nested_list_replacement_and_retired_pr4_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            existing_cfg = {
                "skills": ["~/extra-skills"],
                "mcp": {
                    "servers": {
                        "context7": {
                            "type": "local",
                            "command": ["old-cmd", "--old-flag"],
                        }
                    }
                },
            }
            # Write with UTF-8 BOM (as Windows PowerShell 5.1 Set-Content -Encoding UTF8 does)
            (dest / "opencode.json").write_text(json.dumps(existing_cfg), encoding="utf-8-sig")
            (dest / "AGENTS.md").write_text(
                "# Personal OpenCode Defaults\nOld pr4 rules\n", encoding="utf-8-sig"
            )

            # Seed retired pr4-owned skills/commands alongside unrelated user command
            for retired_skill in ("coder", "design", "researcher", "deep-research"):
                d = dest / "skills" / retired_skill
                d.mkdir(parents=True)
                (d / "SKILL.md").write_text("old\n", encoding="utf-8")
            (dest / "commands").mkdir()
            (dest / "commands" / "sessions-move.md").write_text("old\n", encoding="utf-8")
            (dest / "commands" / "add-notes.md").write_text("keep\n", encoding="utf-8")

            res = self.run_installer("--destination", str(dest))
            self.assertEqual(res.returncode, 0, res.stderr)

            # BOM-encoded pr4 AGENTS.md must NOT be misclassified as custom AGENTS.local.md
            self.assertFalse((dest / "AGENTS.local.md").exists())

            merged = json.loads((dest / "opencode.json").read_text(encoding="utf-8"))
            self.assertEqual(merged["skills"], ["~/extra-skills"])
            self.assertEqual(
                merged["mcp"]["servers"]["context7"],
                {"type": "remote", "url": "https://mcp.context7.com/mcp"},
            )

            # Retired pr4 skills/commands backed up and removed; unrelated add-notes.md kept
            for retired_skill in ("coder", "design", "researcher", "deep-research"):
                self.assertFalse((dest / "skills" / retired_skill).exists(), retired_skill)
            self.assertFalse((dest / "commands" / "sessions-move.md").exists())
            self.assertTrue((dest / "commands" / "add-notes.md").is_file())

    @unittest.skipUnless(sys.platform == "win32", "Windows PowerShell fallback test")
    def test_install_ps1_without_uv_falls_back_past_windowsapps_stub(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "ps-no-uv"
            py_dir = str(Path(sys.executable).resolve().parent)
            win_apps = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps")
            sys_root = os.environ.get("SystemRoot", r"C:\Windows")
            ps_dir = os.path.join(sys_root, "System32", "WindowsPowerShell", "v1.0")
            minimal_path = os.pathsep.join([win_apps, py_dir, os.path.join(sys_root, "System32"), ps_dir])
            env = os.environ.copy()
            env["PATH"] = minimal_path

            ps_run = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(REPO_ROOT / "install.ps1"),
                    "-Destination",
                    str(dest),
                    "-WhatIf",
                ],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(ps_run.returncode, 0, ps_run.stderr + ps_run.stdout)


if __name__ == "__main__":
    unittest.main()
