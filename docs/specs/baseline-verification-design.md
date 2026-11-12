# Baseline installation and verification

**Status: Implemented; maintained through 2026-11-12.** The current workflow is install once, inspect drift, then receive public updates when requested in each workspace. This spec describes that workflow and its underlying installer, receipts and offline verifier. The [README](../../README.md#install-once-per-workspace) provides setup commands. The [completed baseline plan](../plans/archive/2026-11-11-baseline-verification.md) and [shared-harness plan](../plans/archive/2026-11-12-shared-harness-commands.md) retain their original approval and execution records; the latter is the approval source for the update workflow. Dated decisions and verification evidence are preserved below as history.

## Intent

Install shared OpenCode defaults in each machine/user environment or isolated workspace container. Projects using that environment inherit the global defaults. Workspace-only additions remain local; project-specific configuration, instructions and extensions stay in their owning repositories.

Each workspace receives defaults directly from the public repository and chooses when to update. Workspaces may hold different published versions and different local additions. No central `ops-infra` baseline selection, archive delivery or fleet rollout is required. The shared source contains portable defaults, never a workstation's merged personal configuration.

## Goals and limits

- One identity for a baseline that survives being copied anywhere.
- An informational drift report that distinguishes published changes, local edits and local additions without changing the installed harness.
- An explicit update that replaces shared items, removes retired shared items and preserves workspace-only additions, with backups before overwriting or removing existing files.
- An offline check that passes only when the managed baseline and CLI match the selected source. Passing the same `--expect` fingerprint in two workspaces establishes the same baseline; selecting the same version everywhere is optional.
- Local additions survive and never fail the offline check merely by being present. A list placement the installer would reorder is a configuration finding.
- Reports show paths, setting names and statuses, never local setting values or file contents.

The Python implementation uses the standard library. `install.ps1` and `install.sh` remain convenience launchers for `install.py`; direct Python invocation is also supported. Given a local source copy and Python, ordinary install, fingerprint and check need no Git metadata, credentials or network. The public drift/update workflow requires Git and network access to refresh its source; provider sign-ins remain separate.

Out of scope: automatic fleet rollout, sending local changes upstream, machine-readable reports, and proving effective runtime equivalence across project/system overrides, plugins, MCPs or providers. The `project-setup` skill bootstraps or reuses the global harness; it does not automatically run the offline verifier.

## Current workflow

### Install once

Use Git and Python 3.10+ (or `uv`). Clone `https://github.com/patrickreidy6/opencode-defaults.git` into `~/.local/share/opencode-defaults`, outside project repositories. No GitHub account or token is needed to download the defaults. Keep this clone as a clean upstream cache; author and publish improvements from a separate development checkout.

Read the CLI pin from that source's `baseline.json` and install the OpenCode runtime before applying the defaults. From the source directory, preview and install with `./install.ps1 -WhatIf` then `./install.ps1` on Windows, or `sh ./install.sh --dry-run` then `sh ./install.sh` on POSIX. The [README](../../README.md#install-once-per-workspace) gives full platform commands, including Windows execution-policy handling. `uv run --no-project python install.py` is a cross-platform alternative; it accepts `--dry-run` for the preview.

The installer creates the receipt and global slash commands. Connect providers separately in that environment. Additional projects reuse the installed global harness; do not copy the defaults into every repository.

### Inspect drift and receive updates

Run `/shared-harness-drift` and `/shared-harness-update` as separate OpenCode submissions, with no arguments. Their launchers create the dedicated public source cache if absent, then run `shared_harness.py`. Both require an existing valid installation receipt; they do not replace first-time installation.

The driver requires the cache to be a Git clone on `main`, with the expected public `origin` and no tracked or untracked changes. It fetches public `main`, permits only a fast-forward, and runs the newly fetched driver and installer. It stops on local commits or divergent history rather than resetting them. Neither command pushes changes or updates another workspace.

`/shared-harness-drift` refreshes only that source cache and reports:

- **Upstream:** shared files/settings added, changed or removed since the installation receipt.
- **Workspace:** shared files/settings edited or removed locally since the receipt.
- **Local:** workspace-only global additions at the first unowned boundary.
- **Project:** applicable project/ancestor instructions, configuration and `.opencode` extensions. This is an inventory, not a comparison of effective settings.
- **Runtime:** the installed CLI version and published pin.

Differences are informational: a completed report exits successfully even when they exist. Installed and project files remain unchanged. Unlike the offline `--check`, this command fetches upstream and does not treat baseline differences as failures.

`/shared-harness-update` applies the fetched public version in the current workspace:

1. Validate the receipt and run the installer's dry-run preflight with shared-item reset enabled.
2. Probe the CLI. If it differs from the fetched pin, run `opencode upgrade <version>` and verify the resulting version. A missing CLI requires first-time runtime setup.
3. Install with `reset_shared=True`: back up and replace shared items, retire previously managed items even when edited, and preserve workspace-only additions and project files.
4. Verify the installed files and merged configuration, write the new receipt, then run `opencode reload`.

If the CLI binary changes, the command asks for `opencode service restart` from a terminal; it does not terminate the service running its own session. A failed later step can leave a changed CLI or partially applied files. A reload failure occurs after installation and receipt publication. Report the completed stage and failure; there is no automatic rollback.

The equivalent terminal commands, run from the active project, are:

```sh
python3 "$HOME/.local/share/opencode-defaults/shared_harness.py" drift --project .
python3 "$HOME/.local/share/opencode-defaults/shared_harness.py" update
```

Use `uv run --no-project python` on Windows or wherever preferred. `--destination` selects another configuration directory, but an update still operates on the current user's CLI and reloads OpenCode. It does not isolate the runtime.

## Baseline identity

A baseline is every file the installer copies, plus `global/opencode.json` and `baseline.json`.

- [`baseline.json`](../../baseline.json) names the exact CLI pin; read the selected source's file instead of copying a version from historical evidence below. Model defaults and the Superpowers pin stay in `global/opencode.json`. Every installer mode validates `baseline.json` before changing installed files. The update driver may already have refreshed its source cache before this validation.
- The **fingerprint** is one SHA-256 over the sorted list of every input's path and content hash. It uses the installer's `collect_files` list, so fingerprinting and installation agree on managed files. Installer/driver scripts, tests, docs and Git metadata are not inputs.
- `.gitattributes` sets `* text=auto eol=lf` to keep source bytes consistent across platforms; a test rejects CRLF in fingerprint inputs.
- `--fingerprint` prints the local source's fingerprint and exits. The updater also reports the fetched commit as a source label. Fingerprints and receipts remain independent of Git metadata, so offline verification still works with an extracted archive or copy.

## Installation receipt

A successful install writes `opencode-defaults-receipt.json` in the destination. It holds:

- a format number;
- the baseline fingerprint;
- each installed file's destination-relative path and SHA-256;
- a copy of the baseline's `global/opencode.json`, which is repository content, never the merged machine configuration.

The installer writes it last, after re-reading installed files to confirm their hashes and verifying the merged configuration. It backs up the previous receipt, then atomically replaces it. An install failure before that replacement leaves the previous receipt in place, but earlier file changes are not rolled back. The update driver's later reload can fail after the new receipt has been published. Before trusting a receipt, validate its structure and that every path is relative and stays inside the destination.

A missing receipt is bootstrap. An existing malformed, unreadable or unsupported receipt stops install and dry-run before any writes. Name the receipt path and a safe reason, then give recovery guidance: restore a verified receipt from `<destination>/backups/harness-*/opencode-defaults-receipt.json`. If no valid backup exists, preserve the damaged receipt and reconcile ownership manually before deliberately bootstrapping without it; automatic retirement history will be lost. Never automatically delete or replace the invalid receipt.

An ordinary installer dry-run writes nothing. The destination is `--destination`, otherwise absolute `$XDG_CONFIG_HOME/opencode`, otherwise `~/.config/opencode`. Backups live under `<destination>/backups/harness-<timestamp>/`. An existing `opencode.jsonc` stops installation until reconciled with `opencode.json`.

The installer merges shared settings while preserving unrelated local settings and files. Existing `AGENTS.local.md` remains local. Ordinary installation can preserve a pre-existing custom `AGENTS.md` as `AGENTS.local.md` when that file is absent. During a shared reset, edits to receipt-owned `AGENTS.md` are backed up and replaced, without migrating those edits into active local instructions.

Ordinary `install.py` does not inspect or change the CLI runtime. The offline check probes it; the update driver probes and applies the selected pin before installation.

## Retired content

The receipt records what the previous baseline installed. Retirement differs between ordinary reinstall and explicit shared update:

| Content affected by retirement | Ordinary `install.py` | `/shared-harness-update` |
|---|---|---|
| Untouched file or setting | Remove with backup | Remove with backup |
| Locally edited file or setting | Keep as a local addition and name it, unless the incoming baseline owns/replaces it through another path or definition | Remove with backup |
| Unowned workspace-only addition | Preserve | Preserve |

A file is untouched when its hash matches the receipt; a setting is untouched when it equals the previous baseline value. Removed files are backed up first, and empty parent directories are removed. The merged `opencode.json` has its own backup.

Configuration ownership follows the merge rules. Each shared `mcp.servers` definition is atomic: an incoming definition replaces the whole server definition. Root `plugins`, `instructions` and `skills` arrays track membership by value. Values present in the old baseline and dropped by the new one are removed; additional local values survive in both modes. Empty objects left by retirement are removed. Shared content still present in the incoming baseline is replaced in both modes, even when edited locally; the preservation rule above applies to retired content.

Dry-run lists what would be removed. An installation without a receipt has nothing to compare, so the first receipt-writing install removes only what the existing hard-coded retired lists name. Those lists stay for such older installs; later retirements need no code change.

## Check command

```sh
sh ./install.sh --check
sh ./install.sh --check --expect <fingerprint>
sh ./install.sh --fingerprint
```

`install.ps1` offers the same three modes as `-Check`, `-Check -Expect <fingerprint>` and `-Fingerprint`. `--destination` (`-Destination` in PowerShell) selects the installation to check, as it does for installing. Supply a full 64-character fingerprint for `--expect`. This is the offline verifier; `/shared-harness-drift` is the normal informational workflow.

`--check` compares one installation with the source copy beside the installer and changes nothing. It reports a finding when:

- the source copy's fingerprint is not the one given to `--expect`;
- there is no valid receipt, or its fingerprint, managed-file hashes or baseline configuration differ from the source copy's;
- a managed file is missing or differs from the source;
- managed configuration differs, or `opencode.jsonc` exists in the destination;
- the OpenCode CLI is missing or is not the version in `baseline.json`.

**Configuration** matches when `json_equal(merge_settings(installed, baseline), installed)`: structural comparison preserves JSON types and list order, without sorting lists or treating `true` as `1`. List order counts, including within `plugins`, `instructions`, and `skills`. Reinstall may reposition a local list entry; that placement is drift. Reuse the installer's `merge_settings` so check and install cannot disagree; existing root-array membership and merge behavior stay unchanged. That one rule also covers changed values, a missing or altered managed MCP server, legacy V1 keys the installer strips, and a second Superpowers reference.

**Runtime:** run `opencode --version` with a short timeout, looking on `PATH` and then in the standalone install location `~/.opencode/bin`. Read the version as the official install script does: last word, leading `v` dropped. This checks the installed binary, not a server that is already running.

**Local additions** are listed at the first unowned boundary: configuration key names by key path, counts for extra entries in the root `plugins`, `instructions`, and `skills` lists, local files under `agents/`, `commands/`, `skills/`, and `plugins/`, and `AGENTS.local.md`. Stop at an unowned configuration key rather than inspecting its values. Treat the four directory roots as containers and walk deeper only along prefixes containing managed paths. List each nonempty unowned directory once, without descending its tree; skip directly empty directories. Names only, never values or contents. Print one plain, sorted `Local <item>` line per item, or `Local none` when there are no additions. Local presence alone is never a finding; a list placement that reinstall would change is a configuration finding. Every workspace may have local additions; `Local none` is not a rollout requirement.

**Exit codes:** `0` match; `1` any finding, or a check that could not complete; `2` usage error, such as `--expect` without `--check`, `--check` with `--dry-run`, or a malformed fingerprint.

Two properties to hold in tests: the check passes right after a successful install when the pinned CLI is present, and whenever the check passes, reinstalling changes no managed file or setting.

Illustrative output, with the fingerprint abbreviated for readability:

```text
$ sh ./install.sh --check --expect 3f9c1a7e...
Destination  /home/builder/.config/opencode
Baseline     3f9c1a7e...  matches --expect
Receipt      3f9c1a7e...  ok
Files        edited   skills/writer/SKILL.md
Config       differs  agents.title.model
Runtime      opencode 2.2.7  ok
Local        commands/add-notes.md
Local        providers
Result       DRIFT, 2 findings
```

### What a pass means

Without `--expect`: this installation matches this source copy. With `--expect`: it holds the selected baseline, so the same expected value passing in both workspaces means they hold the same baseline. Different workspaces can choose different versions; neither invocation checks whether the local source is the newest public version.

A pass does not cover the running server version, project or system overrides, environment substitutions, plugin loading, MCP connectivity, provider access, or model behavior. The check detects accidental drift and is not tamper-proof: the source copy and installer are writable by the workspace user.

## Files and verification

[`install.py`](../../install.py) owns installation, merging, receipts, fingerprints and offline verification. [`install.ps1`](../../install.ps1) and [`install.sh`](../../install.sh) find Python/`uv` and forward options. [`shared_harness.py`](../../shared_harness.py) owns source refresh, drift reporting and updates; the two [`global/commands/`](../../global/commands/) prompts launch it. The [`project-setup` skill](../../.opencode/skills/project-setup/SKILL.md) reads the source pin, sets up or reuses the harness, and keeps project additions local.

Maintain the README and this spec alongside behavior changes. Publish tested changes from the development checkout to `main`; each workspace receives them only when its update command is invoked. Change `baseline.json` deliberately to select a new CLI pin. A CLI version that differs from the selected source causes the offline check to fail; the updater applies the fetched source's pin. Receipts handle subsequent retirement of managed content without adding entries to the legacy hard-coded lists.

Tests in `tests/test_install.py`, `tests/test_baseline.py` and `tests/test_shared_harness.py` use temporary directories, local Git fixtures and fake CLI behavior without credentials or network. Coverage includes:

- fingerprint: stable, changes with any input, equal for a copy without `.git`, and a fixed fixture yields a recorded value so the format cannot change silently;
- install: receipt written, repeat install stable, dry-run writes nothing, failed verification keeps the old receipt, an existing malformed/unreadable/unsupported receipt stops install and dry-run before writes;
- retirement: ordinary reinstall preserves edited retired content; shared reset removes it with backups; local additions and value-based array membership remain protected;
- check: passes after install, one case per finding, local additions listed at the first unowned boundary without values and not failing on presence alone, list placement that reinstall would change reported as drift, `--expect` match and mismatch, destination unchanged by the check;
- usage errors and both wrappers;
- drift/update: clean-source refresh and freshly fetched code execution, dirty/diverged-source refusal, upstream versus workspace differences, project inventory, no remote mutation, and explicit upgrade/reload failures.

After installer changes, run `uv run --no-project python -m unittest discover -s tests -v` and an install followed by `--check` against an isolated `--destination`, as required by the repository instructions. For portability or runtime changes, also verify the affected behavior on Windows and Linux; keep SSH outside unit tests. Use an isolated runtime environment when exercising the updater, since `--destination` isolates only configuration. Fake-CLI tests do not establish live runtime, provider or plugin readiness.

## Decisions

### Original baseline decisions — 2026-11-11

The following is the original decision record. At that time the repository was private and the proposed delivery route used archives without Git metadata. Those access and central-rollout assumptions were superseded by the public workflow on 2026-11-12; they are not current requirements. Ordinary reinstall retains its original retirement behavior, while explicit shared update uses the reset behavior documented above.

The selected approach was an installation receipt plus a read-only check. A pinned commit plus a manual checklist was considered, but would not detect edits after installation. Content identity kept verification independent of the source-delivery route and remains useful with public Git clones.

Patrick's: receipt plus check command; then, after review on 2026-11-11, the content fingerprint, `--expect`, the pinned runtime, and removing retired files.

Calls made while revising, confirmed with planning approval:

- Untouched retired settings are removed like files, and anything changed locally is kept as a local addition. The review had left retired settings and edited files as findings until removed by hand, which would mean a hand edit on every machine each time the baseline drops a setting.
- The receipt holds no commit. Workspace copies carry no Git metadata to read it from, so the commit-to-fingerprint pairing lives in the `ops-infra` record.
- `--fingerprint` exists so `--expect` has a value to use.
- The check lists local additions by name and never fails on their presence alone; placement that the installer would reorder is drift.
- The runtime check looks on `PATH`, then in `~/.opencode/bin`.

Three `/xm-spec-review` reports on 2026-11-11 led to the amendments above. Patrick accepted trimmed #1 (Local reporting at the first unowned boundary) and #2–#5 (ordered merge comparison, `project-setup` reading the exact version from `baseline.json`, Windows/Linux acceptance before rollout, and stopping before writes on an existing invalid receipt).

## Verified

The dated records below preserve the original acceptance and regression evidence, including source hashes, commands and then-current rollout assumptions. They do not describe today's workspace state or authorize new deployments. The later [shared-harness verification and deployment record](../plans/archive/2026-11-12-shared-harness-commands.md#verification-and-deployment-record) records publication and the public update workflow's acceptance.

### Windows and Linux acceptance — 2026-11-11

Task 8 passed against committed source `b1e4af296d4598e0680e1822da4b17683393f58c`. The logs use UTC dates of 2026-11-12. Both platforms demonstrated a clean positive check followed by detection of one edited managed file; no Task 8 acceptance remains pending.

| Identity | Verified value |
|---|---|
| Baseline fingerprint: Windows checkout, extracted Git archive, and Linux copy | `a77a2a838e31e785883a741616ded0140a5f21b3d09d3f744ea4007f6deebf1e` |
| `FIXTURE_FINGERPRINT`, computed and asserted on both platforms | `83483d0562b62bc84626144a38495270e1dd0a0411350d3b5e1b2c8a29ec842d` |
| Source archive SHA-256, identical before and after transfer to Linux | `86c93d80a2cffc24c8161f2b570fe535b6f8f3b5c07a44e4df50fcd4d8d4cc4b` |

Windows used PowerShell `5.1.26100.9974`, Python `3.15.1`, and the existing `C:\Users\preid\.opencode\bin\opencode.exe`, which reported `opencode v2.2.7`. Linux SSH confirmed hostname `workspace-smoke`, user `builder`, Python `3.15.2`, and initially no OpenCode on `PATH` or in `/home/builder/.opencode/bin`.

The unique Windows scratch directory (`W` below) was `C:\Users\preid\AppData\Local\Temp\opencode\baseline-verify-15f3829aaa6043a0b0231444240ac863.tmp`. The successful Linux scratch directory (`L`) was `/workspace/opencode-baseline-verify-tHxxuRHg.tmp`. `FP` denotes the baseline fingerprint above. The command/result record below is self-contained: substitute these exact paths and fingerprint for `W`, `L` and `FP`.

| Platform / command | Exit | Actual result |
|---|---:|---|
| Windows: `git archive --format=tar -o W\src.tar HEAD`; `tar -xf W\src.tar -C W\src` | 0 each | Committed source extracted without Git metadata |
| Windows: `uv run --no-project python W\src\install.py --fingerprint`; checkout `uv run --no-project python install.py --fingerprint` | 0 each | Both printed `FP` only |
| Windows, archive source directory: `uv run --no-project python -m unittest discover -s tests -v` | 0 | 107 tests, `OK (skipped=9)`; symlink privileges unavailable, including two skipped subcases in the managed-symlink receipt test |
| Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File W\src\install.ps1 -Destination W\dest` | 0 | Isolated install |
| Windows: same wrapper with `-Check -Expect FP -Destination W\dest` | 0 | Baseline, receipt, files, configuration and runtime all `ok`; `Local none`; `Result MATCH` |
| Windows: `Add-Content -LiteralPath W\dest\skills\writer\SKILL.md -Value 'edit'`, then repeat the check | 0, then 1 | Sole finding: `Files edited skills/writer/SKILL.md`; `Local none`; `Result DRIFT, 1 findings` |
| Linux, archive source directory: `python3 -m unittest discover -s tests -v` | 0 | 107 tests, `OK (skipped=3)`; only Windows PowerShell modes, wrapper and fallback tests skipped; all symlink cases executed and passed |
| Linux: `sh L/src/install.sh --fingerprint` | 0 | Printed `FP` only |
| Linux: `sh L/src/install.sh --destination L/dest` | 0 | Isolated install |
| Linux: `sh L/src/install.sh --check --expect FP --destination L/dest` | 0 | Baseline, receipt, files, configuration and runtime all `ok`; `Local none`; `Result MATCH` |
| Linux: `printf 'edit\n' >> L/dest/skills/writer/SKILL.md`, then repeat the check | 0, then 1 | Sole finding: `Files edited skills/writer/SKILL.md`; `Local none`; `Result DRIFT, 1 findings` |

Linux commands ran through SSH, outside the unit suite, using `env -i` with `HOME=L/home`, `TMPDIR=L/tmp`, and `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, and `XDG_RUNTIME_DIR` under `L/xdg/`. `SHELL=/bin/bash`, `LANG=C.UTF-8`, and `PYTHONDONTWRITEBYTECODE=1` were also supplied. Preparation and unit tests used the original `PATH`; only runtime acceptance commands prepended `L/home/.opencode/bin`.

Patrick's scoped verification permission was exercised by downloading `https://opencode.ai/v2/install` into `L/official-install.sh`, reviewing it, and running `bash L/official-install.sh --version 2.2.7 --no-modify-path` with that isolated environment. The installed binary reported `opencode v2.2.7`; its SHA-256 was `589253d36810f21217edd51545cd435b328cdc3cf4f451fbe0cce6f88afcf5e1`. The CLI log inspected during acceptance contained only the three `--version` invocations. No OpenCode authentication, provider or model calls were made.

Two environment issues were diagnosed before the successful Linux run:

- `scp` exited 255 because `/usr/lib/sftp-server` was absent. Transfer instead passed an open binary archive file directly to SSH stdin using Python `subprocess`, avoiding PowerShell 5.1 text pipelines. Matching archive hashes verified byte preservation.
- The first unique scratch directory, `/tmp/opencode-baseline-verify-e76WOBHI.tmp`, was on a `noexec` mount. Its unit run exited 1 with 36 failure records and three Windows-only skips: fake runtime files had mode 755 but were not executable, so runtime discovery reported missing. Direct execution reproduced `EACCES`. Moving the unchanged archive and test scratch to the executable `/workspace` mount, with `TMPDIR` there too, resolved every failure. Production code and tests were not changed.

Acceptance outputs, installed receipts/configuration, edited fixtures, installer script and CLI log were reviewed before cleanup; the durable results are recorded above. Both unique Linux directories and the unique Windows directory were removed, with absence checks returning 0. The temporary CLI and its legacy shim were removed with the Linux scratch directory. Before/after snapshots confirmed the builder's original `PATH`, shell-profile hashes and OpenCode home/config/cache/data/state paths were unchanged; no CLI remained on the original `PATH` or in `/home/builder/.opencode/bin`.

This completes the Windows/Linux acceptance gate. Rollout remains an `ops-infra` task. `sim-funds` and `sim-prime-broker` were not accessed; their recorded OpenCode 2.2.5 rollout is historical evidence, not a claim about their current state.

### Final-review regression verification — 2026-11-11

Behavioral fixes in `73af5e09818414aa29442d18562429efb4edc351` (base `b2bbcb279690bfb79c00422ceda2e7b33e6a95fc`) close I1 and M1. Enumerated Linux names use native path inspection; managed and receipt paths retain strict portable validation. Local ownership recognizes inspected filesystem identities for both leaves and ancestors, after rejecting links, rather than assuming case-insensitivity. M2 is closed by this self-contained record and the removal of disposable evidence dependencies. The Task 8 results above remain the historical real-runtime acceptance.

Tests were written and run before production changes. On Windows, the edited case-only command upgrade falsely printed `Local commands/XM-Old.md`, and both skill-directory upgrade cases falsely printed `Local skills/Writer/`: three failing subcases in the two upgrade tests, with the Linux-only test skipped. On Linux, the new native-filename test failed with exit 1 and `Result could not complete` at `commands/local:notes.md`; both case-only upgrade tests passed on its case-sensitive storage.

After the fixes, the Linux regression asserts exit 0, `Result MATCH`, unchanged source/destination file bytes and mtimes, unchanged directory mtimes, and these exact Local lines:

```text
Local commands/local:notes.md
Local commands/local\notes.md
Local skills/demo/local:refs/
Local skills/demo/local\refs/
```

Case-only command upgrades now report `Local none` on Windows; Linux still reports the distinct edited retired file as `Local commands/XM-Old.md`. For a case-only skill ancestor upgrade containing a local child, Windows reports `Local skills/Writer/local.md`, while Linux reports the distinct unowned directory once as `Local skills/Writer/`. Both edited and untouched upgrade cases pass. Symlinks to managed leaves and ancestors remain Local links, without traversal.

Final runs used Windows Python `3.15.1` and Linux Python `3.15.2`; UTC start times were 2026-11-12 04:12:35. Each full suite ran once after the final code/test changes. The focused selection below is `tests.test_baseline.LocalTests tests.test_baseline.CheckTests tests.test_baseline.RetirementTests tests.test_baseline.ReceiptTests`.

| Platform / command from source directory | Exit | Actual result |
|---|---:|---|
| Windows: `uv run --no-project python -m unittest -v <focused selection>` | 0 | 83 tests, `OK (skipped=10)` |
| Linux: `python3 -m unittest -v <focused selection>` | 0 | 83 tests, `OK`; all symlink cases and native-name regression executed |
| Windows: `uv run --no-project python -m unittest discover -s tests -v` | 0 | 109 tests in 49.364s, `OK (skipped=10)`; nine symlink-related skips and one Linux-only filename test |
| Linux: `python3 -m unittest discover -s tests -v` | 0 | 109 tests in 16.779s, `OK (skipped=3)`; only Windows PowerShell modes, wrapper and fallback tests skipped |

Windows ran from `C:\Users\preid\github\opencode-defaults`, with child-process `TEMP` and `TMP` set to `C:\Users\preid\AppData\Local\Temp\opencode\final-fix-e18136fc389645098e94dba750776256.tmp` and `PYTHONDONTWRITEBYTECODE=1`. The Linux source was a `git archive` of `b2bbcb2` overlaid only with the tested `install.py` and `tests/test_baseline.py` bytes committed in `73af5e0`. Binary-file stdin to `ssh -T workspace-smoke 'cat > /workspace/opencode-final-fix-mmKowI9l.tmp/source.tar'` preserved the archive SHA-256: `2e7d6e47682186381e3b5043c81734fb7826cef90872029e87e46f6729476577`. No SFTP or text-pipeline transfer was used.

The final Linux suite's remote command was the following (`L` is defined here for exact path expansion). The focused suite used the same environment and source directory with its command above.

```sh
L=/workspace/opencode-final-fix-mmKowI9l.tmp
cd "$L/src"
env -i HOME="$L/home" TMPDIR="$L/tmp" \
  PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games \
  SHELL=/bin/bash LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  XDG_CONFIG_HOME="$L/xdg/config" XDG_CACHE_HOME="$L/xdg/cache" \
  XDG_DATA_HOME="$L/xdg/data" XDG_STATE_HOME="$L/xdg/state" \
  XDG_RUNTIME_DIR="$L/xdg/runtime" \
  python3 -m unittest discover -s tests -v
```

Both platforms again computed baseline fingerprint `a77a2a838e31e785883a741616ded0140a5f21b3d09d3f744ea4007f6deebf1e` and fixture fingerprint `83483d0562b62bc84626144a38495270e1dd0a0411350d3b5e1b2c8a29ec842d`. These regression runs used fake CLIs, needed no provider credentials and downloaded no runtime. The executable `/workspace` scratch/TMPDIR avoided the known `/tmp` noexec constraint.

Results were captured locally before removing the two unique scratch directories named above. Their absence was verified; the Linux before/after audit matched for the original PATH, shell-profile hashes and absent OpenCode home/config/cache/data/state locations. Global configuration and simulators were not changed. Final diff checks passed, and the unrelated cross-model document edits remained byte-identical and unstaged.
