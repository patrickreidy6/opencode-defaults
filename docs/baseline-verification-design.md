# Baseline installation and verification

Design revised 2026-11-11 after review. Awaiting Patrick's approval; nothing here is implemented yet.

## Intent

Install the same reviewed OpenCode defaults on every machine, starting with `sim-funds` and `sim-prime-broker`, and confirm it later with one command. Intentional project differences stay in each project's repository. This covers only the shared global baseline.

This repo installs a baseline and checks one installation against it. `ops-infra` decides which baseline each workspace should hold, delivers the source, and runs the check. A workspace receives this portable baseline, never a workstation's merged personal configuration.

## Goals and limits

- One identity for a baseline that survives being copied anywhere.
- A read-only check that passes only when an installation holds exactly that baseline.
- Reinstalling converges: content an earlier baseline installed and the new one drops is cleaned up.
- Local additions survive and never fail the check.

The change has failed, even if it runs, when:

- the check passes while two workspaces hold different managed content;
- the check fails on legitimate local additions, so its result gets ignored;
- the installer removes or overwrites something without a backup;
- installing or checking needs Git metadata, credentials, or network access;
- output reveals local setting values or file contents.

Constraints: Python standard library only, the existing PowerShell and `sh` wrappers, and current installer behavior preserved.

Out of scope: delivering the source to workspaces, the `ops-infra` baseline record, machine-readable output, OpenCode's update prompts, and using the check inside the `project-setup` skill.

## Approaches

- **Selected: installation receipt plus read-only check.** Records what was installed and compares the actual installation with it. A small extension to the existing installer serves manual use and later `ops-infra` checks. Patrick chose this.
- **Considered: pinned commit plus manual checklist.** Less code, but cannot detect edits made after installation.
- **Identity by content, not by commit.** The first draft identified a baseline by its Git commit. This repository is private, and `ops-infra`'s last recorded validation found no Git credentials in the sim builders. Their source will arrive as an archive or copy without Git metadata, so a commit-based check could never pass there. A fingerprint of the content works however the source arrives. Approved after review on 2026-11-11.

## Baseline identity

A baseline is every file the installer copies, plus `global/opencode.json` and a new `baseline.json`.

- `baseline.json` sits at the repository root and names the exact OpenCode CLI version the baseline was tested with: `{"opencode": "2.2.7"}`. That is the version on the Surface on 2026-11-11; whether it suits the Halo containers is a rollout check. Model defaults and the Superpowers pin stay in `global/opencode.json`. Every mode stops before changing anything when `baseline.json` is missing or malformed.
- The **fingerprint** is one SHA-256 over the sorted list of every input's path and content hash. Take the file list from the installer's own `collect_files`, so the fingerprint and the installer cannot disagree about what is managed. The installer scripts are not inputs.
- Add `eol=lf` to the `* text=auto` rule in `.gitattributes` so every checkout, archive, and copy carries the same bytes, and assert in a test that no input contains CRLF. Tested in a scratch copy on 2026-11-11: a checkout and an extracted `git archive` produced the same fingerprint, and simulating `core.autocrlf=true` changed every file until `eol=lf` was set.
- `--fingerprint` prints the source copy's fingerprint and exits. The commit stays the label people use: `ops-infra` records commit, fingerprint, and CLI version together when it selects a baseline. The installer never reads Git metadata.

## Installation receipt

A successful install writes `opencode-defaults-receipt.json` in the destination. It holds:

- a format number;
- the baseline fingerprint;
- each installed file's destination-relative path and SHA-256;
- a copy of the baseline's `global/opencode.json`, which is repository content, never the merged machine configuration.

Write it last. Re-read each installed file, confirm its hash, then replace the receipt in one step. On any failure, exit nonzero and leave the previous receipt alone. Back up the previous receipt with the other overwritten files. Before trusting a receipt, validate its structure and that every path is relative and stays inside the destination. Treat an unreadable or unknown-format receipt as absent.

Dry-run writes nothing. Destination resolution, merging, backups, the `AGENTS.local.md` migration, and the refusal when `opencode.jsonc` exists are unchanged. Installing does not inspect the runtime.

## Retired content

The receipt records what the previous baseline installed. On reinstall, for anything it installed that the new baseline no longer ships:

- **Untouched: remove it.** A file is untouched when its hash still matches the receipt, a setting when its value still equals the previous baseline's. Files go to the backup first, and directories left empty are removed. `opencode.json` is already backed up on every run.
- **Changed locally: keep it.** It becomes a local addition, and the installer names it once in its output.

A setting follows the merge rules: a value in `global/opencode.json`, an entry in `plugins`, `instructions`, or `skills`, or a whole `mcp.servers` definition. Objects left empty by a removal are removed too.

Dry-run lists what would be removed. An installation without a receipt has nothing to compare, so the first receipt-writing install removes only what the existing hard-coded retired lists name. Those lists stay for such older installs; later retirements need no code change.

## Check command

```sh
sh ./install.sh --check
sh ./install.sh --check --expect <fingerprint>
sh ./install.sh --fingerprint
```

`install.ps1` offers the same three modes. `--destination` selects the installation to check, as it does for installing.

`--check` compares one installation with the source copy beside the installer and changes nothing. It reports a finding when:

- the source copy's fingerprint is not the one given to `--expect`;
- there is no valid receipt, or its fingerprint differs from the source copy's;
- a managed file is missing or differs from the source;
- managed configuration differs, or `opencode.jsonc` exists in the destination;
- the OpenCode CLI is missing or is not the version in `baseline.json`.

**Configuration** matches when merging the baseline into the installed configuration would change nothing, ignoring order within `plugins`, `instructions`, and `skills`. Reuse the installer's `merge_settings` so check and install cannot disagree. That one rule covers changed values, a missing or altered managed MCP server, legacy V1 keys the installer strips, and a second Superpowers reference. Tried against the current `merge_settings` on 2026-11-11: eleven fresh, local-addition, and drift cases were all classified correctly.

**Runtime:** run `opencode --version` with a short timeout, looking on `PATH` and then in the standalone install location `~/.opencode/bin`. Read the version as the official install script does: last word, leading `v` dropped. This checks the installed binary, not a server that is already running.

**Local additions** are listed, not judged: configuration keys the baseline does not own, by key path, with counts for extra entries in the three root lists; unmanaged files under `agents/`, `commands/`, `skills/`, and `plugins/`, with a wholly unmanaged folder listed once; and `AGENTS.local.md`. Names only, never values or contents. Output is plain, sorted lines so two workspaces' reports can be compared side by side.

**Exit codes:** `0` match; `1` any finding, or a check that could not complete; `2` usage error, such as `--expect` without `--check`, `--check` with `--dry-run`, or a malformed fingerprint.

Two properties to hold in tests: the check passes right after a successful install when the pinned CLI is present, and whenever the check passes, reinstalling changes no managed file or setting.

Illustrative output. Wording and layout are the builder's; the sections are not.

```text
$ sh ./install.sh --check --expect 3f9c1a7e...
Destination  /home/builder/.config/opencode
Baseline     3f9c1a7e...  matches --expect
Receipt      3f9c1a7e...  ok
Files        edited   skills/writer/SKILL.md
Config       differs  agents.title.model
Runtime      opencode 2.2.7  ok
Local        providers, commands/add-notes.md  (listed, not checked)
Result       DRIFT, 2 findings
```

### What a pass means

Without `--expect`: this installation matches this source copy. With `--expect`: it holds the selected baseline, so the same expected value passing in both workspaces means they hold the same baseline.

A pass does not cover project or system overrides, environment substitutions, plugin loading, MCP connectivity, provider access, or model behavior. The check detects accidental drift and is not tamper-proof: the source copy and installer sit in the builder's writable home. Say so in the output and README.

## How ops-infra uses it

Not built here. This is the interface it relies on.

1. On the Surface, with the reviewed commit checked out and no uncommitted changes, run `--fingerprint` and record commit, fingerprint, and CLI version.
2. Deliver that source to each workspace by whatever route `ops-infra` chooses.
3. In each workspace, install the pinned CLI, run the installer, and connect providers by hand.
4. Run `--check --expect <fingerprint>` in each workspace with its other checks.

## Files and verification

Add `baseline.json`. Change `install.py`, `install.ps1`, `.gitattributes`, `tests/test_install.py`, `README.md`, and the root `AGENTS.md`. `install.sh` already forwards arguments.

README: installing the runtime at the pinned version (the official install script accepts `--version`, and `opencode upgrade <version>` covers an existing install), how a workspace without repository access gets the source, the three modes, how to change the baseline, retirement in place of today's "managed command names are replaced on update" note, and the limits above. Upgrading the runtime means bumping `baseline.json`; until then the check fails on any machine that upgraded, including the Surface.

`docs/cross-model-workflow-design.md` tells maintainers to add a removed command to `RETIRED_PR4_FILES`. Update that note: the receipt now handles it.

Sequencing: the uncommitted `/xm-*` commands work edits `install.py`, `README.md`, `AGENTS.md`, and the tests. Land it before starting this.

Tests use temporary directories with no credentials or network, and stub the CLI probe so they do not depend on an installed OpenCode. Cover:

- fingerprint: stable, changes with any input, equal for a copy without `.git`, and a fixed fixture yields a recorded value so the format cannot change silently;
- install: receipt written, repeat install stable, dry-run writes nothing, failed verification keeps the old receipt;
- retirement: untouched file and setting removed with a backup, changed ones kept and named;
- check: passes after install, one case per finding, local additions listed without values and not failing, `--expect` match and mismatch, destination unchanged by the check;
- usage errors and both wrappers.

Verify with `uv run --no-project python -m unittest discover -s tests -v` and an isolated install, check, edit, check run on Windows. Record the Linux result at rollout.

## Left to the builder

Receipt field names, output wording, how the wrappers pass options, internal structure, and the timeout value.

## Decisions

Patrick's: receipt plus check command; then, after review on 2026-11-11, the content fingerprint, `--expect`, the pinned runtime, and removing retired files.

Calls made while revising, for Patrick to confirm:

- Untouched retired settings are removed like files, and anything changed locally is kept as a local addition. The review had left retired settings and edited files as findings until removed by hand, which would mean a hand edit on every machine each time the baseline drops a setting.
- The receipt holds no commit. Workspace copies carry no Git metadata to read it from, so the commit-to-fingerprint pairing lives in the `ops-infra` record.
- `--fingerprint` exists so `--expect` has a value to use.
- The check lists local additions by name and never fails on them.
- The runtime check looks on `PATH`, then in `~/.opencode/bin`.
