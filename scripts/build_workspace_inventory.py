from __future__ import annotations

import argparse
import json
import re
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


WORKSPACE_ROOTS = {
    "armorhue-and-trade": Path(r"D:\codex"),
    "independent-site-research": Path(r"C:\Users\26014\Documents\独立站"),
    "relay": Path(r"C:\Users\26014\Documents\中转站"),
    "nodes": Path(r"C:\Users\26014\Documents\节点"),
    "self-media": Path(r"C:\Users\26014\Documents\自媒体运营"),
    "skill-inventory": Path(r"C:\Users\26014\Documents\技能"),
}
SKILLS_ROOT = Path(r"C:\Users\26014\.codex\skills")
AUTOMATIONS_ROOT = Path(r"C:\Users\26014\.codex\automations")
EVIDENCE_FILENAMES = (
    "AGENTS.md",
    "TASK_STATE.md",
    "PROJECT_STATE.md",
    "README.md",
    "IMAGE_WORKFLOW.md",
    "PROMOTION_WORKFLOW.md",
)
CONFIG_ONLY_NAMES = {".agents", ".codex", ".git"}
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b([A-Z0-9_]*(?:API_KEY|TOKEN|PASSWORD|SECRET|COOKIE|AUTHORIZATION|PRIVATE_KEY))"
    r"\s*[:=]\s*([^\s\"'`]+)"
)


def _iso_mtime(path: Path) -> str | None:
    try:
        timestamp = path.stat().st_mtime
    except OSError:
        return None
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def _safe_text(value: str) -> str:
    return SECRET_ASSIGNMENT_RE.sub(lambda match: f"{match.group(1)}=redacted", value)


def _safe_value(value: Any) -> Any:
    if isinstance(value, str):
        return _safe_text(value)
    if isinstance(value, list):
        return [_safe_value(item) for item in value]
    return value


def build_workspace_inventory(roots: Mapping[str, Path]) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for name, configured_path in roots.items():
        path = Path(configured_path)
        resolved = path.resolve()
        evidence = [filename for filename in EVIDENCE_FILENAMES if (path / filename).is_file()]
        if not path.exists():
            status = "MISSING"
            updated = None
        else:
            visible_entries = [
                entry
                for entry in path.iterdir()
                if entry.name not in CONFIG_ONLY_NAMES and not entry.name.startswith(".")
            ]
            if evidence:
                status = "ACTIVE"
            elif visible_entries:
                status = "PRESENT"
            else:
                status = "CONFIG_ONLY"
            dated_paths = [path / filename for filename in evidence] or [path]
            timestamps = [stamp for item in dated_paths if (stamp := _iso_mtime(item))]
            updated = max(timestamps, default=None)
        inventory.append(
            {
                "name": _safe_text(name),
                "path": _safe_text(str(resolved)),
                "updated": updated,
                "status": status,
                "evidence_files": evidence,
            }
        )
    return inventory


def build_automation_inventory(root: Path) -> list[dict[str, Any]]:
    root = Path(root)
    if not root.is_dir():
        return []
    inventory: list[dict[str, Any]] = []
    for directory in sorted((item for item in root.iterdir() if item.is_dir()), key=lambda item: item.name.lower()):
        config = directory / "automation.toml"
        metadata: dict[str, Any] = {}
        if config.is_file():
            try:
                with config.open("rb") as handle:
                    parsed = tomllib.load(handle)
                metadata = {
                    key: _safe_value(parsed.get(key))
                    for key in ("name", "status", "rrule", "cwds")
                    if key in parsed
                }
            except (OSError, tomllib.TOMLDecodeError):
                metadata = {}
        cwds = metadata.get("cwds", [])
        if not isinstance(cwds, list):
            cwds = []
        inventory.append(
            {
                "name": metadata.get("name") or _safe_text(directory.name),
                "path": _safe_text(str(directory.resolve())),
                "updated": _iso_mtime(config if config.is_file() else directory),
                "status": metadata.get("status") or "METADATA_MISSING",
                "evidence_files": ["automation.toml"] if config.is_file() else [],
                "rrule": metadata.get("rrule"),
                "cwds": [_safe_text(str(item)) for item in cwds],
            }
        )
    return inventory


def build_skill_inventory(root: Path) -> list[dict[str, Any]]:
    root = Path(root)
    if not root.is_dir():
        return []
    inventory: list[dict[str, Any]] = []
    for skill_file in sorted(root.rglob("SKILL.md"), key=lambda item: str(item).lower()):
        if ".git" in skill_file.parts or "__pycache__" in skill_file.parts:
            continue
        inventory.append(
            {
                "name": _safe_text(skill_file.parent.name),
                "path": _safe_text(str(skill_file.parent.resolve())),
                "updated": _iso_mtime(skill_file),
                "status": "AVAILABLE",
                "evidence_files": ["SKILL.md"],
            }
        )
    return inventory


def write_inventories(
    output: Path,
    workspace_roots: Mapping[str, Path] = WORKSPACE_ROOTS,
    skills_root: Path = SKILLS_ROOT,
    automations_root: Path = AUTOMATIONS_ROOT,
) -> dict[str, int]:
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    payloads = {
        "workspaces.json": build_workspace_inventory(workspace_roots),
        "automations.json": build_automation_inventory(automations_root),
        "skills.json": build_skill_inventory(skills_root),
    }
    for filename, payload in payloads.items():
        (output / filename).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return {filename: len(payload) for filename, payload in payloads.items()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build safe metadata-only vault inventories.")
    parser.add_argument("--output", type=Path, default=Path("sources/inventory"))
    args = parser.parse_args(argv)
    counts = write_inventories(args.output)
    print(" ".join(f"{name}={count}" for name, count in counts.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
