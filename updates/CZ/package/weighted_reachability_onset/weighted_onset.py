#!/usr/bin/env python3
"""Exact weighted row-completion algorithm, requiring SymPy.

Run built-in examples: python3 weighted_onset.py
Run supplied matrices: python3 weighted_onset.py generator.json

JSON schema: {"H": square_matrix, "jumps": [square_matrix, ...]}.
Entries are rational strings/integers, or {"re": rational, "im": rational}.
The algorithm is polynomial in dense matrix dimension, not qubit count.
"""
from __future__ import annotations

import json
import sys
import sympy as s


def scalar(value):
    if isinstance(value, dict) and set(value) <= {"re", "im"}:
        return scalar(value.get("re", 0)) + s.I * scalar(value.get("im", 0))
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("Entries must be exact rationals or Gaussian rationals")
    return s.Rational(value)


def read_matrix(rows):
    return s.Matrix([[scalar(v) for v in row] for row in rows])


def vec(matrix):
    return s.Matrix(list(matrix))


def basis(matrices, d):
    columns = s.Matrix.hstack(*(vec(x) for x in matrices))
    return [s.Matrix(d, d, list(v)) for v in columns.columnspace()]


def row_core(matrices, d):
    perpendicular = s.Matrix.hstack(*(vec(x) for x in matrices)).H.nullspace()
    constraints = []
    for q in perpendicular:
        matrix = s.Matrix(d, d, list(q))
        for col in range(d):
            constraints.append([s.conjugate(matrix[row, col]) for row in range(d)])
    linear = s.Matrix(constraints) if constraints else s.zeros(0, d)
    return linear.nullspace()


def onset(hamiltonian, jumps):
    d = hamiltonian.rows
    if d < 1 or hamiltonian.cols != d or hamiltonian != hamiltonian.H:
        raise ValueError("H must be a nonempty Hermitian square matrix")
    if any(j.shape != (d, d) for j in jumps):
        raise ValueError("All jumps must have the same square shape as H")
    g = -s.I * hamiltonian - sum((j.H * j for j in jumps), s.zeros(d)) / 2
    spaces = [[s.eye(d)]]
    history = []
    cutoff = max(0, 2 * d * d - 3)
    for grade in range(cutoff + 1):
        if grade:
            candidates = list(spaces[-1])
            candidates += [j * x for j in jumps for x in spaces[-1]]
            if grade >= 2:
                candidates += [g * x - x * g for x in spaces[-2]]
            spaces.append(basis(candidates, d))
        core = row_core(spaces[-1], d)
        history.append({"grade": grade, "dimension": len(spaces[-1]),
                        "row_core_dimension": len(core)})
        if core:
            return {"dimension": d, "onset_exponent": grade,
                    "row_core_basis": [[str(v) for v in b] for b in core],
                    "filtration": history}
        if grade >= 2 and len(spaces[-1]) == len(spaces[-2]) == len(spaces[-3]):
            break
    return {"dimension": d, "onset_exponent": None,
            "meaning": "beta and positive CP-replacer coefficient vanish for all t>0",
            "filtration": history}


def examples():
    x = s.Matrix([[0, 1], [1, 0]])
    z = s.diag(1, -1)
    lower = s.Matrix([[0, 1], [0, 0]])
    shift = s.zeros(4)
    for i in range(1, 4):
        shift[i - 1, i] = 1
    p0 = s.diag(1, 0, 0, 0)
    cases = {
        "driven_amplitude_damping": (x / 2, [lower], 3),
        "driven_dephasing": (x / 2, [z], 4),
        "undriven_amplitude_damping": (s.zeros(2), [lower], None),
        "two_pauli_jumps": (s.zeros(2), [x, z], 2),
        "four_level_absorbing_chain": (s.zeros(4), [shift, p0], 3),
    }
    result = {}
    for name, (h, js, expected) in cases.items():
        result[name] = onset(h, js)
        assert result[name]["onset_exponent"] == expected, name
    return result


if __name__ == "__main__":
    if len(sys.argv) == 1:
        answer = examples()
    elif len(sys.argv) == 2:
        with open(sys.argv[1], encoding="utf-8") as source:
            data = json.load(source)
        answer = onset(read_matrix(data["H"]), [read_matrix(j) for j in data["jumps"]])
    else:
        raise SystemExit("Usage: weighted_onset.py [generator.json]")
    print(json.dumps(answer, indent=2))
