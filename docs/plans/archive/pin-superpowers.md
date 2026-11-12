# Pin Superpowers Implementation Plan

**Status:** Complete and archived on 2026-11-12. Moved from `.superpowers/plans/pin-superpowers.md`.

**Approval provenance:** The Spec field below records the user-approved conversation requirements. No separate spec was saved for this work; the [current upgrade instructions](../../../README.md#superpowers-version-and-cache) are maintained guidance, not a retrospective approval source.

**Goal:** Reproduce the installed Superpowers revision across fresh installs and upgrades.
**Spec:** The user-approved plan in this session: pin commit 22f0b463e7a5e579904dd6211a520321035526f7; replace previous canonical Superpowers references; preserve other plugins; test migration, backups, dry-run and idempotence; document deliberate upgrades; deploy locally and verify skills load.
**Architecture:** Keep the package declaration in global/opencode.json and let OpenCode manage its package cache. Add narrowly scoped replacement behavior to the installer's root plugin-array merge.
**Tech stack:** Python 3.10+ standard library, unittest, OpenCode V2, PowerShell/sh wrappers.

## Constraints
- Keep existing backup behavior and unrelated configuration.
- Only repository-managed canonical Superpowers Git string references are replaced; aliases, forks, local plugins, object entries and disable directives retain existing union behavior.
- Use the existing checkout per the shared AI filing workflow's linked main-branch policy.
- No commit or push was requested by the execution plan; leave the source changes available for review.

## Review focus
- Exact upstream identity matching, including revision suffixes and near-match URLs.
- Migration from floating and older pins without duplicate references.
- Absence of a managed incoming reference must not remove an existing plugin.
- Preservation of plugin order, unrelated object options, backups and dry-run behavior.
- Repeat runs and a subsequent pin bump must converge on one selected reference.

### Task 1: Pin, migrate and test
- [x] Add failing migration tests in tests/test_install.py; update the existing installed-plugin expectation.
- [x] Run unittest discovery and observe failures from the missing pin/migration behavior.
- [x] Set global/opencode.json to superpowers@git+https://github.com/obra/superpowers.git#22f0b463e7a5e579904dd6211a520321035526f7.
- [x] Add minimal identity matching and replacement in install.py.
- [x] Run uv run --no-project python -m unittest discover -s tests -v; expected: all tests pass.

### Task 2: Document and review
- [x] Update README.md with config/cache responsibilities, managed-reference replacement and the deliberate pin upgrade workflow.
- [x] Review the diff and get one fresh-context review of the actual uncommitted changes.
- [x] Review reported no material findings; no fix pass or repeated suite was needed.

### Task 3: Deploy and verify
- [x] Preview the installer with install.ps1 -WhatIf.
- [x] Apply install.ps1 to the default destination.
- [x] Reopen installed opencode.json and verify exactly one selected pin and a recoverable backup.
- [x] Check OpenCode plugin status and invoke a Superpowers skill to verify it loads from the pinned package.

## Progress
- Baseline: 7 tests passed with uv run --no-project python -m unittest discover -s tests -v.
- Final: 10 tests passed; review found no issues; live plugin list and skill loader use the selected pin. Deployment backup: C:/Users/preid/.config/opencode/backups/harness-20261110-161159-522.
