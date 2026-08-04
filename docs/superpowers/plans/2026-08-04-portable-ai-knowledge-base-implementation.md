# Portable AI Knowledge Base Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a private, portable Markdown knowledge repository that preserves the user's requirements and reusable Codex work across trade, independent sites, relay/node operations, skills, automations, self-media, and content distillation.

**Architecture:** Markdown files are the canonical knowledge source. A standard-library Python validator enforces structure, source metadata, link integrity, and a conservative secret scan. Existing Codex inventory tooling generates the detailed skills/requirements catalog, while concise topic pages keep the repository usable by humans and different AI clients.

**Tech Stack:** Markdown, Git, Python 3 standard library, existing local `codex_inventory.py`; no server, database, vector store, model download, or new package.

## Global Constraints

- The future GitHub repository must be `Private`; GitHub Pages must remain disabled.
- Do not copy API keys, tokens, cookies, passwords, browser profiles, mailbox contents, or raw customer-sensitive records.
- Do not require a continuously running computer or paid service.
- Preserve source paths, snapshot dates, evidence status, and uncertainty.
- `AGENTS.md` is the Codex entry point; `AI_CONTEXT.md` is the vendor-neutral entry point.
- Large logs, HTML, CSV, archives, images, videos, and complete state files stay in their original workspaces and are represented by inventories and summaries.

---

### Task 1: Vault foundation and AI entry points

**Files:**
- Create: `README.md`
- Create: `AGENTS.md`
- Create: `AI_CONTEXT.md`
- Create: `PROFILE.md`
- Create: `IDENTITY.md`
- Create: `KNOWLEDGE_INDEX.md`
- Create: `TASK_STATE.md`
- Create: `SECURITY.md`
- Create: `.gitignore`
- Create: `templates/knowledge-card.md`
- Create: `templates/source-card.md`
- Create: `templates/project-state.md`
- Create: `templates/decision-record.md`

**Interfaces:**
- Consumes: approved design at `docs/superpowers/specs/2026-08-04-portable-ai-knowledge-base-design.md`.
- Produces: stable entry-point documents and templates used by every later task.

- [ ] **Step 1: Create the root documents**

Write plain-language navigation, the mandatory read order, evidence rules, privacy boundaries, and cross-AI usage instructions. `AGENTS.md` must require reading `PROFILE.md`, `KNOWLEDGE_INDEX.md`, `TASK_STATE.md`, and the relevant topic page before acting.

- [ ] **Step 2: Create reusable templates**

Every knowledge/source card must contain `updated`, `status`, `confidence`, `sources`, `claims`, `unknowns`, and `next_review` fields. Project-state templates must distinguish completed work from pending or externally blocked work.

- [ ] **Step 3: Verify files are readable as UTF-8**

Run:

```powershell
Get-Content -Encoding UTF8 -TotalCount 20 README.md
Get-Content -Encoding UTF8 -TotalCount 40 AGENTS.md
```

Expected: Chinese text renders correctly and the read order is visible.

- [ ] **Step 4: Commit the foundation**

```powershell
git add README.md AGENTS.md AI_CONTEXT.md PROFILE.md IDENTITY.md KNOWLEDGE_INDEX.md TASK_STATE.md SECURITY.md .gitignore templates
git -c user.name=Codex -c user.email=codex@local commit -m "feat: scaffold portable knowledge vault"
```

### Task 2: Automated safety and structure validator

**Files:**
- Create: `scripts/validate_vault.py`
- Create: `tests/test_validate_vault.py`

**Interfaces:**
- Consumes: repository root path.
- Produces: `ValidationResult(errors: list[str], warnings: list[str], scanned_files: int)` and process exit `0` only when no errors exist.

- [ ] **Step 1: Write failing unit tests**

Tests must cover missing required root files, missing source metadata, broken local Markdown links, obvious secret assignments, allowed placeholder names such as `OPENAI_API_KEY`, and a valid minimal vault.

- [ ] **Step 2: Run tests and verify the RED state**

```powershell
python -m unittest tests.test_validate_vault -v
```

Expected: failure because `scripts.validate_vault` does not exist.

- [ ] **Step 3: Implement the validator**

Use only `dataclasses`, `pathlib`, `re`, and `sys`. Scan Markdown, JSON, TOML, YAML, and text files under the vault; skip `.git`. Treat assignments containing non-placeholder values for common secret names and private-key headers as errors. Check local Markdown links without attempting network access.

- [ ] **Step 4: Run focused and repository validation**

```powershell
python -m unittest tests.test_validate_vault -v
python scripts/validate_vault.py .
```

Expected: all unit tests pass and repository validation reports zero errors.

- [ ] **Step 5: Commit the validator**

```powershell
git add scripts/validate_vault.py tests/test_validate_vault.py
git -c user.name=Codex -c user.email=codex@local commit -m "test: validate knowledge vault safety"
```

### Task 3: Import the complete skills and requirements inventory

**Files:**
- Generate: `sources/codex-inventory/codex-inventory.md`
- Generate: `sources/codex-inventory/codex-inventory.json`
- Generate: `sources/codex-inventory/codex-skill-organization.md`
- Generate: `sources/codex-inventory/codex-skill-organization.json`
- Create: `knowledge/system/skills-and-routing.md`
- Create: `knowledge/system/user-requirements.md`

**Interfaces:**
- Consumes: `C:\Users\26014\Documents\技能\codex_inventory.py`, local skills, approved user instructions, and Codex memory metadata.
- Produces: searchable detailed inventory plus concise routing and user-requirement summaries.

- [ ] **Step 1: Verify the existing inventory tool**

```powershell
Set-Location 'C:\Users\26014\Documents\技能'
python -m unittest tests.test_codex_inventory -v
```

Expected: the existing inventory tests pass without installing dependencies.

- [ ] **Step 2: Generate reports directly into the vault**

```powershell
python codex_inventory.py --workspace . --display-workspace 'C:\Users\26014\Documents\技能' --out 'C:\Users\26014\Documents\知识库\sources\codex-inventory'
```

Expected: Markdown and JSON inventories are created; HTML reports are not committed because the portable vault prioritizes text and machine-readable data.

- [ ] **Step 3: Write the concise routing and requirements pages**

Summarize the primary skill groups, duplicate-skill rule, install-size policy, state-file policy, no-secret rule, Shopify authorization boundary, image workflow, social/outreach authorization boundary, and evidence-first reporting conventions.

- [ ] **Step 4: Validate and commit**

```powershell
python scripts/validate_vault.py .
git add sources/codex-inventory knowledge/system
git -c user.name=Codex -c user.email=codex@local commit -m "docs: import Codex skills and requirements"
```

### Task 4: Build the workspace and automation catalog

**Files:**
- Create: `scripts/build_workspace_inventory.py`
- Create: `tests/test_build_workspace_inventory.py`
- Generate: `sources/inventory/workspaces.json`
- Generate: `sources/inventory/automations.json`
- Generate: `sources/inventory/skills.json`
- Create: `knowledge/system/workspace-map.md`
- Create: `knowledge/system/automation-catalog.md`

**Interfaces:**
- Consumes: explicit allowlisted roots and metadata-only fields from state/config files.
- Produces: normalized JSON inventories with `name`, `path`, `updated`, `status`, and `evidence_files` fields.

- [ ] **Step 1: Write tests for safe metadata extraction**

Tests must prove that the scanner ignores hidden credential/config files, never reads environment variables, collects only allowlisted filenames, and redacts values matching secret assignment patterns.

- [ ] **Step 2: Implement and run the inventory builder**

The script must inventory `D:\codex`, `C:\Users\26014\Documents\独立站`, `中转站`, `节点`, `自媒体运营`, `技能`, `C:\Users\26014\.codex\skills`, and `C:\Users\26014\.codex\automations`. It may read automation `name`, `status`, `rrule`, and `cwds`, but not prompts or memory bodies.

- [ ] **Step 3: Generate current inventories**

```powershell
python scripts/build_workspace_inventory.py --output sources/inventory
```

Expected: three JSON files with no secret values and explicit missing/empty workspace states.

- [ ] **Step 4: Write human-readable catalogs and commit**

```powershell
python -m unittest tests.test_build_workspace_inventory -v
python scripts/validate_vault.py .
git add scripts/build_workspace_inventory.py tests/test_build_workspace_inventory.py sources/inventory knowledge/system
git -c user.name=Codex -c user.email=codex@local commit -m "feat: catalog workspaces and automations"
```

### Task 5: Distill reusable knowledge by domain

**Files:**
- Create: `knowledge/trade/foreign-trade-operations.md`
- Create: `knowledge/sites/independent-sites-and-shopify.md`
- Create: `knowledge/infrastructure/relay-and-node-operations.md`
- Create: `knowledge/media/self-media-operations.md`
- Create: `knowledge/distillation/content-distillation-system.md`
- Create: `knowledge/commerce/customer-first-product-research.md`
- Create: `projects/armorhue.md`
- Create: `projects/yufeng.md`
- Create: `projects/ai-global-trade-os.md`
- Create: `projects/self-media-distiller.md`
- Create: `projects/independent-site-research.md`

**Interfaces:**
- Consumes: current `TASK_STATE.md` files, `D:\codex\AGENTS.md`, Codex memory registry, and dated research artifacts.
- Produces: concise evidence-backed pages with current status, reusable rules, source paths, known blockers, and next review date.

- [ ] **Step 1: Write the seven domain knowledge pages**

Each page must separate durable methods from dated operational state. Provider endpoints may be named only when already public/non-secret; credential values and mailbox/customer records are excluded.

- [ ] **Step 2: Write project handoff pages**

Each project page must include scope, latest verified snapshot date, completed work, active blockers, evidence paths, authorization boundaries, and resume instructions.

- [ ] **Step 3: Update the knowledge index**

Link every domain and project page from `KNOWLEDGE_INDEX.md` using relative paths.

- [ ] **Step 4: Validate and commit**

```powershell
python scripts/validate_vault.py .
git add knowledge projects KNOWLEDGE_INDEX.md
git -c user.name=Codex -c user.email=codex@local commit -m "docs: distill cross-project operating knowledge"
```

### Task 6: Add the first video source and knowledge card

**Files:**
- Create: `sources/videos/douyin-7655909545654950769.md`
- Create: `knowledge/ai-workflows/portable-ai-brain.md`

**Interfaces:**
- Consumes: public Douyin page title, author, publication time, duration, chapter summaries, and source URL observed on 2026-08-04.
- Produces: one evidence card and one reusable method card without retaining the video binary.

- [ ] **Step 1: Write the source card**

Record the source URL, video id, title, author, publication time, duration, chapter timeline, evidence level, and the distinction between creator claims and verified platform-visible facts.

- [ ] **Step 2: Write the method card**

Translate the video into the repository's actual design: durable context files, source/knowledge separation, classification, ingestion, review, and optional future automation. Explicitly note that a local Obsidian folder alone does not provide cross-device AI access.

- [ ] **Step 3: Link, validate, and commit**

```powershell
python scripts/validate_vault.py .
git add sources/videos knowledge/ai-workflows KNOWLEDGE_INDEX.md
git -c user.name=Codex -c user.email=codex@local commit -m "docs: add first AI brain knowledge card"
```

### Task 7: Final acceptance and private-remote handoff

**Files:**
- Modify: `TASK_STATE.md`
- Create: `reports/acceptance-2026-08-04.md`

**Interfaces:**
- Consumes: all vault files and test results.
- Produces: a reproducible PASS/WATCH/FAIL report and exact private-GitHub handoff state.

- [ ] **Step 1: Run complete verification**

```powershell
python -m unittest discover -s tests -v
python scripts/validate_vault.py .
git status --short
git log --oneline --decorate -8
```

Expected: tests pass, validator reports zero errors, and only intentional acceptance/state edits remain.

- [ ] **Step 2: Write acceptance and current state**

Report counts for root documents, knowledge pages, project pages, source cards, inventories, skills, automations, validation errors, warnings, and remote status. Mark the remote as `NOT_CREATED` until the private repository exists and is read back as private.

- [ ] **Step 3: Commit acceptance**

```powershell
git add TASK_STATE.md reports/acceptance-2026-08-04.md
git -c user.name=Codex -c user.email=codex@local commit -m "docs: accept portable knowledge vault"
```

- [ ] **Step 4: Confirm external creation details**

At action time, confirm the exact repository name `personal-ai-knowledge-base`, owner account, and `Private` visibility before submitting the GitHub creation form. Do not create GitHub Pages.

- [ ] **Step 5: Create, push, and read back privacy**

Use the already logged-in GitHub browser session. After creation, verify the repository visibility is `Private`, add the HTTPS remote without embedding credentials, push `master`, and confirm the remote files are visible only while authenticated.
