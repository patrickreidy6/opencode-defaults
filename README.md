# OpenCode Defaults (`opencode-defaults`)

Lean, cross-platform OpenCode V2 base defaults for Windows PCs, Linux hosts (`amd-halo`), and Docker workspace containers (`ops-infra`).

## What Is Included

| Source | Installed location / purpose |
|---|---|
| `global/opencode.json` | Native OpenCode V2 defaults: `openai/gpt-6-astra`, title model `openai/gpt-5.6-sol`, `superpowers` plugin, `context7` MCP, and optional `~/.config/opencode/AGENTS.local.md` |
| `global/AGENTS.md` | Short, OS-neutral global working and communication rules |
| `.opencode/skills/writer/` | Concise, practical prose voice for emails, messages, and docs |
| `.opencode/skills/frontend-design/` | Visual UI design craft + `references/ui-preferences.md` for greenfield interfaces |
| `.opencode/skills/data-preferences/` | Analytical data defaults: local/NAS first, Google Cloud / Google Drive when cloud storage is needed, raw CSV + Parquet + Polars + DuckDB |
| `.opencode/skills/skill-authoring/` | [Agent Skills](https://agentskills.io/home) progressive-disclosure spec, OpenCode V2 layout, and `skills-ref` validation |
| `.opencode/skills/naming-files/` | Concise lowercase hyphenated file and date-prefix naming rules |
| `.opencode/skills/naming-directories/` | Concise lowercase hyphenated directory, hierarchy, and `.tmp` naming rules |
| `.opencode/skills/socratic-tutor/` | Opt-in Socratic tutoring loop ("teach/tutor/quiz/drill me") adapted from Jane Street's `agent_skills` |

Domain-specific MCP servers, plugins, and skills stay out of this base harness so unrelated workspaces pay zero extra context tokens.

## Install or Update

Requires OpenCode V2 (`2.0.4+`), Git, and Python 3.10+ (or `uv`).

```sh
git clone https://github.com/patrickreidy6/opencode-defaults.git
cd opencode-defaults
```

**Windows (PowerShell):**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1 -WhatIf
powershell -NoProfile -ExecutionPolicy Bypass -File ./install.ps1
```

On Windows, keep the standalone OpenCode CLI binary at `$HOME\.opencode\bin\opencode.exe` on your User `Path` (with Git for Windows installed) rather than unpacking `opencode.exe` into a custom folder such as `%LOCALAPPDATA%\Programs\OpenCodeCLI`. OpenCode only detects standalone `curl` installs at `~/.opencode/bin/opencode.exe`; custom paths skip CLI/TUI updates with `installation method not found`. After an OpenCode CLI upgrade, run `opencode service restart` from a new terminal so the background server switches to the updated binary.

**Linux / Halo Docker Workspaces (`bash` / `sh`):**
```sh
sh ./install.sh --dry-run
sh ./install.sh
```

In `ops-infra` containers where `/home/builder` is persistent and `/home/builder/.local/bin` is on `PATH`, install OpenCode V2 and link its binary once per workspace:
```sh
curl -fsSL https://opencode.ai/v2/install | bash
ln -sf "$HOME/.opencode/bin/opencode" "$HOME/.local/bin/opencode"
sh ./install.sh
```
(`opencode upgrade` resolves symlinks via `realPath`, so `~/.local/bin/opencode -> ~/.opencode/bin/opencode` preserves automatic `curl` updates while working in non-login SSH shells.)

### Installer Behavior
- Resolves destination to `--destination`, else `$XDG_CONFIG_HOME/opencode` (when absolute), else `~/.config/opencode`.
- Deep-merges `opencode.json` objects and **unions root arrays** (`plugins`, `instructions`, `skills`). Previous repository-managed Superpowers Git references are replaced by the selected pin; other plugin entries and machine-local auth settings are preserved.
- When `AGENTS.local.md` does not already exist, preserves any pre-existing custom `AGENTS.md` as `AGENTS.local.md` (loaded via `~/.config/opencode/AGENTS.local.md` in standard `~/.config/opencode` setups, and skipped silently when absent).
- Backs up overwritten files under `<destination>/backups/harness-<timestamp>/` and leaves unrelated files (`service.json`, `cli.json`, local `commands/`) untouched.

### Superpowers Version and Cache

[`global/opencode.json`](global/opencode.json) pins Superpowers to commit `22f0b463e7a5e579904dd6211a520321035526f7` (package version **7.0.2**). Fresh installations use that same source revision. Rerunning the installer replaces earlier `superpowers@git+https://github.com/obra/superpowers.git` string entries, including entries with a `#revision`, so old references do not accumulate.

The installer copies your settings, global instructions, and personal skills into the OpenCode configuration directory. OpenCode downloads Superpowers and its bundled skills into its own package cache (`~/.cache/opencode/npm/` on the standard setup). Let each machine build its cache; the Git reference in this repository is the portable dependency declaration. OpenCode installs missing packages in the background and reuses downloaded copies.

To upgrade Superpowers deliberately:

1. Select and review an upstream revision, recording its full Git commit hash.
2. Update the `#commit` in `global/opencode.json`, the `PINNED_SUPERPOWERS` fixture in `tests/test_install.py`, and the version note above.
3. Run the [installer tests](#validation), then preview and apply the platform-specific installer using the commands under [Install or Update](#install-or-update).
4. Run `opencode plugin list` and confirm Superpowers loads from the selected revision. Commit the tested defaults, pull them on other machines, and rerun the installer there.

OpenCode's `opencode plugin update` skips full-commit pins. Moving the pin in this repository is what selects the next Superpowers revision; see [OpenCode's plugin documentation](https://opencode.ai/v2/docs/plugins).

## Starting a New Project Repo With Extra MCPs or Plugins

Once `opencode-defaults` is installed globally on a machine or container, every repo automatically inherits `superpowers`, `context7`, your model defaults, and global skills. You do **not** copy files from `opencode-defaults` into new repositories.

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

For repository settings on GitHub, keep **Pull requests** and **Allow squash merging** enabled (for optional review of larger or agent-generated changes with single-commit history) and turn off **Projects**, **Allow merge commits**, and **Allow rebase merging** unless a project specifically needs them.

## Validation

Run the installer unit tests:
```sh
uv run --no-project python -m unittest discover -s tests -v
```

Validate each skill against the [Agent Skills specification](https://agentskills.io/specification):
```sh
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/writer
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/frontend-design
uv run --no-project --with "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref" python -m skills_ref.cli validate .opencode/skills/data-preferences
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
