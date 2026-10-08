"""Small deterministic normalization checks for the regular SU(3) proof.

This is finite evidence, not a proof of the operational optimum.  NumPy only.
The carrier (a,b) is constructed as the contraction kernel in
Sym^a(3) tensor Sym^b(3bar), independently of the central-element formulas.
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


def residual(value, expected, tolerance=3e-9):
    err = float(np.max(np.abs(value - expected)))
    if err > tolerance:
        raise AssertionError((err, value, expected))
    return err


fundamental = old.generators(3)
d_symbol = np.array([[[float((2 * np.trace(
    (fundamental[b] @ fundamental[c] + fundamental[c] @ fundamental[b])
    @ fundamental[a])).real) for c in range(8)] for b in range(8)]
    for a in range(8)])
f_symbol = np.array([[[float((-2j * np.trace(
    (fundamental[a] @ fundamental[b] - fundamental[b] @ fundamental[a])
    @ fundamental[c])).real) for c in range(8)] for b in range(8)]
    for a in range(8)])


def harmonic_carrier(a, b):
    left = list(old.occupations(a, 3))
    right = list(old.occupations(b, 3))
    full = [np.kron(old.lift(t, left), np.eye(len(right)))
            - np.kron(np.eye(len(left)), old.lift(t, right).T)
            for t in fundamental]
    ambient = len(left) * len(right)
    if a and b:
        lower_left = list(old.occupations(a - 1, 3))
        lower_right = list(old.occupations(b - 1, 3))
        row_index = {pair: i for i, pair in enumerate(
            itertools.product(lower_left, lower_right))}
        contraction = np.zeros((len(row_index), ambient), complex)
        for col, (alpha, beta) in enumerate(itertools.product(left, right)):
            for j in range(3):
                if alpha[j] and beta[j]:
                    u, v = list(alpha), list(beta)
                    u[j] -= 1
                    v[j] -= 1
                    contraction[row_index[(tuple(u), tuple(v))], col] += math.sqrt(
                        alpha[j] * beta[j])
        _, singular, vh = np.linalg.svd(contraction, full_matrices=True)
        rank = int(np.count_nonzero(singular > 1e-10))
        assert rank == len(row_index)
        basis = vh[rank:].conj().T
        assert np.linalg.norm(contraction @ basis) < 1e-10
    else:
        basis = np.eye(ambient, dtype=complex)
    dimension = (a + 1) * (b + 1) * (a + b + 2) // 2
    assert basis.shape == (ambient, dimension)
    return [basis.conj().T @ t @ basis for t in full], ambient


def arithmetic():
    count = 0
    for a in range(25):
        for b in range(25):
            if not a + b:
                continue
            c2 = Fraction(a * a + a * b + b * b + 3 * a + 3 * b, 3)
            c3 = Fraction((a - b) * (2 * a + b + 3) * (a + 2 * b + 3), 18)
            delta = c2 * (c2 / 3 + Fraction(1, 4)) - c3 * c3 / c2
            factor = Fraction(a * b * (a + 2) * (b + 2)
                              * (a + b + 1) * (a + b + 3), 12) / c2
            assert delta == factor
            assert (delta > 0) == (a > 0 and b > 0)
            count += 1
    return count


def carrier_case(a, b):
    ts, ambient = harmonic_carrier(a, b)
    dimension = ts[0].shape[0]
    n = max(a, b, 1)
    c2 = (a * a + a * b + b * b + 3 * a + 3 * b) / 3
    c3 = (a - b) * (2 * a + b + 3) * (a + 2 * b + 3) / 18
    alpha = c3 / c2
    delta = c2 * (c2 / 3 + .25) - c3 * c3 / c2
    ds = [sum(d_symbol[k, i, j] * ts[i] @ ts[j]
              for i in range(8) for j in range(8)) for k in range(8)]
    ss = [(d - alpha * t) / n for d, t in zip(ds, ts)]
    cs = delta / n ** 2
    checks = {}
    checks['casimir'] = residual(sum(t @ t for t in ts), c2 * np.eye(dimension))
    checks['cubic'] = residual(sum(t @ d for t, d in zip(ts, ds)), c3 * np.eye(dimension))
    checks['quartic'] = residual(sum(d @ d for d in ds),
                                c2 * (c2 / 3 + .25) * np.eye(dimension))
    checks['orthogonal_gram'] = residual(
        np.array([[np.trace(t @ s) for s in ss] for t in ts]), np.zeros((8, 8)))
    checks['second_gram'] = residual(
        np.array([[np.trace(s @ u) for u in ss] for s in ss]),
        dimension * cs / 8 * np.eye(8))
    checks['second_casimir'] = residual(sum(s @ s for s in ss), cs * np.eye(dimension))
    checks['lie_relations'] = max(residual(
        ts[i] @ ts[j] - ts[j] @ ts[i],
        1j * sum(f_symbol[i, j, k] * ts[k] for k in range(8)))
        for i in range(8) for j in range(8))
    checks['adjoint_covariance'] = max(residual(
        ts[i] @ ss[j] - ss[j] @ ts[i],
        1j * sum(f_symbol[i, j, k] * ss[k] for k in range(8)))
        for i in range(8) for j in range(8))
    rng = np.random.default_rng(20261008 + 31 * a + b)
    max_energy_ratio, max_modulus_residual = 0., 0.
    for _ in range(12):
        x = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
        x /= np.linalg.norm(x)
        et, es = old.energy(x, ts), old.energy(x, ss)
        max_energy_ratio = max(max_energy_ratio, es / et)
        # Here C=max(a,b)/N=1, so K=3.  Bound from the proof is 42.5.
        assert es <= 42.5 * et + 1e-10
        u, singular, vh = np.linalg.svd(x)
        v = vh.conj().T
        left = (u * singular) @ u.conj().T
        right = (v * singular) @ v.conj().T
        gap = et - (old.energy(left, ts) + old.energy(right, ts)) / 2
        expected_gap = sum(float(np.sum(singular[:, None] * singular[None, :]
            * np.abs(u.conj().T @ t @ u - v.conj().T @ t @ v) ** 2)) for t in ts)
        max_modulus_residual = max(max_modulus_residual, abs(gap - expected_gap))
        assert gap >= -1e-10
    checks['two_modulus'] = max_modulus_residual
    h_fund = np.diag([2., -.5, -1.5]).astype(complex)
    x_h = np.array([float((2 * np.trace(t @ h_fund)).real) for t in fundamental])
    th = sum(x * t for x, t in zip(x_h, ts))
    sh = sum(x * s for x, s in zip(x_h, ss))
    h3 = float(np.trace(h_fund @ h_fund @ h_fund).real)
    leading = 3 * delta * h3 / (20 * n ** 3)
    checks['gibbs_second_coefficient'] = residual(
        np.trace(sh @ th @ th) / (2 * dimension * n ** 2), leading)
    observations = []
    for h in [.001, .0005]:
        tau = old.thermal(th / n, h)
        observations.append(float(np.trace(tau @ sh).real) / h ** 2)
    if a and b:
        assert leading > 0
        assert abs(observations[1] - leading) <= abs(observations[0] - leading) + 1e-6
        assert abs(observations[1] - leading) < .01 * leading
    else:
        assert np.linalg.norm(ss) < 1e-10
    return dict(a=a, b=b, N=n, dimension=dimension, ambient_dimension=ambient,
                C2=c2, C3=c3, Delta=delta, max_second_energy_ratio=max_energy_ratio,
                gibbs_second_coefficient=leading, observed_small_h_coefficients=observations,
                residuals=checks)


def nonunital_self_score(dimension):
    rng = np.random.default_rng(841 + dimension)
    z = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    b = (z + z.conj().T) / 2
    b /= np.linalg.norm(b, 2)
    h = .7
    w0 = dimension * old.thermal(b, h)
    # Weyl conjugation is an exact irreducible finite-group twirl.
    shift = np.roll(np.eye(dimension), 1, axis=0)
    phase = np.diag(np.exp(2j * math.pi * np.arange(dimension) / dimension))
    p = .61
    kraus = [math.sqrt(1 - p) * np.eye(dimension, dtype=complex)]
    for j in range(dimension):
        a = np.zeros((dimension, dimension), complex)
        a[0, j] = math.sqrt(p)
        kraus.append(a)
    score, comm, second = 0., 0., np.zeros((dimension, dimension), complex)
    for j, k in itertools.product(range(dimension), repeat=2):
        u = np.linalg.matrix_power(shift, j) @ np.linalg.matrix_power(phase, k)
        w = u @ w0 @ u.conj().T
        output = sum(a @ w @ a.conj().T for a in kraus)
        score += float(np.trace(w @ (w - output)).real) / dimension ** 2
        comm += sum(float(np.linalg.norm(w @ a - a @ w) ** 2)
                    for a in kraus) / dimension ** 2
        second += w @ w / dimension ** 2
    checks = dict(
        TP=residual(sum(a.conj().T @ a for a in kraus), np.eye(dimension)),
        second_moment_scalar=residual(second, np.trace(w0 @ w0) / dimension * np.eye(dimension)),
        self_score=abs(score - comm / 2))
    assert checks['self_score'] < 1e-10
    nonunital = float(np.linalg.norm(sum(a @ a.conj().T for a in kraus) - np.eye(dimension)))
    assert nonunital > .1
    # Independently check the pointwise Gibbs divided-difference inequalities.
    a = kraus[-1]
    eb = np.linalg.norm(b @ a - a @ b) ** 2
    ew = np.linalg.norm(w0 @ a - a @ w0) ** 2
    assert h ** 2 * math.exp(-4 * h) * eb <= ew + 1e-12
    assert ew <= h ** 2 * math.exp(4 * h) * eb + 1e-12
    return dict(dimension=dimension, nonunital_defect=nonunital,
                averaged_score=score, averaged_commutator_energy=comm, residuals=checks)


def main():
    symbol_error = residual(np.einsum('abc,ebc->ae', d_symbol, d_symbol),
                            5 / 3 * np.eye(8))
    carriers = [carrier_case(a, b) for a, b in
                [(1, 1), (2, 1), (1, 2), (2, 2), (3, 1), (1, 3),
                 (3, 2), (2, 3), (1, 0), (0, 1), (2, 0), (0, 2)]]
    scores = [nonunital_self_score(d) for d in [2, 3, 4, 8]]
    result = dict(status='FINITE-EVIDENCE', proof_validation=False,
                  exact_fraction_factorizations=arithmetic(), d_tensor_residual=symbol_error,
                  carrier_cases=carriers, nonunital_score_cases=scores,
                  modulus_samples=12 * len(carriers), second_energy_samples=12 * len(carriers),
                  dependencies=['Python standard library', 'NumPy'], theorem_file='RESULT.txt')
    result['max_matrix_residual'] = max(
        [symbol_error] + [max(c['residuals'].values()) for c in carriers + scores])
    (ROOT / 'CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='passed', carrier_cases=len(carriers),
                         exact_factorizations=result['exact_fraction_factorizations'],
                         nonunital_score_cases=len(scores), max_residual=result['max_matrix_residual'])))


if __name__ == '__main__':
    main()
