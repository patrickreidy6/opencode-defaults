import contextlib
import hashlib
import io
import json
import os
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import install

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE: dict[str, bytes] = {
    "baseline.json": b'{"opencode": "2.2.7"}\n',
    "global/AGENTS.md": b"# Test defaults\n",
    "global/opencode.json": b'{"model": "openai/gpt-6-astra", "agents": {"title": {"model": "openai/gpt-6.1-sol#medium"}}, "plugins": ["managed-plugin"], "instructions": ["~/.config/opencode/AGENTS.local.md"], "mcp": {"servers": {"context7": {"type": "remote", "url": "https://mcp.context7.com/mcp"}}}}\n',
    "global/commands/xm-demo.md": b"Demo $ARGUMENTS.\n",
    ".opencode/skills/demo/SKILL.md": b"---\nname: demo\ndescription: Demo\n---\nBody\n",
}
FIXTURE_FINGERPRINT = "83483d0562b62bc84626144a38495270e1dd0a0411350d3b5e1b2c8a29ec842d"


def make_source(root: Path, files: dict[str, bytes] | None = None) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for rel, content in (DEFAULT_SOURCE if files is None else files).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    shutil.copy2(REPO_ROOT / "install.py", root / "install.py")
    return root


def run_installer(
    source: Path, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(source / "install.py"), *args],
        cwd=source,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def cli_env(
    tmp: Path,
    version: str | None,
    *,
    output: str | None = None,
    exit_code: int = 0,
    in_home: bool = False,
    isolate: bool = True,
) -> dict[str, str]:
    env = os.environ.copy()
    home = tmp / "home"
    bin_dir = tmp / "bin"
    home.mkdir(parents=True, exist_ok=True)
    bin_dir.mkdir(parents=True, exist_ok=True)
    if isolate:
        env.update(HOME=str(home), USERPROFILE=str(home), PATH=str(bin_dir))
    else:
        env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
    if version is not None:
        target_dir = home / ".opencode" / "bin" if in_home else bin_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        text = output if output is not None else f"opencode v{version}"
        if os.name == "nt":
            lines = ["@echo off", "setlocal DisableDelayedExpansion"]
            for line in text.splitlines():
                escaped = line.replace("^", "^^").replace("%", "%%")
                for char in "&|<>()":
                    escaped = escaped.replace(char, "^" + char)
                lines.append("echo(" + escaped)
            lines.append(f"exit /b {exit_code}")
            (target_dir / "opencode.cmd").write_text(
                "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
            )
        else:
            lines = ["#!/bin/sh"]
            if text:
                lines.append(f"printf '%s\\n' {shlex.quote(text)}")
            lines.append(f"exit {exit_code}")
            executable = target_dir / "opencode"
            executable.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
            executable.chmod(0o755)
    return env


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
        for path in root.rglob("*")
        if path.is_file()
    }


def section(output: str, name: str) -> list[str]:
    return [line for line in output.splitlines() if line.split() and line.split()[0] == name]


class FingerprintTests(unittest.TestCase):
    def test_fixed_fixture_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(install.compute_fingerprint(make_source(Path(tmp))), FIXTURE_FINGERPRINT)

    def test_stable_and_ignores_non_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = make_source(Path(tmp))
            original = install.compute_fingerprint(source)
            self.assertEqual(install.compute_fingerprint(source), original)
            non_inputs = {
                "README.md": b"Notes\n",
                "tests/x.py": b"# Test\n",
                "install.py": b"# Changed installer\n",
                "global/commands/notes.txt": b"Not a command\n",
                ".opencode/skills/demo/__pycache__/cached.pyc": b"Cache\n",
            }
            for rel, content in non_inputs.items():
                with self.subTest(rel=rel):
                    path = source / rel
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)
                    self.assertEqual(install.compute_fingerprint(source), original)

    def test_each_input_changes_value(self) -> None:
        for rel in DEFAULT_SOURCE:
            with self.subTest(rel=rel), tempfile.TemporaryDirectory() as tmp:
                source = make_source(Path(tmp))
                original = install.compute_fingerprint(source)
                path = source / rel
                path.write_bytes(path.read_bytes() + b"x")
                self.assertNotEqual(install.compute_fingerprint(source), original)

    def test_synthetic_copy_without_git_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = make_source(Path(tmp) / "source")
            copied = Path(tmp) / "copy"
            shutil.copytree(source, copied)
            for root in (source, copied):
                with self.subTest(root=root.name):
                    self.assertFalse((root / ".git").exists())
                    result = run_installer(root, "--fingerprint")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, FIXTURE_FINGERPRINT + "\n")
                    self.assertEqual(result.stderr, "")

    def test_repo_inputs_have_no_crlf(self) -> None:
        for rel, path in install.fingerprint_inputs(REPO_ROOT):
            self.assertNotIn(b"\r\n", path.read_bytes(), rel)

    def test_fingerprint_mode_prints_only_the_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = make_source(Path(tmp) / "source")
            env = cli_env(Path(tmp), None)
            env["XDG_CONFIG_HOME"] = str(Path(tmp) / "config")
            result = run_installer(source, "--fingerprint", env=env)
            self.assertEqual(
                (result.returncode, result.stdout), (0, install.compute_fingerprint(source) + "\n")
            )
            self.assertEqual(result.stderr, "")
            self.assertFalse((Path(tmp) / "config").exists())

    def test_bad_baseline_stops_every_mode_without_changes(self) -> None:
        bad_baselines = {
            "missing": None,
            "invalid-json": b"{",
            "array": b"[]",
            "invalid-utf8": b"\xff",
            "empty-object": b"{}",
            "number": b'{"opencode": 1}',
            "empty-version": b'{"opencode": ""}',
            "whitespace-version": b'{"opencode": "  "}',
            "extra-key": b'{"opencode": "2.2.7", "x": 1}',
            "duplicate-key": b'{"opencode": "2.2.7", "opencode": "2.2.8"}',
            "unreadable": "directory",
        }
        for name, content in bad_baselines.items():
            for populated in (False, True):
                for mode in ("install", "dry-run", "fingerprint"):
                    with self.subTest(baseline=name, populated=populated, mode=mode):
                        with tempfile.TemporaryDirectory() as tmp:
                            root = Path(tmp)
                            files = {key: value for key, value in DEFAULT_SOURCE.items() if key != "baseline.json"}
                            source = make_source(root / "source", files)
                            baseline = source / "baseline.json"
                            if isinstance(content, bytes):
                                baseline.write_bytes(content)
                            elif content == "directory":
                                baseline.mkdir()
                            destination = root / "config" / "opencode"
                            if populated:
                                destination.mkdir(parents=True)
                                (destination / "opencode.json").write_bytes(b'{"local": "keep"}\n')
                                (destination / "AGENTS.md").write_bytes(b"Local rules\n")
                            before = snapshot(destination)
                            env = cli_env(root, None)
                            env["XDG_CONFIG_HOME"] = str(root / "config")
                            args = ["--destination", str(destination)] if mode != "fingerprint" else []
                            if mode != "install":
                                args.append("--" + mode)
                            result = run_installer(source, *args, env=env)
                            self.assertEqual(result.returncode, 1, result.stderr)
                            self.assertIn("baseline.json", result.stderr)
                            self.assertNotIn("Traceback", result.stderr)
                            self.assertEqual(result.stdout, "")
                            self.assertEqual(snapshot(destination), before)
                            self.assertEqual(destination.exists(), populated)

    def test_fingerprint_usage_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = make_source(Path(tmp) / "source")
            destination = Path(tmp) / "destination"
            for args in (("--dry-run",), ("--destination", str(destination))):
                with self.subTest(args=args):
                    result = run_installer(source, "--fingerprint", *args)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("usage:", result.stderr)
                    self.assertFalse(destination.exists())

    def test_load_baseline_strips_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = make_source(Path(tmp), {**DEFAULT_SOURCE, "baseline.json": b'{"opencode": " 2.2.7 \\n"}\n'})
            self.assertEqual(install.load_baseline(source), "2.2.7")

    def test_managed_paths_and_sorted_source_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = make_source(Path(tmp))
            self.assertEqual(
                install.managed_files(source),
                {
                    "AGENTS.md": source / "global/AGENTS.md",
                    "commands/xm-demo.md": source / "global/commands/xm-demo.md",
                    "skills/demo/SKILL.md": source / ".opencode/skills/demo/SKILL.md",
                },
            )
            self.assertEqual(
                install.fingerprint_inputs(source),
                [(rel, source / rel) for rel in sorted(DEFAULT_SOURCE)],
            )

    def test_sha256_hashes_raw_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input"
            path.write_bytes(b"abc")
            self.assertEqual(
                install.sha256_file(path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

    def test_fingerprint_read_failure_is_concise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = make_source(Path(tmp))
            (source / "global" / "opencode.json").unlink()
            result = run_installer(source, "--fingerprint")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("opencode.json", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(result.stdout, "")


class ReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = make_source(self.root / "source")
        self.destination = self.root / "destination"
        self.destination.mkdir()
        self.receipt_path = self.destination / "opencode-defaults-receipt.json"

    def receipt_data(self) -> dict:
        return {
            "format": 1,
            "fingerprint": FIXTURE_FINGERPRINT,
            "files": {
                rel: hashlib.sha256(DEFAULT_SOURCE[source]).hexdigest()
                for rel, source in {
                    "AGENTS.md": "global/AGENTS.md",
                    "commands/xm-demo.md": "global/commands/xm-demo.md",
                    "skills/demo/SKILL.md": ".opencode/skills/demo/SKILL.md",
                }.items()
            },
            "config": json.loads(DEFAULT_SOURCE["global/opencode.json"]),
        }

    def seed_receipt(self, **overrides) -> None:
        self.receipt_path.write_text(
            json.dumps({**self.receipt_data(), **overrides}), encoding="utf-8"
        )

    def run_install(self, *, dry_run: bool = False) -> tuple[int, str, str]:
        self.assertTrue(hasattr(install, "run_install"), "run_install interface is missing")
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = install.run_install(self.source, self.destination, dry_run=dry_run)
        return code, stdout.getvalue(), stderr.getvalue()

    def symlink(self, link: Path, target: Path, *, directory: bool = False) -> None:
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlinks unavailable: {type(exc).__name__}")

    def test_install_writes_receipt(self) -> None:
        (self.destination / "opencode.json").write_text('{"local": "keep"}', encoding="utf-8")
        result = run_installer(self.source, "--destination", str(self.destination))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.receipt_path.is_file(), "Successful install must publish a receipt")
        data = json.loads(self.receipt_path.read_bytes())
        self.assertEqual(data, self.receipt_data())
        self.assertEqual(data["fingerprint"], install.compute_fingerprint(self.source))
        self.assertEqual(
            data["files"],
            {rel: install.sha256_file(path) for rel, path in install.managed_files(self.source).items()},
        )
        self.assertEqual(
            self.receipt_path.read_bytes(),
            (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )
        receipt = install.read_receipt(self.destination)
        self.assertEqual(receipt, install.Receipt(data["fingerprint"], data["files"], data["config"]))

    def test_repeat_install_keeps_receipt_and_backs_up_previous(self) -> None:
        self.assertEqual(self.run_install()[0], 0)
        previous = self.receipt_path.read_bytes()
        self.assertEqual(self.run_install()[0], 0)
        self.assertEqual(self.receipt_path.read_bytes(), previous)
        backups = list((self.destination / "backups").glob("harness-*/opencode-defaults-receipt.json"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), previous)
        self.assertEqual((backups[0].parent / "AGENTS.md").read_bytes(), DEFAULT_SOURCE["global/AGENTS.md"])
        self.assertTrue((backups[0].parent / "opencode.json").is_file())

    def test_dry_run_writes_no_receipt(self) -> None:
        (self.destination / "opencode.json").write_bytes(b'{"local": "keep"}\n')
        before = snapshot(self.destination)
        result = run_installer(self.source, "--destination", str(self.destination), "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(snapshot(self.destination), before)
        self.assertFalse(self.receipt_path.exists())
        self.assertFalse((self.destination / "backups").exists())

    def test_damaged_receipt_stops_install_and_dry_run(self) -> None:
        valid = self.receipt_data()
        cases = {
            "invalid-json": b"not json SECRET_RECEIPT_VALUE",
            "invalid-utf8": b"\xff",
            "non-json-number": {**valid, "fingerprint": "a" * 64, "config": {"private": float("nan")}},
            "oversized-integer": b'{"format": ' + b"9" * 5000 + b"}",
            "array": [],
            "missing-fields": {},
            "unsupported-format": {**valid, "format": 2},
            "boolean-format": {**valid, "format": True},
            "float-format": {**valid, "format": 1.0},
            "files-array": {**valid, "files": []},
            "hash-number": {**valid, "files": {"AGENTS.md": 1}},
            "uppercase-hash": {**valid, "files": {"AGENTS.md": "A" * 64}},
            "short-hash": {**valid, "files": {"AGENTS.md": "a" * 63}},
            "bad-fingerprint": {**valid, "fingerprint": "XYZ"},
            "non-string-fingerprint": {**valid, "fingerprint": 1},
            "config-array": {**valid, "config": []},
            "directory": None,
        }
        for path in ("../escape", "/abs", "C:/x", "x\\y", "", ".", "./x", "a/../b", "a/./b", "a//b", "a/", "a\x00b"):
            cases[f"path-{path!r}"] = {**valid, "files": {path: "a" * 64}}
        for name, data in cases.items():
            for dry_run in (False, True):
                with self.subTest(case=name, dry_run=dry_run), tempfile.TemporaryDirectory(dir=self.root) as tmp:
                    self.destination = Path(tmp)
                    self.receipt_path = self.destination / "opencode-defaults-receipt.json"
                    if data is None:
                        self.receipt_path.mkdir()
                    else:
                        self.receipt_path.write_bytes(data if isinstance(data, bytes) else json.dumps(data).encode())
                    before = snapshot(self.destination)
                    args = ["--destination", str(self.destination)] + (["--dry-run"] if dry_run else [])
                    result = run_installer(self.source, *args)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(self.receipt_path.name, result.stderr)
                    self.assertIn("backups", result.stderr)
                    self.assertIn("automatic retirement history will be lost", result.stderr)
                    self.assertNotIn("SECRET_RECEIPT_VALUE", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(snapshot(self.destination), before)
                    self.assertFalse((self.destination / "backups").exists())
                    if data is None:
                        self.assertTrue(self.receipt_path.is_dir())
                        self.receipt_path.rmdir()
                    else:
                        self.receipt_path.unlink()

    def test_broken_receipt_symlink_is_not_bootstrap(self) -> None:
        self.symlink(self.receipt_path, self.root / "missing")
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run):
                code, _, stderr = self.run_install(dry_run=dry_run)
                self.assertEqual(code, 1)
                self.assertIn(self.receipt_path.name, stderr)
                self.assertIn("backups", stderr)
                self.assertTrue(self.receipt_path.is_symlink())
                self.assertEqual(list(self.destination.iterdir()), [self.receipt_path])

    def test_receipt_read_error_stops_before_writes(self) -> None:
        self.seed_receipt()
        before = snapshot(self.destination)
        original = Path.read_text

        def denied(path, *args, **kwargs):
            if path == self.receipt_path:
                raise PermissionError("SECRET_READ_ERROR")
            return original(path, *args, **kwargs)

        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run), mock.patch.object(Path, "read_text", denied), \
                    mock.patch("install.backup_file") as backup, \
                    mock.patch("install.shutil.copy2") as copy_file, \
                    mock.patch("install.os.replace") as replace:
                code, _, stderr = self.run_install(dry_run=dry_run)
                self.assertEqual(code, 1)
                self.assertIn(self.receipt_path.name, stderr)
                self.assertIn("backups", stderr)
                self.assertNotIn("SECRET_READ_ERROR", stderr)
                backup.assert_not_called()
                copy_file.assert_not_called()
                replace.assert_not_called()
        self.assertEqual(snapshot(self.destination), before)

    def test_receipt_lstat_error_is_not_absence(self) -> None:
        self.seed_receipt()
        before = snapshot(self.destination)
        original = Path.lstat

        def denied(path, *args, **kwargs):
            if path == self.receipt_path:
                raise PermissionError("SECRET_INSPECTION_ERROR")
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, "lstat", denied):
            for dry_run in (False, True):
                code, _, stderr = self.run_install(dry_run=dry_run)
                self.assertEqual(code, 1)
                self.assertIn("backups", stderr)
                self.assertNotIn("SECRET_INSPECTION_ERROR", stderr)
        self.assertEqual(snapshot(self.destination), before)

    def test_receipt_rejects_missing_path_resolving_outside_destination(self) -> None:
        self.seed_receipt(fingerprint="a" * 64, files={"missing/file.md": "b" * 64})
        original = Path.resolve

        def outside(path, *args, **kwargs):
            if path == self.destination / "missing/file.md":
                return self.root / "outside/file.md"
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, "resolve", outside):
            with self.assertRaises(install.ReceiptError):
                install.read_receipt(self.destination)

    def test_same_fingerprint_with_wrong_metadata_stops_install(self) -> None:
        for overrides in ({"files": {"AGENTS.md": "a" * 64}}, {"config": {"secret": "SECRET_CONFIG"}}):
            for dry_run in (False, True):
                with self.subTest(overrides=tuple(overrides), dry_run=dry_run):
                    self.seed_receipt(**overrides)
                    before = snapshot(self.destination)
                    code, _, stderr = self.run_install(dry_run=dry_run)
                    self.assertEqual(code, 1)
                    self.assertIn(self.receipt_path.name, stderr)
                    self.assertIn("inconsistent", stderr)
                    self.assertNotIn("SECRET_CONFIG", stderr)
                    self.assertEqual(snapshot(self.destination), before)

    def test_valid_historical_receipt_allows_upgrade(self) -> None:
        self.assertEqual(self.run_install()[0], 0)
        previous = self.receipt_path.read_bytes()
        (self.source / "global/commands/xm-demo.md").write_bytes(b"Updated command\n")
        code, _, stderr = self.run_install()
        self.assertEqual(code, 0, stderr)
        self.assertNotEqual(self.receipt_path.read_bytes(), previous)
        self.assertEqual(json.loads(self.receipt_path.read_bytes())["fingerprint"], install.compute_fingerprint(self.source))
        backups = list((self.destination / "backups").glob("harness-*/opencode-defaults-receipt.json"))
        self.assertEqual([path.read_bytes() for path in backups], [previous])

    def test_failed_verification_keeps_old_receipt(self) -> None:
        self.assertEqual(self.run_install()[0], 0)
        previous = self.receipt_path.read_bytes()
        with mock.patch("install.verify_installed", return_value=["AGENTS.md"]):
            code, _, stderr = self.run_install()
        self.assertEqual(code, 1)
        self.assertIn("AGENTS.md", stderr)
        self.assertEqual(self.receipt_path.read_bytes(), previous)
        self.assertEqual(list((self.destination / "backups").glob("harness-*/opencode-defaults-receipt.json")), [])

    def test_written_config_is_verified_before_receipt(self) -> None:
        (self.destination / "opencode.json").write_bytes(b'{"plugins": ["local-plugin"]}\n')
        self.assertEqual(self.run_install()[0], 0)
        previous = self.receipt_path.read_bytes()
        original = Path.write_text

        def reorder(path, text, *args, **kwargs):
            if path == self.destination / "opencode.json":
                config = json.loads(text)
                config["plugins"].reverse()
                text = json.dumps(config)
            return original(path, text, *args, **kwargs)

        with mock.patch.object(Path, "write_text", reorder):
            code, _, stderr = self.run_install()
        self.assertEqual(code, 1)
        self.assertIn("opencode.json", stderr)
        self.assertNotIn("local-plugin", stderr)
        self.assertEqual(self.receipt_path.read_bytes(), previous)

    def test_failed_receipt_replace_keeps_previous(self) -> None:
        self.assertEqual(self.run_install()[0], 0)
        previous = self.receipt_path.read_bytes()
        sentinel = self.receipt_path.with_suffix(".json.tmp")
        sentinel.write_bytes(b"Pre-existing temporary file\n")
        before_names = {path.name for path in self.destination.iterdir()} | {"backups"}
        with mock.patch("install.os.replace", side_effect=OSError("SECRET_REPLACE_ERROR")):
            code, _, stderr = self.run_install()
        self.assertEqual(code, 1)
        self.assertIn(self.receipt_path.name, stderr)
        self.assertNotIn("SECRET_REPLACE_ERROR", stderr)
        self.assertEqual(self.receipt_path.read_bytes(), previous)
        self.assertEqual(sentinel.read_bytes(), b"Pre-existing temporary file\n")
        self.assertEqual({path.name for path in self.destination.iterdir()}, before_names)
        backups = list((self.destination / "backups").glob("harness-*/opencode-defaults-receipt.json"))
        self.assertEqual([path.read_bytes() for path in backups], [previous])

    def test_successful_replace_does_not_clean_someone_elses_temp_file(self) -> None:
        original = os.replace
        reused_paths = []

        def replace_and_reuse(source, target):
            original(source, target)
            Path(source).write_bytes(b"New unrelated file\n")
            reused_paths.append(Path(source))

        with mock.patch("install.os.replace", replace_and_reuse):
            code, _, stderr = self.run_install()
        self.assertEqual(code, 0, stderr)
        self.assertEqual(json.loads(self.receipt_path.read_bytes()), self.receipt_data())
        self.assertEqual(len(reused_paths), 1)
        self.assertTrue(reused_paths[0].is_file(), "A successful rename ends ownership of the temporary path")
        self.assertEqual(reused_paths[0].read_bytes(), b"New unrelated file\n")

    def test_receipt_rejects_managed_symlinks_before_writes(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "kept.md").write_bytes(b"Keep outside content\n")
        for parent in (False, True):
            with self.subTest(parent=parent):
                link = self.destination / "linked"
                self.symlink(link, outside if parent else outside / "kept.md", directory=parent)
                self.seed_receipt(fingerprint="a" * 64, files={"linked/kept.md" if parent else "linked": "b" * 64})
                before = snapshot(self.destination)
                for dry_run in (False, True):
                    code, _, stderr = self.run_install(dry_run=dry_run)
                    self.assertEqual(code, 1)
                    self.assertIn(self.receipt_path.name, stderr)
                    self.assertEqual(snapshot(self.destination), before)
                    self.assertTrue(link.is_symlink())
                    self.assertEqual((outside / "kept.md").read_bytes(), b"Keep outside content\n")
                link.unlink()

    def test_bootstrap_validates_incoming_paths_before_writes(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        self.symlink(self.destination / "commands", outside, directory=True)
        before = snapshot(self.destination)
        for dry_run in (False, True):
            code, _, stderr = self.run_install(dry_run=dry_run)
            self.assertEqual(code, 1)
            self.assertIn("commands", stderr)
            self.assertEqual(snapshot(self.destination), before)
            self.assertEqual(list(outside.iterdir()), [])
            self.assertFalse((self.destination / "backups").exists())

    def test_retired_paths_are_validated_before_writes(self) -> None:
        retired = self.destination / "skills/coder"
        retired.mkdir(parents=True)
        (retired / "SKILL.md").write_bytes(b"Retired content\n")
        before = snapshot(self.destination)
        original = Path.lstat

        def linked(path, *args, **kwargs):
            state = original(path, *args, **kwargs)
            if path == retired:
                return os.stat_result((stat.S_IFLNK | 0o777, *state[1:]))
            return state

        for dry_run in (True, False):
            with self.subTest(dry_run=dry_run), mock.patch.object(Path, "lstat", linked):
                code, _, stderr = self.run_install(dry_run=dry_run)
                self.assertEqual(code, 1)
                self.assertIn("coder", stderr)
                self.assertEqual(snapshot(self.destination), before)

    def test_existing_local_agents_path_is_preserved(self) -> None:
        local = self.destination / "AGENTS.local.md"
        local.mkdir()
        (local / "unowned").write_bytes(b"Keep local content\n")
        (self.destination / "AGENTS.md").write_bytes(b"Custom rules\n")
        before = snapshot(local)
        code, _, stderr = self.run_install()
        self.assertEqual(code, 0, stderr)
        self.assertEqual(snapshot(local), before)

    def test_verify_installed_reports_sorted_bad_paths(self) -> None:
        self.assertTrue(hasattr(install, "verify_installed"), "verify_installed interface is missing")
        (self.destination / "good").write_bytes(b"abc")
        (self.destination / "changed").write_bytes(b"changed")
        (self.destination / "directory").mkdir()
        (self.destination / "unreadable").write_bytes(b"abc")
        expected_hash = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        expected = {name: expected_hash for name in ("unreadable", "missing", "directory", "changed", "good")}
        original = Path.read_bytes

        def denied(path):
            if path.name == "unreadable":
                raise PermissionError("unreadable")
            return original(path)

        with mock.patch.object(Path, "read_bytes", denied):
            self.assertEqual(install.verify_installed(self.destination, expected), ["changed", "directory", "missing", "unreadable"])

    def test_verify_installed_does_not_follow_symlinks(self) -> None:
        (self.destination / "good").write_bytes(b"abc")
        self.symlink(self.destination / "link", self.destination / "good")
        self.symlink(self.destination / "parent", self.root / "source", directory=True)
        self.assertTrue(hasattr(install, "verify_installed"), "verify_installed interface is missing")
        self.assertEqual(
            install.verify_installed(self.destination, {"link": "a" * 64, "parent/global/AGENTS.md": "a" * 64}),
            ["link", "parent/global/AGENTS.md"],
        )

    def test_invalid_config_stops_before_writes(self) -> None:
        for path in (self.source / "global/opencode.json", self.destination / "opencode.json"):
            for content in (b'["SECRET_CONFIG"]', b'{"SECRET_CONFIG":', b"\xff", b'{"SECRET_CONFIG": NaN}'):
                for dry_run in (False, True):
                    with self.subTest(path=path, content=content, dry_run=dry_run):
                        path.write_bytes(content)
                        before = snapshot(self.destination)
                        code, _, stderr = self.run_install(dry_run=dry_run)
                        self.assertEqual(code, 1)
                        self.assertIn("opencode.json", stderr)
                        self.assertNotIn("SECRET_CONFIG", stderr)
                        self.assertNotIn("Traceback", stderr)
                        self.assertEqual(snapshot(self.destination), before)
            if path.is_relative_to(self.source):
                path.write_bytes(DEFAULT_SOURCE["global/opencode.json"])

    def test_copy_error_keeps_old_receipt_without_traceback(self) -> None:
        self.assertEqual(self.run_install()[0], 0)
        previous = self.receipt_path.read_bytes()
        original = shutil.copy2

        def denied(source, target, *args, **kwargs):
            if Path(source).is_relative_to(self.source):
                raise OSError("SECRET_COPY_ERROR")
            return original(source, target, *args, **kwargs)

        with mock.patch("install.shutil.copy2", denied):
            code, _, stderr = self.run_install()
        self.assertEqual(code, 1)
        self.assertIn("AGENTS.md", stderr)
        self.assertNotIn("SECRET_COPY_ERROR", stderr)
        self.assertNotIn("Traceback", stderr)
        self.assertEqual(self.receipt_path.read_bytes(), previous)


if __name__ == "__main__":
    unittest.main()
