#!/usr/bin/env python3
"""Exact finite diagnostics for a CLE-equivalent, state-dependent CRN pair.

All rate vectors and likelihood-overlap calculations use rational arithmetic.
This script checks the stated toy interface; it is not a chemical validation.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json
from math import comb
from pathlib import Path


YIELDS = (1, 2, 3, 4)
W = (-1, 3, -3, 1)
ALPHA_A = (F(11, 10), F(11, 10), F(41, 10), F(1, 10))
ALPHA_B = (F(1, 10), F(41, 10), F(11, 10), F(11, 10))
BETA_A = (3, 1, 8, 5)
BETA_B = (2, 4, 5, 6)


def moments(theta):
    return tuple(sum(F(a) * k**j for a, k in zip(theta, YIELDS)) for j in range(4))


def propensities(alpha, beta, c, volume=1):
    pair_count = F(c * (c - 1), 2)
    return tuple(F(alpha[k]) * c + F(beta[k]) * pair_count / volume for k in range(4))


def mark_probabilities(alpha, beta, c, volume=1):
    a = propensities(alpha, beta, c, volume)
    z = sum(a)
    return tuple(v / z for v in a)


def assay_path_pair(c0=2, volume=1, erasure=F(0)):
    """One full product-mark sequence through depletion from c0 to zero.

    The denominator is common to both hypotheses. Each event label is either
    one of 1..4 or, with probability `erasure`, a common erasure symbol.
    """
    per_state = []
    common_denominator = 1
    for c in range(c0, 0, -1):
        pa = mark_probabilities(ALPHA_A, BETA_A, c, volume)
        pb = mark_probabilities(ALPHA_B, BETA_B, c, volume)
        den = 1
        for q in pa:
            den = den * q.denominator // __import__("math").gcd(den, q.denominator)
        den = den * erasure.denominator // __import__("math").gcd(den, erasure.denominator)
        # Convert probabilities to integer counts on a shared denominator.
        aa = [int((1 - erasure) * q * den) for q in pa] + [int(erasure * den)]
        bb = [int((1 - erasure) * q * den) for q in pb] + [int(erasure * den)]
        per_state.append((aa, bb, den))
        common_denominator *= den

    # Each tuple is one state-indexed readout path and has probability pair
    # (integer_a/common_denominator, integer_b/common_denominator).
    outcomes = [(1, 1)]
    for aa, bb, _den in per_state:
        outcomes = [(pa * aa[z], pb * bb[z])
                    for pa, pb in outcomes for z in range(len(aa))]
    return outcomes, common_denominator


def group_likelihood_ratios(outcomes):
    groups = defaultdict(lambda: [0, 0])
    for pa, pb in outcomes:
        if pa == 0 or pb == 0:
            continue  # these observations have zero overlap under the two laws
        groups[F(pa, pb)][0] += pa
        groups[F(pa, pb)][1] += pb
    return dict((lr, tuple(v)) for lr, v in groups.items())


def repeated_path_overlap(outcomes, denominator, replicates):
    """Exact sum of type-I and type-II errors for the optimal simple LRT."""
    cats = group_likelihood_ratios(outcomes)
    dp = {F(1): (1, 1)}
    for _ in range(replicates):
        nxt = defaultdict(lambda: [0, 0])
        for lr1, (a1, b1) in dp.items():
            for lr2, (a2, b2) in cats.items():
                key = lr1 * lr2
                nxt[key][0] += a1 * a2
                nxt[key][1] += b1 * b2
        dp = {lr: tuple(v) for lr, v in nxt.items()}
    overlap_num = sum(min(a, b) for a, b in dp.values())
    return F(overlap_num, denominator**replicates)


def endpoint_numerators(c0=2, volume=1):
    """Integer probabilities of total product at complete depletion."""
    pa = {0: F(1)}
    pb = {0: F(1)}
    for c in range(c0, 0, -1):
        qa = mark_probabilities(ALPHA_A, BETA_A, c, volume)
        qb = mark_probabilities(ALPHA_B, BETA_B, c, volume)
        na = defaultdict(F)
        nb = defaultdict(F)
        for x, p in pa.items():
            for k, pk in zip(YIELDS, qa):
                na[x + k] += p * pk
        for x, p in pb.items():
            for k, pk in zip(YIELDS, qb):
                nb[x + k] += p * pk
        pa, pb = dict(na), dict(nb)
    den = 1
    for p in (*pa.values(), *pb.values()):
        den = den * p.denominator // __import__("math").gcd(den, p.denominator)
    return den, {x: int(p * den) for x, p in pa.items()}, {x: int(p * den) for x, p in pb.items()}


def endpoint_overlap_exact(den, pa, pb, n):
    """Exact LRT overlap by enumerating multinomial counts on common support."""
    common = [k for k in pa if pa[k] and pb.get(k, 0)]
    vals_a = [pa[k] for k in common]
    vals_b = [pb[k] for k in common]
    total = 0

    def walk(i, remaining, counts):
        nonlocal total
        if i == len(common) - 1:
            cs = counts + [remaining]
            mcoef = comb(n, cs[0])
            used = cs[0]
            for z in range(1, len(cs)):
                mcoef *= comb(n - used, cs[z])
                used += cs[z]
            a = mcoef
            b = mcoef
            for x, y, count in zip(vals_a, vals_b, cs):
                a *= x**count
                b *= y**count
            total += min(a, b)
            return
        for z in range(remaining + 1):
            walk(i + 1, remaining - z, counts + [z])

    walk(0, n, [])
    return F(total, den**n)


def main():
    ma, mb = moments(ALPHA_A), moments(ALPHA_B)
    qa, qb = moments(BETA_A), moments(BETA_B)
    assert ma[:3] == mb[:3] == (F(32, 5), 16, 44)
    assert qa[:3] == qb[:3] == (17, 49, 159)
    assert mb[3] - ma[3] == qb[3] - qa[3] == 6
    assert tuple(b - a for a, b in zip(ALPHA_A, ALPHA_B)) == W
    assert tuple(b - a for a, b in zip(BETA_A, BETA_B)) == W

    path, path_den = assay_path_pair(2, 1)
    path_overlaps = [repeated_path_overlap(path, path_den, n) for n in range(1, 7)]
    assert path_overlaps[4] > F(1, 20) > path_overlaps[5]
    endpoint_den, endpoint_a, endpoint_b = endpoint_numerators(2, 1)
    endpoint_overlaps = {n: endpoint_overlap_exact(endpoint_den, endpoint_a, endpoint_b, n)
                         for n in (1, 6, 20)}
    assert endpoint_overlaps[6] > path_overlaps[5]

    noisy_path, noisy_den = assay_path_pair(2, 1, F(1, 10))
    noisy_overlaps = [repeated_path_overlap(noisy_path, noisy_den, n) for n in range(1, 7)]
    assert noisy_overlaps[4] > F(1, 20) > noisy_overlaps[5]

    out = {
        "status": "finite exact arithmetic diagnostics for stated model only",
        "first_order_moments_A": [str(x) for x in ma],
        "first_order_moments_B": [str(x) for x in mb],
        "second_order_moments_A": [str(x) for x in qa],
        "second_order_moments_B": [str(x) for x in qb],
        "jump_tensor_difference": "only PPP component differs; B-A=6 per source coefficient",
        "initial_C_path": [str(x) for x in path_overlaps],
        "event_path_minimal_replicates_at_5_percent_sum_error": 6,
        "terminal_total_P_overlap": {str(k): {"fraction": str(v), "decimal": float(v)}
                                     for k, v in endpoint_overlaps.items()},
        "10_percent_independent_mark_erasure": {
            "six_assay_overlap_fraction": str(noisy_overlaps[5]),
            "six_assay_overlap_decimal": float(noisy_overlaps[5]),
            "five_assay_overlap_decimal": float(noisy_overlaps[4]),
        },
        "terminal_total_P_law": {
            str(k): {"A": str(F(endpoint_a[k], endpoint_den)),
                     "B": str(F(endpoint_b[k], endpoint_den))}
            for k in sorted(set(endpoint_a) | set(endpoint_b))
        },
    }
    target = Path(__file__).with_name("STATE_DEPENDENT_DIAGNOSTICS.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
