from __future__ import annotations

import html
import json
from pathlib import Path


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def render_index(output_dir: Path, template_dir: Path) -> Path:
    html_template = (template_dir / "index.html").read_text(encoding="utf-8")
    css = (template_dir / "styles.css").read_text(encoding="utf-8")
    js = (template_dir / "app.js").read_text(encoding="utf-8")
    skills = json.loads((output_dir / "skill-catalog.json").read_text(encoding="utf-8"))
    workflows = json.loads((output_dir / "workflow-catalog.json").read_text(encoding="utf-8"))
    coverage = json.loads((output_dir / "coverage-report.json").read_text(encoding="utf-8"))
    payload = {"skills": skills, "workflows": workflows, "coverage": coverage}
    embedded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</script", "<\\/script")
    rendered = html_template.replace("__ATLAS_CSS__", css).replace("__ATLAS_JSON__", embedded).replace("__ATLAS_JS__", js)
    if any(token in rendered for token in ("__ATLAS_CSS__", "__ATLAS_JSON__", "__ATLAS_JS__")):
        raise ValueError("unreplaced atlas template token")
    rendered = rendered.replace('data-skill-count="__SKILL_COUNT__"', f'data-skill-count="{len(skills)}"')
    rendered = rendered.replace('data-workflow-count="__WORKFLOW_COUNT__"', f'data-workflow-count="{len(workflows)}"')
    target = output_dir / "index.html"
    target.write_text(rendered, encoding="utf-8", newline="\n")
    return target
