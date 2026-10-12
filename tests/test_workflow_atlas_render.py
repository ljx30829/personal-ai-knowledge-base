import json
from pathlib import Path
import tempfile
import unittest

from scripts.build_workflow_atlas import build_atlas
from scripts.validate_workflow_atlas import validate_atlas


class WorkflowAtlasRenderTests(unittest.TestCase):
    def test_offline_page_embeds_catalog_and_has_no_remote_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            build_atlas(Path('.'), out, revision='a' * 40)
            page = (out / 'index.html').read_text(encoding='utf-8')
            self.assertIn('data-skill-count="219"', page)
            self.assertIn('data-workflow-count="13"', page)
            self.assertNotIn('__ATLAS_', page)
            self.assertNotIn('fetch(', page)
            self.assertNotIn('<script src=', page)
            payload = page.split('<script id="atlas-data" type="application/json">')[1].split('</script>')[0]
            self.assertEqual(219, len(json.loads(payload)['skills']))
            self.assertEqual([], validate_atlas(Path('.'), out))
