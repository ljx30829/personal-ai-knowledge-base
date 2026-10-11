#!/usr/bin/env sh
set -eu

if [ "$#" -ne 2 ] || [ "$1" != "--project-path" ]; then
  printf '%s\n' '{"schema_version":1,"status":"FAIL","reason":"usage: doctor_project.sh --project-path PATH"}'
  exit 2
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys' >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1 && python -c 'import sys' >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  printf '%s\n' '{"schema_version":1,"status":"FAIL","reason":"python-unavailable"}'
  exit 2
fi
exec "$PYTHON_BIN" "$SCRIPT_DIR/check_project_dependencies.py" --project-path "$2"
