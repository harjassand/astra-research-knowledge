"""Negative guards against intake-specific evidence inflation and route loss."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ei_validate', HERE/'validate.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)
manifest = json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
entry = json.loads((HERE/'CLAIMS.json').read_text())['claims'][0]


class EvidenceGuards(unittest.TestCase):
    def test_all_page_routes_and_original_boundary(self):
        derived = copy.deepcopy(manifest['derived_extractions'][0])
        text = (intake.ROOT/derived['path']).read_text()
        intake.check_page_map(derived,text)
        derived['page_map'][2]['lines'][0] += 1
        with self.assertRaisesRegex(ValueError,'page mapping'):
            intake.check_page_map(derived,text)

    def test_timestamp_is_not_inference_telemetry(self):
        trace = intake.load(entry['workflow_trace'])
        intake.check_unknown_workflow(trace)
        trace['resources']['reported_inference_seconds'] = 1
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_unknown_workflow(trace)

    def test_candidate_cannot_be_promoted_by_archive_checks(self):
        status = intake.load('frontier/cards/'+entry['id']+'.json')
        intake.check_status(status)
        status['claim_status'] = 'externally_verified'
        with self.assertRaisesRegex(ValueError,'promotion'):
            intake.check_status(status)

    def test_topical_similarity_is_not_a_proof_dependency(self):
        status = intake.load('frontier/cards/'+entry['id']+'.json')
        status['depends_on'].append({'target':'N593-chebyshev-signed-particle-fast-forwarding-obstruction','scope':'both mention fast forwarding'})
        with self.assertRaisesRegex(ValueError,'dependency'):
            intake.check_status(status)

    def test_family_route_is_not_theorem_application(self):
        fit = intake.load('updates/EI/FAMILY_FIT.json')
        intake.check_family_fit(fit)
        fit['comparisons'][0]['relation'] = 'proof_dependency'
        with self.assertRaisesRegex(ValueError,'dependency'):
            intake.check_family_fit(fit)


if __name__ == '__main__':
    unittest.main()
