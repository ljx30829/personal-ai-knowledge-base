import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from scripts.export_portable_skills import collect_files, export_bundle
from scripts.install_portable_skills import install_bundle


class PortableSkillsTests(unittest.TestCase):
    def test_export_is_dry_run_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills = root / "skills"
            plugins = root / "plugins"
            output = root / "bundle"
            (skills / "demo").mkdir(parents=True)
            (skills / "demo" / "SKILL.md").write_text("# Demo\n", encoding="utf-8")

            result = export_bundle(skills, plugins, output, execute=False)

            self.assertEqual("DRY_RUN", result["status"])
            self.assertEqual(1, result["skill_file_count"])
            self.assertFalse(output.exists())

    def test_export_excludes_sensitive_and_generated_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills = root / "skills"
            plugins = root / "plugins"
            output = root / "bundle"
            demo = skills / "demo"
            demo.mkdir(parents=True)
            (demo / "SKILL.md").write_text("# Demo\n", encoding="utf-8")
            (demo / ".env").write_text("SECRET=value\n", encoding="utf-8")
            (demo / "session-token.txt").write_text("value\n", encoding="utf-8")
            (demo / "__pycache__").mkdir()
            (demo / "__pycache__" / "x.pyc").write_bytes(b"x")

            result = export_bundle(skills, plugins, output, execute=True)

            self.assertEqual("EXPORTED", result["status"])
            self.assertTrue((output / "user-skills" / "demo" / "SKILL.md").is_file())
            self.assertFalse((output / "user-skills" / "demo" / ".env").exists())
            self.assertFalse((output / "user-skills" / "demo" / "session-token.txt").exists())
            self.assertTrue((output / "portable-skills-manifest.json").is_file())

    def test_collect_prunes_link_like_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            real = root / "versioned" / "demo"
            alias = root / "latest"
            real.mkdir(parents=True)
            alias.mkdir(parents=True)
            (real / "SKILL.md").write_text("# Real\n", encoding="utf-8")
            (alias / "SKILL.md").write_text("# Duplicate\n", encoding="utf-8")

            original = Path.is_symlink

            def fake_is_symlink(path: Path) -> bool:
                return path == alias or original(path)

            with patch.object(Path, "is_symlink", fake_is_symlink):
                files, excluded = collect_files("user-skills", root)

            self.assertEqual(1, sum(item.source_path.name == "SKILL.md" for item in files))
            self.assertEqual(1, excluded["symlink-or-junction"])

    def test_install_skips_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_root = root / "source-skills"
            bundle = root / "bundle"
            target = root / "codex-home"
            source_skill = source_root / "demo" / "SKILL.md"
            source_skill.parent.mkdir(parents=True)
            source_skill.write_text("# New\n", encoding="utf-8")
            export_bundle(source_root, root / "empty-plugins", bundle, execute=True)
            existing = target / "skills" / "demo" / "SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("# Existing\n", encoding="utf-8")

            result = install_bundle(bundle, target, execute=True)

            self.assertEqual(1, result["conflicts_skipped"])
            self.assertEqual("# Existing\n", existing.read_text(encoding="utf-8"))

    def test_install_can_include_plugin_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plugin_root = root / "source-plugins"
            bundle = root / "bundle"
            target = root / "codex-home"
            plugin_skill = plugin_root / "pkg" / "skills" / "demo" / "SKILL.md"
            plugin_skill.parent.mkdir(parents=True)
            plugin_skill.write_text("# Plugin\n", encoding="utf-8")
            export_bundle(root / "empty-skills", plugin_root, bundle, execute=True)

            result = install_bundle(
                bundle,
                target,
                include_plugin_cache=True,
                execute=True,
            )

            self.assertEqual(1, result["installable_files"])
            self.assertTrue(
                (target / "plugins" / "cache" / "pkg" / "skills" / "demo" / "SKILL.md").is_file()
            )

    def test_install_rejects_tampered_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills = root / "source-skills"
            bundle = root / "bundle"
            skill = skills / "demo" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("# Original\n", encoding="utf-8")
            export_bundle(skills, root / "empty-plugins", bundle, execute=True)
            (bundle / "user-skills" / "demo" / "SKILL.md").write_text(
                "# Tampered\n", encoding="utf-8"
            )

            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                install_bundle(bundle, root / "codex-home", execute=False)


if __name__ == "__main__":
    unittest.main()
