# Preferred Devtools

Authoritative preference register for `project-setup`. Treat each entry as a conditional selection rule—including for tools not yet installed—never as an unconditional bundle or proof of runtime availability. Existing project conventions and explicit user instructions override every default below.

## Tool Selection Register

| Tool | Role | Selection & configuration rule |
|---|---|---|
| OpenCode V2 + `opencode-defaults` | Portable agent harness | Shared global base in `$XDG_CONFIG_HOME/opencode` or `~/.config/opencode`. Bootstrap the `opencode` executable separately when absent; never copy `opencode-defaults` files into an application repo. |
| Superpowers | Agent workflow skills | Inherited automatically from the repository-managed full-commit pin in global `opencode.json`. Do not duplicate or re-pin per project. |
| Context7 | Version-current library docs | Inherited from the global remote MCP (`context7`). Reuse globally rather than redefining per project. |
| Native OpenCode web search | General web research | Default mechanism for ordinary web lookups. Keep the environment's active provider unless the user asks to change it. |
| Tavily | Optional search provider / site extraction | Do **not** switch `websearch.provider` to `tavily` unless requested or chosen for the environment. Add a project `tavily` MCP only when crawl, map, extract, or deep-research tools beyond native `websearch` are concretely needed. |
| Chrome DevTools MCP | Web-dashboard actions, live DOM/CSS/console/network/performance inspection | Preferred browser integration when dashboard operations or live browser inspection apply, including web-based project organization dashboards. Configure with an exact tested `chrome-devtools-mcp@<version>` and a verified browser connection for the target environment. |
| Playwright | Repeatable browser tests and scripted flows | Website-project option **only** when repeatable end-to-end flows, regressions, or scripted browser checks justify it (skip on simple static pages without critical flows). Prefer project devDependencies (`@playwright/test`) and CLI/test scripts over adding a second always-on browser MCP alongside `chrome-devtools`. |
| `frontend-design` + Untitled UI React | Greenfield interface design & component foundation | Load `frontend-design` (and its `references/ui-preferences.md`) when designing greenfield interfaces. Apply Untitled UI React only when React fits the requested deliverable and component access exists; preserve any existing framework, component library, or token system on established projects, and keep build-free static sites static unless asked otherwise. |

## Browser-Runtime Boundary

Support two connection modes without mixing their assumptions:

1. **Local workstation:** Connect `chrome-devtools-mcp` to the workstation's local Chrome installation (for example `--autoConnect` on Chrome 144+ with `chrome://inspect/#remote-debugging` enabled). Reuse an already-working global `chrome-devtools` MCP server rather than shadowing it in `<repo>/opencode.json`.
2. **Managed Linux / Docker workspace (`ops-infra`):** OpenCode and `chrome-devtools-mcp` run inside the workspace container and attach to a dedicated per-workspace Chrome service via `--browser-url={env:CHROME_CDP_URL}` (or `--wsEndpoint`) with a persistent workspace-owned profile and private human viewer (such as noVNC over SSH) for sign-in/MFA.

Boundary rules:
- Provisioning browser containers, images, persistent profile volumes, container networking, and human login viewers belongs to `ops-infra`'s trusted management workflow—never to ad-hoc `npx playwright install chromium` or `--headless --no-sandbox` browser installs inside a headless workspace when `CHROME_CDP_URL` is unprovisioned.
- When a managed workspace lacks a provisioned browser endpoint, omit the browser MCP entry or set `"disabled": true` in config, report `Runtime / connection` as `blocked`, and state the `ops-infra` provisioning requirement explicitly.
- When a browser service runs in a separate container, bind the project's dev/preview server to an address reachable from that browser service (`localhost` inside one container does not reach a sibling container).

## Availability Semantics

Keep these states distinct when configuring and reporting:
- **Configured != Connected:** Writing `mcp.servers` JSON does not prove Node/`npx`, Chrome, or the debugging endpoint works; verify with `opencode mcp list` and a read-only browser check when available.
- **Connected != Authenticated:** A working Chrome attachment can still be signed out of target web dashboards. Never embed credentials in committed config; ask the user to sign in manually in the attached browser profile when dashboard actions require authentication.
