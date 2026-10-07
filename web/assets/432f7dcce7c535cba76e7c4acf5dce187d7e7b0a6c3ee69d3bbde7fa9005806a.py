from green_bcs import *
from check_cutrank_bcs import brute
from pathlib import Path
from math import comb
import itertools
import json
import time


def direct_local_count(F, weights):
    n = len(F)
    out = [Q(0)]*(n+1)
    for states in itertools.product(range(3),repeat=n):
        z = direct_amplitude(F,states).abs2()
        for i,x in enumerate(states):
            z *= weights[i][x]
        out[sum(x == 1 for x in states)] += z
    return out


def uniform_min_counts(n):
    out = [Q(1)]
    for k in range(1,n//2+1):
        out.append(Q(2**k*sum(comb(k,j)*comb(n+2*k-j,4*k)
                     for j in range(min(k,n-2*k)+1))))
    return out+[Q(0)]*(n-len(out)+1)


def check_unsimplified(counter):
    # The direct O(k n^3) recurrence independently checks moment compression.
    n = counter.n
    for m in range(1,len(counter.DP)):
        for r in range(n+1):
            want, ep = Q(0), Q(1)
            for p in range(r+1,n+1):
                eq = Q(1)
                for q in range(p+1,n+1):
                    h = counter.A[p]*counter.B[q]+counter.B[p]*counter.A[q]
                    want += ep*eq*(counter.x[p]-counter.x[r]).abs2()*h*counter.DP[m-1][q]
                    eq *= counter.E[q]
                ep *= counter.E[p]
            assert counter.DP[m][r] == want, (m,r)


def run():
    started = time.monotonic()
    report = {'status': 'PASS', 'scope': 'finite exact Green-recognizer/DP diagnostics',
              'cases': [], 'minor_comparisons': 0, 'prefix_comparisons': 0,
              'local_table_comparisons': 0, 'sample_support_checks': 0}
    n = 6
    params = GreenParameters([C(i+1) for i in range(n)], [ONE]*n, [ONE]*n)
    cases = [('min_index',params)]
    n = 5
    params = GreenParameters([C(Q(i-2,3), Q((i*i % 5)+1,7)) for i in range(n)],
                             [C(Q(i+1,3),Q(1,5)) for i in range(n)],
                             [C(Q(2-i,5),Q(i+1,11)) for i in range(n)])
    cases.append(('complex_nonmonotone_gauged',params))
    cases.append(('rank1_cancellation',GreenParameters([ONE]*5,[ONE]*5,[ONE]*5)))
    params = GreenParameters([C(Q(i+1,2**25)) for i in range(5)],
                             [C(Q(i+1,2**10)) for i in range(5)], [ONE]*5)
    cases.append(('tiny_rare_norm',params))
    for name,params in cases:
        F = green_matrix(params)
        # Hard projection licenses arbitrary diagonals, including complex ones.
        for i in range(len(F)):
            F[i][i] = C(i+17,31-i)
        acquired = acquire_dense_green(F)
        verify_green(F,acquired)
        counter = GreenCounter(acquired)
        cs = counter.counts()
        assert cs == brute(F,[Q(0)]*len(F)), name
        check_unsimplified(counter)
        for states in itertools.product(range(3),repeat=len(F)):
            I = [i+1 for i,x in enumerate(states) if x == 1]
            J = [i+1 for i,x in enumerate(states) if x == 2]
            expected = Q(0)
            if len(I) == len(J):
                selected = sorted(I+J)
                if all(states[selected[2*m]-1] != states[selected[2*m+1]-1]
                       for m in range(len(I))):
                    d = ONE
                    previous = 0
                    for m in range(len(I)):
                        p,q = selected[2*m],selected[2*m+1]
                        d = d*(counter.x[p]-counter.x[previous])
                        previous = q
                    expected = d.abs2()
                    for i in I:
                        expected *= acquired.a[i-1].abs2()
                    for j in J:
                        expected *= acquired.b[j-1].abs2()
            assert direct_amplitude(F,states).abs2() == expected, (name,states)
            report['minor_comparisons'] += 1
        for prefix in ([0],[1],[2],[3],[1,2],[0,1,2],[1,1]):
            allowed = [{prefix[i]} if i < len(prefix) else set(range(4))
                       for i in range(len(F))]
            assert green_counts(F,allowed) == brute(F,[Q(0)]*len(F),allowed)
            report['prefix_comparisons'] += 1
        weights = [[Q(int(i % 3 != 1)),Q(i+1,3),Q(int(i % 2 == 0))]
                   for i in range(len(F))]
        wc = GreenCounter(acquired,weights)
        assert wc.counts() == direct_local_count(F,weights)
        check_unsimplified(wc)
        report['local_table_comparisons'] += 1
        for k,z in enumerate(cs):
            if z:
                for seed in (31,41,51):
                    states = counter.sample(k,random.Random(seed))
                    assert sum(x == 1 for x in states) == k
                    assert sum(x == 2 for x in states) == k
                    assert direct_amplitude(F,states)
                    report['sample_support_checks'] += 1
        report['cases'].append({'name': name, 'n': len(F),
                                'counts': [str(x) for x in cs]})
    n = 100
    params = GreenParameters([C(i+1) for i in range(n)],[ONE]*n,[ONE]*n)
    counter = GreenCounter(params)
    assert counter.counts() == uniform_min_counts(n)
    states = counter.sample(35,random.Random(100303))
    assert sum(x == 1 for x in states) == sum(x == 2 for x in states) == 35
    report['n100_closed_formula'] = {'status': 'PASS','n': n,
                                     'top_sector_norm': str(counter.counts()[50]),
                                     'sample_pair_count': 35}
    F = [[C(1) for _ in range(4)] for _ in range(4)]
    F[1][2] = C(2)
    try:
        acquire_dense_green(F)
    except ValueError as e:
        report['rejection_certificate'] = e.args[0]
    else:
        raise AssertionError('failed symmetry gauge not rejected')
    report['elapsed_seconds'] = time.monotonic()-started
    Path(__file__).with_name('checks_green.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    run()
