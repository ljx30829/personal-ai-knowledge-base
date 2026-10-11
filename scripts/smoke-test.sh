#!/usr/bin/env sh
set -eu

if [ "$#" -lt 2 ] || [ "$1" != "--project-path" ]; then
  printf '%s\n' '{"schema_version":1,"status":"FAIL","reason":"usage: smoke-test.sh --project-path PATH [--command COMMAND]"}'
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
if [ "$#" -eq 2 ]; then
  exec "$PYTHON_BIN" "$SCRIPT_DIR/run_project_smoke_test.py" --project-path "$2"
fi
if [ "$#" -eq 4 ] && [ "$3" = "--command" ]; then
  exec "$PYTHON_BIN" "$SCRIPT_DIR/run_project_smoke_test.py" --project-path "$2" --command "$4"
fi
printf '%s\n' '{"schema_version":1,"status":"FAIL","reason":"usage: smoke-test.sh --project-path PATH [--command COMMAND]"}'
exit 2
