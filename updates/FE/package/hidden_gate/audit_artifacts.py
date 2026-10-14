"""Replay certificates from recorded public inputs and query transcripts."""
from pathlib import Path
from fractions import Fraction
import json
from probe import soft_east
from certify import certify_run

ROOT = Path(__file__).resolve().parent

def main() -> None:
    data = json.loads((ROOT / 'final_results.json').read_text())
    checked = 0
    rows = []
    for entry in data['results']:
        model = soft_east(entry['L'], entry['q'], entry['softness'], entry['seed'])
        public = {key: value for key, value in model.items() if key not in ('fac', 'order')}
        for item in entry['runs']:
            cert = certify_run(public, item['run'])
            lower = Fraction(int(cert['exact_lower_numerator']), int(cert['exact_lower_denominator']))
            upper = Fraction(int(cert['exact_upper_numerator']), int(cert['exact_upper_denominator']))
            assert 0 < lower <= upper
            assert upper / lower <= Fraction(11, 10)
            assert item['run']['queries'] == len(item['run']['selected_edges'])
            assert item['run']['queries'] == len(item['run']['observed_facilitations'])
            assert len(set(item['run']['selected_edges'])) == item['run']['queries']
            checked += 1
            rows.append({'q': entry['q'], 'softness': entry['softness'], 'seed': entry['seed'],
                         'policy': item['run']['policy'], 'queries': item['run']['queries'],
                         'replayed_lower': cert['certified_lower'],
                         'replayed_upper': cert['certified_upper'],
                         'replayed_ratio_upper': cert['certified_upper_lower_ratio']})
    result = {'status': 'PASS', 'canonical_settings': len(data['results']),
              'transcript_certificates_replayed': checked,
              'scope': 'Same-session independent residual-verifier replay, not external review.',
              'results': rows}
    (ROOT / 'audit_results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps({key: value for key, value in result.items() if key != 'results'}, indent=2))

if __name__ == '__main__':
    main()
