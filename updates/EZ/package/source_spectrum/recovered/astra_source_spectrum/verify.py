#!/usr/bin/env python3
"""Finite diagnostics for the accompanying operator-theory research note.

Exact tests use fractions.Fraction and integer arithmetic. Floating-point
stress tests are diagnostics, not interval certificates or infinite-dimensional
proofs. The theorem proofs are in research_note.md.

Run: python verify.py --output verification_results.json
Requires: Python 3.10+ and NumPy (for the numerical diagnostic section).
"""
from __future__ import annotations

import argparse
import json
import math
import platform
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from random import Random
from typing import Any

import numpy as np

EXACT: Counter[str] = Counter()
NUMERIC: Counter[str] = Counter()
METRICS: dict[str, Any] = {}


def check_exact(test: bool, category: str) -> None:
    if not test:
        raise AssertionError(f"Exact diagnostic failed: {category}")
    EXACT[category] += 1


def check_numeric(test: bool, category: str) -> None:
    if not test:
        raise AssertionError(f"Numerical diagnostic failed: {category}")
    NUMERIC[category] += 1


def g(t: F, a: F) -> F:
    return t / (1 + a * t)


def f(t: F, a: F) -> F:
    if a * t >= 1:
        raise ValueError("f requires a*t < 1")
    return t / (1 - a * t)


def window_rank(lambdas: list[F], a: F) -> int:
    """Exact maximum occupancy of half-open reciprocal windows [x,x+a)."""
    if not lambdas:
        return 0
    xi = sorted(1 / t for t in lambdas if t > 0)
    right, best = 0, 0
    for left in range(len(xi)):
        right = max(right, left)
        while right < len(xi) and xi[right] < xi[left] + a:
            right += 1
        best = max(best, right - left)
    return best


def interlacing_rank(lambdas: list[F], a: F) -> int:
    lam = sorted(lambdas, reverse=True)
    for r in range(len(lam) + 1):
        if all(f(lam[j + r], a) <= lam[j]
               for j in range(len(lam) - r)):
            return r
    raise AssertionError("A finite list always admits its full rank")


def exact_rank_checks() -> None:
    rng = Random(731926)
    cases: list[tuple[list[F], F]] = [([], F(1))]
    # Endpoint equality must not put two levels in the same half-open window.
    for length in range(1, 24):
        for denom in (1, 2, 3):
            a = F(1, denom)
            xis = [2 * a + a * k for k in range(length)]
            cases.append(([1 / x for x in xis], a))
            doubled = [v for v in xis for _ in range(2)]
            cases.append(([1 / x for x in doubled], a))
    for _ in range(350):
        a = F(rng.randrange(1, 6), rng.randrange(1, 6))
        xis = sorted(a + F(rng.randrange(1, 70), rng.randrange(1, 9))
                     for _ in range(rng.randrange(1, 24)))
        cases.append(([1 / x for x in xis], a))
    for lam, a in cases:
        lam.sort(reverse=True)
        r = window_rank(lam, a)
        check_exact(r == interlacing_rank(lam, a), "rank_window_equals_interlacing")
        if not lam:
            continue
        # T e_j = sqrt(lambda_j)e_(j+r), on n+r coordinates.
        n = len(lam)
        aa = lam + [F(0)] * r
        cc = [F(0)] * r + lam
        pp = [f(lam[j], a) if j < r else F(0) for j in range(n + r)]
        for av, cv, pv in zip(aa, cc, pp):
            check_exact(av <= g(cv + pv, a), "exact_rank_optimal_shift_curvature")
        check_exact(sum(p > 0 for p in pp) == r, "rank_optimal_source_size")
        if r > 0:
            check_exact(any(f(lam[j + r - 1], a) > lam[j]
                            for j in range(n - r + 1)),
                        "smaller_rank_fails_necessary_interlacing")
    METRICS["finite_rank_spectra_tested"] = len(cases)


def exact_shift_and_precision_checks() -> None:
    for a in (F(1, 3), F(1), F(7, 2)):
        for b2 in (F(1, 11), F(1), F(9, 2)):
            n = 45
            lam = [b2 / (1 + a * b2 * (k + 1)) for k in range(n)]
            for k in range(n):
                source_or_previous = b2 if k == 0 else lam[k - 1]
                check_exact(lam[k] == g(source_or_previous, a),
                            "harmonic_shift_exact_curvature_equality")
            x = [F(0)] * n
            for k in range(n + 1):
                expected = [lam[j] if j < k else F(0) for j in range(n)]
                check_exact(x == expected, "source_iteration_exact_support_and_values")
                err = max(l - y for l, y in zip(lam, x))
                check_exact(err <= 1 / (a * (k + 1)),
                            "source_iteration_exact_uniform_error_bound")
                if k < n:
                    check_exact(err == lam[k], "source_iteration_exact_tail_error")
                x = [g(b2, a)] + [g(v, a) for v in x[:-1]]
            # Fixed error-floor block, epsilon chosen so the equality is rational.
            for m in (F(1, 100), F(1, 4), F(1), F(3)):
                eps = a * m * m / (1 + a * m)
                check_exact(m == g(m, a) + eps,
                            "essential_floor_scalar_equality")
                check_exact(a * m * m - a * eps * m - eps == 0,
                            "essential_floor_quadratic_identity")


def multi_indices(n: int, degree: int):
    if n == 1:
        yield (degree,)
    else:
        for first in range(degree + 1):
            for rest in multi_indices(n - 1, degree - first):
                yield (first,) + rest


def exact_product_source_checks() -> None:
    for n in range(1, 6):
        spectrum: list[F] = []
        for degree in range(8):
            indices = list(multi_indices(n, degree))
            check_exact(len(indices) == math.comb(n + degree - 1, degree),
                        "product_degree_multiplicity")
            spectrum.extend([F(1, degree + 2)] * len(indices))
            for alpha in indices:
                if degree:
                    check_exact(sum(F(v, degree) for v in alpha) == 1,
                                "commuting_row_shift_is_subunital")
                    phi_value = sum(F(v, degree) * F(1, degree + 1)
                                    for v in alpha)
                    check_exact(F(1, degree + 2) == g(phi_value, F(1)),
                                "product_source_fixed_point_exact")
                else:
                    check_exact(F(1, 2) == g(F(1), F(1)),
                                "product_source_vacuum_exact")
                # Equality of squared two-step coefficients, i != j.
                for i in range(n):
                    for j in range(i + 1, n):
                        ij = F(alpha[i] + 1, degree + 1) * F(alpha[j] + 1, degree + 2)
                        ji = F(alpha[j] + 1, degree + 1) * F(alpha[i] + 1, degree + 2)
                        check_exact(ij == ji, "row_shift_commutation_exact")
            check_exact(window_rank(spectrum, F(1)) == math.comb(n + degree - 1, degree),
                        "scalar_source_rank_matches_highest_degree_multiplicity")
            check_exact(len(spectrum) == math.comb(n + degree, n),
                        "commuting_word_space_dimension")
    METRICS["n20_degree20_minimum_scalar_source_rank"] = math.comb(39, 20)
    METRICS["n20_degree20_full_space_dimension"] = math.comb(40, 20)


def sym(x: np.ndarray) -> np.ndarray:
    return (x + x.conj().T) / 2


def positive_part(x: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eigh(sym(x))
    return (v * np.maximum(w, 0)) @ v.conj().T


def matrix_g(x: np.ndarray, a: float) -> np.ndarray:
    # Spectral implementation for stable diagnostics; this is not a certified solver.
    w, v = np.linalg.eigh(sym(x))
    return sym((v * (w / (1 + a * w))) @ v.conj().T)


def numerical_schatten_checks() -> None:
    rng = np.random.default_rng(730912)
    worst_ratio = 0.0
    worst_curvature_min = 0.0
    instances = 0
    for n in (2, 3, 5, 8, 12):
        for _ in range(30):
            a = float(rng.uniform(0.2, 2.0))
            t = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
            target = float(rng.uniform(0.015, 0.9))
            t *= math.sqrt(target / a) / np.linalg.norm(t, 2)
            aa, cc = sym(t.conj().T @ t), sym(t @ t.conj().T)
            w, v = np.linalg.eigh(aa)
            fa = sym((v * (w / (1 - a * w))) @ v.conj().T)
            pp = positive_part(fa - cc)
            residual = sym(matrix_g(cc + pp, a) - aa)
            residual_min = float(np.linalg.eigvalsh(residual)[0])
            worst_curvature_min = min(worst_curvature_min, residual_min)
            check_numeric(residual_min >= -2e-10, "noncommuting_curvature_residual")
            lam = np.maximum(np.linalg.eigvalsh(aa), 0)
            bp = np.maximum(np.linalg.eigvalsh(pp), 0)
            for p in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 8.0):
                b_p_power = float(np.sum(bp ** (p / 2)))
                if p <= 2:
                    lhs = float(np.sum(lam ** ((p + 2) / 2)))
                    rhs = 2 * b_p_power / (p * a)
                else:
                    lhs = float(np.sum(lam ** p) ** (2 / p))
                    rhs = b_p_power ** (2 / p) / a
                ratio = lhs / rhs if rhs else 0.0
                worst_ratio = max(worst_ratio, ratio)
                check_numeric(lhs <= rhs + 2e-9 * max(1.0, rhs),
                              "sharp_schatten_bounds_noncommuting")
            instances += 1
    METRICS["noncommuting_schatten_instances"] = instances
    METRICS["largest_schatten_lhs_over_rhs"] = worst_ratio
    METRICS["smallest_float_curvature_residual_eigenvalue"] = worst_curvature_min


def numerical_positive_recursion_checks() -> None:
    rng = np.random.default_rng(91425)
    largest_modulus_ratio = 0.0
    for n in (2, 4, 7):
        for _ in range(12):
            a = float(rng.uniform(0.3, 2.0))
            vs = [rng.standard_normal((n, n)) for _ in range(3)]
            row_sum = sum(v @ v.T for v in vs)
            scale = math.sqrt(np.linalg.norm(row_sum, 2))
            vs = [v / scale for v in vs]
            source = rng.standard_normal((n, 1))
            pp = source @ source.T

            def mapping(x: np.ndarray) -> np.ndarray:
                return matrix_g(sum(v @ x @ v.T for v in vs) + pp, a)

            r1, r2 = rng.standard_normal((n, n)), rng.standard_normal((n, n))
            x, y = r1 @ r1.T, r2 @ r2.T
            delta = float(np.linalg.norm(x - y, 2))
            actual = float(np.linalg.norm(mapping(x) - mapping(y), 2))
            bound = delta / (1 + a * delta)
            largest_modulus_ratio = max(largest_modulus_ratio, actual / bound)
            check_numeric(actual <= bound + 2e-10, "positive_map_nonlinear_modulus")
            lower, upper = np.zeros((n, n)), np.eye(n) / a
            for k in range(41):
                difference = sym(upper - lower)
                check_numeric(float(np.linalg.eigvalsh(difference)[0]) >= -2e-10,
                              "source_iteration_bracketing_order")
                error_bracket = float(np.linalg.norm(difference, 2))
                check_numeric(error_bracket <= 1 / (a * (k + 1)) + 2e-10,
                              "source_iteration_dimension_free_bracket")
                lower, upper = mapping(lower), mapping(upper)
    METRICS["positive_recursion_instances"] = 36
    METRICS["largest_positive_map_modulus_ratio"] = largest_modulus_ratio


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("verification_results.json"))
    args = parser.parse_args()
    exact_rank_checks()
    exact_shift_and_precision_checks()
    exact_product_source_checks()
    numerical_schatten_checks()
    numerical_positive_recursion_checks()
    report = {
        "status": "PASS_FINITE_DIAGNOSTICS_ONLY",
        "scope_warning": "These checks neither prove the universal theorems nor establish historical novelty. Numerical tests are not interval-certified.",
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "exact_assertions_total": sum(EXACT.values()),
        "exact_assertions_by_category": dict(EXACT),
        "floating_diagnostic_assertions_total": sum(NUMERIC.values()),
        "floating_diagnostic_assertions_by_category": dict(NUMERIC),
        "metrics": METRICS,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
