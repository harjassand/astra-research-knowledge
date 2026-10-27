"""Certified positive rational time quadrature; no source queries or root oracle.

The exact coefficient acquisition uses only integers and Fraction.  Optional
floating execution of the acquired covariance action uses the separate main
compiler module.  Certificates concern the exact rational coefficients, not
floating point sampling or empirical total variation.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q


def ceil_log2(x: Q) -> int:
    """Least integer b >= 0 such that 2**b >= x, using integer comparisons."""
    if x <= 1:
        return 0
    b = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    if (1 << b) * x.denominator < x.numerator:
        b += 1
    return b


def legendre_values(m: int, x: Q) -> list[Q]:
    vals = [Q(1)]
    if not m:
        return vals
    vals.append(x)
    for k in range(1, m):
        vals.append(((2*k+1)*x*vals[-1] - k*vals[-2])/(k+1))
    return vals


def roots_at_most(m: int, x: Q) -> tuple[int, bool]:
    """Sturm rank in (-1,x], with zero terms deleted from the sign sequence."""
    vals = legendre_values(m, x)
    signs = [1 if y > 0 else -1 for y in vals if y]
    variations = sum(a != b for a, b in zip(signs, signs[1:]))
    return m - variations, vals[-1] == 0


def root_brackets(m: int, bits: int) -> tuple[list[tuple[Q, Q]], int]:
    """One certified bracket for each ranked root, at most m*bits rank calls."""
    brackets = []
    calls = 0
    for rank in range(1, m+1):
        lo, hi = Q(-1), Q(1)
        for _ in range(bits):
            mid = (lo+hi)/2
            count, is_root = roots_at_most(m, mid)
            calls += 1
            if is_root and count == rank:
                lo = hi = mid
                break
            if count >= rank:
                hi = mid
            else:
                lo = mid
        brackets.append((lo, hi))
    return brackets, calls


def legendre_coefficients(m: int) -> list[Q]:
    """Ascending coefficients, by the exact rational three-term recurrence."""
    prev, cur = [Q(1)], [Q(0), Q(1)]
    if m == 0:
        return prev
    for k in range(1, m):
        nxt = [Q(0)] * (len(cur)+1)
        for i, a in enumerate(cur):
            nxt[i+1] += Q(2*k+1, k+1)*a
        for i, a in enumerate(prev):
            nxt[i] -= Q(k, k+1)*a
        prev, cur = cur, nxt
    return cur


def interval_product(a: tuple[Q, Q], b: tuple[Q, Q]) -> tuple[Q, Q]:
    values = [x*y for x in a for y in b]
    return min(values), max(values)


def interval_square(a: tuple[Q, Q]) -> tuple[Q, Q]:
    lo, hi = a
    return (Q(0) if lo <= 0 <= hi else min(lo*lo, hi*hi),
            max(lo*lo, hi*hi))


def interval_polynomial(coeff: list[Q], x: tuple[Q, Q]) -> tuple[Q, Q]:
    result = Q(0), Q(0)
    for c in reversed(coeff):
        lo, hi = interval_product(result, x)
        result = lo+c, hi+c
    return result


@dataclass(frozen=True)
class LegendreCertificate:
    order: int
    tolerance: Q
    nodes: tuple[Q, ...]
    weights: tuple[Q, ...]  # on [-1,1], positive and sum exactly two
    root_brackets: tuple[tuple[Q, Q], ...]
    weight_brackets: tuple[tuple[Q, Q], ...]  # true, before normalization
    maximum_node_error: Q
    weight_l1_error_bound: Q
    bits_used: int
    bits_cap: int
    rank_calls: int


def acquire_legendre(m: int, zeta: Q) -> LegendreCertificate:
    """Acquire positive rational nodes/weights, with a deterministic bit cap.

    Root error <= 2*zeta and weight L1 error <= 2*zeta on [-1,1].
    After affine mapping to an interval of length delta, both relevant
    errors are <= delta*zeta, and total weight is exactly delta.
    """
    zeta = Q(zeta)
    if not isinstance(m, int) or m < 1 or not 0 < zeta < 1:
        raise ValueError("Need integer order >=1 and 0 < rational tolerance < 1")
    coeff = legendre_coefficients(m)
    deriv = [i*coeff[i] for i in range(1, len(coeff))]
    # Horner interval width and the true Gauss weight <= 2 prove this cap.
    constant = Q(16 * m**3 * (m+1) * 9**m)
    cap = max(4, ceil_log2(constant/zeta)+1, ceil_log2(1/zeta)+2)
    bits = min(cap, max(8, ceil_log2(1/zeta)//2))
    total_calls = 0
    while True:
        brackets, calls = root_brackets(m, bits)
        total_calls += calls
        nodes = [(lo+hi)/2 for lo, hi in brackets]
        node_error = max((hi-lo)/2 for lo, hi in brackets)
        weight_intervals = []
        for bracket in brackets:
            x2 = interval_square(bracket)
            denom = interval_product((1-x2[1], 1-x2[0]),
                                     interval_square(interval_polynomial(deriv, bracket)))
            if denom[0] <= 0:
                break
            weight_intervals.append((2/denom[1], 2/denom[0]))
        if len(weight_intervals) == m:
            eta = sum(((hi-lo)/2 for lo, hi in weight_intervals), Q(0))
            if node_error <= 2*zeta and eta <= zeta:
                raw = [(lo+hi)/2 for lo, hi in weight_intervals]
                total = sum(raw, Q(0))
                weights = [2*w/total for w in raw]
                assert all(-1 < t < 1 for t in nodes)
                assert all(w > 0 for w in weights) and sum(weights) == 2
                return LegendreCertificate(
                    m, zeta, tuple(nodes), tuple(weights), tuple(brackets),
                    tuple(weight_intervals), node_error, 2*eta, bits, cap, total_calls)
        if bits == cap:
            raise ArithmeticError("The proved interval precision cap was violated")
        bits = min(cap, 2*bits)


@dataclass(frozen=True)
class TimeQuadrature:
    intervals: int
    certificate: LegendreCertificate
    nodes: tuple[Q, ...]
    weights: tuple[Q, ...]
    bias_bound: Q  # multiplied by L**2
    squared_weight_sum: Q

    def replication_counts(self, budget: int) -> tuple[int, ...]:
        """At most budget + len(nodes) actions, variance sum w^2/r <= 1/budget."""
        if budget < 1:
            raise ValueError("Need positive budget")
        return tuple((budget*w.numerator+w.denominator-1)//w.denominator
                     for w in self.weights)


def acquire_time_quadrature(J: int, m: int, zeta: Q) -> TimeQuadrature:
    if not isinstance(J, int) or J < 1:
        raise ValueError("Need a positive interval count")
    cert = acquire_legendre(m, zeta)
    nodes, weights = [], []
    for j in range(1, J+1):
        delta = Q(1, 2**j)
        for x, w in zip(cert.nodes, cert.weights):
            nodes.append(1-Q(3, 2)*delta+delta*x/2)
            weights.append(delta*w/2)
    assert sum(weights) == 1-Q(1, 2**J)
    bias = Q(1, 2**J)+Q(2*m+1, 16**m)+2*cert.tolerance
    return TimeQuadrature(J, cert, tuple(nodes), tuple(weights), bias,
                          sum((w*w for w in weights), Q(0)))


def fixed_time_covariance_action(g, v, t: float, rng):
    """Floating prototype of the exact four-query operation at a fixed node."""
    import math
    from check_covariance_compiler import heat_action
    center = math.sqrt(t)*rng.standard_normal(v.size)
    scale = math.sqrt(1-t)
    return heat_action(g, center, scale,
                       heat_action(g, center, scale, v, rng), rng)


def quadrature_covariance_action(g, v, quadrature: TimeQuadrature, rng,
                                 replications: tuple[int, ...] | None = None):
    """Actual positive action, at most 4*sum(replications) original values."""
    import numpy as np
    counts = replications or (1,)*len(quadrature.nodes)
    if len(counts) != len(quadrature.nodes) or min(counts) < 1:
        raise ValueError("One positive integer replication count per node")
    result = np.zeros_like(v)
    for t, w, count in zip(quadrature.nodes, quadrature.weights, counts):
        for _ in range(count):
            result += float(w)/count*fixed_time_covariance_action(g, v, float(t), rng)
    return result


def quadrature_gaussian_mean_sample(g, d, sigma, replica_m, quadrature, rng,
                                    replications=None):
    """Complete value-only sampler with precomputed rational quadrature.

    Exact-real program cap: replica_m**3 + 1 + 4*sum(replications).
    Numerical implementation follows that program; rounding-TV is not asserted.
    """
    import math
    import numpy as np
    from check_covariance_compiler import rational_weights
    n, a, b, kappa = rational_weights(replica_m)
    value = np.zeros(d)
    for _ in range(n):
        value += float(a)*g(rng.standard_normal(d))
    value += float(b)*g(rng.standard_normal(d))
    z = rng.standard_normal(d)
    action = quadrature_covariance_action(g, z, quadrature, rng, replications)
    tau = sigma/math.sqrt(2)
    return value+tau*z-float(kappa)*action/(2*tau)+tau*rng.standard_normal(d)
