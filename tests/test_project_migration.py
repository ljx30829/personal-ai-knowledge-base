import json
import os
import tempfile
import unittest
from pathlib import Path

from scripts.build_project_inventory import scan_project, write_inventory
from scripts.build_project_manifest import build_manifest, should_exclude
from scripts.check_project_dependencies import inspect_project
from scripts.export_project_source import build_export, collect_files
from scripts.export_document_workspace import build_document_export


class ProjectMigrationTests(unittest.TestCase):
    def test_inventory_records_entrypoints_state_and_exclusion_without_reading_secret(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            (root / ".git").mkdir(parents=True)
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("print('ok')", encoding="utf-8")
            (root / "PROJECT_STATE.md").write_text("status: WATCH", encoding="utf-8")
            (root / ".env").write_text("API_KEY=never-read", encoding="utf-8")
            (root / ".env.example").write_text("API_KEY=", encoding="utf-8")

            result = scan_project(root)

            self.assertEqual("ACTIVE", result["status"])
            self.assertTrue(result["git"]["is_repo"])
            self.assertIn("PROJECT_STATE.md", result["state_files"])
            self.assertIn("src/main.py", result["entrypoints"])
            self.assertIn(".env", result["secret_candidates"])
            self.assertNotIn(".env.example", result["secret_candidates"])
            self.assertNotIn("never-read", json.dumps(result))

    def test_inventory_classifies_excluded_projects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ("Armor" + "Hue automotive" + "-film project")
            root.mkdir()
            result = scan_project(root)
            self.assertEqual("EXCLUDED", result["status"])
            self.assertTrue(result["exclusion_reason"])

    def test_dependency_inspection_only_reports_known_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"name":"demo"}', encoding="utf-8")
            (root / "pnpm-lock.yaml").write_text("lockfileVersion: 9", encoding="utf-8")
            (root / "pyproject.toml").write_text(
                "[project]\nname='demo'\nrequires-python='>=3.11'\n", encoding="utf-8"
            )
            (root / ".env").write_text("TOKEN=never-read", encoding="utf-8")

            result = inspect_project(root)
            paths = {item["path"] for item in result["dependency_files"]}

            self.assertEqual("PASS", result["status"])
            self.assertEqual({"package.json", "pnpm-lock.yaml", "pyproject.toml"}, paths)
            self.assertEqual("pnpm", result["package_manager"])
            self.assertNotIn("never-read", json.dumps(result))

    def test_dependency_inspection_ignores_descriptive_paths_but_flags_secret_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "setup-browser-cookies" / "SKILL.md"
            credential = root / "credentials" / "session.json"
            docs.parent.mkdir(parents=True)
            credential.parent.mkdir(parents=True)
            docs.write_text("public instructions", encoding="utf-8")
            credential.write_text("not-read", encoding="utf-8")
            (root / ".env").write_text("TOKEN=not-read", encoding="utf-8")

            result = inspect_project(root)

            self.assertNotIn("setup-browser-cookies/SKILL.md", result["secret_candidates"])
            self.assertIn("credentials/session.json", result["secret_candidates"])
            self.assertIn(".env", result["secret_candidates"])
            self.assertNotIn("not-read", json.dumps(result))

    def test_manifest_excludes_sensitive_and_domain_paths(self) -> None:
        self.assertEqual((True, "secret-name"), should_exclude(Path(".env")))
        self.assertEqual((False, None), should_exclude(Path(".env.example")))
        self.assertEqual((True, "excluded-domain"), should_exclude(Path("adult/research.md")))
        self.assertEqual((False, None), should_exclude(Path("src/main.py")))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("hello", encoding="utf-8")
            (root / ".env").write_text("TOKEN=never-copy", encoding="utf-8")
            output = Path(tmp) / "manifest.json"

            result = build_manifest(root, output)
            payload = json.loads(output.read_text(encoding="utf-8"))

            self.assertEqual(1, result["included_file_count"])
            self.assertEqual("src/main.py", payload["files"][0]["path"])
            self.assertGreater(len(payload["files"][0]["sha256"]), 32)
            self.assertNotIn("never-copy", output.read_text(encoding="utf-8"))

    def test_manifest_refuses_output_inside_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                build_manifest(root, root / "manifest.json")

    def test_source_export_is_dry_run_and_excludes_data_and_sensitive_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "distiller"
            (root / "src").mkdir(parents=True)
            (root / "tests").mkdir()
            (root / "accounts").mkdir()
            (root / "output").mkdir()
            (root / "src" / "main.py").write_text("print('ok')", encoding="utf-8")
            excluded_phrase = "automotive" + " film"
            (root / "src" / "example.py").write_text(f"topic = '{excluded_phrase}'", encoding="utf-8")
            (root / "tests" / "test_main.py").write_text("# test", encoding="utf-8")
            (root / "accounts" / "private.json").write_text("TOKEN=never-copy", encoding="utf-8")
            (root / "src" / ".env").write_text("API_KEY=never-copy", encoding="utf-8")
            output = Path(tmp) / "export"

            dry_run = build_export(root, output)
            self.assertEqual("DRY_RUN", dry_run["execution"])
            self.assertFalse(output.exists())
            self.assertEqual(3, dry_run["included_file_count"])
            self.assertIn("secret-name", dry_run["excluded_counts"])

            executed = build_export(root, output, execute=True)
            self.assertEqual("EXECUTED", executed["execution"])
            self.assertTrue((output / "src" / "main.py").is_file())
            self.assertIn("unrelated factory product", (output / "src" / "example.py").read_text(encoding="utf-8"))
            self.assertNotIn(excluded_phrase, (output / "src" / "example.py").read_text(encoding="utf-8"))
            self.assertTrue((output / "scripts" / "setup.ps1").is_file())
            self.assertTrue((output / "scripts" / "setup.sh").is_file())
            self.assertTrue((output / "DEPENDENCY_REPORT.json").is_file())
            self.assertTrue((output / "requirements.txt").is_file())
            self.assertTrue((output / "scripts" / "doctor.ps1").is_file())
            self.assertTrue((output / "scripts" / "verify_manifest.py").is_file())
            self.assertIn("__pycache__/", (output / ".gitignore").read_text(encoding="utf-8"))
            self.assertFalse((output / "accounts").exists())
            self.assertNotIn("never-copy", (output / "PROJECT_EXPORT_MANIFEST.json").read_text(encoding="utf-8"))

    def test_document_export_keeps_age_term_but_excludes_sensitive_domains(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "research"
            root.mkdir()
            (root / "TASK_STATE.md").write_text("18-24 Adult Trend Explorer", encoding="utf-8")
            (root / "brand.md").write_text("Candy" + ".ai benchmark", encoding="utf-8")
            (root / "secret.md").write_text("API_KEY=long-secret-value", encoding="utf-8")
            output = Path(tmp) / "export"

            result = build_document_export(root, output, execute=True)

            self.assertEqual(1, result["included_file_count"])
            self.assertTrue((output / "TASK_STATE.md").is_file())
            self.assertFalse((output / "brand.md").exists())
            self.assertFalse((output / "secret.md").exists())

    def test_inventory_writer_and_docs_are_wired(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            output = Path(tmp) / "inventory.json"
            payload = write_inventory([root], output)
            self.assertEqual(1, payload["project_count"])
            self.assertTrue(output.is_file())

        index = Path("KNOWLEDGE_INDEX.md").read_text(encoding="utf-8")
        readme = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("project-migration-toolkit.md", index)
        self.assertIn("project-migration-toolkit.md", readme)


if __name__ == "__main__":
    unittest.main()
