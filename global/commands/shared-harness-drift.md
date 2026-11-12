---
description: Show published updates and this workspace's harness differences
agent: build
subagent: false
model: openai/gpt-6.1-sol#low
---

Run the shared harness drift report for this workspace. Arguments: $ARGUMENTS

This command accepts no arguments. If any were supplied, explain the usage and stop.
Use one shell call to run the Python program below with `uv run --no-project python`
or an available Python 3.10+ interpreter. Use PowerShell's here-string piped to
Python on Windows, or a quoted heredoc on POSIX. Keep the current working directory
so the report includes the active project's harness files.

```python
import os
from pathlib import Path
import subprocess
import sys

source = Path.home() / '.local/share/opencode-defaults'
os.environ['GIT_TERMINAL_PROMPT'] = '0'
os.environ['GCM_INTERACTIVE'] = 'never'
if not source.exists():
    source.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', '-c', 'credential.helper=', '-c', 'core.askPass=',
                    'clone', '--quiet', '--branch', 'main',
                    'https://github.com/patrickreidy6/opencode-defaults.git', str(source)], check=True)
raise SystemExit(subprocess.run([sys.executable, str(source / 'shared_harness.py'),
                                'drift', '--project', str(Path.cwd())]).returncode)
```

Display the report concisely, retaining its Upstream, Workspace, Local, Project and
Runtime distinctions. Differences are expected information, not a request to fix
anything. The command refreshes its source cache but does not change the installed
harness or project. On failure report the error; do not attempt an installation,
credential setup, reset, push, review, or another command. Do not inspect secrets
or reinterpret the report through a planning workflow.
