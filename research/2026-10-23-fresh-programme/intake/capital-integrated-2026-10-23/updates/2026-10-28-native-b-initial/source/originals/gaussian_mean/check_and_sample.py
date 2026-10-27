"""Checks and a value-only sampler for POINTWISE_NEWTON_OBSTRUCTION.txt.

Theorems are in the proof file. Numerical law integration is a diagnostic,
not a replacement for the analytic TV bound. No derivatives or means enter
paired_fill. Analysis-only fixtures below have known means for comparison.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import csv
import math
import numpy as np
from scipy.integrate import quad
from scipy.special import gammaln, logsumexp, roots_hermitenorm
from scipy.stats import chi2, norm

ROOT = Path(__file__).resolve().parent
PHI1 = math.exp(-0.5) / math.sqrt(2 * math.pi)


class CountedOracle:
    def __init__(self, fn):
        self.fn = fn
        self.calls = 0

    def __call__(self, x):
        self.calls += 1
        return np.asarray(self.fn(x), dtype=float)


def uniform_from_gaussians(rng):
    c = rng.standard_normal(3)
    r = np.linalg.norm(c)
    return 0.5 if r == 0 else (1 + c[0] / r) / 2


def paired_fill(g, d, lam, cap, tau, rng):
    """At most three original whole-vector g-value calls on every run.

    Assumption for the quantitative bound: g-lam*id is eta*M Lipschitz.
    The actual program uses neither eta nor M nor E[g(G)].
    """
    if not (0 < lam < 1 and tau > 0 and cap >= 0):
        raise ValueError("Need 0<lam<1, tau>0, cap>=0")
    a = math.sqrt(1 - lam * lam)
    G, Z, Zp, V = rng.standard_normal((4, d))
    X, Xp = lam * G + a * Z, lam * G + a * Zp
    out = g(G) + a * Z + tau * V
    power = 1.0
    branch = None
    for j in range(cap):
        if uniform_from_gaussians(rng) >= lam * lam:
            branch = j
            p = a * a * power
            r = lam * power
            U = rng.standard_normal(d)
            b = math.sqrt(1 - r * r)
            A, B = r * X + b * U, r * Xp + b * U
            out -= (g(A) - g(B) - lam * (A - B)) / p
            break
        power *= lam * lam
    return out, G, branch


def law_bound(d, eta, M, lam, cap, tau):
    a2 = 1 - lam * lam
    first = abs(eta) * M * math.sqrt(d) * lam ** (2 * cap + 1)
    first /= tau * math.sqrt(2 * math.pi)
    second = PHI1 * eta * eta * M * M * d / (tau * tau)
    second *= 1 + 2 * lam * lam * (1 - lam ** (2 * cap)) / a2
    return first + second


def exact_chaos_checks():
    lam, a = Fraction(3, 5), Fraction(4, 5)
    for n in range(81):
        # Unnormalized He_(n-j)(G) He_j(Z) basis, forcing He_n(G).
        coeff = [-1 / (2 * a)]
        for j in range(1, n + 1):
            coeff.append(-lam * (n - j + 1) * coeff[-1] / (a * (j + 2)))
        assert 2 * a * coeff[0] == -1
        for j in range(1, n + 1):
            assert a * (j + 2) * coeff[j] + lam * (n - j + 1) * coeff[j - 1] == 0
        weights = [Fraction(math.factorial(n - j) * math.factorial(j), math.factorial(n)) for j in range(n + 1)]
        dz_u2 = sum(c * c * w * (j + 1) ** 2 for j, (c, w) in enumerate(zip(coeff, weights)))
        lower = a ** (-2 * n - 2) / (n + 2) ** 2
        assert dz_u2 >= lower
        # Exact threshold upper bound at rho=a, for all these degrees.
        assert a ** (2 * n) * dz_u2 <= 1 / (4 * a * a)
    return 81


def chaos_log_norms(lam, n):
    a = math.sqrt(1 - lam * lam)
    j = np.arange(n + 1, dtype=float)
    logs = (-2 * math.log(a) + 2 * j * math.log(lam / a)
            + gammaln(n + 1) - gammaln(j + 1) - gammaln(n - j + 1))
    logJ = 0.5 * logsumexp(logs - 2 * np.log(j + 1) - 2 * np.log(j + 2))
    logDzU = 0.5 * logsumexp(logs - 2 * np.log(j + 2))
    return logJ, logDzU


def write_amplification_table():
    rows = []
    for lam in (0.1, 0.3, 0.5, 0.8):
        for n in (0, 10, 100, 300, 1000):
            logJ, logDzU = chaos_log_norms(lam, n)
            rows.append((lam, n, logJ / math.log(10), logDzU / math.log(10)))
    with (ROOT / "INVERSE_AMPLIFICATION.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("lambda", "source_chaos_degree", "log10_norm_J", "log10_norm_Dz_u"))
        writer.writerows(rows)
    return rows


def cosine_inverse_checks():
    # Compare the exact integral expression to independent Hermite summation.
    lam = 0.6
    a = math.sqrt(1 - lam * lam)
    r = lam / a
    nodes, weights = np.polynomial.legendre.leggauss(100)
    t, w = (nodes + 1) / 2, weights / 2
    ts = t[:, None] * t[None, :]
    qq = (1 - t[:, None]) * (1 - t[None, :])
    rows = []
    for k in (1, 2, 4, 6, 8):
        K = k * k * r * r
        integral = np.sum(w[:, None] * w[None, :] * ts
                          * (np.exp(K * qq) + np.exp(-2 * k * k - K * qq))) / (2 * a * a)
        terms = []
        for n in range(0, 302, 2):
            logc2 = -k * k + 2 * n * math.log(k) - gammaln(n + 1)
            logJ, _ = chaos_log_norms(lam, n)
            terms.append(logc2 + 2 * logJ)
        series = math.exp(logsumexp(terms))
        rel = abs(integral - series) / integral
        assert rel < 2e-10, (k, integral, series, rel)
        if K >= 2:
            lower = math.exp(K - 2) / (8 * a * a * K ** 4)
            assert integral >= lower
        rows.append((k, integral, rel))
    return rows


def f_fixture(x):
    # M=1.4 is a valid derivative bound. Mean is used only by diagnostics.
    return 0.35 + np.sin(1.3 * x) / 1.3 + 0.4 * np.cos(0.7 * x) / 0.7


def ou_fixture(r, x):
    return (0.35 + math.exp(-1.3 ** 2 * (1 - r * r) / 2) * np.sin(1.3 * r * x) / 1.3
            + 0.4 * math.exp(-0.7 ** 2 * (1 - r * r) / 2) * np.cos(0.7 * r * x) / 0.7)


def conditional_identity_check():
    # Directly integrate the actual two endpoint queries, independently of
    # the analytic OU formula used for the expected result.
    lam, cap = 0.5, 6
    z, w = roots_hermitenorm(40)
    w /= math.sqrt(2 * math.pi)
    weights = w[:, None] * w[None, :]
    maxerr = 0.0
    for x in np.linspace(-4, 4, 33):
        value = np.dot(w, f_fixture(lam * x + math.sqrt(1 - lam ** 2) * z))
        xp = lam ** 2 * x + math.sqrt(1 - lam ** 4) * z[:, None]
        for j in range(cap):
            p = (1 - lam ** 2) * lam ** (2 * j)
            r = lam ** (2 * j + 1)
            b = math.sqrt(1 - r * r)
            U = z[None, :]
            # Include both the branch probability and the inverse weight.
            expected_D_on_branch = np.sum(weights * (-(f_fixture(r * x + b * U) - f_fixture(r * xp + b * U)) / p))
            value += p * expected_D_on_branch
        expected = ou_fixture(lam ** (2 * cap + 1), x)
        maxerr = max(maxerr, abs(value - expected))
    assert maxerr < 2e-13
    return maxerr


def affine_complete_law_checks():
    lam, tau, cap = 0.5, 1.0, 10
    a2 = 1 - lam * lam
    tail = lam ** (2 * cap)
    rows = []
    for eta in (0.025, 0.05, 0.1, 0.2):
        # f(x)=x+b, M=1. The actual factory is exactly a two-Gaussian mixture.
        b = 0.4
        mean = eta * b
        v_target = 1 + tau * tau
        v_active = v_target + eta ** 2 * (1 + 2 * lam * lam / a2)
        v_tail = v_target + 2 * lam * eta + eta ** 2
        def diff(x):
            return ((1 - tail) * norm.pdf(x, mean, math.sqrt(v_active))
                    + tail * norm.pdf(x, mean, math.sqrt(v_tail))
                    - norm.pdf(x, mean, math.sqrt(v_target)))
        value, err = quad(lambda x: abs(diff(x)), -14, 14, epsabs=2e-11, limit=300)
        tv = value / 2
        tail_bound = ((1 - tail) * 2 * norm.sf((14 - abs(mean)) / math.sqrt(v_active))
                      + tail * 2 * norm.sf((14 - abs(mean)) / math.sqrt(v_tail))
                      + 2 * norm.sf((14 - abs(mean)) / math.sqrt(v_target))) / 2
        bound = law_bound(1, eta, 1, lam, cap, tau)
        assert tv + err / 2 + tail_bound < bound
        rows.append((eta, tv, bound, tail_bound, err / 2))
    return rows


def exact_affine_floor():
    lam, eta, tau = 0.5, 0.1, 1.0
    v0 = 1 + tau * tau
    v1 = v0 + eta * eta * (1 + 2 * lam * lam / (1 - lam * lam))
    result = []
    for d in (1, 100, 10000, 1000000):
        cross = d * v0 * v1 * math.log(v1 / v0) / (v1 - v0)
        tv = chi2.cdf(cross / v0, d) - chi2.cdf(cross / v1, d)
        result.append((d, tv))
    return result


def gaussian_mixture_density(grid, means, weights, sd):
    out = np.empty_like(grid)
    scale = 1 / (math.sqrt(2 * math.pi) * sd)
    for start in range(0, len(grid), 48):
        y = grid[start:start + 48, None]
        out[start:start + 48] = scale * (np.exp(-0.5 * ((y - means[None, :]) / sd) ** 2) @ weights)
    return out


def nonlinear_density(grid, eta, lam, cap, tau, order):
    # Condition X on the three Gaussian variables determining G,A_j,B_j.
    # The remaining Gaussian and reserve are integrated exactly.
    a = math.sqrt(1 - lam * lam)
    q, w = roots_hermitenorm(order)
    w /= math.sqrt(2 * math.pi)
    G, H, Q = np.meshgrid(q, q, q, indexing="ij")
    ww = (w[:, None, None] * w[None, :, None] * w[None, None, :]).ravel()
    G, H, Q = G.ravel(), H.ravel(), Q.ravel()
    result = np.zeros_like(grid)
    for j in range(cap):
        p = a * a * lam ** (2 * j)
        r = lam ** (2 * j + 1)
        b = math.sqrt(1 - r * r * (1 + lam * lam) / 2)
        A = r * lam * G + b * H + r * a * Q / math.sqrt(2)
        B = r * lam * G + b * H - r * a * Q / math.sqrt(2)
        conditional_X = lam * G + r * a * a * H / (2 * b) + a * Q / math.sqrt(2)
        conditional_variance = a * a * (1 - r * r) / (2 * b * b)
        means = conditional_X + eta * (f_fixture(G) - (f_fixture(A) - f_fixture(B)) / p)
        result += p * gaussian_mixture_density(grid, means, ww, math.sqrt(tau * tau + conditional_variance))
    tail = lam ** (2 * cap)
    result += tail * gaussian_mixture_density(grid, lam * q + eta * f_fixture(q), w, math.sqrt(a * a + tau * tau))
    return result


def nonlinear_complete_law_checks():
    lam, cap, tau, M = 0.5, 6, 1.0, 1.4
    mu = 0.35 + 0.4 * math.exp(-0.7 ** 2 / 2) / 0.7
    grid = np.linspace(-12, 12, 1601)
    rows = []
    density_columns = [grid]
    for eta in (0.04, 0.08, 0.16):
        p20 = nonlinear_density(grid, eta, lam, cap, tau, 20)
        p28 = nonlinear_density(grid, eta, lam, cap, tau, 28)
        target = norm.pdf(grid, eta * mu, math.sqrt(1 + tau * tau))
        tv = np.trapezoid(abs(p28 - target), grid) / 2
        stability = np.trapezoid(abs(p28 - p20), grid) / 2
        masserr = abs(np.trapezoid(p28, grid) - 1)
        # A rigorous tail bound for the exact output, independent of quadrature.
        a = math.sqrt(1 - lam * lam)
        fmax = 0.35 + 1 / 1.3 + 0.4 / 0.7
        coefficients = np.array([lam, a + eta * M * lam / a, eta * M * lam / a, tau])
        radius = (12 - eta * fmax) / np.linalg.norm(coefficients)
        tail_bound = (chi2.sf(radius * radius, 4)
                      + 2 * norm.sf((12 - abs(eta * mu)) / math.sqrt(1 + tau * tau))) / 2
        bound = law_bound(1, eta, M, lam, cap, tau)
        assert stability < 2e-7, (eta, stability)
        assert masserr < 1e-9, (eta, masserr)
        assert tv < bound
        rows.append((eta, tv, bound, stability, tail_bound, masserr))
        density_columns.extend((p28, target))
    with (ROOT / "NONLINEAR_DENSITY_CHECK.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("x", "factory_eta_004", "target_eta_004", "factory_eta_008", "target_eta_008", "factory_eta_016", "target_eta_016"))
        writer.writerows(zip(*density_columns))
    return rows


def query_and_symmetry_checks():
    rng = np.random.default_rng(20261027)
    trials = 0
    for d in (1, 4, 17):
        for cap in (0, 1, 6, 30):
            for _ in range(100):
                g = CountedOracle(lambda x: 0.5 * x + 0.08 * f_fixture(x))
                output, G, branch = paired_fill(g, d, 0.5, cap, 1.0, rng)
                assert output.shape == (d,)
                assert np.isfinite(output).all()
                assert g.calls in (1, 3)
                assert g.calls == (1 if branch is None else 3)
                assert branch is None or 0 <= branch < cap
                trials += 1
    # Pathwise antisymmetry is stronger evidence for mean preservation than
    # a finite empirical mean comparison. This check swaps the two replicas.
    maximum = 0.0
    for j in range(12):
        x, xp, u = rng.standard_normal((3, 17))
        r, p = 0.5 ** (2 * j + 1), 0.75 * 0.5 ** (2 * j)
        a = r * x + math.sqrt(1 - r * r) * u
        b = r * xp + math.sqrt(1 - r * r) * u
        D = -(f_fixture(a) - f_fixture(b)) / p
        swapped = -(f_fixture(b) - f_fixture(a)) / p
        maximum = max(maximum, np.max(abs(D + swapped)))
    assert maximum == 0.0
    return trials, maximum


def main():
    lines = ["GAUSSIAN-MEAN CHECKS: exact algebra and complete-density diagnostics",
             "No finite moment or KS test is treated as a TV certificate."]
    n = exact_chaos_checks()
    lines.append(f"Exact rational chaos equations, inverse lower bounds and smoothing upper bounds: {n} degrees PASS.")
    rows = write_amplification_table()
    for lam, degree, logj, logd in rows:
        if lam == 0.5 and degree in (100, 300):
            lines.append(f"lambda={lam}, degree={degree}: log10 ||J||={logj:.9f}, log10 ||Dz u||={logd:.9f}.")
    cosine = cosine_inverse_checks()
    lines.append(f"Cosine integral versus independent Hermite sum: {len(cosine)} frequencies, max relative residual {max(v[2] for v in cosine):.3g}.")
    lines.append(f"Nonlinear conditional telescope from direct endpoint quadrature: max error {conditional_identity_check():.3g}.")
    n, err = query_and_symmetry_checks()
    lines.append(f"Actual factory executions with counted original g calls: {n}, maximum 3 calls; swap-antisymmetry error {err:g}.")
    for eta, tv, bound, tail, quadrature in affine_complete_law_checks():
        lines.append(f"Affine full density: eta={eta:g}, TV={tv:.10g}, proved bound={bound:.10g}, tail<={tail:.2g}, integration estimate={quadrature:.2g}.")
    for d, tv in exact_affine_floor():
        lines.append(f"Infinite-cap affine variance-floor exact TV, lambda=.5 eta=.1 tau=1: d={d}, TV={tv:.10g}.")
    for eta, tv, bound, stability, tail, masserr in nonlinear_complete_law_checks():
        lines.append(f"Nonlinear full density: eta={eta:g}, TV diagnostic={tv:.10g}, proved bound={bound:.10g}, GH20/28 difference={stability:.2g}, tail<={tail:.2g}, mass error={masserr:.2g}.")
    lines.extend(["PASS. The analytic proof provides full-law validity; floating quadrature diagnoses the implementation.",
                  "The quadratic dimension term and Lipschitz-closure failure are unresolved for recursive N687 use."])
    text = "\n".join(lines) + "\n"
    (ROOT / "CHECK_RESULTS.txt").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
