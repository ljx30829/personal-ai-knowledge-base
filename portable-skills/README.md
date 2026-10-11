# Portable skills package

This directory contains a filtered, credential-screened snapshot of the current local skill trees.

The original `user-skills/` and `plugin-cache/` paths are preserved so the files can be restored to their expected Codex locations. Use `SKILL_CATALOG.md` to browse categories and `portable-skills-manifest.json` to verify hashes.

This package excludes selected domain-specific skill units and any files matching the configured sensitive-content filter. The source knowledge vault remains the place for project notes; this directory is only for executable skill files and their support assets.

The package is intended for the private repository only. Review platform and third-party licenses before redistributing it outside the owner account.

The snapshot contains 219 `SKILL.md` entrypoints and 2,389 manifest-tracked files. Run `python scripts/audit_portable_skills.py --bundle portable-skills` from the vault root before installation. The audit preserves upstream files: 61 entrypoints follow the current strict template, while 158 use loadable legacy or vendor metadata extensions and are reported as compatibility warnings rather than rewritten.
