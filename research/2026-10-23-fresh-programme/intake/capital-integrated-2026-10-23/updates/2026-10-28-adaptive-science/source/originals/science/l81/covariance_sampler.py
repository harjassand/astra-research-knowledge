"""Finite positive value-only Gaussian-mean covariance correction.

Only NumPy is required. Arrays have shape (batch, d). An oracle call returns
one whole-vector value per row; batched rows represent independent executions.
The mathematical algorithm uses Gaussian seeds, square roots and arithmetic.
All stored exact mean/covariance formulas are test comparators, never sampler inputs.
"""
from dataclasses import dataclass
import numpy as np

@dataclass
class QueryOracle:
    function: object
    queries_per_execution: int = 0

    def __call__(self, x):
        self.queries_per_execution += 1
        return self.function(x)


def gaussian_uniform(rng, shape):
    """Uniform[0,1] from a Gaussian direction in R^3; null event -> 1/2."""
    w = rng.standard_normal(shape + (3,))
    radius = np.linalg.norm(w, axis=-1)
    out = np.zeros(shape)
    np.divide(w[..., 0], radius, out=out, where=radius != 0)
    return 0.5 * (1.0 + out)


def heat_action(oracle, center, scale, vector, rng):
    """R22 exact conditional mean H_s(c)v, norm <= L ||v||; two values.

    scale is a positive scalar per batch row. All query points are actual
    finite points. The source derivatives appear only in the proof.
    """
    batch, dim = vector.shape
    nv = np.linalg.norm(vector, axis=1)
    unit = np.divide(vector, nv[:, None], out=np.zeros_like(vector),
                     where=nv[:, None] != 0)
    z = rng.standard_normal((batch, dim))
    perp = z - np.sum(unit * z, axis=1)[:, None] * unit
    chi3 = np.linalg.norm(rng.standard_normal((batch, 3)), axis=1)
    radius = scale * chi3
    base = center + scale[:, None] * perp
    offset = radius[:, None] * unit
    plus, minus = oracle(base + offset), oracle(base - offset)
    ans = np.divide(nv[:, None] * (plus - minus), 2.0 * radius[:, None],
                    out=np.zeros_like(vector), where=radius[:, None] != 0)
    return ans


def covariance_action(oracle, vector, rng, time_interval=(0.0, 1.0)):
    """Four-value action J with E[J(v)|v]=Cov(g(G))v and ||J||<=L²||v||.

    Both heat actions share (time, center, scale), and use independent seeds.
    """
    batch, dim = vector.shape
    lo, hi = time_interval
    if not 0.0 <= lo < hi <= 1.0:
        raise ValueError("time_interval must be inside [0,1]")
    time = lo + (hi-lo)*gaussian_uniform(rng, (batch,))
    center = np.sqrt(time)[:, None] * rng.standard_normal((batch, dim))
    scale = np.sqrt(1.0 - time)
    first = heat_action(oracle, center, scale, vector, rng)
    return heat_action(oracle, center, scale, first, rng)


def sample_mean(oracle, n, batch, dim, rng):
    mean = np.zeros((batch, dim))
    for _ in range(n):
        mean += oracle(rng.standard_normal((batch, dim))) / n
    return mean


def corrected_sampler(oracle, n, k, batch, dim, sigma, rng, stratified_time=False):
    """Output with exactly n+4k original whole-vector value calls per execution.

    tau²=eta²=sigma²/2. No target mean or covariance is input. k actions are
    averaged conditionally on the retained Gaussian Z; the final W is unused
    by all value queries and correction randomness.
    """
    if min(n, k) < 1 or sigma <= 0:
        raise ValueError("n,k must be positive integers and sigma positive")
    tau = sigma / np.sqrt(2.0)
    mean = sample_mean(oracle, n, batch, dim, rng)
    z = rng.standard_normal((batch, dim))
    action = np.zeros_like(z)
    for j in range(k):
        interval = (j/k, (j+1)/k) if stratified_time else (0.0, 1.0)
        action += covariance_action(oracle, z, rng, interval) / k
    w = rng.standard_normal((batch, dim))
    return mean + tau * z - action / (2.0 * tau * n) + tau * w


def ordinary_sampler(oracle, n, batch, dim, sigma, rng):
    return sample_mean(oracle, n, batch, dim, rng) + sigma * rng.standard_normal((batch, dim))


def safe_bound(dim, n, k, L=1.0, sigma=1.0):
    """Conservative proved TV upper bound; see THEOREM.md.

    Constants are deliberately rounded upward. This is a mathematical upper
    bound, not a finite-diagnostic TV estimate.
    """
    tau2 = eta2 = sigma * sigma / 2.0
    stein = L*L*np.sqrt(dim)/(n**1.5)
    cov_residual = L**4*np.sqrt(dim)/(4.0*tau2*n*n)
    randomization = L**4*dim/(8.0*tau2*eta2*n*n*k)
    return min(1.0, (stein+cov_residual)/(2.0*eta2) + randomization)


def ordinary_bound(dim, n, L=1.0, sigma=1.0):
    """Stein/smoothing independent-average upper bound, with safe constants."""
    return min(1.0, L*L*np.sqrt(dim)/(2.0*sigma*sigma*n))


def explicit_schedule(dim, epsilon, L=1.0, sigma=1.0):
    """Deterministic schedule with each theorem term <= epsilon/3."""
    import math
    if dim < 1 or not 0.0 < epsilon < 1.0 or L < 0 or sigma <= 0:
        raise ValueError("invalid dimension, epsilon, L or sigma")
    ratio = L/sigma
    n = math.ceil(max(1.0, (3*ratio**2*math.sqrt(dim)/epsilon)**(2/3),
                          math.sqrt(3*ratio**4*math.sqrt(dim)/(2*epsilon))))
    k = max(1, math.ceil(3*ratio**4*dim/(2*epsilon*n*n)))
    return n, k


def covariance_word(oracle, vector, power, rng, last_interval=(0.0, 1.0)):
    """Fresh global words: mean Sigma**power v, norm <= L**(2power)||v||.

    The final operation can be stratified across an average of words. Earlier
    operations remain global Uniform[0,1] actions; no common matrix is formed.
    """
    if power < 1:
        raise ValueError("power must be positive")
    out = vector
    for j in range(power):
        interval = last_interval if j == power-1 else (0.0, 1.0)
        out = covariance_action(oracle, out, rng, interval)
    return out


def second_corrected_sampler(oracle, n, k, ell, batch, dim, sigma, rng,
                             stratified_time=False):
    """Second binomial correction. Exactly n+4k+8ell values per execution."""
    if min(n,k,ell)<1 or sigma<=0:
        raise ValueError("n,k,ell and sigma must be positive")
    tau = sigma/np.sqrt(2.0)
    mean = sample_mean(oracle,n,batch,dim,rng)
    z = rng.standard_normal((batch,dim))
    action1=np.zeros_like(z);action2=np.zeros_like(z)
    for j in range(k):
        interval=(j/k,(j+1)/k) if stratified_time else (0.0,1.0)
        action1 += covariance_action(oracle,z,rng,interval)/k
    for j in range(ell):
        interval=(j/ell,(j+1)/ell) if stratified_time else (0.0,1.0)
        action2 += covariance_word(oracle,z,2,rng,interval)/ell
    return mean+tau*z-action1/(2*tau*n)-action2/(8*tau**3*n*n)+tau*rng.standard_normal((batch,dim))


def second_safe_bound(dim,n,k,ell,L=1.0,sigma=1.0):
    ratio=L/sigma
    return min(1.0, ratio**2*np.sqrt(dim)/n**1.5
               +ratio**6*np.sqrt(dim)/(2*n**3)+ratio**8*np.sqrt(dim)/(8*n**4)
               +ratio**4*dim/(2*n*n*k)+ratio**8*dim/(8*n**4*ell))
