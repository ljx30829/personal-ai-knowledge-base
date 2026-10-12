from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.workflow_atlas.extract import load_skill_cards
from scripts.workflow_atlas.models import to_jsonable
from scripts.workflow_atlas.render import render_index, write_json
from scripts.workflow_atlas.taxonomy import group_duplicate_names, load_workflows, route_skill


def git_revision(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unverified-local-state"


def build_coverage_report(cards, workflows, duplicate_groups, revision: str) -> dict[str, object]:
    completeness: dict[str, int] = {}
    missing_fields: dict[str, int] = {}
    counts = {workflow.id: 0 for workflow in workflows}
    for card in cards:
        completeness[card.completeness] = completeness.get(card.completeness, 0) + 1
        for field in card.missing_fields:
            missing_fields[field] = missing_fields.get(field, 0) + 1
        for workflow_id in card.workflow_ids:
            counts[workflow_id] = counts.get(workflow_id, 0) + 1
    orphan_skills = [card.id for card in cards if not card.workflow_ids]
    orphan_workflows = [workflow.id for workflow in workflows if counts.get(workflow.id, 0) == 0]
    return {
        "schema_version": 1,
        "source_revision": revision,
        "generation_command": "python scripts/build_workflow_atlas.py .",
        "inventory": {
            "skill_source_instances": len(cards),
            "unique_skill_names": len({card.name for card in cards}),
            "workflow_count": len(workflows),
        },
        "completeness": dict(sorted(completeness.items())),
        "missing_field_counts": dict(sorted(missing_fields.items())),
        "coverage": {
            "orphan_skill_count": len(orphan_skills),
            "orphan_skill_ids": sorted(orphan_skills),
            "orphan_workflow_count": len(orphan_workflows),
            "orphan_workflow_ids": sorted(orphan_workflows),
            "fallback_routed_skill_ids": sorted(card.id for card in cards if "routing_fallback" in card.missing_fields),
            "workflow_skill_counts": dict(sorted(counts.items())),
        },
        "duplicate_name_groups": duplicate_groups,
    }


def build_atlas(root: Path, output_dir: Path, *, revision: str | None = None, archify_candidates: bool = False) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    workflows = load_workflows(root)
    cards = tuple(route_skill(card, workflows) for card in load_skill_cards(root))
    revision = revision or git_revision(root)
    report = build_coverage_report(cards, workflows, group_duplicate_names(cards), revision)
    write_json(output_dir / "skill-catalog.json", [to_jsonable(card) for card in cards])
    write_json(output_dir / "workflow-catalog.json", [to_jsonable(item) for item in workflows])
    write_json(output_dir / "coverage-report.json", report)
    template_dir = root / "templates/workflow-atlas"
    if (template_dir / "index.html").exists() and (template_dir / "styles.css").exists() and (template_dir / "app.js").exists():
        render_index(output_dir, template_dir)
    if archify_candidates:
        from scripts.workflow_atlas.archify import attach_model_lines, build_archify_candidate, build_overview_candidate

        repository = {"url": "https://github.com/ljx30829/personal-ai-knowledge-base.git", "revision": revision}
        sources = output_dir / "sources"
        sources.mkdir(parents=True, exist_ok=True)
        model_text = (root / "knowledge/system/workflow-purpose-model.json").read_text(encoding="utf-8")
        write_json(sources / "archify-overview.json", attach_model_lines(build_overview_candidate(workflows, repository), model_text))
        for workflow in workflows:
            write_json(sources / f"{workflow.id}.json", attach_model_lines(build_archify_candidate(workflow, repository), model_text))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--revision")
    parser.add_argument("--archify-candidates", action="store_true")
    args = parser.parse_args()
    report = build_atlas(Path(args.root).resolve(), Path(args.root).resolve() / "docs/workflows", revision=args.revision, archify_candidates=args.archify_candidates)
    print(json.dumps(report["inventory"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
