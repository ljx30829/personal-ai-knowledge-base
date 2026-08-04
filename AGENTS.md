# Codex Knowledge Vault Instructions

This repository is the user's portable source of durable context.

## Required read order

Before starting work:

1. Read `PROFILE.md` for stable user preferences and constraints.
2. Read `KNOWLEDGE_INDEX.md` to locate the relevant domain page.
3. Read `TASK_STATE.md` for the current vault state.
4. Read the relevant file under `projects/` before changing or reporting on a project.
5. Read linked source cards when a claim depends on dated evidence.

## Operating rules

- Prefer persistent file state over chat history.
- Treat this vault as a summary and routing layer, not a replacement for the original project workspace.
- Preserve `PASS`, `WATCH`, `FAIL`, `BLOCKED`, and `UNVERIFIED` distinctions.
- Never invent contacts, interest, prices, specifications, certifications, analytics proof, permissions, platform state, deployment state, sends, or publication.
- Do not expose or store passwords, tokens, cookies, API keys, mailbox contents, browser profiles, or raw customer-sensitive records.
- Do not execute outreach, social actions, live Shopify changes, deployments, purchases, account changes, or external submissions without exact current authorization.
- Before installing packages, models, browsers, Docker images, or large dependencies, estimate download size, installed size, default location, and whether D: or E: can be used; ask first for large installs.
- When new durable knowledge is confirmed, update the relevant knowledge/project page, its source links, `KNOWLEDGE_INDEX.md`, and `TASK_STATE.md`.
- When evidence is incomplete or stale, say so and record the next verification needed.

## Source policy

- `knowledge/` contains reusable conclusions.
- `projects/` contains dated operational handoffs.
- `sources/` contains evidence summaries and machine-readable inventories.
- `inbox/` is unreviewed and must not be treated as verified knowledge.
- Original large artifacts stay at their recorded source paths unless the user explicitly asks to import them.

## Validation

Before committing meaningful changes, run:

```powershell
python scripts/validate_vault.py .
```

If the validator reports a possible secret, stop and inspect the exact file before committing.
