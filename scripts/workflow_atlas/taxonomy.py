from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from .models import SkillCard, SourceRef, WorkflowDefinition, WorkflowStep


def _source(root: Path, value: dict[str, object]) -> SourceRef:
    path = str(value['path'])
    start = int(value.get('line', 1))
    end = int(value.get('end_line', start))
    if start == end == 1:
        lines = (root / path).read_text(encoding='utf-8').splitlines()
        start = next((i for i, line in enumerate(lines, 1) if line.startswith('# ')), 1)
        end = len(lines)
    return SourceRef(path, start, end)


def load_workflows(root: Path) -> tuple[WorkflowDefinition, ...]:
    data = json.loads((root / "knowledge/system/workflow-purpose-model.json").read_text(encoding="utf-8"))
    workflows = []
    for item in data:
        steps = tuple(
            WorkflowStep(
                id=str(step["id"]), phase=str(step["phase"]), lane=str(step["lane"]),
                label=str(step["label"]), detail=str(step["detail"]), kind=str(step["kind"]),
                sources=tuple(_source(root, source) for source in step.get("sources", [])),
            ) for step in item["steps"]
        )
        workflows.append(WorkflowDefinition(
            id=str(item["id"]), label=str(item["label"]), purpose=str(item["purpose"]),
            trigger=tuple(item["trigger"]), inputs=tuple(item["inputs"]), logic=tuple(item["logic"]),
            steps=steps, approval_gate=tuple(item["approval_gate"]), outputs=tuple(item["outputs"]),
            validation=tuple(item["validation"]), failure_modes=tuple(item["failure_modes"]),
            keywords=tuple(item["keywords"]), source_paths=tuple(_source(root, source) for source in item["source_paths"]),
        ))
    return tuple(workflows)


def assign_workflows(card: SkillCard, workflows: tuple[WorkflowDefinition, ...]) -> tuple[str, ...]:
    haystack = " ".join((card.name, card.purpose, card.source)).casefold()
    matched = tuple(
        workflow.id for workflow in workflows
        if any(keyword.casefold() in haystack for keyword in workflow.keywords)
    )
    return matched or ("knowledge-portability",)


def route_skill(card: SkillCard, workflows: tuple[WorkflowDefinition, ...]) -> SkillCard:
    haystack = " ".join((card.name, card.purpose, card.source)).casefold()
    routes = assign_workflows(card, workflows)
    explicit = any(any(keyword.casefold() in haystack for keyword in workflow.keywords) for workflow in workflows)
    missing = card.missing_fields if explicit else card.missing_fields + ("routing_fallback",)
    return replace(card, workflow_ids=routes, missing_fields=tuple(dict.fromkeys(missing)))


def group_duplicate_names(cards: tuple[SkillCard, ...]) -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = {}
    for card in cards:
        grouped.setdefault(card.name.casefold(), []).append(card.id)
    return {name: tuple(sorted(ids)) for name, ids in sorted(grouped.items()) if len(ids) > 1}
