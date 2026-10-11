# Knowledge Vault Task State

## 2026-10-11 Complete Portable Recovery

- STATUS: `PASS_PRIVATE_REMOTES_AND_RECOVERY_ENTRYPOINT_READY`.
- KNOWLEDGE: This Private repository includes the durable vault, the filtered portable skill bundle, project inventory, integrity tools, and cross-platform bootstrap scripts.
- SOURCE_PROJECT: `https://github.com/ljx30829/account-knowledge-distiller`, Private, `master`, commit `41a53041d32b063b5d97744ca33af3cdbc92b354`; 62 reviewed files; manifest verification and `118/118` tests pass after extraction.
- RESEARCH_PROJECT: `https://github.com/ljx30829/independent-site-research-vault`, Private, `master`, commit `74f6cbc80cd2c10a3c6cdcab6a20a908973f8da1`; 23 reviewed files.
- LOCAL_BACKUP: Source ZIP `D:\codex\output\self-media-source-export-20261011-complete2.zip`, SHA-256 `6B1DC3D4269E59FF79661737B74ADF4E343F0524B0BD7E0DF5949E40A2122CD7`; research ZIP `D:\codex\output\independent-site-research-export-20261011-clean.zip`, SHA-256 `78152A3F794A4EF6F20981060AE20EA490351D6DDF6C0883C0B6259E42F428A8`.
- RESTORE: Run `scripts/bootstrap_portable_workspace.ps1` first without `-Execute`, then with `-Execute`; it restores both project repositories, audits and installs reviewed user/plugin skills without overwriting existing files, and runs source tests.
- SKILL_AUDIT: `219` entrypoints are readable and contain required metadata; `61` match the current strict template and `158` retain loadable legacy/vendor extensions. The manifest covers `2389/2389` files and the bootstrap restores both source trees.
- EXCLUDED: User-declared excluded brands, product domains, and content categories are absent from the published current tree. Credentials, sessions, account data, browser profiles, media, caches, and generated output are not included.
- LIMIT: External accounts, API access, cookies, servers, databases, domains, and deployments require fresh authorization and are not restored by Git.

## 2026-10-11 Project Migration Toolkit

- STATUS: `PASS_TOOLKIT_VERIFIED`.
- TOOLS: Added project inventory, dependency inspection, SHA-256 manifests, source-only export, document-only export, doctor, smoke test, and complete workspace bootstrap commands.
- VERIFY: Vault tests `30/30`; vault validator `errors=0 warnings=0`; project remote tree review found no excluded or generated paths.

## 2026-08-04 Reproducibility Expansion

- REVIEW: `APPROVED_FOR_PACKAGING`; the user replied "可以打包" on 2026-08-04. The approved review is `reports/full-knowledge-requirements-review-2026-08-04.md`.
- STATUS: `PASS_PACKAGED_AND_SYNCED_PRIVATE`.
- GOAL: Build a private, zero-subscription, cross-device Markdown knowledge base for the user's Codex work and long-term requirements.
- COMPLETED: Root navigation, Codex and vendor-neutral AI entry points, safety rules, templates, skills/requirements inventory, workspace/automation/skill catalogs, 21 knowledge pages including 10 detailed execution/recovery guides, five project handoffs, and the first Douyin source card.
- COVERAGE: Foreign trade, ExcludedBrand, Shopify/independent sites, Yufeng, relay/node operations, skills, automations, self-media, content distillation, customer-first research, and portable AI workflow.
- VERIFICATION: Vault tests `18/18 PASS`; validator `scanned_files=50 errors=0 warnings=0`; `git diff --check` clean; 21 knowledge pages; long-term requirement IDs are continuous through `R-170`. The assembled package manifest had `2529` entries; short-path extraction verified `missing=0` and `hash_mismatch=0`.
- INVENTORY: `251` skills, `1569` requirement entries, `186` local skill definitions, `10` automation directories, and `6` tracked workspaces.
- PORTABILITY: The skill bundle was exported to `D:\codex\output\personal-ai-knowledge-package-20260804-230623\portable-skills`: `2468` files, `251` skills, `108369128` bytes. Full manifest verification passed `2468/2468`; high-risk pattern review classified all 13 matched files as test fixtures or documented placeholders/environment examples.
- PACKAGE: `D:\codex\output\personal-ai-knowledge-package-20260804-230623.zip` contains `knowledge-vault/`, `portable-skills/`, and `package-manifest.json`. Extract to a short Windows path such as `D:\AIKB` to avoid legacy 260-character limits in deep plugin-cache paths.
- REMOTE: `PRIVATE_REMOTE_VERIFIED_CURRENT`; the reproducibility expansion was pushed to `https://github.com/ljx30829/personal-ai-knowledge-base` on `master` as commit `b4e8686`. The repository was authenticated as Private and GitHub Pages was not enabled.
- SAFETY: No passwords, tokens, cookies, API keys, browser profiles, mailbox contents, or raw customer-sensitive records were intentionally imported. Generated automation inventory excludes prompts and memory bodies.
- CURRENT VIEW: Open `README.md` or `KNOWLEDGE_INDEX.md` locally, or open `https://github.com/ljx30829/personal-ai-knowledge-base` while signed in to the authorized GitHub account.
- NEXT: On another device, clone the private repository for the Markdown vault. To restore the full local skill bundle as well, copy the ZIP and follow `knowledge-vault/README.md` plus the skills portability guide.

## Source Truth

- Durable reusable methods live under `knowledge/`.
- Dated operating state and resume instructions live under `projects/`.
- Large artifacts and sensitive operational records stay in their original workspaces.
- Relay/node status is historical and requires live revalidation; AI Global Trade OS is local-only and has an existing dirty worktree that must be preserved.
