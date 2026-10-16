#!/usr/bin/env python3
"""Bounded standard-library exact checks. No installs, network, or source writes."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import time

HERE = Path(__file__).resolve().parent
ZERO = (F(0), F(0))


def pair(x):
    return x if isinstance(x, tuple) else (F(x), F(0))


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def scale(x, a):
    return x[0] * a, x[1] * a


def mul(x, y):
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def conj(x):
    return x[0], -x[1]


def norm2(x):
    return x[0] ** 2 + x[1] ** 2


def kp(eta, label):
    out = F(1)
    while label:
        bit = label & -label
        out *= eta[bit.bit_length() - 1]
        label ^= bit
    return out


def residual(eta, v, alpha, h, label):
    out = (h * kp(eta, label), F(0))
    for support, coefficient in v.items():
        out = add(out, scale(pair(coefficient), -alpha * kp(eta, label ^ support)))
    return out


def pattern_groups(eta, v):
    support = sorted(v)
    groups = {}
    for a in range(len(eta)):
        key = sum(((label >> a) & 1) << j for j, label in enumerate(support))
        groups.setdefault(key, []).append(a)
    return [groups[key] for key in sorted(groups)]


def candidate_labels(eta, groups):
    all_masks = [sum(1 << a for a in group) for group in groups]
    largest = [1 << max(group, key=lambda a: (eta[a], -a)) for group in groups]
    g = len(groups)
    for bits in range(1, 1 << g):
        yield sum(all_masks[j] for j in range(g) if (bits >> j) & 1)
    for anchor in range(g):
        others = [j for j in range(g) if j != anchor]
        for bits in range(1 << len(others)):
            label = largest[anchor]
            label += sum(all_masks[j] for k, j in enumerate(others) if (bits >> k) & 1)
            yield label


def compressed_max(eta, v, alpha, h, max_groups=16):
    groups = pattern_groups(eta, v)
    if len(groups) > max_groups:
        raise RuntimeError("Bounded replay cap exceeded; theorem has no such cap")
    best, winner, count = F(-1), None, 0
    for label in candidate_labels(eta, groups):
        value = norm2(residual(eta, v, alpha, h, label))
        if value > best:
            best, winner = value, label
        count += 1
    expected = (1 << len(groups)) - 1 + len(groups) * (1 << (len(groups) - 1))
    assert count == expected
    return best, winner, count, len(groups)


def brute_max(eta, v, alpha, h):
    return max(norm2(residual(eta, v, alpha, h, s)) for s in range(1, 1 << len(eta)))


def quadratic(eta, v):
    return sum(x * y * kp(eta, s ^ t) for s, x in v.items() for t, y in v.items())


def objective(eta, v, alpha, h):
    return 2 * h * sum(x * kp(eta, s) for s, x in v.items()) - alpha * quadratic(eta, v)


def certificate(eta, v, alpha, h):
    assert sum(abs(x) for x in v.values()) <= 1
    square, winner, count, groups = compressed_max(eta, v, alpha, h)
    # Every real residual modulus is rational, even if squared comparison was used.
    maximum = abs(residual(eta, v, alpha, h, winner)[0])
    assert maximum ** 2 == square
    lower = objective(eta, v, alpha, h)
    upper = alpha * quadratic(eta, v) + 2 * maximum
    assert upper >= lower
    return lower, upper, winner, count, groups


def fw(eta, p, epsilon):
    alpha, h, q = p * p, p * (1 - p), 2 * p - p * p
    assert 0 < epsilon < alpha
    v = {}
    ratio = 32 * alpha / epsilon
    first_steps = -(-ratio.numerator // ratio.denominator)
    second_limit = int(8 * alpha / epsilon) + 2
    history = []
    max_support = 0
    max_patterns = 0
    for k in range(first_steps + second_limit + 1):
        lower, upper, winner, count, groups = certificate(eta, v, alpha, h)
        gap = upper - lower
        history.append({"iteration": k, "support": len(v), "patterns": groups,
                        "candidate_evaluations": count, "gap": str(gap)})
        max_support = max(max_support, len(v))
        max_patterns = max(max_patterns, groups)
        if gap <= epsilon:
            return {"p": str(p), "epsilon": str(epsilon), "updates": k,
                    "max_support": max_support, "max_patterns": max_patterns,
                    "lower_F": str(q + lower), "upper_F": str(q + upper),
                    "gap": str(gap), "v": {str(s): str(x) for s, x in v.items()},
                    "history": history}
        assert k < first_steps + second_limit
        gamma = F(2, k + 2) if k < first_steps else epsilon / (8 * alpha)
        sign = 1 if residual(eta, v, alpha, h, winner)[0] >= 0 else -1
        v = {s: (1 - gamma) * x for s, x in v.items()}
        v[winner] = v.get(winner, F(0)) + gamma * sign
        v = {s: x for s, x in v.items() if x}
    raise AssertionError("The proved stopping bound failed")


def phase(label, phases):
    out = (F(1), F(0))
    for a, ph in enumerate(phases):
        if (label >> a) & 1:
            out = mul(out, ph)
    return out


def main():
    started = time.monotonic()
    rng = random.Random(16062026)
    diagnostics = []
    # Bounded arbitrary sparse real/complex cases, including singular eta boundaries.
    for m in range(1, 8):
        for trial in range(10):
            eta = [F(rng.randrange(0, 9), 8) for _ in range(m)]
            n = min(3, (1 << m) - 1)
            support = rng.sample(range(1, 1 << m), n)
            v = {s: (F(rng.randrange(-5, 6), 7), F(rng.randrange(-5, 6), 11))
                 for s in support}
            alpha, h = F(9, 49), F(12, 49)
            compressed, winner, count, groups = compressed_max(eta, v, alpha, h)
            full = brute_max(eta, v, alpha, h)
            assert compressed == full
            diagnostics.append({"m": m, "trial": trial, "eta": list(map(str, eta)),
                                "support": support, "patterns": groups,
                                "candidate_evaluations": count,
                                "max_modulus_squared": str(full), "winner": winner})
    # Empty candidate and good-coordinate exclusion require the singleton anchor.
    eta = [F(1, 4), F(1, 3)]
    got, winner, _, _ = compressed_max(eta, {}, F(1, 4), F(1, 4))
    assert winner == 2 and got == F(1, 12) ** 2
    assert got > norm2(residual(eta, {}, F(1, 4), F(1, 4), 3))
    # Exact phase gauge on a complex tensor kernel, with arbitrary complex v.
    eta = [F(1, 3), F(2, 5), F(0)]
    phases = [(F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))]
    v = {1: (F(2, 7), F(1, 9)), 3: (F(-1, 5), F(2, 11)), 6: (F(1, 8), F(-1, 6))}
    gauged = {s: mul(phase(s, phases), x) for s, x in v.items()}
    for s in range(8):
        original = scale(phase(s, phases), F(3, 16) * kp(eta, s))
        for t, x in gauged.items():
            kernel = scale(mul(phase(s, phases), conj(phase(t, phases))), kp(eta, s ^ t))
            original = add(original, scale(mul(kernel, x), -F(1, 16)))
        after = mul(phase(s, phases), residual(eta, v, F(1, 16), F(3, 16), s))
        assert original == after
    # Exact constrained three-sector family, without a large sector array.
    p = F(10, 21)
    alpha, h, q = p * p, p * (1 - p), 2 * p - p * p
    active = [F(4, 5), F(3, 4)]
    v = {1: F(19, 34), 2: F(36, 85), 3: F(-3, 170)}
    normalized_lambda, normalized_g0 = F(273, 3400), F(147, 425)
    assert sum(abs(x) for x in v.values()) == 1
    assert residual(active, v, F(1), F(11, 10), 0)[0] == normalized_g0
    for s, sign in [(1, 1), (2, 1), (3, -1)]:
        assert residual(active, v, F(1), F(11, 10), s)[0] == sign * normalized_lambda
    threshold = normalized_lambda / normalized_g0
    assert threshold == F(91, 392)
    tails = [F(j, 300) for j in range(1, 63)]
    large_eta = active + tails
    lo, up, winner, count, groups = certificate(large_eta, v, alpha, h)
    assert lo == up and q + lo == F(7763, 8330)
    assert groups == 3 and count == 19
    large_receipt = {"m": 64, "bad_sector_count": (1 << 64) - 1,
                     "eta": list(map(str, large_eta)), "v": {str(s): str(x) for s, x in v.items()},
                     "F": str(q + lo), "decimal_F": float(q + lo),
                     "gap": str(up - lo), "candidate_evaluations": count,
                     "patterns": groups, "screen_threshold": str(threshold)}
    screen_checks = []
    for tail in [F(0), F(1, 5), threshold, threshold + F(1, 1000000), F(1)]:
        eta = active + [tail]
        full = brute_max(eta, v, alpha, h)
        predicted = max((alpha * normalized_lambda) ** 2,
                        (tail * alpha * normalized_g0) ** 2)
        assert full == predicted
        lo2, up2, _, _, _ = certificate(eta, v, alpha, h)
        gap_expected = 2 * max(F(0), alpha * (tail * normalized_g0 - normalized_lambda))
        assert up2 - lo2 == gap_expected
        screen_checks.append({"tail": str(tail), "gap": str(up2 - lo2),
                              "exact_candidate_optimality_certified": up2 == lo2})
    assert not screen_checks[-2]["exact_candidate_optimality_certified"]
    # Interior truncation is approximate, not automatically exact.
    p2 = F(1, 2)
    active2 = [F(1, 3), F(1, 4)]
    v2 = {1: F(1, 3), 2: F(1, 4), 3: F(-1, 12)}
    eta2 = active2 + [F(j, 1000000) for j in range(1, 63)]
    lo2, up2, _, _, _ = certificate(eta2, v2, F(1, 4), F(1, 4))
    assert F(3, 4) + lo2 == F(19, 24)
    assert up2 - lo2 == F(31, 1200000) > 0
    # Global approximation construction, using exact fractions and exact compressed gaps.
    fw_receipts = []
    for eta, p3 in [([F(4, 5), F(3, 4), F(1, 5)], F(10, 21)),
                    ([F(1, 5), F(2, 5), F(3, 5), F(1, 7), F(2, 7)], F(1, 3))]:
        receipt = fw(eta, p3, p3 * p3 / 16)
        receipt["eta"] = list(map(str, eta))
        fw_receipts.append(receipt)
    results = {"status": "PASS", "arithmetic": "Python standard-library Fraction",
               "seed": 16062026, "compressed_vs_full_cases": diagnostics,
               "complex_phase_gauge_cases": 8, "good_label_anchor_check": "PASS",
               "large_constrained_family": large_receipt, "screen_boundary_checks": screen_checks,
               "interior_truncation_gap": str(up2 - lo2), "fw": fw_receipts,
               "elapsed_seconds": time.monotonic() - started,
               "scope": "Finite algebra and implementation checks; global results use PROOF.md"}
    out = HERE / "results.json"
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"status": results["status"], "oracle_cases": len(diagnostics),
                      "large_exact_F": large_receipt["F"], "large_candidate_evaluations": count,
                      "FW_updates": [r["updates"] for r in fw_receipts],
                      "elapsed_seconds": results["elapsed_seconds"],
                      "results_sha256": hashlib.sha256(out.read_bytes()).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
