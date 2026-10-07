"""Bounded exact checks against determinant enumeration, independent of MPS."""
from cutrank_bcs import *
import itertools
import json
import time
from math import comb
from pathlib import Path


def brute(F, t, allowed=None):
    n = len(F)
    allowed = [range(4) for _ in F] if allowed is None else allowed
    out = [Q(0)]*(n+1)
    for x in itertools.product(*allowed):
        a = direct_amplitude(F, x)
        w = a.abs2()
        for i, z in enumerate(x):
            if z == 3:
                w *= t[i]
        out[sum(z & 1 for z in x)] += w
    return out


def run():
    started = time.monotonic()
    cases = []
    cases.append(('zero', [[C(0) for _ in range(3)] for _ in range(3)]))
    cases.append(('complex_dense', [[C(1), C(2,1), C(-1)],
                                   [C(1,-1), C(0), C(3)],
                                   [C(2), C(-2,1), C(1)]]))
    cases.append(('cancel_J_minus_I', [[C(i != j) for j in range(4)]
                                     for i in range(4)]))
    cases.append(('complex_dense_cutrank4',
                  [[C(((3*i+5*j+i*j) % 7)-3, ((i+2*j*j) % 5)-2)
                    for j in range(4)] for i in range(4)]))
    cases.append(('rank2_dense_nonbipartite',
                  [[C((i+1)*(j+2)+(i % 2)*(j % 3),
                      (i % 2)*(j+2))
                    for j in range(5)] for i in range(5)]))
    cases.append(('directed_odd_cycle', [[C(int(j == (i+1) % 5))
                                        for j in range(5)] for i in range(5)]))
    cases.append(('tiny_rational', [[C(0), C(Q(1, 2**35)), C(1)],
                                   [C(1), C(0), C(Q(1, 2**34))],
                                   [C(Q(1, 2**36)), C(1), C(0)]]))
    report = {'status': 'PASS', 'scope': 'finite exact implementation checks',
              'cases': [], 'amplitudes_checked': 0, 'count_vectors_checked': 0,
              'prefix_vectors_checked': 0, 'sample_support_checks': 0}
    rng = random.Random(312031)
    for name, F in cases:
        n = len(F)
        mps = acquire_mps(F, max_dimension=32)
        for x in itertools.product(range(4), repeat=n):
            assert mps.amplitude(x) == direct_amplitude(F, x), (name, x)
            report['amplitudes_checked'] += 1
        filters = [[Q(0)]*n, [Q(1)]*n,
                   [Q((i % 3)+1, (i % 2)+1) if i != n-1 else Q(0)
                    for i in range(n)]]
        for t in filters:
            got, want = counts(mps, t), brute(F, t)
            assert got == want, (name, t, got, want)
            report['count_vectors_checked'] += 1
        t = filters[2]
        for prefix in ([], [0], [1], [2], [3], [1,2]):
            if len(prefix) > n:
                continue
            allowed = [{prefix[i]} if i < len(prefix) else set(range(4))
                       for i in range(n)]
            assert counts(mps, t, allowed) == brute(F, t, allowed), (name, prefix)
            report['prefix_vectors_checked'] += 1
        hard = counts(mps)
        for k, norm in enumerate(hard):
            if norm:
                for _ in range(3):
                    x = sample(mps, k, rng=rng)
                    assert 3 not in x and sum(z & 1 for z in x) == k
                    assert direct_amplitude(F, x)
                    report['sample_support_checks'] += 1
            else:
                try:
                    sample(mps, k, rng=rng)
                except ValueError as e:
                    assert str(e) == 'zero requested sector'
                else:
                    raise AssertionError('zero sector not rejected')
        report['cases'].append({'name': name, 'n': n,
                                'cut_ranks': [b.rank for b in mps.cuts],
                                'max_bond_dimension': max(b.dim for b in mps.cuts),
                                'hard_counts': [str(z) for z in hard]})
    F = [[C(1) if i == j else C(0) for j in range(3)] for i in range(3)]
    mps = acquire_mps(F)
    assert counts(mps) == [Q(1), Q(0), Q(0), Q(0)]
    assert counts(mps, [Q(3)]*3) == [Q(1), Q(9), Q(27), Q(27)]
    report['diagonal_hard_deletion_and_attraction'] = 'PASS'
    n = 16
    F = [[C(1 if i < j else 2 if i > j else 0)
          for j in range(n)] for i in range(n)]
    mps = acquire_mps(F, max_dimension=4)
    got = counts(mps)
    expected = [Q(1)]+[Q(5*comb(n, 2*k)) if 2*k <= n else Q(0)
                      for k in range(1, n+1)]
    assert got == expected
    assert determinant(F) == C((-1)**(n-1)*(2**n-2))
    report['full_rank_dense_semiseparable'] = {
        'n': n, 'max_cutrank': mps.max_cutrank,
        'determinant': str(determinant(F).re),
        'hard_counts': [str(z) for z in got],
        'comparison': 'exact all-size formula 1, 5 binomial(n,2k)',
        'status': 'PASS'}
    report['elapsed_seconds'] = time.monotonic()-started
    Path(__file__).with_name('checks_initial.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    run()
