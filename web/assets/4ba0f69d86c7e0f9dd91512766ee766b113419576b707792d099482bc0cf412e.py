#!/usr/bin/env python3
"""Exact low-dimensional checks for the MUB/Bell collective-CMI witness.

Fraction arithmetic checks the d=2 quantum realization and d=2,3,4,8
conditional classical probability laws. The all-d entropy limits are proved
analytically in approx_markov_collective_correlation.txt.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction as F


def fs(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def zero_matrix(n: int) -> list[list[F]]:
    return [[F(0) for _ in range(n)] for _ in range(n)]


def add(A: list[list[F]], B: list[list[F]]) -> list[list[F]]:
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]


def scale(a: F, A: list[list[F]]) -> list[list[F]]:
    return [[a * A[i][j] for j in range(len(A))] for i in range(len(A))]


def trace_product(A: list[list[F]], B: list[list[F]]) -> F:
    n = len(A)
    return sum(A[i][j] * B[j][i] for i in range(n) for j in range(n))


def matmul(A: list[list[F]], B: list[list[F]]) -> list[list[F]]:
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m))
             for j in range(p)] for i in range(n)]


def bell_projector_d2(b: int, j: int) -> list[list[F]]:
    # Bell ket (|0,b> + (-1)^j |1,1+b mod 2>)/sqrt(2).
    signs = [0, 0, 0, 0]
    signs[0 * 2 + b] = 1
    signs[1 * 2 + ((1 + b) % 2)] = -1 if j else 1
    return [[F(signs[u] * signs[v], 2) for v in range(4)] for u in range(4)]


def partial_trace_d2(P: list[list[F]], keep: str) -> list[list[F]]:
    out = zero_matrix(2)
    if keep == "B":
        # trace C: output indices are (b,b')
        for b in range(2):
            for bp in range(2):
                out[b][bp] = sum(P[2 * b + c][2 * bp + c] for c in range(2))
    else:
        # trace B: output indices are (c,c')
        for c in range(2):
            for cp in range(2):
                out[c][cp] = sum(P[2 * b + c][2 * b + cp] for b in range(2))
    return out


def check_probability_law(d: int, eps: F) -> dict:
    q = eps + (1 - eps) / d
    pxy: dict[tuple[int, int, int, int], F] = {}
    for b in range(2):
        for j in range(d):
            for bp in range(2):
                for k in range(d):
                    if bp == b:
                        value = (1 - eps) / (2 * d) + (eps / 2 if k == j else 0)
                    else:
                        value = F(1, 2 * d)
                    pxy[(b, j, bp, k)] = value
            assert sum(pxy[(b, j, bp, k)] for bp in range(2) for k in range(d)) == 1

    # The uniform prior on 2d labels makes every measurement outcome uniform.
    for bp in range(2):
        for k in range(d):
            assert sum(pxy[(b, j, bp, k)] for b in range(2) for j in range(d)) / (2 * d) == F(1, 2 * d)

    same_spike = pxy[(0, 0, 0, 0)]
    same_other = pxy[(0, 0, 0, 1 % d)] if d > 1 else F(0)
    cross = pxy[(0, 0, 1, 0)]
    assert same_spike == q / 2
    assert same_other == (1 - eps) / (2 * d)
    assert cross == F(1, 2 * d)
    return {
        "d": d,
        "epsilon": fs(eps),
        "special_same_basis_outcome": fs(same_spike),
        "other_same_basis_outcome": fs(same_other),
        "cross_basis_outcome": fs(cross),
        "uniform_output_probability": fs(F(1, 2 * d)),
        "input_holevo_exact": "C_d",
        "joint_output_accessible_information_exact": "C_d/2",
        "checks": "PASS (all conditional probabilities exact over Fraction)",
    }


def check_d2_quantum_realization() -> dict:
    d, eps = 2, F(1, 2)
    I2 = [[F(1), F(0)], [F(0), F(1)]]
    P = [
        [[F(1), F(0)], [F(0), F(0)]],
        [[F(0), F(0)], [F(0), F(1)]],
        [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]],
        [[F(1, 2), F(-1, 2)], [F(-1, 2), F(1, 2)]],
    ]
    labels = [(b, j) for b in range(2) for j in range(2)]
    effects = [scale(F(1, 2), proj) for proj in P]
    total = zero_matrix(2)
    for effect in effects:
        total = add(total, effect)
    assert total == I2

    # The two bases really do contain noncommuting projectors.
    pzp = matmul(P[0], P[2])
    pxz = matmul(P[2], P[0])
    assert pzp != pxz

    rho = [add(scale(1 - eps, scale(F(1, 2), I2)), scale(eps, proj)) for proj in P]
    for state in rho:
        delta00 = state[0][0] - F(1, 2)
        delta01 = state[0][1]
        # A traceless Hermitian 2x2 difference has eigenvalues +/-sqrt(...).
        assert delta00**2 + delta01**2 == F(1, 16)
    probabilities = [[trace_product(effects[y], rho[x]) for y in range(4)]
                     for x in range(4)]
    assert probabilities == [
        [F(3, 8), F(1, 8), F(1, 4), F(1, 4)],
        [F(1, 8), F(3, 8), F(1, 4), F(1, 4)],
        [F(1, 4), F(1, 4), F(3, 8), F(1, 8)],
        [F(1, 4), F(1, 4), F(1, 8), F(3, 8)],
    ]

    bells = [bell_projector_d2(b, j) for b, j in labels]
    for y in range(4):
        for z in range(4):
            # Each projector is rank one; Bell ket inner products square to delta.
            inner = sum(bells[y][u][v] * bells[z][v][u]
                        for u in range(4) for v in range(4))
            assert inner == (1 if y == z else 0)
        assert partial_trace_d2(bells[y], "B") == scale(F(1, 2), I2)
        assert partial_trace_d2(bells[y], "C") == scale(F(1, 2), I2)

    output_states = []
    tau = scale(F(1, 2), I2)
    for x in range(4):
        omega = zero_matrix(4)
        for y in range(4):
            omega = add(omega, scale(probabilities[x][y], bells[y]))
        output_states.append(omega)
        assert partial_trace_d2(omega, "B") == tau
        assert partial_trace_d2(omega, "C") == tau
        assert sum(omega[u][u] for u in range(4)) == 1

    average = zero_matrix(4)
    for omega in output_states:
        average = add(average, scale(F(1, 4), omega))
    maximally_mixed_4 = scale(F(1, 4), [[F(int(i == j)) for j in range(4)] for i in range(4)])
    assert average == maximally_mixed_4

    trace_error = F(1, 4)
    return {
        "dimension": 2,
        "epsilon": fs(eps),
        "POVM_effects_sum_to_identity": True,
        "input_family_contains_noncommuting_states": True,
        "four_Bell_preparations_orthonormal_and_maximally_entangled": True,
        "all_conditional_receiver_marginals": "I/2",
        "all_receiver_marginals_for_every_input": "Tr(Z) I/2",
        "input_state_eigenvalues": ["3/4", "1/4"],
        "broadcast_and_replacement_EB_error": fs(trace_error),
        "conditional_measurement_row_for_X0": [fs(v) for v in probabilities[0]],
        "chi_input_exact": "ln(2) - H(3/4,1/4)",
        "I_X_BC_exact": "(ln(2) - H(3/4,1/4))/2",
        "I_X_C_exact": "0",
        "recovery_trace_distance_lower_exact": "sqrt((ln(2)-H(3/4,1/4))/4)",
        "checks": "PASS (all matrix/probability checks exact over Fraction)",
    }


def main() -> None:
    fixtures = [check_probability_law(2, F(1, 2)),
                check_probability_law(3, F(1, 3)),
                check_probability_law(4, F(1, 4)),
                check_probability_law(8, F(1, 8))]
    c = 0.5
    asymptotic = []
    for d in (16, 256, 4096, 10**12, 10**100):
        eps = c / math.log(d)
        q = eps + (1 - eps) / d
        capacity = q * math.log(d * q) + (1 - q) * math.log(1 - eps)
        asymptotic.append({
            "d": str(d),
            "c_target_nats": c,
            "epsilon_c_over_log_d": eps,
            "capacity_numeric": capacity,
            "broadcast_error_upper_numeric": eps * (1 - 1 / d),
            "CMI_numeric": capacity / 2,
            "status": "numeric illustration; asymptotic limits are analytic in report",
        })

    print(json.dumps({"exact_d2_quantum_realization": check_d2_quantum_realization(),
                      "exact_probability_fixtures": fixtures,
                      "asymptotic_numeric_illustration": asymptotic}, indent=2))


if __name__ == "__main__":
    main()
