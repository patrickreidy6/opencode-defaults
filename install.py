#!/usr/bin/env python3
"""Cross-platform installer for the opencode-defaults OpenCode V2 global harness."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SKIP_PARTS = {"__pycache__", "node_modules", ".venv", ".git"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".pyd"}
PR4_AGENTS_HEADER = "# Personal OpenCode Defaults"
UNION_ROOT_LIST_KEYS = {"plugins", "instructions", "skills"}
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
            for item in result[key]:
                if item not in merged_list:
                    merged_list.append(copy.deepcopy(item))
            result[key] = merged_list
        else:
            result[key] = copy.deepcopy(in_val)

    if is_root and "$schema" in result:
        schema = result.pop("$schema")
        result = {"$schema": schema, **result}

    return result


def collect_files(repo_root: Path) -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = [
        (repo_root / "global" / "AGENTS.md", Path("AGENTS.md")),
    ]
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
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent
    destination = args.destination.expanduser().resolve() if args.destination else default_destination()

    jsonc_path = destination / "opencode.jsonc"
    if jsonc_path.exists():
        print(
            f"Error: {jsonc_path} already exists. Reconcile it with opencode.json before installing.",
            file=sys.stderr,
        )
        return 1

    incoming_cfg = json.loads((repo_root / "global" / "opencode.json").read_text(encoding="utf-8-sig"))
    config_path = destination / "opencode.json"
    if config_path.is_file():
        current_cfg = json.loads(config_path.read_text(encoding="utf-8-sig"))
    else:
        current_cfg = {}

    merged_cfg = merge_settings(current_cfg, incoming_cfg)
    merged_json = json.dumps(merged_cfg, indent=2) + "\n"

    files = collect_files(repo_root)
    incoming_agents = (repo_root / "global" / "AGENTS.md").read_text(encoding="utf-8-sig")
    agents_target = destination / "AGENTS.md"
    agents_local = destination / "AGENTS.local.md"
    migrate_local_agents = False
    existing_agents_text = ""

    if agents_target.is_file() and not agents_local.exists():
        existing_agents_text = agents_target.read_text(encoding="utf-8-sig")
        if existing_agents_text != incoming_agents and not re.match(
            r"^\s*" + re.escape(PR4_AGENTS_HEADER) + r"\b", existing_agents_text
        ):
            migrate_local_agents = True

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
    backup_root = destination / "backups" / f"harness-{timestamp}"

    if args.dry_run:
        print(f"[dry-run] Would install harness into {destination}")
        print(f"[dry-run] Would write merged {config_path}")
        if migrate_local_agents:
            print(f"[dry-run] Would preserve existing custom AGENTS.md as {agents_local}")
        prune_retired_pr4_assets(destination, backup_root, dry_run=True)
        for _, rel in files:
            print(f"[dry-run] Would install {destination / rel}")
        return 0

    destination.mkdir(parents=True, exist_ok=True)
    backup_file(config_path, Path("opencode.json"), backup_root)
    config_path.write_text(merged_json, encoding="utf-8", newline="\n")

    if migrate_local_agents:
        agents_local.write_text(existing_agents_text, encoding="utf-8", newline="\n")

    prune_retired_pr4_assets(destination, backup_root, dry_run=False)

    for src, rel in files:
        target = destination / rel
        backup_file(target, rel, backup_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)

    print(f"Installed harness in {destination}")
    if migrate_local_agents:
        print(f"Preserved pre-existing custom AGENTS.md at {agents_local}")
    if backup_root.exists():
        print(f"Previous files backed up in {backup_root}")
    print("OpenCode reloads config and skills automatically (or run /reload in an active session).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
