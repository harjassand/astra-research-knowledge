"""Independent finite normalization diagnostics for the SU(m) frame.

NumPy only. This does not prove an all-N statement or optimize a memory code.
SU4 carriers are highest-Casimir components of fundamental exterior tensor
powers; SU3 uses the earlier independent contraction-kernel constructor.
"""
import importlib.util
import itertools
import json
import math
import pathlib
from fractions import Fraction

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "old_controls", ROOT.parent / "verify_operational.py")
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
spec3 = importlib.util.spec_from_file_location(
    "su3_controls", ROOT.parent / "regular_su3" / "verify_regular_su3.py")
su3 = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(su3)


def close(value, expected, tolerance=2e-9):
    err = float(np.max(np.abs(value - expected)))
    if err > tolerance:
        raise AssertionError((err, value, expected))
    return err


def highest_diagonal(labels):
    raw = np.array([sum(labels[i:]) for i in range(len(labels))] + [0.])
    return raw - raw.mean()


def weyl_dimension(labels):
    m, answer = len(labels) + 1, Fraction(1)
    for i in range(m):
        for j in range(i + 1, m):
            answer *= Fraction(j - i + sum(labels[i:j]), j - i)
    assert answer.denominator == 1
    return int(answer)


def wedge_lift(t, degree):
    """Exterior generator, built directly from occupation replacement signs."""
    basis = list(itertools.combinations(range(t.shape[0]), degree))
    index = {beta: j for j, beta in enumerate(basis)}
    result = np.zeros((len(basis), len(basis)), complex)
    for col, beta in enumerate(basis):
        for position, j in enumerate(beta):
            result[col, col] += t[j, j]
            rest = list(beta)
            rest.pop(position)
            for i in range(t.shape[0]):
                if i == j or i in rest:
                    continue
                gamma = tuple(sorted(rest + [i]))
                replacement_position = gamma.index(i)
                result[index[gamma], col] += (
                    (-1) ** (position + replacement_position) * t[i, j])
    return result


def product_highest_component(labels):
    """Fixed small tensor construction; does not assume a Gram formula."""
    m = len(labels) + 1
    fund = old.generators(m)
    factors = []
    for degree, count in enumerate(labels, 1):
        factors.extend([[wedge_lift(t, degree) for t in fund]] * count)
    assert factors
    sizes = [factor[0].shape[0] for factor in factors]
    ambient = math.prod(sizes)
    full = []
    for a in range(m * m - 1):
        lifted = np.zeros((ambient, ambient), complex)
        for position in range(len(factors)):
            term = np.array([[1.]], complex)
            for j, factor in enumerate(factors):
                term = np.kron(term, factor[a] if j == position else np.eye(sizes[j]))
            lifted += term
        full.append(lifted)
    casimir = sum(t @ t for t in full)
    vals, vectors = np.linalg.eigh(casimir)
    mask = np.abs(vals - vals[-1]) < 1e-8
    basis = vectors[:, mask]
    dimension = weyl_dimension(labels)
    assert basis.shape == (ambient, dimension)
    # Lexicographically first occupation is highest in every exterior factor.
    highest = basis.conj().T[:, 0]
    assert abs(np.linalg.norm(highest) - 1.) < 1e-10
    ts = [basis.conj().T @ t @ basis for t in full]
    return ts, highest, ambient


def carrier(m, labels):
    if m == 2:
        basis = list(old.occupations(labels[0], 2))
        ts = [old.lift(t, basis) for t in old.generators(2)]
        highest = np.eye(len(basis), dtype=complex)[:, 0]
        return ts, highest, len(basis)
    if m == 3:
        ts, ambient = su3.harmonic_carrier(*labels)
        # A generic interior Cartan has the unique highest eigenvector.
        h = np.diag([2., -.3, -1.7])
        coords = [float((2 * np.trace(t @ h)).real) for t in old.generators(3)]
        _, vecs = np.linalg.eigh(sum(x * t for x, t in zip(coords, ts)))
        return ts, vecs[:, -1], ambient
    return product_highest_component(labels)


def frame_case(m, labels):
    fund = old.generators(m)
    ts, psi, ambient = carrier(m, labels)
    dimension = ts[0].shape[0]
    n = max(labels)
    q, p = m * m - 1, m - 1
    c_f = q / (2 * m)
    means = np.array([float(np.vdot(psi, t @ psi).real) / n for t in ts])
    xi = sum(a * t for a, t in zip(means, fund))
    normalized_labels = highest_diagonal(labels) / n
    rho = np.arange(m - 1, -m, -2) / 2
    beta = float(normalized_labels @ rho)
    c_n = n ** 2 * np.sum(normalized_labels ** 2) / 2 + n * beta
    b = math.sqrt(c_f * c_n) / n
    checks = dict(
        fundamental_normalization=close(np.array([[np.trace(t @ u) for u in fund]
                                                  for t in fund]), np.eye(q) / 2),
        highest_mean=close(xi, np.diag(normalized_labels / 2)),
        casimir=close(sum(t @ t for t in ts), c_n * np.eye(dimension)),
        highest_variance=close(sum(np.linalg.norm(t @ psi / n - a * psi) ** 2
                                  for t, a in zip(ts, means)), beta / n))
    x = sum(np.kron(t, u) for t, u in zip(fund, ts)) / n
    assert np.linalg.norm(x, 2) <= b + 1e-10
    y, symbols = [], []
    power = np.eye(m * dimension, dtype=complex)
    xi_power = np.eye(m, dtype=complex)
    for s in range(1, p + 1):
        power = power @ x
        xi_power = xi_power @ xi
        blocks = power.reshape(m, dimension, m, dimension)
        y.append([2 * np.einsum('ij,jxiy->xy', t, blocks) for t in fund])
        symbols.append(np.array([float((2 * np.trace(t @ xi_power)).real)
                                 for t in fund]))
        # Check the vector-error estimate prior to the central Gram step.
        deviation = sum(np.linalg.norm(u @ psi - z * psi) ** 2
                        for u, z in zip(y[-1], symbols[-1]))
        bound = q ** 2 * beta * s ** 2 * b ** (2 * s - 2) / n
        assert deviation <= bound + 1e-8
    checks['Y1'] = close(y[0], np.array(ts) / n)
    checks['hermiticity'] = max(close(u, u.conj().T) for group in y for u in group)
    f = np.array([[[float((-2j * np.trace((fund[a] @ fund[b] - fund[b] @ fund[a])
                                         @ fund[k])).real) for k in range(q)]
                   for b in range(q)] for a in range(q)])
    checks['adjoint_covariance'] = max(
        close(ts[a] @ group[b] - group[b] @ ts[a],
              1j * sum(f[a, b, k] * group[k] for k in range(q)))
        for group in y for a in range(q) for b in range(q))
    gram, central = np.zeros((p, p)), 0.
    for s in range(p):
        for t in range(p):
            component_gram = np.array([[np.trace(u @ v) / dimension
                                       for v in y[t]] for u in y[s]])
            gram[s, t] = float(np.trace(component_gram).real) / q
            central = max(central, close(component_gram, gram[s, t] * np.eye(q)))
            z = sum((u @ v + v @ u) / 2 for u, v in zip(y[s], y[t]))
            central = max(central, close(z, q * gram[s, t] * np.eye(dimension)))
            central = max(central, close(np.vdot(psi, z @ psi), q * gram[s, t]))
    checks['central_gram_and_normalized_trace'] = central
    if p >= 2:
        dsymbol = np.array([[[float((2 * np.trace(fund[a] @
                            (fund[b] @ fund[k] + fund[k] @ fund[b]))).real)
                             for k in range(q)] for b in range(q)] for a in range(q)])
        checks['exact_Y2_linear_correction'] = max(close(y[1][a],
            (sum(dsymbol[a, j, k] * ts[j] @ ts[k] / 2
                 for j in range(q) for k in range(q)) - m * ts[a] / 4) / n ** 2)
            for a in range(q))
    classical = np.array(symbols) @ np.array(symbols).T
    eigenvalues = np.linalg.eigvalsh(gram)
    regular = min(labels) > 0
    if regular:
        assert eigenvalues[0] > 1e-10
    else:
        assert eigenvalues[0] < 1e-10
    for s in range(p):
        for t in range(p):
            u_s, u_t = math.sqrt(2 * m) * b ** (s + 1), math.sqrt(2 * m) * b ** (t + 1)
            v_s = q * math.sqrt(beta) * (s + 1) * b ** s
            v_t = q * math.sqrt(beta) * (t + 1) * b ** t
            bound = (u_s * v_t + u_t * v_s) / math.sqrt(n) + v_s * v_t / n
            assert abs(q * gram[s, t] - classical[s, t]) <= bound + 1e-9
    rng = np.random.default_rng(5131 + m + sum(labels))
    ratios = np.zeros(p)
    parseval_residual = 0.
    for _ in range(5):
        a = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
        a /= np.linalg.norm(a)
        e = old.energy(a, ts)
        comm = x @ np.kron(np.eye(m), a) - np.kron(np.eye(m), a) @ x
        parseval_residual = max(parseval_residual, close(np.linalg.norm(comm) ** 2, e / (2 * n ** 2)))
        for s, group in enumerate(y, 1):
            observed = old.energy(a, group)
            bound = s ** 2 * b ** (2 * s - 2) * e / n ** 2
            assert observed <= bound + 1e-9
            ratios[s - 1] = max(ratios[s - 1], observed / bound)
    checks['fundamental_commutator_parseval'] = parseval_residual
    return dict(m=m, labels=labels, N=n, dimension=dimension, ambient_dimension=ambient,
                regular=regular, C2=c_n, highest_variance=beta / n,
                Gram=gram.tolist(), classical_Gram=classical.tolist(),
                Gram_eigenvalues=eigenvalues.tolist(),
                max_random_energy_to_bound_ratio=ratios.tolist(), residuals=checks)


def determinant_fraction(matrix):
    n = len(matrix)
    answer = Fraction(0)
    for perm in itertools.permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = Fraction((-1) ** inversions)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        answer += term
    return answer


def vandermonde_arithmetic():
    count = 0
    for m in range(2, 7):
        for shift in range(1, 5):
            labels = [Fraction(shift + i % 2, shift + 1) for i in range(m - 1)]
            raw = [sum(labels[i:], Fraction(0)) for i in range(m - 1)] + [Fraction(0)]
            mean = sum(raw) / m
            eta = [(x - mean) / 2 for x in raw]
            h = [[2 * (sum(x ** (s + t) for x in eta)
                       - sum(x ** s for x in eta) * sum(x ** t for x in eta) / m)
                  for t in range(1, m)] for s in range(1, m)]
            expected = Fraction(2 ** (m - 1), m)
            for i in range(m):
                for j in range(i + 1, m):
                    expected *= (eta[i] - eta[j]) ** 2
            assert determinant_fraction(h) == expected > 0
            count += 1
    return count


def main():
    cases = [(2, [1]), (2, [3]), (2, [6]),
             (3, [1, 1]), (3, [2, 1]), (3, [2, 2]), (3, [3, 3]),
             (4, [1, 1, 1]), (4, [2, 1, 1]),
             (4, [1, 0, 1]), (4, [1, 0, 0])]
    carriers = [frame_case(m, labels) for m, labels in cases]
    result = dict(status='FINITE-EVIDENCE', proof_validation=False,
                  theorem_file='RESULT.txt', exact_vandermonde_cases=vandermonde_arithmetic(),
                  carrier_cases=carriers, random_commutator_controls=5 * len(carriers),
                  dependencies=['Python standard library', 'NumPy'],
                  max_matrix_residual=max(max(case['residuals'].values()) for case in carriers))
    (ROOT / 'CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='passed', carrier_cases=len(carriers),
                         regular_carriers=sum(case['regular'] for case in carriers),
                         wall_controls=sum(not case['regular'] for case in carriers),
                         exact_vandermonde_cases=result['exact_vandermonde_cases'],
                         max_matrix_residual=result['max_matrix_residual'])))


if __name__ == '__main__':
    main()
