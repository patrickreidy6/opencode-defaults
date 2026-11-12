# Documentation

Maintained specs live in `specs/`, active plans in `plans/`, and completed plans in `plans/archive/`. Ordinary, XM and Superpowers work share the [`naming-files` convention](../.opencode/skills/naming-files/SKILL.md). Repository instructions can specify a different arrangement. There are no active plans in this repository at this migration.

## Specs and associated plans

| Maintained spec or requirements source | Associated plan | Status |
|---|---|---|
| [Baseline installation and verification](specs/baseline-verification-design.md) | [Baseline verification](plans/archive/2026-11-11-baseline-verification.md) | Complete; Windows/Linux acceptance and later regression results recorded in the spec. |
| [Cross-model workflow](specs/cross-model-workflow-design.md) | [Initial cross-model commands](plans/archive/cross-model-commands.md) | Complete; initial approval came from the conversation named in the plan. The maintained spec includes later changes. |
| [Project setup](specs/project-setup-design.md) | No separate retained plan | Skill implemented; the spec distinguishes current setup behavior, per-workspace browser prerequisites and historical verification. |
| Requirements in the plan's Contract | [Shared harness commands](plans/archive/2026-11-12-shared-harness-commands.md) | Complete; implementation, review, publication and workspace verification recorded in the plan. Related baseline spec is not its approval source. |
| Conversation requirements retained in the plan's Spec field | [Pin Superpowers](plans/archive/pin-superpowers.md) | Complete; tests, local deployment and skill loading recorded in the plan. No separate spec was saved. |

Completion archives the plan, not its maintained spec. Archived plans retain historical requirements, commands and evidence; they are not instructions to rerun completed work. Follow-up work gets a new active plan linked to its spec. Reviews may use an explicit archived path.

[Deferred cross-model work](specs/cross-model-workflow-design.md#deferred-work) tracks the separate boundary review and optional workflow-assistance/runner assessment.

## Document migration 2026-11-12

| Original path | Current path |
|---|---|
| `docs/baseline-verification-design.md` | [docs/specs/baseline-verification-design.md](specs/baseline-verification-design.md) |
| `docs/cross-model-workflow-design.md` | [docs/specs/cross-model-workflow-design.md](specs/cross-model-workflow-design.md) |
| `docs/project-setup-design.md` | [docs/specs/project-setup-design.md](specs/project-setup-design.md) |
| `docs/superpowers/plans/2026-11-11-baseline-verification.md` | [docs/plans/archive/2026-11-11-baseline-verification.md](plans/archive/2026-11-11-baseline-verification.md) |
| `docs/superpowers/plans/2026-11-12-shared-harness-commands.md` | [docs/plans/archive/2026-11-12-shared-harness-commands.md](plans/archive/2026-11-12-shared-harness-commands.md) |
| `.superpowers/plans/pin-superpowers.md` | [docs/plans/archive/pin-superpowers.md](plans/archive/pin-superpowers.md) |
| `.superpowers/sdd/cross-model-commands/plan.md` | [docs/plans/archive/cross-model-commands.md](plans/archive/cross-model-commands.md) |

Navigational links now use the current paths. Historical task commands, source paths in those commands, review hashes and approval wording remain as recorded; use this mapping when interpreting them. The two `.superpowers` documents were previously ignored local files. Other ignored Superpowers logs and execution state were retained during the migration. No other repository was migrated, and upstream Superpowers skills were not changed.

The remaining local `.superpowers` directory was subsequently removed from this repository at the user's request on 2026-11-12 (sent to the Recycle Bin). Its old run history does not configure save locations. The `.superpowers/` ignore rule remains, and Superpowers can recreate execution state there as needed; the shared spec and plan locations are unchanged.

Migration checks, live fixtures and the local installation are recorded in the [verification results](specs/cross-model-workflow-design.md#document-organization-and-surface-rollout-2026-11-12).

Migration checks confirmed all 17 remaining `.superpowers` files retained their SHA-256 hashes. Removing only the added archive notes and reversing the navigational/status updates reproduces the original SHA-256 of each of the four archived plans. Internal documentation links and anchors were also checked.
