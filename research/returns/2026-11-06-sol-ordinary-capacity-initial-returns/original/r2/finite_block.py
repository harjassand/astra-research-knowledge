"""Exact rational finite-block coherent-information computation.

This is a total finite-block algorithm, not a capacity evaluator.  Its full
state-net search is implemented and has explicitly astronomical cost.
Only SymPy, already present in the environment, is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import isqrt
import json
import time
import sympy as s

R = s.Rational


def ceil_log2(n: int) -> int:
    return (n - 1).bit_length()


def ceil_sqrt(n: int) -> int:
    k = isqrt(n)
    return k if k * k == n else k + 1


def ln2_interval(terms: int):
    """Positive rational lower/upper bounds from 2 atanh(1/3)."""
    assert terms >= 1
    lo = 2 * sum((R(1, 3 ** (2 * j + 1) * (2 * j + 1))
                  for j in range(terms)), R(0))
    tail = R(9, 4 * (2 * terms + 1) * 3 ** (2 * terms + 1))
    return lo, lo + tail


def entropy_interval(x: s.Matrix, tolerance=R(1, 100)):
    """Certified interval for S(x) in bits; input promised a density matrix.

    -x log x = sum_{k>=1} x(1-x)^k/k on [0,1].
    The scalar remainder is between 0 and 1/(m+1), including x=0.
    All matrix arithmetic and interval endpoints are exact rationals.
    """
    tolerance = R(tolerance)
    assert tolerance > 0 and x.rows == x.cols
    d = x.rows
    terms = max(1, int(s.ceiling(4 * d / tolerance)))
    log_terms = 1
    while True:
        log_lo, log_hi = ln2_interval(log_terms)
        if d * (log_hi - log_lo) / log_lo ** 2 <= tolerance / 2:
            break
        log_terms += 1
    z = s.eye(d) - x
    power = s.eye(d)
    p = R(0)
    for k in range(1, terms + 1):
        power = power * z
        p += s.trace(x * power) / k
    p = s.simplify(p)
    if p.is_real is not True:
        raise ValueError("Expected a real exact trace")
    lo = p / log_hi
    hi = (p + R(d, terms + 1)) / log_lo
    assert hi - lo <= tolerance
    return lo, hi, {"entropy_dimension": d, "polynomial_terms": terms,
                    "logarithm_terms": log_terms}


@dataclass(frozen=True)
class Channel:
    a: int
    b: int
    images: tuple  # row-major N(|i><j|)

    @classmethod
    def from_normalized_choi(cls, a, b, j):
        assert j.shape == (a * b, a * b)
        images = tuple(a * j[i*b:(i+1)*b, k*b:(k+1)*b]
                       for i in range(a) for k in range(a))
        return cls(a, b, images)

    def choi(self):
        j = s.zeros(self.a * self.b)
        for i in range(self.a):
            for k in range(self.a):
                j[i*self.b:(i+1)*self.b, k*self.b:(k+1)*self.b] = (
                    self.images[i*self.a+k] / self.a)
        return j

    def tensor(self, other):
        a, b = self.a * other.a, self.b * other.b
        images = []
        for i in range(a):
            i0, i1 = divmod(i, other.a)
            for j in range(a):
                j0, j1 = divmod(j, other.a)
                images.append(s.kronecker_product(
                    self.images[i0*self.a+j0],
                    other.images[i1*other.a+j1]))
        return Channel(a, b, tuple(images))

    def tensor_power(self, n):
        assert n >= 1
        out = self
        for _ in range(n - 1):
            out = out.tensor(self)
        return out

    def apply_reference(self, rho, r):
        assert rho.shape == (r*self.a, r*self.a)
        out = s.zeros(r * self.b)
        for u in range(r):
            for v in range(r):
                block = s.zeros(self.b)
                for i in range(self.a):
                    for j in range(self.a):
                        c = rho[u*self.a+i, v*self.a+j]
                        if c:
                            block += c * self.images[i*self.a+j]
                out[u*self.b:(u+1)*self.b,
                    v*self.b:(v+1)*self.b] = block
        return out


def trace_reference(rho, r, b):
    return sum((rho[u*b:(u+1)*b, u*b:(u+1)*b]
                for u in range(r)), s.zeros(b))


def integer_pure_density(entries):
    """Gaussian-integer amplitudes normalize to a rational-complex density."""
    v = s.Matrix(entries)
    norm = (v.conjugate().T * v)[0]
    assert norm > 0
    return v * v.conjugate().T / norm


def coherent_interval(channel, purification, r, tolerance=R(1, 100)):
    rb = channel.apply_reference(purification, r)
    b = trace_reference(rb, r, channel.b)
    blo, bhi, cost_b = entropy_interval(b, R(tolerance) / 2)
    rblo, rbhi, cost_rb = entropy_interval(rb, R(tolerance) / 2)
    return blo - rbhi, bhi - rblo, [cost_b, cost_rb]


def grid_parameters(a, b, n, tolerance):
    """A sufficient finite purification net, with no assumed rate bound."""
    tolerance = R(tolerance)
    an, bn = a ** n, b ** n
    length = an * an
    q = 1
    while R(1, 2 ** q) * (ceil_log2(bn) + ceil_log2(an*bn)
                           + 2*q + 4) > tolerance / 2:
        q += 1
    grid_radius = 2 ** q * ceil_sqrt(2 * length)
    candidates = (2*grid_radius+1) ** (2*length) - 1
    return {"n": n, "input_dimension": an, "output_dimension": bn,
            "purification_amplitudes": length, "dyadic_exponent": q,
            "grid_radius": grid_radius, "candidates": candidates,
            "continuity_error_bound": str(R(1, 2**q) * (
                ceil_log2(bn)+ceil_log2(an*bn)+2*q+4))}


def finite_block_interval(channel, n, tolerance=R(1, 10)):
    """Total exhaustive algorithm for max I_c(rho,N^n), in bits per block.

    There is intentionally no resource cap or early non-certified return in
    this mathematical algorithm.  Consult grid_parameters before executing.
    It is not run on a nontrivial complete state net in the accompanying checks.
    """
    tolerance = R(tolerance)
    plan = grid_parameters(channel.a, channel.b, n, tolerance)
    cn = channel.tensor_power(n)
    r = cn.a
    length = r * r
    radius = plan["grid_radius"]
    low = R(0)  # every channel has a pure input of coherent information zero
    upper = None
    for coordinates in product(range(-radius, radius+1), repeat=2*length):
        if not any(coordinates):
            continue
        v = [coordinates[2*j] + s.I*coordinates[2*j+1]
             for j in range(length)]
        rho = integer_pure_density(v)
        lo, hi, _ = coherent_interval(cn, rho, r, tolerance / 2)
        low = max(low, lo)
        upper = hi if upper is None else max(upper, hi)
    hi = max(R(0), upper) + tolerance / 2
    assert hi - low <= tolerance
    return low, hi, plan


def capacity_lower_bounds(channel):
    """Increasing rational lower bounds converging to ordinary Q.

    Each yielded value takes finite time.  No stopping/error certificate for
    Q is provided.  Full state nets make even the early stages impractical.
    """
    lower = R(0)
    stage = 1
    while True:
        for n in range(1, stage + 1):
            lo, _, _ = finite_block_interval(channel, n, R(n, stage))
            lower = max(lower, lo / n)
        yield lower
        stage += 1


def identity_channel(d):
    return Channel(d, d, tuple(s.eye(d)[:, i] * s.eye(d)[j, :]
                              for i in range(d) for j in range(d)))


def erasure_channel(d, p):
    p = R(p)
    images = []
    for i in range(d):
        for j in range(d):
            x = s.zeros(d+1)
            x[i, j] = 1-p
            if i == j:
                x[d, d] = p
            images.append(x)
    return Channel(d, d+1, tuple(images))


def bell_density(d):
    return integer_pure_density([int(i == j)
                                for i in range(d) for j in range(d)])


def execute_checks():
    start = time.perf_counter()
    checks = []
    # Exact spectral values are an independent reference for these inputs.
    for name, matrix, expected in [
        ("pure", s.diag(1, 0), R(0)),
        ("maximally_mixed_qubit", s.eye(2)/2, R(1)),
        ("rank_deficient_four_level", s.diag(R(1,2), R(1,2), 0, 0), R(1)),
        ("complex_pure", integer_pure_density([1, s.I]), R(0)),
    ]:
        lo, hi, cost = entropy_interval(matrix, R(1, 20))
        assert lo <= expected <= hi
        checks.append({"name": name, "low": str(lo), "high": str(hi),
                       "expected": str(expected), "cost": cost})

    for p in [R(0), R(1,4), R(1,2), R(3,4), R(1)]:
        channel = erasure_channel(2, p)
        j = channel.choi()
        assert j.is_hermitian and j.is_positive_semidefinite
        assert s.trace(j) == 1
        for i in range(2):
            for k in range(2):
                assert s.trace(j[i*3:(i+1)*3, k*3:(k+1)*3]) == R(int(i==k), 2)
        reconstructed = Channel.from_normalized_choi(2, 3, j)
        assert reconstructed.images == channel.images
        lo, hi, costs = coherent_interval(channel, bell_density(2), 2, R(1,10))
        expected = 1-2*p  # exact erasure-channel entropy exchange
        assert lo <= expected <= hi
        checks.append({"name": "erasure_"+str(p), "low": str(lo),
                       "high": str(hi), "expected": str(expected),
                       "cost": costs})

    # Exact tensor construction, including complex off-diagonal inputs.
    phase = s.diag(1, s.I)
    complex_channel = identity_channel(2)
    complex_channel = Channel(2, 2, tuple(phase*x*phase.conjugate().T
                                         for x in complex_channel.images))
    doubled = complex_channel.tensor(erasure_channel(2, R(1,2)))
    assert doubled.choi().is_positive_semidefinite
    assert s.trace(doubled.choi()) == 1
    checks.append({"name": "complex_tensor_choi", "passed": True,
                   "choi_rows": doubled.choi().rows})

    # Actually execute one complete net in the degenerate one-dimensional case.
    lo, hi, plan = finite_block_interval(identity_channel(1), 1, R(10))
    assert lo <= 0 <= hi
    checks.append({"name": "full_degenerate_net", "low": str(lo),
                   "high": str(hi), "plan": plan})

    # A complete qubit net is deliberately not misreported as executed.
    plan = grid_parameters(2, 2, 1, R(1,4))
    compact_plan = {k: str(v) for k, v in plan.items() if k != "candidates"}
    compact_plan["candidate_decimal_digits"] = len(str(plan["candidates"]))
    compact_plan["candidate_count"] = str(plan["candidates"])
    return {"status": "PASS", "checks": checks,
            "qubit_full_net_plan_only": compact_plan,
            "elapsed_seconds": time.perf_counter()-start,
            "scope": "Certified finite entropy and fixed-input block values; no capacity or nontrivial complete state-net execution."}


if __name__ == "__main__":
    result = execute_checks()
    with open("checks.json", "w") as handle:
        json.dump(result, handle, indent=2)
    print(json.dumps({"status": result["status"],
                      "check_count": len(result["checks"]),
                      "elapsed_seconds": result["elapsed_seconds"],
                      "qubit_net_candidates": result["qubit_full_net_plan_only"]["candidate_count"],
                      "scope": result["scope"]}, indent=2))
