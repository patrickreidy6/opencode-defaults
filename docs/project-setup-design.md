# Project setup skill: design specification

Design specification for `.opencode/skills/project-setup/`, updated 2026-11-10. Implemented in [`.opencode/skills/project-setup/SKILL.md`](../.opencode/skills/project-setup/SKILL.md) with the authoritative tool register in [`.opencode/skills/project-setup/references/preferred-devtools.md`](../.opencode/skills/project-setup/references/preferred-devtools.md).

## Intent

When Patrick asks to create a repository using `opencode-defaults`, install the portable OpenCode base and consult task-specific tooling preferences. A preference records what to choose when useful; it does not assert that a package, MCP server, account, browser, or service is already installed.

Website creation should bring the website preferences into the setup decision automatically. Existing repository requirements and explicit user choices take precedence. Dashboard actions will eventually run from Halo/Docker workspaces.

## Approach and activation

Use one small, on-demand `project-setup` skill. Repository bootstrapping includes runtime availability, inherited configuration, project dependencies, browser connections, and verification. The existing `frontend-design` skill is explicitly visual-only; reuse it for interface work rather than broadening it to cover installation. Keep detailed preferences out of always-loaded instructions.

Frontmatter:

```yaml
name: project-setup
description: Use when setting up a new repository with OpenCode or adopting opencode-defaults in an existing repository, including website projects.
```

Trigger on a new repository using this base, website-project setup, or explicit adoption/refresh of the base in an existing repository. Routine coding, visual-only edits, standalone dashboard actions, general tool comparisons, and host/container provisioning do not trigger this skill.

The skill must read `[references/preferred-devtools.md](references/preferred-devtools.md)` during setup. A preference is a selection rule, not evidence of installation or permission to install every listed tool. This design adds no framework, deployment-service, or database defaults.

## Authoritative tools register

See [`.opencode/skills/project-setup/references/preferred-devtools.md`](../.opencode/skills/project-setup/references/preferred-devtools.md) for the single maintained tool-selection table (OpenCode V2 + `opencode-defaults`, Superpowers, Context7, native OpenCode web search, optional Tavily, Chrome DevTools MCP, conditional Playwright, and `frontend-design` + Untitled UI React).

## Browser-runtime boundary

Support two portable connection modes:

- **Local workstation:** use the available Chrome installation and a verified connection to the intended profile. `--autoConnect` is one supported mode when Chrome is already running and remote debugging is enabled.
- **Managed workspace:** OpenCode and its MCP process run inside the workspace, connecting to that workspace's browser service through a provisioned endpoint.

The skill consumes and verifies the chosen connection. It does not create browser containers, images, volumes, network rules, or remote viewers. Those capabilities belong to `ops-infra`'s trusted management workflow. A missing browser endpoint is a provisioning need, not a reason to invent a URL or apply a desktop command to a headless container.

### Verified workstation setup vs. pending Halo/Docker provisioning

- **Verified on Windows ARM64 workstation (2026-11-10):** Chrome `156.0.8078.80` with `chrome://inspect/#remote-debugging` enabled, Node.js `26.13.0` LTS ARM64 (`OpenJS.NodeJS.LTS`) / npm `11.20.0`, and machine-global `chrome-devtools` MCP (`cmd.exe /d /c npx -y chrome-devtools-mcp@1.12.0 --autoConnect` with `Path=C:\Program Files\nodejs;{env:PATH}`). Confirmed `connected` in `opencode mcp list` and verified live tab listing via `list_pages` after approving Chrome's prompt. Kept machine-local in `~/.config/opencode/opencode.json` (preserved across `install.ps1` runs) rather than `global/opencode.json`.
- **Target design (pending `ops-infra` provisioning):** Per-workspace Chrome service, persistent browser profile, private login viewer, and `CHROME_CDP_URL` wiring for Halo/Docker workspaces as specified below.

### Halo/Docker target context

Recommended topology:

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
- Acceptance: connection, page snapshot, harmless dashboard action, local-site preview, profile persistence across recreation, operation with the Surface disconnected, and the existing workspace isolation checks.

Repository evidence: `ops-infra/AGENTS.md` permits project-owned service containers and requires independent workspace state; `container-defaults.md` adds Node/browser automation only for identified needs. Its management checkout stays on the Surface. This planning session inspected repository guidance, not live Halo state.

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
2. **Resolve the defaults source.** Use the supplied or established checkout and its instructions. If absent, obtain the canonical repository through its documented source. Preserve local changes; do not reset or silently refresh a dirty checkout.
3. **Consult preferences.** Read the bundled reference before selecting tools. Website setup considers browser inspection, repeatable browser tests and the existing UI preference automatically, selecting each only when useful for the actual project.
4. **Ensure the runtime.** Verify OpenCode V2 in the execution environment. When missing, use current official guidance and that environment's management conventions to bootstrap it. Load the `opencode` skill for OpenCode-specific setup. Installing the executable is separate from applying this repository's defaults.
5. **Apply or reuse the base.** Resolve the install destination using the existing installer rules. Reuse an already-current installation; otherwise preview and apply the platform installer. Preserve local additions through its merge/backup behavior. Reconcile an existing `opencode.jsonc` conflict rather than bypassing the installer's refusal. OpenCode resolves declared plugin packages separately.
6. **Configure project-owned tools.** Use the existing dependency system and configuration conventions. Place project-specific MCP/plugin declarations in the project's OpenCode configuration, reusing compatible inherited integrations. Avoid duplicate declarations or competing configuration files. Invoke `frontend-design` when visual work begins.
7. **Verify and document.** Check tools in the actual execution environment. Record selected tools, verified connections and a fast local check in the new repo's instructions. Distinguish missing accounts, unavailable components and unmet infrastructure provisioning from completed setup.

Repeated setup must converge on the same effective configuration without duplicate dependencies or instruction sections. Existing projects retain their stack and design system. The existing installer may create backups on repeated application; idempotence concerns effective configuration, not zero writes.

Deployment reuses `install.py`'s recursive copying of `.opencode/skills/`; no always-on global MCP bundle is added.

## Availability and completion

For selected tools, distinguish:

- **Selection:** preferred, selected, or unnecessary for this project.
- **Software/configuration:** missing, present, or configured.
- **Runtime/connection:** unverified, working, or blocked.
- **Account/access:** unnecessary, awaiting sign-in/access, or verified.

Configuration alone does not establish a working connection, and installed software does not establish account access. Keep credentials outside committed configuration. A handoff states the installed/reused base, selected additions, verification evidence, and any concrete blocker.

## Verification and acceptance

For a project being set up, document and run a fast, deterministic, credential-free check in its `AGENTS.md`. Reuse an existing command where possible; every documented command must exist. Match checks to the project's consequences of failure. Verify browser connectivity and authenticated dashboard access separately from the local check.

Skill verification (verified 2026-11-10):

- `tests/test_install.py` verifies both `project-setup` files deploy with source-matching bytes on initial and repeated runs alongside dry-run, merge, backup, and Superpowers pin tests (`10/10` passing).
- `skills-ref` validates both `.opencode/skills/project-setup` and the installed global copy.
- Subagent pressure scenarios verified conditional tool selection, Halo/`ops-infra` boundary compliance, existing-stack/dirty-worktree preservation, and negative-trigger non-activation.

```sh
uv run --no-project python -m unittest discover -s tests -v
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/project-setup
```

| Situation | Expected behavior |
| --- | --- |
| New website; OpenCode absent | Consult preferences, bootstrap the runtime separately, apply defaults, add justified project tools. |
| New repo; base already current | Reuse inherited defaults without copying them into the project. |
| Existing project with a custom stack and working changes | Adopt narrowly; preserve stack, design system and unrelated changes. |
| Preferred browser tool absent | Select it based on need; install/configure within scope or identify the specific provisioning requirement. |
| Simple site without meaningful repeatable flows | Do not add Playwright solely because it appears in the list. |
| Site with repeatable critical flows | Prefer project-owned Playwright tests and CLI execution. |
| Ordinary research with working native search | Retain the current provider; no automatic Tavily switch or extra MCP. |
| Browser connected; dashboard signed out | Report working browser and pending account access separately. |
| Container without provisioned Chrome | Route provisioning to ops-infra; do not apply desktop connection assumptions. |
| Routine visual edit or standalone dashboard action | Use the relevant existing workflow without repository setup. |
| Setup repeated | Effective configuration remains stable without duplicate declarations or instructions. |

No further preference decisions block this skill design. Technology choices, account access and browser endpoints are supplied by each actual setup task.

## Sources

- [OpenCode web search](https://opencode.ai/v2/docs/websearch)
- [OpenCode MCP servers](https://opencode.ai/v2/docs/mcp-servers)
- [Chrome DevTools MCP requirements](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Chrome connection and profile options](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md)
- [Playwright MCP versus CLI/skills](https://github.com/microsoft/playwright-mcp#playwright-mcp-vs-playwright-cli)
- [Agent Skills specification](https://agentskills.io/specification)
