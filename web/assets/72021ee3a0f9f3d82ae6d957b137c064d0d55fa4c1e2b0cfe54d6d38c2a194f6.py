from treecut_bcs import *
from check_cutrank_bcs import brute
from pathlib import Path
from math import comb
import itertools
import json
import time


def run():
    started = time.monotonic()
    report = {'status': 'PASS', 'scope': 'finite exact tree-tensor diagnostics',
              'cases': [], 'amplitude_comparisons': 0,
              'count_comparisons': 0, 'prefix_comparisons': 0}
    F = [[C(((3*i+5*j+i*j) % 7)-3, ((i+2*j*j) % 5)-2)
          for j in range(4)] for i in range(4)]
    cases = [('noncontiguous_original_labels', F, ((3,1),(0,2)))]
    F = [[C(1 if i < j else 0) for j in range(5)] for i in range(5)]
    cases.append(('one_direction_cutrank1', F, balanced_order_tree(5)))
    F = [[C(0) for _ in range(5)] for _ in range(5)]
    for i, j in ((0,1),(0,3),(1,2),(1,4)):
        F[i][j], F[j][i] = C(i+1,j+1), C(j+1,-i-1)
    for i in range(5):
        F[i][i] = C(Q(i+1,7))
    ft = forest_tree(F)
    assert ft is not None
    cases.append(('acquired_forest_with_soft_diagonals', F, ft))
    F = [[C(0) for _ in range(5)] for _ in range(5)]
    for i, j in ((0,1),(1,2),(2,0),(2,3),(3,4)):
        F[i][j], F[j][i] = C(i+1,j+1), C(j+1,-i-1)
    assert forest_tree(F) is None
    st, sw = separator_tree(F, 2)
    cases.append(('nonbipartite_acquired_separator', F, st))
    report['separator_witness'] = sw
    for name, F, tree in cases:
        n = len(F)
        compiled = acquire_tree(F, tree, max_dimension=32)
        for x in itertools.product(range(4), repeat=n):
            assert compiled.amplitude(x) == direct_amplitude(F, x), (name,x)
            report['amplitude_comparisons'] += 1
        filters = [[Q(0)]*n, [Q(1)]*n,
                   [Q(0) if i % 3 == 0 else Q(i+1,2) for i in range(n)]]
        for t in filters:
            assert tree_counts(compiled, t) == brute(F,t), (name,t)
            report['count_comparisons'] += 1
        for prefix in ([0], [1], [2], [3], [1,2]):
            allowed = [{prefix[i]} if i < len(prefix) else set(range(4))
                       for i in range(n)]
            assert tree_counts(compiled, filters[2], allowed) == brute(F,filters[2],allowed)
            report['prefix_comparisons'] += 1
            conditional = tree_counts(compiled, filters[2], allowed)
            for k,z in enumerate(conditional):
                if z:
                    states = tree_sample(compiled,k,filters[2],random.Random(19+k),allowed)
                    assert states[:len(prefix)] == prefix
                    assert direct_amplitude(F,states)
        cs = tree_counts(compiled)
        for k, z in enumerate(cs):
            if z:
                x = tree_sample(compiled, k, rng=random.Random(8303+k))
                assert 3 not in x and sum(y & 1 for y in x) == k
                assert direct_amplitude(F,x)
        report['cases'].append({'name': name, 'n': n,
                                'acquired_order': compiled.order,
                                'max_cutrank': compiled.max_cutrank,
                                'hard_counts': [str(z) for z in cs]})
    n = 12
    F = [[C(1 if i < j else 2 if i > j else 0)
          for j in range(n)] for i in range(n)]
    compiled = acquire_tree(F, balanced_order_tree(n), max_dimension=16)
    expected = [Q(1)]+[Q(5*comb(n,2*k)) if 2*k <= n else Q(0)
                      for k in range(1,n+1)]
    assert tree_counts(compiled) == expected
    report['dense_fullrank_balanced_tree'] = {'n': n,
        'max_cutrank': compiled.max_cutrank, 'status': 'PASS',
        'hard_counts': [str(z) for z in expected]}
    F = [[C(i != j) for j in range(6)] for i in range(6)]
    try:
        separator_tree(F, 2)
    except ValueError as e:
        report['separator_rejection_certificate'] = e.args[0]
    else:
        raise AssertionError('K6 has no size<=2 balanced separator')
    report['elapsed_seconds'] = time.monotonic()-started
    Path(__file__).with_name('checks_tree.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    run()
