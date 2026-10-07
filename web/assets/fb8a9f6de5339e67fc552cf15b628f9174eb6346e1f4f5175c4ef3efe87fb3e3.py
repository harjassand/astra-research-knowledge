#!/usr/bin/env python3
"""Exact qutrit realization of the sharp c=2 broadcasting calibration.

All arithmetic is symbolic in Q(exp(2*pi*i/3)); no floating point or SDP
solver is used. The script verifies a 12-outcome complete-MUB measurement,
its EB channel, the symmetric universal-cloner channel, and exact equality
I-Psi = 2(I-Phi) on the full 9-dimensional operator space.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import sympy as sp


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def partial_trace_second(matrix: sp.MatrixBase, d: int) -> sp.Matrix:
    return sp.Matrix(d, d, lambda i, k: sum(matrix[i * d + j, k * d + j] for j in range(d)))


def partial_trace_first(matrix: sp.MatrixBase, d: int) -> sp.Matrix:
    return sp.Matrix(d, d, lambda j, ell: sum(matrix[i * d + j, i * d + ell] for i in range(d)))


def main() -> None:
    started = time.perf_counter()
    d = 3
    eye = sp.eye(d)
    omega = (-1 + sp.I * sp.sqrt(3)) / 2

    # Wootters--Fields prime-dimensional vectors: the computational basis
    # and the three quadratic-phase bases |a,k>_j = omega^(a*j^2+k*j)/sqrt(3).
    bases: list[list[sp.Matrix]] = [[sp.eye(d)[:, j] for j in range(d)]]
    root_d = sp.sqrt(d)
    for a in range(d):
        bases.append([
            sp.Matrix([omega ** (a * j * j + k * j) for j in range(d)]) / root_d
            for k in range(d)
        ])

    for basis in bases:
        unitary = sp.Matrix.hstack(*basis)
        assert zero_matrix(unitary.conjugate().T * unitary - eye)

    for left in range(d + 1):
        for right in range(left + 1, d + 1):
            for v in bases[left]:
                for w in bases[right]:
                    overlap = (v.conjugate().T * w)[0]
                    assert sp.simplify(overlap * sp.conjugate(overlap) - sp.Rational(1, d)) == 0

    projectors = [v * v.conjugate().T for basis in bases for v in basis]
    assert len(projectors) == d * (d + 1)
    assert zero_matrix(sum(projectors, sp.zeros(d)) - (d + 1) * eye)

    def psi(matrix: sp.MatrixBase) -> sp.Matrix:
        return sum((sp.trace(p * matrix) * p for p in projectors), sp.zeros(d)) / (d + 1)

    matrix_units = [sp.eye(d)[:, i] * sp.eye(d)[j, :] for i in range(d) for j in range(d)]
    for unit in matrix_units:
        expected = (unit + sp.trace(unit) * eye) / (d + 1)
        assert zero_matrix(psi(unit) - expected)

    swap = sp.zeros(d * d)
    for i in range(d):
        for j in range(d):
            swap[i * d + j, j * d + i] = 1
    symmetric_projector = (sp.eye(d * d) + swap) / 2
    assert zero_matrix(symmetric_projector * symmetric_projector - symmetric_projector)

    # K_a = sqrt(2/(d+1)) P_sym (I tensor |a>) are exact Kraus matrices for
    # C(A) = 2/(d+1) P_sym (A tensor I) P_sym.
    kraus = []
    for a in range(d):
        embedding = sp.zeros(d * d, d)
        for i in range(d):
            embedding[i * d + a, i] = 1
        kraus.append(sp.sqrt(sp.Rational(2, d + 1)) * symmetric_projector * embedding)
    assert zero_matrix(sum((k.conjugate().T * k for k in kraus), sp.zeros(d)) - eye)

    def cloner_marginal(matrix: sp.MatrixBase) -> sp.Matrix:
        output = sum((k * matrix * k.conjugate().T for k in kraus), sp.zeros(d * d))
        return partial_trace_second(output, d)

    def phi(matrix: sp.MatrixBase) -> sp.Matrix:
        return ((d + 2) * matrix + sp.trace(matrix) * eye) / (2 * (d + 1))

    def phi_from_superoperator(matrix: sp.MatrixBase) -> sp.Matrix:
        return cloner_marginal(matrix)

    for unit in matrix_units:
        assert zero_matrix(phi_from_superoperator(unit) - phi(unit))
        output = sum((k * unit * k.conjugate().T for k in kraus), sp.zeros(d * d))
        assert zero_matrix(partial_trace_first(output, d) - phi(unit))
        assert zero_matrix(swap * output * swap - output)
        assert zero_matrix((unit - psi(unit)) - 2 * (unit - phi(unit)))

    result = {
        "status": "PASS_EXACT_SYMBOLIC",
        "dimension": d,
        "coefficient_field": "Q(exp(2*pi*i/3))",
        "measurement_outcomes": len(projectors),
        "checks": {
            "four_orthonormal_bases": True,
            "pairwise_mutual_unbiasedness": True,
            "complete_MUB_projectors_sum_to_4I": True,
            "Psi(A)=(A+Tr(A)I)/4_on_all_matrix_units": True,
            "cloner_Kraus_completeness": True,
            "both_clone_marginals_equal_Phi": True,
            "clone_output_is_swap_symmetric": True,
            "I_minus_Psi_equals_2_times_I_minus_Phi": True,
        },
        "maps": {
            "Phi(A)": "(5 A + Tr(A) I)/8",
            "Psi(A)": "(A + Tr(A) I)/4",
            "traceless_eigenvalues": {"Phi": "5/8", "Psi": "1/4"},
            "Dirichlet_ratio": "2 exactly",
        },
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "limitations": [
            "This is a sharp calibration/example, not a proof of universal EB Dirichlet rounding.",
            "The exact finite qutrit construction does not establish an efficient general-dimensional compiler.",
        ],
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
