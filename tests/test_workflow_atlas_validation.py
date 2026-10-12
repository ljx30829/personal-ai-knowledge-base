import json
from pathlib import Path
import tempfile
import unittest

from scripts.build_workflow_atlas import build_atlas
from scripts.validate_workflow_atlas import validate_atlas


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
