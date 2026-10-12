from __future__ import annotations

import re

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LIST_RE = re.compile(r"^\s*(?:[-*+] |\d+[.)]\s+)(.+?)\s*$")


def _clean_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return {}
    result: dict[str, str] = {}
    index = 1
    while index < end:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            index += 1
            continue
        key, raw = line.split(":", 1)
        key = key.strip()
        raw = raw.strip()
        if raw in {">", ">-", "|", "|-"}:
            block: list[str] = []
            index += 1
            while index < end and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
                block.append(lines[index].strip())
                index += 1
            joined = " ".join(item for item in block if item)
            if raw.endswith("-"):
                result[key] = joined
            else:
                result[key] = "\n".join(block)
            continue
        result[key] = _clean_scalar(raw)
        index += 1
    return result


def extract_sections(text: str) -> dict[str, tuple[str, ...]]:
    sections: dict[str, list[str]] = {"root": []}
    current = "root"
    in_fence = False
    for raw in text.splitlines():
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = HEADING_RE.match(raw)
        if heading:
            current = heading.group(2).strip().lower()
            sections.setdefault(current, [])
            continue
        item = LIST_RE.match(raw)
        if item:
            sections[current].append(item.group(1).strip())
    return {key: tuple(values) for key, values in sections.items()}


def section_values(sections: dict[str, tuple[str, ...]], aliases: tuple[str, ...]) -> tuple[str, ...]:
    for key, values in sections.items():
        normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", key).strip()
        if any(alias.casefold() in normalized.casefold() for alias in aliases):
            if values:
                return values[:12]
    return ()
