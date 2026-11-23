#!/usr/bin/env python3
"""Publish the authoring machine's installed OpenCode version to public main."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import install
from shared_harness import PUBLIC_REPO

PUBLISH_URLS = {
    PUBLIC_REPO.removesuffix(".git"),
    "git@github.com:patrickreidy6/opencode-defaults",
    "ssh://git@github.com/patrickreidy6/opencode-defaults",
}
MAIN = "refs/heads/main"
RELEASE_VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?(?:\+[A-Za-z0-9.-]+)?")


class PublishError(Exception):
    """Publication could not be completed or verified."""


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, stdin=subprocess.DEVNULL, capture_output=True,
        encoding="utf-8", errors="replace", timeout=90,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"},
    )
    if result.returncode:
        if args[0] == "push":
            raise PublishError("Git push failed. Check write access and the current public main, then retry.")
        raise PublishError(f"Git {args[0]} failed. Check the defaults checkout and its Git configuration.")
    return result.stdout.strip()


def prepare_pin(repo: Path, parent: str, version: str) -> str:
    # A detached checkout of the published parent keeps the author's index and
    # unpublished commits out of the candidate, and uses their normal Git identity.
    with tempfile.TemporaryDirectory(prefix="opencode-version-") as temporary:
        checkout = Path(temporary).resolve() / "pin"
        git(repo, "worktree", "add", "--quiet", "--detach", str(checkout), parent)
        try:
            if install.load_baseline(checkout) == version:
                return parent
            pin = install.BASELINE_FILE
            content = json.dumps({"opencode": version})
            (checkout / pin).write_text(content + "\n", encoding="utf-8", newline="\n")
            git(checkout, "commit", "--only", "-m", f"Pin OpenCode to {version}", "--", pin)
            revision = git(checkout, "rev-parse", "HEAD")
            if (git(checkout, "rev-list", "--parents", "-1", revision) != f"{revision} {parent}"
                    or git(checkout, "diff", "--no-renames", "--name-only", parent, revision) != pin
                    or git(checkout, "show", f"{revision}:{pin}") != content):
                raise PublishError("The candidate commit differs from the requested pin change.")
            return revision
        finally:
            git(repo, "worktree", "remove", "--force", str(checkout))


def sync_author_checkout(repo: Path, revision: str) -> None:
    if git(repo, "rev-parse", "HEAD") == revision:
        return
    pin = install.BASELINE_FILE
    if (git(repo, "branch", "--show-current") == "main"
            and git(repo, "diff", "--name-only", "HEAD", revision) == pin
            and not git(repo, "status", "--porcelain", "--", pin)):
        git(repo, "merge", "--ff-only", "--no-autostash", revision)
    else:
        print("The author checkout has separate history or local changes. See git status before syncing it.")


def publish(repo: Path) -> None:
    if (Path(git(repo, "rev-parse", "--show-toplevel")).resolve() != repo.resolve()
            or repo.resolve() == (Path.home() / ".local/share/opencode-defaults").resolve()):
        raise PublishError("Run this command in the defaults authoring checkout.")
    fetch_url = git(repo, "remote", "get-url", "origin")
    push_url = git(repo, "remote", "get-url", "--push", "--all", "origin")
    if any(url.removesuffix(".git") not in PUBLISH_URLS for url in (fetch_url, push_url)):
        raise PublishError("The fetch and push destinations for origin must be the public defaults repository.")

    status, version = install.probe_opencode_version()
    if status != "ok" or not RELEASE_VERSION.fullmatch(version):
        raise PublishError("Could not read a release version from opencode --version.")

    git(repo, "fetch", "--quiet", "--no-tags", "origin", f"+{MAIN}:refs/remotes/origin/main")
    parent = git(repo, "rev-parse", "refs/remotes/origin/main")
    revision = prepare_pin(repo, parent, version)
    if revision != parent:
        # The candidate is a verified direct child. The lease also catches a
        # concurrent deletion or rewind of main before the push.
        git(repo, "push", "--no-follow-tags", "--recurse-submodules=no",
            f"--force-with-lease={MAIN}:{parent}", "origin", f"{revision}:{MAIN}")
    if git(repo, "ls-remote", "--exit-code", "origin", MAIN).split() != [revision, MAIN]:
        raise PublishError("Public main changed before the pin could be verified. Run the command again.")
    result = "Already published" if revision == parent else "Published"
    print(f"{result} OpenCode {version} on main at {revision}.", flush=True)
    try:
        sync_author_checkout(repo, revision)
    except (PublishError, OSError, subprocess.TimeoutExpired):
        print("The author checkout could not fast-forward to the verified pin. See git status before syncing it.")


def main(argv: list[str] | None = None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    try:
        publish(Path(__file__).resolve().parent)
    except (PublishError, install.BaselineError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
