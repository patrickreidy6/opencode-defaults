---
name: shared-harness-update
description: Apply the published OpenCode defaults and CLI pin for the current user when they request a shared harness update from a Codex workspace.
---

# Update the shared OpenCode harness

Run the existing updater from the current project, under the account running Codex. It fetches public `main`, backs up changed shared files, aligns OpenCode to the exact published version, and reloads its configuration. One invocation covers every project sharing that user's OpenCode installation.

In Windows PowerShell, run

```powershell
uv run --no-project python "$HOME/.local/share/opencode-defaults/shared_harness.py" update --project .
```

On Linux or macOS, run

```sh
python3 "$HOME/.local/share/opencode-defaults/shared_harness.py" update --project .
```

Use another available Python 3.10+ interpreter if needed. Report the published revision and result, including any backup path or service-restart instruction the updater prints. If it exits with an error, identify the failed step and any changes it already applied.
