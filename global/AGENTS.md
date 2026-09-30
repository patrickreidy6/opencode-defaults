# Personal OpenCode Defaults

## Environment
- Windows 11; use the active shell's syntax. PowerShell 5.1 does not support `&&`.
- Python 3.14 is available at `C:/Python314/python.exe`. Prefer a project's virtual environment when provided; otherwise use `python` or that full path, not `python3`.
- Follow each repository's setup, architecture, commands, and design rules.

## Core behavior
- Identify the root cause before proposing a solution.
- Keep changes within the request. Do not add unrelated features, refactors, comments, error handling, or compatibility shims for removed code.
- Prefer editing existing files; create files only when necessary.
- Preserve unrelated changes and incomplete work.
- If a request is ambiguous, ask one clarifying question before making changes. Resolve routine details from the repo.
- Prefer simple, proven patterns and incremental delivery.

## Communication
- Lead with the answer. Keep responses concise and practical.
- No emojis, filler phrases, or trailing summaries.
- Reference code with file paths and line numbers as Markdown links.

## Workflow
- For tasks touching more than three files, explore and plan before coding. Use Plan mode to agree on the approach before implementation.
- After implementing, run relevant checks and verify the requested result. Keep live external checks distinct from local or mocked verification.
- Prefer `/clear` between unrelated tasks.
- Use Context7 for current library, framework, SDK, API, CLI, and service documentation. General programming concepts and business-logic debugging do not need it.
- Keep credentials, OAuth tokens, session exports, generated outputs, and installed dependencies out of commits.

## Optional guidance
- For substantive new UI design, read `~/.config/opencode/preferences/UI_PREFERENCES.md`. Existing project design rules take precedence.
- For analytical storage or processing choices, read `~/.config/opencode/preferences/DATA_PREFERENCES.md`. Do not migrate an existing app's storage just to match these preferences.
- When creating, importing, reviewing, or updating skills, read `~/.config/opencode/guides/skill-authoring.md` and fetch the current Agent Skills specification. Use the built-in `customize-opencode` skill for OpenCode configuration work.
- General skills are installed globally; domain-specific skills belong in the application's `.opencode/skills/` directory.
