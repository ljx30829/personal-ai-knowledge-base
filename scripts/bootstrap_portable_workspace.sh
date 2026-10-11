#!/usr/bin/env sh
set -eu

ROOT=${1:-"$HOME/AIWorkspace"}
VAULT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PROJECTS_ROOT="$ROOT/projects"

if [ "${EXECUTE:-0}" != "1" ]; then
  printf '%s\n' "DRY_RUN root=$ROOT"
  printf '%s\n' "Set EXECUTE=1 to clone the private project repositories, restore skills, and run tests."
  exit 0
fi

command -v git >/dev/null 2>&1 || { printf '%s\n' "Git is required" >&2; exit 2; }
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys' >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1 && python -c 'import sys' >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  printf '%s\n' "Python 3.11 or newer is required" >&2
  exit 2
fi
mkdir -p "$PROJECTS_ROOT"

if [ ! -d "$PROJECTS_ROOT/account-knowledge-distiller/.git" ]; then
  git clone https://github.com/ljx30829/account-knowledge-distiller.git "$PROJECTS_ROOT/account-knowledge-distiller"
fi
if [ ! -d "$PROJECTS_ROOT/independent-site-research-vault/.git" ]; then
  git clone https://github.com/ljx30829/independent-site-research-vault.git "$PROJECTS_ROOT/independent-site-research-vault"
fi

"$PYTHON_BIN" "$VAULT_ROOT/scripts/audit_portable_skills.py" \
  --bundle "$VAULT_ROOT/portable-skills"

"$PYTHON_BIN" "$VAULT_ROOT/scripts/install_portable_skills.py" \
  --bundle "$VAULT_ROOT/portable-skills" \
  --target-codex-home "${CODEX_HOME:-$HOME/.codex}" \
  --include-plugin-cache \
  --execute

sh "$PROJECTS_ROOT/account-knowledge-distiller/scripts/setup.sh"
printf '%s\n' "PASS_LOCAL_RESTORE"
