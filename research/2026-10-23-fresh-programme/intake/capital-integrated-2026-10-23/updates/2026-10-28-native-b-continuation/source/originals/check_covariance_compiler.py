"""Executable value-only covariance compiler and positive Gaussian-mean sampler.

Proof: ACQUIRED_COVARIANCE_AND_FOURTH_ORDER_SAMPLER.txt.
The sampler receives no means, covariances, derivatives or hidden basis.
Analytic fixture parameters below are verifier-only. Monte Carlo checks are
diagnostics, not full-law TV certificates. Exact rational checks use Fraction.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import csv
import math
import numpy as np
from scipy.integrate import quad
from scipy.stats import chi2

ROOT = Path(__file__).resolve().parent
PHI1 = math.exp(-.5) / math.sqrt(2 * math.pi)
C_IDEAL = math.sqrt(6) + 1 / (2 * math.sqrt(2))


class CountedOracle:
    def __init__(self, fn):
        self.fn, self.calls = fn, 0

    def __call__(self, x):
        self.calls += 1
        return np.asarray(self.fn(np.asarray(x)), dtype=float)


def uniform_from_gaussians(rng):
    c = rng.standard_normal(3)
    radius = np.linalg.norm(c)
    return .5 if radius == 0 else float((1 + c[0] / radius) / 2)


def heat_action(g, center, scale, v, rng):
    """Existing S4 exact two-value heat-Hessian action, implemented literally."""
    size = float(np.linalg.norm(v))
    if size == 0:
        return np.zeros_like(v)
    if scale <= 0:
        raise ValueError("Need a positive heat scale")
    direction = v / size
    z = rng.standard_normal(v.size)
    z_perp = z - np.dot(direction, z) * direction
    radius = scale * np.linalg.norm(rng.standard_normal(3))
    if radius == 0:
        return np.zeros_like(v)  # null event in the exact-real model
    anchor = center + scale * z_perp
    return size * (g(anchor + radius * direction)
                   - g(anchor - radius * direction)) / (2 * radius)


def covariance_action(g, v, rng):
    """At most four original values, E[action|v]=Cov(g(G)) v."""
    if np.linalg.norm(v) == 0:
        return np.zeros_like(v)
    t = uniform_from_gaussians(rng)
    if t >= 1:  # floating endpoint/null-event convention, not a derivative
        t = np.nextafter(1., 0.)
    center = math.sqrt(t) * rng.standard_normal(v.size)
    scale = math.sqrt(1 - t)
    inner = heat_action(g, center, scale, v, rng)
    return heat_action(g, center, scale, inner, rng)


def rational_weights(m):
    if not isinstance(m, int) or m < 2:
        raise ValueError("m must be an integer >=2")
    n = m ** 3
    return n, Fraction(1, n - m), Fraction(-1, m * m - 1), Fraction(1, (m-1)**2 * (m+1))


def gaussian_mean_sample(g, d, sigma, m, actions, rng):
    """Positive program; deterministic original-query cap m**3+1+4*actions."""
    if sigma <= 0 or actions < 1:
        raise ValueError("Need positive sigma and action count")
    n, a, b, kappa = rational_weights(m)
    value = np.zeros(d)
    for _ in range(n):
        value += float(a) * g(rng.standard_normal(d))
    value += float(b) * g(rng.standard_normal(d))
    z = rng.standard_normal(d)
    action_sum = np.zeros(d)
    for _ in range(actions):
        action_sum += covariance_action(g, z, rng)
    tau = sigma / math.sqrt(2)
    return (value + tau * z - float(kappa) * action_sum / (2 * tau * actions)
            + tau * rng.standard_normal(d))


def theorem_bound(d, lipschitz, sigma, m, actions):
    _, _, _, kappa = rational_weights(m)
    rho = lipschitz / sigma
    if float(kappa) * rho * rho > .5:
        return math.inf
    return float(kappa)**2 * rho**4 * (C_IDEAL * math.sqrt(d) + PHI1 * d / actions)


def select_parameters(d, lipschitz, sigma, epsilon):
    """Integer-only cube selection; no source-dependent fitting or moments."""
    if d < 1 or lipschitz <= 0 or sigma <= 0 or not (0 < epsilon < 1):
        raise ValueError("Invalid supplied dimensions/bounds/accuracy")
    rho = lipschitz / sigma
    action_budget = (128 / 9) * PHI1 * rho**4 * d / epsilon
    ideal_budget = (128 / 9) * C_IDEAL * rho**4 * math.sqrt(d) / epsilon

    def sufficient(m):
        n = m ** 3
        return n >= (16/3)*rho*rho and n*n >= ideal_budget and n**3 >= 8*action_budget

    hi = 2
    while not sufficient(hi):
        hi *= 2
    lo = 2
    while lo < hi:
        mid = (lo + hi) // 2
        if sufficient(mid):
            hi = mid
        else:
            lo = mid + 1
    m = lo
    n = m ** 3
    actions = max(1, math.ceil(action_budget / (n*n)))
    return m, actions, n + 1 + 4 * actions


class GaussianValueCircuit:
    """Explicit scalar-block affine Gaussian value circuit (theorem Section 2)."""
    def __init__(self, g, centers, coefficients, beta):
        self.g = g
        self.centers = np.asarray(centers)
        self.coefficients = np.asarray(coefficients)
        self.beta = np.asarray(beta)
        self.q, self.d = self.centers.shape
        self.r = self.beta.shape[1]
        self.sizes = np.linalg.norm(self.beta, axis=1)
        masses = np.abs(self.coefficients) * self.sizes
        self.total = float(masses.sum())
        self.probabilities = masses / self.total if self.total else masses

    def value(self, w):
        result = np.zeros(self.d)
        for c, center, beta in zip(self.coefficients, self.centers, self.beta):
            result += c * self.g(center + beta @ w)
        return result

    def choose(self, rng):
        u = uniform_from_gaussians(rng)
        cumulative = 0.
        last = None
        for i, p in enumerate(self.probabilities):
            if p > 0:
                last = i
                cumulative += p
                if u < cumulative:
                    return i
        return last

    def cov_action(self, z, rng):
        if self.total == 0 or np.linalg.norm(z) == 0:
            return np.zeros(self.d)
        t = min(uniform_from_gaussians(rng), np.nextafter(1., 0.))
        w = math.sqrt(t) * rng.standard_normal((self.r, self.d))
        # Transpose action: d -> r*d.
        i = self.choose(rng)
        inner = heat_action(self.g, self.centers[i] + self.beta[i] @ w,
                            math.sqrt(1-t)*self.sizes[i], z, rng)
        inner_blocks = (self.coefficients[i]/self.probabilities[i]
                        * self.beta[i, :, None] * inner[None, :])
        # Fresh index and fresh secant seeds at the same T,W.
        j = self.choose(rng)
        outer_input = self.beta[j] @ inner_blocks
        return (self.coefficients[j] / self.probabilities[j]
                * heat_action(self.g, self.centers[j] + self.beta[j] @ w,
                              math.sqrt(1-t)*self.sizes[j], outer_input, rng))


def rotated_fixture(d, rng):
    """Verifier knows the hidden basis; sampler sees only fn and Lip bound."""
    q, _ = np.linalg.qr(rng.standard_normal((d, d)))
    omega = rng.uniform(.6, 1.8, d)
    amplitude = rng.uniform(.12, .25, d) / omega
    linear = rng.uniform(-.15, .15, d)
    phase = rng.uniform(-2, 2, d)
    offset = rng.standard_normal(d) * 2

    def fn(x):
        u = q.T @ x
        return q @ (amplitude * np.cos(omega*u+phase) + linear*u) + offset

    mean = q @ (amplitude * np.exp(-omega**2/2) * np.cos(phase)) + offset
    variance = (amplitude**2 * (.5*(1+np.exp(-2*omega**2)*np.cos(2*phase))
                                -np.exp(-omega**2)*np.cos(phase)**2)
                + linear**2 - 2*amplitude*linear*omega*np.exp(-omega**2/2)*np.sin(phase))
    lipschitz = float(np.max(np.abs(linear) + amplitude*omega))
    return fn, lipschitz, mean, q @ np.diag(variance) @ q.T, (q, omega, amplitude, linear, phase)


def analytic_circuit_covariance(centers, coefficients, beta, params):
    q, omega, amp, linear, phase = params
    hidden_centers = centers @ q
    variances = np.sum(beta**2, axis=1)
    output_diag = np.zeros(q.shape[0])
    for i, ci in enumerate(coefficients):
        mi = omega * hidden_centers[i] + phase
        ei = np.exp(-omega**2 * variances[i] / 2)
        for j, cj in enumerate(coefficients):
            mj = omega * hidden_centers[j] + phase
            ej = np.exp(-omega**2 * variances[j] / 2)
            cov = float(beta[i] @ beta[j])
            cos_product = .5*(
                np.cos(mi-mj)*np.exp(-omega**2*(variances[i]+variances[j]-2*cov)/2)
                +np.cos(mi+mj)*np.exp(-omega**2*(variances[i]+variances[j]+2*cov)/2))
            pair_cov = (amp**2*(cos_product-ei*ej*np.cos(mi)*np.cos(mj))
                        + linear**2*cov
                        - amp*linear*omega*cov*(ei*np.sin(mi)+ej*np.sin(mj)))
            output_diag += ci*cj*pair_cov
    return q @ np.diag(output_diag) @ q.T


def gaussian_variance_tv(d, v0, v1):
    if v0 == v1:
        return 0.
    if v1 < v0:
        v0, v1 = v1, v0
    crossing = d*v0*v1*math.log(v1/v0)/(v1-v0)
    return float(chi2.cdf(crossing/v0, d)-chi2.cdf(crossing/v1, d))


def main():
    rng = np.random.default_rng(27062026)
    lines = ["ACQUIRED COVARIANCE COMPILER: exact algebra and declared numerical diagnostics.",
             "The analytic full-law theorem is in the companion proof; MC is not a TV certificate."]
    for m in range(2, 21):
        n, a, b, kappa = rational_weights(m)
        assert n*a+b == 1
        assert n*a**3+b**3 == 0
        assert n*a*a+b*b == kappa
        assert kappa <= Fraction(8, 3*n)
    lines.append("Exact rational weights/mean/third-tensor/variance identities: 19 integer cubes PASS.")

    max_linear = 0.
    for d in (1, 3, 17):
        q, _ = np.linalg.qr(rng.standard_normal((d, d)))
        eig = rng.uniform(-.7, .7, d)
        mat = q @ np.diag(eig) @ q.T
        offset = rng.standard_normal(d)
        for _ in range(40):
            g = CountedOracle(lambda x: mat @ x + offset)
            v = rng.standard_normal(d)
            obtained = covariance_action(g, v, rng)
            error = np.linalg.norm(obtained - mat @ mat @ v)
            max_linear = max(max_linear, float(error))
            assert error < 2e-11 * (1+np.linalg.norm(v))
            assert g.calls <= 4
    lines.append(f"Unknown symmetric affine matrices, exact C v identity: 120 checks, maximum error {max_linear:.3g}; <=4 values.")

    fn, lip, mu, covariance, params = rotated_fixture(6, rng)
    q, omega, amp, linear, phase = params
    quadrature_error = 0.
    for k in range(6):
        def integrand(t):
            return (linear[k]**2 - 2*linear[k]*amp[k]*omega[k]*math.exp(-omega[k]**2/2)*math.sin(phase[k])
                    + .5*amp[k]**2*omega[k]**2*math.exp(-omega[k]**2*(1-t))
                    *(1-math.exp(-2*omega[k]**2*t)*math.cos(2*phase[k])))
        truth = (q.T @ covariance @ q)[k, k]
        quadrature_error = max(quadrature_error, abs(quad(integrand, 0, 1, epsabs=1e-13)[0]-truth))
    lines.append(f"Independent Brownian covariance integral versus analytic nonlinear covariance: max error {quadrature_error:.3g}.")

    count = 20000
    v = rng.standard_normal(6)
    oracle = CountedOracle(fn)
    samples = np.asarray([covariance_action(oracle, v, rng) for _ in range(count)])
    expected = covariance @ v
    standard_error = samples.std(axis=0, ddof=1)/math.sqrt(count)
    max_z = np.max(np.abs(samples.mean(axis=0)-expected)/standard_error)
    max_ratio = np.max(np.linalg.norm(samples, axis=1))/(lip**2*np.linalg.norm(v))
    assert oracle.calls <= 4*count
    assert max_ratio <= 1+1e-10
    lines.append(f"Hidden rotated nonlinear gradient, fixed-v covariance action: {count} samples, max standardized mean residual {max_z:.3f}; max pathwise norm ratio {max_ratio:.6f} <=1.")

    centers = rng.standard_normal((3, 6))*.3
    coefficients = np.array([1., -.5, .35])
    beta = np.array([[.7,.2], [.15,-.6], [.45,.4]])
    circuit_oracle = CountedOracle(fn)
    circuit = GaussianValueCircuit(circuit_oracle, centers, coefficients, beta)
    expected_cov = analytic_circuit_covariance(centers, coefficients, beta, params)
    v = rng.standard_normal(6)
    circuit_samples = np.asarray([circuit.cov_action(v, rng) for _ in range(count)])
    se = circuit_samples.std(axis=0, ddof=1)/math.sqrt(count)
    residual = np.max(np.abs(circuit_samples.mean(axis=0)-expected_cov @ v)/se)
    ratio = np.max(np.linalg.norm(circuit_samples, axis=1))/((lip*circuit.total)**2*np.linalg.norm(v))
    assert circuit_oracle.calls <= 4*count
    assert ratio <= 1+1e-10
    lines.append(f"Conditional scalar-block value circuit: {count} covariance actions, max standardized residual {residual:.3f}; max norm ratio {ratio:.6f}; <=4 original values/action.")

    cap_checks = 0
    for d in (1, 4, 19):
        fn, lip, *_ = rotated_fixture(d, rng)
        for m in (2, 3):
            for actions in (1, 4):
                for _ in range(10):
                    oracle = CountedOracle(fn)
                    out = gaussian_mean_sample(oracle, d, 2., m, actions, rng)
                    assert np.all(np.isfinite(out))
                    assert oracle.calls <= m**3+1+4*actions
                    cap_checks += 1
    lines.append(f"Actual unknown-mean sampler: {cap_checks} executions, all deterministic n+1+4M query caps PASS.")

    budget_rows = []
    for d in (1, 1024, 10**6, 10**12):
        for epsilon in (.1, .01, 1e-6):
            m, actions, cap = select_parameters(d, 1., 1., epsilon)
            bound = theorem_bound(d, 1., 1., m, actions)
            assert bound <= epsilon*(1+1e-12)
            denom = math.sqrt(-math.expm1(-2*math.log1p(4*epsilon**2)/d))
            averaging = max(1, math.ceil(1/denom))
            budget_rows.append(dict(d=d,epsilon=epsilon,m=m,n=m**3,actions=actions,
                                    query_cap=cap,analytic_TV_bound=bound,S5_averaging_cap=averaging))
    with (ROOT/'QUERY_COMPARISON.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=budget_rows[0].keys())
        writer.writeheader(); writer.writerows(budget_rows)
    lines.append("Twelve declared budget/accuracy pairs, including d=10^12: analytic cap selection PASS (no large-d data allocated).")

    rows = []
    _, _, _, kappa = rational_weights(2)
    kappa = float(kappa)
    for d in (1, 100, 10000):
        for amplitude in (.05, .1, .2):
            v0 = 1.
            v1 = v0 + kappa*kappa*amplitude**4/2
            tv = gaussian_variance_tv(d,v0,v1)
            bound = theorem_bound(d,amplitude,1.,2,1)
            assert tv <= bound + 1e-12
            rows.append(dict(d=d,amplitude=amplitude,exact_variance=v1,exact_full_TV=tv,
                             analytic_bound=bound))
    with (ROOT/'AFFINE_FULL_LAW.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    lines.append("Nine exact affine full-law Gaussian comparisons obey the theorem; the residual variance is fourth order and nonzero.")
    lines.append("PASS. The general/conditional theorems establish full-law validity. Numerical diagnostics neither fit a mean/covariance for the sampler nor certify TV from moments.")
    report='\n'.join(lines)+'\n'
    (ROOT/'CHECK_RESULTS.txt').write_text(report)
    print(report)


if __name__ == '__main__':
    main()
