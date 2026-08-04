import json
import os
import tempfile
import unittest
from pathlib import Path

from scripts.build_workspace_inventory import (
    build_automation_inventory,
    build_skill_inventory,
    build_workspace_inventory,
    write_inventories,
)


class BuildWorkspaceInventoryTests(unittest.TestCase):
    def test_workspace_inventory_uses_only_allowlisted_evidence_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            (root / "AGENTS.md").write_text("rules", encoding="utf-8")
            (root / "TASK_STATE.md").write_text("state", encoding="utf-8")
            (root / ".env").write_text(
                "OPENAI_API_KEY=should-never-be-read-or-copied", encoding="utf-8"
            )
            (root / "customer-export.csv").write_text("private", encoding="utf-8")

            result = build_workspace_inventory({"example": root})
            serialized = json.dumps(result, ensure_ascii=False)

            self.assertEqual(["AGENTS.md", "TASK_STATE.md"], result[0]["evidence_files"])
            self.assertNotIn(".env", serialized)
            self.assertNotIn("customer-export", serialized)
            self.assertNotIn("should-never", serialized)

    def test_missing_and_config_only_workspaces_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            config_only = base / "config-only"
            config_only.mkdir()
            (config_only / ".git").mkdir()

            result = build_workspace_inventory(
                {"config_only": config_only, "missing": base / "missing"}
            )
            by_name = {item["name"]: item for item in result}

            self.assertEqual("CONFIG_ONLY", by_name["config_only"]["status"])
            self.assertEqual("MISSING", by_name["missing"]["status"])

    def test_automation_inventory_ignores_prompt_and_memory_bodies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            automation = root / "daily"
            automation.mkdir()
            (automation / "automation.toml").write_text(
                '''id = "daily"
name = "Daily check"
prompt = "PASSWORD=never-copy-this-value"
status = "ACTIVE"
rrule = "FREQ=DAILY;BYHOUR=9"
cwds = ["D:\\\\codex"]
''',
                encoding="utf-8",
            )
            (automation / "memory.md").write_text(
                "COOKIE=another-private-value", encoding="utf-8"
            )

            result = build_automation_inventory(root)
            serialized = json.dumps(result, ensure_ascii=False)

            self.assertEqual("ACTIVE", result[0]["status"])
            self.assertEqual(["D:\\codex"], result[0]["cwds"])
            self.assertNotIn("prompt", serialized.lower())
            self.assertNotIn("never-copy", serialized)
            self.assertNotIn("memory.md", serialized)
            self.assertNotIn("another-private", serialized)

    def test_suspicious_values_in_allowed_fields_are_redacted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            automation = root / "daily"
            automation.mkdir()
            (automation / "automation.toml").write_text(
                '''name = "Daily API_KEY=unsafe-long-value"
status = "ACTIVE"
rrule = "FREQ=DAILY"
cwds = []
''',
                encoding="utf-8",
            )

            result = build_automation_inventory(root)
            serialized = json.dumps(result, ensure_ascii=False)

            self.assertNotIn("unsafe-long-value", serialized)
            self.assertIn("redacted", serialized)

    def test_skill_inventory_reads_metadata_not_skill_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "sample"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "# Sample\n\nTOKEN=private-skill-body-value\n", encoding="utf-8"
            )

            result = build_skill_inventory(root)
            serialized = json.dumps(result, ensure_ascii=False)

            self.assertEqual("sample", result[0]["name"])
            self.assertNotIn("private-skill-body", serialized)

    def test_write_inventories_does_not_include_environment_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            output = root / "output"
            sentinel = "environment-secret-sentinel-123"
            old_value = os.environ.get("INVENTORY_TEST_SECRET")
            os.environ["INVENTORY_TEST_SECRET"] = sentinel
            try:
                write_inventories(
                    output,
                    {"workspace": workspace},
                    root / "skills",
                    root / "automations",
                )
            finally:
                if old_value is None:
                    os.environ.pop("INVENTORY_TEST_SECRET", None)
                else:
                    os.environ["INVENTORY_TEST_SECRET"] = old_value

            combined = "\n".join(path.read_text(encoding="utf-8") for path in output.glob("*.json"))
            self.assertNotIn(sentinel, combined)


if __name__ == "__main__":
    unittest.main()
