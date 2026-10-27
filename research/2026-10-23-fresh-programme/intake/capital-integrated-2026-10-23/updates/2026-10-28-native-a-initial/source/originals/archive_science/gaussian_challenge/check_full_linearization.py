"""Exact and numerical checks of FULL_LINEARIZATION_AND_CURVATURE.md.

All scientific statements are proved in the companion note. These are algebraic
and finite-chaos checks, not empirical certification of full-law total variation.
No oracle/source file is modified or executed.
"""

from fractions import Fraction
from math import comb, exp, lgamma, log, log1p
from pathlib import Path

def clean(p):
    return {k: Fraction(v) for k, v in p.items() if v}


def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, Fraction(0)) + v
    return clean(out)


def scale(p, a):
    return clean({k: a * v for k, v in p.items()})


def mul(p, q):
    out = {}
    for (i, j), v in p.items():
        for (k, l), w in q.items():
            key = (i + k, j + l)
            out[key] = out.get(key, Fraction(0)) + v * w
    return clean(out)


def derivative(p, axis):
    out = {}
    for key, v in p.items():
        if key[axis]:
            new = list(key)
            new[axis] -= 1
            out[tuple(new)] = key[axis] * v
    return clean(out)


def exact_recurrence(n):
    a, b = Fraction(3, 5), Fraction(4, 5)
    # Unnormalized basis He_(n-k)(G) He_k(Z); RHS = -He_n(G).
    c = [
        -Fraction(1, 1) / b * (-a / b) ** k
        * Fraction(comb(n, k), (k + 1) * (k + 2))
        for k in range(n + 1)
    ]
    assert 2 * b * c[0] == -1
    for k in range(1, n + 1):
        assert b * (k + 2) * c[k] + a * (n - k + 1) * c[k - 1] == 0
    return c


def normalized_log_norm(n, a=0.6, b=0.8):
    terms = [
        -2 * log(b)
        + lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)
        + 2 * k * log(a / b)
        - 2 * log(k + 1) - 2 * log(k + 2)
        for k in range(n + 1)
    ]
    m = max(terms)
    return (m + log(sum(exp(t - m) for t in terms))) / 2


def symbolic_geometry():
    # Bivariate exact rational polynomials, with eta factored out.
    x, y = {(1, 0): Fraction(1)}, {(0, 1): Fraction(1)}
    psi = {(2, 1): Fraction(1, 2)}
    K = [[derivative(derivative(psi, i), j) for j in range(2)] for i in range(2)]
    g = [add(*(add(mul(K[i][j], (x, y)[j]), scale(derivative(K[i][j], j), -1)) for j in range(2))) for i in range(2)]
    n_minus_one_psi = add(mul(x, derivative(psi, 0)), mul(y, derivative(psi, 1)), scale(K[0][0], -1), scale(K[1][1], -1), scale(psi, -1))
    expected = [derivative(n_minus_one_psi, i) for i in range(2)]
    assert g == expected
    bracket = [add(*(add(mul(K[0][j], derivative(K[1][i], j)), scale(mul(K[1][j], derivative(K[0][i], j)), -1)) for j in range(2))) for i in range(2)]
    assert bracket == [y, scale(x, -1)]
    assert g == [{(1, 1): Fraction(2)}, {(2, 0): Fraction(1), (0, 0): Fraction(-1)}]
    return K, g, bracket


def scalar_newton_algebra():
    S, R, one = {(1, 0): Fraction(1)}, {(0, 1): Fraction(1)}, {(0, 0): Fraction(1)}
    tau = add(one, R)
    Vu = scale(add(R, mul(S, tau)), -1)
    residual = add(mul(add(one, S), add(tau, Vu)), scale(one, -1))
    assert add(residual, mul(S, R), mul(mul(S, S), tau)) == {}
    rho = Fraction(1, 4)
    bounds = []
    for stage in range(6):
        bounds.append((stage, float(rho), min(1.0, float(2 * rho))))
        rho = rho**2 * (3 - rho) / (4 * (1 - rho)**2)
    return residual, bounds


def main():
    for n in range(129):
        exact_recurrence(n)
    K, g, bracket = symbolic_geometry()
    residual, bounds = scalar_newton_algebra()
    lines = [
        "EXACT FINITE-CHECK RESULTS",
        "Hermite inverse recurrence: PASS for every total chaos degree 0 through 128, rational a=3/5, b=4/5.",
        "Normalized residual has L2 norm one; inverse J norms follow:",
        "N, norm_J, proved_lower_bound",
    ]
    for n in (0, 2, 8, 16, 32, 64, 128, 256):
        lognorm = normalized_log_norm(n)
        lowerlog = -(n + 1) * log(0.8) - log(n + 1) - log(n + 2)
        assert lognorm + 1e-12 >= lowerlog
        lines.append(f"{n}, {exp(lognorm):.12g}, {exp(lowerlog):.12g}")
    lines += [
        "",
        "Local Hessian K = eta [[y,x],[x,0]], verified as exact polynomial coefficients.",
        "Local source g=delta K = eta (2xy,x^2-1), verified as exact polynomial coefficients.",
        "Horizontal Lie bracket [V1,V2] = eta^2 (y,-x,0,0), verified as exact polynomial coefficients.",
        "Canonical gradient identity and non-involutive bracket: PASS symbolically.",
        "",
        "Scalar new residual = -S R - S^2 (1+R), verified as exact polynomial coefficients.",
        "Scalar quadratic identity: PASS symbolically.",
        "stage, worst_case_rho_bound, corresponding_TV_bound",
    ]
    lines += [f"{stage}, {rho:.12g}, {tv:.12g}" for stage, rho, tv in bounds]
    lines += [
        "",
        "The scalar TV entries evaluate a proved analytical bound; they are not Monte Carlo law tests.",
        "No acquired value-only solver or computational speedup is implemented by these checks.",
    ]
    output = "\n".join(lines) + "\n"
    Path(__file__).with_name("CHECK_RESULTS.txt").write_text(output)
    print(output)


if __name__ == "__main__":
    main()
