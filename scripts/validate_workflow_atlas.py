from __future__ import annotations

import json
from pathlib import Path
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.workflow_atlas.extract import load_skill_cards
from scripts.workflow_atlas.models import STATUSES, to_jsonable
from scripts.workflow_atlas.taxonomy import group_duplicate_names, load_workflows

DISALLOWED = ("armorhue", "candy", "adult", "vehicle film", "车膜")
SECRET_RE = re.compile(r"(?i)\b[A-Z0-9_]*(?:API_KEY|TOKEN|PASSWORD|SECRET|COOKIE|AUTHORIZATION|PRIVATE_KEY)\s*[:=]\s*[\"']?([^\s\"'`]+)")
SAFE_VALUES = {"missing", "unset", "none", "null", "redacted", "example", "placeholder", "required", "not_configured"}


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def display_path(path: Path, root: Path) -> str:
    """Render paths safely even when tests place output outside the repository."""
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def validate_atlas(root: Path, output: Path) -> list[str]:
    errors: list[str] = []
    required = [output / "skill-catalog.json", output / "workflow-catalog.json", output / "coverage-report.json", output / "index.html"]
    for path in required:
        if not path.is_file():
            errors.append(f"missing generated artifact: {display_path(path, root)}")
    if errors:
        return errors
    try:
        skills = _load(output / "skill-catalog.json")
        workflows = _load(output / "workflow-catalog.json")
        report = _load(output / "coverage-report.json")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid generated JSON: {exc}"]
    source_cards = load_skill_cards(root)
    expected_cards = {card.id: card for card in source_cards}
    workflow_ids = {item["id"] for item in workflows}
    skill_ids = [item.get("id") for item in skills]
    if len(skills) != len(source_cards):
        errors.append(f"skill source count mismatch: {len(skills)} != {len(source_cards)}")
    if len(skill_ids) != len(set(skill_ids)):
        errors.append("duplicate skill IDs")
    if set(skill_ids) != set(expected_cards):
        errors.append("skill source identities differ from inventory")
    if tuple(item["id"] for item in workflows) != tuple(item.id for item in load_workflows(root)):
        errors.append("workflow ordering or IDs differ from source model")
    counts = {workflow_id: 0 for workflow_id in workflow_ids}
    for item in skills:
        if item.get("completeness") not in STATUSES:
            errors.append(f"invalid completeness for {item.get('id')}")
        expected = expected_cards.get(item.get('id'))
        if expected and (item.get('content_sha256') != expected.content_sha256 or item.get('source_paths') != to_jsonable(expected.source_paths)):
            errors.append(f"skill source/hash mismatch: {item.get('id')}")
        if not item.get('workflow_ids'):
            errors.append(f"unrouted skill: {item.get('id')}")
        for workflow_id in item.get("workflow_ids", []):
            if workflow_id not in workflow_ids:
                errors.append(f"{item.get('id')} references missing workflow {workflow_id}")
            else:
                counts[workflow_id] += 1
        for source in item.get("source_paths", []):
            source_path = root / source["path"]
            if not source_path.is_file():
                errors.append(f"missing skill source: {source['path']}")
    for workflow_id, count in counts.items():
        if count == 0:
            errors.append(f"orphan workflow: {workflow_id}")
    if report.get("inventory", {}).get("skill_source_instances") != len(source_cards):
        errors.append("coverage report skill count mismatch")
    if report.get("inventory", {}).get("unique_skill_names") != len({card.name for card in source_cards}):
        errors.append("coverage report unique-name count mismatch")
    if report.get("duplicate_name_groups") != to_jsonable(group_duplicate_names(source_cards)):
        errors.append("duplicate-name groups mismatch")
    if report.get('coverage', {}).get('workflow_skill_counts') != counts:
        errors.append('coverage report route counts mismatch')
    page = (output / 'index.html').read_text(encoding='utf-8')
    match = re.search(r'<script id="atlas-data" type="application/json">(.*?)</script>', page, re.S)
    if not match:
        errors.append('missing embedded offline catalog')
    else:
        try:
            embedded = json.loads(match.group(1))
            if embedded != {'skills': skills, 'workflows': workflows, 'coverage': report}:
                errors.append('offline embedded catalogs are stale')
        except json.JSONDecodeError:
            errors.append('invalid embedded offline catalog')
    if re.search(r'<(?:script|link)\b[^>]*(?:src|href)=[\"\']https?://', page, re.I):
        errors.append('remote runtime dependency in offline page')
    for path in output.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".html", ".md"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lowered = text.casefold()
        for term in DISALLOWED:
            if term in lowered:
                errors.append(f"excluded term in {display_path(path, root)}: {term}")
        for match in SECRET_RE.finditer(text):
            if match.group(1).casefold() not in SAFE_VALUES:
                errors.append(f"possible secret assignment in {display_path(path, root)}")
    return sorted(set(errors))


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate_atlas(root, root / "docs/workflows")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("workflow_atlas_errors=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
