"""Complete reversible-hidden LP witness compiler on a simplex grid.

Input: rational probabilities of every chronological word of length 2L+1,
in lexicographic order, alphabet size, L, and the chosen mesh. Hidden-state
parameters are not inputs. A finite grid may return no strict certificate.
The output dual must be checked by the standard-library receiver.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import json
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from flow_grid import geometry, word_feature, endpoint_coefficient


def compile_certificate(data, mesh, max_states=400):
    start = time.perf_counter()
    alphabet, depth = data['alphabet_size'], data['depth']
    leaves, nodes, descriptors, words = geometry(alphabet, depth, mesh, max_states)
    p = list(map(Q, data['probabilities']))
    assert len(p) == len(words) and min(p) >= 0 and sum(p) == 1
    n, d, nw = len(nodes), len(descriptors), len(words)
    edges = [(i, j) for i in range(n) for j in range(i, n)]
    nf, nr = len(edges), n * d + 2 * nw
    ri, ci, vv = [], [], []
    norm = np.zeros(nf + 1)
    # Coefficients are rational in the verifier. Floating values only find
    # a proposed dual through HiGHS.
    F = np.array([[float(word_feature(node, word, leaves, depth, mesh)) for node in nodes] for word in words])
    # Cache the prefix values so each flow column has cheap endpoint rows.
    coefficients = np.empty((n, n, d))
    for i, node in enumerate(nodes):
        for j, other in enumerate(nodes):
            coefficients[i, j] = [float(endpoint_coefficient(node, other, desc, leaves, mesh)) for desc in descriptors]
    for col, (i, j) in enumerate(edges):
        norm[col] = 1 if i == j else 2
        for current, other in ((i, j),) if i == j else ((i, j), (j, i)):
            for r, value in enumerate(coefficients[current, other]):
                if value:
                    ri.append(d * current + r); ci.append(col); vv.append(value)
        values = F[:, i] if i == j else F[:, i] + F[:, j]
        for widx, value in enumerate(values):
            if value:
                for side, sign in enumerate((1., -1.)):
                    ri.append(n * d + 2 * widx + side); ci.append(col); vv.append(sign * value)
    for row in range(n * d, nr):
        ri.append(row); ci.append(nf); vv.append(-1.)
    A = coo_matrix((vv, (ri, ci)), shape=(nr, nf + 1)).tocsr()
    rhs = np.zeros(nr)
    for i, prob in enumerate(p):
        rhs[n * d + 2 * i] = float(prob)
        rhs[n * d + 2 * i + 1] = -float(prob)
    objective = np.zeros(nf + 1); objective[-1] = 1.
    opt = linprog(objective, A_ub=A, b_ub=rhs, A_eq=norm[None, :], b_eq=[1.], bounds=(0, None), method='highs')
    result = {'scope': __doc__, 'alphabet_size': alphabet, 'depth': depth, 'mesh': mesh, 'probabilities': list(map(str, p)), 'grid_states': n, 'symmetric_flow_columns': nf, 'conditional_rows': n * d, 'solver_status': opt.message, 'seconds': time.perf_counter() - start}
    if not opt.success:
        result['certificate_status'] = 'NO_CERTIFICATE_SOLVER_FAILURE'
        return result
    result['raw_distance_Linfinity'] = float(opt.fun)
    if opt.fun <= 1e-10:
        result['certificate_status'] = 'NO_STRICT_CERTIFICATE_AT_THIS_GRID'
        return result
    y = [min(Q(0), Q(str(float(x))).limit_denominator(10 ** 7)) for x in opt.ineqlin.marginals]
    tcoef = -sum(y[n * d:], Q(0))
    if tcoef > 1:
        y = [a / tcoef for a in y]
    yd = [y[n * d + 2 * w] - y[n * d + 2 * w + 1] for w in range(nw)]
    rdata = [sum((coef * word_feature(node, word, leaves, depth, mesh) for coef, word in zip(yd, words)), Q(0)) for node in nodes]

    def endpoint(i, j):
        return rdata[i] + sum((y[d * i + r] * endpoint_coefficient(nodes[i], nodes[j], desc, leaves, mesh) for r, desc in enumerate(descriptors) if y[d * i + r]), Q(0))

    z = min(-endpoint(i, j) if i == j else -(endpoint(i, j) + endpoint(j, i)) / 2 for i, j in edges)
    gap = z + sum((a * prob for a, prob in zip(yd, p)), Q(0))
    result.update({'row_duals': list(map(str, y[:n * d])), 'data_duals': list(map(str, y[n * d:])), 'normalization_dual': str(z), 'exact_source_gap': str(gap), 'word_statistic': list(map(str, [-z - a for a in yd])), 'certificate_status': 'RATIONAL_DUAL_PROPOSED' if gap > 0 else 'RATIONALIZATION_DID_NOT_CERTIFY', 'seconds': time.perf_counter() - start})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--mesh', type=int, default=8)
    parser.add_argument('--max-states', type=int, default=400)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = compile_certificate(json.loads(args.input.read_text()), args.mesh, args.max_states)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ['probabilities', 'row_duals', 'data_duals', 'normalization_dual', 'word_statistic', 'scope']}, indent=2))


if __name__ == '__main__':
    main()
