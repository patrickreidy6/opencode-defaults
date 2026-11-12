#!/usr/bin/env python3
"""Receive shared defaults from public main; report before applying them."""

from __future__ import annotations

import argparse
import contextlib
import io
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys

import install

PUBLIC_REPO = 'https://github.com/patrickreidy6/opencode-defaults.git'


class HarnessError(Exception):
    """An operation could not complete; no configuration values in the message."""


def git(source: Path, *args: str, allow_failure: bool = False) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, 'GIT_TERMINAL_PROMPT': '0', 'GCM_INTERACTIVE': 'never'}
    result = subprocess.run(
        ['git', '-c', 'credential.helper=', '-c', 'core.askPass=', *args],
        cwd=source, env=env, stdin=subprocess.DEVNULL, capture_output=True,
        text=True, timeout=90, check=False,
    )
    if result.returncode and not allow_failure:
        raise HarnessError(f'Git {args[0]} failed; check public GitHub connectivity and the source checkout.')
    return result


def refresh_source(source: Path, *, expected_remote: str | None = None) -> str:
    """Fast-forward a clean clone; neither discard local commits nor push."""
    expected_remote = PUBLIC_REPO if expected_remote is None else expected_remote
    if not (source / '.git').exists():
        raise HarnessError('The defaults source must be a Git clone. Follow the one-time bootstrap instructions.')
    if git(source, 'remote', 'get-url', 'origin').stdout.strip() != expected_remote:
        raise HarnessError('Source origin does not match the shared defaults repository.')
    if git(source, 'branch', '--show-current').stdout.strip() != 'main':
        raise HarnessError('The dedicated defaults checkout must be on main.')
    if git(source, 'status', '--porcelain', '--untracked-files=all').stdout.strip():
        raise HarnessError('Source checkout has local changes; preserve them in the authoring repo before updating this cache.')
    git(source, 'fetch', '--quiet', '--no-tags', 'origin', 'main')
    revision = git(source, 'rev-parse', 'FETCH_HEAD').stdout.strip()
    if git(source, 'merge-base', '--is-ancestor', 'HEAD', revision, allow_failure=True).returncode:
        raise HarnessError('Source checkout has local commits or diverged history; nothing was reset.')
    git(source, 'merge', '--quiet', '--ff-only', revision)
    return revision


def dispatch(mode: str, source: Path, destination: Path, project: Path) -> subprocess.CompletedProcess[str]:
    revision = refresh_source(source)
    print(f'Published main {revision}', flush=True)
    # Reload both this driver and install.py from the freshly received revision.
    result = subprocess.run(
        [sys.executable, str(source / 'shared_harness.py'), mode, '--prepared',
         '--destination', str(destination), '--project', str(project)],
        capture_output=True, text=True, check=False,
    )
    print(result.stdout, end='')
    print(result.stderr, end='', file=sys.stderr)
    return result


def project_items(project: Path) -> list[str]:
    """Inventory active ancestor harness files; do not parse their values."""
    project = project.resolve()
    if not project.is_dir():
        raise HarnessError('Project directory does not exist.')
    result = git(project, 'rev-parse', '--show-toplevel', allow_failure=True)
    root = Path(result.stdout.strip()).resolve() if result.returncode == 0 else project
    if not project.is_relative_to(root):
        root = project
    home = Path.home().resolve()
    items = []

    def display(path: Path) -> str:
        return path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix()

    current = project
    while True:
        # Config discovery reaches the filesystem root, including above a Git repo.
        names = ['opencode.json', 'opencode.jsonc', '.opencode/opencode.json', '.opencode/opencode.jsonc']
        within_project = current.is_relative_to(root)
        if within_project or (project.is_relative_to(home) and current.is_relative_to(home)):
            names.append('AGENTS.md')
        if within_project:
            names.append('.opencode/AGENTS.md')
        for name in names:
            path = current / name
            if path.exists() or path.is_symlink():
                items.append(display(path))
        extensions = current / '.opencode'
        if extensions.is_symlink():
            items.append(display(extensions) + '/')
        elif within_project and extensions.is_dir():
            for name in install.list_local_additions(extensions, None, {}, set()):
                items.append(display(extensions / name) + ('/' if name.endswith('/') else ''))
        elif (extensions / 'plugins').is_dir():
            # Plugin directories follow discovered configuration, unlike project skills.
            for plugin in (extensions / 'plugins').iterdir():
                items.append(display(plugin) + ('/' if plugin.is_dir() and not plugin.is_symlink() else ''))
        if current.parent == current:
            break
        current = current.parent
    return sorted(set(items))


def report_drift(source: Path, destination: Path, project: Path) -> int:
    previous = install.read_receipt(destination)
    if previous is None:
        raise HarnessError('No installation receipt. Run the one-time installer before checking shared harness drift.')
    pinned = install.load_baseline(source)
    incoming = install.read_config(source / 'global/opencode.json')
    files = {name: install.sha256_file(path) for name, path in install.managed_files(source).items()}
    print(f'Default {install.compute_fingerprint(source)}')
    print(f'Installed {previous.fingerprint}')

    upstream = []
    for name in sorted(previous.files.keys() | files.keys()):
        if name not in previous.files:
            upstream.append(f'added file {name}')
        elif name not in files:
            upstream.append(f'removed file {name}')
        elif files[name] != previous.files[name]:
            upstream.append(f'updated file {name}')
    upstream.extend(f'changed setting {name}' for name in install.config_drift_paths(previous.config, incoming))
    for item in upstream or ['none in shared files/settings']:
        print(f'Upstream {item}')

    workspace = []
    for name, expected in sorted(previous.files.items()):
        state = install.path_state(destination, name)
        if state is None:
            workspace.append(f'removed file {name}')
        elif not stat.S_ISREG(state.st_mode):
            raise HarnessError(f'Unable to inspect managed file {name}.')
        elif install.sha256_file(destination / name) != expected:
            workspace.append(f'edited file {name}')
    config_state = install.path_state(destination, 'opencode.json')
    if config_state is None:
        current = {}
        workspace.append('removed file opencode.json')
    elif not stat.S_ISREG(config_state.st_mode):
        raise HarnessError('Unable to inspect opencode.json.')
    else:
        current = install.read_config(destination / 'opencode.json')
    workspace.extend(f'changed setting {name}' for name in install.config_drift_paths(
        current, install.merge_settings(current, previous.config)
    ))
    for item in workspace or ['no shared edits since last install/update']:
        print(f'Workspace {item}')
    for name in install.list_local_additions(destination, current, previous.config, set(previous.files)) or ['none']:
        print(f'Local {name}')
    if (destination / 'opencode.jsonc').exists():
        print('Local opencode.jsonc (update requires reconciliation with opencode.json)')
    for name in project_items(project) or ['none']:
        print(f'Project {name}')
    status, version = install.probe_opencode_version()
    print(f'Runtime {version if status == "ok" else status}; published default requires {pinned}')
    print('Differences are informational. Update replaces shared items with backups; Local and Project additions remain.')
    print('Project entries are an inventory, not an effective runtime comparison. Values and credentials are not shown.')
    return 0


def run_opencode(*args: str) -> None:
    executable = shutil.which('opencode') or shutil.which('opencode', path=str(Path.home() / '.opencode/bin'))
    if executable is None:
        raise HarnessError('OpenCode CLI is missing; complete the one-time runtime installation first.')
    try:
        result = subprocess.run([executable, *args], stdin=subprocess.DEVNULL, capture_output=True,
                                text=True, timeout=300, check=False)
    except (OSError, UnicodeError, subprocess.TimeoutExpired):
        raise HarnessError(f'OpenCode {args[0]} could not complete; retry from a terminal.') from None
    if result.returncode:
        raise HarnessError(f'OpenCode {args[0]} failed. Run that command in a terminal for details.')


def apply_update(source: Path, destination: Path) -> int:
    if install.read_receipt(destination) is None:
        raise HarnessError('No installation receipt. Run the one-time installer first.')
    preview = io.StringIO()
    with contextlib.redirect_stdout(preview):
        code = install.run_install(source, destination, dry_run=True, reset_shared=True)
    if code:
        raise HarnessError('Update preflight failed; shared files were not changed.')
    pinned = install.load_baseline(source)
    status, version = install.probe_opencode_version()
    if status != 'ok':
        raise HarnessError('Cannot identify the installed OpenCode CLI; complete runtime setup first.')
    upgraded = version != pinned
    if upgraded:
        print(f'Updating OpenCode CLI from {version} to {pinned}', flush=True)
        run_opencode('upgrade', pinned)
        if install.probe_opencode_version() != ('ok', pinned):
            raise HarnessError('OpenCode CLI version still differs from the pin; harness update was not applied.')
        print('The CLI binary changed. Run `opencode service restart` from a terminal to activate it in the background service.', flush=True)
    if install.run_install(source, destination, dry_run=False, reset_shared=True):
        raise HarnessError('Harness installation did not complete. Inspect the reported backup/receipt status.')
    try:
        run_opencode('reload')
    except HarnessError as exc:
        raise HarnessError(f'Shared defaults were installed, but reload failed. {exc}') from None
    print('Shared harness updated. Workspace-only additions and project files were preserved.')
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['drift', 'update'])
    parser.add_argument('--destination', type=Path, default=None)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--prepared', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    source = Path(__file__).resolve().parent
    destination = args.destination.expanduser().resolve() if args.destination else install.default_destination()
    try:
        if not args.prepared:
            return dispatch(args.mode, source, destination, args.project.resolve()).returncode
        if args.mode == 'drift':
            return report_drift(source, destination, args.project)
        return apply_update(source, destination)
    except (HarnessError, install.ReceiptError, install.InstallError, install.BaselineError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        print('Error: shared harness operation could not complete (filesystem, command, or network failure).', file=sys.stderr)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
