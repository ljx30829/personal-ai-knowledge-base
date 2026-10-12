from pathlib import Path
import unittest

from scripts.workflow_atlas.archify import attach_model_lines, build_archify_candidate, build_overview_candidate
from scripts.workflow_atlas.taxonomy import load_workflows


class WorkflowAtlasArchifyTests(unittest.TestCase):
    def test_workflow_candidate_has_required_archify_shape_and_gated_edges(self):
        workflow = load_workflows(Path('.'))[0]
        candidate = build_archify_candidate(workflow, {'url': 'https://github.com/ljx30829/personal-ai-knowledge-base.git', 'revision': '0' * 40})
        candidate = attach_model_lines(candidate, Path('knowledge/system/workflow-purpose-model.json').read_text(encoding='utf-8'))
        self.assertEqual(2, candidate['schema_version'])
        self.assertEqual(f'{workflow.id}-purpose', candidate['mainPath'][0])
        self.assertEqual(f'{workflow.id}-state', candidate['mainPath'][-1])
        self.assertTrue(all(node['sources'][0]['line'] > 1 for node in candidate['nodes']))
        gates = [e for e in candidate['edges'] if e['from'].endswith('-authorize')]
        self.assertTrue(all(e.get('label') for e in gates))

    def test_overview_has_thirteen_independent_work_purposes(self):
        workflows = load_workflows(Path('.'))
        candidate = build_overview_candidate(workflows, {'url': 'https://github.com/ljx30829/personal-ai-knowledge-base.git', 'revision': '0' * 40})
        self.assertEqual(13, len([n for n in candidate['components'] if n['id'].startswith('purpose-')]))
        self.assertEqual(52, len(candidate['components']))
        self.assertEqual(39, len(candidate['connections']))
        # Every relationship stays within its own work purpose.
        for edge in candidate['connections']:
            self.assertEqual(edge['from'].split('-', 1)[1], edge['to'].split('-', 1)[1])
