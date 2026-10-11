from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXCLUDED_PATH_TERMS = (
    "armor" + "hue",
    "automotive" + "-film",
    "automotive" + "_film",
    "car" + "-film",
    "car" + "_film",
    "candy" + ".ai",
    "candy" + "-ai",
    "adult-fiction",
    "adult_content",
)
EXCLUDED_CONTENT_RE = re.compile(
    r"(?i)\b(?:"
    + "armor" + "hue|"
    + "automotive" + r"[ -]?" + "film|"
    + "car" + r"[ -]?" + "film|"
    + "candy" + r"\." + "ai|"
    + "adult" + r"[- ]" + r"fiction)\b"
)
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret|cookie)\s*[:=]\s*[^\s`'\"<>]{8,}"
)
ALLOWED_SUFFIXES = {".md", ".txt", ".csv", ".json"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_documents(root: Path) -> tuple[list[Path], dict[str, int]]:
    root = Path(root).resolve()
    selected: list[Path] = []
    excluded: dict[str, int] = {}

    def reject(reason: str) -> None:
        excluded[reason] = excluded.get(reason, 0) + 1

    for path in sorted(root.rglob("*"), key=lambda item: str(item).lower()):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root)
        if any(part.startswith(".") for part in relative.parts):
            reject("hidden-or-vcs")
            continue
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            reject("unsupported-file-type")
            continue
        relative_text = relative.as_posix().lower()
        if any(term in relative_text for term in EXCLUDED_PATH_TERMS):
            reject("excluded-domain")
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError):
            reject("unreadable-text")
            continue
        if EXCLUDED_CONTENT_RE.search(text):
            reject("excluded-content")
            continue
        if SECRET_ASSIGNMENT_RE.search(text):
            reject("possible-secret")
            continue
        selected.append(path)
    return selected, excluded


def build_document_export(root: Path, output: Path, execute: bool = False) -> dict[str, Any]:
    root = Path(root).expanduser().resolve()
    output = Path(output).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"workspace root is not a directory: {root}")
    if any(term in str(root).lower() for term in EXCLUDED_PATH_TERMS):
        raise ValueError("workspace root is in an excluded domain")
    try:
        output.relative_to(root)
    except ValueError:
        pass
    else:
        raise ValueError("export output must be outside the workspace root")
    if output.exists():
        raise FileExistsError(f"export output already exists: {output}")
    selected, excluded = collect_documents(root)
    files = [
        {
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in selected
    ]
    payload: dict[str, Any] = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace_name": root.name,
        "included_file_count": len(files),
        "included_bytes": sum(item["bytes"] for item in files),
        "excluded_counts": dict(sorted(excluded.items())),
        "files": files,
        "execution": "EXECUTED" if execute else "DRY_RUN",
    }
    if not execute:
        return payload
    output.mkdir(parents=True)
    for source in selected:
        target = output / source.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    (output / "DOCUMENT_EXPORT_MANIFEST.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "README.md").write_text(
        f"# {root.name} Portable Research Workspace\n\n"
        "This reviewed document export contains research and dated state only. It has no deployable application, account session, platform login, private contact list, or executable dependency.\n\n"
        "Start with `TASK_STATE.md`. Revalidate dated market/platform claims before making decisions. External outreach, purchases, publishing, and account actions still require current authorization.\n",
        encoding="utf-8",
    )
    (output / ".gitignore").write_text(
        ".env*\n!.env.example\n*.log\n.cache/\noutput/\n", encoding="utf-8"
    )
    (output / ".gitattributes").write_text("* text=auto eol=lf\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export a reviewed document-only workspace.")
    parser.add_argument("--workspace-path", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    payload = build_document_export(args.workspace_path, args.output, execute=args.execute)
    print(json.dumps({
        "workspace_name": payload["workspace_name"],
        "execution": payload["execution"],
        "included_file_count": payload["included_file_count"],
        "included_bytes": payload["included_bytes"],
        "excluded_counts": payload["excluded_counts"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
