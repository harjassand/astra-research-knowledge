"""Exact candidate and node checks against the already accepted cover only."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT/'results/COARSE_COMPRESSED_MODEL.json'
COVER = ROOT/'results/COARSE_SWITCHING_COVER.json'


def multiply(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(2)), F(0))
             for j in range(2)] for i in range(2)]


def survival(maps, word):
    product = [[F(1), F(0)], [F(0), F(1)]]
    for i in word:
        product = multiply(maps[int(i)], product)
    return sum(map(sum, product))/2


def main():
    saved, acquired = (json.loads(p.read_text()) for p in (MODEL, COVER))
    prior = json.loads(Path(__file__).with_name('COARSE_SWITCHING_COVER_REVIEW_RESULTS.json').read_text())
    cover_hash = hashlib.sha256(COVER.read_bytes()).hexdigest()
    assert cover_hash == prior['result_sha256']
    maps = [[[F(x) for x in row] for row in a] for a in saved['maps']]
    matrix_receipts = []
    for a in maps:
        assert a[0][1] == a[1][0]
        assert all(x >= 0 for row in a for x in row)
        rows = list(map(sum, a))
        assert all(x <= 1 for x in rows)
        determinant = a[0][0]*a[1][1]-a[0][1]**2
        assert a[0][0] > 0 and a[1][1] > 0 and determinant > 0
        complement_determinant = (1-a[0][0])*(1-a[1][1])-a[0][1]**2
        assert 1-a[0][0] > 0 and 1-a[1][1] > 0 and complement_determinant > 0
        matrix_receipts.append(dict(row_sums=[str(x) for x in rows],
            determinant=str(determinant), strict_positive_contraction_verified=True))
    assert list(map(F, saved['model_initial_distribution'])) == [F(1, 2)]*2
    assert survival(maps, '') == 1
    nodes = acquired['cover']['nodes']
    reports = {r['word']:r for r in saved['future_word_checks']}
    assert len(reports) == len(saved['future_word_checks']) == len(nodes) == 84
    assert set(reports) == set(nodes)
    overall = branch_bound = F(0)
    for word, node in nodes.items():
        p = survival(maps, word)
        lo, hi = map(F, node['interval'])
        if node['kind'] == 'terminal':
            bound = max(hi, p)
        else:
            bound = max(abs(p-lo), abs(p-hi))
            branch_bound = max(branch_bound, bound)
        report = reports[word]
        assert report['kind'] == node['kind']
        assert F(report['prediction']) == p
        assert F(report['error_or_all_extension_bound']) == bound
        assert 0 <= p <= 1 and bound <= F(acquired['cover']['all_word_error'])
        overall = max(overall, bound)
    assert F(saved['uniform_all_switching_error']) == overall
    assert F(saved['retained_branch_error_bound']) == branch_bound
    assert saved['new_source_queries'] == 0 and saved['source_confidence_event_unchanged'] is True
    assert saved['finite_model_dimension'] == 2 and saved['hidden_source_dimension_upper_bound'] is None
    out = dict(model_result_sha256=hashlib.sha256(MODEL.read_bytes()).hexdigest(),
        accepted_cover_result_sha256=cover_hash, matrices=matrix_receipts,
        exact_saved_node_checks=84, uniform_all_switching_error=str(overall),
        retained_branch_error_bound=str(branch_bound),
        source_acquisition_or_confidence_review_repeated=False,
        new_trajectories_generated=0, all_reviewed_checks_passed=True)
    path = Path(__file__).with_name('COARSE_COMPRESSED_MODEL_REVIEW_RESULTS.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
