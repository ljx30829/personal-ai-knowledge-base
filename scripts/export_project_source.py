from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.build_project_inventory import EXCLUDED_TERMS
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from build_project_inventory import EXCLUDED_TERMS


DEFAULT_ROOT_FILES = {
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "uv.lock",
    "poetry.lock",
    "Dockerfile",
    "compose.yml",
    "compose.yaml",
    "docker-compose.yml",
    "docker-compose.yaml",
}
DEFAULT_SOURCE_DIRS = {"src", "tests", "examples"}
SKIP_DIRS = {".git", ".worktrees", "__pycache__", ".pytest_cache", ".mypy_cache", ".venv", "venv", "node_modules"}
SECRET_PARTS = (".env", "secret", "token", "password", "credential", "cookie", "private_key")
TEXT_SUFFIXES = {".md", ".py", ".json", ".toml", ".txt", ".yaml", ".yml", ".ps1", ".sh", ".js", ".ts"}
MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".mov", ".avi", ".wav", ".mp3", ".zip"}
SANITIZE_REPLACEMENTS = (
    ("Armor" + "Hue", "ExcludedBrand"),
    ("armor" + "hue", "excluded-brand"),
    ("automotive" + " film", "unrelated factory product"),
    ("Automotive" + " Film", "Unrelated Factory Product"),
    ("car" + " film", "factory product"),
    ("汽" + "车" + "膜", "示例产品"),
    ("车" + "膜", "示例产品"),
    ("%E6%B1%BD%E8%BD%A6%E8%86%9C", "%E7%A4%BA%E4%BE%8B%E4%BA%A7%E5%93%81"),
    ("Candy" + ".ai", "ExcludedService"),
    ("candy" + ".ai", "excluded-service"),
)
PROTECTIVE_IGNORE = "\n".join(
    ["accounts/", "assets/", "output/", "__pycache__/", ".pytest_cache/", ".venv/", ".env*", "!.env.example"]
)


def _has_excluded_term(value: str) -> bool:
    lowered = value.lower()
    return any(term in lowered for term in EXCLUDED_TERMS)


def _looks_secret(relative: Path) -> bool:
    name = relative.name.lower()
    if name in {".env.example", ".env.sample", ".env.template"}:
        return False
    return any(part in name for part in SECRET_PARTS)


def _text_is_safe(path: Path) -> tuple[bool, str | None]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return True, None
    try:
        text = path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError):
        return False, "unreadable-text"
    if _has_excluded_term(text):
        return False, "excluded-content"
    lowered = text.lower()
    assignment_markers = ("api_key=", "token=", "password=", "secret=", "cookie=")
    if any(marker in lowered for marker in assignment_markers):
        return False, "secret-assignment"
    return True, None


def collect_files(root: Path) -> tuple[list[Path], dict[str, int]]:
    root = Path(root).resolve()
    excluded: dict[str, int] = {}
    selected: list[Path] = []

    def reject(reason: str) -> None:
        excluded[reason] = excluded.get(reason, 0) + 1

    for name in DEFAULT_ROOT_FILES:
        candidate = root / name
        if not candidate.is_file():
            continue
        relative = Path(name)
        if _looks_secret(relative):
            reject("secret-name")
            continue
        safe, reason = _text_is_safe(candidate)
        if not safe:
            reject(reason or "policy")
            continue
        selected.append(candidate)

    for directory in DEFAULT_SOURCE_DIRS:
        source_root = root / directory
        if not source_root.is_dir():
            continue
        for current, directories, filenames in os.walk(source_root, topdown=True, followlinks=False):
            current_path = Path(current)
            directories[:] = [
                name for name in directories
                if name.lower() not in SKIP_DIRS and not (current_path / name).is_symlink()
            ]
            for filename in filenames:
                path = current_path / filename
                if path.is_symlink():
                    reject("symlink")
                    continue
                relative = path.relative_to(root)
                if _has_excluded_term(relative.as_posix()):
                    reject("excluded-domain")
                    continue
                if _looks_secret(relative):
                    reject("secret-name")
                    continue
                if path.suffix.lower() in MEDIA_SUFFIXES:
                    reject("media")
                    continue
                safe, reason = _text_is_safe(path)
                if not safe:
                    reject(reason or "policy")
                    continue
                selected.append(path)
    return sorted(set(selected), key=lambda item: item.relative_to(root).as_posix().lower()), excluded


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _export_bytes(path: Path) -> bytes:
    if path.name == ".gitignore":
        text = path.read_text(encoding="utf-8", errors="strict")
        return (text.rstrip() + "\n" + PROTECTIVE_IGNORE + "\n").encode("utf-8")
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return path.read_bytes()
    text = path.read_text(encoding="utf-8", errors="strict")
    for source, replacement in SANITIZE_REPLACEMENTS:
        text = text.replace(source, replacement)
    return text.encode("utf-8")


def build_export(root: Path, output: Path, execute: bool = False) -> dict[str, Any]:
    root = Path(root).expanduser().resolve()
    output = Path(output).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"project root is not a directory: {root}")
    if _has_excluded_term(str(root)):
        raise ValueError("project root is in an excluded domain")
    try:
        output.relative_to(root)
    except ValueError:
        pass
    else:
        raise ValueError("export output must be outside the project root")
    if output.exists():
        raise FileExistsError(f"export output already exists: {output}")
    selected, excluded = collect_files(root)
    exported_payloads = [(path, _export_bytes(path)) for path in selected]
    files = [
        {
            "path": path.relative_to(root).as_posix(),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        for path, data in exported_payloads
    ]
    payload: dict[str, Any] = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_name": root.name,
        "source_dirs": sorted(DEFAULT_SOURCE_DIRS),
        "included_file_count": len(files),
        "included_bytes": sum(item["bytes"] for item in files),
        "excluded_counts": dict(sorted(excluded.items())),
        "files": files,
        "execution": "EXECUTED" if execute else "DRY_RUN",
    }
    if not execute:
        return payload
    output.mkdir(parents=True)
    for path, data in exported_payloads:
        target = output / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (output / "PROJECT_EXPORT_MANIFEST.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "PORTABLE_PROJECT_README.md").write_text(
        f"# {root.name} Portable Source\n\n"
        "This source-only export intentionally omits local account data, generated output, media, caches, credentials, and machine-specific tools.\n\n"
        "## Restore\n\n"
        "1. Install Python 3.11 or newer.\n"
        "2. Run `scripts/setup.ps1` on Windows or `sh scripts/setup.sh` on POSIX systems; setup verifies the manifest before testing.\n"
        "3. Install optional local tools such as FFmpeg or Whisper separately only after estimating size and confirming the target drive.\n"
        "4. Recreate account data from public or user-authorized inputs; it is not included here.\n",
        encoding="utf-8",
    )
    setup_dir = output / "scripts"
    setup_dir.mkdir(parents=True, exist_ok=True)
    (setup_dir / "setup.ps1").write_text(
        "param([string]$Python = 'python')\n"
        "$ErrorActionPreference = 'Stop'\n"
        "& $Python --version\n"
        "if ($LASTEXITCODE -ne 0) { throw 'Python 3.11+ is required' }\n"
        "& $Python (Join-Path $PSScriptRoot 'verify_manifest.py')\n"
        "if ($LASTEXITCODE -ne 0) { throw 'Manifest verification failed' }\n"
        "$env:PYTHONPATH = Join-Path (Split-Path -Parent $PSScriptRoot) 'src'\n"
        "& $Python -m unittest discover -s (Join-Path (Split-Path -Parent $PSScriptRoot) 'tests') -p 'test_*.py'\n"
        "exit $LASTEXITCODE\n",
        encoding="utf-8",
    )
    (setup_dir / "setup.sh").write_text(
        "#!/usr/bin/env sh\n"
        "set -eu\n"
        "PYTHON=${PYTHON:-python3}\n"
        "$PYTHON --version\n"
        "\"$PYTHON\" \"$(dirname -- \"$0\")/verify_manifest.py\"\n"
        "PYTHONPATH=\"$(CDPATH= cd -- \"$(dirname -- \"$0\")/../src\" && pwd)\" \\\n"
        "  \"$PYTHON\" -m unittest discover -s \"$(CDPATH= cd -- \"$(dirname -- \"$0\")/../tests\" && pwd)\" -p 'test_*.py'\n",
        encoding="utf-8",
    )
    (output / "DEPENDENCY_REPORT.json").write_text(
        json.dumps(
            {
                "python": ">=3.11",
                "python_dependencies": [],
                "optional_external_tools": ["FFmpeg", "whisper.cpp"],
                "installation_policy": "optional tools require separate size/location review",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (output / "requirements.txt").write_text(
        "# Core project uses only the Python standard library.\n",
        encoding="utf-8",
    )
    if not (output / ".gitignore").is_file():
        (output / ".gitignore").write_text(PROTECTIVE_IGNORE + "\n", encoding="utf-8")
    (output / ".gitattributes").write_text("* text=auto eol=lf\n", encoding="utf-8")
    (setup_dir / "verify_manifest.py").write_text(
        "import hashlib\n"
        "import json\n"
        "from pathlib import Path\n\n"
        "root = Path(__file__).resolve().parent.parent\n"
        "manifest = json.loads((root / 'PROJECT_EXPORT_MANIFEST.json').read_text(encoding='utf-8'))\n"
        "failures = []\n"
        "for item in manifest['files']:\n"
        "    path = root / item['path']\n"
        "    if not path.is_file():\n"
        "        failures.append(f\"missing:{item['path']}\")\n"
        "        continue\n"
        "    actual = hashlib.sha256(path.read_bytes()).hexdigest()\n"
        "    if actual != item['sha256']:\n"
        "        failures.append(f\"hash:{item['path']}\")\n"
        "if failures:\n"
        "    print(json.dumps({'status': 'FAIL', 'failures': failures}, ensure_ascii=False))\n"
        "    raise SystemExit(1)\n"
        "print(json.dumps({'status': 'PASS', 'verified_files': len(manifest['files'])}))\n",
        encoding="utf-8",
    )
    (setup_dir / "doctor.ps1").write_text(
        "param([string]$Python = 'python')\n"
        "$ErrorActionPreference = 'Stop'\n"
        "$pythonInfo = & $Python --version 2>&1\n"
        "$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue\n"
        "$whisper = Get-Command whisper-cli -ErrorAction SilentlyContinue\n"
        "[ordered]@{\n"
        "  status = if ($LASTEXITCODE -eq 0) { 'PASS_CORE' } else { 'FAIL_PYTHON' }\n"
        "  python = [string]$pythonInfo\n"
        "  core_dependencies = @()\n"
        "  ffmpeg_optional = [bool]$ffmpeg\n"
        "  whisper_optional = [bool]$whisper\n"
        "} | ConvertTo-Json\n",
        encoding="utf-8",
    )
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export source-only project files after safety filtering.")
    parser.add_argument("--project-path", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--execute", action="store_true", help="Copy the reviewed file set; default is dry-run.")
    args = parser.parse_args(argv)
    payload = build_export(args.project_path, args.output, execute=args.execute)
    print(json.dumps({
        "project_name": payload["project_name"],
        "execution": payload["execution"],
        "included_file_count": payload["included_file_count"],
        "included_bytes": payload["included_bytes"],
        "excluded_counts": payload["excluded_counts"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
