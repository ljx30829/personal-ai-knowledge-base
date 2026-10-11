from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from scripts.build_project_inventory import EXCLUDED_TERMS, SAFE_ENV_NAMES, _iter_files, _path_has_excluded_term, _relative
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from build_project_inventory import EXCLUDED_TERMS, SAFE_ENV_NAMES, _iter_files, _path_has_excluded_term, _relative


DEPENDENCY_NAMES = {
    "package.json": "node",
    "package-lock.json": "node",
    "pnpm-lock.yaml": "node",
    "yarn.lock": "node",
    "bun.lockb": "node",
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "uv.lock": "python",
    "poetry.lock": "python",
    "Pipfile": "python",
    "Pipfile.lock": "python",
    "Dockerfile": "docker",
    "docker-compose.yml": "docker",
    "docker-compose.yaml": "docker",
    "compose.yml": "docker",
    "compose.yaml": "docker",
    "Package.swift": "swift",
    "Package.resolved": "swift",
}
VERSION_RE = re.compile(r"^[A-Za-z0-9_.+:-]{1,80}$")
SENSITIVE_FILE_TERMS = ("secret", "token", "password", "cookie", "credential", "session", "private-key", "private_key")
SENSITIVE_DIR_NAMES = {".aws", ".ssh", "browser-profile", "browser-profiles", "cookies", "credentials", "secrets", "sessions"}


def inspect_project(path: Path) -> dict[str, Any]:
    root = Path(path).expanduser()
    exclusion = _path_has_excluded_term(root)
    result: dict[str, Any] = {
        "schema_version": 1,
        "project_path": str(root.resolve()),
        "status": "MISSING" if not root.exists() else ("EXCLUDED" if exclusion else "PASS"),
        "exclusion_reason": exclusion,
        "dependency_files": [],
        "project_types": [],
        "package_manager": None,
        "runtime_hints": [],
        "secret_candidates": [],
    }
    if not root.is_dir() or exclusion:
        return result
    records: list[dict[str, Any]] = []
    types: set[str] = set()
    secret_candidates: list[str] = []
    package_manager = None
    for file_path, stat in _iter_files(root):
        name = file_path.name
        relative = _relative(root, file_path)
        category = DEPENDENCY_NAMES.get(name)
        if category is None and name.startswith("requirements-") and name.endswith(".txt"):
            category = "python"
        if category:
            records.append({"path": relative, "bytes": stat.st_size, "kind": category})
            types.add(category)
        if name == "pnpm-lock.yaml":
            package_manager = "pnpm"
        elif name == "package-lock.json" and package_manager is None:
            package_manager = "npm"
        elif name == "yarn.lock" and package_manager is None:
            package_manager = "yarn"
        elif name == "bun.lockb" and package_manager is None:
            package_manager = "bun"
        if name in {".nvmrc", ".node-version", ".python-version"}:
            try:
                value = file_path.read_text(encoding="utf-8", errors="replace").strip().splitlines()[0]
            except (OSError, IndexError):
                value = ""
            if value and VERSION_RE.fullmatch(value):
                result["runtime_hints"].append({"file": relative, "value": value})
        lower_name = name.lower()
        parent_names = {part.lower() for part in file_path.relative_to(root).parts[:-1]}
        sensitive_name = lower_name.startswith(".env") or any(
            term in lower_name for term in SENSITIVE_FILE_TERMS
        )
        if lower_name not in SAFE_ENV_NAMES and (
            sensitive_name or bool(parent_names & SENSITIVE_DIR_NAMES)
        ):
            secret_candidates.append(relative)
    result["dependency_files"] = sorted(records, key=lambda item: item["path"].lower())
    result["project_types"] = sorted(types)
    result["package_manager"] = package_manager
    result["runtime_hints"] = sorted(result["runtime_hints"], key=lambda item: item["file"].lower())
    result["secret_candidates"] = sorted(set(secret_candidates))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect project dependency metadata without installing anything.")
    parser.add_argument("--project-path", required=True, type=Path)
    args = parser.parse_args(argv)
    result = inspect_project(args.project_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" and not result["secret_candidates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
