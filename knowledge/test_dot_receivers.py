"""Scope regressions for the fixed quantum receiver intake.

These checks protect model/access/cost distinctions, not the truth of a theorem.
Finite scientific receiver replay is recorded separately in validation/.
"""
import json
import unittest
from pathlib import Path
from knowledge.model import ROOT, Inputs, evidence_refs

class DotReceiverBoundaries(unittest.TestCase):
    def test_all_registered_passages_have_their_exact_frozen_bytes(self):
        inputs=Inputs(ROOT)
        statuses=[json.loads(line) for line in (ROOT/'frontier/CURRENT_CLAIM_STATUS.d/2026-10-27-dot-receivers.jsonl').read_text().splitlines()]
        self.assertEqual(len(statuses),8)
        for status in statuses:
            for reference in evidence_refs(status):
                inputs.source(reference)

    def test_mixed_flag_access_lower_bounds_keep_different_scopes(self):
        r=ROOT/'research/2026-10-27-dot-scientific/source/quantum_operational_certification_20261024'
        physical=(r/'mixed_flag_haar_collision_independent_audit.md').read_text()
        retry=(r/'known_probe_to_choi_retry_reduction.md').read_text()
        choi=(r/'joint_flag_rank_signal_all_p_choi_corollary.md').read_text()
        self.assertIn('bounded definite-causal adaptive physical-query extension',physical)
        self.assertIn('n>=3r²/(65536p²)-4log(32/p)-1/6',retry)
        self.assertIn('retained UNKNOWN quantum memory',retry)
        self.assertIn('9r²/(32768p²)',choi)
        unit=json.loads((ROOT/'knowledge/units/U1104-latent-flag-adaptive-collision/v0001.json').read_text())
        self.assertIn('integer r>=2 and0<zeta<1',unit['statement'])
        self.assertIn('separate all-real-p Choi component allows integer r>=1',unit['contract']['requires'][0])

    def test_finite_receiver_error_tradeoffs_remain_distinct(self):
        r=ROOT/'research/2026-10-27-dot-scientific/source/quantum_operational_certification_20261024'
        partial=(r/'noise_adapted_quadratic_training_receiver.md').read_text()
        full=(r/'full_throughput_noise_adapted_quadratic_receiver.md').read_text()
        self.assertIn('eps p+50epsilon_ent',partial)
        self.assertIn('(p/9 id,(1-p/9) erasure)',partial)
        self.assertIn('19800epsilon_ent+37p xi',full)
        self.assertIn('2*10^9 S²/xi+36Lrm',full)

    def test_replay_distinguishes_support_failure_from_received_asymptotics(self):
        report=json.loads((ROOT/'research/2026-10-27-dot-scientific/validation/receiver-replay.json').read_text())
        rows={row['script']:row for row in report['results']}
        self.assertTrue(all(row['returncode']==0 for row in rows.values()))
        changed=rows['mixed_flag_three_program_support_change_check.py']['stdout']
        self.assertIn('conditional_chi=2.22222222222',changed)
        self.assertIn('linear_candidate=2.25',changed)
        self.assertIn('2400',rows['rare_spectral_filter_check.py']['stdout'])

    def test_support_change_display_stays_a_finite_diagnostic(self):
        parent=next((ROOT/'cards').glob('N1107-*.txt')).read_text()
        self.assertIn('approximately2.22222222222',parent)
        self.assertIn('not a certified enclosure',parent)
        self.assertNotIn('gives20/9',parent)
        notices=[json.loads(line) for line in (ROOT/'agent/SEMANTIC_NOTICES.d/2026-10-27-dot-receivers.jsonl').read_text().splitlines()]
        old=next(n for n in notices if n['notice_id']=='S1107-dot-diagnostics-and-failed-extrapolation')
        correction=next(n for n in notices if n['notice_id']=='S1107-dot-support-diagnostic-numeric-correction')
        self.assertIn('returns20/9',old['clarification'])
        self.assertEqual(correction['correction_of_notice_id'],old['notice_id'])
        self.assertIn('no exact20/9 certificate',correction['clarification'])
        review=json.loads((ROOT/'knowledge/reviews/A1152-dot-receiver-support-diagnostic.json').read_text())
        self.assertEqual([s['id'] for s in review['subjects']],['N1107-program-access-support-and-transported-projection-obstructions'])

    def test_overlap_is_not_an_entropy_transfer(self):
        unit=json.loads((ROOT/'knowledge/units/U1103-paired-parity-overlap-charge/v0001.json').read_text())
        self.assertIn('No beta-from-Delta inference',unit['statement'])
        self.assertIn('NOT inferred from mixed-success Delta',unit['contract']['assumptions'][0])

if __name__=='__main__': unittest.main()
