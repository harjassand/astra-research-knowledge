"""Fixed-size independent matrix checks of crossed_statistic_obstruction.txt.

NumPy only. These checks validate the closed formulas and finite evaluation;
the data-processing argument is analytic. No all-output receiver is simulated.
"""
import json
import math
from pathlib import Path
import numpy as np

I = np.eye(2, dtype=complex)
P = [np.array([[0, 1], [1, 0]], complex),
     np.array([[0, -1j], [1j, 0]], complex), np.diag([1, -1])]
PHI = np.array([[1, 0, 0, 1], [0, 0, 0, 0],
                [0, 0, 0, 0], [1, 0, 0, 1]], complex) / 2
SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0],
                 [0, 1, 0, 0], [0, 0, 0, 1]], complex)
S = [np.kron(np.kron(p, I), I) for p in P]
R = [np.kron(np.kron(I, p), I) for p in P]
A = [np.kron(np.kron(I, I), p) for p in [P[0], -P[1], P[2]]]
Q = sum(S[a] @ A[a] for a in range(3))


def embed_two(operation, a, b, n):
    result = np.zeros((2**n, 2**n), complex)
    for r in range(2**n):
        rb = [(r >> (n - 1 - j)) & 1 for j in range(n)]
        for c in range(2**n):
            cb = [(c >> (n - 1 - j)) & 1 for j in range(n)]
            if all(rb[j] == cb[j] for j in range(n) if j not in [a, b]):
                result[r, c] = operation[2 * rb[a] + rb[b], 2 * cb[a] + cb[b]]
    return result


def direct_step(matrix, theta):
    c, s = math.cos(theta), math.sin(theta)
    source = embed_two(c * np.eye(4) + 1j * s * SWAP, 0, 3, 4)
    crossed = embed_two(c * np.eye(4) - 2j * s * PHI, 2, 3, 4)
    op = crossed @ source
    updated = op @ np.kron(matrix, I / 2) @ op.conj().T
    return np.trace(updated.reshape(8, 2, 8, 2), axis1=1, axis2=3)


def coefficients(theta, n):
    c, s = math.cos(theta), math.sin(theta)
    return (c**(2*n), (1-s**4)**n, (c*c*math.cos(2*theta))**n,
            n*c**(2*n-1)*s**3 if n else 0.0)


def formula(theta, n):
    u, v, w, h = coefficients(theta, n)
    baseline = np.kron(I / 2, u * PHI + (1-u) * np.eye(4) / 4)
    delta = u * S[2] + (1-v) * R[2] + v * R[2] @ Q / 3
    for a in range(3):
        delta += u * R[a] @ (S[2] @ A[a] - S[a] @ A[2]) / 2
        symmetric = (S[2] @ A[a] + S[a] @ A[2]) / 2
        if a == 2:
            symmetric -= Q / 3
        delta += w * R[a] @ symmetric
    delta += h * (R[0] @ (S[1] - A[1]) - R[1] @ (S[0] - A[0]))
    return baseline, delta / 8


def chi_formula(theta, n):
    u, v, w, h = coefficients(theta, n)
    return (36*h*h*u+24*h*h+9*u**3-12*u*u*v-30*u*u*w+12*u*u
            +16*u*v*v-24*u*v+5*u*w*w+12*u+8*v*v-12*v+10*w*w+6) / (
                6*(1-u)*(3*u+1))


def main():
    matrix_residual, chi_residual, norm_bound_excess = 0.0, 0.0, 0.0
    checks = 0
    for theta in [.03, .1, .3, .7, 1.1]:
        baseline, delta = np.kron(I / 2, PHI), np.kron(P[2] / 2, PHI)
        for n in range(1, 21):
            baseline, delta = direct_step(baseline, theta), direct_step(delta, theta)
            exact_base, exact_delta = formula(theta, n)
            matrix_residual = max(matrix_residual, np.linalg.norm(baseline-exact_base),
                                  np.linalg.norm(delta-exact_delta))
            chi_direct = np.trace(delta @ delta @ np.linalg.inv(baseline)).real
            chi_residual = max(chi_residual, abs(chi_direct-chi_formula(theta, n)))
            u, v, w, h = coefficients(theta, n)
            limit_norm = (1+3*abs(1-4*v/3))/4
            norm = np.linalg.norm(delta, ord='nuc')
            bound = 3*u+(10/3)*abs(w)+4*abs(h)
            norm_bound_excess = max(norm_bound_excess, abs(norm-limit_norm)-bound)
            checks += 1
    theta = .1
    n = math.ceil(math.log(.75) / math.log(1-math.sin(theta)**4))
    u, v, w, h = coefficients(theta, n)
    baseline, delta = formula(theta, n)
    limit_norm = (1+3*abs(1-4*v/3))/4
    bound = 3*u+(10/3)*abs(w)+4*abs(h)
    result = {
        'scope': 'Fixed-size virtual-statistic formula; no physical receiver claim',
        'direct_matrix_cases': checks,
        'maximum_frobenius_formula_residual': float(matrix_residual),
        'maximum_chi_formula_residual': float(chi_residual),
        'maximum_trace_norm_bound_violation': float(norm_bound_excess),
        'finite_point': {'theta': theta, 'prefix_collisions': n,
                         'u': u, 'v': v, 'w': w, 'h': h,
                         'virtual_input_Z_distinguishability': float(np.linalg.norm(delta, ord='nuc')),
                         'rigorous_analytic_upper_bound': limit_norm+bound,
                         'half_diamond_error_floor_for_any_continuation': (1-limit_norm-bound)/2},
        'interpretation': 'Any real receiver matching this joint source/statistic at the cut loses the stated payload information irreversibly. Different statistics remain open.'}
    assert matrix_residual < 1e-12
    assert chi_residual < 1e-9
    assert norm_bound_excess < 1e-12
    Path(__file__).with_name('crossed_statistic_verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
