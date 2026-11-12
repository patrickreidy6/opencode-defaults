# Project setup skill: design specification

**Status: Implemented; maintained through 2026-11-12.** This spec describes the current [project-setup skill](../../.opencode/skills/project-setup/SKILL.md), including public-source setup, reuse of workspace defaults and project-specific tool selection. The [preferred-devtools reference](../../.opencode/skills/project-setup/references/preferred-devtools.md) is the authoritative tool-selection register. The [baseline spec](baseline-verification-design.md) owns installation, drift and update behavior. Dated verification records below describe past checks, not current machine or account readiness.

## Intent

When Patrick asks to create a repository using `opencode-defaults`, or adopt the base in an existing repository, install or reuse the workspace's portable OpenCode base and consult task-specific tooling preferences. A preference records what to choose when useful; it does not assert that a package, MCP server, account, browser, or service is already installed.

Website creation brings the website preferences into the setup decision automatically. Existing repository requirements and explicit user choices take precedence. Dashboard actions can use a workstation or a managed workspace when that environment has a verified browser connection and the required account access.

## Approach and activation

Use one small, on-demand `project-setup` skill. Repository bootstrapping includes runtime availability, inherited configuration, project dependencies, browser connections, and verification. The existing `frontend-design` skill covers interface design and visual implementation; reuse it for that work rather than broadening it to cover environment setup. Keep detailed preferences out of always-loaded instructions.

Frontmatter:

```yaml
name: project-setup
description: Use when setting up a new repository with OpenCode or adopting opencode-defaults in an existing repository, including website projects.
```

Trigger on a new repository using this base, website-project setup, or explicit adoption/refresh of the base in an existing repository. Routine coding, visual-only edits, standalone dashboard actions, general tool comparisons, and host/container provisioning do not trigger this skill.

The skill must read its bundled `references/preferred-devtools.md` during setup. A preference is a selection rule, not evidence of installation or permission to install every listed tool. This skill adds no universal framework, deployment-service, or database choice; it applies conditional tooling preferences without replacing an established stack.

## Authoritative tools register

See [`.opencode/skills/project-setup/references/preferred-devtools.md`](../../.opencode/skills/project-setup/references/preferred-devtools.md) for the single maintained tool-selection table (OpenCode V2 + `opencode-defaults`, Superpowers, Context7, native OpenCode web search, optional Tavily, Chrome DevTools MCP, conditional Playwright, and `frontend-design` + Untitled UI React).

## Browser-runtime boundary

Support two portable connection modes:

- **Local workstation:** use the available Chrome installation and a verified connection to the intended profile. `--autoConnect` is one supported mode when Chrome is already running and remote debugging is enabled.
- **Managed workspace:** OpenCode and its MCP process run inside the workspace, connecting to that workspace's browser service through a provisioned endpoint.

The skill consumes and verifies the chosen connection. It does not create browser containers, images, volumes, network rules, or remote viewers. Those capabilities belong to `ops-infra`'s trusted management workflow. A missing managed-browser endpoint is a provisioning need: omit the browser MCP entry or set `"disabled": true`, report `Runtime / connection` as `blocked`, and identify the required infrastructure. Do not invent a URL, apply a desktop command to a headless container, or install an ad-hoc browser there to bypass the provisioning boundary.

### Managed workspace requirements

The topology below is an infrastructure target, not a record of deployed services. The `ops-infra` source review on 2026-11-12 found no browser service in the `workspace/<name>/compose.yaml` definitions for `sim-funds`, `sim-prime-broker` or `workspace-smoke`. Actual provisioning and readiness must be established separately in each workspace; installation of the shared harness does not establish browser availability.

Target topology:

```text
Surface browser -- existing private SSH access --> per-workspace browser viewer
Halo workspace: OpenCode -> Chrome DevTools MCP -> that workspace's Chrome service
                                                       |
                                              persistent project profile
```

- Provision one optional browser service alongside each workspace that needs it. Its Chrome profile belongs to that workspace and survives browser/container replacement. Do not share a personal desktop browser or a profile between unrelated business workspaces.
- Run the MCP process in the development workspace. Attach it to the browser service with `--browser-url` (or `--wsEndpoint` when needed), rather than desktop `--autoConnect`.
- Provide a small browser-viewing interface, such as noVNC, for human login/MFA and inspection through the established private access path. The profile retains session state, subject to the site's session-expiry rules.
- Configure only the workspace-to-own-browser connection. Keep the browser control endpoint private; do not publish it publicly. Use the existing `ops-infra` management workflow for image, volume, network and viewer provisioning.
- The browser must reach both public dashboards and that project's preview server. Give the app an address reachable from the browser service; `localhost` in separate containers does not refer to the other container.
- Bind environment-specific connection values through configuration, for example `CHROME_CDP_URL`, and select an exact tested MCP package version at setup time. The exact endpoint and any needed forwarding depend on the deployed service and require a connection test.
- Record exact tested Chrome/MCP versions and the browser image digest. Keep persistent profiles separate from rebuildable package caches.
- Infrastructure acceptance: connection, page snapshot, an authorized harmless dashboard action, local-site preview, profile persistence across recreation, operation with the Surface disconnected, and the existing workspace isolation checks. The setup skill consumes the resulting endpoint and verifies the connection it needs; it does not perform infrastructure recreation as part of ordinary project setup.

`ops-infra/AGENTS.md` permits project-owned service containers and requires independent workspace state; `ops-infra/container-defaults.md` adds Node/browser automation only for identified needs. Its trusted management checkout stays on the Surface. These are infrastructure ownership rules; no live Halo/browser state was verified in this documentation review.

## Files and discovery

Durable layout:

```text
opencode-defaults/.opencode/skills/project-setup/
  SKILL.md
  references/preferred-devtools.md
```

| File | Role |
| --- | --- |
| `.opencode/skills/project-setup/SKILL.md` | Concise activation contract, ordered workflow, scope boundaries, and completion requirements. |
| `.opencode/skills/project-setup/references/preferred-devtools.md` | Single authoritative preference register, with selection/availability semantics and portable browser guidance. |
| `global/AGENTS.md` | On-demand skill discovery trigger for new-repository setup or `opencode-defaults` adoption. |
| `README.md` | Inventory entry, sample request, runtime-versus-defaults distinction, workstation `chrome-devtools` runbook, links, and validation command. |
| `AGENTS.md` | Source-layout skill inventory. |
| `tests/test_install.py` | Deployment and repeat-install byte-equality assertions for the skill and its nested reference. |

Portable skill content excludes workstation-specific paths, personal global configuration dumps, and duplicated visual-design guidance.

## Ordered setup behavior

1. **Inspect the destination.** Read applicable instructions, manifests, lockfiles, configuration and working changes. Identify new-project setup versus adoption. Clarify only choices that materially affect setup.
2. **Resolve the defaults source.** Use the public `https://github.com/patrickreidy6/opencode-defaults.git` checkout at `~/.local/share/opencode-defaults`, outside the target repository; clone there if absent. Downloading defaults needs no GitHub credential or management-delivered archive. Preserve local changes and stop rather than resetting or pulling over a dirty cache. Read the repository sources, not a workstation's merged personal configuration.
3. **Consult preferences.** Read the bundled reference before selecting tools. Website setup considers browser inspection, repeatable browser tests and the existing UI preference automatically, selecting each only when useful for the actual project.
4. **Ensure the runtime.** Read the exact `opencode` pin from the selected source's `baseline.json`. Run `opencode --version` in the execution environment, take the last whitespace-separated word and remove a leading `v`, then compare it with that pin. If the CLI is missing or differs, load the `opencode` skill and install that exact version using the environment's supported setup route; use `opencode upgrade <version>` for an existing installation. Installing the executable is separate from applying the defaults. The [README](../../README.md#install-once-per-workspace) provides platform setup details.
5. **Bootstrap or reuse the base.** Resolve the global destination as absolute `$XDG_CONFIG_HOME/opencode` or `~/.config/opencode`. For first installation, preview and apply the platform installer from the defaults source directory (`./install.ps1 -WhatIf` then `./install.ps1`, or `sh ./install.sh --dry-run` then `sh ./install.sh`). Reuse an existing workspace harness when adding another project. Periodic updates are opt-in: `/shared-harness-drift` reports differences, then `/shared-harness-update` receives public defaults with backups while preserving workspace-only and project additions. Different workspaces may choose different update times and local additions. Stop on an `opencode.jsonc` conflict rather than bypassing the installer. OpenCode resolves declared plugin packages separately.
6. **Configure project-owned tools.** Use the existing dependency system and configuration conventions. Place project-specific MCP/plugin declarations in `<repo>/opencode.json` or its existing supported configuration file, reusing compatible inherited integrations. Pin exact tested package versions rather than floating `@latest`. Avoid duplicate declarations, competing configuration files, or copying the global base into the project. Invoke `frontend-design` when visual work begins.
7. **Adopt document locations.** Load [`naming-files`](../../.opencode/skills/naming-files/SKILL.md). Unless repository instructions specify another arrangement, use `docs/specs/<topic>-design.md` for maintained specs, `docs/plans/YYYY-MM-DD-<topic>.md` for active plans, and `docs/plans/archive/` for completed, verified plans. Apply this convention to ordinary, XM and Superpowers work. Keep existing project documents and tool-managed `.superpowers/sdd/` state in place unless migration is requested.
8. **Verify and document.** Check selected tools in the actual execution environment. Record verified stack facts, browser/connection assumptions and a fast, deterministic, credential-free check command in the project's `AGENTS.md`, then run it. Distinguish missing accounts, unavailable components and unmet infrastructure provisioning from completed setup.

Repeated setup must converge on the same effective configuration without duplicate dependencies or instruction sections. Existing projects retain their stack and design system. The existing installer may create backups on repeated application; idempotence concerns effective configuration, not zero writes.

Deployment reuses `install.py`'s recursive copying of `.opencode/skills/`; no always-on global MCP bundle is added.

Shared update and ordinary reinstall have different retirement behavior: the update command backs up and removes edited retired shared items, while ordinary reinstall generally retains them as local additions. Use the [baseline spec](baseline-verification-design.md#retired-content) for ownership, receipt and failure semantics. The offline `--check` remains available for strict baseline verification; the setup skill does not automatically run it or require `Local none`.

## Availability and completion

Report every requested or candidate tool, including those skipped, using the skill's four separate states:

- **Selection:** `selected` or `skipped`, with the project-specific reason.
- **Software / config:** `present`, `configured`, or `missing`.
- **Runtime / connection:** `verified`, `unverified`, or `blocked`.
- **Account / access:** `unnecessary`, `awaiting manual sign-in/credentials`, or `verified`.

Configuration alone does not establish a working connection, and installed software does not establish account access. Verify a selected browser integration with `opencode mcp list` and a read-only browser check when available. When dashboard actions require authentication, the user signs in to the attached browser profile; keep credentials outside committed configuration. A handoff states whether the global base was installed or reused, links verification evidence, and identifies any concrete blocker.

## Verification and acceptance

For a project being set up, document and run a fast, deterministic, credential-free check in its `AGENTS.md`. Reuse an existing command where possible; every documented command must exist. Match checks to the project's consequences of failure. Verify browser connectivity and authenticated dashboard access separately from the local check.

For skill or installer changes, the relevant validation commands are below. `tests/test_install.py` checks that the skill and nested reference deploy with source-matching bytes on initial and repeated installation. Skill validation checks the package structure; neither check establishes a working browser connection or account access. Use scenario review for activation boundaries and conditional tool selection.

```sh
uv run --no-project python -m unittest discover -s tests -v
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/project-setup
```

| Situation | Expected behavior |
| --- | --- |
| New website; OpenCode absent | Consult preferences, install the exact source pin separately, apply defaults, add justified project tools. |
| OpenCode present but version differs from the selected source pin | Load the OpenCode setup guidance and align the CLI with `baseline.json`; do not treat any V2 version as sufficient. |
| New repo; workspace base already installed | Reuse inherited defaults without copying them into the project or automatically replacing the installed baseline. |
| Explicit shared-default update requested | Use the drift/update workflow; keep workspace-only and project additions while replacing shared items with backups. |
| Dedicated defaults cache has local changes | Preserve them and stop source refresh; do not reset or overwrite the cache. |
| Existing project with a custom stack and working changes | Adopt narrowly; preserve stack, design system and unrelated changes. |
| Preferred browser tool absent | Select it based on need; install/configure within scope or identify the specific provisioning requirement. |
| Simple site without meaningful repeatable flows | Do not add Playwright solely because it appears in the list. |
| Site with repeatable critical flows | Prefer project-owned Playwright tests and CLI execution. |
| Ordinary research with working native search | Retain the current provider; no automatic Tavily switch or extra MCP. |
| Browser connected; dashboard signed out | Report working browser and pending account access separately. |
| Container without provisioned Chrome | Omit or disable the browser MCP, report the runtime blocked, and route provisioning to ops-infra; do not apply desktop connection assumptions. |
| Routine visual edit or standalone dashboard action | Use the relevant existing workflow without repository setup. |
| Setup repeated | Effective configuration remains stable without duplicate declarations or instructions. |

No further preference decisions block this skill design. Technology choices, account access and browser endpoints are supplied by each actual setup task.

## Historical verification

These are the retained 2026-11-10 results. The version numbers and test total describe that check, not current pins, a fresh test run, or proof of present workstation/Halo readiness.

### Windows workstation — 2026-11-10

- **Verified on Windows ARM64 workstation (2026-11-10):** Chrome `156.0.8078.80` with `chrome://inspect/#remote-debugging` enabled, Node.js `26.13.0` LTS ARM64 (`OpenJS.NodeJS.LTS`) / npm `11.20.0`, and machine-global `chrome-devtools` MCP (`cmd.exe /d /c npx -y chrome-devtools-mcp@1.12.0 --autoConnect` with `Path=C:\Program Files\nodejs;{env:PATH}`). Confirmed `connected` in `opencode mcp list` and verified live tab listing via `list_pages` after approving Chrome's prompt. Kept machine-local in `~/.config/opencode/opencode.json` (preserved across `install.ps1` runs) rather than `global/opencode.json`.

### Skill verification — 2026-11-10

- `tests/test_install.py` verifies both `project-setup` files deploy with source-matching bytes on initial and repeated runs alongside dry-run, merge, backup, and Superpowers pin tests (`10/10` passing).
- `skills-ref` validates both `.opencode/skills/project-setup` and the installed global copy.
- Subagent pressure scenarios verified conditional tool selection, Halo/`ops-infra` boundary compliance, existing-stack/dirty-worktree preservation, and negative-trigger non-activation.

The later [shared-harness verification record](../plans/archive/2026-11-12-shared-harness-commands.md#verification-and-deployment-record) covers public-source updates, installer suites and project-setup skill validation on 2026-11-12. It does not establish managed-browser provisioning or revalidate the workstation browser connection.

## Sources

- [OpenCode web search](https://opencode.ai/v2/docs/websearch)
- [OpenCode MCP servers](https://opencode.ai/v2/docs/mcp-servers)
- [Chrome DevTools MCP requirements](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Chrome connection and profile options](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md)
- [Playwright MCP versus CLI/skills](https://github.com/microsoft/playwright-mcp#playwright-mcp-vs-playwright-cli)
- [Agent Skills specification](https://agentskills.io/specification)
