"""Read-only independent audit of frozen new experiment outputs.

Does not import the search or scientific backend and executes no transition.
Checks source bindings, complete final-basis key coverage, origin degrees,
history consistency and process receipts. This is not a witness certificate.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def admissible(kind, left, right=None):
    if kind == 'L':
        return left[0] <= 3
    if kind == 'R':
        return left[1] <= 3
    if kind == 'S':
        return left[1] + right[0] <= 4
    assert kind == 'P'
    return left[0] + right[0] <= 4 and left[1] + right[1] <= 4


def degree_out(kind, left, right=None):
    if kind == 'L':
        return [1, left[1]]
    if kind == 'R':
        return [left[0], 1]
    if kind == 'S':
        return [left[0], right[1]]
    return [left[0] + right[0], left[1] + right[1]]


def main():
    frozen = json.loads((ROOT / 'FROZEN_INPUTS.json').read_text())
    for entry in frozen['files']:
        path = ROOT / entry['path']
        assert path.stat().st_size == entry['bytes']
        assert sha(path) == entry['sha256']
    receipts = json.loads((ROOT / 'results/WHOLE_PROCESS_RECEIPTS.json').read_text())
    assert receipts['protocol_sha256'] == sha(ROOT / 'PROTOCOL.txt')
    assert receipts['frozen_inputs_sha256'] == sha(ROOT / 'FROZEN_INPUTS.json')
    assert len(receipts['receipts']) == 3
    reports = []
    for receipt in receipts['receipts']:
        arm = receipt['arm']
        path = ROOT / 'results' / (arm + '.json')
        assert receipt['returncode'] == 0 and not receipt['wall_kill']
        assert sha(path) == receipt['output_sha256']
        result = json.loads(path.read_text())
        assert result['common_driver_sha256'] == sha(ROOT / 'common_search.py')
        assert result['reason'] == 'closed'
        assert result['failure'] is None
        assert result['remaining_heap'] == 0
        assert not result['final_basis_missing_keys']
        records = result['records']
        assert len(records) == result['discovered_families'] < 2500
        active = set()
        for i, (record, history) in enumerate(zip(records, result['history'])):
            assert record['id'] == history['id'] == i
            assert record['degree'] == history['degree']
            assert len(record['states']) == history['states'] > 0
            assert all(1 <= d <= 4 for d in record['degree'])
            for state in record['states']:
                if arm == 'A_counts_flags':
                    dl = 4 if state[2] is None else sum(state[2])
                    dr = 4 if state[4] is None else sum(state[4])
                else:
                    dl, dr = state[2], state[5]
                assert [dl, dr] == record['degree']
            expression = record['expression']
            kind = expression['kind']
            if kind == 'path':
                assert i == 0 and expression['length'] == 2
                assert record['degree'] == [1, 1]
            else:
                children = expression['children']
                assert all(0 <= child < i for child in children)
                assert len(children) == (1 if kind in ('L', 'R') else 2)
                left = records[children[0]]['degree']
                right = None if len(children) == 1 else records[children[1]]['degree']
                assert admissible(kind, left, right)
                assert degree_out(kind, left, right) == record['degree']
            assert all(removed in active for removed in history['removed'])
            active.difference_update(history['removed'])
            active.add(i)
        assert len(result['history']) == len(records)
        assert sorted(active) == result['basis_ids']
        assert len(active) == result['active_families']
        tested = [tuple(key) for key in result['tested_transitions']]
        tested_set = set(tested)
        assert len(tested_set) == len(tested) == result['checked_transitions']
        assert dict(Counter(key[0] for key in tested)) == result['transition_kinds']
        for key in tested:
            left = records[key[1]]['degree']
            right = None if len(key) == 2 else records[key[2]]['degree']
            assert admissible(key[0], left, right)
        required = set()
        for i in active:
            dl = records[i]['degree']
            for kind in ('L', 'R'):
                if admissible(kind, dl):
                    required.add((kind, i))
            for j in active:
                dr = records[j]['degree']
                if admissible('S', dl, dr):
                    required.add(('S', i, j))
                if i <= j and admissible('P', dl, dr):
                    required.add(('P', i, j))
        assert not (required - tested_set)
        assert len(required) == result['final_basis_required_keys']
        assert receipt['whole_process_cpu_seconds'] >= result['cost']['body_cpu_seconds']
        assert receipt['whole_process_peak_rss_bytes'] < 512 * 1024**2
        for key in ('reason', 'active_families', 'discovered_families', 'checked_transitions'):
            assert receipt[key] == result[key]
        reports.append({'arm': arm, 'status': 'PASS', 'final_required_keys': len(required),
                        'tested_keys': len(tested), 'origin_records': len(records),
                        'output_sha256': sha(path)})
    out = {'status': 'PASS', 'frozen_files_checked': len(frozen['files']), 'arms': reports,
           'scope': 'Read-only independent bindings, ledger and structural checks. '
                    'No search, scientific transition, original suite or witness certificate replay.',
           'check_source_sha256': sha(Path(__file__))}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
