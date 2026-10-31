"""Numerical convex entropy program on an all-hidden predictive simplex grid.

This implements the outer lower programs in PROOF.txt for any supplied finite
alphabet and word depth within the explicit execution-size cap. Solver output
is diagnostic; an exact entropy-dual verifier is not provided by this driver.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import argparse
import json
import time
import numpy as np
import cvxpy as cp
from flow_grid import geometry, prefix, word_feature


def solve(data, mesh, max_states=250):
    start = time.perf_counter()
    s, depth = data['alphabet_size'], data['depth']
    leaves, nodes, descriptors, words = geometry(s, depth, mesh, max_states)
    p = list(map(Q, data['probabilities']))
    assert len(p) == len(words) and min(p) >= 0 and sum(p) == 1
    n = len(nodes)
    J = cp.Variable((n, n), nonneg=True)
    mu = cp.sum(J, axis=1)
    constraints = [mu == cp.sum(J, axis=0), cp.sum(J) == 1]
    prefixes = [w for length in range(depth) for w in product(range(s), repeat=length)]
    for side in (0, 1):
        for b in range(s):
            for word in prefixes:
                next_feature = np.array([float(prefix(node, side, word, leaves, mesh)) if node[0] == b else 0. for node in nodes])
                current = np.array([float(prefix(node, side, (b,) + word, leaves, mesh)) for node in nodes])
                flow = (J if side == 0 else J.T) @ next_feature
                residual = flow - cp.multiply(mu, current)
                constraints.extend([residual <= mu / mesh, -residual <= mu / mesh])
    F = np.array([[float(word_feature(node, word, leaves, depth, mesh)) for node in nodes] for word in words])
    constraints.append(F @ mu == np.array(list(map(float, p))))
    epigraph = cp.Variable((n, n))
    cone = cp.ExpCone(-epigraph, J, J.T)
    problem = cp.Problem(cp.Minimize(cp.sum(epigraph)), constraints + [cone])
    value = problem.solve(solver='CLARABEL', max_iter=150, tol_gap_abs=1e-8, tol_feas=1e-8, tol_gap_rel=1e-8)
    residual = max(float(np.max(c.violation())) for c in constraints) if J.value is not None else None
    return {'scope': __doc__, 'alphabet_size': s, 'depth': depth, 'mesh': mesh, 'grid_states': n, 'flow_entries': n * n, 'solver_status': problem.status, 'raw_epigraph_objective': float(value), 'maximum_linear_constraint_violation': residual, 'scientific_bound_status': 'NUMERICAL_ONLY_NOT_AN_EXACT_ENTROPY_DUAL_CERTIFICATE', 'hidden_architecture_input': None, 'seconds': time.perf_counter() - start}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--mesh', type=int, default=8)
    parser.add_argument('--max-states', type=int, default=250)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = solve(json.loads(args.input.read_text()), args.mesh, args.max_states)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'scope'}, indent=2))


if __name__ == '__main__':
    main()
