"""Exact finite moment and matrix checks; no optimal-wall conclusion.

Cartan moments are computed from virtual harmonic weight characters and
the exact KMS/root commutator identity, independently of dense carrier
tensor operators. Fraction arithmetic checks Taylor quotients. NumPy
checks the same words in the contraction-kernel representation.
"""
import functools
import importlib.util
import itertools
import json
import math
import pathlib
from collections import Counter
from fractions import Fraction as F

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'su3_checks', ROOT.parent / 'regular_su3' / 'verify_regular_su3.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

H = (F(2), F(-1, 2), F(-3, 2))
mean_h2 = sum(t * t for t in H) / 3
Y = tuple(t * t - mean_h2 for t in H)


@functools.lru_cache(None)
def weights(a, b):
    result = Counter(tuple(x - y for x, y in zip(alpha, beta))
                     for alpha in c.old.occupations(a, 3)
                     for beta in c.old.occupations(b, 3))
    if a and b:
        result.subtract(Counter(tuple(x - y for x, y in zip(alpha, beta))
                                for alpha in c.old.occupations(a - 1, 3)
                                for beta in c.old.occupations(b - 1, 3)))
    assert all(multiplicity >= 0 for multiplicity in result.values())
    result = +result
    assert sum(result.values()) == (a + 1) * (b + 1) * (a + b + 2) // 2
    return tuple(result.items())


@functools.lru_cache(None)
def traces(a, b, z, h, degree):
    """Return normalized Tr T_Z T_H^k and Tr D_Z T_H^k, exactly.

Use the U(3) lift (a+b,b,0), n_i=nu_i+b, total charge a+2b.
For i!=j, Tr E_ji E_ij exp(t T_H)
 =Tr(n_i-n_j)exp(t T_H)/(exp(t(h_i-h_j))-1).
The characteristic-matrix identity is
D_Z=sum_i z_i sum_j E_ji E_ij+(3/2-2(a+2b)/3)T_Z.
"""
    dimension = (a + 1) * (b + 1) * (a + b + 2) // 2
    factorial = [math.factorial(k) for k in range(degree + 2)]
    u = [[F(0) for _ in range(degree + 2)] for _ in range(3)]
    v = [[F(0) for _ in range(degree + 1)] for _ in range(3)]
    tz = [F(0) for _ in range(degree + 1)]
    for nu, multiplicity in weights(a, b):
        energy = sum(t * n for t, n in zip(h, nu))
        ns = [n + b for n in nu]
        power = F(1)
        z_weight = sum(t * n for t, n in zip(z, nu))
        for k in range(degree + 2):
            for i in range(3):
                u[i][k] += multiplicity * ns[i] * power / factorial[k]
                if k <= degree:
                    v[i][k] += multiplicity * ns[i] ** 2 * power / factorial[k]
            if k <= degree:
                tz[k] += multiplicity * z_weight * power / factorial[k]
            power *= energy
    d_coeff = [sum(z[i] * v[i][k] for i in range(3))
               + (F(3, 2) - F(2 * (a + 2 * b), 3)) * tz[k]
               for k in range(degree + 1)]
    for i, j in itertools.permutations(range(3), 2):
        delta_h = h[i] - h[j]
        assert delta_h
        denominator = [F(0)] + [delta_h ** p / factorial[p]
                                for p in range(1, degree + 2)]
        numerator = [u[i][p] - u[j][p] for p in range(degree + 2)]
        assert numerator[0] == 0
        quotient = []
        for k in range(degree + 1):
            quotient.append((numerator[k + 1] - sum(
                denominator[p] * quotient[k + 1 - p]
                for p in range(2, k + 2))) / denominator[1])
            d_coeff[k] += z[i] * quotient[k]
    return (tuple(tz[k] * factorial[k] / dimension for k in range(degree + 1)),
            tuple(d_coeff[k] * factorial[k] / dimension for k in range(degree + 1)))


def central_quotients(a, b, z, degree):
    c2 = F(a * a + a * b + b * b + 3 * a + 3 * b, 3)
    c3 = F((a - b) * (2 * a + b + 3) * (a + 2 * b + 3), 18)
    ordinary, quadratic = traces(a, b, z, H, degree)
    p6 = a * b * (a + 2) * (b + 2) * (a + b + 1) * (a + b + 3)
    numerators = tuple(c2 * d - c3 * t for t, d in zip(ordinary, quadratic))
    if not p6:
        assert all(value == 0 for value in numerators)
        return numerators
    assert numerators[0] == numerators[1] == 0
    result = tuple(value / p6 for value in numerators)
    assert result[2] == sum(z_i * h_i * h_i for z_i, h_i in zip(z, H)) / 40
    return result


def exact_checks():
    degree = 7
    records = []
    for z in [H, Y]:
        table = {(a, b): central_quotients(a, b, z, degree)
                 for a in range(1, degree + 2) for b in range(1, degree + 2)}
        for a in range(1, 13):
            central_quotients(a, 0, z, degree)
            central_quotients(0, a, z, degree)
        count = 0
        for k in range(2, degree + 1):
            ell = k - 2
            for i in range(ell + 2):
                j = ell + 1 - i
                value = sum((-1) ** (i + j - u - v) * math.comb(i, u)
                            * math.comb(j, v) * table[(1 + u, 1 + v)][k]
                            for u in range(i + 1) for v in range(j + 1))
                assert value == 0, (z, k, i, j, value)
                count += 1
        records.append(dict(Z=[str(t) for t in z], degree=degree,
                            interior_grid_cases=len(table),
                            pure_wall_cases=24, mixed_degree_differences=count,
                            quadratic_quotient=str(table[(1, 1)][2])))
    return records


def residual(value, expected, tolerance=5e-9):
    err = float(np.max(np.abs(np.asarray(value) - np.asarray(expected))))
    scale = max(1., float(np.max(np.abs(np.asarray(expected)))))
    if err / scale > tolerance:
        raise AssertionError((err, scale, value, expected))
    return err / scale


def matrix_case(a, b):
    ts, ambient = c.harmonic_carrier(a, b)
    dimension = ts[0].shape[0]
    n = a + b
    c2 = (a * a + a * b + b * b + 3 * a + 3 * b) / 3
    c3 = (a - b) * (2 * a + b + 3) * (a + 2 * b + 3) / 18
    alpha = c3 / c2
    delta = c2 * (c2 / 3 + .25) - c3 * c3 / c2
    cs = delta / n ** 2
    ds = [sum(c.d_symbol[k, i, j] * ts[i] @ ts[j]
              for i in range(8) for j in range(8)) for k in range(8)]
    ss = [(d - alpha * t) / n for t, d in zip(ts, ds)]
    checks = []
    x = np.array([float((2 * np.trace(t @ np.diag([float(u) for u in H]))).real)
                  for t in c.fundamental])
    th = sum(u * t for u, t in zip(x, ts))
    for z_diag in [H, Y]:
        z = np.array([float((2 * np.trace(t @ np.diag([float(u) for u in z_diag]))).real)
                      for t in c.fundamental])
        tz, dz = sum(u * t for u, t in zip(z, ts)), sum(u * d for u, d in zip(z, ds))
        expected_t, expected_d = traces(a, b, z_diag, H, 6)
        power = np.eye(dimension)
        for k in range(7):
            checks.append(residual(np.trace(tz @ power) / dimension, float(expected_t[k])))
            checks.append(residual(np.trace(dz @ power) / dimension, float(expected_d[k])))
            power = power @ th
    posterior = []
    for h_diag in [H, (F(1), F(0), F(-1))]:
        h_mat = np.diag([float(t) for t in h_diag])
        y_mat = h_mat @ h_mat - np.trace(h_mat @ h_mat) / 3 * np.eye(3)
        x = np.array([float((2 * np.trace(t @ h_mat)).real) for t in c.fundamental])
        y = np.array([float((2 * np.trace(t @ y_mat)).real) for t in c.fundamental])
        th = sum(u * t for u, t in zip(x, ts))
        eigenvalues, eigenvectors = np.linalg.eigh(th)
        h = .01
        probs = np.exp(h * eigenvalues / n)
        tau = (eigenvectors * (probs / sum(probs))) @ eigenvectors.conj().T
        mt = np.array([np.trace(tau @ t).real for t in ts])
        ms = np.array([np.trace(tau @ s).real for s in ss])
        z = y - np.dot(y, mt) / np.dot(mt, mt) * mt
        isolated = float(np.dot(ms, z))
        assert np.linalg.norm(z) > 0
        assert isolated > 0
        checks.append(residual(float(np.dot(mt, z)), 0.))
        target = (3 / 40) * cs / n * h ** 2 * np.dot(z, y)
        assert .9 <= isolated / target <= 1.1
        # Scalar-square score identity for a nonunital reset channel.
        rng = np.random.default_rng(20261008 + 17 * a + b)
        v = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
        v /= np.linalg.norm(v)
        reset = [v[:, None] @ np.eye(dimension)[i:i + 1, :] for i in range(dimension)]
        assert np.linalg.norm(sum(t.conj().T @ t for t in reset) - np.eye(dimension)) < 1e-10
        score = sum(np.trace(s @ (s - sum(t @ s @ t.conj().T for t in reset))).real
                    for s in ss)
        energy = sum(c.old.energy(t, ss) for t in reset)
        checks.append(residual(score, energy / 2))
        posterior.append(dict(H=[str(t) for t in h_diag], h=h,
                              ordinary_cancel_residual=float(abs(np.dot(mt, z))),
                              isolated_second_moment=isolated,
                              divided_quadratic_prediction=isolated / target,
                              cubic_trace=float(np.trace(h_mat @ h_mat @ h_mat).real)))
    # A coherent projector is a control, not a weighted-profile optimizer.
    v = eigenvectors[:, -1]
    p = v[:, None] @ v.conj()[None, :]
    et, es = c.old.energy(p, ts), c.old.energy(p, ss)
    checks.append(residual(et, 2 * n))
    return dict(a=a, b=b, N=n, dimension=dimension, ambient_dimension=ambient,
                C_S=cs, max_relative_residual=max(checks), posterior=posterior,
                coherent_projector=dict(E_T=et, E_S=es,
                                        E_T_over_N2=et / n ** 2,
                                        E_S_over_N_sqrtCS=es / (n * math.sqrt(cs))))


def main():
    exact = exact_checks()
    cases = [matrix_case(a, b) for a, b in [(1, 1), (2, 1), (3, 1), (5, 1),
                                          (8, 1), (2, 2), (3, 2), (1, 3)]]
    result = dict(status='FINITE-EVIDENCE', proof_validation=False,
                  theorem_file='WEIGHTED_POSTERIOR_CONVERSE.txt',
                  optimal_wall_profile='UNKNOWN', exact_moment_quotients=exact,
                  matrix_cases=cases,
                  max_relative_residual=max(t['max_relative_residual'] for t in cases),
                  diagnostic_h_warning='h=.01 checks are finite controls, not the loose proved h_* cutoff.',
                  dependencies=['Python standard library', 'NumPy'])
    (ROOT / 'MOMENT_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='passed', matrix_cases=len(cases),
                         exact_quotient_cases=sum(t['interior_grid_cases'] for t in exact),
                         exact_wall_cases=sum(t['pure_wall_cases'] for t in exact),
                         exact_degree_differences=sum(t['mixed_degree_differences'] for t in exact),
                         max_relative_residual=result['max_relative_residual'],
                         optimal_wall_profile='UNKNOWN')))


if __name__ == '__main__':
    main()
