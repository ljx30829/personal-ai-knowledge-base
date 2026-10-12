import unittest

from scripts.workflow_atlas.models import SkillCard, SourceRef, stable_id, to_jsonable


class WorkflowAtlasModelTests(unittest.TestCase):
    def test_stable_id_distinguishes_same_name_from_different_sources(self):
        left = stable_id("user-skills", "alpha/SKILL.md", "review")
        right = stable_id("plugin-cache", "pkg/skills/review/SKILL.md", "review")
        self.assertNotEqual(left, right)
        self.assertEqual(left, stable_id("user-skills", "alpha/SKILL.md", "review"))

    def test_skill_card_serializes_required_fields(self):
        card = SkillCard(
            id="user-skills-review-a1b2c3d4", name="review", source="user-skills",
            purpose="Review a change before landing.",
            when_to_use=("Before merging a change.",), inputs=("Repository diff",),
            logic=("Inspect evidence before making a finding.",),
            outputs=("Prioritized findings",), dependencies=(), approval_gate="read-only",
            validation=("Every finding has a source location.",),
            failure_modes=("Missing diff keeps the card UNVERIFIED.",),
            workflow_ids=("quality-assurance",),
            source_paths=(SourceRef("portable-skills/user-skills/review/SKILL.md"),),
            completeness="PASS", missing_fields=(), content_sha256="0" * 64,
        )
        payload = to_jsonable(card)
        self.assertEqual(["quality-assurance"], payload["workflow_ids"])
        self.assertEqual("PASS", payload["completeness"])
