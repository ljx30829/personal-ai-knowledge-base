from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path


EXCLUDED_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "temp",
    "tmp",
}
EXCLUDED_SUFFIXES = {".db", ".key", ".log", ".p12", ".pem", ".pfx", ".pyc", ".sqlite"}
SENSITIVE_NAME_PARTS = ("cookie", "credential", "private-key", "secret", "session", "token")


@dataclass(frozen=True)
class ExportFile:
    source_label: str
    source_path: Path
    relative_path: Path
    size: int


def is_link_like(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction and is_junction())


def is_excluded(path: Path, root: Path) -> tuple[bool, str]:
    relative = path.relative_to(root)
    if any(part.lower() in EXCLUDED_DIR_NAMES for part in relative.parts[:-1]):
        return True, "excluded-directory"
    lowered_name = path.name.lower()
    if lowered_name == ".env" or lowered_name.startswith(".env."):
        return True, "environment-file"
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return True, "sensitive-or-generated-suffix"
    if any(part in lowered_name for part in SENSITIVE_NAME_PARTS):
        return True, "sensitive-name"
    if is_link_like(path):
        return True, "symlink-or-junction"
    return False, ""


def collect_files(label: str, root: Path) -> tuple[list[ExportFile], dict[str, int]]:
    files: list[ExportFile] = []
    excluded: dict[str, int] = {}
    if not root.is_dir():
        return files, {"missing-root": 1}

    for current_root, directory_names, file_names in os.walk(root, topdown=True):
        current = Path(current_root)
        kept_directories: list[str] = []
        for name in sorted(directory_names):
            directory = current / name
            relative = directory.relative_to(root)
            if name.lower() in EXCLUDED_DIR_NAMES:
                excluded["excluded-directory"] = excluded.get("excluded-directory", 0) + 1
            elif is_link_like(directory):
                excluded["symlink-or-junction"] = excluded.get("symlink-or-junction", 0) + 1
            elif any(part.lower() in EXCLUDED_DIR_NAMES for part in relative.parts):
                excluded["excluded-directory"] = excluded.get("excluded-directory", 0) + 1
            else:
                kept_directories.append(name)
        directory_names[:] = kept_directories

        for name in sorted(file_names):
            path = current / name
            blocked, reason = is_excluded(path, root)
            if blocked:
                excluded[reason] = excluded.get(reason, 0) + 1
                continue
            files.append(
                ExportFile(
                    source_label=label,
                    source_path=path,
                    relative_path=path.relative_to(root),
                    size=path.stat().st_size,
                )
            )
    files.sort(key=lambda item: item.relative_path.as_posix())
    return files, excluded


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def export_bundle(
    user_skills_root: Path,
    plugin_cache_root: Path,
    output: Path,
    execute: bool = False,
) -> dict[str, object]:
    sources = (
        ("user-skills", user_skills_root),
        ("plugin-cache", plugin_cache_root),
    )
    all_files: list[ExportFile] = []
    excluded: dict[str, dict[str, int]] = {}
    for label, root in sources:
        files, skipped = collect_files(label, root)
        all_files.extend(files)
        excluded[label] = skipped

    summary: dict[str, object] = {
        "status": "DRY_RUN" if not execute else "EXPORTED",
        "file_count": len(all_files),
        "skill_file_count": sum(item.source_path.name == "SKILL.md" for item in all_files),
        "total_bytes": sum(item.size for item in all_files),
        "excluded": excluded,
    }
    if not execute:
        return summary

    output = output.resolve()
    for _, root in sources:
        root = root.resolve()
        if output == root or root in output.parents:
            raise ValueError(f"Output must not be inside a source root: {output}")
    if output.exists():
        raise FileExistsError(f"Output already exists; choose a new empty path: {output}")

    output.mkdir(parents=True)
    manifest_files: list[dict[str, object]] = []
    for item in all_files:
        destination = output / item.source_label / item.relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item.source_path, destination)
        manifest_files.append(
            {
                "source": item.source_label,
                "path": item.relative_path.as_posix(),
                "bytes": item.size,
                "sha256": sha256(destination),
            }
        )

    manifest = {**summary, "files": manifest_files}
    (output / "portable-skills-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def build_parser() -> argparse.ArgumentParser:
    user_profile = Path(os.environ.get("USERPROFILE", Path.home()))
    parser = argparse.ArgumentParser(
        description="Estimate or export a credential-filtered portable Codex skills tree."
    )
    parser.add_argument(
        "--user-skills-root",
        type=Path,
        default=user_profile / ".codex" / "skills",
    )
    parser.add_argument(
        "--plugin-cache-root",
        type=Path,
        default=user_profile / ".codex" / "plugins" / "cache",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Copy files. Without this flag the command is read-only.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = export_bundle(
        user_skills_root=args.user_skills_root,
        plugin_cache_root=args.plugin_cache_root,
        output=args.output,
        execute=args.execute,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
