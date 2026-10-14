#!/usr/bin/env python3
"""Independent finite and numeric checks for the FL ancestry note.

This is a fresh reconstruction from the supplied note, not the producer script
mentioned there. It intentionally keeps synthetic checks separate from proofs.
Only Python's standard library is used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
import math
import random


BITS = tuple(product((0, 1), repeat=4))
EVEN = tuple(x for x in BITS if sum(x) % 2 == 0)
ODD = tuple(x for x in BITS if sum(x) % 2 == 1)


def parity(x):
    return sum(x) % 2


def marginal_distribution(rows, coords):
    return Counter(tuple(row[j] for j in coords) for row in rows)


def bernoulli_count_distribution(probabilities):
    dist = [F(1)]
    for p in probabilities:
        nxt = [F(0)] * (len(dist) + 1)
        for k, mass in enumerate(dist):
            nxt[k] += mass * (1 - p)
            nxt[k + 1] += mass * p
        dist = nxt
    return tuple(dist)


def mixed_count_distribution(rows, mask, p_low, p_high):
    out = [F(0)] * 5
    for x in rows:
        probabilities = [p_high if mask[j + xj] else p_low
                         for j, xj in enumerate(x)]
        conditional = bernoulli_count_distribution(probabilities)
        for k, mass in enumerate(conditional):
            out[k] += mass / 8
    return tuple(out)


def check_parity_marginals_and_masks():
    assert len(EVEN) == len(ODD) == 8
    compared_marginals = 0
    for size in range(1, 4):
        for coords in combinations(range(4), size):
            assert marginal_distribution(EVEN, coords) == marginal_distribution(ODD, coords)
            compared_marginals += 1
    assert compared_marginals == 14

    p_low, p_high = F(1, 100), F(99, 100)
    differing = []
    pulse_masks = 0
    checked = 0
    for mask in product((0, 1), repeat=5):
        e = mixed_count_distribution(EVEN, mask, p_low, p_high)
        o = mixed_count_distribution(ODD, mask, p_low, p_high)
        checked += 1
        if e != o:
            differing.append("".join(map(str, mask)))
        switches = sum(mask[j] != mask[j + 1] for j in range(4))
        if switches <= 2:
            pulse_masks += 1
            assert e == o
    assert checked == 32
    assert pulse_masks == 22
    assert len(differing) == 2
    assert set(differing) == {"01010", "10101"}
    return {
        "proper_coordinate_marginals_equal": compared_marginals,
        "five_node_masks_checked": checked,
        "masks_with_at_most_two_switches": pulse_masks,
        "count_law_distinguishing_masks_at_p_low_0.01_p_high_0.99": differing,
    }


def check_unequal_purity_recoding():
    p_low, p_high = F(1, 5), F(7, 10)
    a = p_high - p_low
    b = p_high + p_low - 1
    assert (a, b) == (F(1, 2), F(-1, 10))
    for signs in product((-1, 1), repeat=4):
        probabilities = [(1 + b + a * s) / 2 for s in signs]
        expected = F(0)
        for labels in product((-1, 1), repeat=4):
            probability = F(1)
            for label, p in zip(labels, probabilities):
                probability *= p if label == 1 else 1 - p
            k = sum(label == 1 for label in labels)
            weight = (1 - b) ** k * (-1 - b) ** (4 - k) / a**4
            expected += probability * weight
        assert expected == math.prod(signs)
    b_n = ((1 + abs(b)) / a) ** 4
    assert b_n == F(2_342_560, 100_000)
    return {
        "p_low": str(p_low),
        "p_high": str(p_high),
        "a": str(a),
        "b": str(b),
        "all_code_sign_patterns_checked": 16,
        "max_abs_product_weight_B4": str(b_n),
    }


def check_eo_age_laws_and_waveforms():
    # With ages A_j = C + (j + X_j) tau, the adjacent-pair length
    # is (A_4-A_3) + (A_2-A_1), in units of tau.
    lengths = {
        "E": Counter(2 + x[3] - x[2] + x[1] - x[0] for x in EVEN),
        "O": Counter(2 + x[3] - x[2] + x[1] - x[0] for x in ODD),
    }
    assert lengths["E"] == Counter({0: 1, 2: 6, 4: 1})
    assert lengths["O"] == Counter({1: 4, 3: 4})

    r_tau = 2.0
    x = math.exp(-2 * r_tau)
    q_e = (1 + 6 * x**2 + x**4) / 8
    q_o = (x + x**3) / 2
    gap = (1 - x) ** 4 / 8
    assert abs(q_e - 0.12525161103782373) < 2e-16
    assert abs(q_o - 0.009160891550543754) < 2e-16
    assert abs(q_e - q_o - 0.11609071948727998) < 2e-16
    assert abs(q_e - q_o - gap) < 2e-16

    # Verify Delta = (1/8) product_j (u_j-u_{j+1}) on exact rational inputs.
    waveform_examples = [
        tuple(map(F, (1, 1, -1, -1, 1))),
        tuple(map(F, (-1, 1, -1, 1, -1))),
        (F(1), F(1, 2), F(-1, 3), F(2, 3), F(-1)),
    ]
    deltas = []
    for u in waveform_examples:
        q_even = sum(math.prod(u[j + xj] for j, xj in enumerate(bits))
                     for bits in EVEN) / 8
        q_odd = sum(math.prod(u[j + xj] for j, xj in enumerate(bits))
                    for bits in ODD) / 8
        product_formula = math.prod(u[j] - u[j + 1] for j in range(4)) / 8
        assert q_even - q_odd == product_formula
        deltas.append(str(q_even - q_odd))

    alternating = tuple(map(F, (1, -1, 1, -1, 1)))
    assert deltas[1] == "2"
    assert math.prod(alternating[j] - alternating[j + 1] for j in range(4)) / 8 == 2

    # The square-wave age sign is (-1)^(j+X_j) times a common phase;
    # its four-factor product is exactly (-1)^sum X for every history.
    for bits in BITS:
        signs = [(-1) ** (j + bits[j]) for j in range(4)]
        assert math.prod(signs) == (-1) ** sum(bits)

    # At ideal pure levels, full count distributions are the even/odd
    # weight enumerators of the parity classes.
    pure_e = mixed_count_distribution(EVEN, (0, 1, 0, 1, 0), F(0), F(1))
    pure_o = mixed_count_distribution(ODD, (0, 1, 0, 1, 0), F(0), F(1))
    assert pure_e == (F(1, 8), F(0), F(3, 4), F(0), F(1, 8))
    assert pure_o == (F(0), F(1, 2), F(0), F(1, 2), F(0))
    imperfect_e = mixed_count_distribution(EVEN, (0, 1, 0, 1, 0), F(1, 100), F(99, 100))
    imperfect_o = mixed_count_distribution(ODD, (0, 1, 0, 1, 0), F(1, 100), F(99, 100))
    a = F(98, 100)
    corrected_e = sum(((-1) ** k) * mass for k, mass in enumerate(imperfect_e)) / a**4
    corrected_o = sum(((-1) ** k) * mass for k, mass in enumerate(imperfect_o)) / a**4
    assert corrected_e == 1 and corrected_o == -1
    return {
        "E_pair_gap_multiplicities_tau_units": dict(sorted(lengths["E"].items())),
        "O_pair_gap_multiplicities_tau_units": dict(sorted(lengths["O"].items())),
        "r_tau": r_tau,
        "x_exp_minus_2r_tau": x,
        "Q_E": q_e,
        "Q_O": q_o,
        "telegraph_contrast": q_e - q_o,
        "squarewave_corrected_E": 1,
        "squarewave_corrected_O": -1,
        "squarewave_corrected_contrast": 2,
        "pure_squarewave_count_law_E": [str(v) for v in pure_e],
        "pure_squarewave_count_law_O": [str(v) for v in pure_o],
        "imperfect_purity_squarewave_corrected_parity_E": str(corrected_e),
        "imperfect_purity_squarewave_corrected_parity_O": str(corrected_o),
        "mean_switch_rate_squarewave_over_telegraph_at_r_tau_2": "1/tau over 2/tau",
    }


def interval_overlap(intervals, shift):
    total = F(0)
    for ai, bi in intervals:
        for aj, bj in intervals:
            total += max(F(0), min(bi, bj + shift) - max(ai, aj + shift))
    return total


def exact_covariance_integral(intervals, rate):
    ell = sum((b - a for a, b in intervals), F(0))
    s_max = max(b for _, b in intervals) - min(a for a, _ in intervals)
    points = {F(0), s_max}
    for ai, bi in intervals:
        for aj, bj in intervals:
            for bp in (ai - aj, bi - aj, ai - bj, bi - bj):
                if 0 < bp < s_max:
                    points.add(bp)
    ordered = sorted(points)
    total = 0.0
    for left, right in zip(ordered, ordered[1:]):
        width = right - left
        h_left = interval_overlap(intervals, left)
        h_right = interval_overlap(intervals, right)
        delta_left, delta_right = ell - h_left, ell - h_right
        slope = (delta_right - delta_left) / width
        a = float(delta_left)
        w = float(width)
        lam = 4.0 * float(rate)
        if slope == 0:
            int_exp = math.exp(-lam * a) * w
        elif slope > 0:
            d = float(slope)
            int_exp = math.exp(-lam * a) * (-math.expm1(-lam * d * w)) / (lam * d)
        else:
            d = float(slope)
            right = float(delta_right)
            int_exp = math.exp(-lam * right) * (-math.expm1(lam * d * w)) / (-lam * d)
        total += int_exp - math.exp(-lam * float(ell)) * w
    return max(0.0, total)


def check_geometry_and_covariance(seed=20261014, samples=1000):
    rng = random.Random(seed)
    maximum_ratio = 0.0
    maximum_lemma_slack_error = 0.0
    cases = 0
    for _ in range(samples):
        m = rng.randint(1, 5)
        cursor = 0
        intervals = []
        for _j in range(m):
            cursor += rng.randint(1, 10_000)
            length = rng.randint(1, 100)
            intervals.append((F(cursor), F(cursor + length)))
            cursor += length
        ell = sum((b - a for a, b in intervals), F(0))
        rate = F(rng.randint(1, 100), rng.randint(1, 100))

        # Check the geometric inequality at every piecewise-linear breakpoint
        # and at the kink ell/m. This is an exact finite check of each sample.
        s_max = intervals[-1][1] - intervals[0][0]
        points = {F(0), s_max, ell / m}
        for ai, bi in intervals:
            for aj, bj in intervals:
                for bp in (ai - aj, bi - aj, ai - bj, bi - bj):
                    if 0 < bp < s_max:
                        points.add(bp)
        for s in points:
            if s == 0:
                continue
            h = interval_overlap(intervals, s)
            delta = ell - h
            rhs = min(s, ell / m)
            slack = delta - rhs
            maximum_lemma_slack_error = max(maximum_lemma_slack_error, max(0.0, -float(slack)))
            assert slack >= 0

        integral = exact_covariance_integral(intervals, rate)
        bound = (1.0 + m * m / math.e) / (4.0 * float(rate))
        ratio = integral / bound
        maximum_ratio = max(maximum_ratio, ratio)
        assert ratio <= 1.0 + 2e-11
        cases += 1
    return {
        "seed": seed,
        "interval_union_cases": cases,
        "components_per_case": "1..5",
        "component_integer_lengths": "1..100",
        "integer_gaps": "1..10000",
        "rates": "rational numerator and denominator in 1..100",
        "geometric_lemma_exact_breakpoint_checks": True,
        "max_negative_lemma_slack": maximum_lemma_slack_error,
        "max_covariance_integral_to_bound_ratio": maximum_ratio,
        "covariance_integrals": "independent exact piecewise-linear geometry, analytic exponential integration",
    }


def main():
    results = {
        "provenance": "independently reconstructed checks; original producer script was not supplied",
        "parity_marginals_and_single_pulse_masks": check_parity_marginals_and_masks(),
        "unequal_purity_recoding": check_unequal_purity_recoding(),
        "E_O_laws_and_waveforms": check_eo_age_laws_and_waveforms(),
        "geometry_and_covariance": check_geometry_and_covariance(),
    }
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
