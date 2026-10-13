"""Finite marked collision genealogy, research prototype (2026-10-13).

Model: normalized, homogeneous, isotropic 3-D Maxwell collisions and
initial centered Gaussian scale mixtures, with scalar variances in [a,b].
The probability identities are ideal-arithmetic results. This NumPy code
is floating-point, not a certified exact-real or random-bit implementation.

Run tests: python validate.py --output results.json
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, sqrt, pi
from typing import Callable
import numpy as np

VarianceSampler = Callable[[np.random.Generator], float]

@dataclass(frozen=True)
class DiscreteVariance:
    values: tuple[float, ...]
    probabilities: tuple[float, ...]

    def __post_init__(self) -> None:
        v = np.asarray(self.values, dtype=float)
        p = np.asarray(self.probabilities, dtype=float)
        if len(v) == 0 or len(v) != len(p):
            raise ValueError('Nonempty values and equally long probabilities required.')
        if not np.all(np.isfinite(v)) or not np.all(v > 0):
            raise ValueError('Variances must be finite and strictly positive.')
        if not np.all(np.isfinite(p)) or np.any(p < 0) or abs(p.sum()-1) > 1e-12:
            raise ValueError('Probabilities must be nonnegative and sum to one.')

    def __call__(self, rng: np.random.Generator) -> float:
        # Simple inversion; building an alias table is preferable for large mixtures.
        u = rng.random()
        acc = 0.0
        for value, probability in zip(self.values, self.probabilities):
            acc += probability
            if u < acc:
                return float(value)
        return float(self.values[-1])


def terminal_blocks(n: int, t: float, rng: np.random.Generator) -> tuple[list[int], int, int]:
    """Return terminal multiplicities, number of splits, and visited nodes.

    Each block k>=2 waits Exp((k-1)/(k+1)); on splitting r is uniform in
    {1,...,k-1}. Both children receive the same remaining horizon.
    Work is at most 2*n-1 nodes, regardless of t (n>0).
    """
    if not isinstance(n, (int, np.integer)) or n < 0:
        raise ValueError('n must be a nonnegative integer.')
    if not np.isfinite(t) or t < 0:
        raise ValueError('t must be finite and nonnegative.')
    if n == 0:
        return [], 0, 0
    stack = [(int(n), float(t))]
    blocks: list[int] = []
    splits = nodes = 0
    while stack:
        k, remaining = stack.pop()
        nodes += 1
        if k == 1 or remaining == 0:
            blocks.append(k)
            continue
        waiting = rng.exponential((k+1)/(k-1))
        if waiting >= remaining:
            blocks.append(k)
        else:
            r = int(rng.integers(1, k))
            left = remaining-waiting
            stack.append((r, left))
            stack.append((k-r, left))
            splits += 1
    assert sum(blocks) == n and splits <= n-1 and nodes <= 2*n-1
    return blocks, splits, nodes


def moment_sample(k: int, t: float, a: float, b: float,
                  initial: VarianceSampler, rng: np.random.Generator) -> tuple[float, int, int]:
    """Unbiased ideal-arithmetic estimate of E[((b-V_t)/(b-a))**k]."""
    if not (np.isfinite(a) and np.isfinite(b) and 0 < a < b):
        raise ValueError('Require 0 < a < b.')
    blocks, splits, nodes = terminal_blocks(k, t, rng)
    value = 1.0
    for count in blocks:
        v = initial(rng)
        if not a <= v <= b:
            raise ValueError('Initial sampler violated supplied bounds.')
        value *= ((b-v)/(b-a))**count
    return value, splits, nodes


def laplace_sample(z: float, t: float, a: float, b: float,
                   initial: VarianceSampler, rng: np.random.Generator) -> tuple[float, int, int]:
    """Estimate L_t(z)=E[exp(-z V_t)] with no tree/time truncation.

    Returns estimate, Poisson degree, and effective split count.
    """
    if not (np.isfinite(z) and z >= 0 and 0 < a <= b):
        raise ValueError('Require finite z>=0 and 0<a<=b.')
    if not (np.isfinite(t) and t >= 0):
        raise ValueError('t must be finite and nonnegative.')
    if a == b:
        return exp(-a*z), 0, 0
    k = int(rng.poisson((b-a)*z))
    h, splits, _ = moment_sample(k, t, a, b, initial, rng)
    return exp(-a*z)*h, k, splits


def density_sample(v: np.ndarray, t: float, a: float, b: float,
                   initial: VarianceSampler, rng: np.random.Generator) -> tuple[float, int, int]:
    """Unbiased signed estimate of the 3-D velocity density at v.

    Its magnitude is bounded by (2*pi*a)**(-3/2). This is an estimator,
    not a velocity draw and not a nonnegative density realization.
    """
    v = np.asarray(v, dtype=float)
    if v.shape != (3,) or not np.all(np.isfinite(v)):
        raise ValueError('v must be a finite 3-vector.')
    if not (np.isfinite(a) and np.isfinite(b) and 0 < a <= b):
        raise ValueError('Require 0<a<=b.')
    if not (np.isfinite(t) and t >= 0):
        raise ValueError('t must be finite and nonnegative.')
    if a == b:
        return (2*pi*a)**(-1.5)*exp(-float(v@v)/(2*a)), 0, 0
    frequency = rng.normal(size=3)/sqrt(a)
    z = float(frequency@frequency)/2
    k = int(rng.poisson((b-a)*z))
    h, splits, _ = moment_sample(k, t, a, b, initial, rng)
    return (2*pi*a)**(-1.5)*float(np.cos(frequency@v))*h, k, splits


def approximate_velocity(n: int, t: float, a: float, b: float,
                         initial: VarianceSampler, rng: np.random.Generator
                         ) -> tuple[np.ndarray, float, int, int]:
    """Full-law approximation: returns velocity, latent variance, splits, nodes.

    In ideal arithmetic its total variation error is at most
    sqrt(15/2)*(b-a)**2/(16*a*a*n), uniformly over t>=0.
    The guarantee is relative to the supplied mixture/collision model,
    not to arbitrary gas data. Every call uses fresh randomness.
    """
    if not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError('n must be a positive integer.')
    if not (np.isfinite(a) and np.isfinite(b) and 0 < a <= b):
        raise ValueError('Require finite 0<a<=b.')
    blocks, splits, nodes = terminal_blocks(n, t, rng)
    total = 0.0
    for count in blocks:
        variance = initial(rng)
        if not a <= variance <= b:
            raise ValueError('Initial sampler violated supplied bounds.')
        total += count*variance
    variance = total/n
    return sqrt(variance)*rng.normal(size=3), variance, splits, nodes


def tv_bound(n: int, a: float, b: float) -> float:
    if n < 1 or not (0 < a <= b):
        raise ValueError('Require n>=1 and 0<a<=b.')
    return min(1.0, sqrt(15/2)*(b-a)**2/(16*a*a*n))
