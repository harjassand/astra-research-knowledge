"""CPTP-extension diagnostic for the actual homogeneous-source reachable family.

Requires cvxpy; this run installs it separately in /tmp/weak_stream_deps.
No feasibility result is treated as an analytic construction or certificate.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import cvxpy as cp

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
PAULIS = [I, X, Y, Z]
BELL_VECTOR = np.array([1, 0, 0, 1], complex) / np.sqrt(2)
BELL = np.outer(BELL_VECTOR, BELL_VECTOR.conj())
SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0],
                 [0, 1, 0, 0], [0, 0, 0, 1]], complex)


def apply_two(matrix, operation, a, b, n):
    rest = [i for i in range(n) if i not in [a, b]]
    axes = [a, b] + rest + [n+a, n+b] + [n+i for i in rest]
    tensor = matrix.reshape([2] * (2*n)).transpose(axes).reshape(
        4, 2**(n-2), 4, 2**(n-2))
    tensor = np.einsum('ia,arbs,jb->irjs', operation, tensor,
                       operation.conj(), optimize=True)
    return tensor.reshape([2] * (2*n)).transpose(np.argsort(axes)).reshape(2**n, 2**n)


def virtual_step(family, theta):
    c, s = np.cos(theta), np.sin(theta)
    source = c * np.eye(4) + 1j * s * SWAP
    crossed = c * np.eye(4) - 2j * s * BELL
    before, after = [], []
    for matrix in family:
        incoming = apply_two(np.kron(matrix, I/2), source, 0, 3, 4)
        updated = apply_two(incoming, crossed, 2, 3, 4)
        updated = np.trace(updated.reshape(8, 2, 8, 2), axis1=1, axis2=3)
        before.append(incoming)
        after.append(updated)
    return before, after


def source_coefficients(matrix, memory_dimension):
    tensor = matrix.reshape(2, memory_dimension, 2, memory_dimension)
    return [np.einsum('ab,biaj->ij', pauli, tensor) for pauli in PAULIS]


def weighted_chi_square(family):
    baseline = family[0]
    values, vectors = np.linalg.eigh(baseline)
    inverse = np.zeros_like(values)
    inverse[values > 1e-13] = 1 / values[values > 1e-13]
    inverse = (vectors * inverse) @ vectors.conj().T
    return float(np.trace(family[3] @ family[3] @ inverse).real)


def extension(before, target, solver, approximate):
    input_dimension, output_dimension = 8, 4
    choi = cp.Variable((32, 32), hermitian=True)
    constraints = [choi >> 0]
    for a in range(input_dimension):
        for b in range(input_dimension):
            block = choi[4*a:4*a+4, 4*b:4*b+4]
            constraints.append(cp.trace(block) == (1 if a == b else 0))
    pairs = []
    for incoming, outgoing in zip(before, target):
        pairs.extend(zip(source_coefficients(incoming, 8),
                         source_coefficients(outgoing, 4)))
    x = np.column_stack([pair[0].reshape(-1) for pair in pairs])
    y = np.column_stack([pair[1].reshape(-1) for pair in pairs])
    u, singular, vh = np.linalg.svd(x, full_matrices=False)
    keep = singular > 1e-11 * singular[0]
    transform = vh.conj().T[:, keep] / singular[keep]
    reduced_x = x @ transform
    reduced_y = y @ transform
    deviations = []
    for k in range(reduced_x.shape[1]):
        incoming = reduced_x[:, k].reshape(8, 8)
        wanted = reduced_y[:, k].reshape(4, 4)
        mapped = sum(incoming[a, b] * choi[4*a:4*a+4, 4*b:4*b+4]
                     for a in range(8) for b in range(8))
        if approximate:
            deviations.append(cp.sum_squares(cp.abs(mapped - wanted)))
        else:
            constraints.append(mapped == wanted)
    problem = cp.Problem(cp.Minimize(sum(deviations) if approximate else 0), constraints)
    options = dict(verbose=False)
    if solver == 'SCS':
        options.update(eps=2e-8, max_iters=100000)
    elif solver == 'CLARABEL':
        options.update(tol_gap_abs=1e-8, tol_feas=1e-8, max_iter=150)
    problem.solve(solver=solver, **options)
    result = {"status": problem.status,
              "objective": problem.value if problem.value is not None and math.isfinite(problem.value) else None,
              "reachable_operator_span_rank": int(np.sum(keep)),
              "span_singular_values": singular.tolist(),
              "solver": solver,
              "solver_time": problem.solver_stats.solve_time,
              "objective_is_orthonormal_span_squared_Frobenius_error": bool(approximate)}
    if choi.value is not None:
        j = choi.value
        result['minimum_choi_eigenvalue'] = float(np.min(np.linalg.eigvalsh(j)))
        result['tp_residual'] = float(np.linalg.norm(
            np.array([[np.trace(j[4*a:4*a+4, 4*b:4*b+4]) for b in range(8)]
                      for a in range(8)]) - np.eye(8)))
        error = 0.0
        for incoming, wanted in pairs:
            mapped = sum(incoming[a, b] * j[4*a:4*a+4, 4*b:4*b+4]
                         for a in range(8) for b in range(8))
            error = max(error, np.linalg.norm(mapped - wanted))
        result['maximum_original_constraint_frobenius_error'] = float(error)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--theta', type=float, default=0.3)
    parser.add_argument('--steps', type=int, nargs='+', default=[1, 2, 3])
    parser.add_argument('--solver', choices=['SCS', 'CLARABEL'], default='CLARABEL')
    parser.add_argument('--approximate', action='store_true')
    args = parser.parse_args()
    family = [np.kron(pauli / 2, BELL) for pauli in PAULIS]
    records = []
    for step in range(1, max(args.steps) + 1):
        chi_before = weighted_chi_square(family)
        before, target = virtual_step(family, args.theta)
        chi_after = weighted_chi_square(target)
        if step in args.steps:
            record = extension(before, target, args.solver, args.approximate)
            record.update(theta=args.theta, step=step,
                          weighted_chi_square_before=chi_before,
                          weighted_chi_square_after=chi_after,
                          virtual_trace_errors=[float(abs(np.trace(target[k]) - (1 if k == 0 else 0)))
                                                for k in range(4)])
            records.append(record)
            print(json.dumps(record), flush=True)
        family = target
    suffix = ('approx' if args.approximate else 'exact') + '_' + str(args.theta).replace('.', 'p')
    Path(__file__).with_name('crossed_extension_' + suffix + '.json').write_text(
        json.dumps(records, indent=2) + '\n')


if __name__ == '__main__':
    main()
