"""Exact finite checks for the four-state universal stopping obstruction.

The arbitrary-time impossibility is proved in the companion Markdown file.
These checks independently validate the source, a concrete failed ordinary
controller, the finite-tolerance comparison, and first-order response on all
deterministic visible stopping trees through three native calls.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


STATES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
MU = [F(1, 4)] * 4
NU = [F(1, 6), F(1, 6), F(1, 3), F(1, 3)]


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def rowmul(a, b):
    return [sum(a[k] * b[k][j] for k in range(len(a)))
            for j in range(len(b[0]))]


def inv(a):
    n = len(a)
    work = [a[i][:] + eye(n)[i] for i in range(n)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if work[i][col])
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for i in range(n):
            if i != col:
                scale = work[i][col]
                work[i] = [x - scale * y for x, y in zip(work[i], work[col])]
    return [r[n:] for r in work]


def submatrix(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def tv(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / 2


def kernel(delta, lam):
    return [[(1 - delta) * (1 + lam * h * hp) / 4
             + delta * int((yp, hp) == (h, y))
             for yp, hp in STATES] for y, h in STATES]


def swap_derivative(lam):
    base = kernel(F(0), lam)
    return [[F(int(STATES[j] == (h, y))) - base[i][j]
             for j in range(4)] for i, (y, h) in enumerate(STATES)]


def first_target(p, desired):
    target = [i for i, x in enumerate(STATES) if x[0] == desired]
    other = [i for i in range(4) if i not in target]
    killed = submatrix(p, other, other)
    resolvent = inv([[F(i == j) - killed[i][j] for j in range(2)]
                     for i in range(2)])
    occupation = rowmul([MU[i] for i in other], resolvent)
    arrivals = rowmul(occupation, submatrix(p, other, target))
    endpoint = [F(0)] * 4
    for j, a in zip(target, arrivals):
        endpoint[j] = MU[j] + a
    return endpoint, sum(occupation)


def literal_n2_compiler(p):
    k = zeros(4, 4)
    means = [F(1)] * 4
    for start, (y, h) in enumerate(STATES):
        for mid, (ym, hm) in enumerate(STATES):
            prob = p[start][mid]
            if ym == 1:
                k[start][mid] += prob
            elif y == -1:
                means[start] += prob
                for end in range(4):
                    k[start][end] += prob * p[mid][end]
            else:
                k[start][mid] += prob / 2
                means[start] += prob / 2
                for end in range(4):
                    k[start][end] += prob * p[mid][end] / 2
    return k, means


def trees(depth):
    if depth == 0:
        return [None]
    children = trees(depth - 1)
    return [None] + [(left, right) for left in children for right in children]


def iid_tree_statistics(policy):
    coefficients = [F(0)] * 3
    mean_count = F(0)
    mean_y = F(0)

    def visit(node, path, prob):
        nonlocal mean_count, mean_y
        if node is None:
            t = len(path) - 1
            mean_count += prob * t
            mean_y += prob * path[-1]
            for lag in range(t):
                coefficients[lag] += prob * path[t - lag - 1]
            return
        for j, sign in enumerate((-1, 1)):
            visit(node[j], path + [sign], prob / 2)

    for j, sign in enumerate((-1, 1)):
        visit(policy[j], [sign], F(1, 2))
    assert sum(coefficients) == -mean_y
    assert sum(abs(c) for c in coefficients) <= mean_count
    return coefficients, mean_count, mean_y


def actual_tree_first_order(policy, lam):
    p = kernel(F(0), lam)
    dp = swap_derivative(lam)
    terminal = [F(0)] * 4
    derivative = [F(0)] * 4

    def visit(node, mass, dmass):
        if node is None:
            for i in range(4):
                terminal[i] += mass[i]
                derivative[i] += dmass[i]
            return
        nxt = rowmul(mass, p)
        dnxt = [a + b for a, b in zip(rowmul(dmass, p), rowmul(mass, dp))]
        for j, sign in enumerate((-1, 1)):
            selected = [v if STATES[i][0] == sign else F(0)
                        for i, v in enumerate(nxt)]
            dselected = [v if STATES[i][0] == sign else F(0)
                         for i, v in enumerate(dnxt)]
            visit(node[j], selected, dselected)

    for j, sign in enumerate((-1, 1)):
        mass = [MU[i] if STATES[i][0] == sign else F(0) for i in range(4)]
        visit(policy[j], mass, [F(0)] * 4)
    assert sum(terminal) == 1 and sum(derivative) == 0
    hidden = sum(derivative[i] * STATES[i][1] for i in range(4))
    visible = sum(derivative[i] * STATES[i][0] for i in range(4))
    assert visible == 0
    return hidden


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(x) for x in value]
    return value


def main():
    family_cases = []
    first_target_fixture = None
    for delta, lam in product([F(0), F(1, 64), F(1, 8), F(1, 4)],
                              [F(0), F(1, 8), F(1, 4), F(1, 2)]):
        p = kernel(delta, lam)
        assert all(sum(row) == 1 for row in p)
        assert all(p[i][j] == p[j][i] for i in range(4) for j in range(4))
        assert rowmul(MU, p) == MU
        assert min(x for row in p for x in row) >= F(3, 32)

        neg, neg_mean = first_target(p, -1)
        pos, pos_mean = first_target(p, 1)
        out = [x / 3 + 2 * y / 3 for x, y in zip(neg, pos)]
        mean = neg_mean / 3 + 2 * pos_mean / 3
        b = delta / (2 + delta - lam)
        predicted = [(1 + F(1, 3) * y) * (1 - y * h * b) / 4 for y, h in STATES]
        assert out == predicted
        assert sum(out[i] * STATES[i][0] for i in range(4)) == F(1, 3)
        assert sum(out[i] * STATES[i][1] for i in range(4)) == -b / 3
        later = rowmul(out, p)
        assert sum(later[i] * STATES[i][0] for i in range(4)) == -delta * b / 3
        assert tv(out, NU) == b / 2
        assert mean == 1 + delta * delta / ((1 - delta) * (2 + delta - lam))

        k, means = literal_n2_compiler(p)
        assert all(sum(row) == 1 for row in k)
        assert rowmul(NU, k) == NU
        assert min(x for row in k for x in row) >= F(9, 512)
        assert sum(NU[i] * means[i] for i in range(4)) == F(4, 3)
        at = MU[:]
        trace = []
        for n in range(1, 9):
            at = rowmul(at, k)
            assert tv(at, NU) <= F(119, 128) ** n
            if n in (1, 2, 4, 8):
                trace.append({'macros': n, 'tv': tv(at, NU),
                              'universal_bound': F(119, 128) ** n})
        family_cases.append({'delta': delta, 'lambda': lam,
                             'native_min_entry': min(x for row in p for x in row),
                             'compiled_min_entry': min(x for row in k for x in row),
                             'first_target_hidden_bias': -b / 3,
                             'first_target_tv': b / 2,
                             'first_target_mean_calls': mean,
                             'finite_tolerance_trace': trace})
        if delta == F(1, 8) and lam == F(1, 4):
            first_target_fixture = {'native_kernel': p, 'target': NU,
                                    'actual_endpoint': out,
                                    'hidden_mean': -b / 3, 'tv': b / 2,
                                    'next_visible_mean': -delta * b / 3,
                                    'mean_calls': mean, 'compiled_kernel': k}

    children = trees(3)
    policy_count = 0
    nonzero_mean_count = 0
    response_count = 0
    witness = None
    for policy in product(children, repeat=2):
        coefficients, count, ymean = iid_tree_statistics(policy)
        policy_count += 1
        if ymean:
            nonzero_mean_count += 1
            assert any(coefficients)
        for lam in (F(0), F(1, 4), F(1, 2)):
            observed = actual_tree_first_order(policy, lam)
            predicted = sum(c * lam ** lag for lag, c in enumerate(coefficients))
            assert observed == predicted
            response_count += 1
        if witness is None and ymean == F(3, 4):
            witness = {'iid_mean_calls': count, 'iid_terminal_y_mean': ymean,
                       'response_coefficients': coefficients}

    root = Path(__file__).resolve().parent
    proof = root / 'FOUR_STATE_UNIVERSAL_PREPARATION_OBSTRUCTION.md'
    result = {'scope': 'Exact synthetic checks. The arbitrary-time impossibility is analytic; no finite enumeration establishes its infinite-mean conclusion by itself.',
              'family_cases': family_cases,
              'ordinary_first_label_fixture': first_target_fixture,
              'stopping_tree_checks': {'max_native_calls': 3,
                                      'deterministic_policies': policy_count,
                                      'policies_with_nonzero_terminal_mean': nonzero_mean_count,
                                      'exact_response_checks': response_count,
                                      'witness': witness},
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest()}
    output = root / 'FOUR_STATE_OBSTRUCTION_CHECKS.json'
    output.write_text(json.dumps(encode(result), indent=2) + '\n')
    print(json.dumps({'status': 'all exact assertions passed',
                      'family_cases': len(family_cases),
                      'stopping_policies': policy_count,
                      'linear_response_checks': response_count,
                      'output': str(output)}))


if __name__ == '__main__':
    main()
