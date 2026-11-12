import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
