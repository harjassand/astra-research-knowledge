#!/usr/bin/env python3
"""Positive finite-horizon memory fitting with an exact output certificate.

Theorem implementation layer: normalized mass <= 1 and horizon 1.  No hidden
rate count, rate gap, or rate ceiling is used by make_plan or fit_certified.

SciPy proposes an LP solution.  Exact rational arithmetic, including exponential
enclosures and Chebyshev-root enclosures, decides whether to issue a certificate.
An uncertified numerical proposal is rejected. A finite, exact support-and-weight
search is the guaranteed fallback on admitted data; its very large worst-case
cost is explicitly recorded. Standard exact rational LP can replace that fallback
with a polynomial-time algorithm, but floating-point HiGHS is not identified with
such an algorithm.

Synthetic source access occurs only in make_reports and diagnostics.  The learner
receives the plan and finite rational reports, not microscopic rates or weights.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as Q
from itertools import combinations
import json
from math import ceil, isqrt
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.optimize import linprog
from scipy.integrate import quad
import sympy as sp


def pow2(k: int) -> Q:
    return Q(1 << k) if k >= 0 else Q(1, 1 << (-k))


def ceil_log2(q: Q) -> int:
    assert q > 0
    k = q.numerator.bit_length() - q.denominator.bit_length()
    while pow2(k) < q:
        k += 1
    while pow2(k - 1) >= q:
        k -= 1
    return k


def floor_dyadic(q: Q, bits: int) -> Q:
    d = 1 << bits
    return Q((q.numerator * d) // q.denominator, d)


def nearest_dyadic(q: Q, bits: int) -> Q:
    return floor_dyadic(q + Q(1, 1 << (bits + 1)), bits)


def as_q(x) -> Q:
    if isinstance(x, Q):
        return x
    return Q(int(sp.numer(x)), int(sp.denom(x)))


def exp_neg_bounds(x: Q, bits: int = 40) -> tuple[Q, Q]:
    """Exact rational enclosure of exp(-x), width <= 2**(-bits).

    Alternating Taylor bounds on [0,1], followed by repeated squaring.  For
    very large x use e > 2, so no work scales with the magnitude of a hidden
    or retained fast rate.
    """
    assert x >= 0 and bits >= 1
    if x == 0:
        return Q(1), Q(1)
    if x >= bits + 2:
        return Q(0), pow2(-(bits + 2))
    s = max(0, ceil_log2(x))
    u = x / pow2(s)
    assert 0 < u <= 1
    target = pow2(-(bits + s + 3))
    total = Q(1)
    term = Q(1)
    n = 0
    while True:
        n += 1
        previous = total
        term *= u / n
        total += (-term if n % 2 else term)
        lower, upper = (total, previous) if n % 2 else (previous, total)
        if term <= target:
            break
    assert 0 <= lower <= upper <= 1
    for _ in range(s):
        lower *= lower
        upper *= upper
    assert upper - lower <= pow2(-bits)
    return lower, upper


def rounded_exp_floor(x: Q, bits: int) -> Q:
    lower, _ = exp_neg_bounds(x, bits + 2)
    return floor_dyadic(lower, bits)


def cheb_value(n: int, x: Q) -> Q:
    t0, t1 = Q(1), x
    if n == 0:
        return t0
    for _ in range(2, n + 1):
        t0, t1 = t1, 2 * x * t1 - t0
    return t1


@dataclass
class Plan:
    epsilon: Q
    a: Q
    n: int
    J: int
    L: int
    delta: Q
    nodes: list[Q]
    intervals: list[tuple[Q, Q]]
    canonical_nodes: list[Q]
    root_enclosures: list[tuple[Q, Q]]
    poles: list[Q]
    H: int
    R: int
    bits_A: int
    bits_y: int


def make_plan(epsilon: Q) -> Plan:
    assert 0 < epsilon < 1
    a = epsilon / 8
    n = ceil_log2(128 / epsilon)
    J = ceil_log2(1 / a)
    L = isqrt(2 * n - 1)
    if L * L < 2 * n - 1:
        L += 1
    delta = epsilon / (16 * L)

    # SymPy's rational Sturm isolation supplies exact root brackets.  Convert
    # their midpoints to dyadic coordinates and verify the resulting bounds.
    x = sp.Symbol("x")
    polynomial = sp.Poly(sp.chebyshevt(n, x), x)
    raw = polynomial.intervals(eps=sp.Rational(delta.numerator,
                                               4 * delta.denominator))
    roots = [(as_q(lo), as_q(hi)) for (lo, hi), mult in raw for _ in range(mult)]
    assert len(roots) == n
    bits_node = ceil_log2(4 / delta)
    canonical = [nearest_dyadic((lo + hi) / 2, bits_node)
                 for lo, hi in roots]
    for q, (lo, hi) in zip(canonical, roots):
        assert -1 <= lo <= q <= hi <= 1 or max(abs(q - lo), abs(q - hi)) <= delta
        assert -1 < q < 1
        assert max(abs(q - lo), abs(q - hi)) <= delta
        if lo != hi:
            assert cheb_value(n, lo) * cheb_value(n, hi) < 0
    assert all(canonical[i] < canonical[i + 1] for i in range(n - 1))

    intervals, nodes = [], []
    for j in range(J):
        left, right = a * pow2(j), min(a * pow2(j + 1), Q(1))
        assert left < right <= 2 * left
        intervals.append((left, right))
        nodes.extend((left + right) / 2 + (right - left) * q / 2
                     for q in canonical)
    assert len(nodes) == n * J
    assert min(nodes) >= a and max(nodes) <= 1

    mu0 = delta / 4
    H = ceil(Q(4) / delta)
    cutoff_n = ceil_log2(4 / delta)
    R = max(0, ceil_log2(Q(cutoff_n) / (a * mu0)))
    poles = [Q(0)]
    for j in range(R):
        poles.extend(mu0 * pow2(j) * (1 + Q(ell, H)) for ell in range(H))
    poles.append(mu0 * pow2(R))
    assert all(poles[i] < poles[i + 1] for i in range(len(poles) - 1))
    assert poles[-1] * a >= cutoff_n
    return Plan(epsilon, a, n, J, L, delta, nodes, intervals, canonical,
                roots, poles, H, R, ceil_log2(8 / delta),
                ceil_log2(128 / delta))


def compress_exact(weights: dict[int, Q], plan: Plan) -> dict[int, Q]:
    """Conic Caratheodory elimination preserving rounded samples and mass."""
    M = len(plan.nodes)
    weights = {j: w for j, w in weights.items() if w > 0}
    while len(weights) > M + 1:
        ids = list(weights)[:M + 2]
        d = 1 << plan.bits_A
        rows = [[int(rounded_exp_floor(plan.nodes[i] * plan.poles[j],
                                      plan.bits_A) * d) for j in ids]
                for i in range(M)]
        rows.append([d] * len(ids))
        null = sp.Matrix(rows).nullspace()
        assert null
        v = [as_q(q) for q in null[0]]
        if not any(q > 0 for q in v):
            v = [-q for q in v]
        theta = min(weights[j] / q for j, q in zip(ids, v) if q > 0)
        for j, q in zip(ids, v):
            weights[j] -= theta * q
            assert weights[j] >= 0
        weights = {j: w for j, w in weights.items() if w > 0}
    return weights


def fit_fast_proposal(plan: Plan, reports: list[Q]) -> dict:
    """Use no source information. Return only after an exact certificate passes."""
    M, N = len(plan.nodes), len(plan.poles)
    assert len(reports) == M
    started = perf_counter()
    A = np.exp(-np.outer(np.array([float(t) for t in plan.nodes]),
                         np.array([float(p) for p in plan.poles])))
    denominator = float(1 << plan.bits_A)
    A = np.floor(A * denominator) / denominator
    y = np.array([float(q) for q in reports])
    # The exact construction uses coefficient error <= delta/4 and radius
    # 2 delta.  A smaller proposal radius leaves ample verification margin.
    proposed_radius = 1.75 * float(plan.delta)
    constraints = np.vstack((A, -A, np.ones((1, N))))
    rhs = np.concatenate((y + proposed_radius, -y + proposed_radius, [1.0]))
    solved = linprog(np.ones(N), A_ub=constraints, b_ub=rhs,
                     bounds=(0, None), method="highs-ds")
    proposal_seconds = perf_counter() - started
    if not solved.success:
        raise RuntimeError("Numerical LP proposal failed; no certificate issued: "
                           + solved.message)
    weights = {j: Q(float(w)) for j, w in enumerate(solved.x) if w > 0}
    mass = sum(weights.values(), Q(0))
    if mass > 1:
        weights = {j: w / mass for j, w in weights.items()}
    weights = compress_exact(weights, plan)
    assert len(weights) <= M + 1
    bits_w = ceil_log2(Q(8 * (M + 1)) / plan.delta)
    weights = {j: floor_dyadic(w, bits_w) for j, w in weights.items()}
    weights = {j: w for j, w in weights.items() if w > 0}
    assert all(w >= 0 for w in weights.values())
    mass = sum(weights.values(), Q(0))
    assert mass <= 1

    check_started = perf_counter()
    residual = Q(0)
    bits_exp = ceil_log2(128 / plan.delta)
    for t, report in zip(plan.nodes, reports):
        lower, upper = Q(0), Q(0)
        for j, w in weights.items():
            lo, hi = exp_neg_bounds(t * plan.poles[j], bits_exp)
            lower += w * lo
            upper += w * hi
        residual = max(residual, abs(lower - report), abs(upper - report))
    if residual > 19 * plan.delta / 8:
        raise RuntimeError("Exact nodal verification rejected the proposal")
    # One delta for report uncertainty; one for the two node-rounding errors.
    l1_bound = plan.a + 16 * pow2(-plan.n) + plan.L * (residual + 2 * plan.delta)
    assert l1_bound < plan.epsilon
    verification_seconds = perf_counter() - check_started
    model = [{"pole": str(plan.poles[j]), "weight": str(w)}
             for j, w in sorted(weights.items())]
    encoded_bits = sum(plan.poles[j].numerator.bit_length()
                       + plan.poles[j].denominator.bit_length()
                       + w.numerator.bit_length() + w.denominator.bit_length()
                       for j, w in weights.items())
    return {
        "model": model,
        "mass_exact": str(mass),
        "retained_modes": len(weights),
        "sample_count": M,
        "dictionary_size": N,
        "rational_report_count": len(reports),
        "max_verified_report_residual_exact": str(residual),
        "max_verified_report_residual": float(residual),
        "sample_acquisition_error_allowance": float(plan.delta),
        "certified_L1_bound_exact": str(l1_bound),
        "certified_L1_bound": float(l1_bound),
        "target_epsilon": float(plan.epsilon),
        "finite_model_integer_bits": encoded_bits,
        "weight_fractional_bits": bits_w,
        "LP_matrix_float_bytes": int(constraints.nbytes),
        "proposal_seconds": proposal_seconds,
        "exact_verification_seconds": verification_seconds,
        "certificate_scope": "conditional on all rational reports having error <= delta",
        "construction": "floating LP proposal, exact rational output verification",
    }


def positive_weight_vectors(size: int, budget: int):
    """All positive integer vectors of this size with sum at most budget."""
    if size == 0:
        yield ()
        return
    for first in range(1, budget - size + 2):
        for rest in positive_weight_vectors(size - 1, budget - first):
            yield (first,) + rest


def fit_finite_search(plan: Plan, reports: list[Q]) -> dict:
    """Guaranteed finite exact fallback on admitted data, intentionally costly.

    A true grid witness can be compressed in the M sample coordinates plus mass.
    Rounding its <=M+1 weights down at the denominator used here loses <=delta/8.
    Therefore this finite search contains a model whose exact interval check
    passes with strict slack. There is no unbounded precision loop.
    """
    M, N = len(plan.nodes), len(plan.poles)
    bits_w = ceil_log2(Q(8 * (M + 1)) / plan.delta)
    D = 1 << bits_w
    bits_exp = ceil_log2(128 / plan.delta)
    started = perf_counter()
    tested = 0
    cache = {}
    for size in range(min(M + 1, N, D) + 1):
        for ids in combinations(range(N), size):
            for j in ids:
                if j not in cache:
                    cache[j] = [exp_neg_bounds(t * plan.poles[j], bits_exp)
                                for t in plan.nodes]
            for integers in positive_weight_vectors(size, D):
                tested += 1
                weights = [Q(z, D) for z in integers]
                residual = Q(0)
                for i, report in enumerate(reports):
                    lower = sum((w * cache[j][i][0] for j, w in zip(ids, weights)), Q(0))
                    upper = sum((w * cache[j][i][1] for j, w in zip(ids, weights)), Q(0))
                    residual = max(residual, abs(lower - report), abs(upper - report))
                    if residual > 19 * plan.delta / 8:
                        break
                else:
                    l1_bound = plan.a + 16 * pow2(-plan.n) + plan.L * (residual + 2 * plan.delta)
                    assert l1_bound < plan.epsilon
                    model = [{"pole": str(plan.poles[j]), "weight": str(w)}
                             for j, w in zip(ids, weights)]
                    encoded_bits = sum(plan.poles[j].numerator.bit_length()
                                       + plan.poles[j].denominator.bit_length()
                                       + w.numerator.bit_length() + w.denominator.bit_length()
                                       for j, w in zip(ids, weights))
                    return {
                        "model": model, "mass_exact": str(sum(weights, Q(0))),
                        "retained_modes": size, "sample_count": M, "dictionary_size": N,
                        "rational_report_count": M,
                        "max_verified_report_residual_exact": str(residual),
                        "max_verified_report_residual": float(residual),
                        "sample_acquisition_error_allowance": float(plan.delta),
                        "certified_L1_bound_exact": str(l1_bound),
                        "certified_L1_bound": float(l1_bound),
                        "target_epsilon": float(plan.epsilon),
                        "finite_model_integer_bits": encoded_bits,
                        "weight_fractional_bits": bits_w,
                        "LP_matrix_float_bytes": 0, "proposal_seconds": 0,
                        "exact_verification_seconds": perf_counter() - started,
                        "tested_candidates": tested,
                        "construction": "finite exhaustive positive support-and-weight fallback",
                        "certificate_scope": "conditional on all rational reports having error <= delta",
                    }
    raise RuntimeError("Finite search exhausted: reports fail the admitted-data guarantee")


def fit_certified(plan: Plan, reports: list[Q]) -> dict:
    try:
        return fit_fast_proposal(plan, reports)
    except (RuntimeError, AssertionError, ValueError, OverflowError, FloatingPointError):
        return fit_finite_search(plan, reports)


def make_reports(plan: Plan, source: list[tuple[Q, Q]], seed: int) -> tuple[list[Q], dict]:
    """Synthetic reporter, deliberately outside learner; errors certified exactly."""
    assert all(p >= 0 and w >= 0 for p, w in source)
    assert sum(w for _, w in source) <= 1
    rng = np.random.default_rng(seed)
    reports, worst = [], Q(0)
    bits = ceil_log2(1024 / plan.delta)
    for t in plan.nodes:
        lower, upper = Q(0), Q(0)
        for p, w in source:
            lo, hi = exp_neg_bounds(p * t, bits)
            lower += w * lo
            upper += w * hi
        sign = 1 if rng.integers(0, 2) else -1
        report = nearest_dyadic((lower + upper) / 2 + sign * plan.delta / 3,
                                plan.bits_y)
        error = max(abs(report - lower), abs(report - upper))
        assert error <= plan.delta
        worst = max(worst, error)
        reports.append(report)
    return reports, {"max_actual_report_error_bound": float(worst),
                     "reports": [str(q) for q in reports]}


def diagnostic_L1(source: list[tuple[Q, Q]], model: list[dict], a: Q) -> float:
    """Floating numerical diagnostic, never used to establish the certificate."""
    p = np.array([float(q) for q, _ in source])
    w = np.array([float(q) for _, q in source])
    ph = np.array([float(Q(m["pole"])) for m in model])
    wh = np.array([float(Q(m["weight"])) for m in model])
    def difference(t):
        return abs(np.dot(w, np.exp(-p * t)) - np.dot(wh, np.exp(-ph * t)))
    points = sorted(set([0.0, 1.0, float(a)] +
                        [min(1.0, max(1e-15, 1 / q)) for q in p if q > 0]))
    return sum(quad(difference, lo, hi, epsabs=1e-10, limit=150)[0]
               for lo, hi in zip(points[:-1], points[1:]))


def compression_audit(plan: Plan) -> dict:
    """Exercise the elimination branch independently of a sparse LP proposal."""
    small = replace(plan, nodes=[Q(1, 4), Q(3, 4)],
                    poles=[Q(0), Q(1, 2), Q(1), Q(3, 2), Q(2)], bits_A=16)
    before = {j: Q(1, 5) for j in range(5)}
    after = compress_exact(before.copy(), small)
    assert len(after) <= 3
    assert sum(before.values()) == sum(after.values())
    for t in small.nodes:
        lhs = sum(w * rounded_exp_floor(t * small.poles[j], small.bits_A)
                  for j, w in before.items())
        rhs = sum(w * rounded_exp_floor(t * small.poles[j], small.bits_A)
                  for j, w in after.items())
        assert lhs == rhs
    return {"input_modes": 5, "output_modes": len(after),
            "sample_moments_and_mass_preserved_exactly": True,
            "output_weights": {str(j): str(w) for j, w in after.items()}}


def fallback_audit(plan: Plan) -> dict:
    small = replace(plan, poles=[Q(0)])
    reports = [3 * plan.delta] * len(plan.nodes)
    result = fit_finite_search(small, reports)
    assert result["retained_modes"] == 1
    return {"tested_candidates": result["tested_candidates"],
            "retained_modes": result["retained_modes"],
            "constant_source": str(3 * plan.delta),
            "model": result["model"],
            "certificate": result["certified_L1_bound"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epsilon", default="1/4")
    parser.add_argument("--output", default=str(Path(__file__).with_name("passive_fit_results.json")))
    args = parser.parse_args()
    plan = make_plan(Q(args.epsilon))
    cases = {
        "zero_slow_and_ultrafast": [(Q(0), Q(1, 5)), (Q(1, 10**9), Q(1, 10)),
                                    (Q(1, 7), Q(1, 4)), (Q(4), Q(1, 4)),
                                    (Q(10**9), Q(1, 5))],
        "thirteen_decades": [(Q(10**j) if j >= 0 else Q(1, 10**(-j)), Q(1, 13))
                              for j in range(-6, 7)],
        "nearly_colliding_rates": [(Q(10000 + j, 10000), Q(1, 12))
                                    for j in range(12)],
    }
    output = {
        "normalization": "B=T=1; physical rescaling is Khat(t)=B*khat(t/T)",
        "epsilon": str(plan.epsilon), "a": str(plan.a), "n": plan.n,
        "J": plan.J, "M": len(plan.nodes), "L": plan.L,
        "delta": str(plan.delta), "H": plan.H, "R": plan.R,
        "dictionary_size": len(plan.poles),
        "nodes": [str(q) for q in plan.nodes],
        "root_enclosures": [[str(lo), str(hi)] for lo, hi in plan.root_enclosures],
        "sparse_extraction_audit": compression_audit(plan),
        "finite_fallback_audit": fallback_audit(plan),
        "cases": {},
        "limitations": ["Synthetic bounded-error reports; no physical control acquisition is simulated.",
                        "HiGHS proposes; failure invokes a guaranteed finite but very costly exact search.",
                        "Diagnostic quadrature is not the proof of the L1 certificate."],
    }
    for i, (name, source) in enumerate(cases.items()):
        reports, report_audit = make_reports(plan, source, 57100 + i)
        result = fit_certified(plan, reports)
        result["synthetic_report_audit"] = report_audit
        result["diagnostic_actual_L1"] = diagnostic_L1(source, result["model"], plan.a)
        output["cases"][name] = result
        print(json.dumps({"case": name, "modes": result["retained_modes"],
                          "L1_certificate": result["certified_L1_bound"],
                          "diagnostic_L1": result["diagnostic_actual_L1"],
                          "LP_seconds": result["proposal_seconds"]}))
    Path(args.output).write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
