from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


STANDARD_KEYS = {"allowed-tools", "description", "license", "metadata", "name"}
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s|$)")
STANDARD_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def inspect_skill(path: Path) -> dict[str, object]:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return {"path": path.as_posix(), "errors": [f"unreadable: {exc}"]}

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {"path": path.as_posix(), "errors": ["missing opening frontmatter delimiter"]}

    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return {"path": path.as_posix(), "errors": ["missing closing frontmatter delimiter"]}

    keys: dict[str, str] = {}
    for line in lines[1:closing]:
        if line[:1].isspace():
            continue
        match = TOP_LEVEL_KEY_RE.match(line)
        if match:
            key = match.group(1)
            keys[key] = line.split(":", 1)[1].strip().strip("\"'")

    errors: list[str] = []
    if not keys.get("name"):
        errors.append("missing name")
    if "description" not in keys:
        errors.append("missing description")

    extension_keys = sorted(set(keys) - STANDARD_KEYS)
    nonstandard_name = bool(keys.get("name") and not STANDARD_NAME_RE.fullmatch(keys["name"]))
    return {
        "path": path.as_posix(),
        "errors": errors,
        "extension_keys": extension_keys,
        "nonstandard_name": nonstandard_name,
    }


def audit_bundle(bundle: Path) -> dict[str, object]:
    bundle = bundle.resolve()
    if not bundle.is_dir():
        raise FileNotFoundError(f"Portable skill bundle not found: {bundle}")

    paths = sorted(bundle.rglob("SKILL.md"), key=lambda item: item.as_posix().lower())
    results = [inspect_skill(path) for path in paths]
    errors = [item for item in results if item.get("errors")]
    extension_counts: Counter[str] = Counter()
    extended_files = 0
    nonstandard_names = 0
    for item in results:
        extensions = item.get("extension_keys", [])
        if extensions:
            extended_files += 1
            extension_counts.update(extensions)
        if item.get("nonstandard_name"):
            nonstandard_names += 1

    warning_files = sum(
        bool(item.get("extension_keys")) or bool(item.get("nonstandard_name"))
        for item in results
    )
    return {
        "schema_version": 1,
        "status": "PASS_COMPATIBLE" if not errors else "FAIL",
        "bundle": str(bundle),
        "skill_files": len(paths),
        "strict_template_compatible": len(paths) - warning_files - len(errors),
        "compatible_with_warnings": warning_files,
        "extended_frontmatter_files": extended_files,
        "nonstandard_name_files": nonstandard_names,
        "extension_key_counts": dict(sorted(extension_counts.items())),
        "errors": errors,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit portable SKILL.md entrypoints without modifying upstream files."
    )
    parser.add_argument("--bundle", type=Path, default=Path("portable-skills"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = audit_bundle(args.bundle)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS_COMPATIBLE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
