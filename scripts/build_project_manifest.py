from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.build_project_inventory import EXCLUDED_TERMS
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from build_project_inventory import EXCLUDED_TERMS


MAX_MEDIA_BYTES = 50 * 1024 * 1024
SECRET_NAMES = re.compile(r"(?i)^(\.env(?:\..*)?|.*(?:secret|token|password|credential|cookie|private[-_]?key).*)$")
SAFE_ENV_NAMES = {".env.example", ".env.sample", ".env.template"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".cache", "cache", "logs", "tmp", "temp", "browser", "profiles"}
DATABASE_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".mdb", ".bak"}
MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".mov", ".avi", ".zip", ".7z", ".rar"}


def should_exclude(relative_path: Path, size: int | None = None) -> tuple[bool, str | None]:
    parts = relative_path.parts
    lowered = "/".join(parts).lower()
    if any(term in lowered for term in EXCLUDED_TERMS):
        return True, "excluded-domain"
    if any(part.lower() in SKIP_DIRS for part in parts[:-1]):
        return True, "generated-or-cache-dir"
    if SECRET_NAMES.fullmatch(relative_path.name) and relative_path.name.lower() not in SAFE_ENV_NAMES:
        return True, "secret-name"
    if relative_path.suffix.lower() in DATABASE_SUFFIXES:
        return True, "database"
    if size is not None and relative_path.suffix.lower() in MEDIA_SUFFIXES and size > MAX_MEDIA_BYTES:
        return True, "large-media"
    return False, None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path, output: Path) -> dict[str, Any]:
    root = Path(root).expanduser().resolve()
    output = Path(output).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"project root is not a directory: {root}")
    if any(term in str(root).lower() for term in EXCLUDED_TERMS):
        raise ValueError("project root is in an excluded domain")
    try:
        output.relative_to(root)
    except ValueError:
        pass
    else:
        raise ValueError("manifest output must be outside the project root")
    output.parent.mkdir(parents=True, exist_ok=True)
    files: list[dict[str, Any]] = []
    excluded = Counter()
    for current, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        directories[:] = [
            name for name in directories
            if name.lower() not in SKIP_DIRS and not (current_path / name).is_symlink()
        ]
        for filename in filenames:
            path = current_path / filename
            if path.is_symlink():
                excluded["symlink"] += 1
                continue
            relative = path.relative_to(root)
            try:
                size = path.stat().st_size
            except OSError:
                excluded["unreadable"] += 1
                continue
            skip, reason = should_exclude(relative, size)
            if skip:
                excluded[reason or "policy"] += 1
                continue
            files.append({"path": relative.as_posix(), "bytes": size, "sha256": _sha256(path)})
    files.sort(key=lambda item: item["path"].lower())
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root_name": root.name,
        "included_file_count": len(files),
        "included_bytes": sum(item["bytes"] for item in files),
        "excluded_counts": dict(sorted(excluded.items())),
        "files": files,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a safe SHA-256 project file manifest.")
    parser.add_argument("--project-path", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    payload = build_manifest(args.project_path, args.output)
    print(json.dumps({"included_file_count": payload["included_file_count"], "included_bytes": payload["included_bytes"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
