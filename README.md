# OpenCode Defaults (`opencode-defaults`)

Lean, cross-platform OpenCode V2 base defaults for Windows PCs, Linux hosts (`amd-halo`), and Docker workspace containers (`ops-infra`).

See the [documentation index](docs/README.md) for maintained specs, completed plans and their original approval sources.

## What Is Included

| Source | Installed location / purpose |
|---|---|
| `global/opencode.json` | Native OpenCode V2 model defaults and cross-model agent profiles, `superpowers` plugin, `context7` MCP, and optional `~/.config/opencode/AGENTS.local.md` |
| `global/commands/*.md` | Five opt-in `/xm-*` cross-model planning and review commands installed into global `commands/` |
| `shared_harness.py` + `/shared-harness-*` | Receive-only public updates and neutral per-workspace difference reports |
| `global/AGENTS.md` | Short, OS-neutral global working and communication rules |
| `.opencode/skills/writer/` | Concise, practical voice for emails and workplace/personal correspondence; use `@writer` explicitly for other prose |
| `.opencode/skills/frontend-design/` | Visual UI design craft + `references/ui-preferences.md` for greenfield interfaces |
| `.opencode/skills/data-preferences/` | Analytical data defaults: local/NAS first, Google Cloud / Google Drive when cloud storage is needed, raw CSV + Parquet + Polars + DuckDB |
| `.opencode/skills/project-setup/` | New-repository bootstrapping & `opencode-defaults` adoption + `references/preferred-devtools.md` conditional tool register |
| `.opencode/skills/skill-authoring/` | [Agent Skills](https://agentskills.io/home) progressive-disclosure spec, OpenCode V2 layout, and `skills-ref` validation |
| `.opencode/skills/naming-files/` | File naming plus shared spec, plan and archive conventions |
| `.opencode/skills/naming-directories/` | Concise lowercase hyphenated directory, hierarchy, and `.tmp` naming rules |
| `.opencode/skills/socratic-tutor/` | Opt-in Socratic tutoring loop ("teach/tutor/quiz/drill me") adapted from Jane Street's `agent_skills` |

Domain-specific MCP servers, plugins, and skills stay out of this base harness so unrelated workspaces pay zero extra context tokens.

## Install Once per Workspace

Requires Git, Python 3.10+ (or `uv`), and the OpenCode CLI version in [`baseline.json`](baseline.json). This repository is public; downloading defaults needs no GitHub account or token. Provider sign-ins remain separate in each workspace.

```sh
git clone https://github.com/patrickreidy6/opencode-defaults.git "$HOME/.local/share/opencode-defaults"
cd "$HOME/.local/share/opencode-defaults"
```

**Windows (PowerShell):**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -WhatIf
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1
```

On Windows, keep the standalone OpenCode CLI binary at `$HOME\.opencode\bin\opencode.exe` on your User `Path` rather than unpacking `opencode.exe` into a custom folder such as `%LOCALAPPDATA%\Programs\OpenCodeCLI`. OpenCode only detects standalone `curl` installs at `~/.opencode/bin/opencode.exe`; custom paths skip CLI/TUI updates with `installation method not found`. After an OpenCode CLI upgrade, run `opencode service restart` from a new terminal so the background server switches to the updated binary.

**Linux / Halo Docker Workspaces (`bash` / `sh`):**
```sh
sh ./install.sh --dry-run
sh ./install.sh
```

In `ops-infra` containers where `/home/builder` is persistent and `/home/builder/.local/bin` is on `PATH`, install the pinned OpenCode V2 version and link its binary once per workspace. Run from the selected defaults source directory (replace `python3` with `uv run --no-project python` if using `uv`):
```sh
version="$(python3 -c 'import json; print(json.load(open("baseline.json"))["opencode"])')"
curl -fsSL https://opencode.ai/v2/install | bash -s -- --version "$version"
ln -sf "$HOME/.opencode/bin/opencode" "$HOME/.local/bin/opencode"
sh ./install.sh
```
(`opencode upgrade` resolves symlinks via `realPath`, so `~/.local/bin/opencode -> ~/.opencode/bin/opencode` preserves automatic `curl` updates while working in non-login SSH shells.)

Keep this checkout as the workspace's clean upstream cache. Author improvements in your normal `opencode-defaults` development checkout and push them to `main`; each workspace chooses when to receive them. The installer adds the global slash commands, so they are available from any project in that workspace.

## Periodic Drift and Update

Run each command as its own OpenCode submission:

```text
/shared-harness-drift
```

This fetches public `main` into the source cache and reports:
- **Upstream:** shared files/settings added, changed or removed since the last installation receipt.
- **Workspace:** shared files/settings edited or removed locally since that receipt.
- **Local:** workspace-only global additions, reported at the first unowned boundary.
- **Project:** applicable project instruction/configuration files and `.opencode` extensions. This is an inventory, not a comparison of effective settings.
- **Runtime:** installed CLI version and the published default's pin.

Differences are normal. The report changes no installed or project files; only its dedicated Git source cache is refreshed. It exits successfully when inspection completes, even if differences exist. It shows paths/statuses rather than private values or file contents.

When ready, run:

```text
/shared-harness-update
```

**Behavior 2:** receive and apply public `main` in this workspace. Back up and replace edited shared files/settings, and remove previously managed retired items even if edited. Preserve workspace-only additions, provider credentials, `AGENTS.local.md`, and project files. Shared MCP definitions are replaced as complete definitions; shared root-array entries are tracked by value, with additional local entries preserved. No changes are sent upstream, proposed for review, or applied to another workspace.

The command fast-forwards only a clean `main` cache and runs its newly fetched updater. Dirty/diverged source checkouts or invalid receipts stop with an error. Existing receipt validation and backups still apply. The updater verifies the installation, applies the CLI pin with `opencode upgrade <version>` if necessary, and reloads configuration. If the CLI binary changed, it asks you to run `opencode service restart` from a terminal so it does not terminate the OpenCode session performing the update.

Both slash commands use a small fixed Python driver and one shell call on GPT-6.1 Sol low. They accept no arguments. They create `~/.local/share/opencode-defaults` on first use if an older installation was made elsewhere. The equivalent terminal commands, from any active project, are:

```sh
python3 "$HOME/.local/share/opencode-defaults/shared_harness.py" drift --project .
python3 "$HOME/.local/share/opencode-defaults/shared_harness.py" update
```

Use `uv run --no-project python` on Windows, or wherever preferred. `--destination <path>` selects an isolated configuration directory for diagnostics/tests. Updating also upgrades/reloads the CLI for the current user; that option does not isolate the runtime. `--check` below remains an offline strict baseline verifier, while `/shared-harness-drift` is the normal informational workflow.

### Installer Behavior
- Resolves destination to `--destination`, else `$XDG_CONFIG_HOME/opencode` (when absolute), else `~/.config/opencode`.
- Deep-merges `opencode.json` objects and **unions root arrays** (`plugins`, `instructions`, `skills`). Previous repository-managed Superpowers Git references are replaced by the selected pin; other plugin entries and machine-local auth settings are preserved.
- When `AGENTS.local.md` does not already exist, preserves any pre-existing custom `AGENTS.md` as `AGENTS.local.md` (loaded via `~/.config/opencode/AGENTS.local.md` in standard `~/.config/opencode` setups, and skipped silently when absent).
- Copies `global/commands/*.md` into `<destination>/commands/`. The receipt tracks installed files and baseline settings: on the next install, unchanged retired content is removed with a backup; locally changed retired content is kept and named. Other local commands are preserved.
- Writes `<destination>/opencode-defaults-receipt.json` after verifying the installed files. A missing receipt is bootstrap; an existing malformed, unreadable or unsupported receipt stops install and dry-run before writes. Restore a verified receipt from `<destination>/backups/harness-*/opencode-defaults-receipt.json`; if none exists, preserve the damaged receipt and reconcile ownership before deliberately bootstrapping without its retirement history.
- Backs up overwritten or removed files under `<destination>/backups/harness-<timestamp>/` and leaves unrelated files such as `service.json`, `cli.json`, and `commands/add-notes.md` untouched.

### Superpowers Version and Cache

[`global/opencode.json`](global/opencode.json) pins Superpowers to commit `22f0b463e7a5e579904dd6211a520321035526f7` (package version **7.0.2**). Fresh installations use that same source revision. Rerunning the installer replaces earlier `superpowers@git+https://github.com/obra/superpowers.git` string entries, including entries with a `#revision`, so old references do not accumulate.

The installer copies your settings, global instructions, commands, and personal skills into the OpenCode configuration directory. OpenCode downloads Superpowers and its bundled skills into its own package cache (`~/.cache/opencode/npm/` on the standard setup). Let each machine build its cache; the Git reference in this repository is the portable dependency declaration. OpenCode installs missing packages in the background and reuses downloaded copies.

To upgrade Superpowers deliberately:

1. Select and review an upstream revision, recording its full Git commit hash.
2. Update the `#commit` in `global/opencode.json`, the `PINNED_SUPERPOWERS` fixture in `tests/test_install.py`, and the version note above.
3. Run the [installer tests](#validation), then preview and apply the platform-specific installer using the commands under [Install Once per Workspace](#install-once-per-workspace).
4. Run `opencode plugin list` and confirm Superpowers loads from the selected revision. Commit and push the tested defaults. In each workspace, run `/shared-harness-drift`, then `/shared-harness-update` when ready.

OpenCode's `opencode plugin update` skips full-commit pins. Moving the pin in this repository is what selects the next Superpowers revision; see [OpenCode's plugin documentation](https://opencode.ai/v2/docs/plugins).

## Baseline and Check

The baseline fingerprint is a SHA-256 of every copied source file, `global/opencode.json`, and `baseline.json`. Installer scripts, tests, docs and Git metadata are not inputs. Each check reads one source folder and one destination, without changing either.

**Linux / Docker:**
```sh
sh ./install.sh --fingerprint
sh ./install.sh --check
sh ./install.sh --check --expect <fingerprint>
```

**Windows (PowerShell):**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -Fingerprint
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -Check
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -Check -Expect <fingerprint>
```

These lower-level commands are useful for offline installation verification and tests. Replace `<fingerprint>` with the full 64-character value of a selected baseline. `--check --expect` pins that specific source version; workspaces need not select the same version. Select a non-default destination with `--destination <path>` / `-Destination <path>` for install or check.

Exit codes: **0** for a match (or successful install/fingerprint), **1** for any finding, install failure or operation that could not complete, and **2** for usage errors. `--expect` requires `--check`; check, fingerprint and dry-run modes cannot be combined. Fingerprinting does not accept a destination.

`Local` lines name additions at the first unowned boundary: configuration key paths, extra-entry counts in root `plugins` / `instructions` / `skills` lists, local files under `agents/`, `commands/`, `skills/` and `plugins/`, and `AGENTS.local.md`. Nonempty unowned directories are named once without inspecting their trees. Each workspace can have its own additions; their presence alone never fails the check. The strict verifier preserves JSON types and list order; the slash-command drift report presents such differences neutrally.

To improve the defaults, edit and test this repo, then commit and push to `main`. Workspaces receive those improvements only when you invoke `/shared-harness-update` there. Choose a tested CLI version in `baseline.json`; updates apply that pin. There is no central rollout service, shared GitHub credential, or private-repository archive-delivery step.

The check covers only the installed global baseline and CLI version, **not** the running server version, project or system overrides, environment substitutions, plugin loading, MCP connectivity, provider access or model behavior. It detects accidental drift and is **not tamper-proof**: the source and installer are writable by the workspace user.

## Model Defaults

| Role | Model |
|---|---|
| New-session default | `openai/gpt-6-astra` |
| `title` | `openai/gpt-6.1-sol#medium` |
| `explore` | `openai/gpt-6-astra#medium` |
| `general` | `openai/gpt-6-astra#high` |

These agent defaults apply in every project. Explicit command or dispatch model overrides take precedence. The root model does not retain a reasoning variant; select the desired effort for the main session through `/models`. Switching a primary agent alone does not reliably switch an already-selected session model. See the [V2 models](https://opencode.ai/docs/models/) and [agents](https://opencode.ai/docs/agents/) references.

Use the OpenAI provider connected to the account that holds your API credits. Model selection does not verify credit eligibility or impose a spending cap. A new subagent has fresh conversation context, but its own instructions, task, file reads and tool results still consume tokens. Long-context pricing is evaluated per model request, including subagent requests; it is not the sum of all agents' usage. Fresh tasks reduce context growth but do not guarantee staying below a pricing threshold. Default compaction targets the model's context limit, not its cheaper pricing tier.

## Opt-In Cross-Model Workflow

Use this for foundational specs and new codebases where extra independent review is worthwhile. Invoke the commands explicitly in the OpenCode TUI; normal Plan and Superpowers sessions use the ordinary workflow. Maintained artifacts from each workflow use the locations in [`naming-files`](.opencode/skills/naming-files/SKILL.md): maintained specs at `docs/specs/<topic>-design.md`, active plans at `docs/plans/YYYY-MM-DD-<topic>.md` (creation date), and completed plans at `docs/plans/archive/`. Repository instructions may specify another arrangement. The built-in Plan agent's write restriction still applies; use Build to persist its selected draft at the repository path before implementation. Design decisions, verified behavior, scripted invocation and maintenance steps are in [`docs/specs/cross-model-workflow-design.md`](docs/specs/cross-model-workflow-design.md).

| Command | Model | Behavior |
|---|---|---|
| `/xm-spec-review <spec-path>` | GPT-6 Astra `xhigh` | Fresh reviewer judges scope and value, protects the core payoff, and recommends what to remove, shrink or defer |
| `/xm-plan-write <spec-or-plan-path>` | Claude Fable 5.2 `high` | Current session writes or revises a focused plan with clear task outcomes, shared contracts and checks, preserving the approved scope |
| `/xm-plan-review <plan-path>` | Gemini 4 Carbon `high` | Fresh reviewer checks technical feasibility, spec coverage, interfaces and tests |
| `/xm-plan-simplify <plan-path>` | GPT-6 Astra `xhigh` | Fresh reviewer proposes justified reductions in scope and complexity |
| `/xm-code-review <plan-or-spec-path> [base-ref]` | Claude Fable 5.2 `high` | Fresh reviewer checks the branch and local changes against the requirements |

### Typical sequence

1. Select `anthropic/claude-fable-5-2#high` using `/models` and brainstorm the feature with Superpowers. Save its maintained design at `docs/specs/<topic>-design.md`.
2. Run `/xm-spec-review <exact-spec-path>`. The authoring session presents the recommendations and waits for you to choose which scope changes to accept before editing the spec.
3. Run `/xm-plan-write <exact-spec-path>` instead of replying "approved" to brainstorming (which would continue into the ordinary Superpowers planning workflow). The command approves the spec for planning, not implementation. It loads `writing-plans` and saves the implementation plan at `docs/plans/YYYY-MM-DD-<topic>.md`, with a spec link and clear status. Revise an already selected active plan in place. The planner returns the exact saved path and ready-to-use optional review commands.
4. For both perspectives, submit `/xm-plan-review <exact-plan-path>` and `/xm-plan-simplify <exact-plan-path>` against the same unchanged plan and spec. Both run in background child sessions and include plan/spec content hashes in their reports. When both are requested, wait for **both**, confirm their paths and hashes match, then reconcile them in one revision. If either input changed, rerun the stale review against the current draft first. Each report carries this hold instruction for the parent session. Reviews are opt-in; requesting only one does not require waiting for its companion.
5. Approve the revised plan. Start a fresh Build session, select `openai/gpt-6-astra#high`, and ask it to execute the plan using `subagent-driven-development`, giving it the plan and spec paths. Unoverridden `general` workers also use Astra `high`.
6. Before merging, run `/xm-code-review <exact-plan-path> <base-ref-or-SHA>`. The reviewer inspects committed, staged, unstaged and relevant untracked changes. Give an explicit starting SHA when working directly on main/master; the command will not interpret an empty branch comparison as approval. Resolve findings in the implementation session.
7. After implementation and verification, the Build session marks the plan complete, moves it to `docs/plans/archive/` with the same filename, and repairs links. Maintained specs stay in `docs/specs/`; `.superpowers/sdd/` remains tool-managed execution state.

Use explicit paths, especially when several specs/plans are active. Quote paths containing spaces. For omitted paths, spec commands inspect top-level Markdown documents in both `docs/specs/` and legacy `docs/superpowers/specs/`; plan reviews inspect `docs/plans/` and legacy `docs/superpowers/plans/`; code review inspects all four. Exclude archives, nested documents and indexes such as `README.md` and `index.md`. Select only when exactly one eligible document remains across the relevant directories; otherwise list candidates and request an explicit path. The in-session planner may also use a spec already explicitly selected in the conversation. An explicit missing path fails without substitution. Reviews accept explicit archived paths. `/xm-plan-write` also accepts an explicit active or archived plan: it resolves that plan's governing spec, revises a selected active plan, or creates a new active follow-up plan from an archive. If the governing spec cannot be resolved, it requests the exact spec path instead of inventing a spec or approval.

The four review commands use `xm-reviewer`, a child-only agent with file edits and delegation denied and shell access limited to Git inspection. Reviews return findings to the parent rather than editing artifacts. They cannot run the test suite: provide test evidence or run the requested checks in Build. For spec reviews, you choose the scope changes before the author revises; for other reviews, the author reconciles feedback and you approve the result.

`xm-spec-review` gives an opinion on whether the proposed build is worthwhile and appropriately sized, with a bias toward justified reductions. It reads the spec and relevant code/docs without requiring Git metadata. Its report identifies what to protect, what to cut and any essential gaps, then recommends a build boundary. It checks completeness where omissions threaten the intended outcome; technical plan coverage is checked by `/xm-plan-review`.

`xm-plan-write` uses `xm-planner`, a primary agent with edit permissions for `docs/plans/*.md` and legacy `docs/superpowers/plans/*.md`; explicit archive denies follow both allow rules. OpenCode wildcards also match subdirectories, so the later archive denies are necessary ([permission matching](https://opencode.ai/docs/permissions#matching)). New plans go in `docs/plans/`; an explicitly selected legacy active plan can be revised in place. Shell commands and delegation are disabled. Run it from the repository root. For a repository-defined alternative, add a project-local `agents.xm-planner.permissions` edit rule for that path and a later deny for its archive. The command pins Fable 5.2 `high` for its invocation; check the session model before later revision turns and reselect Fable 5.2 `high` if needed. The session remains in `xm-planner`; switch back to Build before editing a spec, archiving, committing, or implementing.

The planner preserves approved exclusions and deferrals, justifies consequential implementation additions, and leaves routine coding choices to Astra. It uses the `writing-plans` structure with explicit overrides for proportional detail, no fixed review-case quota and the cross-model handoff. Verification commands in a plan are proposed checks, not executed test evidence.

The plan and code reviewers include simulation/evaluation questions where relevant: independent actor state, virtual-time causality, reproducibility and separation of hidden evaluation truth from observations. Plan writing carries forward the approved spec's domain constraints without a fixed domain checklist. The spec review weighs domain-specific concerns by their effect on value and scope.

Connect Anthropic, OpenAI and Google on each workstation/container using the workflow. Config reloads automatically; `/reload` forces a refresh. Check resolved agents with `opencode api get /api/agent` and command registrations with `opencode api get /api/command`. For a specific project, append `?location[directory]=<URL-encoded-absolute-project-path>`; the API's default location may be your home directory rather than the shell's cwd. A configured model still needs working provider access. Commands are prompt templates, not an enforced orchestration engine; use the TUI rather than assuming `opencode run "/xm-..."` executes a command. See [V2 commands](https://opencode.ai/docs/commands/).

## Starting a New Project Repo With Extra MCPs or Plugins

Once `opencode-defaults` is installed globally on a machine or container, every repo automatically inherits `superpowers`, `context7`, your model defaults, and global skills (including [`project-setup`](.opencode/skills/project-setup/SKILL.md)). Installing the `opencode` V2 runtime executable is separate from applying `opencode-defaults`: bootstrap `opencode` first when an environment does not have it yet, then run `install.ps1` / `install.sh`. You do **not** copy files from `opencode-defaults` into new repositories.

Example prompt to bootstrap a project with your conditional tooling preferences:

```text
Set up a new repo to build a website using opencode-defaults to define the base OpenCode harness installation.
```

`project-setup` reuses or installs the shared base, evaluates [`preferred-devtools.md`](.opencode/skills/project-setup/references/preferred-devtools.md) against the project's actual needs (rather than installing every listed tool indiscriminately), and reports selection, config, runtime connection, and account sign-in separately. It adopts the shared spec/plan convention unless repository instructions specify another arrangement, preserving existing documents in other repositories. See [`docs/specs/project-setup-design.md`](docs/specs/project-setup-design.md) for the design specification and Halo/Docker browser boundary.

When starting a new repo (for example, a website repo `xyz` that needs extra MCP servers `abc` and `def`), declare **only** the project-specific additions in `xyz/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "abc": {
        "type": "remote",
        "url": "https://mcp.example.com/abc"
      },
      "def": {
        "type": "local",
        "command": ["npx", "-y", "@example/def-mcp"]
      }
    }
  }
}
```

(Or run `opencode mcp add abc --url ...` from inside `xyz`.) OpenCode V2 merges `~/.config/opencode/opencode.json` + `xyz/opencode.json` at runtime, so `xyz` gets `superpowers` + `context7` + `abc` + `def` while all other workspaces remain lean.

### Optional Workstation Browser MCP (`chrome-devtools`)

`chrome-devtools` is kept out of `global/opencode.json` because `--autoConnect` requires a local desktop Chrome session and does not apply to headless Halo/Docker containers (`ops-infra` provisions container browser services separately via `--browser-url={env:CHROME_CDP_URL}`). Configure it once per desktop workstation in `~/.config/opencode/opencode.json`; `install.py` preserves machine-local `mcp.servers` entries on future updates.

1. Ensure **Google Chrome 144+** and **Node.js LTS** (`winget install --id OpenJS.NodeJS.LTS --exact` on Windows) are installed.
2. Start Chrome, open `chrome://inspect/#remote-debugging`, and enable remote debugging on the profile used for project/dashboard work.
3. Register the pinned MCP server globally on that workstation:
   - **Windows** (`cmd.exe /d /c` runs `npx.cmd` reliably under stdio; explicit `Path` lets an already-running OpenCode background service find a freshly installed Node.js without restarting):
     ```powershell
     opencode mcp add chrome-devtools --global --env "Path=C:\Program Files\nodejs;{env:PATH}" -- cmd.exe /d /c npx -y chrome-devtools-mcp@1.12.0 --autoConnect
     ```
   - **Linux / macOS desktop:**
     ```sh
     opencode mcp add chrome-devtools --global -- npx -y chrome-devtools-mcp@1.12.0 --autoConnect
     ```
4. Verify `opencode mcp list` shows `chrome-devtools connected`, run a read-only browser check (`list_pages`), and click **Allow** on Chrome's connection prompt. Sign in to web dashboards manually in that Chrome profile; never store dashboard credentials in `opencode.json`.

For repository settings on GitHub, keep **Pull requests** and **Allow squash merging** enabled (for optional review of larger or agent-generated changes with single-commit history) and turn off **Projects**, **Allow merge commits**, and **Allow rebase merging** unless a project specifically needs them.

## Validation

Run the installer unit tests:
```sh
uv run --no-project python -m unittest discover -s tests -v
```

After changing `global/commands/` or the `xm-*` agents, also run the [live command check](docs/specs/cross-model-workflow-design.md#changing-models-prompts-or-permissions). It calls paid models, so it is not part of the unit tests.

Validate each skill against the [Agent Skills specification](https://agentskills.io/specification):
```sh
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/writer
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/frontend-design
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/data-preferences
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/project-setup
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/skill-authoring
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/naming-files
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/naming-directories
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/socratic-tutor
```

## Related Repos
- [pr3 — media](https://github.com/patrickreidy6/pr3)
- [pr5 — travel](https://github.com/patrickreidy6/pr5)
- [pr6 — trader](https://github.com/patrickreidy6/pr6)
- [pr7 — organization & workflow](https://github.com/patrickreidy6/pr7)
- [ops-infra — Halo workspaces](https://github.com/patrickreidy6/ops-infra)
