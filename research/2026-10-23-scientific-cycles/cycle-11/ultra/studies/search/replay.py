#!/usr/bin/env python3
"""Exact rational admissions of the NEW classical lemma; no old science replay.

Not a quantum receiver or a large coding implementation. Fraction elimination
computes exact wrong-endpoint probabilities and expected walk steps for the
stated independent alpha=1/16 instance of the broader conditional-noise theorem.
The conditional-noise theorem is analytic in PROOF.txt.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time


def ceil_log_inverse(p):
    x = 0
    while F(1, 2 ** x) > p:
        x += 1
    return x


def sfe_tree(probs, values):
    words = []
    cumulative = F(0)
    for p in probs:
        length = ceil_log_inverse(p) + 1
        midpoint = cumulative + p / 2
        digit = (midpoint.numerator * 2 ** length) // midpoint.denominator
        words.append(format(digit, '0%db' % length))
        cumulative += p
    assert cumulative == 1
    for i, w in enumerate(words):
        for j, v in enumerate(words):
            if i != j:
                assert not v.startswith(w)
    assert words == sorted(words)
    nodes = []

    def make(indices, level=0, parent=None, depth=0):
        if len(indices) == 1:
            k = indices[0]
            idx = len(nodes)
            nodes.append(dict(parent=parent, depth=depth, a=values[k],
                              b=values[k], leaf=k, children=[]))
            return idx
        while len({words[k][level] for k in indices}) == 1:
            level += 1
        idx = len(nodes)
        nodes.append(dict(parent=parent, depth=depth, a=values[indices[0]],
                          b=values[indices[-1]], leaf=None, children=[]))
        left = [k for k in indices if words[k][level] == '0']
        right = [k for k in indices if words[k][level] == '1']
        assert left and right
        children = [make(left, level + 1, idx, depth + 1),
                    make(right, level + 1, idx, depth + 1)]
        nodes[idx]['children'] = children
        return idx
    make(list(range(len(probs))))
    return nodes, words


def add_paths(nodes, s):
    leaves = [(i, d['leaf'], d['depth']) for i, d in enumerate(nodes)
              if d['leaf'] is not None]
    endpoints = {}
    depths = {}
    for idx, k, ell in leaves:
        depths[k] = ell
        m = ell + s
        assert m >= 1
        parent = idx
        for _ in range(m):
            child = len(nodes)
            nodes.append(dict(parent=parent, depth=nodes[parent]['depth'] + 1,
                              a=nodes[idx]['a'], b=nodes[idx]['b'], leaf=k,
                              children=[]))
            nodes[parent]['children'] = [child]
            parent = child
        endpoints[parent] = k
    return endpoints, depths


def eliminate(matrix, rhs):
    """Exact Gauss-Jordan, multiple RHS columns."""
    n = len(matrix)
    cols = len(rhs[0])
    aug = [matrix[i][:] + rhs[i][:] for i in range(n)]
    for c in range(n):
        pivot = next(i for i in range(c, n) if aug[i][c])
        aug[c], aug[pivot] = aug[pivot], aug[c]
        d = aug[c][c]
        aug[c] = [v / d for v in aug[c]]
        for i in range(n):
            if i == c or not aug[i][c]:
                continue
            factor = aug[i][c]
            aug[i] = [x - factor * y for x, y in zip(aug[i], aug[c])]
    return [row[n:n+cols] for row in aug]


def transition(nodes, v, actual, alpha=F(1, 16)):
    d = nodes[v]
    yes_a = F(1) if d['a'] <= actual else alpha
    maximum = nodes[0]['b']
    yes_b = F(0) if d['b'] == maximum else (F(1) if d['b'] + 1 <= actual else alpha)
    passed = yes_a * (1 - yes_b)
    # The known high sentinel is synthetic NO at every containing interval.
    ans = {}

    def add(u, p):
        ans[u] = ans.get(u, F(0)) + p
    if d['parent'] is not None:
        add(d['parent'], 1 - passed)
    else:
        assert passed == 1
    if len(d['children']) == 1:
        add(d['children'][0], passed)
    else:
        left, right = d['children']
        threshold = nodes[right]['a']
        yes = F(1) if threshold <= actual else alpha
        add(right, passed * yes)
        add(left, passed * (1 - yes))
    assert sum(ans.values()) == 1
    return ans


def admission(probs, values, s):
    nodes, words = sfe_tree(probs, values)
    endpoints, depths = add_paths(nodes, s)
    live = [i for i in range(len(nodes)) if i not in endpoints]
    mapping = {i: j for j, i in enumerate(live)}
    n = len(live)
    out = []
    for k, actual in enumerate(values):
        matrix = [[F(i == j) for j in range(n)] for i in range(n)]
        rhs = [[F(1), F(0)] for _ in range(n)]
        for vi, v in enumerate(live):
            for u, prob in transition(nodes, v, actual).items():
                if u in endpoints:
                    if endpoints[u] != k:
                        rhs[vi][1] += prob
                else:
                    matrix[vi][mapping[u]] -= prob
        solved = eliminate(matrix, rhs)
        steps, error = solved[mapping[0]]
        d = 2 * depths[k] + s
        drift_bound = F(4 * d, 3)
        err_bound = F(1, 6 * 7 ** s)
        assert steps <= drift_bound
        assert error <= err_bound
        # Exact depth/Kraft checks; no floating entropy used in admission.
        assert F(1, 2 ** depths[k]) >= probs[k] / 4
        out.append(dict(k=actual, leaf_depth=depths[k],
                        steps=str(steps), error=str(error),
                        step_bound=str(drift_bound), error_bound=str(err_bound)))
    assert sum(F(1, 2 ** d) for d in depths.values()) <= 1
    return dict(prior=[str(p) for p in probs], values=values, s=s,
                words=words, vertices=len(nodes), conditional=out)


def main():
    start = time.perf_counter()
    cases = [([F(1, 2)] * 2, [1, 2]),
             ([F(1, 2)] * 2, [1, 1000000]),
             ([F(1, 3)] * 3, [1, 2, 3]),
             ([F(1, 5)] * 5, [1, 2, 3, 4, 5]),
             ([F(1, 2), F(1, 4), F(1, 8), F(1, 8)], [1, 2, 3, 4]),
             ([F(255, 256), F(1, 256)], [1, 1000000])]
    results = [admission(p, v, s) for p, v in cases for s in [1, 2]]
    # The two point examples are exactly gap-independent as abstract oracle
    # chains; this DOES NOT establish their physical Bell-loss cost.
    assert results[0]['conditional'] != []
    for a, b in [(0, 2), (1, 3)]:
        assert [(x['steps'], x['error']) for x in results[a]['conditional']] == \
               [(x['steps'], x['error']) for x in results[b]['conditional']]
    result = dict(status='PASS', scope='new exact classical admissions only',
                  cases=len(results), conditional_cases=sum(len(c['conditional']) for c in results),
                  proof_sha256=hashlib.sha256(Path(__file__).with_name('PROOF.txt').read_bytes()).hexdigest(),
                  exact_markov_results=results,
                  wall_seconds=time.perf_counter() - start)
    Path(__file__).with_name('RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'exact_markov_results'}, indent=2))


if __name__ == '__main__':
    main()
