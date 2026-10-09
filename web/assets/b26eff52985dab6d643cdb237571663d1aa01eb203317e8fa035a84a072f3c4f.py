#!/usr/bin/env python3
"""Exact, read-only replay for Cycle05 scoped obstructions.

Dependency: Python 3 and SymPy. This is finite/symbolic diagnostic evidence,
not a formal proof of the arbitrary-family theorems. It writes no files.
"""
from fractions import Fraction
import sympy as sp


count = 0


def check(statement):
    global count
    assert statement
    count += 1


def zero(x):
    return sp.simplify(x) == 0


def matrix_equal(a, b):
    check(a.shape == b.shape)
    for x in a - b:
        check(zero(x))


def psd_exact(a):
    """Exact LDL Schur pivots, including zero-pivot rows."""
    a = sp.simplify(a)
    matrix_equal(a, a.conjugate().T)
    while a.rows:
        p = sp.simplify(a[0, 0])
        check(p.is_nonnegative is True)
        if zero(p):
            for x in a[0, :]:
                check(zero(x))
            a = a[1:, 1:]
        else:
            col = a[1:, 0]
            a = sp.simplify(a[1:, 1:] - col * col.conjugate().T / p)


def pure_channel(t):
    h = sp.Matrix([[1, t, 0], [t, 1, 0], [0, 0, 1 + t]])
    norm = 3 + 2 * t + 3 * t * t
    sigma = h * h / norm
    m = (1 + t * t) / norm
    k = (1 + t) ** 2 / norm
    gamma = 2 * t / (1 + t * t)
    ensemble = []
    for s in [-1, 1]:
        for r in [-1, 1]:
            v = sp.Matrix([sp.sqrt(m), s * sp.sqrt(m), r * sp.sqrt(k)])
            pi = sp.simplify(v * v.T)
            weight = (1 + s * gamma) / 4
            effect = sp.simplify(weight * norm * h.inv() * pi * h.inv())
            ensemble.append((weight, pi, effect))
    return h, norm, sigma, m, k, ensemble


def obs_map(a, ensemble):
    return sp.simplify(sum((effect * sp.trace(pi * a)
                            for _, pi, effect in ensemble), sp.zeros(3)))


def state_map(a, ensemble):
    return sp.simplify(sum((pi * sp.trace(effect * a)
                            for _, pi, effect in ensemble), sp.zeros(3)))


def check_channel(t):
    h, norm, sigma, m, k, ensemble = pure_channel(t)
    identity = sp.eye(3)
    check(t >= 0 and t < 1)
    check(h.det() > 0)
    matrix_equal(sum((w * pi for w, pi, _ in ensemble), sp.zeros(3)), sigma)
    matrix_equal(sum((effect for _, _, effect in ensemble), sp.zeros(3)), identity)
    for weight, pi, effect in ensemble:
        check(weight > 0)
        check(zero(sp.trace(pi) - 1))
        matrix_equal(pi * pi, pi)
        check(zero(sp.trace(sigma * effect) - weight))
        matrix_equal(h * effect * h / norm, weight * pi)
    matrix_equal(state_map(sigma, ensemble), sigma)
    a, b, c = sp.symbols("a b c", real=True)
    diag = sp.diag(a, b, c)
    matrix_equal(obs_map(diag, ensemble), sp.trace(sigma * diag) * identity)
    root_l = sp.diag(1 / sp.sqrt(5), 3 / sp.sqrt(5), 1)
    l = root_l * root_l
    rho = h * l * h / norm
    matrix_equal(state_map(rho, ensemble), sigma)
    delta = sp.Rational(4, 5) * (t * t - 1) / norm * sp.diag(1, -1, 0)
    matrix_equal(rho - sigma, delta)
    # G and C in an ordinary Hermitian basis. No inferred orthonormalization.
    basis = [sp.diag(1, 0, 0), sp.diag(0, 1, 0), sp.diag(0, 0, 1)]
    for i in range(3):
        for j in range(i + 1, 3):
            x, y = sp.zeros(3), sp.zeros(3)
            x[i, j] = x[j, i] = 1
            y[i, j], y[j, i] = -sp.I, sp.I
            basis.extend([x, y])
    gram = sp.Matrix([[sp.trace(h * a * h * b) / norm
                       for b in basis] for a in basis])
    cross = sp.Matrix([[sum(w * sp.trace(pi * a) * sp.trace(pi * b)
                            for w, pi, _ in ensemble)
                        for b in basis] for a in basis])
    psd_exact(sp.simplify(gram - cross))
    # The channel coefficients and this broadcaster's Choi coefficients are
    # rational after the sign sums, despite algebraic branch states/effects.
    for i in range(3):
        for j in range(3):
            unit = sp.zeros(3)
            unit[i, j] = 1
            image = state_map(unit, ensemble)
            broad = sp.simplify(sum((sp.trace(effect * unit) * sp.kronecker_product(pi, pi)
                                    for _, pi, effect in ensemble), sp.zeros(9)))
            for x in image:
                check(x.is_Rational)
            for x in broad:
                check(x.is_Rational)


def root_formula_checks():
    t = sp.symbols("t", real=True)
    norm = 3 + 2 * t + 3 * t * t
    h = sp.Matrix([[1, t, 0], [t, 1, 0], [0, 0, 1 + t]])
    sigma = h * h / norm
    l = sp.diag(sp.Rational(1, 5), sp.Rational(9, 5), 1)
    root = sp.diag(1 / sp.sqrt(5), 3 / sp.sqrt(5), 1)

    def energy(a, b=None):
        if b is None:
            b = a
        return sp.trace(h * a * h * b) / norm - sp.trace(sigma * a) * sp.trace(sigma * b)

    check(zero(sp.trace(sigma * l) - 1))
    check(zero(energy(l) - 32 * (1 - t * t) / (25 * norm)))
    # Keep log(9) formal to avoid log-branch transformations.
    log5, log9 = sp.symbols("log5 log9", real=True)
    log_l = sp.diag(-log5, log9 - log5, 0)
    check(zero(energy(l, log_l) - sp.Rational(4, 5) * (1 - t * t) * log9 / norm))
    claimed = ((2 + sp.Rational(6, 5) * t * t + (1 + t) ** 2) / norm
               - (4 * (1 + t * t) / sp.sqrt(5) + (1 + t) ** 2) ** 2 / norm ** 2)
    check(zero(energy(root) - claimed))
    check(zero(sp.limit(energy(root), t, 1) - (9 - 4 * sp.sqrt(5)) / 20))
    check(9 - 4 * sp.sqrt(5) > 0)


def negative_entropy_checks():
    t = sp.Rational(99, 100)
    h, norm, sigma, m, k, ensemble = pure_channel(t)
    mu = 2 * m + sp.Rational(9, 10) * k
    check(mu == sp.Rational(752429, 792030))
    l0 = sp.diag(sp.Rational(1, 5), sp.Rational(9, 5), sp.Rational(9, 10))
    l = l0 / mu
    rho = h * l * h / norm
    matrix_equal(state_map(rho, ensemble), sigma)
    check(sp.Rational(9, 10) < mu < 1)
    log2, log9, log5 = sp.symbols("log2 log9 log5", real=True)
    logs = sp.diag(-log5, log9 - log5, log9 - log5 - log2)
    lhs = sp.trace(h * l0 * h * logs) / norm - mu * sp.trace(sigma * logs)
    aa = -sp.Rational(8, 5) * (t * t / norm - m * m) + sp.Rational(7, 10) * m * k
    cc = m * k / 5
    check(zero(lhs - aa * log9 - cc * log2))
    check(aa == -sp.Rational(131609645, 12546230418))
    check(cc == sp.Rational(784139401, 31365576045))
    check(aa < 0 < cc)
    check(2 * aa + sp.Rational(7, 10) * cc == -sp.Rational(363835481, 104551920150))
    check(2 * aa + sp.Rational(7, 10) * cc < 0)
    check(sum(Fraction(7, 10) ** j / sp.factorial(j) for j in range(5)) > 2)
    check(zero(sigma[2, 2] - rho[2, 2] - m * k / (5 * mu)))
    check(m * k / (5 * mu) > 0)


def rare_classical_checks():
    for n in range(2, 65):
        w, q, hh = Fraction(1, n), Fraction(1, 2 ** (2 * n)), Fraction(1, 2 ** n)
        check(q + hh <= w)
        rho = [1 - w, w, Fraction(0)]
        sigma = [1 - q - hh, q, hh]
        tau = [sigma[0], q + hh, Fraction(0)]
        check(all(x > 0 for x in sigma))
        check(sum(rho) == sum(sigma) == sum(tau) == 1)
        check(sum(abs(x - y) for x, y in zip(sigma, tau)) / 2 == hh)
        check((q + hh) / q == 1 + 2 ** n)
        corrected = [rho[0], w * q / (q + hh), w * hh / (q + hh)]
        check(sum(abs(x - y) for x, y in zip(rho, corrected)) / 2 == Fraction(1, n) / (1 + Fraction(1, 2 ** n)))


if __name__ == "__main__":
    root_formula_checks()
    negative_entropy_checks()
    check_channel(sp.Rational(0))
    check_channel(sp.Rational(99, 100))
    rare_classical_checks()
    print(f"PASS: {count} exact assertions; symbolic roots/log coefficients; 4-outcome pure channels; KMS covariance PSD; 63 rare-label instances.")
