#!/usr/bin/env python3
"""Fresh exact checks for the ancestry prose intake (stdlib Fractions only).

This is not a replay of a producer: the incoming ancestry item is prose-only.
The checks are finite algebra diagnostics for statements proved separately in
REPORT.md.  No capital or source-directory code is imported or executed.
"""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def matvec(M, x):
    return [sum((a * b for a, b in zip(row, x)), F(0)) for row in M]


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def count_law_from_probabilities(ps):
    out = [F(1)]
    for p in ps:
        out = poly_mul(out, [1 - p, p])
    return out


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def main():
    # Explicit four-to-three random deletion channel, columns indexed by parent K.
    D = [
        [F(1), F(1, 4), F(0), F(0), F(0)],
        [F(0), F(3, 4), F(1, 2), F(0), F(0)],
        [F(0), F(0), F(1, 2), F(3, 4), F(0)],
        [F(0), F(0), F(0), F(1, 4), F(1)],
    ]
    p_even = [F(1, 8), F(0), F(6, 8), F(0), F(1, 8)]
    p_odd = [F(0), F(4, 8), F(0), F(4, 8), F(0)]
    q_even = matvec(D, p_even)
    q_odd = matvec(D, p_odd)
    v = [F(1), F(-4), F(6), F(-4), F(1)]
    parity_w = [F(1), F(-1), F(1), F(-1), F(1)]
    dv = matvec(D, v)
    col_sums = [sum((D[i][j] for i in range(4)), F(0)) for j in range(5)]
    row_sum = [sum((D[i][j] for i in range(4)), F(0)) for j in range(5)]
    leading_minor_det = D[0][0] * D[1][1] * D[2][2] * D[3][3]
    assert q_even == q_odd == [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
    assert dv == [0, 0, 0, 0]
    assert sum(v) == 0 and dot(parity_w, v) == 16
    assert col_sums == [1] * 5
    assert row_sum == [1] * 5 and leading_minor_det == F(3, 32)

    # Full-histogram and parity Fisher information for the exact E/O family.
    # q_theta = Binomial(4,1/2) + (2 theta - 1) a^4 v/16.
    a = F(49, 50)
    a4, a8 = a**4, a**8
    qbar = [F(1, 16), F(4, 16), F(6, 16), F(4, 16), F(1, 16)]
    dq = [a4 * x / 8 for x in v]
    q_mid = qbar[:]
    fi_full_eo_mid = sum((dqk * dqk / qk for dqk, qk in zip(dq, q_mid)), F(0))
    # Parity is exactly sufficient in this constructed one-parameter E/O family.
    m_mid = dot(parity_w, q_mid)
    m_prime = dot(parity_w, dq)
    fi_parity_eo_mid = m_prime**2 / (1 - m_mid**2)
    eta = F(2, 3)
    fi_per_detected_event = eta * fi_full_eo_mid
    assert fi_full_eo_mid == 4 * a8
    assert fi_parity_eo_mid == fi_full_eo_mid
    assert fi_per_detected_event == 4 * eta * a8

    # A strict data-processing example: K~Binomial(2,theta), parity coarsened.
    theta = F(1, 4)
    q2 = [(1-theta)**2, 2*theta*(1-theta), theta**2]
    dq2 = [-2*(1-theta), 2-4*theta, 2*theta]
    fi_full_bin2 = sum((d*d/q for d, q in zip(dq2, q2)), F(0))
    q_even2 = q2[0] + q2[2]
    dq_even2 = dq2[0] + dq2[2]
    m2 = 2*q_even2 - 1
    dm2 = 2*dq_even2
    fi_parity_bin2 = dm2**2 / (1-m2**2)
    assert fi_full_bin2 == F(32, 3)
    assert fi_parity_bin2 == F(64, 15)
    assert fi_parity_bin2 < fi_full_bin2

    # Product count law is invariant to a permutation of the same age multiset.
    p_by_age = {0: F(1, 5), 1: F(3, 7), 2: F(4, 5), 3: F(2, 9)}
    ages_1 = [0, 1, 1, 3]
    ages_2 = [3, 1, 0, 1]
    law_1 = count_law_from_probabilities([p_by_age[a] for a in ages_1])
    law_2 = count_law_from_probabilities([p_by_age[a] for a in ages_2])
    assert law_1 == law_2 and sum(law_1) == 1
    # Equal marginal p=1/2 does not fix the count law without label independence.
    independent_two_label_law = count_law_from_probabilities([F(1, 2), F(1, 2)])
    common_batch_law = [F(1, 2), F(0), F(1, 2)]
    assert independent_two_label_law == [F(1, 4), F(1, 2), F(1, 4)]
    assert common_batch_law != independent_two_label_law

    # Fair stationary two-state telegraph path: sign reversal cancels odd products.
    # Exact finite CTMC spot-check (initial sign fair; per-gap flip probability 1/4).
    flip = F(1, 4)
    signs = [-1, 1]
    odd_product_mean = F(0)
    for path in product(signs, repeat=5):
        prob = F(1, 2)
        for s0, s1 in zip(path, path[1:]):
            prob *= flip if s0 != s1 else (1-flip)
        odd_product_mean += prob * F(path[0]*path[1]*path[2]*path[3]*path[4])
    assert odd_product_mean == 0

    # Linear marking expectation: sum of marked eligible-atom fate probabilities.
    epsilon = F(1, 4)
    fate_probs = [F(1, 2), F(1, 3), F(1, 4)]
    expected_marked_fates = epsilon * sum(fate_probs, F(0))
    assert expected_marked_fates == F(13, 48)

    result = {
        "scope": "exact finite algebra checks only; not physical or external validation",
        "random_single_carbon_deletion": {
            "P_even_parent": [str(x) for x in p_even],
            "P_odd_parent": [str(x) for x in p_odd],
            "shared_fragment_distribution": [str(x) for x in q_even],
            "D_times_v": [str(x) for x in dv],
            "normalization_null_witness_sum_v": str(sum(v)),
            "parity_target_dot_v": str(dot(parity_w, v)),
            "detector_column_sums": [str(x) for x in col_sums],
            "detector_rank": 4,
            "leading_4_by_4_minor_determinant": str(leading_minor_det),
            "normalization_already_in_detector_row_span": row_sum == [1] * 5,
        },
        "fisher_information": {
            "isotope_contrast_a": str(a),
            "intact_fraction_eta": str(eta),
            "E_O_full_count_FI_at_mixture_midpoint": str(fi_full_eo_mid),
            "E_O_parity_FI_at_mixture_midpoint": str(fi_parity_eo_mid),
            "E_O_FI_per_detected_event_with_uninformative_fragments": str(fi_per_detected_event),
            "scaling": "4 * eta * a^8 for this specified E/O local model",
            "Binomial_2_full_FI_theta_1_4": str(fi_full_bin2),
            "Binomial_2_parity_FI_theta_1_4": str(fi_parity_bin2),
            "strict_data_processing": fi_parity_bin2 < fi_full_bin2,
        },
        "all_waveform_map": {
            "age_multiset": ages_1,
            "permuted_age_multiset": ages_2,
            "exact_count_law": [str(x) for x in law_1],
        },
        "label_independence_counterexample": {
            "per_atom_marginal_heavy_probability": "1/2",
            "independent_label_count_law": [str(x) for x in independent_two_label_law],
            "shared_fair_batch_label_count_law": [str(x) for x in common_batch_law],
            "same_marginals_different_count_law": common_batch_law != independent_two_label_law,
        },
        "odd_telegraph_product_mean_n5_exact_spot_check": str(odd_product_mean),
        "mark_fate_linearity_example": {
            "epsilon": str(epsilon),
            "eligible_atom_fate_probabilities": [str(x) for x in fate_probs],
            "expected_marked_fates": str(expected_marked_fates),
        },
        "assertions": "all passed",
    }
    out = Path(__file__).with_name("independent_checks.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
