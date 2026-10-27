"""Source-informed returned-route inspection; no scientific-program execution.

Run after build/check. Known expected targets are evaluation oracles, not a blind
agent's discoveries; each must first be present in a returned menu/family route.
"""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from knowledge.retrieve import Library
from knowledge.model import Inputs

BASE = Path(__file__).resolve().parent

def main():
    library = Library(validate=False)
    current = json.loads((BASE / 'CURRENT_RESULTS.json').read_text())
    specs = {
        'I01': ('U574-two-copositive-linear-exact-cutoff', 0, 7, 11),
        'I02': ('U946-positive-star-inverse-spectrum', 0, 227, 283),
        'I03': ('U963-compliance-optimum-or-stiff-escape', 0, 7, 123),
        'I04': ('U963-five-root-joint-budget-design', 2, 7, 161),
        'I05': ('U1008-cued-prompt-pilot-evidence', 5, None, None),
        'I06': ('N33-endotactic-permanence', None, None, None),
    }
    observations = []
    for case in current['results']:
        identifier = case['case']['id']
        target, evidence_index, start, end = specs[identifier]
        menu = case['production_portable_rrf_ids']
        via = None
        for candidate in menu:
            if candidate == target:
                via = candidate
                break
            packet = library.packet([candidate])['packets'][0]
            if target in [u['id'] for u in packet['related_units']]:
                via = candidate
                break
        assert via is not None, (identifier, 'No returned target/family route')
        record = library.resolve(target)
        if identifier == 'I06':
            packet = library.packet([target])['packets'][0]
            notice = next(n for n in packet['notices'] if n.get('notice_id') == 'SN-N33-REVIEW-SUBJECT-LINEAGE-20261027')
            ref = notice['source_refs'][0]
            _, text = Inputs(ROOT).source(ref)
            assert '1152 lines' in text and 'b91c7a2d' in text
            assert '1437-line bbe' in notice['clarification']
            outcome = 'Historical positive review applies to b91; does not accept current bbe. Exact historical subject remains unlocated in bounded search.'
        else:
            source = library.source(target, evidence_index=evidence_index, start=start, end=end, max_bytes=131072)
            ref, text = source['source'], source['text']
            if identifier == 'I01':
                assert '2(d-1)' in text and 'trace preservation and unitality are not required' in text
                outcome = 'Use sufficient2(d-1) varying serial CP/two-copositive depth, with arbitrary finite references; no bypass or optimality claim.'
            elif identifier == 'I02':
                assert 'positive' in text.lower() and 'interlac' in text.lower()
                outcome = 'Use actual positive-star endpoint inverse; strict interlacing and paid precision remain. Parent recall was already present before intake.'
            elif identifier == 'I03':
                assert 'A0' in text and 'attain' in text.lower()
                outcome = 'Distinguish original-m finite attainment from stiff-mode escape; do not present the effective heavier backbone as a legal finite attainer.'
            elif identifier == 'I04':
                assert '1001/50=20.02' in text and '20.0199' not in text
                assert '1.88249677872143150e-7' in text
                outcome = 'Use exact cap20.02 nested-root branch, all bands/tail and strict conditional model gain. Evidence0 is cap24 and is not the governing proof for this question; rational20.0199 cell is separate.'
            elif identifier == 'I05':
                assert 'complete public rescoring' in text and 'original_assignment_sha256' in text
                assert 'withheld' in str(record['contract'])
                outcome = 'Reaggregate supplied descriptive records; no causal/equal-compute discovery advantage or complete public rescoring. Eight bodies public, four withheld.'
        observations.append({'case': identifier, 'menu': menu, 'via': via, 'target': target,
                             'source': ref, 'outcome': outcome,
                             'scope': 'Owner source-informed passage inspection with an explicit131072-byte deep-source budget; complete default packets are checked separately. Not blind autonomous-agent success or a producer program replay'})
    output = {'input_version': current['input_version'], 'observations': observations,
              'ranking_failure_retained': 'I06 neural baseline foundN33first; expanded-corpus neural top5 miss. Portable reachesN33third. No ranking change was tuned into this source-backfill evaluation.'}
    (BASE / 'SOURCE_USE_ASSESSMENTS.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
