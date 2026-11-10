# Personal OpenCode Defaults

## Environment
- Use the active OS and shell shown in `<env>` (`win32`/PowerShell vs `linux`/Bash). Note that Windows PowerShell 5.1 does not support `&&`.
- Prefer the project's `.venv` or `uv` (`uv run python ...`); otherwise verify a working `python3` or `python` executable rather than assuming a fixed path.
- Explicit request contracts, caller schemas, and the active repository's `AGENTS.md`/conventions always override global defaults; never alter a requested deliverable's shape.

## Behavior, Skills & Project Design
- Identify root causes before proposing fixes. Keep changes scoped to the request and preserve unrelated work. Keep the code you change easy to maintain: reuse existing logic and simplify duplication when it directly supports the requested change.
- Load on-demand global skills when triggered: `naming-files` (creating/renaming files), `naming-directories` (creating/renaming folders or `.tmp`), `data-preferences` (new storage/analytics choices), `frontend-design` (visual UI work), `writer` (prose deliverables), `socratic-tutor` (explicit "teach/tutor/quiz/drill me" requests), and `skill-authoring` (`SKILL.md` / workflow packaging).
- Design repos for self-verification and future improvement: document one fast, deterministic, credential-free check command in `<repo>/AGENTS.md`, and re-open/verify generated artifacts rather than trusting write exit codes alone.
- Put verified repo facts in `<repo>/AGENTS.md`, repeatable deterministic operations in `scripts/`, and situation-triggered workflows in `.opencode/skills/`. Treat `AGENTS.md` as zero-sum—trim when adding, and add rules/skills only from observed failures or repeated friction.
- Delegate bounded tasks when parallel work, specialized expertise, or independent review justifies the coordination cost; otherwise work directly.
- Declare project-specific MCP servers or plugins only in `<repo>/opencode.json` so other workspaces stay lean. Use Context7 for version-sensitive docs. Keep credentials, tokens, `.env` files, and generated outputs out of commits.

## Communication
- Lead with the answer. Keep responses concise and practical, with no emojis, filler phrases, or trailing summaries.
- Reference code with file paths and line numbers as Markdown links.
- When handing work back for review, summarize the outcome, link to verification evidence, and make any decision needed explicit with a recommendation.
