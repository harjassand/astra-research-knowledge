"""Exact finite audits of the experiment-fed construction.

This runs no physical experiment and no full rare-event sampler. All probability
comparisons below use exact rational arithmetic. Decimal strings are reporting
only. Unknown rates enter the mathematical reference audit, not a purported
physical controller that is allowed to read them.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import platform
import sys
import time

sys.set_int_max_str_digits(0)


def dec(x: F, digits: int = 24) -> str:
    with localcontext() as c:
        c.prec = digits
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def ceil_log2(x: F) -> int:
    if x <= 0:
        raise ValueError("log argument must be positive")
    k = x.numerator.bit_length() - x.denominator.bit_length()
    while F(2) ** k < x:
        k += 1
    while F(2) ** (k - 1) >= x:
        k -= 1
    return k


def finite_walk_exact(p: F, m: int, n: int) -> tuple[F, F, F]:
    """Return success, boundary-failure, unabsorbed masses at cap n.

    At each step all numerators have common denominator p.denominator**step.
    This independently enumerates the finite path law by dynamic programming.
    """
    a, d = p.numerator, p.denominator
    active = {0: 1}
    success = failed = 0
    denominator = 1
    for _ in range(n):
        new = {}
        success *= d
        failed *= d
        for pos, w in active.items():
            up, down = w * a, w * (d - a)
            if pos + 1 == 1:
                success += up
            elif up:
                new[pos + 1] = new.get(pos + 1, 0) + up
            if pos - 1 == -m:
                failed += down
            elif down:
                new[pos - 1] = new.get(pos - 1, 0) + down
        active = new
        denominator *= d
        assert success + failed + sum(active.values()) == denominator
    return F(success, denominator), F(failed, denominator), F(sum(active.values()), denominator)


def audit_walks() -> list[dict]:
    results = []
    rho = F(2)
    for theta in (F(1, 2**8), F(1, 2**20)):
        m = ceil_log2(F(8) / theta)
        n = 72 * m
        for lam in (F(0), F(1), F(1, 2), F(1, 50), F(1, 2**100)):
            p = lam / (lam + rho)
            target = lam / rho
            finite, failed, survive = finite_walk_exact(p, m, n)
            r = p / (1 - p)
            boundary_success = (r - r**(m + 1)) / (1 - r**(m + 1))
            error = target - finite
            geometric_bound = r**(m + 1)
            cap_bound = F(1, 2**m)
            assert p <= F(1, 3)
            assert r == target
            assert finite <= boundary_success <= target
            assert target - boundary_success <= geometric_bound
            assert survive <= cap_bound
            assert error <= geometric_bound + cap_bound
            assert error < theta / 4
            results.append({
                "theta": dec(theta),
                "lambda": dec(lam),
                "boundary_zero_rate_diagnostic": lam == 0,
                "rho": dec(rho),
                "input_p": dec(p),
                "m": m,
                "n": n,
                "target_probability": dec(target),
                "finite_success_probability": dec(finite),
                "absolute_error": dec(error),
                "rigorous_bound": dec(geometric_bound + cap_bound),
                "unabsorbed_mass_at_cap": dec(survive),
                "success_numerator_bits": finite.numerator.bit_length(),
                "success_denominator_bits": finite.denominator.bit_length(),
                "exact_rational_checks_passed": True,
            })
    return results


def audit_gibbs() -> list[dict]:
    results = []
    theta = F(1, 2**20)
    attempts = 4 * ceil_log2(F(8) / theta)
    for q in (F(1, 4), F(1, 3), F(1, 2), F(3, 4)):
        for weight in (F(1, 2**100), F(1, 1000), F(1), F(1000), F(2**100)):
            branch = weight / (1 + weight)
            accepted_one = branch * q
            accepted_zero = (1 - branch) * (1 - q)
            acceptance = accepted_one + accepted_zero
            target = weight * q / (weight * q + 1 - q)
            rejection = 1 - acceptance
            pending, success = F(1), F(0)
            for _ in range(attempts):
                success += pending * accepted_one
                pending *= rejection
            assert acceptance >= F(1, 4)
            assert target == accepted_one / acceptance
            assert success == target * (1 - rejection**attempts)
            error = target - success
            assert 0 <= error <= rejection**attempts <= F(3, 4)**attempts
            assert error < theta / 8
            results.append({
                "q": dec(q),
                "shift_weight_a": dec(weight),
                "attempt_cap": attempts,
                "target_probability": dec(target),
                "finite_success_probability": dec(success),
                "absolute_error": dec(error),
                "fallback_probability": dec(pending),
                "exact_rational_checks_passed": True,
            })
    return results


def audit_pin_mass() -> list[dict]:
    """Independently enumerate a small rational Gibbs law and test the identity.

    It audits the missing unknown-W identity, not noisy acquisition or a
    conditional-sampling runtime claim.
    """
    n = 4
    edges = ((0, 1), (1, 2), (2, 3), (3, 0))
    states = list(product((0, 1), repeat=n))
    weights = {
        x: F(2) ** (-12 * sum(x) + 3 * sum(x[i] * x[j] for i, j in edges))
        for x in states
    }
    total = sum(weights.values(), F(0))

    def compatible(x, pins):
        return all(x[i] == b for i, b in pins.items())

    def heavy_complete(original):
        pins = dict(original)
        heavy_product = F(1)
        for i in range(n):
            if i in pins:
                continue
            mass = sum((weights[x] for x in states if compatible(x, pins)), F(0))
            one_mass = sum((weights[x] for x in states if compatible(x, pins) and x[i]), F(0))
            q = one_mass / mass
            b = int(q >= F(1, 2))
            heavy_product *= q if b else 1 - q
            pins[i] = b
        return tuple(pins[i] for i in range(n)), heavy_product

    x0, h0 = heavy_complete({})
    results = []
    for original in ({}, {0: 1}, {0: 1, 2: 1}, {i: 1 for i in range(n)}):
        xd, hd = heavy_complete(original)
        path = list(x0)
        local_ratio = F(1)
        changes = 0
        for i in range(n):
            if path[i] == xd[i]:
                continue
            old = tuple(path)
            path[i] ^= 1
            new = tuple(path)
            # Equal to the full conditional odds or inverse odds at the
            # current context; no global partition function occurs.
            local_ratio *= weights[new] / weights[old]
            changes += 1
        expected = sum((weights[x] for x in states if compatible(x, original)), F(0)) / total
        reconstructed = local_ratio * h0 / hd
        assert local_ratio == weights[xd] / weights[x0]
        assert reconstructed == expected
        assert changes <= n
        results.append({
            "pinning": original,
            "x0": x0,
            "xD": xd,
            "local_ratio_path_length": changes,
            "true_pin_probability": dec(expected),
            "reconstructed_pin_probability": dec(reconstructed),
            "exact_rational_checks_passed": True,
        })
    return results


def service_example() -> dict:
    theta, rho = F(1, 2**20), F(2)
    m = ceil_log2(F(8) / theta)
    n = 72 * m
    beta = theta / (8 * n)
    deadline = F(ceil_log2(F(32) / beta), 1) / rho
    delta = beta / (256 * rho)
    exponent_integer = math.ceil(rho * deadline)
    # e**(rho*deadline) <= 3**ceil(rho*deadline), entirely rational bound.
    bits = max(
        ceil_log2(F(256) / beta),
        ceil_log2(F(32 * 3**exponent_integer) / (rho * delta)),
    )
    assert F(1, 2**bits) <= beta / 256
    assert F(1, 2**bits) <= rho * delta / (32 * 3**exponent_integer)
    return {
        "theta": dec(theta),
        "rho": dec(rho),
        "m": m,
        "maximum_pins": n,
        "race_error_budget_beta": dec(beta),
        "deadline_from_formula": dec(deadline),
        "deadline_rounded_up_to_whole_unit": math.ceil(deadline),
        "maximum_censored_dwell_formula": dec(n * deadline),
        "maximum_censored_dwell_with_whole_unit_rounding": n * math.ceil(deadline),
        "comparison_time_resolution_upper_bound": dec(delta),
        "sufficient_deadline_uniform_bits_using_e_lt_3": bits,
        "excluded_costs_still_required": [
            "context realization",
            "actual operating-environment reproduction",
            "focal state pins",
            "settling and release",
            "first-exit detection",
            "reference clock calibration and drift",
            "timestamp/response service",
            "finite arithmetic and memory",
        ],
    }


def main() -> None:
    started = time.perf_counter()
    result = {
        "purpose": "Exact rational audits of finite local factories and unknown-weight pin-mass identity.",
        "scope": "Mathematical execution only; no physical experiment and no full rare-event or cut sampler.",
        "python": platform.python_version(),
        "walk_cases": audit_walks(),
        "gibbs_cases": audit_gibbs(),
        "pin_mass_cases": audit_pin_mass(),
        "service_example": service_example(),
    }
    result["elapsed_seconds"] = time.perf_counter() - started
    result["all_checks_passed"] = True
    out = Path(__file__).with_name("factory_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "all_checks_passed": True,
        "walk_cases": len(result["walk_cases"]),
        "gibbs_cases": len(result["gibbs_cases"]),
        "pin_mass_cases": len(result["pin_mass_cases"]),
        "elapsed_seconds": result["elapsed_seconds"],
        "output": str(out),
        "service_example": result["service_example"],
    }, indent=2))


if __name__ == "__main__":
    main()
