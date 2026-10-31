"""Compile a reversible-hidden word inequality through a grid LP.

The exact verifier in outputs/predictive_flow/receive.py independently checks
the rationalized dual against every flow column. HiGHS proposes a certificate;
floating feasibility or optimality never supplies the final sign.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as Q
import json
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

ROOT = Path(__file__).resolve().parent.parent


def feature(node, word, k):
    a, plus, minus = node
    u, center, v = word
    if center != a:
        return Q(0)
    return (Q(minus, k) if u else 1 - Q(minus, k)) * (Q(plus, k) if v else 1 - Q(plus, k))


def solve(k=8):
    start = time.perf_counter()
    nodes = list(product(range(2), range(k + 1), range(k + 1)))
    words = list(product(range(2), repeat=3))
    target = [Q(1, 8) - Q(1, 32) * (1 - 2 * u) * (1 - 2 * v) for u, a, v in words]
    n = len(nodes)
    edges = [(i, j) for i in range(n) for j in range(i, n)]
    nf = len(edges)
    nr = 4 * n + 16
    ri, ci, vv = [], [], []
    norm = np.zeros(nf + 1)
    F = np.array([[float(feature(node, w, k)) for node in nodes] for w in words])
    for col, (i, j) in enumerate(edges):
        norm[col] = 1 if i == j else 2
        for current, other in ((i, j),) if i == j else ((i, j), (j, i)):
            labj = nodes[other][0]
            for r, q in enumerate((nodes[current][1] / k, nodes[current][2] / k)):
                for side, value in enumerate((labj - q - 1 / k, q - labj - 1 / k)):
                    if value:
                        ri.append(4 * current + 2 * r + side); ci.append(col); vv.append(value)
        values = F[:, i] if i == j else F[:, i] + F[:, j]
        for widx, value in enumerate(values):
            if value:
                for side, sign in enumerate((1., -1.)):
                    ri.append(4 * n + 2 * widx + side); ci.append(col); vv.append(sign * value)
    for r in range(4 * n, nr):
        ri.append(r); ci.append(nf); vv.append(-1.)
    matrix = coo_matrix((vv, (ri, ci)), shape=(nr, nf + 1)).tocsr()
    rhs = np.zeros(nr)
    for i, p in enumerate(target):
        rhs[4 * n + 2 * i] = float(p)
        rhs[4 * n + 2 * i + 1] = -float(p)
    objective = np.zeros(nf + 1); objective[-1] = 1.
    opt = linprog(objective, A_ub=matrix, b_ub=rhs, A_eq=norm[None, :], b_eq=[1.], bounds=(0, None), method='highs')
    assert opt.success
    raw = opt.ineqlin.marginals
    y = [min(Q(0), Q(str(float(x))).limit_denominator(10 ** 7)) for x in raw]
    # The t column must have dual coefficient <=1. Rescaling all duals
    # preserves their signs and gives that inequality exactly.
    tcoef = -sum(y[4 * n:], Q(0))
    if tcoef > 1:
        y = [a / tcoef for a in y]
    yd = [y[4 * n + 2 * w] - y[4 * n + 2 * w + 1] for w in range(8)]
    rdata = [sum((yd[w] * feature(node, word, k) for w, word in enumerate(words)), Q(0)) for node in nodes]

    def endpoint(i, j):
        label = nodes[j][0]
        out = rdata[i]
        for group, num in enumerate(nodes[i][1:]):
            q = Q(num, k)
            out += y[4 * i + 2 * group] * (label - q - Q(1, k))
            out += y[4 * i + 2 * group + 1] * (q - label - Q(1, k))
        return out

    z = min(-endpoint(i, j) if i == j else -(endpoint(i, j) + endpoint(j, i)) / 2 for i, j in edges)
    source_gap = z + sum((a * p for a, p in zip(yd, target)), Q(0))
    assert source_gap > 0
    witness = [-z - x for x in yd]
    width = max(witness) - min(witness)
    needed = 8 * width ** 2 / source_gap ** 2
    windows = (needed.numerator + needed.denominator - 1) // needed.denominator
    result = {'scope': __doc__, 'mesh': k, 'nodes': n, 'symmetric_flow_columns': nf, 'inequality_rows': nr, 'raw_solver_distance_Linfinity': float(opt.fun), 'row_duals': list(map(str, y[:4 * n])), 'data_duals': list(map(str, y[4 * n:])), 'normalization_dual': str(z), 'exact_positive_source_dual_gap': str(source_gap), 'source_dual_gap_numeric': float(source_gap), 'word_order': [''.join(map(str, w)) for w in words], 'word_statistic': list(map(str, witness)), 'exact_word_statistic_range_width': str(width), 'iid_validation_windows_sufficient_for_each_error_below_0_025': windows, 'hidden_state_count_assumption': None, 'exact_certificate_verified_by_separate_receiver': False, 'seconds': time.perf_counter() - start}
    (ROOT / 'outputs/predictive_flow/lp_certificate.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({a: result[a] for a in ['mesh', 'nodes', 'symmetric_flow_columns', 'raw_solver_distance_Linfinity', 'source_dual_gap_numeric', 'iid_validation_windows_sufficient_for_each_error_below_0_025', 'seconds']}, indent=2))


if __name__ == '__main__':
    solve()
