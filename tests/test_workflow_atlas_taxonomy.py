import unittest
from pathlib import Path

from scripts.workflow_atlas.extract import load_skill_cards
from scripts.workflow_atlas.taxonomy import assign_workflows, group_duplicate_names, load_workflows


class WorkflowAtlasTaxonomyTests(unittest.TestCase):
    def test_taxonomy_has_exact_reviewed_purpose_ids(self):
        workflows = load_workflows(Path("."))
        self.assertEqual(tuple(item.id for item in workflows), (
            "market-research", "email-outreach", "sales-follow-up", "product-commerce",
            "site-commerce", "content-production", "content-distillation",
            "visual-experience", "software-delivery", "quality-assurance",
            "deployment-operations", "automation-agents", "knowledge-portability",
        ))

    def test_every_skill_has_at_least_one_route(self):
        workflows = load_workflows(Path("."))
        for card in load_skill_cards(Path(".")):
            self.assertTrue(assign_workflows(card, workflows))

    def test_same_name_different_source_is_reported_as_duplicate_group(self):
        groups = group_duplicate_names(load_skill_cards(Path(".")))
        self.assertTrue(all(len(ids) > 1 for ids in groups.values()))
