import tempfile
import unittest
from pathlib import Path

from scripts.validate_vault import validate_vault


REQUIRED_ROOT_FILES = (
    "README.md",
    "AGENTS.md",
    "AI_CONTEXT.md",
    "PROFILE.md",
    "IDENTITY.md",
    "KNOWLEDGE_INDEX.md",
    "TASK_STATE.md",
    "SECURITY.md",
)


def make_minimal_vault(root: Path) -> None:
    for name in REQUIRED_ROOT_FILES:
        (root / name).write_text(f"# {name}\n", encoding="utf-8")
    source_dir = root / "sources" / "example"
    source_dir.mkdir(parents=True)
    (source_dir / "source.md").write_text(
        """---
updated: 2026-08-04
status: VERIFIED
confidence: HIGH
sources:
  - https://example.com
next_review: 2026-09-04
---

# Source
""",
        encoding="utf-8",
    )


class ValidateVaultTests(unittest.TestCase):
    def test_valid_minimal_vault_has_no_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_minimal_vault(root)

            result = validate_vault(root)

            self.assertEqual([], result.errors)
            self.assertGreaterEqual(result.scanned_files, len(REQUIRED_ROOT_FILES) + 1)

    def test_missing_required_root_file_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_minimal_vault(root)
            (root / "PROFILE.md").unlink()

            result = validate_vault(root)

            self.assertTrue(any("PROFILE.md" in item for item in result.errors))

    def test_source_markdown_requires_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_minimal_vault(root)
            (root / "sources" / "example" / "source.md").write_text(
                "# Missing metadata\n", encoding="utf-8"
            )

            result = validate_vault(root)

            self.assertTrue(any("metadata" in item.lower() for item in result.errors))

    def test_broken_relative_markdown_link_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_minimal_vault(root)
            (root / "README.md").write_text(
                "# Home\n\n[Missing](knowledge/missing.md)\n", encoding="utf-8"
            )

            result = validate_vault(root)

            self.assertTrue(any("broken link" in item.lower() for item in result.errors))

    def test_obvious_secret_assignment_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_minimal_vault(root)
            (root / "notes.txt").write_text(
                "OPENAI_API_KEY=sk-live-example-secret-value-123456\n",
                encoding="utf-8",
            )

            result = validate_vault(root)

            self.assertTrue(any("possible secret" in item.lower() for item in result.errors))

    def test_secret_variable_names_without_values_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_minimal_vault(root)
            (root / "README.md").write_text(
                "Use `OPENAI_API_KEY` or `$env:OPENAI_API_KEY`; never store its value.\n",
                encoding="utf-8",
            )

            result = validate_vault(root)

            self.assertEqual([], result.errors)


if __name__ == "__main__":
    unittest.main()
