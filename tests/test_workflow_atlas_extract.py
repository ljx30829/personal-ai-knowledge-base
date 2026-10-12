import json
from pathlib import Path
import tempfile
import unittest

from scripts.workflow_atlas.extract import load_skill_cards
from scripts.workflow_atlas.markdown import parse_frontmatter


class SkillExtractionTests(unittest.TestCase):
    def test_folded_description_is_read_completely(self):
        text = "---\nname: mail-helper\ndescription: >-\n  Draft mail.\n  Use before outreach.\n---\n# Mail\n"
        self.assertEqual(parse_frontmatter(text), {
            "name": "mail-helper", "description": "Draft mail. Use before outreach."
        })

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
            (root / "portable-skills").mkdir(exist_ok=True)
            (root / "portable-skills/SKILL_CATALOG.json").write_text(json.dumps(catalog), encoding="utf-8")
            cards = load_skill_cards(root)
            self.assertEqual(1, len(cards))
            self.assertEqual("demo", cards[0].name)
            self.assertEqual(("Read input.", "Validate output."), cards[0].logic)
