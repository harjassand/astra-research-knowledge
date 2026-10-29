"""Current human acceptance must not manufacture a proof audit or change inputs."""
import hashlib
import json
import unittest
from knowledge.model import ROOT, evidence_refs
from knowledge.retrieve import Library

ID='N675-complete-quantum-channel-information-order-undecidability'
BASE='research/2026-10-28-channel-programme-acceptance/source/'
STATUS='accepted_for_programme_use_by_harjas'
FULL='U675-complete-order-and-reference-cutoff'
NOTICE='SN-N675-HARJAS-PROGRAMME-ACCEPTANCE-20261028'


class ProgrammeAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_actual_authority_passage_is_acceptance_not_operational_status(self):
        record=self.library.resolve('N675')
        notice=next(n for n in record['notices']if n.get('notice_id')==NOTICE)
        index=next(i for i,r in enumerate(evidence_refs(notice))
                   if r['path']==BASE+'HUMAN_ACCEPTANCE_INSTRUCTION.txt')
        passage=self.library.source('N675',index,notice=NOTICE)['text']
        self.assertTrue(passage.startswith('DIRECT HUMAN SCIENTIFIC ACCEPTANCE —'))
        self.assertIn('CORRECT AND ACCEPTED',passage)
        self.assertIn('01a1820e-891f-75d1-a824-53e6c85b2e2e',passage)
        self.assertIn('not a new audit',passage)
        self.assertNotIn('LATEST LIVE RETRIEVAL CHECK',passage)
        self.assertTrue(notice['legacy_status_fields_are_historical'])
        self.assertEqual(notice['current_programme_status'],'CORRECT_AND_ACCEPTED')
        self.assertEqual(notice['current_scope_unit'],FULL)
        current=self.library.resolve(FULL)
        self.assertEqual(current['review']['acceptance'],STATUS)
        self.assertNotIn('gaps',current['review'])
        self.assertFalse(current['review']['new_audit'])
        self.assertFalse(record['review_overlays'])
        self.assertFalse(notice['new_audit'])
        self.assertIn({'id':ID,'content_version':record['content_version']},notice['accepted_subjects'])
        # The real coordinate correction survives the current authority change.
        self.assertIn('zeta=sum conjugate(v_alpha) Z_alpha',json.dumps(record['relationships']))

    def test_immutable_unit_successors_keep_statement_and_all_mathematical_inputs(self):
        for name in ('U675-edge-penalty','U675-ordered-word-compiler'):
            old_path=ROOT/f'knowledge/units/{name}/v0001.json'
            old=json.loads(old_path.read_bytes())
            second_path=ROOT/f'knowledge/units/{name}/v0002.json'
            second=json.loads(second_path.read_bytes())
            new=json.loads((ROOT/f'knowledge/units/{name}/v0003.json').read_bytes())
            self.assertEqual(second['previous'],hashlib.sha256(old_path.read_bytes()).hexdigest())
            self.assertEqual(new['previous'],hashlib.sha256(second_path.read_bytes()).hexdigest())
            self.assertEqual(new['statement'],old['statement'])
            for field in ('requires','provides','assumptions','costs','units'):
                self.assertEqual(new['contract'][field],old['contract'][field])
            self.assertEqual(new['evidence'][0],old['evidence'][0])
            current=self.library.resolve(name)
            self.assertEqual(current['version'],3)
            self.assertEqual(current['review']['acceptance'],STATUS)
            self.assertFalse(current['review']['new_audit'])
            self.assertFalse(current['review_overlays'])
            self.assertEqual([x['version']for x in current['history']],[1,2,3])
            # Read actual governing constructions,not the new authority excerpt.
            passage=self.library.source(name,0)['text']
            anchor=('Its zero set is exactly the desired edge recurrence'if name.endswith('edge-penalty')
                    else'Suffix closure preserves the declared noncommutative')
            self.assertIn(anchor,passage)

    def test_scope_originals_and_exact_previous_assessment_remain(self):
        record=self.library.resolve(FULL)
        self.assertIn('no equal-reference-marginal restriction',' '.join(record['contract']['assumptions']))
        self.assertIn('fixed input dimension',' '.join(record['contract']['assumptions']))
        self.assertIn('no efficiency',' '.join(record['contract']['costs']).lower())
        old=(ROOT/(BASE+'HISTORICAL_CARD_BEFORE_ACCEPTANCE.txt')).read_bytes()
        self.assertEqual(hashlib.sha256(old).hexdigest(),
                         '755ee83015b294fbaef1e7512527d10e579517e71c6ac0feefbec51b84a85753')
        self.assertIn(b'STATUS: source_derived_unreviewed',old)
        old_status=json.loads((ROOT/(BASE+'HISTORICAL_STATUS_BEFORE_ACCEPTANCE.json')).read_bytes())
        self.assertTrue(old_status['requires_external_validation'])
        for filename,expected in (
                ('channel_order_undecidability.pdf','e7ca558825f266d892ec1cedaac40ad33b3db3ecaf5ebd456ef70938cb4e127f'),
                ('EXTRACTED_TEXT.txt','8ca424ee229e68ed1e8833859d826ef243df44fba74e7927dd76e09cf714bb34')):
            path=ROOT/'updates/DG/package/channel_order_undecidability'/filename
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),expected)
        self.assertNotEqual(self.library.resolve('N661')['review']['reported_status'],STATUS)

    def test_checkpoint_pinned_card_and_status_remain_at_their_original_paths(self):
        for name in ('2026-10-11-channel-order-undecidability','2026-10-11-fixed-generator-order-classification'):
            checkpoint=json.loads((ROOT/f'state/checkpoints/theoretical-pro/{name}.json').read_bytes())
            pins=[r for r in checkpoint['evidence_refs']if '/N675-'in r['path']]
            self.assertTrue(pins)
            for ref in pins:
                self.assertEqual(hashlib.sha256((ROOT/ref['path']).read_bytes()).hexdigest(),ref['sha256'])
        definition=self.library.source(FULL,0)
        self.assertIn('Definition 1.1.',definition['text'])
        self.assertIn('no restriction requiring equal reference marginals',definition['text'])
        # The operation definition is now the first citation. Preserve the
        # actual classification theorem route as a separate scoped premise;
        # neither citation is presumed to prove every part of the unit.
        record=self.library.resolve(FULL)
        theorem_index=next(i for i,ref in enumerate(record['evidence'])
                           if ref.get('quote')=='Theorem 1.2 (Main theorem).')
        proof=self.library.source(FULL,theorem_index)
        self.assertIn('Theorem 1.2 (Main theorem).',proof['text'])
        self.assertIn('no restriction requiring equal reference marginals',proof['text'])


if __name__=='__main__':unittest.main()
