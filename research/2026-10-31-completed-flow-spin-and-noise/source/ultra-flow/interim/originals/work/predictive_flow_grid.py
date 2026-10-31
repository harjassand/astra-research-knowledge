"""Finite convex predictive-flow programs for an exact binary triple law.

Mesh-tolerant levels are universal lower programs, not hidden-size fits.
The zero-tolerance grid is an inner construction and is labeled separately.
Floating solver diagnostics do not replace the analytic lower certificates.
"""
from pathlib import Path
from itertools import product
import importlib.util
import json
import time
import numpy as np
import cvxpy as cp


def solve(k, tolerant=True):
    start = time.perf_counter()
    nodes = np.array(list(product(range(2), range(k + 1), range(k + 1))), dtype=float)
    lab, plus, minus = nodes[:, 0], nodes[:, 1] / k, nodes[:, 2] / k
    n = len(nodes)
    J = cp.Variable((n, n), nonneg=True)
    mu = cp.sum(J, axis=1)
    h = 1 / k if tolerant else 0.
    constraints = [cp.sum(J) == 1, mu == cp.sum(J, axis=0)]
    constraints += [J @ lab - cp.multiply(mu, plus) <= h * mu, cp.multiply(mu, plus) - J @ lab <= h * mu]
    constraints += [J.T @ lab - cp.multiply(mu, minus) <= h * mu, cp.multiply(mu, minus) - J.T @ lab <= h * mu]
    for u, a, v in product(range(2), repeat=3):
        feature = (lab == a) * (minus if u else 1 - minus) * (plus if v else 1 - plus)
        target = (1 - .25 * (1 - 2 * u) * (1 - 2 * v)) / 8
        constraints.append(feature @ mu == target)
    # Evaluate the affine epigraph objective after solve. Directly evaluating
    # rel_entr on a returned matrix can report +inf when a numerically tiny
    # reverse entry is clipped to zero, despite an accurate cone solution.
    epigraph = cp.Variable((n, n))
    constraints.append(cp.ExpCone(-epigraph, J, J.T))
    problem = cp.Problem(cp.Minimize(cp.sum(epigraph)), constraints)
    value = problem.solve(solver='CLARABEL', max_iter=150, tol_gap_abs=1e-8, tol_feas=1e-8, tol_gap_rel=1e-8)
    residual = max(float(np.max(c.violation())) for c in constraints[:-1]) if J.value is not None else None
    out = {'mesh': k, 'grid_states': n, 'flow_variables': n * n, 'row_tolerance': h, 'kind': 'universal_outer_lower_program' if tolerant else 'inner_exact_grid_model', 'solver_status': problem.status, 'objective_numeric': float(value), 'maximum_constraint_violation': residual, 'analytic_true_minimum': float(np.log(3) / 2), 'proof_of_new_global_bound': False, 'seconds': time.perf_counter() - start}
    print(json.dumps(out), flush=True)
    return out


def main():
    rows = []
    for k in (1, 2, 4, 8):
        rows.append(solve(k))
    rows.append(solve(4, tolerant=False))
    Path(__file__).with_suffix('.json').write_text(json.dumps({'scope': __doc__, 'levels': rows}, indent=2) + '\n')


if __name__ == '__main__':
    main()
