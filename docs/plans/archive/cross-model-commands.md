# Cross-model commands implementation plan

**Status:** Complete and archived on 2026-11-12. Moved from `.superpowers/sdd/cross-model-commands/plan.md`; related tool-managed execution state was subsequently removed from the repository at the user's request, as recorded in the [document index](../../README.md#document-migration-2026-11-12).

**Approval provenance:** The conversation cited below approved the initial implementation. The [maintained design record](../../specs/cross-model-workflow-design.md) describes the workflow and later changes; it does not replace that original approval. Model names below remain historical.

Approved spec: the current conversation, Setup (2), with title/explore = GPT-6.1 Sol medium and general = GPT-6 Astra high.

Goal: install opt-in cross-model slash commands alongside the existing Superpowers workflow, plus the approved global model defaults.

## Tasks
- [x] Task 1: Test command deployment, backup, dry-run and local-file preservation; extend collect_files and update model defaults.
- [x] Task 2: Add five commands with pinned models, document-writing and read-only agent profiles, and usage documentation.
- [x] Task 3: Run the full tests, isolated install, independent review, deployment preview and installation; inspect live agent/command resolution.

## Review focus
- A planner must be able to write the repository plan without implementing it.
- Reviewers must resolve their input from files without inherited parent history.
- Parallel reviews must target the same unchanged plan revision.
- A branch review must include committed and local changes, with a clear review base.
- Installer must back up managed commands and preserve unrelated local configuration.
