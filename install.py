#!/usr/bin/env python3
"""Cross-platform installer for the opencode-defaults OpenCode V2 global harness."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

BASELINE_FILE = "baseline.json"
RECEIPT_NAME = "opencode-defaults-receipt.json"
RECEIPT_FORMAT = 1
CHECK_SCOPE_NOTE = "Covers the installed global baseline and CLI version only; the running server version, project or system overrides, environment substitutions, plugin loading, MCP connectivity, provider access and model behavior are not checked. Detects accidental drift only (not tamper-proof)."
LOCAL_SCAN_DIRS = ("agents", "commands", "skills", "plugins")
SKIP_PARTS = {"__pycache__", "node_modules", ".venv", ".git"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".pyd"}
PR4_AGENTS_HEADER = "# Personal OpenCode Defaults"
UNION_ROOT_LIST_KEYS = {"plugins", "instructions", "skills"}
SUPERPOWERS_PACKAGE = "superpowers@git+https://github.com/obra/superpowers.git"
RETIRED_PR4_DIRS = (
    Path("skills/coder"),
    Path("skills/design"),
    Path("skills/researcher"),
    Path("skills/deep-research"),
)
RETIRED_PR4_FILES = (
    Path("commands/sessions-move.md"),
    Path("preferences/UI_PREFERENCES.md"),
    Path("preferences/DATA_PREFERENCES.md"),
    Path("guides/skill-authoring.md"),
)


class BaselineError(Exception):
    """The source baseline is missing, unreadable or invalid."""


def load_baseline(repo_root: Path) -> str:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result = dict(pairs)
        if len(result) != len(pairs):
            raise BaselineError(f"{BASELINE_FILE}: duplicate keys are not allowed")
        return result

    try:
        text = (repo_root / BASELINE_FILE).read_text(encoding="utf-8")
        baseline = json.loads(text, object_pairs_hook=unique_object)
    except OSError as exc:
        raise BaselineError(f"{BASELINE_FILE}: {exc.strerror or 'unable to read file'}") from None
    except UnicodeDecodeError:
        raise BaselineError(f"{BASELINE_FILE}: invalid UTF-8") from None
    except json.JSONDecodeError as exc:
        raise BaselineError(f"{BASELINE_FILE}: invalid JSON ({exc.msg})") from None

    if not isinstance(baseline, dict) or set(baseline) != {"opencode"}:
        raise BaselineError(f"{BASELINE_FILE}: expected an object with only the opencode key")
    version = baseline["opencode"]
    if not isinstance(version, str) or not version.strip():
        raise BaselineError(f"{BASELINE_FILE}: opencode must be a nonempty version string")
    return version.strip()


def default_destination() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    if xdg:
        xdg_path = Path(xdg).expanduser()
        if xdg_path.is_absolute():
            return (xdg_path / "opencode").resolve()
    return (Path.home() / ".config" / "opencode").resolve()


def clean_legacy_v1_keys(config: dict[str, Any]) -> None:
    config.pop("small_model", None)

    experimental = config.get("experimental")
    if isinstance(experimental, dict):
        experimental.pop("openTelemetry", None)
        if not experimental:
            config.pop("experimental", None)

    mcp = config.get("mcp")
    if isinstance(mcp, dict):
        mcp.pop("context7", None)
        mcp.pop("gmail", None)


def is_managed_superpowers_plugin(plugin: Any) -> bool:
    return isinstance(plugin, str) and plugin.partition("#")[0] == SUPERPOWERS_PACKAGE


def merge_settings(
    current: dict[str, Any],
    incoming: dict[str, Any],
    *,
    path: tuple[str, ...] = (),
) -> dict[str, Any]:
    is_root = len(path) == 0
    result = copy.deepcopy(current)
    if is_root:
        clean_legacy_v1_keys(result)

    for key, in_val in incoming.items():
        # Each MCP server object under mcp.servers.<name> is an atomic definition
        if path == ("mcp", "servers"):
            result[key] = copy.deepcopy(in_val)
        elif key not in result:
            result[key] = copy.deepcopy(in_val)
        elif isinstance(result[key], dict) and isinstance(in_val, dict):
            result[key] = merge_settings(result[key], in_val, path=(*path, key))
        elif is_root and key in UNION_ROOT_LIST_KEYS and isinstance(result[key], list) and isinstance(in_val, list):
            merged_list = copy.deepcopy(in_val)
            replace_superpowers = key == "plugins" and any(is_managed_superpowers_plugin(p) for p in in_val)
            for item in result[key]:
                # The repository selects one Superpowers revision; do not retain previous references.
                if replace_superpowers and is_managed_superpowers_plugin(item):
                    continue
                if item not in merged_list:
                    merged_list.append(copy.deepcopy(item))
            result[key] = merged_list
        else:
            result[key] = copy.deepcopy(in_val)

    if is_root and "$schema" in result:
        schema = result.pop("$schema")
        result = {"$schema": schema, **result}

    return result


def json_equal(value: Any, other: Any) -> bool:
    """Compare parsed JSON structurally, preserving types and array order."""
    if type(value) is not type(other):
        return False
    if isinstance(value, dict):
        return value.keys() == other.keys() and all(json_equal(value[key], other[key]) for key in value)
    if isinstance(value, list):
        return len(value) == len(other) and all(json_equal(item, other_item) for item, other_item in zip(value, other))
    return value == other


def retire_settings(
    current: dict[str, Any], previous: dict[str, Any], incoming: dict[str, Any]
) -> tuple[dict[str, Any], list[str], list[str]]:
    """Remove unchanged settings dropped by the baseline, retaining local edits."""
    result = copy.deepcopy(current)
    removed: list[str] = []
    kept: list[str] = []

    def walk(now: dict[str, Any], old: dict[str, Any], new: dict[str, Any], path: tuple[str, ...]) -> None:
        for key, old_value in old.items():
            if key not in now:
                continue
            value = now[key]
            display = ".".join((*path, key))
            dropped = key not in new
            new_value = new.get(key)
            atomic_retirement = path == ("mcp", "servers") and dropped
            if not path and key in UNION_ROOT_LIST_KEYS and isinstance(value, list) and isinstance(old_value, list):
                if dropped or isinstance(new_value, list):
                    incoming_items = [] if dropped else new_value
                    remaining = [item for item in value if item not in old_value or item in incoming_items]
                    count = len(value) - len(remaining)
                    if count:
                        removed.append(f"{display} (-{count})")
                        if remaining:
                            now[key] = remaining
                        else:
                            del now[key]
            elif not atomic_retirement and isinstance(value, dict) and isinstance(old_value, dict) and (
                dropped or isinstance(new_value, dict)
            ):
                was_nonempty = bool(value)
                walk(value, old_value, {} if dropped else new_value, (*path, key))
                if was_nonempty and not value:
                    del now[key]
            elif dropped:
                if json_equal(value, old_value):
                    del now[key]
                    removed.append(display)
                else:
                    kept.append(display)

    walk(result, previous, incoming, ())
    return result, removed, kept


def collect_files(repo_root: Path) -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = [
        (repo_root / "global" / "AGENTS.md", Path("AGENTS.md")),
    ]
    commands_root = repo_root / "global" / "commands"
    for path in sorted(commands_root.glob("*.md")):
        if path.is_file():
            files.append((path, Path("commands") / path.name))
    skills_root = repo_root / ".opencode" / "skills"
    if skills_root.is_dir():
        for path in sorted(skills_root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(skills_root)
            if any(part in SKIP_PARTS for part in rel.parts) or path.suffix in SKIP_SUFFIXES:
                continue
            files.append((path, Path("skills") / rel))
    return files


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def managed_files(repo_root: Path) -> dict[str, Path]:
    return {rel.as_posix(): source for source, rel in collect_files(repo_root)}


def fingerprint_inputs(repo_root: Path) -> list[tuple[str, Path]]:
    sources = [source for source, _ in collect_files(repo_root)]
    sources.extend((repo_root / "global" / "opencode.json", repo_root / BASELINE_FILE))
    return sorted((source.relative_to(repo_root).as_posix(), source) for source in sources)


def compute_fingerprint(repo_root: Path) -> str:
    manifest = "".join(f"{sha256_file(path)}  {rel}\n" for rel, path in fingerprint_inputs(repo_root))
    return hashlib.sha256(manifest.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Receipt:
    fingerprint: str
    files: dict[str, str]
    config: dict[str, Any]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Receipt):
            return NotImplemented
        return (
            self.fingerprint == other.fingerprint
            and self.files == other.files
            and json_equal(self.config, other.config)
        )


class ReceiptError(Exception):
    """An existing receipt cannot safely establish installation history."""


class InstallError(Exception):
    """An installation cannot proceed; the message contains no setting values."""


def reject_json_constant(value: str) -> Any:
    raise ValueError("non-finite numbers are not valid JSON")


def path_state(destination: Path, rel: str, *, allow_leaf_link: bool = False) -> os.stat_result | None:
    """Inspect a canonical relative path without traversing links or junctions."""
    if (
        not isinstance(rel, str)
        or not rel
        or any(char in rel for char in ("\\", ":", "\x00"))
        or any(part in ("", ".", "..") for part in rel.split("/"))
    ):
        raise ValueError("expected a canonical relative POSIX path")

    target = destination
    parts = rel.split("/")
    for index in range(len(parts) + 1):
        try:
            state = target.lstat()
        except FileNotFoundError:
            state = None
            break
        if stat.S_ISLNK(state.st_mode) or getattr(state, "st_reparse_tag", 0) == 0xA0000003:
            if allow_leaf_link and index == len(parts):
                return state
            raise ValueError("symlinks and directory junctions are not allowed")
        if index < len(parts):
            if not stat.S_ISDIR(state.st_mode):
                raise ValueError("parent is not a directory")
            target /= parts[index]

    if not (destination / rel).resolve().is_relative_to(destination.resolve()):
        raise ValueError("path resolves outside the destination")
    return state


def read_receipt(destination: Path) -> Receipt | None:
    path = destination / RECEIPT_NAME
    try:
        state = path.lstat()
    except FileNotFoundError:
        return None
    except OSError:
        raise ReceiptError(f"{path}: unable to inspect receipt") from None
    if not stat.S_ISREG(state.st_mode):
        raise ReceiptError(f"{path}: expected a non-symlink regular file")
    try:
        data = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_json_constant)
    except OSError:
        raise ReceiptError(f"{path}: unable to read receipt") from None
    except UnicodeError:
        raise ReceiptError(f"{path}: invalid UTF-8") from None
    except (ValueError, RecursionError):
        raise ReceiptError(f"{path}: invalid JSON") from None

    if not isinstance(data, dict) or not {"format", "fingerprint", "files", "config"} <= data.keys():
        raise ReceiptError(f"{path}: expected an object containing format, fingerprint, files and config")
    if type(data["format"]) is not int or data["format"] != RECEIPT_FORMAT:
        raise ReceiptError(f"{path}: unsupported receipt format")
    if not isinstance(data["files"], dict) or not isinstance(data["config"], dict):
        raise ReceiptError(f"{path}: files and config must be objects")
    if not isinstance(data["fingerprint"], str) or not re.fullmatch(r"[0-9a-f]{64}", data["fingerprint"]):
        raise ReceiptError(f"{path}: invalid fingerprint")
    for rel, digest in data["files"].items():
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ReceiptError(f"{path}: invalid managed file hash")
        try:
            path_state(destination, rel)
        except (OSError, ValueError, UnicodeError):
            raise ReceiptError(f"{path}: invalid or inaccessible managed file path") from None
    return Receipt(data["fingerprint"], data["files"], data["config"])


def plan_file_retirement(destination: Path, receipt: Receipt, managed: set[str]) -> tuple[list[str], list[str]]:
    removed: list[str] = []
    kept: list[str] = []
    for rel in sorted(receipt.files.keys() - managed):
        target = destination / rel
        try:
            state = path_state(destination, rel)
            if state is None:
                continue
            if not stat.S_ISREG(state.st_mode):
                raise InstallError(f"{target}: expected a non-symlink regular retired file")
            unchanged = sha256_file(target) == receipt.files[rel]
        except (OSError, ValueError, UnicodeError):
            raise InstallError(f"{target}: unable to inspect or read retired file safely") from None
        (removed if unchanged else kept).append(rel)
    return removed, kept


def write_receipt(destination: Path, receipt: Receipt) -> None:
    data = {
        "format": RECEIPT_FORMAT,
        "fingerprint": receipt.fingerprint,
        "files": receipt.files,
        "config": receipt.config,
    }
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=destination,
            prefix=f".{RECEIPT_NAME}.", suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(json.dumps(data, indent=2, sort_keys=True) + "\n")
        os.replace(temporary, destination / RECEIPT_NAME)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def verify_installed(destination: Path, expected: dict[str, str]) -> list[str]:
    failures = []
    for rel, digest in expected.items():
        try:
            state = path_state(destination, rel)
            if state is None or not stat.S_ISREG(state.st_mode) or sha256_file(destination / rel) != digest:
                failures.append(rel)
        except (OSError, ValueError, UnicodeError):
            failures.append(rel)
    return sorted(failures)


def read_config(path: Path) -> dict[str, Any]:
    try:
        config = json.loads(path.read_text(encoding="utf-8-sig"), parse_constant=reject_json_constant)
    except (ValueError, RecursionError):
        raise InstallError(f"{path}: expected valid UTF-8 JSON") from None
    if not isinstance(config, dict):
        raise InstallError(f"{path}: expected a JSON object")
    return config


def probe_opencode_version(timeout: float = 10.0) -> tuple[Literal["ok", "missing", "failed"], str]:
    executable = shutil.which("opencode") or shutil.which("opencode", path=str(Path.home() / ".opencode" / "bin"))
    if executable is None:
        return "missing", ""
    try:
        result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired, UnicodeError):
        return "failed", ""
    words = result.stdout.split()
    if result.returncode or not words:
        return "failed", ""
    version = words[-1].removeprefix("v")
    return ("ok", version) if version else ("failed", "")


def config_drift_paths(installed: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    differences: list[str] = []

    def walk(current: dict[str, Any], wanted: dict[str, Any], path: tuple[str, ...]) -> None:
        for key in current.keys() | wanted.keys():
            child = (*path, key)
            if key not in current or key not in wanted:
                differences.append(".".join(child))
            elif not json_equal(current[key], wanted[key]):
                if path != ("mcp", "servers") and isinstance(current[key], dict) and isinstance(wanted[key], dict):
                    walk(current[key], wanted[key], child)
                else:
                    differences.append(".".join(child))

    walk(installed, expected, ())
    return sorted(differences)


def list_local_additions(
    destination: Path, installed_cfg: dict[str, Any] | None, baseline_cfg: dict[str, Any], managed: set[str]
) -> list[str]:
    additions: set[str] = set()

    def config_walk(current: dict[str, Any], baseline: dict[str, Any], path: tuple[str, ...]) -> None:
        for key, value in current.items():
            child = (*path, key)
            display = ".".join(child)
            if not path and key in UNION_ROOT_LIST_KEYS and isinstance(value, list):
                base_list = baseline.get(key, [])
                if isinstance(base_list, list):
                    count = sum(item not in base_list for item in value)
                    if count:
                        additions.add(f"{key} (+{count})")
            elif key not in baseline:
                additions.add(display)
            elif path != ("mcp", "servers") and isinstance(value, dict) and isinstance(baseline[key], dict):
                config_walk(value, baseline[key], child)

    if installed_cfg is not None:
        config_walk(installed_cfg, baseline_cfg, ())

    prefixes = {rel[:index] for rel in managed for index, char in enumerate(rel) if char == "/"}

    def file_walk(rel: str, *, container: bool = False) -> None:
        if rel in managed:
            return
        target = destination / rel
        try:
            state = path_state(destination, rel, allow_leaf_link=True)
            if state is None:
                return
            if stat.S_ISLNK(state.st_mode) or getattr(state, "st_reparse_tag", 0) == 0xA0000003:
                additions.add(rel)
            elif stat.S_ISDIR(state.st_mode):
                if container or rel in prefixes:
                    for child in target.iterdir():
                        file_walk(f"{rel}/{child.name}")
                elif next(target.iterdir(), None) is not None:
                    additions.add(rel + "/")
            else:
                additions.add(rel)
        except (OSError, ValueError, RuntimeError):
            raise InstallError(f"{target}: unable to inspect local additions safely") from None

    for root in LOCAL_SCAN_DIRS:
        file_walk(root, container=True)
    try:
        if path_state(destination, "AGENTS.local.md", allow_leaf_link=True) is not None:
            additions.add("AGENTS.local.md")
    except (OSError, ValueError, RuntimeError):
        raise InstallError(f"{destination / 'AGENTS.local.md'}: unable to inspect local additions safely") from None
    return sorted(additions)


def run_check(repo_root: Path, destination: Path, expect: str | None) -> int:
    findings: dict[str, list[str]] = {name: [] for name in ("Destination", "Baseline", "Receipt", "Files", "Config", "Runtime")}
    details = {"Destination": [str(destination)]}
    active_path = repo_root / BASELINE_FILE
    try:
        pinned = load_baseline(repo_root)
        active_path = repo_root / "global/opencode.json"
        baseline_cfg = read_config(active_path)
        files = managed_files(repo_root)
        hashes = {}
        for rel, source in files.items():
            active_path = source
            hashes[rel] = sha256_file(source)
        active_path = repo_root
        fingerprint = compute_fingerprint(repo_root)
        details["Baseline"] = [fingerprint]
        if expect is not None and expect != fingerprint:
            findings["Baseline"].append("mismatch")

        try:
            path_state(destination, RECEIPT_NAME)
            receipt = read_receipt(destination)
            if receipt is None:
                findings["Receipt"].append("missing")
            elif receipt != Receipt(fingerprint, hashes, baseline_cfg):
                findings["Receipt"].append("differs")
        except (ReceiptError, OSError, ValueError, RuntimeError):
            findings["Receipt"].append("invalid")

        for rel, digest in hashes.items():
            problem = None
            try:
                state = path_state(destination, rel)
                if state is None:
                    problem = "missing"
                elif not stat.S_ISREG(state.st_mode):
                    problem = "invalid"
                elif sha256_file(destination / rel) != digest:
                    problem = "edited"
            except (ValueError, RuntimeError):
                problem = "invalid"
            except OSError:
                problem = "unreadable"
            if problem:
                findings["Files"].append(f"{problem} {rel}")

        installed_cfg = None
        try:
            state = path_state(destination, "opencode.json")
            if state is None:
                findings["Config"].append("missing opencode.json")
            elif not stat.S_ISREG(state.st_mode):
                findings["Config"].append("unreadable opencode.json")
            else:
                installed_cfg = read_config(destination / "opencode.json")
        except (InstallError, OSError, ValueError, RuntimeError):
            findings["Config"].append("unreadable opencode.json")
        if installed_cfg is not None:
            expected_cfg = merge_settings(installed_cfg, baseline_cfg)
            findings["Config"].extend(f"differs {path}" for path in config_drift_paths(installed_cfg, expected_cfg))

        active_path = destination / "opencode.jsonc"
        if path_state(destination, "opencode.jsonc", allow_leaf_link=True) is not None:
            findings["Config"].append("present opencode.jsonc")

        active_path = destination
        status, version = probe_opencode_version()
        if status != "ok":
            findings["Runtime"].append(status)
        elif version != pinned:
            findings["Runtime"].append(f"mismatch {version} (baseline {pinned})")
        local = list_local_additions(destination, installed_cfg, baseline_cfg, set(files))
    except (BaselineError, InstallError) as exc:
        print(f"Destination {destination}")
        print(f"Error: {exc}")
        print("Result could not complete")
        print(CHECK_SCOPE_NOTE)
        return 1
    except (OSError, ValueError, RuntimeError):
        print(f"Destination {destination}")
        print(f"Error: {active_path}: unable to inspect baseline or destination safely")
        print("Result could not complete")
        print(CHECK_SCOPE_NOTE)
        return 1

    for name, items in findings.items():
        for item in sorted(details.get(name, []) + (items or ["ok"])):
            print(f"{name} {item}")
    for item in local or ["none"]:
        print(f"Local {item}")
    count = sum(len(items) for items in findings.values())
    print(f"Result DRIFT, {count} findings" if count else "Result MATCH")
    print(CHECK_SCOPE_NOTE)
    return 1 if count else 0


def backup_file(target: Path, rel_path: Path, backup_root: Path) -> None:
    if target.is_file():
        backup_target = backup_root / rel_path
        backup_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup_target)


def prune_retired_pr4_assets(destination: Path, backup_root: Path, *, dry_run: bool) -> None:
    for rel_dir in RETIRED_PR4_DIRS:
        target_dir = destination / rel_dir
        if not target_dir.is_dir():
            continue
        if dry_run:
            print(f"[dry-run] Would remove retired skill directory {target_dir}")
            continue
        for file_path in sorted(target_dir.rglob("*")):
            if file_path.is_file():
                backup_file(file_path, file_path.relative_to(destination), backup_root)
        shutil.rmtree(target_dir)

    for rel_file in RETIRED_PR4_FILES:
        target_file = destination / rel_file
        if not target_file.is_file():
            continue
        if dry_run:
            print(f"[dry-run] Would remove retired file {target_file}")
            continue
        backup_file(target_file, rel_file, backup_root)
        target_file.unlink()
        parent = target_file.parent
        if parent != destination and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()


def run_install(repo_root: Path, destination: Path, *, dry_run: bool) -> int:
    active_path = repo_root / BASELINE_FILE
    try:
        load_baseline(repo_root)
        jsonc_path = destination / "opencode.jsonc"
        if jsonc_path.exists():
            raise InstallError(f"{jsonc_path} already exists. Reconcile it with opencode.json before installing.")

        previous = read_receipt(destination)
        active_path = repo_root / "global" / "opencode.json"
        incoming_cfg = read_config(active_path)
        files = managed_files(repo_root)
        hashes = {}
        for rel, source in files.items():
            active_path = source
            hashes[rel] = sha256_file(source)
        active_path = repo_root
        receipt = Receipt(compute_fingerprint(repo_root), hashes, incoming_cfg)
        if previous is not None and previous.fingerprint == receipt.fingerprint and previous != receipt:
            raise ReceiptError(f"{destination / RECEIPT_NAME}: inconsistent history for the same fingerprint")

        # Preflight incoming managed writes and their backup parents.
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup_root = destination / "backups" / f"harness-{timestamp}"
        for rel in [*files, "opencode.json", RECEIPT_NAME]:
            active_path = destination / rel
            state = path_state(destination, rel)
            if state is not None and not stat.S_ISREG(state.st_mode):
                raise InstallError(f"{active_path}: expected a non-symlink regular file")
            backup_rel = (backup_root.relative_to(destination) / rel).as_posix()
            path_state(destination, backup_rel)

        retired_files: list[str] = []
        kept_files: list[str] = []
        if previous is not None:
            retired_files, kept_files = plan_file_retirement(destination, previous, set(files))
            for rel in retired_files:
                active_path = destination / rel
                path_state(destination, (backup_root.relative_to(destination) / rel).as_posix())
            # An old spelling can still name an incoming target on this filesystem.
            # Its local edits follow the normal managed-file backup/replacement rule.
            active_targets = [destination / rel for rel in files if (destination / rel).exists()]
            local_files = []
            for rel in kept_files:
                active_path = destination / rel
                if not any(active_path.samefile(target) for target in active_targets):
                    local_files.append(rel)
            kept_files = local_files
        else:
            # Bootstrap PR4 cleanup also mutates paths; validate it before writes.
            for rel_path in (*RETIRED_PR4_DIRS, *RETIRED_PR4_FILES):
                active_path = destination / rel_path
                state = path_state(destination, rel_path.as_posix())
                if rel_path in RETIRED_PR4_DIRS and state is not None and stat.S_ISDIR(state.st_mode):
                    for child in active_path.rglob("*"):
                        active_path = child
                        child_rel = child.relative_to(destination)
                        path_state(destination, child_rel.as_posix())
                        path_state(destination, (backup_root.relative_to(destination) / child_rel).as_posix())
                else:
                    path_state(destination, (backup_root.relative_to(destination) / rel_path).as_posix())

        config_path = destination / "opencode.json"
        active_path = config_path
        current_cfg = read_config(config_path) if path_state(destination, "opencode.json") is not None else {}
        retired_settings: list[str] = []
        kept_settings: list[str] = []
        if previous is not None:
            current_cfg, retired_settings, kept_settings = retire_settings(current_cfg, previous.config, incoming_cfg)
        merged_cfg = merge_settings(current_cfg, incoming_cfg)
        # Atomic replacement (or legacy cleanup) can discard a retirement survivor.
        # Only announce settings that also survive the final merge unchanged.
        replaced_settings = config_drift_paths(current_cfg, merged_cfg)
        kept_settings = [
            path for path in kept_settings
            if not any(path == changed or path.startswith(changed + ".") for changed in replaced_settings)
        ]
        merged_json = json.dumps(merged_cfg, indent=2) + "\n"

        active_path = repo_root / "global" / "AGENTS.md"
        incoming_agents = active_path.read_text(encoding="utf-8-sig")
        agents_target = destination / "AGENTS.md"
        agents_local = destination / "AGENTS.local.md"
        migrate_local_agents = False
        existing_agents_text = ""
        active_path = agents_local
        try:
            agents_local.lstat()
            local_agents_present = True
        except FileNotFoundError:
            local_agents_present = False
        active_path = agents_target
        if agents_target.is_file() and not local_agents_present:
            existing_agents_text = agents_target.read_text(encoding="utf-8-sig")
            if existing_agents_text != incoming_agents and not re.match(
                r"^\s*" + re.escape(PR4_AGENTS_HEADER) + r"\b", existing_agents_text
            ):
                migrate_local_agents = True

        for kind, removed, kept in (("file", retired_files, kept_files), ("setting", retired_settings, kept_settings)):
            if dry_run:
                for path in removed:
                    print(f"[dry-run] Would remove retired {kind}: {path}")
            for path in kept:
                print(f"{'[dry-run] ' if dry_run else ''}Kept locally changed retired {kind}: {path}")

        if dry_run:
            print(f"[dry-run] Would install harness into {destination}")
            print(f"[dry-run] Would write merged {config_path}")
            if migrate_local_agents:
                print(f"[dry-run] Would preserve existing custom AGENTS.md as {agents_local}")
            if previous is None:
                prune_retired_pr4_assets(destination, backup_root, dry_run=True)
            for rel in files:
                print(f"[dry-run] Would install {destination / rel}")
            print(f"[dry-run] Would write {destination / RECEIPT_NAME}")
            return 0

        active_path = destination
        destination.mkdir(parents=True, exist_ok=True)
        active_path = config_path
        backup_file(config_path, Path("opencode.json"), backup_root)
        config_path.write_text(merged_json, encoding="utf-8", newline="\n")
        if migrate_local_agents:
            active_path = agents_local
            agents_local.write_text(existing_agents_text, encoding="utf-8", newline="\n")

        active_path = destination
        if previous is None:
            prune_retired_pr4_assets(destination, backup_root, dry_run=False)
        for rel in retired_files:
            active_path = target = destination / rel
            backup_file(target, Path(rel), backup_root)
            target.unlink()
            parent = target.parent
            while parent != destination and parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
        for rel, source in files.items():
            active_path = target = destination / rel
            backup_file(target, Path(rel), backup_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        failures = verify_installed(destination, receipt.files)
        try:
            state = path_state(destination, "opencode.json")
            if state is None or not stat.S_ISREG(state.st_mode) or not json_equal(read_config(config_path), merged_cfg):
                failures.append("opencode.json")
        except (OSError, ValueError, UnicodeError, InstallError):
            failures.append("opencode.json")
        if failures:
            print("Error: installed verification failed:", file=sys.stderr)
            for rel in sorted(set(failures)):
                print(rel, file=sys.stderr)
            return 1

        active_path = destination / RECEIPT_NAME
        backup_file(active_path, Path(RECEIPT_NAME), backup_root)
        write_receipt(destination, receipt)
    except ReceiptError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print(
            f"Restore a verified receipt from `{destination / 'backups' / 'harness-*' / RECEIPT_NAME}`. "
            "If no valid backup exists, preserve the damaged receipt and reconcile ownership manually "
            "before deliberately bootstrapping without it; automatic retirement history will be lost.",
            file=sys.stderr,
        )
        return 1
    except (BaselineError, InstallError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, UnicodeError):
        print(f"Error: {active_path}: unable to install (I/O error, invalid path or invalid text)", file=sys.stderr)
        return 1

    print(f"Installed harness in {destination}")
    if migrate_local_agents:
        print(f"Preserved pre-existing custom AGENTS.md at {agents_local}")
    if backup_root.exists():
        print(f"Previous files backed up in {backup_root}")
    print("OpenCode reloads config and skills automatically (or run /reload in an active session).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install personal OpenCode V2 global defaults.")
    parser.add_argument(
        "--destination",
        type=Path,
        default=None,
        help="Target OpenCode config directory (defaults to $XDG_CONFIG_HOME/opencode or ~/.config/opencode).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying the filesystem.",
    )
    parser.add_argument(
        "--fingerprint",
        action="store_true",
        help="Print the portable source-content fingerprint without installing.",
    )
    parser.add_argument("--check", action="store_true", help="Check the installed global baseline without changing files.")
    parser.add_argument("--expect", default=None, metavar="FINGERPRINT", help="Require this source fingerprint with --check.")
    args = parser.parse_args(argv)
    if sum((args.check, args.dry_run, args.fingerprint)) > 1:
        parser.error("--check, --dry-run and --fingerprint cannot be combined")
    if args.fingerprint and (args.dry_run or args.destination is not None):
        parser.error("--fingerprint cannot be combined with --dry-run or --destination")
    if args.expect is not None:
        if not args.check:
            parser.error("--expect requires --check")
        args.expect = args.expect.strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", args.expect):
            parser.error("--expect must contain exactly 64 hexadecimal characters")

    repo_root = Path(__file__).resolve().parent
    try:
        if args.fingerprint:
            load_baseline(repo_root)
            print(compute_fingerprint(repo_root))
            return 0
    except BaselineError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: {exc.filename}: {exc.strerror or 'unable to read source file'}", file=sys.stderr)
        return 1

    destination = args.destination.expanduser().resolve() if args.destination else default_destination()
    if args.check:
        return run_check(repo_root, destination, args.expect)
    return run_install(repo_root, destination, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
