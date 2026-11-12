---
name: naming-files
description: Use when creating, saving, exporting, or renaming files, documents, reports, or artifacts outside tool- or language-mandated filenames.
---

# File Naming

- Use a short, recognizable title: `descriptive-title.ext`.
- Add a useful document/event date or reporting period when applicable: `YYYY-MM-DD-title.ext`, `YYYY-MM-title.ext`, or `YYYY-title.ext`.
- Prefer lowercase hyphenated words, with a hyphen between the date and title.
- Omit unknown dates; keep ongoing topics and projects undated unless a date helps distinguish them.
- Use numbering when an intentional order helps.
- Preserve exact filenames, paths, and extensions required by the user's request, caller/test contracts, downstream schemas, languages, frameworks, tools, or repositories (such as `AGENTS.md`, `SKILL.md`, `README.md`, `Dockerfile`, or Python `snake_case` modules).

## Repository specs and plans

Use this convention for ordinary, XM and Superpowers work unless the user or repository instructions specify another arrangement. These project document locations override the default save paths in Superpowers; do not edit upstream skills to apply them.

These locations do not override agent edit permissions. If the built-in Plan agent can only save a working draft under `~/.opencode/plan`, hand that draft to Build to save the selected maintained plan in `docs/plans/` before implementation. Saving the plan does not approve implementation.

- Maintain specs at `docs/specs/<topic>-design.md`. Keep the spec available and current after implementation; completing a plan does not archive its spec.
- Save new plans at `docs/plans/YYYY-MM-DD-<topic>.md`, using the plan's creation date. Revise the selected active plan in place, including an explicitly selected legacy plan, rather than creating competing copies. Do not rename existing plans merely to add or refresh a date.
- Every new plan must link its governing spec and state its status, such as `Draft`, `Approved`, `In progress`, or `Complete`. Do not infer approval from a filename or create a retrospective spec for historical work. When a historical plan's authority is a conversation or requirements within the plan, preserve and identify that provenance.
- For follow-up work on an archived plan, create a new active plan linked to the archive and the governing spec; leave the archived plan unchanged. Do not migrate another repository's existing documents as part of adopting these defaults.
- After implementation and verification, the Build session marks the plan `Complete`, records the verification outcome, moves it to `docs/plans/archive/` with the same filename, and repairs inbound links and the plan's relative spec link. The restricted XM planner cannot edit archives. Keep historical commands, approval evidence and review hashes intact, and record moved paths when needed to interpret them.
- Keep `.superpowers/sdd` for tool-managed execution state, not maintained specs or plans. Preserve logs and execution evidence when moving documents.

Return the exact saved spec and plan paths as applicable. When handing a spec or plan back, include ready-to-use optional XM review commands with the actual paths, for example `/xm-spec-review docs/specs/<topic>-design.md`, `/xm-plan-review docs/plans/YYYY-MM-DD-<topic>.md` and `/xm-plan-simplify docs/plans/YYYY-MM-DD-<topic>.md`. Quote paths containing spaces. Offer these commands without running them automatically or changing existing approval boundaries. If both plan reviews are requested, keep their plan and spec unchanged until both reports arrive and their paths and content hashes match.
