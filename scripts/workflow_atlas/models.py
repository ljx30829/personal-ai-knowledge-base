from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import re
from typing import Any

STATUSES = frozenset({"PASS", "WATCH", "FAIL", "BLOCKED", "UNVERIFIED"})


@dataclass(frozen=True)
class SourceRef:
    path: str
    line: int | None = None
    end_line: int | None = None
    label: str | None = None


@dataclass(frozen=True)
class SkillCard:
    id: str
    name: str
    source: str
    purpose: str
    when_to_use: tuple[str, ...]
    inputs: tuple[str, ...]
    logic: tuple[str, ...]
    outputs: tuple[str, ...]
    dependencies: tuple[str, ...]
    approval_gate: str
    validation: tuple[str, ...]
    failure_modes: tuple[str, ...]
    workflow_ids: tuple[str, ...]
    source_paths: tuple[SourceRef, ...]
    completeness: str
    missing_fields: tuple[str, ...]
    content_sha256: str


@dataclass(frozen=True)
class WorkflowStep:
    id: str
    phase: str
    lane: str
    label: str
    detail: str
    kind: str
    sources: tuple[SourceRef, ...]


@dataclass(frozen=True)
class WorkflowDefinition:
    id: str
    label: str
    purpose: str
    trigger: tuple[str, ...]
    inputs: tuple[str, ...]
    logic: tuple[str, ...]
    steps: tuple[WorkflowStep, ...]
    approval_gate: tuple[str, ...]
    outputs: tuple[str, ...]
    validation: tuple[str, ...]
    failure_modes: tuple[str, ...]
    keywords: tuple[str, ...]
    source_paths: tuple[SourceRef, ...]


def stable_id(source: str, path: str, name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", f"{source}-{name}".lower()).strip("-") or "skill"
    digest = sha256(f"{source}\0{path}\0{name}".encode("utf-8")).hexdigest()[:10]
    return f"{slug}-{digest}"


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [to_jsonable(item) for item in value]
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    return value


def with_routes(card: SkillCard, workflow_ids: tuple[str, ...], missing_fields: tuple[str, ...] = ()) -> SkillCard:
    return replace(card, workflow_ids=workflow_ids, missing_fields=tuple(dict.fromkeys(card.missing_fields + missing_fields)))
