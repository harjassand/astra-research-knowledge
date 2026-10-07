"""Exact adversarial checks for raw and phase-matched low-sector estimators.

All arithmetic is integer Gaussian/rational. The peer sampler is imported only
from the copy in this directory, made before execution as required by the
phase-two audit. Fixtures have n<=8 and enumerate at most 256 sign words.
"""
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import json
from fractions import Fraction as Q

from peer_low_sector_sampler_copy import LowSector

ZERO = (0, 0)
ONE = (1, 0)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    return -a[0], -a[1]


def mul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def abs2(a):
    return a[0] * a[0] + a[1] * a[1]


def det(A):
    n = len(A)
    if n == 0:
        return ONE
    ans = ZERO
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        x = ONE
        for i, j in enumerate(p):
            x = mul(x, A[i][j])
        ans = add(ans, neg(x) if inv & 1 else x)
    return ans


def pf(A):
    n = len(A)
    if n == 0:
        return ONE
    if n % 2:
        return ZERO
    ans = ZERO
    for j in range(1, n):
        rest = [r for r in range(1, n) if r != j]
        x = mul(A[0][j], pf([[A[r][c] for c in rest] for r in rest]))
        ans = add(ans, neg(x) if j % 2 == 0 else x)
    return ans


def skew(F, signs, phased):
    gammas = [(0, s) if phased and i % 2 else (s, 0)
              for i, s in enumerate(signs)]
    n = len(F)
    return [[add(mul(gammas[i], F[i][j]), neg(mul(F[j][i], gammas[j])))
             for j in range(n)] for i in range(n)]


def sector_norm(F, k):
    n = len(F)
    total = 0
    for I in combinations(range(n), k):
        for J in combinations([j for j in range(n) if j not in I], k):
            d = det([[F[i][j] for j in J] for i in I])
            total += abs2(d)
    return total


def estimator_samples(F, k, phased):
    n = len(F)
    out = []
    for signs in product((-1, 1), repeat=n):
        A = skew(F, signs, phased)
        out.append(sum(abs2(pf([[A[i][j] for j in R] for i in R]))
                       for R in combinations(range(n), 2 * k)))
    return out


def exact_matching_certificate(F, k):
    n = len(F)
    G = [[F[i][i] if i == j else ZERO for j in range(n)] for i in range(n)]
    beta = []
    for i in range(0, n, 2):
        a, b = F[i][i + 1][0], F[i + 1][i][0]
        G[i][i + 1], G[i + 1][i] = (a, 0), (b, 0)
        beta.append(a * a + b * b)
    residual = sum(abs2(add(F[i][j], neg(G[i][j])))
                   for i in range(n) for j in range(n))
    beta = [Q(x) for x in beta]
    residual = Q(residual)
    threshold = None if k == 0 else min(beta, default=Q(0)) / (256 * k * k)
    accepted = (k == 0 or (min(beta, default=Q(0)) > 0 and residual <= threshold))
    return {"accepted": accepted, "beta": beta, "residual_squared": residual,
            "threshold": threshold}


def summary(samples):
    mean = Q(sum(samples), len(samples))
    second = Q(sum(x * x for x in samples), len(samples))
    return {"sample_count": len(samples), "mean": mean,
            "second_moment_ratio": None if mean == 0 else second / (mean * mean),
            "zero_count": sum(x == 0 for x in samples),
            "zero_probability": Q(sum(x == 0 for x in samples), len(samples)),
            "positive_values": sorted(set(x for x in samples if x > 0))}


def adjacent_swaps(m):
    n = 2 * m
    F = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(0, n, 2):
        F[i][i + 1] = F[i + 1][i] = ONE
    return F


def perturbed_adjacent_swaps(m, denominator=256):
    """Rational-complex residual near a nonuniform positive matching."""
    n = 2 * m
    F = [[(Q(0), Q(0)) for _ in range(n)] for _ in range(n)]
    for pair, i in enumerate(range(0, n, 2)):
        F[i][i + 1] = (Q(1) + Q(pair, 7), Q(0))
        F[i + 1][i] = (Q(1) - Q(pair, 11), Q(0))
    for i in range(n):
        for j in range(n):
            if i == j or j == i + 1 and i % 2 == 0 or i == j + 1 and j % 2 == 0:
                continue
            re = Q((-1) ** (i + 2 * j), denominator)
            im = Q((-1) ** (2 * i + j), 2 * denominator)
            F[i][j] = (re, im)
    return F


def parity_class_swaps(q):
    """n=4q; matching edges join equal index parity, not adjacent sites."""
    n = 4 * q
    F = [[ZERO for _ in range(n)] for _ in range(n)]
    pairs = []
    evens = list(range(0, n, 2))
    odds = list(range(1, n, 2))
    for group in (evens, odds):
        for j in range(0, len(group), 2):
            u, v = group[j], group[j + 1]
            F[u][v] = F[v][u] = ONE
            pairs.append((u, v))
    return F, pairs


def direct_prefix_count(F, k, up=(), down=(), empty=()):
    n = len(F)
    total = 0
    for I in combinations(range(n), k):
        I = set(I)
        for J in combinations([j for j in range(n) if j not in I], k):
            J = set(J)
            if not set(up) <= I or not set(down) <= J:
                continue
            if (I | J) & set(empty):
                continue
            d = det([[F[i][j] for j in sorted(J)] for i in sorted(I)])
            total += abs2(d)
    return total


def main():
    # The aligned paired-volume estimator is exactly constant after phases,
    # while its unphased control has the familiar rare-positive event.
    aligned = adjacent_swaps(3)
    unphased_aligned = summary(estimator_samples(aligned, 3, phased=False))
    phased_aligned = summary(estimator_samples(aligned, 3, phased=True))
    assert sector_norm(aligned, 3) == 8
    assert unphased_aligned["mean"] == 8 and unphased_aligned["second_moment_ratio"] == 8
    assert unphased_aligned["zero_probability"] == Q(7, 8)
    assert phased_aligned["mean"] == 8 and phased_aligned["second_moment_ratio"] == 1
    assert phased_aligned["zero_probability"] == 0
    aligned_cert = exact_matching_certificate(aligned, 3)
    assert aligned_cert["accepted"]

    # Exact perturbation audit: every sign word, every k, on rational-complex
    # inputs accepted by the squared-Frobenius matching certificate.
    perturbation_checks = []
    for m in (2, 3):
        matrix = perturbed_adjacent_swaps(m)
        for kk in range(1, m + 1):
            cert = exact_matching_certificate(matrix, kk)
            assert cert["accepted"], (m, kk, cert)
            baseline = [Q(1)] + [Q(0)] * m
            for beta in cert["beta"]:
                for d in range(m, 0, -1):
                    baseline[d] += beta * baseline[d - 1]
            values = estimator_samples(matrix, kk, phased=True)
            ratios = [Q(x) / baseline[kk] for x in values]
            assert all(Q(3, 4) <= x <= Q(4, 3) for x in ratios), (m, kk, cert, ratios)
            perturbation_checks.append({
                "n": 2 * m, "k": kk, "sign_words": len(values),
                "certificate": cert,
                "baseline_sector": baseline[kk],
                "min_sample_to_baseline_ratio": min(ratios),
                "max_sample_to_baseline_ratio": max(ratios),
            })

    # Negative control: the exact matching is misaligned with the acquired
    # adjacent pairing. Applying alternating phases alone leaves an exact
    # exponential-variance estimator; the certificate correctly abstains.
    F, pairs = parity_class_swaps(2)
    k, n = 4, 8
    phased_misaligned = summary(estimator_samples(F, k, phased=True))
    assert sector_norm(F, k) == 16
    assert phased_misaligned["mean"] == 16
    assert phased_misaligned["second_moment_ratio"] == 16
    assert phased_misaligned["zero_probability"] == Q(15, 16)
    misaligned_cert = exact_matching_certificate(F, k)
    assert not misaligned_cert["accepted"] and min(misaligned_cert["beta"]) == 0

    # Exact physical-prefix counterinstances. U={0} has mass 8; its estimator
    # is 64 on 1/8 of sign words and zero on 7/8. The formal C_ab=35 bound
    # still holds. Forcing one up site in every true matching pair leaves a
    # unique positive occupation and makes the prefix draw identically 1.
    low = LowSector(F)
    signs_all = list(product((-1, 1), repeat=n))
    prefix_up = (0,)
    mass = direct_prefix_count(F, k, up=prefix_up)
    draws = [low.prefix_draw_integer(k, s, up=prefix_up) for s in signs_all]
    a, b = 1, 0
    C_ab = comb(2 * k - a - b, k - a)
    assert mass == 8 and C_ab == 35
    prefix_summary = summary(draws)
    assert prefix_summary["mean"] == mass
    assert prefix_summary["zero_probability"] == Q(7, 8)
    assert prefix_summary["second_moment_ratio"] == 8
    assert max(draws) <= C_ab * mass
    forced_up = (0, 4, 1, 5)
    forced_mass = direct_prefix_count(F, k, up=forced_up)
    forced_draws = [low.prefix_draw_integer(k, s, up=forced_up) for s in signs_all]
    assert forced_mass == 1 and set(forced_draws) == {1}

    # Separate role restrictions at k<m exercise down-site inclusion-exclusion
    # and empty-site deletion. Compare every sign word to direct minor sums.
    role_cases = [
        {"k": 3, "up": (0,), "down": (), "empty": ()},
        {"k": 3, "up": (), "down": (0,), "empty": ()},
        {"k": 3, "up": (), "down": (), "empty": (0,)},
        {"k": 3, "up": (0,), "down": (), "empty": (2,)},
        {"k": 3, "up": (0,), "down": (4,), "empty": ()},
    ]
    role_outputs = []
    for case in role_cases:
        kk = case["k"]
        mass_case = direct_prefix_count(F, kk, case["up"], case["down"], case["empty"])
        vals = [low.prefix_draw_integer(kk, s, case["up"], case["down"], case["empty"])
                for s in signs_all]
        a_case, b_case = len(case["up"]), len(case["down"])
        cap_case = comb(2 * kk - a_case - b_case, kk - a_case)
        vals_summary = summary(vals)
        assert vals_summary["mean"] == mass_case, (case, vals_summary, mass_case)
        assert all(0 <= value <= cap_case * mass_case for value in vals), (case, vals, cap_case, mass_case)
        if mass_case == 0:
            assert not any(vals), (case, vals)
        else:
            assert vals_summary["second_moment_ratio"] <= cap_case, (case, vals_summary, cap_case)
        role_outputs.append({**case, "exact_prefix_mass": mass_case,
                             "C_ab": cap_case, "draw_summary": vals_summary,
                             "pointwise_bound_holds": all(0 <= value <= cap_case * mass_case
                                                           for value in vals)})

    out = {
        "status": "PASS",
        "source_program_copy": "peer_low_sector_sampler_copy.py",
        "aligned_adjacent_matching": {
            "n": 6, "k": 3, "exact_norm": 8,
            "certificate": aligned_cert,
            "unphased": unphased_aligned,
            "phased": phased_aligned,
        },
        "accepted_rational_complex_perturbation_checks": perturbation_checks,
        "misaligned_same_parity_matching": {
            "n": n, "k": k, "matching_pairs": pairs,
            "exact_norm": 16, "certificate": misaligned_cert,
            "phased_without_certificate": phased_misaligned,
        },
        "positive_prefix_with_false_zero_draws": {
            "n": n, "k": k, "up": list(prefix_up), "down": [], "empty": [],
            "exact_prefix_mass": mass, "C_ab": C_ab,
            "prefix_draw_distribution": prefix_summary,
            "pointwise_bound_holds": max(draws) <= C_ab * mass,
            "all_roles_forced": {
                "up": list(forced_up), "exact_prefix_mass": forced_mass,
                "distinct_prefix_draw_values": sorted(set(forced_draws)),
            },
        },
        "down_and_empty_role_checks": role_outputs,
        "interpretation": (
            "Formal low-k C_k and prefix bounds survive these checks. "
            "An alternating-phase heuristic without successful matching "
            "acquisition has exponential variance; the phase certificate "
            "rejects this family. Positive prefix mass may still yield a "
            "zero single draw, so zero is not a support certificate."
        ),
    }
    path = Path(__file__).with_name("phase_prefix_counterexamples.json")
    def encode(x):
        if isinstance(x, Q):
            return str(x)
        if isinstance(x, list):
            return [encode(y) for y in x]
        if isinstance(x, dict):
            return {key: encode(value) for key, value in x.items()}
        return x
    encoded = encode(out)
    path.write_text(json.dumps(encoded, indent=2) + "\n")
    print(json.dumps(encoded, indent=2))


if __name__ == "__main__":
    main()
