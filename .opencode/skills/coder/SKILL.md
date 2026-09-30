---
name: coder
description: Apply the active project's coding conventions when changing application logic, fixing bugs, or reviewing code.
---

# Coder

## Project context

- Read the active repository's applicable `AGENTS.md` files and the code relevant to the change. Follow existing patterns rather than introducing a new architecture.
- Use the project's documented interpreter, virtual environment, dependency manifests, and commands with the active shell's syntax.
- Load credentials through the project's existing configuration mechanism; keep their contents out of output and commits.

## Scope and completion

- Fix the cause of a bug and keep changes within the requested scope. Preserve unrelated work in the working tree.
- Resolve routine implementation choices from nearby code. Ask when missing information would materially change the behavior or scope.
- For implementation tasks, completion means the requested behavior works and checks relevant to the change support that conclusion. Continue through fixes for failures caused by the change; report any genuine blocker precisely.
- Choose verification by risk: existing tests for affected behavior, a focused regression test for a meaningful bug, or direct output inspection for a small presentation change. Stop expanding verification once the relevant checks pass unless new evidence warrants it.
- For review tasks, deliver actionable findings with file and line references; edit code only if the request includes fixes.
