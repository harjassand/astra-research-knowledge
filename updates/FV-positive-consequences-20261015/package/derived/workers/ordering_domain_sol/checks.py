#!/usr/bin/env python3
"""Exact rational identities and small floating diagnostics; not proof premises."""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def matrix_det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def geometric_variance(eta, scale):
    r = (1 - eta) / (1 + eta)
    lhs = 2 * (2 * scale) ** 2 * r / (1 - r) ** 2
    rhs = 2 * scale ** 2 * (eta ** -2 - 1)
    assert lhs == rhs
    return r, lhs


def main():
    counts = {"variance_identity": 0, "fiber_gap_identity": 0,
              "qubit_determinant": 0, "variance_region_equivalence": 0}
    for i in range(1, 20):
        r = F(i, 20)
        gap = ((1 + r) ** 2 / 4 + r - 2 * r) / (1 - r) ** 2
        assert gap == F(1, 4)
        counts["fiber_gap_identity"] += 1
        for j in range(1, 11):
            geometric_variance(r, F(j, 7))
            counts["variance_identity"] += 1

    # U=sigma_z, V=(3/5)sigma_x+(4/5)sigma_z. All coefficients rational.
    c = F(4, 5)
    d = F(3, 5)
    for i in range(-10, 11):
        m = F(i, 10)
        for j in range(-10, 11):
            n = F(j, 10)
            scalar = 1 + m * n * c
            matrix = [[scalar + m + n * c, n * d],
                      [n * d, scalar - m - n * c]]
            determinant = 1 - m * m - n * n + c * c * m * m * n * n
            assert matrix_det(matrix) == determinant
            counts["qubit_determinant"] += 1
            if m and n:
                x = m ** -2 - 1
                y = n ** -2 - 1
                assert (determinant >= 0) == (x * y >= d * d)
                counts["variance_region_equivalence"] += 1

    # A fully exact boundary witness for the orthogonal Pauli pair.
    eta1, eta2 = F(3, 5), F(4, 5)
    r1, v1 = geometric_variance(eta1, F(1))
    r2, v2 = geometric_variance(eta2, F(1))
    assert r1 == F(1, 4) and r2 == F(1, 9)
    assert v1 == F(32, 9) and v2 == F(9, 8) and v1 * v2 == 4
    for eps in [-1, 1]:
        for tau in [-1, 1]:
            effect4 = [[1 + eps * eta1, tau * eta2],
                       [tau * eta2, 1 - eps * eta1]]
            assert matrix_det(effect4) == 0
            assert effect4[0][0] > 0 and effect4[1][1] > 0

    # Equal-weight orthogonal optimum and finite-output budgets.
    eta = 1 / math.sqrt(2)
    r = (1 - eta) / (1 + eta)
    alpha = math.atanh(eta)
    beta = alpha / 2
    q = r * math.exp(2 * beta)
    D = (1 - r) * math.exp(beta) / (1 - q)
    desired = 1e-6
    N = max(0, math.ceil(math.log(2 * D * D / desired) / (2 * (alpha - beta))) - 1)
    tilt_bound = D * D * 2 * q ** (N + 1)
    tv_bound = 2 * r ** (N + 1)
    assert tilt_bound <= desired
    result = {
        "status": "PASSED_DIAGNOSTICS_ONLY",
        "exact_identity_counts": counts,
        "exact_boundary_example": {"eta1": str(eta1), "eta2": str(eta2),
                                   "r1": str(r1), "r2": str(r2),
                                   "v1": str(v1), "v2": str(v2),
                                   "variance_product": str(v1 * v2)},
        "equal_pauli_optimum_diagnostic": {
            "eta": eta, "geometric_ratio": r, "moment_half_width": alpha,
            "noise_variance_each": 2,
            "full_report_second_moment_each": 3,
            "conditioned_report_second_moment_each": 2,
            "maximally_mixed_sample_mean_copy_ratio": 1.5,
            "largest_scaled_euclidean_domain_radius": math.sqrt(2) * math.asinh(1)},
        "finite_output_example": {"requested_tilt_half_width": beta,
                                  "requested_operator_error": desired,
                                  "N_each": N, "max_magnitude_each": 2 * N + 1,
                                  "alphabet_size_upper_bound": 4 * (N + 1) ** 2,
                                  "uniform_tilt_error_bound": tilt_bound,
                                  "uniform_state_TV_bound": tv_bound},
        "proof_sha256": hashlib.sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
        "limits": "Finite rational identities and floating diagnostics do not establish the universal theorem or historical novelty."
    }
    (HERE / "CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
