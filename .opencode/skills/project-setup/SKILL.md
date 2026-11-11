---
name: project-setup
description: Use when setting up a new repository with OpenCode or adopting opencode-defaults in an existing repository, including website projects.
---

# Project Setup

Bootstrap new repositories or adopt `opencode-defaults` in existing ones by pairing the shared global OpenCode base with only the project-justified tools from [references/preferred-devtools.md](references/preferred-devtools.md). Explicit user requirements and existing repository conventions always take precedence.

## When to Use
- Creating a new repository that uses `opencode-defaults` as its OpenCode base.
- Bootstrapping a website repository and selecting its development, browser, and UI tooling.
- Adopting or refreshing `opencode-defaults` for an existing repository.

Do **not** use for routine feature/bug work, visual-only edits (`frontend-design`), standalone browser/dashboard actions, general tool comparisons, or host/container infrastructure provisioning (`ops-infra`).

## Setup Workflow

1. **Inspect destination:** Read instructions, manifests, lockfiles, OpenCode configs, and `git status`. Preserve uncommitted work, established stacks, and existing design systems. Ask only about missing decisions that materially alter setup.
2. **Resolve defaults source:** Reuse an established `opencode-defaults` checkout; clone `https://github.com/patrickreidy6/opencode-defaults.git` outside the target repo only when absent. Never reset or pull over a dirty checkout, and read repository sources rather than copying a workstation's personal `~/.config/opencode/`.
3. **Select tools by rule, not as a bundle:** Read [references/preferred-devtools.md](references/preferred-devtools.md) before adding packages or MCPs. Even when asked to wire the "full preferred stack," evaluate each tool's selection rule against the concrete project and runtime environment.
4. **Ensure OpenCode runtime:** Verify `opencode` V2 (`2.0.4+`) in the target execution environment. If absent, load `opencode` and install the CLI binary separately—`opencode-defaults` configures OpenCode after the executable exists.
5. **Apply or reuse portable base:** Check `$XDG_CONFIG_HOME/opencode` (when absolute) or `~/.config/opencode`. Reuse an already-current installation; otherwise run the platform installer with dry-run preview first (`./install.ps1 -WhatIf` then `./install.ps1`, or `sh ./install.sh --dry-run` then `sh ./install.sh`). Stop and report any `opencode.jsonc` conflict for reconciliation rather than bypassing the installer.
6. **Configure project-owned additions:** Install selected libraries via the project's package manager and place project-specific MCPs/plugins in `<repo>/opencode.json` (or the repo's existing `opencode.jsonc` / `.opencode/opencode.json(c)`, avoiding competing config files) using exact tested package versions—never floating `@latest`. Do not copy global base files into the project or redefine a working global `mcp.servers.<name>` entry unless intentionally replacing it. Load `frontend-design` when visual interface work starts.
7. **Verify and document:** Check selected tools in the execution environment. Record verified stack facts, browser/connection assumptions, and a fast, deterministic, credential-free check command in `<repo>/AGENTS.md`, then run that command. Repeated setup must converge without duplicate dependencies, MCP entries, or instruction sections.

## Readiness Report Contract

State whether the global base was installed or reused, link verification evidence, and report every requested or candidate tool across four separate states:
- **Selection:** `selected` or `skipped` (state the project-specific reason).
- **Software / config:** `present`, `configured`, or `missing`.
- **Runtime / connection:** `verified`, `unverified`, or `blocked` (route unprovisioned managed-workspace browsers to `ops-infra`).
- **Account / access:** `unnecessary`, `awaiting manual sign-in/credentials`, or `verified`.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "User asked for the full preferred website stack in a rush" | Preferences are conditional rules, not a bundle. Skip Playwright on static sites without critical flows; keep existing web search unless Tavily or crawl/extract is needed. |
| "No Chrome in this container—install headless Chromium with `--no-sandbox`" | Managed workspace browser services, persistent profiles, and viewers belong to `ops-infra`. Report the `ops-infra` provisioning need instead of installing ad-hoc browsers inside builder containers. |
| "Use `@latest` in `npx` MCP commands" | Resolve and pin an exact tested package version so project configuration stays reproducible. |
| "Replace web-dashboard task tracking with a SaaS MCP" | Actioning project organization in web dashboards via `chrome-devtools` is an intentional workflow preference. Preserve it and note when the attached browser profile needs manual sign-in. |
