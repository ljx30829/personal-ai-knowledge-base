from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
import re

from .markdown import extract_sections, parse_frontmatter, section_values
from .models import SkillCard, SourceRef, stable_id

SECTION_ALIASES = {
    "logic": ("workflow", "工作流", "process", "流程", "how it works", "使用方式"),
    "inputs": ("inputs", "input", "输入", "requirements", "前置条件", "scope"),
    "outputs": ("outputs", "output", "输出", "deliverables", "交付"),
    "validation": ("validation", "verify", "verification", "验收", "验证", "quality"),
    "failure_modes": ("failure", "failures", "故障处理", "troubleshooting", "错误处理", "边界"),
    "dependencies": ("dependencies", "dependency", "依赖", "tools", "工具", "setup"),
}
SIDE_EFFECT_RE = re.compile(r"(?i)\b(send|publish|deploy|purchase|account|social|email|shopify|上线|发布|发送|部署|购买|账号|外联)\b")


def _first_sentence(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _field(values: tuple[str, ...], fallback: tuple[str, ...] = ()) -> tuple[str, ...]:
    return values or fallback


def _extract_one(root: Path, entry: dict[str, object]) -> SkillCard:
    relative = str(entry["skill_file"]).replace("\\", "/")
    path = root / "portable-skills" / Path(relative)
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    front = parse_frontmatter(text)
    sections = extract_sections(text)
    name = str(front.get("name") or entry.get("name") or path.parent.name)
    description = _first_sentence(str(front.get("description") or ""))
    logic = section_values(sections, SECTION_ALIASES["logic"])
    inputs = section_values(sections, SECTION_ALIASES["inputs"])
    outputs = section_values(sections, SECTION_ALIASES["outputs"])
    validation = section_values(sections, SECTION_ALIASES["validation"])
    failures = section_values(sections, SECTION_ALIASES["failure_modes"])
    dependencies = section_values(sections, SECTION_ALIASES["dependencies"])
    missing: list[str] = []
    if not description:
        missing.append("purpose")
    if not logic:
        missing.append("logic")
    if not inputs:
        missing.append("inputs")
    if not outputs:
        missing.append("outputs")
    if not validation:
        missing.append("validation")
    if not failures:
        missing.append("failure_modes")
    purpose = description or f"技能 {name} 的正文未提供可验证简介。"
    when_to_use = (description,) if description else ()
    source_ref = SourceRef("portable-skills/" + relative, 1, max(1, len(text.splitlines())), "SKILL.md")
    if SIDE_EFFECT_RE.search(f"{name} {description} {text}"):
        approval = "涉及外部副作用；发送、发布、部署、账号或购买动作必须获得当次人工授权。"
    else:
        approval = "未由关键词识别出外部动作；执行前仍需核对完整技能原文和当次授权范围。"
    completeness = "PASS" if not missing else ("WATCH" if description else "UNVERIFIED")
    return SkillCard(
        id=stable_id(str(entry.get("source", "unknown")), relative, name),
        name=name,
        source=str(entry.get("source", "unknown")),
        purpose=purpose,
        when_to_use=when_to_use,
        inputs=inputs,
        logic=logic,
        outputs=outputs,
        dependencies=dependencies,
        approval_gate=approval,
        validation=validation,
        failure_modes=failures,
        workflow_ids=(),
        source_paths=(source_ref,),
        completeness=completeness,
        missing_fields=tuple(missing),
        content_sha256=sha256(raw).hexdigest(),
    )


def load_skill_cards(root: Path) -> tuple[SkillCard, ...]:
    catalog_path = root / "portable-skills" / "SKILL_CATALOG.json"
    entries = json.loads(catalog_path.read_text(encoding="utf-8"))
    cards = [_extract_one(root, entry) for entry in entries]
    return tuple(sorted(cards, key=lambda card: (card.name.casefold(), card.source, card.id)))
