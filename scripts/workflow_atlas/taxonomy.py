from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from .models import SkillCard, SourceRef, WorkflowDefinition, WorkflowStep

NAME_ROUTE_RULES = {
    "market-research": ("research", "scrape", "hackernews", "browse", "hermes"),
    "email-outreach": ("email", "mail", "outreach", "sender", "hermes"),
    "sales-follow-up": ("sales", "follow", "trade", "excel"),
    "product-commerce": ("product", "catalog", "commerce", "marketplace", "payment"),
    "site-commerce": ("shopify", "storefront", "ecommerce", "cms", "site", "web-rebuilder"),
    "content-production": ("content", "document", "pdf", "presentation", "remotion", "writing", "brandkit", "template"),
    "content-distillation": ("distill", "transcrib", "whisper", "document", "content"),
    "visual-experience": ("design", "visual", "frontend", "ui", "ux", "image", "figma", "geist", "shadcn", "impeccable", "satori", "stitch"),
    "software-delivery": ("code", "codex", "debug", "investigat", "dev", "software", "sdk", "api", "react", "next", "turbo", "routing", "runtime", "auth", "bootstrap", "function", "ios", "android", "skill-creator"),
    "quality-assurance": ("test", "qa", "review", "audit", "verify", "verification", "benchmark", "health", "canary", "careful", "guard", "cso", "autoplan", "gstack", "ship", "playwright", "spreadsheet"),
    "deployment-operations": ("deploy", "observability", "monitor", "ops", "infrastructure", "relay", "node", "gateway", "firewall", "service", "storage", "env-var", "vercel-cli"),
    "automation-agents": ("automation", "agent", "workflow", "cron", "orchestration", "queue", "computer-use", "gbrain"),
    "knowledge-portability": ("knowledge", "portable", "git", "vault", "context", "migration", "learn", "skill-installer", "browser-cookies", "freeze", "diagram", "landing-report", "office-hours", "spec"),
}


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
    name = card.name.casefold()
    matched = tuple(
        workflow.id for workflow in workflows
        if workflow.id in NAME_ROUTE_RULES
        and any(keyword in name for keyword in NAME_ROUTE_RULES[workflow.id])
    )
    return matched or ("knowledge-portability",)


def route_skill(card: SkillCard, workflows: tuple[WorkflowDefinition, ...]) -> SkillCard:
    routes = assign_workflows(card, workflows)
    explicit = any(
        workflow_id in NAME_ROUTE_RULES
        and any(keyword in card.name.casefold() for keyword in NAME_ROUTE_RULES[workflow_id])
        for workflow_id in routes
    )
    missing = card.missing_fields if explicit else card.missing_fields + ("routing_fallback",)
    return replace(card, workflow_ids=routes, missing_fields=tuple(dict.fromkeys(missing)))


def group_duplicate_names(cards: tuple[SkillCard, ...]) -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = {}
    for card in cards:
        grouped.setdefault(card.name.casefold(), []).append(card.id)
    return {name: tuple(sorted(ids)) for name, ids in sorted(grouped.items()) if len(ids) > 1}
