# Baseline installation and verification

**Workflow update, 2026-11-12:** this records the original offline baseline verifier and its historical acceptance. The current user workflow is [install once, inspect drift, receive updates](../README.md#periodic-drift-and-update). The repo is public; central archive delivery and identical workspace/`Local none` expectations are superseded. Updates explicitly reset shared items with backups while retaining workspace-only and project additions. The receipt/fingerprint and offline check remain useful implementation components.

Approved for planning 2026-11-11, with the review amendments recorded under Decisions.

## Intent

Install the same reviewed OpenCode defaults on every machine, starting with `sim-funds` and `sim-prime-broker`, and confirm it later with one command. Intentional project differences stay in each project's repository. This covers only the shared global baseline.

This repo installs a baseline and checks one installation against it. `ops-infra` decides which baseline each workspace should hold, delivers the source, and runs the check. A workspace receives this portable baseline, never a workstation's merged personal configuration.

## Goals and limits

- One identity for a baseline that survives being copied anywhere.
- A read-only check that passes only when an installation holds exactly that baseline.
- Reinstalling converges: content an earlier baseline installed and the new one drops is cleaned up.
- Local additions survive and never fail the check, unless placed where the installer would reorder them.

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

Write it last. Re-read each installed file, confirm its hash, then replace the receipt in one step. On any failure, exit nonzero and leave the previous receipt alone. Back up the previous receipt with the other overwritten files. Before trusting a receipt, validate its structure and that every path is relative and stays inside the destination.

A missing receipt is bootstrap. An existing malformed, unreadable or unsupported receipt stops install and dry-run before any writes. Name the receipt path and a safe reason, then give recovery guidance: restore a verified receipt from `<destination>/backups/harness-*/opencode-defaults-receipt.json`. If no valid backup exists, preserve the damaged receipt and reconcile ownership manually before deliberately bootstrapping without it; automatic retirement history will be lost. Never automatically delete or replace the invalid receipt.

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

**Configuration** matches when `json_equal(merge_settings(installed, baseline), installed)`: structural comparison preserves JSON types and list order, without sorting lists or treating `true` as `1`. List order counts, including within `plugins`, `instructions`, and `skills`. Reinstall may reposition a local list entry; that placement is drift. Reuse the installer's `merge_settings` so check and install cannot disagree; existing root-array membership and merge behavior stay unchanged. That one rule also covers changed values, a missing or altered managed MCP server, legacy V1 keys the installer strips, and a second Superpowers reference.

**Runtime:** run `opencode --version` with a short timeout, looking on `PATH` and then in the standalone install location `~/.opencode/bin`. Read the version as the official install script does: last word, leading `v` dropped. This checks the installed binary, not a server that is already running.

**Local additions** are listed at the first unowned boundary: configuration key names by key path, counts for extra entries in the root `plugins`, `instructions`, and `skills` lists, local files under `agents/`, `commands/`, `skills/`, and `plugins/`, and `AGENTS.local.md`. Stop at an unowned configuration key rather than inspecting its values. Treat the four directory roots as containers and walk deeper only along prefixes containing managed paths. List each nonempty unowned directory once, without descending its tree; skip directly empty directories. Names only, never values or contents. Print one plain, sorted `Local <item>` line per item, or `Local none` when there are no additions. Local presence alone is never a finding; a list placement that reinstall would change is a configuration finding. Surface additions are expected; `sim-funds` and `sim-prime-broker` should show `Local none`.

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
Local        commands/add-notes.md
Local        providers
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

Add `baseline.json`. Change `install.py`, `install.ps1`, `.gitattributes`, `tests/test_install.py`, `README.md`, the root `AGENTS.md`, and `.opencode/skills/project-setup/SKILL.md`. `install.sh` already forwards arguments.

`project-setup` reads the exact OpenCode version from the defaults source's `baseline.json` instead of requiring `2.0.4+`. Automatic use of the check inside the skill remains out of scope.

README: installing the runtime at the pinned version (the official install script accepts `--version`, and `opencode upgrade <version>` covers an existing install), how a workspace without repository access gets the source, the three modes, how to change the baseline, retirement in place of today's "managed command names are replaced on update" note, and the limits above. Upgrading the runtime means bumping `baseline.json`; until then the check fails on any machine that upgraded, including the Surface.

`docs/cross-model-workflow-design.md` tells maintainers to add a removed command to `RETIRED_PR4_FILES`. Update that note: the receipt now handles it.

Sequencing done: the `/xm-*` commands work has been committed; all five `global/commands/xm-*.md` files are tracked.

Tests use temporary directories with no credentials or network, and stub the CLI probe so they do not depend on an installed OpenCode. Cover:

- fingerprint: stable, changes with any input, equal for a copy without `.git`, and a fixed fixture yields a recorded value so the format cannot change silently;
- install: receipt written, repeat install stable, dry-run writes nothing, failed verification keeps the old receipt, an existing malformed/unreadable/unsupported receipt stops install and dry-run before writes;
- retirement: untouched file and setting removed with a backup, changed ones kept and named;
- check: passes after install, one case per finding, local additions listed at the first unowned boundary without values and not failing on presence alone, list placement that reinstall would change reported as drift, `--expect` match and mismatch, destination unchanged by the check;
- usage errors and both wrappers.

Verify with `uv run --no-project python -m unittest discover -s tests -v`. Before rollout, require Windows/Linux fixture fingerprint parity and an isolated install, check, edit, check run on both platforms: the first check passes with the pinned runtime and `Local none`, then the edited managed file is detected as drift. Keep SSH outside unit tests. A missing real Linux runtime or unavailable Linux host leaves acceptance pending; fake-CLI unit tests do not establish live runtime readiness.

Patrick authorized a verification-only exception: download OpenCode 2.2.7 only into a temporary `workspace-smoke` acceptance directory and remove it afterward. Task 8 exercised this permission and completed real Linux acceptance without a global install or a simulator runtime upgrade; results are recorded under Verified below.

## Left to the builder

Receipt field names, output wording, how the wrappers pass options, internal structure, and the timeout value.

## Decisions

Patrick's: receipt plus check command; then, after review on 2026-11-11, the content fingerprint, `--expect`, the pinned runtime, and removing retired files.

Calls made while revising, confirmed with planning approval:

- Untouched retired settings are removed like files, and anything changed locally is kept as a local addition. The review had left retired settings and edited files as findings until removed by hand, which would mean a hand edit on every machine each time the baseline drops a setting.
- The receipt holds no commit. Workspace copies carry no Git metadata to read it from, so the commit-to-fingerprint pairing lives in the `ops-infra` record.
- `--fingerprint` exists so `--expect` has a value to use.
- The check lists local additions by name and never fails on their presence alone; placement that the installer would reorder is drift.
- The runtime check looks on `PATH`, then in `~/.opencode/bin`.

Three `/xm-spec-review` reports on 2026-11-11 led to the amendments above. Patrick accepted trimmed #1 (Local reporting at the first unowned boundary) and #2–#5 (ordered merge comparison, `project-setup` reading the exact version from `baseline.json`, Windows/Linux acceptance before rollout, and stopping before writes on an existing invalid receipt).

## Verified

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
