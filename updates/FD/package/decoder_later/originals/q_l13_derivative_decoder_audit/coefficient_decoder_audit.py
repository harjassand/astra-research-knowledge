#!/usr/bin/env python3
"""Finite exact audit of shifted-flat ANF coefficient decoding and B corruption."""
from itertools import combinations, product
import json
from pathlib import Path


def masks_upto(n, d):
    out = []
    for k in range(min(d, n) + 1):
        for inds in combinations(range(n), k):
            m = 0
            for i in inds:
                m |= 1 << i
            out.append(m)
    return out


def submasks(mask):
    s = mask
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & mask


def monomial(mask, x):
    return int((mask & x) == mask)


def eval_anf(coeff, x):
    value = 0
    for m, c in coeff.items():
        if c and monomial(m, x):
            value ^= 1
    return value


def decode_coefficients(labels, centers, n, d):
    """Sequential peeling, reusing the same shifted balls at every degree."""
    learned = {}
    by_degree = {k: [m for m in masks_upto(n, d) if m.bit_count() == k]
                 for k in range(min(n, d) + 1)}
    for k in range(min(n, d), -1, -1):
        for s in by_degree[k]:
            votes = []
            for x in centers:
                parity = 0
                for t in submasks(s):
                    parity ^= labels[x ^ t]
                # For U containing S, Delta_S(x_U)=x_(U\S).
                for u, c in learned.items():
                    if c and u != s and (u & s) == s:
                        parity ^= monomial(u ^ s, x)
                votes.append(parity)
            ones = sum(votes)
            if 2 * ones == len(votes):
                learned[s] = None
            else:
                learned[s] = int(2 * ones > len(votes))
    return learned


def rank_bits(x, n):
    # Keep bit 0 as the first (most significant) output coordinate.
    return tuple((x >> i) & 1 for i in range(n))


def q_map(x, n):
    bits = list(rank_bits(x, n))
    bits[1] ^= bits[2] & bits[3]
    return tuple(bits)


def lex_compare(x, y, n):
    return int(q_map(x, n) < q_map(y, n))


def comparison_label_table(n, bad_item, v, forward_bad, reverse_bad):
    N = 1 << n
    labels = []
    for x in range(N):
        y = x ^ v
        if x == bad_item and y != bad_item:
            c = forward_bad
        elif y == bad_item and x != bad_item:
            c = reverse_bad
        else:
            c = lex_compare(x, y, n)
        labels.append(1 ^ c)
    return labels


def main():
    n, d = 5, 2
    N = 1 << n
    all_centers = list(range(N))
    all_masks = masks_upto(n, d)
    # q_1=x_1+x_2*x_3, represented in bit positions 1, {2,3}.
    true_coeff = {m: 0 for m in all_masks}
    true_coeff[1 << 1] = 1
    true_coeff[(1 << 2) | (1 << 3)] = 1
    clean = [eval_anf(true_coeff, x) for x in range(N)]

    # Exhaust every fixed label error set of size at most two. This includes
    # the full B union (B+v) support allowed by one bad comparison item.
    support_cases = 0
    max_parity_error_fraction = {str(k): 0.0 for k in range(d + 1)}
    for e_size in range(3):
        for err_points in combinations(range(N), e_size):
            support_cases += 1
            err = set(err_points)
            labels = [clean[x] ^ int(x in err) for x in range(N)]
            decoded = decode_coefficients(labels, all_centers, n, d)
            assert decoded == true_coeff, (err_points, decoded)
            for s in all_masks:
                k = s.bit_count()
                bad_parities = 0
                for x in all_centers:
                    parity_error = 0
                    for t in submasks(s):
                        parity_error ^= int((x ^ t) in err)
                    bad_parities += parity_error
                max_parity_error_fraction[str(k)] = max(
                    max_parity_error_fraction[str(k)], bad_parities / N)
                assert bad_parities <= (1 << k) * e_size

    # Exact comparison-oracle check. Q is a degree-two bijection, v=e_1
    # preserves q_0 and toggles q_1. For each singleton B, enumerate all four
    # arbitrary directed answers on the affected pair. Equal answers are
    # explicitly non-antisymmetric. Every resulting label table decodes.
    v = 1 << 1
    comparison_cases = 0
    observed_label_error_max = 0
    nonantisymmetric_cases = 0
    for bad in range(N):
        for fwd, rev in product((0, 1), repeat=2):
            labels = comparison_label_table(n, bad, v, fwd, rev)
            errors = sum(labels[x] != clean[x] for x in range(N))
            observed_label_error_max = max(observed_label_error_max, errors)
            assert errors <= 2
            if fwd == rev:
                nonantisymmetric_cases += 1
                assert fwd + rev != 1
            decoded = decode_coefficients(labels, all_centers, n, d)
            assert decoded == true_coeff, (bad, fwd, rev, errors, decoded)
            comparison_cases += 1

    # The strict radius is real for this local estimator. A single bad point
    # in F2^3 has density 1/8=2^(-d-1) for d=2. Its parity on every shifted
    # {0,e0,e1,e0+e1} flat is wrong on exactly half the centers.
    boundary_n = 3
    boundary_s = (1 << 0) | (1 << 1)
    boundary_errors = {0}
    boundary_bad = 0
    for x in range(1 << boundary_n):
        parity_error = 0
        for t in submasks(boundary_s):
            parity_error ^= int((x ^ t) in boundary_errors)
        boundary_bad += parity_error
    assert boundary_bad * 2 == (1 << boundary_n)

    receipt = {
        "status": "PASS",
        "scope": "exact finite audit only; theorem is analytic",
        "n": n,
        "d": d,
        "domain_size": N,
        "monomial_count": len(all_masks),
        "fixed_teacher_error_supports_exhausted": support_cases,
        "maximum_shift_parity_error_fraction_by_degree": max_parity_error_fraction,
        "comparison_cases": comparison_cases,
        "bad_item_locations_exhausted": N,
        "arbitrary_directed_answers_per_bad_translation_pair": 4,
        "nonantisymmetric_comparison_cases": nonantisymmetric_cases,
        "maximum_raw_label_errors_in_comparison_cases": observed_label_error_max,
        "strict_radius_boundary_witness": {
            "n": boundary_n,
            "d": 2,
            "error_support_size": 1,
            "error_density": 1 / (1 << boundary_n),
            "top_coefficient_parity_error_fraction": boundary_bad / (1 << boundary_n),
        },
        "comparison_interface": "C(x,y) exact for clean endpoints; arbitrary independently directed answers for pairs incident to B",
        "decoder_centers": "all 32 centers (finite exhaustive verification, not a randomized run)",
        "verified": [
            "all ANF coefficients recovered for every fixed error support of size 0, 1, or 2",
            "every degree-k parity error count is at most 2^k times the support size",
            "all singleton-B directed-comparison assignments recover the exact quadratic coordinate",
            "equal values on both orientations were included, so antisymmetry was not assumed",
            "at rho=2^(-d-1), a fixed single-point error makes one degree-d parity wrong on half of all shifts",
        ],
    }
    Path(__file__).with_name("coefficient_decoder_audit.json").write_text(
        json.dumps(receipt, indent=2) + "\n"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
