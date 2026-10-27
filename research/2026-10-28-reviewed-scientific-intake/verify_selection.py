"""Read-only public source-selection and supplied-record arithmetic checks.

Never imports or executes archived scientific/collector code; no network calls.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
METHOD = ROOT / 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-method-tranche-originals'

def load(path):
    return json.loads(path.read_text())

def verify():
    ledger = load(METHOD / 'PUBLIC_SELECTION.json')
    index = load(METHOD / 'source/INDEX.json')
    assert len(index['files']) == 39
    assert sum(e['kind'] == 'frozen_original' for e in index['files']) == 33
    declared = set()
    for entry in index['files']:
        path = METHOD / entry['path']
        data = path.read_bytes()
        assert len(data) == entry['bytes'], str(path)
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], str(path)
        declared.add(path.relative_to(ROOT).as_posix())
    assert len(ledger['original_files']) == 57
    assert Counter(e['selection'] for e in ledger['original_files']) == {
        'unchanged_public_original': 33, 'private_original_retained': 24}
    for entry in ledger['original_files']:
        path = ROOT / entry['path']
        if entry['selection'] == 'private_original_retained':
            assert not path.exists(), str(path)
            assert entry['path'] not in declared
        else:
            assert entry['path'] in declared
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256']
    pilot = load(METHOD / 'source/selected/pilot_numeric_records.json')
    rows = pilot['records']
    ids = {r['response_id'] for r in rows}
    assert len(rows) == len(ids) == 12
    assert Counter(r['arm'] for r in rows) == {'A': 6, 'B': 6}
    assert Counter(r['task_id'] for r in rows) == {'T1': 4, 'T2': 4, 'T3': 4}
    assert sum(r['response_body_public'] for r in rows) == 8
    by_id = {r['response_id']: r for r in rows}
    score_totals = {}
    expected = {'blind_scores.json': {'A': 44, 'B': 47},
                'auditor_scores.json': {'A': 45, 'B': 47}}
    for name, totals in expected.items():
        scores = load(METHOD / 'source/originals/review' / name)
        scores = scores.get('scores', scores.get('responses'))
        assert len(scores) == 12 and {s['response_id'] for s in scores} == ids
        result = {'A': 0, 'B': 0}
        for score in scores:
            record = by_id[score['response_id']]
            assert score['task_id'] == record['task_id']
            assert 0 <= score['total'] <= 8
            if 'output_sha256' in score:
                assert score['output_sha256'] == record['output_sha256']
            result[record['arm']] += score['total']
        assert result == totals
        score_totals[name] = {a: str(Fraction(t, 6)) for a, t in result.items()}
    usage = {k: sum(r['runtime_token_counter'][k] for r in rows) for k in
             ('input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens')}
    assert usage == {'input_tokens': 831935, 'cached_input_tokens': 779136,
                     'output_tokens': 15564, 'reasoning_output_tokens': 11289}
    assert usage['input_tokens'] + usage['output_tokens'] == 847499
    for row in rows:
        assert row['runtime_token_counter']['reasoning_output_tokens'] <= row['runtime_token_counter']['output_tokens']
        for kind, ext in [('prompts', '.txt'), ('responses', '.json')]:
            path = METHOD / f"source/originals/experiment/{kind}/{row['response_id']}{ext}"
            assert path.exists() == row['response_body_public']
    trajectory_path = METHOD / 'source/selected/trajectory_scientific_evidence.json'
    trajectory = load(trajectory_path)
    assert trajectory['selected_scientific_passages'] == 28
    assert sum(len(e['evidence']) for e in trajectory['episodes']) == 28
    assert len(trajectory['omitted_passages']) == 9
    assert all(e['id'] != 'T6' for e in trajectory['episodes'])
    assert '/Users/' not in trajectory_path.read_text()
    transfer = METHOD / 'source/selected/transfer_scientific_evidence.json'
    assert '/Users/' not in transfer.read_text()
    assert 'future_protocol' not in load(transfer)
    return {'scope': 'Selection integrity and supplied descriptive arithmetic only; no execution authentication, score truth, theorem replay or efficacy',
            'public_method_sources': 39, 'unchanged_originals': 33,
            'private_retained_originals': 24, 'numeric_starts': 12,
            'public_response_bodies': 8, 'selected_trajectory_passages': 28,
            'score_means': score_totals, 'usage': usage,
            'input_plus_output': 847499, 'passed': True}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
