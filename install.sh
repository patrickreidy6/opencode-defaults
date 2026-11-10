#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if command -v uv >/dev/null 2>&1; then
    exec uv run --no-project python "$SCRIPT_DIR/install.py" "$@"
fi

for cmd in python3 python; do
    if command -v "$cmd" >/dev/null 2>&1 && "$cmd" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
        exec "$cmd" "$SCRIPT_DIR/install.py" "$@"
    fi
done

echo "Error: Python 3.10+ (or uv) is required to run install.py." >&2
exit 1
