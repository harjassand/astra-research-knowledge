#!/usr/bin/env python3
"""Exact matrix replay for the quadratic-dilation obstructions.

This verifies the displayed finite matrices and rational identities.  The
universal POVM lower bounds are proved in PROOF.txt, not inferred by this
script.  Requires SymPy; no solver and no floating-point arithmetic.
"""

import json
from pathlib import Path

import sympy as s


def kron(*matrices):
    result = s.Matrix([[1]])
    for matrix in matrices:
        result = s.kronecker_product(result, matrix)
    return result


def partial_trace(matrix, dims, keep):
    """Partial trace with big-endian product indexing."""
    from itertools import product

    keep = tuple(keep)
    traced = tuple(i for i in range(len(dims)) if i not in keep)
    kept_indices = list(product(*(range(dims[i]) for i in keep)))
    traced_indices = list(product(*(range(dims[i]) for i in traced)))

    def index(coordinates):
        result = 0
        for coordinate, dimension in zip(coordinates, dims):
            result = result * dimension + coordinate
        return result

    result = s.zeros(len(kept_indices))
    for row, left in enumerate(kept_indices):
        for col, right in enumerate(kept_indices):
            for common in traced_indices:
                x = [0] * len(dims)
                y = [0] * len(dims)
                for i, a, b in zip(keep, left, right):
                    x[i], y[i] = a, b
                for i, a in zip(traced, common):
                    x[i] = y[i] = a
                result[row, col] += matrix[index(x), index(y)]
    return result


def permutation_matrix(dimension, order):
    from itertools import product

    result = s.zeros(dimension ** len(order))
    for coordinates in product(range(dimension), repeat=len(order)):
        before = 0
        after = 0
        for x in coordinates:
            before = before * dimension + x
        for i in order:
            after = after * dimension + coordinates[i]
        result[after, before] = 1
    return result


def main():
    X = s.Matrix([[0, 1], [1, 0]])
    Yp = s.Matrix([[0, -s.I], [s.I, 0]])
    Z = s.diag(1, -1)
    pauli = (X, Yp, Z)
    I2, I3 = s.eye(2), s.eye(3)
    P = s.diag(1, 1, 0)
    D = s.diag(0, 0, 1)
    A = tuple(s.diag(a, s.zeros(1)) for a in pauli)
    L = sum((a * a for a in A), s.zeros(3))
    dual_Y = 2 * P
    assert L == 3 * P

    # All entries of each density operator are rational.  The square root
    # appears only in this convenient normalized vector representation.
    vectors = []
    for pair in ((0, 1), (0, 2), (1, 2)):
        vector = s.zeros(27, 1)
        for k in (0, 1):
            coordinates = [2, 2, 2]
            coordinates[pair[0]] = coordinates[pair[1]] = k
            index = 9 * coordinates[0] + 3 * coordinates[1] + coordinates[2]
            vector[index] = 1 / s.sqrt(2)
        vectors.append(vector)
    pure = tuple(v * v.H for v in vectors)
    R = sum(pure, s.zeros(27)) / 3
    assert s.trace(R) == 1
    for register in range(3):
        assert partial_trace(R, (3, 3, 3), (register,)) == I3 / 3
    swap_BC = permutation_matrix(3, (0, 2, 1))
    assert swap_BC * R * swap_BC == R

    J = partial_trace(R, (3, 3, 3), (0, 1))
    omega = s.zeros(9, 1)
    omega[0] = omega[4] = 1 / s.sqrt(2)
    asserted_J = omega * omega.H / 3 + (kron(P, D) + kron(D, P)) / 6
    assert J == asserted_J

    def phi(matrix):
        return (P * matrix * P + s.trace(P * matrix) * D + matrix[2, 2] * P) / 2

    assert phi(I3) == I3
    units = []
    for row in range(3):
        for col in range(3):
            matrix = s.zeros(3)
            matrix[row, col] = 1
            units.append(matrix)
    for matrix in units:
        assert s.trace(phi(matrix)) == s.trace(matrix)
        choi_output = 3 * partial_trace(kron(matrix.T, I3) * J, (3, 3), (1,))
        assert choi_output == phi(matrix)
    for left in units:
        for right in units:
            assert s.trace(left.H * phi(right)) == s.trace(phi(left).H * right)
    for a in A:
        assert phi(a) == a / 2

    W = sum((kron(a.T, a, I3) + kron(a.T, I3, a) for a in A), s.zeros(27))
    H = kron(L.T, I3, I3) + (kron(I3, L, I3) + kron(I3, I3, L)) / 2 - W
    V = s.trace(L) / 3
    score = sum(s.trace(a * phi(a)) / 3 for a in A)
    energy = s.trace(R * H)
    variance = s.trace(dual_Y) / 3
    assert (V, score, energy, variance) == (2, 1, 2, s.Rational(4, 3))
    bad_operator = H - kron(dual_Y.T, I3, I3)
    witness = s.trace(pure[0] * bad_operator)
    assert witness == -s.Rational(1, 2)
    assert s.trace(R * bad_operator) == s.Rational(2, 3)

    rho_BC = partial_trace(R, (3, 3, 3), (1, 2))
    asserted_BC = omega * omega.H / 3 + (kron(P, D) + kron(D, P)) / 6
    assert rho_BC == asserted_BC
    M = tuple((kron(a, I3) + kron(I3, a)) / 2 for a in A)
    M2 = sum((m * m for m in M), s.zeros(9))
    active_EPR_second_moment = (omega.H * M2 * omega)[0]
    assert active_EPR_second_moment == 2
    sector_tracial_minimum = s.Rational(9, 4)
    trace_cost_lower_bound = (2 * sector_tracial_minimum + active_EPR_second_moment) / 3
    assert trace_cost_lower_bound == s.Rational(13, 6) > V

    # Constant-L, scalar-dual-Y refinement: five 4x4 Clifford generators.
    gamma = (kron(X, I2), kron(Z, I2), kron(Yp, X), kron(Yp, Z), kron(Yp, Yp))
    I4 = s.eye(4)
    for i, g in enumerate(gamma):
        assert g.H == g and g * g == I4 and s.trace(g) == 0
        for h in gamma[i + 1 :]:
            assert g * h + h * g == s.zeros(4)
    average_gamma = tuple((kron(g, I4) + kron(I4, g)) / 2 for g in gamma)
    average_tracial_square_sum = sum(s.trace(m * m) / 16 for m in average_gamma)
    assert average_tracial_square_sum == s.Rational(5, 2)
    constant_L_cost_lower_bound = average_tracial_square_sum ** 2
    assert constant_L_cost_lower_bound == s.Rational(25, 4) > 5

    # Independently derived reverse-allocation failure, preserved without
    # any scan or replay of the coordinator's separate spin1 candidate.
    pauli_average = tuple((kron(g, I2) + kron(I2, g)) / 2 for g in pauli)
    L_composite = sum((m * m for m in pauli_average), s.zeros(4))
    A_reverse = tuple(s.diag(g, m) for g, m in zip(pauli, pauli_average))
    Y_reverse = s.diag(2 * I2, s.zeros(4))
    L_reverse = sum((a * a for a in A_reverse), s.zeros(6))
    G_reverse = L_reverse - Y_reverse
    assert L_reverse == s.diag(3 * I2, L_composite)
    assert G_reverse == s.diag(I2, L_composite)
    epr_composite = s.zeros(16, 1)
    for i in range(4):
        epr_composite[4 * i + i] = s.Rational(1, 2)
    reverse_W = sum((2 * kron(m.T, m) for m in pauli_average), s.zeros(16))
    reverse_restriction = kron(L_composite.T, I4) + s.eye(16) - reverse_W
    reverse_witness = (epr_composite.H * reverse_restriction * epr_composite)[0]
    assert reverse_witness == -s.Rational(1, 2)

    result = {
        "status": "exact_matrix_identities_verified",
        "solver": None,
        "arithmetic": "SymPy exact rational and imaginary units",
        "d3": {
            "marginals": "I3/3",
            "BC_swap": True,
            "Phi_unital_TP_HS_self_adjoint": True,
            "Phi_Pauli_eigenvalue": "1/2",
            "V": str(V),
            "s": str(score),
            "k_exact_analytic_proof_in_report": "2/3",
            "v": str(variance),
            "Tr_R_H": str(energy),
            "operator_witness_H_minus_YA": str(witness),
            "legal_expectation_H_minus_YA": "2/3",
            "unbiased_moment_cost_lower_bound_analytic_proof_in_report": str(trace_cost_lower_bound),
            "available_second_moment_budget": str(V),
        },
        "constant_L_scalar_Y": {
            "dimension": 4,
            "frame_rank": 5,
            "L": "5 I4",
            "dual_Y": "4 I4",
            "legal_R": "(I4/4) tensor (I4/4) tensor (I4/4)",
            "unbiased_moment_cost_lower_bound_analytic_proof_in_report": str(constant_L_cost_lower_bound),
            "available_second_moment_budget": "5",
        },
        "independent_reverse_allocation_failure": {
            "dimension": 6,
            "frame": "Pauli_i direct-sum ((Pauli_i tensor I + I tensor Pauli_i)/2)",
            "dual_Y": "2I2 direct-sum 0_4",
            "D_rev_witness": str(reverse_witness),
            "legal_tracial_witness": False,
            "coordinator_spin1_candidate": "separately source-reported, not replayed here",
        },
        "limits": [
            "POVM lower bounds require the analytic arguments in PROOF.txt",
            "No general gate proof or counterexample is claimed",
            "No external validation or novelty claim is made",
        ],
    }
    print(json.dumps(result, indent=2))
    destination = Path(__file__).with_name("replay_results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
