# Knowledge Vault Workflow Atlas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an offline interactive atlas that explains every allowed work purpose, gives every included skill source instance a complete evidence-backed card, renders 13 Archify workflow diagrams, and publishes only the validated artifacts to the private Git repository.

**Architecture:** A Python-standard-library pipeline reads the existing portable skill catalog and complete `SKILL.md` files, converts them into typed skill cards, assigns them to a curated 13-purpose workflow taxonomy, and emits deterministic JSON plus one self-contained offline HTML entry point. Archify candidates are generated from the same workflow records, finalized into standalone HTML, and checked with provenance against the pinned repository revision. Generated output is validated for coverage, exclusions, secrets, links, schema consistency, and browser behavior before navigation and project state are updated.

**Tech Stack:** Python 3 standard library (`dataclasses`, `hashlib`, `html`, `json`, `pathlib`, `re`, `unittest`), vanilla HTML/CSS/JavaScript, Archify CLI, Git.

## Global Constraints

- Work only in the isolated `codex/workflow-map` worktree.
- Do not install packages, browsers, models, Docker images, or large dependencies.
- Treat `portable-skills/SKILL_CATALOG.json` and complete included `SKILL.md` files as the skill inventory source; do not infer a skill from its directory name alone.
- Cover all 219 catalog entries as source instances, preserve the 161-name duplicate relationship, and never silently collapse same-name entries from different paths.
- Apply the user-approved exclusion policy before generating any user-facing artifact.
- Do not include secrets, mailbox contents, browser profiles, cookies, tokens, raw customer-sensitive records, or unverified business claims.
- Preserve `PASS`, `WATCH`, `FAIL`, `BLOCKED`, and `UNVERIFIED` semantics.
- External side effects such as sending, publishing, deployment, purchases, or account changes must expose an explicit human-authorization gate.
- `docs/workflows/index.html` must work directly from `file://` with no CDN, online font, remote script, local server, or GitHub Pages dependency.
- Stable IDs and sorted output are required so identical input produces byte-stable JSON.
- GitHub Pages remains disabled; the repository remains private.
- Use LF-normalized UTF-8 JSON with `ensure_ascii=False`, two-space indentation, sorted keys where map ordering is not meaningful, and a trailing newline.

---

## File Structure

### Source and build code

- Create `scripts/workflow_atlas/__init__.py`: package exports.
- Create `scripts/workflow_atlas/models.py`: typed immutable records, status rules, stable IDs, serialization.
- Create `scripts/workflow_atlas/markdown.py`: dependency-free frontmatter, heading, list, and code-reference extraction.
- Create `scripts/workflow_atlas/extract.py`: catalog loading and complete skill-card extraction.
- Create `scripts/workflow_atlas/taxonomy.py`: 13 workflow definitions, keyword routing, fallback routing, duplicate grouping.
- Create `scripts/workflow_atlas/render.py`: deterministic JSON and self-contained HTML rendering.
- Create `scripts/workflow_atlas/archify.py`: Archify workflow-candidate generation.
- Create `scripts/build_workflow_atlas.py`: command-line build entry point.
- Create `scripts/validate_workflow_atlas.py`: independent generated-artifact validation entry point.
- Create `templates/workflow-atlas/index.html`: semantic offline shell.
- Create `templates/workflow-atlas/styles.css`: responsive visual system.
- Create `templates/workflow-atlas/app.js`: local filtering, selection, keyboard, hash, and detail-panel behavior.

### Curated evidence model

- Create `knowledge/system/workflow-purpose-model.json`: 13 reviewed work-purpose definitions and their source files.

### Tests

- Create `tests/test_workflow_atlas_models.py`.
- Create `tests/test_workflow_atlas_extract.py`.
- Create `tests/test_workflow_atlas_taxonomy.py`.
- Create `tests/test_workflow_atlas_render.py`.
- Create `tests/test_workflow_atlas_validation.py`.

### Generated delivery

- Create `docs/workflows/index.html`.
- Create `docs/workflows/README.md`.
- Create `docs/workflows/skill-catalog.json`.
- Create `docs/workflows/workflow-catalog.json`.
- Create `docs/workflows/coverage-report.json`.
- Create `docs/workflows/sources/archify-overview.json`.
- Create one Archify candidate and finalized HTML for each workflow ID under `docs/workflows/sources/` and `docs/workflows/diagrams/`.
- Modify `README.md`, `KNOWLEDGE_INDEX.md`, and `TASK_STATE.md` only after all generated-artifact checks pass.

---

### Task 1: Typed Workflow Atlas Model

**Files:**
- Create: `scripts/workflow_atlas/__init__.py`
- Create: `scripts/workflow_atlas/models.py`
- Create: `tests/test_workflow_atlas_models.py`

**Interfaces:**
- Produces: `SourceRef`, `SkillCard`, `WorkflowStep`, `WorkflowDefinition`, `stable_id()`, `to_jsonable()`.
- Consumes: no earlier task output.

- [ ] **Step 1: Write failing model tests**

```python
import unittest

from scripts.workflow_atlas.models import SkillCard, SourceRef, stable_id, to_jsonable


class WorkflowAtlasModelTests(unittest.TestCase):
    def test_stable_id_distinguishes_same_name_from_different_sources(self):
        left = stable_id("user-skills", "alpha/SKILL.md", "review")
        right = stable_id("plugin-cache", "pkg/skills/review/SKILL.md", "review")
        self.assertNotEqual(left, right)
        self.assertEqual(left, stable_id("user-skills", "alpha/SKILL.md", "review"))

    def test_skill_card_serializes_required_fields(self):
        card = SkillCard(
            id="user-skills-review-a1b2c3d4", name="review", source="user-skills",
            purpose="Review a change before landing.",
            when_to_use=("Before merging a change.",), inputs=("Repository diff",),
            logic=("Inspect evidence before making a finding.",),
            outputs=("Prioritized findings",), dependencies=(), approval_gate="read-only",
            validation=("Every finding has a source location.",),
            failure_modes=("Missing diff keeps the card UNVERIFIED.",),
            workflow_ids=("quality-assurance",),
            source_paths=(SourceRef("portable-skills/user-skills/review/SKILL.md"),),
            completeness="PASS", missing_fields=(), content_sha256="0" * 64,
        )
        payload = to_jsonable(card)
        self.assertEqual(["quality-assurance"], payload["workflow_ids"])
        self.assertEqual("PASS", payload["completeness"])
```

- [ ] **Step 2: Run the focused tests and confirm import failure**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_models.py' -v`  
Expected: `ModuleNotFoundError: No module named 'scripts.workflow_atlas'`.

- [ ] **Step 3: Implement immutable records and stable IDs**

```python
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import re
from typing import Any

STATUSES = frozenset({"PASS", "WATCH", "FAIL", "BLOCKED", "UNVERIFIED"})


@dataclass(frozen=True)
class SourceRef:
    path: str
    line: int | None = None
    end_line: int | None = None


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
    slug = re.sub(r"[^a-z0-9]+", "-", f"{source}-{name}".lower()).strip("-")
    digest = sha256(f"{source}\0{path}\0{name}".encode("utf-8")).hexdigest()[:10]
    return f"{slug}-{digest}"


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [to_jsonable(item) for item in value]
    return value
```

- [ ] **Step 4: Run focused tests**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_models.py' -v`  
Expected: 2 tests, `OK`.

- [ ] **Step 5: Commit the model**

```powershell
git add scripts/workflow_atlas tests/test_workflow_atlas_models.py
git commit -m "feat: add workflow atlas data model"
```

### Task 2: Evidence-Backed Skill Extraction

**Files:**
- Create: `scripts/workflow_atlas/markdown.py`
- Create: `scripts/workflow_atlas/extract.py`
- Create: `tests/test_workflow_atlas_extract.py`

**Interfaces:**
- Consumes: `SkillCard`, `SourceRef`, `stable_id()` from Task 1.
- Produces: `parse_frontmatter(text)`, `extract_sections(text)`, `load_skill_cards(root)`.

- [ ] **Step 1: Write failing parser and inventory tests**

```python
import json
from pathlib import Path
import tempfile
import unittest

from scripts.workflow_atlas.extract import load_skill_cards
from scripts.workflow_atlas.markdown import parse_frontmatter


class SkillExtractionTests(unittest.TestCase):
    def test_folded_description_is_read_completely(self):
        text = "---\nname: mail-helper\ndescription: >-\n  Draft mail.\n  Use before outreach.\n---\n# Mail\n"
        assert parse_frontmatter(text) == {
            "name": "mail-helper",
            "description": "Draft mail. Use before outreach.",
        }

    def test_every_catalog_entry_becomes_one_source_instance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "portable-skills/user-skills/demo/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                "---\nname: demo\ndescription: Use for verified demos.\n---\n"
                "# Demo\n## Workflow\n1. Read input.\n2. Validate output.\n",
                encoding="utf-8",
            )
            catalog = [{"name": "demo", "source": "user-skills", "skill_file": "user-skills/demo/SKILL.md"}]
            (root / "portable-skills/SKILL_CATALOG.json").write_text(json.dumps(catalog), encoding="utf-8")
            cards = load_skill_cards(root)
            assert len(cards) == 1
            assert cards[0].name == "demo"
            assert cards[0].logic == ("Read input.", "Validate output.")
```

- [ ] **Step 2: Run tests and confirm missing modules**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_extract.py' -v`  
Expected: import failure for `scripts.workflow_atlas.extract`.

- [ ] **Step 3: Implement dependency-free Markdown extraction**

Implement `parse_frontmatter()` so scalar, `>-`, `>`, `|-`, and `|` values are supported. Implement `extract_sections()` as a mapping from normalized heading text to bullet or numbered-list content. Preserve original text, remove Markdown list markers, and never execute code blocks.

```python
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LIST_RE = re.compile(r"^\s*(?:[-*+] |\d+[.)]\s+)(.+?)\s*$")


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
```

- [ ] **Step 4: Implement catalog-to-card extraction**

`load_skill_cards(root)` must open every path named by `SKILL_CATALOG.json`, hash the complete bytes, read the complete UTF-8 `SKILL.md`, and populate every `SkillCard` field. Explicit sections win; otherwise use frontmatter description for `purpose` and `when_to_use`. Missing evidence yields an empty tuple, records the field in `missing_fields`, and lowers `completeness` to `WATCH` or `UNVERIFIED`; it must never invent content.

```python
SECTION_ALIASES = {
    "logic": ("workflow", "工作流", "process", "流程", "how it works"),
    "inputs": ("inputs", "input", "输入", "requirements", "前置条件"),
    "outputs": ("outputs", "output", "输出", "deliverables", "交付"),
    "validation": ("validation", "verify", "verification", "验收", "验证"),
    "failure_modes": ("failure", "failures", "故障处理", "troubleshooting", "错误处理"),
    "dependencies": ("dependencies", "dependency", "依赖", "tools", "工具"),
}


def load_skill_cards(root: Path) -> tuple[SkillCard, ...]:
    catalog_path = root / "portable-skills/SKILL_CATALOG.json"
    entries = json.loads(catalog_path.read_text(encoding="utf-8"))
    cards = [_extract_one(root, entry) for entry in entries]
    return tuple(sorted(cards, key=lambda card: (card.name.casefold(), card.source, card.id)))
```

- [ ] **Step 5: Run focused extraction tests and real inventory smoke check**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_extract.py' -v`  
Expected: all tests `OK`.

Run:

```powershell
python -c "from pathlib import Path; from scripts.workflow_atlas.extract import load_skill_cards; c=load_skill_cards(Path('.')); print(len(c), len({x.name for x in c}))"
```

Expected: `219 161`.

- [ ] **Step 6: Commit extraction**

```powershell
git add scripts/workflow_atlas/markdown.py scripts/workflow_atlas/extract.py tests/test_workflow_atlas_extract.py
git commit -m "feat: extract evidence-backed skill cards"
```

### Task 3: Curated Work-Purpose Taxonomy and Routing

**Files:**
- Create: `knowledge/system/workflow-purpose-model.json`
- Create: `scripts/workflow_atlas/taxonomy.py`
- Create: `tests/test_workflow_atlas_taxonomy.py`

**Interfaces:**
- Consumes: extracted `SkillCard` instances.
- Produces: `load_workflows(root)`, `assign_workflows(card, workflows)`, `route_skill(card, workflows)`, `group_duplicate_names(cards)`.

- [ ] **Step 1: Write failing taxonomy tests**

```python
import unittest
from dataclasses import replace
from pathlib import Path

from scripts.workflow_atlas.extract import load_skill_cards
from scripts.workflow_atlas.taxonomy import assign_workflows, group_duplicate_names, load_workflows


class WorkflowAtlasTaxonomyTests(unittest.TestCase):
    def test_taxonomy_has_exact_reviewed_purpose_ids(self):
        workflows = load_workflows(Path("."))
        self.assertEqual(tuple(item.id for item in workflows), (
            "market-research", "email-outreach", "sales-follow-up", "product-commerce",
            "site-commerce", "content-production", "content-distillation",
            "visual-experience", "software-delivery", "quality-assurance",
            "deployment-operations", "automation-agents", "knowledge-portability",
        ))

    def test_every_skill_has_at_least_one_route(self):
        workflows = load_workflows(Path("."))
        for card in load_skill_cards(Path(".")):
            self.assertTrue(assign_workflows(card, workflows))

    def test_same_name_different_source_is_reported_as_duplicate_group(self):
        groups = group_duplicate_names(load_skill_cards(Path(".")))
        self.assertTrue(all(len(ids) > 1 for ids in groups.values()))
```

- [ ] **Step 2: Run tests and confirm taxonomy is missing**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_taxonomy.py' -v`  
Expected: import or file-not-found failure.

- [ ] **Step 3: Create the reviewed workflow source model**

Create a JSON array in the exact ID order asserted above. Every object must contain `id`, `label`, `purpose`, `trigger`, `inputs`, `logic`, `steps`, `approval_gate`, `outputs`, `validation`, `failure_modes`, `keywords`, and `source_paths`. Each `steps` item must contain `id`, `phase`, `lane`, `label`, `detail`, `kind`, and `sources`. The exact step IDs are `purpose`, `trigger`, `input`, `logic`, `execute`, `authorize`, `output`, `validate`, `failure`, and `state`; the non-error main path uses all except `failure` in that order. Every source reference includes a verified repository-relative path plus inclusive `line` and `end_line` values.

Use these evidence routes:

| Workflow ID | Primary evidence |
|---|---|
| `market-research` | `knowledge/commerce/customer-first-research-runbook.md`, `knowledge/trade/foreign-trade-operations.md` |
| `email-outreach` | `knowledge/trade/foreign-trade-operations.md`, allowed email skills |
| `sales-follow-up` | `knowledge/trade/foreign-trade-operations.md`, allowed trade skills |
| `product-commerce` | `knowledge/commerce/customer-first-product-research.md`, `knowledge/commerce/jd-product-automation.md` |
| `site-commerce` | `knowledge/sites/independent-sites-and-shopify.md`, `knowledge/sites/shopify-connection-guide.md` |
| `content-production` | `knowledge/media/self-media-operations.md` |
| `content-distillation` | `knowledge/media/self-media-distillation-runbook.md`, `knowledge/distillation/content-distillation-system.md` |
| `visual-experience` | design and visual skill source files |
| `software-delivery` | planning, implementation, debugging, and review skill source files |
| `quality-assurance` | QA, security, performance, and verification skill source files |
| `deployment-operations` | `knowledge/infrastructure/relay-configuration-guide.md`, deployment and monitoring skills |
| `automation-agents` | `knowledge/system/automation-rebuild-guide.md`, agent and automation skills |
| `knowledge-portability` | `knowledge/ai-workflows/portable-ai-brain.md`, `knowledge/system/skills-portability-guide.md`, `knowledge/system/workspace-portability-guide.md` |

Every workflow must explicitly include the canonical stages `目的`, `触发`, `输入与证据`, `判断逻辑`, `执行`, `授权门`, `输出`, `验收`, `失败处理`, and `状态沉淀`. For workflows without external side effects, the approval step says `只读或本地操作，无外部副作用`; for workflows with side effects it names the exact approval boundary.

- [ ] **Step 4: Implement deterministic routing**

Use case-folded text from `name`, `purpose`, and source category. Match explicit workflow keywords first; if several match, preserve workflow-model order. Route skills with no keyword match to `knowledge-portability` and add `routing_fallback` to their missing fields so the coverage report exposes the weak classification.

```python
def assign_workflows(card: SkillCard, workflows: tuple[WorkflowDefinition, ...]) -> tuple[str, ...]:
    haystack = " ".join((card.name, card.purpose, card.source)).casefold()
    matched = tuple(
        workflow.id
        for workflow in workflows
        if any(keyword.casefold() in haystack for keyword in workflow.keywords)
    )
    return matched or ("knowledge-portability",)


def route_skill(card: SkillCard, workflows: tuple[WorkflowDefinition, ...]) -> SkillCard:
    matched = assign_workflows(card, workflows)
    has_explicit_match = any(
        any(keyword.casefold() in " ".join((card.name, card.purpose, card.source)).casefold()
            for keyword in workflow.keywords)
        for workflow in workflows
    )
    missing = card.missing_fields if has_explicit_match else card.missing_fields + ("routing_fallback",)
    return replace(card, workflow_ids=matched, missing_fields=missing)


def group_duplicate_names(cards: tuple[SkillCard, ...]) -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = {}
    for card in cards:
        grouped.setdefault(card.name.casefold(), []).append(card.id)
    return {
        name: tuple(sorted(ids))
        for name, ids in sorted(grouped.items())
        if len(ids) > 1
    }
```

- [ ] **Step 5: Run taxonomy tests**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_taxonomy.py' -v`  
Expected: all tests `OK`, 13 workflows, 0 unrouted skills.

- [ ] **Step 6: Commit taxonomy**

```powershell
git add knowledge/system/workflow-purpose-model.json scripts/workflow_atlas/taxonomy.py tests/test_workflow_atlas_taxonomy.py
git commit -m "feat: define work-purpose taxonomy"
```

### Task 4: Deterministic Catalog Builder and Coverage Gate

**Files:**
- Create: `scripts/build_workflow_atlas.py`
- Create: `scripts/workflow_atlas/render.py`
- Create: `scripts/validate_workflow_atlas.py`
- Create: `tests/test_workflow_atlas_validation.py`
- Generate: `docs/workflows/skill-catalog.json`
- Generate: `docs/workflows/workflow-catalog.json`
- Generate: `docs/workflows/coverage-report.json`

**Interfaces:**
- Consumes: `load_skill_cards()`, `load_workflows()`, `route_skill()`, `group_duplicate_names()`.
- Produces: `build_atlas(root, output_dir) -> dict`, `validate_atlas(root, output_dir) -> list[str]`.

- [ ] **Step 1: Write failing end-to-end coverage tests**

```python
class WorkflowAtlasValidationTests(unittest.TestCase):
    def test_real_catalog_has_complete_source_instance_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = build_atlas(Path("."), Path(tmp))
            self.assertEqual(219, report["inventory"]["skill_source_instances"])
            self.assertEqual(161, report["inventory"]["unique_skill_names"])
            self.assertEqual(0, report["coverage"]["orphan_skill_count"])
            self.assertEqual(0, report["coverage"]["orphan_workflow_count"])

    def test_validator_rejects_unknown_workflow_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            build_atlas(Path("."), out)
            cards = json.loads((out / "skill-catalog.json").read_text(encoding="utf-8"))
            cards[0]["workflow_ids"] = ["missing-workflow"]
            (out / "skill-catalog.json").write_text(json.dumps(cards), encoding="utf-8")
            errors = validate_atlas(Path("."), out)
            self.assertTrue(any("missing-workflow" in item for item in errors))
```

- [ ] **Step 2: Run test and confirm builder is absent**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_validation.py' -v`  
Expected: import failure for builder or validator.

- [ ] **Step 3: Implement deterministic JSON writes and coverage report**

```python
def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build_atlas(root: Path, output_dir: Path) -> dict[str, object]:
    workflows = load_workflows(root)
    cards = tuple(route_skill(card, workflows) for card in load_skill_cards(root))
    report = build_coverage_report(cards, workflows, group_duplicate_names(cards))
    write_json(output_dir / "skill-catalog.json", [to_jsonable(card) for card in cards])
    write_json(output_dir / "workflow-catalog.json", [to_jsonable(item) for item in workflows])
    write_json(output_dir / "coverage-report.json", report)
    return report
```

The report must contain inventory counts, completeness counts, duplicate-name groups, fallback-routed skill IDs, missing-field counts, orphan counts, workflow skill counts, source revision, and generation command. It must not contain timestamps so repeat builds remain byte-stable.

- [ ] **Step 4: Implement fail-closed validation**

Validate JSON syntax, required fields, allowed statuses, unique IDs, exact source-instance count, source-path existence, workflow cross-references, at least one skill per workflow, at least one workflow per skill, duplicate-group consistency, absence of disallowed content in generated files, and absence of secret-assignment patterns. Exit 1 with one error per line; exit 0 with a compact count summary.

```python
def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    output = root / "docs/workflows"
    errors = validate_atlas(root, output)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("workflow_atlas_errors=0")
    return 0
```

- [ ] **Step 5: Build twice and prove deterministic JSON**

Run:

```powershell
python scripts\build_workflow_atlas.py .
Get-FileHash docs\workflows\skill-catalog.json,docs\workflows\workflow-catalog.json,docs\workflows\coverage-report.json
python scripts\build_workflow_atlas.py .
Get-FileHash docs\workflows\skill-catalog.json,docs\workflows\workflow-catalog.json,docs\workflows\coverage-report.json
```

Expected: both hash sets are identical.

- [ ] **Step 6: Run validation tests and real validator**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_validation.py' -v`  
Expected: all tests `OK`.

Run: `python scripts\validate_workflow_atlas.py .`  
Expected: `workflow_atlas_errors=0`.

- [ ] **Step 7: Commit catalogs and validation**

```powershell
git add scripts/build_workflow_atlas.py scripts/validate_workflow_atlas.py scripts/workflow_atlas/render.py tests/test_workflow_atlas_validation.py docs/workflows/*.json
git commit -m "feat: build complete workflow catalogs"
```

### Task 5: Offline Interactive Atlas

**Files:**
- Create: `templates/workflow-atlas/index.html`
- Create: `templates/workflow-atlas/styles.css`
- Create: `templates/workflow-atlas/app.js`
- Create: `tests/test_workflow_atlas_render.py`
- Generate: `docs/workflows/index.html`

**Interfaces:**
- Consumes: generated skill, workflow, and coverage JSON.
- Produces: `render_index(output_dir, template_dir) -> Path` and a self-contained `index.html`.

- [ ] **Step 1: Write failing render tests**

```python
class WorkflowAtlasRenderTests(unittest.TestCase):
    def test_index_is_self_contained_and_embeds_all_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            build_atlas(Path("."), out)
            html_path = render_index(out, Path("templates/workflow-atlas"))
            html_text = html_path.read_text(encoding="utf-8")
            self.assertNotIn("https://", html_text)
            self.assertNotIn("<script src=", html_text)
            self.assertNotIn("<link rel=\"stylesheet\"", html_text)
            self.assertIn('id="atlas-data"', html_text)
            self.assertIn('data-skill-count="219"', html_text)

    def test_generated_html_has_keyboard_and_filter_controls(self):
        html_text = (Path("docs/workflows/index.html")).read_text(encoding="utf-8")
        for marker in ("workflow-search", "status-filter", "domain-nav", "detail-panel", "aria-live"):
            self.assertIn(marker, html_text)
```

- [ ] **Step 2: Run test and confirm renderer is absent**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_render.py' -v`  
Expected: import or file-not-found failure.

- [ ] **Step 3: Implement the semantic template**

The shell contains a compact header, search input, status filter, purpose navigation, workflow stage rail, skill result list, detail panel, coverage drawer, and diagram links. Use buttons for actions, a native select for status, visible focus, `aria-live="polite"` for result counts, and no instructional marketing copy.

```html
<script id="atlas-data" type="application/json">__ATLAS_JSON__</script>
<script>__ATLAS_JS__</script>
```

The renderer must replace all three exact tokens `__ATLAS_CSS__`, `__ATLAS_JSON__`, and `__ATLAS_JS__`, escape `</script` in embedded JSON, and fail if any token remains.

- [ ] **Step 4: Implement responsive visual styling**

Use a quiet workbench palette with neutral canvas, white surfaces, charcoal text, teal active state, amber `WATCH`, red `FAIL/BLOCKED`, and gray `UNVERIFIED`. Cards use at most 8px radius. Desktop uses fixed tracks `240px minmax(360px, 1fr) minmax(320px, 420px)`; below 980px it becomes one column. Do not scale font size with viewport width. Set `letter-spacing: 0`; never hide overflow to pass tests.

- [ ] **Step 5: Implement interaction logic**

```javascript
const data = JSON.parse(document.getElementById("atlas-data").textContent);
const state = { workflowId: location.hash.slice(1) || data.workflows[0].id, query: "", status: "ALL", skillId: null };

function filteredSkills() {
  const query = state.query.trim().toLocaleLowerCase("zh-CN");
  return data.skills.filter((skill) => {
    const inWorkflow = skill.workflow_ids.includes(state.workflowId);
    const inStatus = state.status === "ALL" || skill.completeness === state.status;
    const text = [skill.name, skill.purpose, ...skill.inputs, ...skill.outputs].join(" ").toLocaleLowerCase("zh-CN");
    return inWorkflow && inStatus && (!query || text.includes(query));
  });
}

function selectWorkflow(id) {
  if (!data.workflows.some((workflow) => workflow.id === id)) return;
  state.workflowId = id;
  state.skillId = null;
  history.replaceState(null, "", `#${id}`);
  render();
}
```

`render()` must preserve layout dimensions, update selected states, show all canonical workflow stages, list matching skills, render every card field, expose source paths as local relative links, and build diagram links with `` `diagrams/${workflow.id}.html` ``. Escape all rendered text; never use source content as HTML.

- [ ] **Step 6: Generate and test the offline page**

Run: `python scripts\build_workflow_atlas.py .`  
Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_render.py' -v`  
Expected: all tests `OK`; generated HTML contains 219 embedded skill records.

- [ ] **Step 7: Commit the offline atlas**

```powershell
git add templates/workflow-atlas tests/test_workflow_atlas_render.py scripts/workflow_atlas/render.py docs/workflows/index.html
git commit -m "feat: add offline workflow atlas"
```

### Task 6: Archify Workflow Diagrams

**Files:**
- Create: `scripts/workflow_atlas/archify.py`
- Modify: `scripts/build_workflow_atlas.py`
- Create: `tests/test_workflow_atlas_archify.py`
- Generate: `docs/workflows/sources/archify-overview.json`
- Generate: `docs/workflows/sources/market-research.json`, `email-outreach.json`, `sales-follow-up.json`, `product-commerce.json`, `site-commerce.json`, `content-production.json`, `content-distillation.json`, `visual-experience.json`, `software-delivery.json`, `quality-assurance.json`, `deployment-operations.json`, `automation-agents.json`, and `knowledge-portability.json`.
- Generate: `docs/workflows/diagrams/workflow-overview.html`
- Generate: the same 13 exact IDs as `.html` files under `docs/workflows/diagrams/`.

**Interfaces:**
- Consumes: `WorkflowDefinition`, repository URL, pinned 40-character revision.
- Produces: `build_archify_candidate(workflow, repository) -> dict`, `build_overview_candidate(workflows, repository) -> dict`, and 14 validated standalone HTML diagrams.

- [ ] **Step 1: Write failing candidate-shape tests**

```python
import unittest
from pathlib import Path

from scripts.workflow_atlas.archify import build_archify_candidate, build_overview_candidate
from scripts.workflow_atlas.taxonomy import load_workflows


class WorkflowAtlasArchifyTests(unittest.TestCase):
    def test_workflow_candidate_has_required_archify_shape(self):
        workflow = load_workflows(Path("."))[0]
        candidate = build_archify_candidate(
            workflow,
            {"url": "https://github.com/ljx30829/personal-ai-knowledge-base.git", "revision": "0" * 40},
        )
        self.assertEqual(2, candidate["schema_version"])
        self.assertEqual("workflow", candidate["diagram_type"])
        self.assertEqual(f"{workflow.id}-purpose", candidate["mainPath"][0])
        self.assertEqual(f"{workflow.id}-state", candidate["mainPath"][-1])
        self.assertTrue(all(node["sources"] for node in candidate["nodes"]))

    def test_overview_candidate_links_all_thirteen_purposes(self):
        workflows = load_workflows(Path("."))
        candidate = build_overview_candidate(
            workflows,
            {"url": "https://github.com/ljx30829/personal-ai-knowledge-base.git", "revision": "0" * 40},
        )
        workflow_nodes = [node for node in candidate["nodes"] if node["id"].startswith("purpose-")]
        self.assertEqual(13, len(workflow_nodes))
```

- [ ] **Step 2: Run focused test and confirm generator is absent**

Run: `python -m unittest discover -s tests -p 'test_workflow_atlas_archify.py' -v`  
Expected: import failure for `scripts.workflow_atlas.archify`.

- [ ] **Step 3: Implement candidates from the reviewed workflow records**

Use schema version 2, `diagram_type: workflow`, `locale: zh-CN`, `visual_preset: editorial`, `quality_profile: showcase`, and no animation. Use four lanes: `intent`, `evidence`, `execution`, and `governance`; use six columns and three phases. Convert the canonical stages into a readable main path and use branch/error edges for authorization denial and validation failure. Every node gets one to three repository source references.

```python
def build_archify_candidate(workflow: WorkflowDefinition, repository: dict[str, str]) -> dict[str, object]:
    nodes = [step_to_node(workflow.id, step) for step in workflow.steps]
    return {
        "schema_version": 2,
        "diagram_type": "workflow",
        "meta": {
            "title": f"{workflow.label}：目的、逻辑与执行流程",
            "locale": "zh-CN",
            "output": f"docs/workflows/diagrams/{workflow.id}.html",
            "animation": "none",
            "visual_preset": "editorial",
            "quality_profile": "showcase",
            "repository": {**repository, "provider": "github", "link_mode": "web"},
        },
        "lanes": LANES,
        "phases": PHASES,
        "mainPath": [node["id"] for node in nodes if node["tag"] != "异常"],
        "nodes": nodes,
        "edges": build_edges(workflow.id, nodes),
        "cards": build_cards(workflow),
    }


def build_overview_candidate(
    workflows: tuple[WorkflowDefinition, ...], repository: dict[str, str]
) -> dict[str, object]:
    nodes = [overview_node(workflow, index) for index, workflow in enumerate(workflows)]
    return {
        "schema_version": 2,
        "diagram_type": "workflow",
        "meta": {
            "title": "知识库完整工作目的地图",
            "locale": "zh-CN",
            "output": "docs/workflows/diagrams/workflow-overview.html",
            "animation": "none",
            "visual_preset": "editorial",
            "quality_profile": "showcase",
            "repository": {**repository, "provider": "github", "link_mode": "web"},
        },
        "lanes": OVERVIEW_LANES,
        "phases": OVERVIEW_PHASES,
        "mainPath": [node["id"] for node in nodes],
        "nodes": nodes,
        "edges": overview_edges(nodes),
        "cards": overview_cards(workflows),
    }
```

- [ ] **Step 4: Generate all 14 candidates at the final pinned commit**

Record Task 5 `HEAD` and pass it unchanged as repository evidence:

```powershell
$sourceRevision = (git rev-parse HEAD).Trim()
python scripts\build_workflow_atlas.py . --archify-candidates --revision $sourceRevision
```

Expected: 14 candidate JSON files and no HTML yet.

- [ ] **Step 5: Finalize every candidate**

Run the exact 14-item batch:

```powershell
$diagramIds = @(
  "workflow-overview", "market-research", "email-outreach", "sales-follow-up",
  "product-commerce", "site-commerce", "content-production", "content-distillation",
  "visual-experience", "software-delivery", "quality-assurance",
  "deployment-operations", "automation-agents", "knowledge-portability"
)
foreach ($diagramId in $diagramIds) {
  $candidateId = if ($diagramId -eq "workflow-overview") { "archify-overview" } else { $diagramId }
  node C:\Users\26014\.codex\skills\archify\bin\archify.mjs finalize workflow `
    "docs\workflows\sources\$candidateId.json" `
    "docs\workflows\diagrams\$diagramId.html" `
    --repo-root . --quality showcase --out-dir "docs\workflows\evidence\$diagramId" --json
  if ($LASTEXITCODE -ne 0) { throw "Archify finalize failed: $diagramId" }
}
```

Expected for every invocation: exit 0, showcase validation 9/9, strict check pass, browser check pass. Keep compact summary receipts in each exact-ID directory under `docs/workflows/evidence/`; do not commit screenshots, delivery locks, journals, or temporary evidence.

- [ ] **Step 6: Run optional captures and inspect the requested visual surface**

Run `visual-check --summary --require-provenance` for the overview and a representative dense workflow. Inspect 1440x900 and 2048x1320 in light and dark themes. Check text fit, route crossings, label fit, lower-band balance, search/focus behavior, and diagram links. Permit at most two focused correction rounds; after any candidate change, rerun full `finalize` with a fresh evidence directory.

- [ ] **Step 7: Commit candidates and finalized diagrams**

```powershell
git add scripts/workflow_atlas/archify.py scripts/build_workflow_atlas.py tests/test_workflow_atlas_archify.py docs/workflows/sources docs/workflows/diagrams
git commit -m "feat: add validated workflow diagrams"
```

### Task 7: Documentation and Navigation

**Files:**
- Create: `docs/workflows/README.md`
- Modify: `README.md`
- Modify: `KNOWLEDGE_INDEX.md`
- Modify: `TASK_STATE.md`

**Interfaces:**
- Consumes: final coverage report, diagram receipts, commit revision.
- Produces: durable entry points and truthful handoff state.

- [ ] **Step 1: Write the workflow README**

Document the three layers, direct local-open path, search/filter behavior, status meanings, rebuild commands, verification commands, GitHub raw-file limitation, private-repository requirement, and no-Pages rule. State exact inventory counts from `coverage-report.json`, not handwritten estimates.

- [ ] **Step 2: Add root navigation links**

Add one concise “交互式工作流地图” entry to `README.md` and `KNOWLEDGE_INDEX.md`, pointing to `docs/workflows/index.html` and `docs/workflows/README.md`. Do not add marketing copy or claim online hosting.

- [ ] **Step 3: Update durable state from evidence**

Replace `DESIGN_REVIEW_PENDING` with the actual result. Record the final commit, exact skill source-instance and unique-name counts, workflow count, completeness distribution, validator output, Archify gate results, visual-review scope, and any `WATCH/UNVERIFIED` gaps. Do not write `PASS` for a gate that did not run successfully.

- [ ] **Step 4: Validate navigation and commit**

Run: `python scripts\validate_vault.py .`  
Expected: 0 errors, 0 warnings.

```powershell
git add docs/workflows/README.md README.md KNOWLEDGE_INDEX.md TASK_STATE.md
git commit -m "docs: publish workflow atlas navigation"
```

### Task 8: Full Verification and Private Git Publication

**Files:**
- Verify all files changed since `5526753e4c4d6045d2594985e971ba5cdc3c5c34`.
- No new implementation files beyond those listed in this plan unless a verified defect requires a focused test fixture.

**Interfaces:**
- Consumes: all prior task outputs.
- Produces: verified `codex/workflow-map` branch and fast-forward-safe private remote update.

- [ ] **Step 1: Run all tests and validators from scratch**

```powershell
python -m unittest discover -s tests -p 'test_*.py'
python scripts\validate_workflow_atlas.py .
python scripts\validate_vault.py .
git diff --check origin/master...HEAD
```

Expected: all unit tests pass; both validators report 0 errors; diff check is silent.

- [ ] **Step 2: Verify scope and exclusion boundaries**

Inspect `git diff --name-status origin/master...HEAD`. Confirm every changed file belongs to the design, plan, workflow source/build/test/template/delivery/navigation/state scope. Scan only newly generated workflow artifacts for the configured exclusion patterns and secret patterns; expected result is no matches.

- [ ] **Step 3: Verify offline browser behavior**

Open `docs/workflows/index.html` through `file://` at 1440x900 and 390x844. Verify nonblank content, no horizontal overflow, working purpose selection, search, status filter, skill selection, hash deep links, local source links, and diagram links. Check console errors and failed network requests; expected counts are zero.

- [ ] **Step 4: Rebase safely if remote moved**

```powershell
git fetch origin
git rev-list --left-right --count origin/master...HEAD
```

If `origin/master` advanced, rebase the isolated branch onto it, rerun Step 1, and resolve only workflow-atlas files. Never force-push and never use the dirty primary workspace as a merge source.

- [ ] **Step 5: Push the reviewed branch and fast-forward master**

Push `codex/workflow-map`, verify the remote branch commit, then fast-forward remote `master` only when Git confirms no non-fast-forward overwrite. Keep the repository private and do not enable Pages.

```powershell
git push -u origin codex/workflow-map
git push origin codex/workflow-map:master
git ls-remote origin refs/heads/master refs/heads/codex/workflow-map
```

Expected: both refs resolve to the verified final commit.

- [ ] **Step 6: Final handoff evidence**

Report the remote commit, local entry path, three catalog paths, 14 diagram count, exact coverage counts, test totals, validator results, browser checks, perceptual review status, and remaining `WATCH/UNVERIFIED` gaps. Explicitly state that GitHub stores the files and local opening supplies the interaction.

---

## Plan Self-Review

- Spec coverage: data model, full skill-source coverage, work-purpose workflows, offline interaction, Archify output, exclusions, authorization gates, validation, navigation, and private Git publication each have a dedicated task.
- Deferred-work scan: no implementation step leaves behavior unspecified; the three `__ATLAS_*__` strings are deliberate renderer tokens and the renderer test requires all of them to be replaced.
- Type consistency: `SkillCard`, `WorkflowStep`, `WorkflowDefinition`, `load_skill_cards`, `load_workflows`, `assign_workflows`, `build_atlas`, `render_index`, `build_archify_candidate`, and `validate_atlas` are defined once and consumed by their exact names.
- Scope decision: this remains one plan because the catalog, UI, and diagrams share one schema and one coverage gate; splitting them would allow inconsistent counts and orphan references.
