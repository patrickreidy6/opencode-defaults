# Baseline installation and verification

Design proposed 2026-11-11. Patrick selected the installation receipt and check-command approach; this document is awaiting approval before implementation.

## Intent and scope

Make it easy to install the same reviewed OpenCode defaults in `sim-funds` and `sim-prime-broker`, then detect unexpected changes. Extend the existing Python standard-library installer and its shell wrappers. Keep project-specific configuration in each project's repository.

This repo owns baseline installation and local verification. `ops-infra` selects the commit deployed to each workspace and coordinates upgrades. Automatic synchronization, remote deployment, credential management, and runtime installation are outside this change.

## Approaches

- **Selected: installation receipt plus read-only check.** Records provenance and checks actual installed contents. A small extension to the existing installer supports both manual use and later `ops-infra` checks.
- **Considered: pinned commit plus manual checklist.** Less code, but cannot reliably detect edits after installation. Patrick chose the automated check.

## Baseline identity

- Use the full Git commit as the defaults revision, rather than another manually maintained release number. Record source modifications explicitly; a dirty or unidentifiable source is not certified as a reviewed baseline.
- Add `baseline.json` with a schema version and the expected exact OpenCode CLI version. The proposed starting version is `2.2.7`, observed locally with `opencode --version` on 2026-11-11. Halo compatibility remains a rollout check, not an asserted result.
- Keep model defaults and the Superpowers pin in `global/opencode.json`; avoid duplicating them in `baseline.json`.

## Installation receipt

After a successful installation, write `install-state.json` inside the resolved OpenCode configuration destination. Back up an existing receipt using the installer's existing backup mechanism and publish the new receipt only after verifying the managed output.

The versioned receipt records:

- Source commit and clean/modified/unknown provenance.
- Expected and observed CLI version, or an explicit unavailable status.
- Relative managed-file paths and SHA-256 fingerprints.
- The repository-owned configuration expectations needed to distinguish managed settings from local additions.
- Previously managed paths/settings that have been retired but still need reconciliation.

Record only repository-owned expectations, never a copy of the merged machine configuration or provider state. Validate receipt structure and relative paths before using it. A missing runtime or Git metadata can be recorded during installation without preventing the existing file-installation workflow.

Preserve the existing merge, backup, destination-resolution, and `opencode.jsonc` conflict behavior. Dry-run creates no receipt or other files. Reinstallation refreshes the receipt without forgetting unresolved retired assets; this change reports those assets rather than adding a general-purpose deletion policy.

## Check command

Add `--check` to `install.py`, passed through by `install.sh`, and expose `-Check` in `install.ps1`. Check mode and dry-run are mutually exclusive.

```sh
sh ./install.sh --check
sh ./install.sh --check --destination /path/to/opencode
```

The checkout running the command is the desired baseline. Compare its source identity and expectations with the receipt and the actual destination, so checking an old checkout cannot claim to match some newer deployment target.

Report missing or invalid receipts, revision differences, modified/unidentifiable source, missing or edited managed files, configuration differences, retired assets still present, and missing or mismatched CLI versions. CLI discovery uses a bounded `opencode --version` invocation. The checker verifies the installed binary, not the version of an already-running server.

Compare configuration structurally according to the existing merge rules: repository-owned values must match, owned root-array entries must be present, and managed MCP server definitions must match. Whole-file hashes are unsuitable for the merged configuration. Summarize local additions by configuration key or relative filename; additions outside managed ownership do not fail the baseline check. Diagnostics identify paths and statuses without printing local setting values or file contents.

Exit codes: `0` means the checked global baseline matches; `1` means drift or incomplete verification, including a missing receipt/runtime/provenance; `2` means invalid input or a check that could not be completed. Check mode makes no changes and needs no provider credentials or network connection.

A passing result covers the installed global baseline. Project and system overrides, environment substitutions, plugin loading, MCP connectivity, provider access, and model behavior require separate runtime checks. Describe this boundary in the output and README.

## Files and verification

Add `baseline.json`; extend `install.py`, `install.ps1`, and `tests/test_install.py`; update README usage and the root `AGENTS.md` verification guidance. `install.sh` already forwards arguments. Keep this document in the existing `docs/` folder.

Use isolated, credential-free fixtures to cover installation and repeat installation, receipt provenance, file/configuration drift, permitted additions, retirement tracking, invalid receipts, CLI mismatch/unavailability, and the zero-write contract. Inject or stub CLI discovery so tests do not depend on a real provider connection or installed OpenCode version. Run platform-specific wrapper tests only where their shell is available, and retain the existing installer regression suite.

Verify with `uv run --no-project python -m unittest discover -s tests -v` and an isolated install/check demonstration. Record Windows and Linux results separately; live simulator installation remains a later rollout step.

## Review checkpoint

The proposed behavior preserves local additions while making shared-baseline changes visible. Approval of this document is the next checkpoint; implementation planning follows approval.
