#!/usr/bin/env python3
"""Independently recheck compiler output using this audit's Fourier algebra."""

from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path

import verify_weighted_audit as v


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]


def evaluate_terms(terms, values):
    total = F(0)
    for monomial, coefficient in terms.items():
        term = coefficient
        for value, exponent in zip(values, monomial):
            term *= value ** exponent
        total += term
    return total


def evaluate_fields(terms, fields):
    total = {}
    for monomial, coefficient in terms.items():
        term = {(0, 0): coefficient}
        for field, exponent in zip(fields, monomial):
            term = v.multiply(term, v.power(field, exponent))
        total = v.add(total, term)
    return total


def mixed_coefficient(terms, vectors):
    total = F(0)
    for mask in range(1 << len(vectors)):
        value = [F(0)] * 4
        for i, vector in enumerate(vectors):
            if mask & (1 << i):
                value = [x + y for x, y in zip(value, vector)]
        total += (-1) ** (len(vectors) - mask.bit_count()) * evaluate_terms(terms, value)
    return total


def read_fourier(items):
    return {tuple(item["frequency"]): F(item["complex_exponential_coefficient"]) for item in items}


def multiply_matrix(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inverse(a):
    d = det(a)
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def main():
    receipt_path = HERE / "compiler_replay/VERIFICATION_RECEIPT.json"
    receipt = json.loads(receipt_path.read_text())
    sigma = F(2)
    polynomials = {
        "forbidden_first_jet_cubic": {(1, 2, 0, 0): F(1)},
        "single_wave_invisible_cubic": {(2, 1, 0, 0): sigma, (0, 2, 1, 0): F(1)},
        "independent_defect_cubic": {(0, 2, 0, 1): F(1)},
        "target_cubic_exponent_obstruction": {
            (1, 0, 0, 2): F(2), (2, 0, 0, 1): F(-3), (0, 0, 2, 1): F(1),
            (0, 1, 1, 1): F(-2), (3, 0, 0, 0): F(-1), (1, 0, 2, 0): F(-1),
        },
        "single_wave_invisible_quartic": {
            (4, 0, 0, 0): sigma ** 2, (2, 1, 1, 0): 2 * sigma, (0, 2, 2, 0): F(1),
        },
        "quadratic_partial_determinant": {(1, 0, 0, 1): F(-1)},
    }
    grouped_results = {}
    for name, terms in polynomials.items():
        witness = receipt["witnesses"][name]
        m = witness["degree"]
        j = witness["leading_weight"]
        leading = {e: c for e, c in terms.items() if v.weight(e) == j}
        psi = read_fourier(witness["psi_fourier"])
        scalar = read_fourier(witness["k_fourier"])
        vectors = []
        cosine_product = {(0, 0): F(1)}
        frequency_slots = []
        groups = []
        for slot in witness["slots"]:
            x, y = slot["frequency"]
            frequency_slots.append((x, y))
            vector = (F(0), F(0), F(0), F(1)) if slot["source"] == "k" else (
                -F(x * y), -F(y * y), sigma * x * x, F(0)
            )
            vectors.append(vector)
            cosine_product = v.multiply(cosine_product, v.cosine(x, y))
            canonical = (x, y) if x > 0 else (-x, -y)
            group = (slot["source"], canonical)
            if group not in groups:
                groups.append(group)
        B = mixed_coefficient(leading, vectors)
        v.require(B == F(witness["resonance_mixed_coefficient"]) and B != 0, f"independent polarization {name}")
        v.require(v.average(cosine_product) == F(1, 2 ** (m - 1)), f"isolated cosine resonance {name}")
        signs = [choice for choice in product((-1, 1), repeat=m)
                 if all(sum(sign * freq[d] for sign, freq in zip(choice, frequency_slots)) == 0 for d in (0, 1))]
        v.require(len(signs) == 2, f"only two sign resonances {name}")

        # Reconstruct a witness after grouping repeated cosine frequencies,
        # so the stated bound applies to actual, distinct Fourier amplitudes.
        grouped_selected = None
        for amplitudes in product(range(1, m + 2), repeat=len(groups)):
            grouped_psi, grouped_scalar = {}, {}
            for (source, (x, y)), amplitude in zip(groups, amplitudes):
                if source == "k":
                    grouped_scalar = v.add(grouped_scalar, v.cosine(x, y, amplitude))
                else:
                    grouped_psi = v.add(grouped_psi, v.cosine(x, y, amplitude))
            xx, xy, yy = v.hessian(grouped_psi)
            fields = (xy, yy, v.scale(xx, -sigma), grouped_scalar)
            mean = v.average(evaluate_fields(leading, fields))
            if mean:
                grouped_selected = {"amplitudes": amplitudes, "leading_mean": str(mean), "distinct_groups": len(groups)}
                break
        v.require(grouped_selected is not None, f"bounded grouped amplitude search {name}")
        grouped_results[name] = grouped_selected

        for N in sorted({1, 2, witness["all_N_at_least"], witness["all_N_at_least"] + 1}):
            a, b, c, d, q = v.compatible_components(psi, scalar, sigma, N)
            actual = v.average(evaluate_fields(terms, (a, b, c, q)))
            expected = sum(F(coefficient) / N ** int(exponent)
                           for exponent, coefficient in witness["exact_signed_epsilon_polynomial"].items())
            v.require(actual == expected, f"independent exact average {name}, N={N}")
            if N >= witness["all_N_at_least"]:
                v.require(abs(actual) >= abs(F(witness["leading_signed_average"])) / (2 * N ** j),
                          f"exact divergence numerator {name}, N={N}")

    J = [[F(0), F(1)], [F(0), F(0)]]
    identity = [[F(1), F(0)], [F(0), F(1)]]
    invertible_matrices = []
    for entries in product(range(-2, 3), repeat=4):
        matrix = [[F(entries[0]), F(entries[1])], [F(entries[2]), F(entries[3])]]
        if det(matrix):
            invertible_matrices.append(matrix)
    for index in range(32):
        A = invertible_matrices[index]
        S = invertible_matrices[-1-index]
        N = multiply_matrix(multiply_matrix(S, J), inverse(S))
        B = multiply_matrix(A, N)
        recovered = multiply_matrix(inverse(A), B)
        v.require(multiply_matrix(recovered, recovered) == [[F(0), F(0)], [F(0), F(0)]],
                  f"nilpotent pencil {index}")
        basis_column = 0 if any(recovered[i][0] for i in range(2)) else 1
        basis_v = [F(int(i == basis_column)) for i in range(2)]
        basis_u = [recovered[i][basis_column] for i in range(2)]
        basis = [[basis_u[0], basis_v[0]], [basis_u[1], basis_v[1]]]
        v.require(det(basis) != 0, f"Jordan basis independent {index}")
        left = multiply_matrix(inverse(basis), inverse(A))
        v.require(multiply_matrix(multiply_matrix(left, A), basis) == identity, f"x-pencil coefficient {index}")
        v.require(multiply_matrix(multiply_matrix(left, B), basis) == J, f"y-pencil coefficient {index}")

    sources = [
        CAMPAIGN / "workers/ga_polynomial_genesis/EXTENSIONS_v1.md",
        CAMPAIGN / "workers/ga_polynomial_genesis/weighted_jet_verify.py",
    ]
    out = {
        "status": "PASS_FINITE_ALGEBRA_ONLY",
        "checks": len(v.CHECKS),
        "compiler_witnesses_independently_reconstructed": len(polynomials),
        "additional_pencil_fixtures": 32,
        "grouped_amplitude_witnesses": grouped_results,
        "source_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        "scope": "Independent standard-library rational Fourier and matrix algebra. General degree bounds, finite grid interpolation, localization, and analytic estimates remain written proofs, not formal verification.",
    }
    destination = HERE / "EXTENSION_AUDIT_RECEIPT.json"
    destination.write_text(json.dumps(out, indent=2) + "\n")
    print(f"PASS: {len(v.CHECKS)} exact independent checks; {destination}")


if __name__ == "__main__":
    main()
