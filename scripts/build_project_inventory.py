from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


EXCLUDED_TERMS = (
    "armor" + "hue",
    "automotive" + "-film",
    "automotive" + "_film",
    "car" + "-film",
    "car" + "_film",
    "candy" + ".ai",
    "candy" + "-ai",
    "adult",
)
EVIDENCE_FILES = {
    "AGENTS.md",
    "README.md",
    "TASK_STATE.md",
    "PROJECT_STATE.md",
    "IMAGE_WORKFLOW.md",
    "PROMOTION_WORKFLOW.md",
}
STATE_FILES = {"TASK_STATE.md", "PROJECT_STATE.md"}
ENTRYPOINT_NAMES = {
    "main.py",
    "app.py",
    "server.py",
    "manage.py",
    "index.js",
    "index.ts",
    "main.js",
    "main.ts",
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "Package.swift",
}
SECRET_NAME_RE = re.compile(
    r"(?i)(^|[._-])(\.env(?:\..*)?|.*(?:secret|token|password|credential|cookie|private[-_]?key).*)$"
)
SAFE_ENV_NAMES = {".env.example", ".env.sample", ".env.template"}
SKIP_DIR_NAMES = {".git", ".venv", "venv", "node_modules", "__pycache__", ".cache", ".worktrees"}
LARGE_FILE_BYTES = 50 * 1024 * 1024


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _path_has_excluded_term(path: Path) -> str | None:
    lowered = "/".join(path.parts).lower()
    for term in EXCLUDED_TERMS:
        if term in lowered:
            return term
    return None


def _iter_files(root: Path) -> Iterable[tuple[Path, os.stat_result]]:
    for current, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        directories[:] = [
            name
            for name in directories
            if name.lower() not in SKIP_DIR_NAMES and not (Path(current) / name).is_symlink()
        ]
        for filename in filenames:
            file_path = Path(current) / filename
            try:
                stat = file_path.stat()
            except OSError:
                continue
            if file_path.is_symlink():
                continue
            yield file_path, stat


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def scan_project(path: Path) -> dict[str, Any]:
    root = Path(path).expanduser()
    exclusion = _path_has_excluded_term(root)
    base: dict[str, Any] = {
        "name": root.name,
        "source_path": str(root.resolve()),
        "status": "MISSING" if not root.exists() else "PRESENT",
        "exclusion_reason": exclusion,
        "git": {"is_repo": (root / ".git").exists()},
        "entrypoints": [],
        "state_files": [],
        "evidence_files": [],
        "dependency_files": [],
        "secret_candidates": [],
        "large_file_summary": {"count": 0, "bytes": 0},
    }
    if not root.is_dir():
        return base
    if exclusion:
        base["status"] = "EXCLUDED"
    entrypoints: list[str] = []
    states: list[str] = []
    evidence: list[str] = []
    secrets: list[str] = []
    large_count = 0
    large_bytes = 0
    for file_path, stat in _iter_files(root):
        relative = _relative(root, file_path)
        filename = file_path.name
        if filename in EVIDENCE_FILES:
            evidence.append(relative)
        if filename in STATE_FILES:
            states.append(relative)
        if filename in ENTRYPOINT_NAMES or (Path(relative).parts[0] in {"src", "app"} and file_path.suffix in {".py", ".js", ".ts", ".tsx"}):
            if len(entrypoints) < 200:
                entrypoints.append(relative)
        if SECRET_NAME_RE.search(filename) and filename.lower() not in SAFE_ENV_NAMES:
            secrets.append(relative)
        if stat.st_size >= LARGE_FILE_BYTES:
            large_count += 1
            large_bytes += stat.st_size
    base["entrypoints"] = sorted(entrypoints)
    base["state_files"] = sorted(states)
    base["evidence_files"] = sorted(evidence)
    base["dependency_files"] = sorted(
        item["path"] for item in _dependency_file_records(root)
    )
    base["secret_candidates"] = sorted(secrets)
    base["large_file_summary"] = {"count": large_count, "bytes": large_bytes}
    if base["status"] == "PRESENT" and (entrypoints or states or evidence):
        base["status"] = "ACTIVE"
    return base


def _dependency_file_records(root: Path) -> list[dict[str, Any]]:
    names = {
        "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb",
        "pyproject.toml", "requirements.txt", "requirements-dev.txt", "uv.lock", "poetry.lock",
        "Pipfile", "Pipfile.lock", "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
        "compose.yml", "compose.yaml", "Package.swift", "Package.resolved", "playwright.config.ts",
        "playwright.config.js", ".nvmrc", ".node-version", ".python-version",
    }
    records: list[dict[str, Any]] = []
    for file_path, stat in _iter_files(root):
        if file_path.name in names or file_path.name.startswith("requirements-"):
            records.append({"path": _relative(root, file_path), "bytes": stat.st_size})
    return sorted(records, key=lambda item: item["path"].lower())


def write_inventory(paths: list[Path], output: Path) -> dict[str, Any]:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    scanned = [scan_project(Path(path)) for path in paths]
    excluded = [item for item in scanned if item["status"] == "EXCLUDED"]
    projects = [item for item in scanned if item["status"] != "EXCLUDED"]
    payload = {
        "schema_version": 1,
        "generated_at": _now(),
        "project_count": len(projects),
        "excluded_project_count": len(excluded),
        "projects": projects,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


DEFAULT_PROJECTS = [
    Path(r"C:\Users\26014\Documents\独立站"),
    Path(r"C:\Users\26014\Documents\自媒体运营"),
    Path(r"C:\Users\26014\Documents\中转站"),
    Path(r"C:\Users\26014\Documents\节点"),
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build metadata-only project migration inventory.")
    parser.add_argument("--project", action="append", type=Path, dest="projects", help="Project path; repeatable.")
    parser.add_argument("--output", type=Path, default=Path("sources/inventory/project-migration.json"))
    args = parser.parse_args(argv)
    payload = write_inventory(args.projects or DEFAULT_PROJECTS, args.output)
    counts: dict[str, int] = {}
    for item in payload["projects"]:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    print(json.dumps({"project_count": payload["project_count"], "statuses": counts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
