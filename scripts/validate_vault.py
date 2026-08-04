from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


REQUIRED_ROOT_FILES = (
    "README.md",
    "AGENTS.md",
    "AI_CONTEXT.md",
    "PROFILE.md",
    "IDENTITY.md",
    "KNOWLEDGE_INDEX.md",
    "TASK_STATE.md",
    "SECURITY.md",
)
TEXT_EXTENSIONS = {".md", ".json", ".toml", ".yaml", ".yml", ".txt"}
SOURCE_METADATA = {"updated", "status", "confidence", "sources", "next_review"}
GENERATED_SOURCE_DIRS = {"codex-inventory", "inventory"}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b[A-Z0-9_]*(?:API_KEY|TOKEN|PASSWORD|SECRET|COOKIE|AUTHORIZATION|PRIVATE_KEY)"
    r"\s*[:=]\s*[\"']?([^\s\"'`]+)"
)
PRIVATE_KEY_RE = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
SAFE_SECRET_VALUES = {
    "missing",
    "unset",
    "none",
    "null",
    "redacted",
    "example",
    "placeholder",
    "required",
    "not_configured",
}


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    scanned_files: int = 0


def _is_ignored(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return ".git" in relative.parts or "__pycache__" in relative.parts


def _read_text(path: Path, result: ValidationResult) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        result.errors.append(f"Non-UTF-8 text file: {path}")
        return None


def _check_source_metadata(path: Path, root: Path, text: str, result: ValidationResult) -> None:
    relative = path.relative_to(root)
    if len(relative.parts) < 2 or relative.parts[0] != "sources":
        return
    if relative.parts[1] in GENERATED_SOURCE_DIRS:
        return
    if path.suffix.lower() != ".md":
        return
    if not text.startswith("---\n"):
        result.errors.append(f"Source card missing metadata front matter: {relative}")
        return
    closing = text.find("\n---\n", 4)
    if closing == -1:
        result.errors.append(f"Source card has unclosed metadata front matter: {relative}")
        return
    keys = {
        line.split(":", 1)[0].strip()
        for line in text[4:closing].splitlines()
        if ":" in line and not line.startswith((" ", "\t", "-"))
    }
    missing = sorted(SOURCE_METADATA - keys)
    if missing:
        result.errors.append(
            f"Source card missing metadata keys {', '.join(missing)}: {relative}"
        )


def _check_links(path: Path, root: Path, text: str, result: ValidationResult) -> None:
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split()[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target_path = target.split("#", 1)[0].split("?", 1)[0]
        if not target_path:
            continue
        resolved = (path.parent / target_path).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            result.warnings.append(f"Link points outside vault: {path.relative_to(root)} -> {target}")
            continue
        if not resolved.exists():
            result.errors.append(f"Broken link: {path.relative_to(root)} -> {target}")


def _check_secrets(path: Path, root: Path, text: str, result: ValidationResult) -> None:
    relative = path.relative_to(root)
    if PRIVATE_KEY_RE.search(text):
        result.errors.append(f"Possible secret private key in {relative}")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in SECRET_ASSIGNMENT_RE.finditer(line):
            value = match.group(1).strip().rstrip(",;)")
            lowered = value.lower()
            if (
                lowered in SAFE_SECRET_VALUES
                or value.startswith(("$env:", "${", "<", "YOUR_"))
                or len(value) < 8
            ):
                continue
            result.errors.append(
                f"Possible secret assignment in {relative}:{line_number}"
            )


def validate_vault(root: Path | str) -> ValidationResult:
    root = Path(root).resolve()
    result = ValidationResult()
    for name in REQUIRED_ROOT_FILES:
        if not (root / name).is_file():
            result.errors.append(f"Missing required root file: {name}")

    for path in root.rglob("*"):
        if not path.is_file() or _is_ignored(path, root):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        result.scanned_files += 1
        text = _read_text(path, result)
        if text is None:
            continue
        _check_source_metadata(path, root, text, result)
        if path.suffix.lower() == ".md":
            _check_links(path, root, text, result)
        _check_secrets(path, root, text, result)
    return result


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    root = Path(args[0] if args else ".")
    result = validate_vault(root)
    print(
        f"scanned_files={result.scanned_files} errors={len(result.errors)} "
        f"warnings={len(result.warnings)}"
    )
    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
