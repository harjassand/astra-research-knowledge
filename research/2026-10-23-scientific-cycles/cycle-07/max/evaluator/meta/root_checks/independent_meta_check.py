#!/usr/bin/env python3
"""Independent exact checks; synthetic metadata and a finite proof DAG only."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, math, time, resource


def pairwise_midrank(values):
    return [F(1, 2) + sum(x < v for x in values) + F(sum(x == v for x in values), 2)
            for v in values]


def exact_rho(a, b):
    a, b = pairwise_midrank(a), pairwise_midrank(b)
    center = F(len(a) + 1, 2)
    cov = sum((x-center)*(y-center) for x, y in zip(a, b))
    va = sum((x-center)**2 for x in a)
    vb = sum((y-center)**2 for y in b)
    square = cov*cov/(va*vb)
    return {'square': str(square), 'value': math.copysign(math.sqrt(float(square)), cov) if cov else 0.0}


def shared_factor():
    result = []
    for levels in (2, 5, 10, 50):
        table = [(10**j, length, uses) for j, length, uses in product(range(levels), (100, 200), range(1, 5))]
        V, L, d = map(list, zip(*table))
        I = [F(100*v, ell) for v, ell in zip(V, L)]
        U = [v*u for v, u in zip(V, d)]
        # Every value of I occurs equally often with every use count.
        independent = all(sum(i == z and u == k for i, u in zip(I, d))*len(I)
                          == sum(i == z for i in I)*sum(u == k for u in d)
                          for z in set(I) for k in set(d))
        assert independent
        out = {'levels': levels, 'rows': len(table), 'I_U': exact_rho(I, U),
               'I_d': exact_rho(I, d), 'V_U_control': exact_rho(V, U),
               'I_d_jointly_independent': independent}
        assert out['I_d']['square'] == '0'
        result.append(out)
    return result


def expansion():
    costs = {'T': 1, 'A': 1, 'B': 1, 'L': 20, 'p': 0}
    deps = {'T': {'A', 'B'}, 'A': {'L'}, 'B': {'L'}, 'L': {'p'}, 'p': set()}
    records = []
    for order in (('A','B','L'), ('A','L','B','L')):
        frontier = set(deps['T']); label = costs['T']; events = []
        for item in order:
            assert item in frontier
            frontier.remove(item); frontier.update(deps[item]); label += costs[item]
            events.append({'expanded': item, 'frontier': sorted(frontier), 'label': label})
        records.append({'order': order, 'target': 'T', 'final_premises': sorted(frontier),
                        'label': label, 'events': events})
    assert records[0]['final_premises'] == records[1]['final_premises'] == ['p']
    assert [r['label'] for r in records] == [23,43]
    seen = set()
    def memoized(node):
        if node in seen or node == 'p': return 0
        seen.add(node)
        return costs[node] + sum(memoized(child) for child in sorted(deps[node]))
    control = memoized('T')
    assert control == 23
    return {'paths': records, 'shared_DAG_control_cost': control,
            'scope': 'Same declared proof dependency graph; not actual Mathlib rows or shortest Lean proof.'}


def main():
    start = time.perf_counter()
    result = {'status': 'PASS', 'shared_factor': shared_factor(), 'expansion': expansion(),
              'scope': 'Independent implementation checks; no prospective discovery or empirical reanalysis claim.'}
    result['wall_seconds'] = time.perf_counter() - start
    result['peak_rss_kib_linux'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    output = Path(__file__).with_name('ROOT_EXACT_CHECK.json')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
