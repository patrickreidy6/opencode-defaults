# Personal OpenCode Defaults

## Environment
- Use the active OS and shell shown in `<env>` (`win32`/PowerShell vs `linux`/Bash). Note that Windows PowerShell 5.1 does not support `&&`.
- Prefer the project's `.venv` or `uv` (`uv run python ...`); otherwise verify a working `python3` or `python` executable rather than assuming a fixed path.
- Follow the active repository's `AGENTS.md`, architecture, commands, and conventions first.

## Behavior & Workflow
- Identify root causes before proposing fixes. Keep changes scoped to the request; preserve unrelated work.
- Prefer editing existing files over creating new ones.
- When starting or configuring a project repository that needs extra MCP servers or plugins beyond the global defaults (`superpowers`, `context7`), declare only those project-specific additions in `<repo>/opencode.json` so other workspaces stay lean.
- Use Context7 for version-sensitive library, framework, SDK, API, and CLI documentation.
- Keep credentials, OAuth tokens, `.env` files, and generated outputs out of commits.

## Communication
- Lead with the answer. Keep responses concise and practical, with no emojis, filler phrases, or trailing summaries.
- Reference code with file paths and line numbers as Markdown links.
