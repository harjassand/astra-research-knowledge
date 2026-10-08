#!/usr/bin/env python3
"""Arithmetic for a conservative generic Givens/Naimark readout bound.

This is cost accounting, not an optimized gate compiler.  It assumes a
16-column isometry into M=2**b label states; arbitrary U(2) Givens gates are
implemented with Gray-code CNOT conjugations, a multi-control decomposition
using clean Toffoli ancillas, and at most ten arbitrary one-qubit rotations.
Each exact Toffoli is charged as 6 CNOT + 7 T.  A final 16 computational-state
phase corrections are separately charged.  The isometry formula and exact
frame checks live in cycle10_finite_compiler/.
"""

from math import ceil, log2
from pathlib import Path
import json


def costs(label_bits: int, d: int = 16, phase_corrections: int = 16):
    M = 1 << label_bits
    givens = d * (M - 1) - d * (d - 1) // 2
    cnot_per_givens = 14 * label_bits - 24
    toffoli_per_givens = 2 * (label_bits - 2)
    cnot_per_phase = 12 * (label_bits - 1)
    toffoli_per_phase = 2 * (label_bits - 1)
    arbitrary_rotations = 10 * givens + phase_corrections
    toffolis = givens * toffoli_per_givens + phase_corrections * toffoli_per_phase
    cnots = givens * cnot_per_givens + phase_corrections * cnot_per_phase
    assert cnots == (toffolis * 6 + givens * 2 + phase_corrections * 0 +
                     givens * 2 * (label_bits - 1))
    return {
        "label_bits": label_bits,
        "padded_outcomes": M,
        "givens_upper_bound": givens,
        "phase_corrections": phase_corrections,
        "cnot_upper_bound": cnots,
        "toffoli_upper_bound": toffolis,
        "t_from_exact_toffolis_only": 7 * toffolis,
        "arbitrary_one_qubit_rotations": arbitrary_rotations,
        "clean_workspace_qubits": label_bits - 1,
    }


def accuracy_bits(rotation_count: int, epsilon: float = 1e-3):
    """If each rotation has operator error <=2^-p, bound product error by eps."""
    return ceil(log2(rotation_count / epsilon))


def main():
    rows = {name: costs(bits) for name, bits in (("v_H", 11), ("v_V", 10), ("v_R", 8))}
    expected = {
        "v_H": (32632, 4244080, 587696, 4113872, 326336, 10),
        "v_V": (16248, 1886496, 260256, 1821792, 162496, 9),
        "v_R": (3960, 349824, 47744, 334208, 39616, 7),
    }
    for name, row in rows.items():
        got = (row["givens_upper_bound"], row["cnot_upper_bound"],
               row["toffoli_upper_bound"], row["t_from_exact_toffolis_only"],
               row["arbitrary_one_qubit_rotations"], row["clean_workspace_qubits"])
        assert got == expected[name], (name, got, expected[name])
        row["operator_error_budget"] = "epsilon=1e-3 total; each arbitrary rotation <= epsilon/count"
        row["binary_accuracy_bits_at_epsilon_1e-3"] = accuracy_bits(
            row["arbitrary_one_qubit_rotations"])
    assert [rows[x]["binary_accuracy_bits_at_epsilon_1e-3"]
            for x in ("v_H", "v_V", "v_R")] == [29, 28, 26]
    result = {
        "status": "PASS_ARITHMETIC_ONLY",
        "scope": "generic Naimark/Givens upper-bound arithmetic; not an optimized or emitted readout circuit",
        "assumptions": [
            "d=16 input isometry columns, padded label dimension M=2^b",
            "G=d(M-1)-d(d-1)/2 two-level U(2) operations suffice, plus d phase corrections",
            "each two-level U(2) on b wires costs at most 14b-24 CNOTs and 2(b-2) Toffolis",
            "each residual basis-state phase costs 12(b-1) CNOTs and 2(b-1) Toffolis",
            "each Toffoli is charged as 6 CNOT and 7 T; arbitrary rotations are not T-synthesized",
            "operator product error is bounded by the sum of individual rotation errors"
        ],
        "rows": rows,
    }
    target = Path(__file__).with_name("NAIMARK_UPPER_BOUND.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
