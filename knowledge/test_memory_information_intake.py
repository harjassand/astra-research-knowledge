"""Guard actual source branches, review scopes and incompatible transfers."""
import json
import unittest
from knowledge.model import ROOT, digest
from knowledge.retrieve import Library


class MemoryInformationIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library(ROOT, validate=False)

    def passage(self, identifier, index=0):
        ref = self.library.resolve(identifier)['evidence'][index]
        data = (ROOT / ref.get('read_path', ref['path'])).read_bytes()
        self.assertEqual(digest(data), ref['sha256'])
        a, b = ref['lines']
        return '\n'.join(data.decode().splitlines()[a-1:b])

    def test_actual_stability_passage_contains_the_import_and_thermal_exclusion(self):
        text = self.passage('U1228-check-soundness-to-qualified-zero-temperature-stability')
        self.assertIn('Yin', text)
        self.assertIn('weighted local norm', text)
        self.assertIn('zero-temperature spectral-stability', text)
        self.assertIn('does not prove a finite-temperature perturbed memory lifetime', text)
        # Previously exposed wrong-range citation: the criterion precedes the example.
        krylov = self.passage('U1220-invariant-krylov-predictive-alternative')
        self.assertIn('## 6. A sufficient structural alternative', krylov)
        self.assertIn('D preserves', krylov)

    def test_midpoint_source_keeps_the_actual_operation_and_timing_contract(self):
        text = self.passage('U1225-midpoint-operation-and-precision-debit')
        for condition in ('true microscopic involution', 'pi Theta=pi', '2 Lambda kappa',
                          'conditioning on a realized', 'No native measurements'):
            self.assertIn(condition, text)
        noise = self.passage('U1221-optical-calibration-does-not-identify-memory-noise')
        self.assertIn('UNEXECUTED', noise)
        self.assertIn('leaves original optical qubit', noise)

    def test_completed_reviews_remain_at_their_actual_subject_versions(self):
        accepted = []
        for record in self.library.records.values():
            if not record['id'].startswith(tuple('U'+str(n)+'-' for n in range(1221,1230))):
                continue
            for review in record['review_overlays']:
                self.assertEqual(review['decision'], 'accepted_internally_verified')
                self.assertIn({'id':record['id'], 'content_version':record['content_version']}, review['subjects'])
                self.assertEqual(review['physical_measurement'], 'not established')
                accepted.append(record['id'])
        self.assertEqual(len(accepted), 16)
        for record in self.library.records.values():
            if record['id'].startswith('U1228-'):
                original=ROOT/'knowledge/units'/record['id']/'v0001.json'
                revised=json.loads((original.parent/'v0002.json').read_bytes())
                self.assertEqual(revised['previous'],digest(original.read_bytes()))
                self.assertEqual(revised['statement'],json.loads(original.read_bytes())['statement'])
                self.assertIn('distinct original receipt was not identified',json.loads(original.read_bytes())['body'])
                self.assertNotIn('distinct original receipt was not identified',record['body'])
                self.assertIn('one available whole-chain review plus supplement',record['body'])
        provisional = self.library.resolve('U1226-smooth-clock-extension-proposal')
        self.assertEqual(provisional['review_overlays'], [])
        self.assertIn('provisional', provisional['review']['acceptance'])
        self.assertEqual(self.library.resolve('U1223-root-capacity-saturation-report')['review_overlays'], [])
        foundation = self.library.resolve('N675')
        self.assertEqual(foundation['content_version'], '31d54f0ee3c87b122810e4d837733ab6b39f9a5f8570e9a7624d2a0fd695d19a')
        self.assertTrue(foundation['current_acceptance'])
        self.assertNotIn('current_acceptance', self.library.resolve('N661'))

    def test_typed_connections_bind_only_the_named_component_and_same_task(self):
        name='B1229-accepted-complete-order-to-pair-localizer'
        edge=json.loads((ROOT/'knowledge/transfers'/f'{name}.json').read_bytes())
        for side in ('from','to'):
            self.assertEqual(edge[side+'_version'],self.library.resolve(edge[side])['content_version'])
        self.assertIn('no equal-reference-marginal', edge['slot_binding']['reference_scope'])
        self.assertIn('Only the accepted equivalence component', edge['slot_binding']['qualification'])
        task=json.loads((ROOT/'knowledge/transfers/B1229-decision-gap-to-qualified-task-bound.json').read_bytes())
        self.assertEqual(task['slot_binding']['lower'], '1/640')
        self.assertEqual(task['slot_binding']['upper'], '1/640')
        self.assertIn('not relative entropy', task['slot_binding']['units'])
        self.assertIn('No moment-family', task['slot_binding']['qualification'])
        self.assertIn('357/640', self.passage('U1229-entropy-order-not-every-decision-loss'))

    def test_original_download_gaps_and_provisional_versions_remain_explicit(self):
        record=self.library.resolve('U1227-last-erasure-causal-cut-service-report')
        self.assertEqual(record['review_overlays'], [])
        ref=record['evidence'][0]
        self.assertEqual(ref['hash_kind'], 'rendered_ui_text_bytes_not_original')
        self.assertIn('not acquired original proof bytes', ref['range_scope'])
        notices=self.library.resolve('N1226')['notices']
        revision=next(n for n in notices if n.get('kind')=='source_revision')
        self.assertNotEqual(revision['previous_source']['sha256'], revision['current_source']['sha256'])
        self.assertIn('not_accepted', revision['status'])


if __name__=='__main__':
    unittest.main()
