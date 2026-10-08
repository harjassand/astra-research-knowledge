#!/usr/bin/env python3
"""Exact audit of a FALSE sufficient tensor-certificate inequality.

Python standard library only. All arithmetic uses fractions.Fraction.
This proves a failure of a proposed co-Choi domination certificate, NOT a
counterexample to Werner undistillability and NOT NPT bound entanglement.

Run:
    python verify_exact_schur_certificate_failure.py
    python -O verify_exact_schur_certificate_failure.py --output receipt.json
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
from typing import Callable

Matrix = list[list[Q]]


def zeros(rows: int, cols: int) -> Matrix:
    return [[Q(0) for _ in range(cols)] for _ in range(rows)]


def eye(n: int) -> Matrix:
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    if len(a[0]) != len(b):
        raise ValueError("Incompatible matrix dimensions")
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a: Matrix, b: Matrix, scale_b: Q = Q(1)) -> Matrix:
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("Incompatible matrix dimensions")
    return [[a[i][j] + scale_b * b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def outer(a: list[Q], b: list[Q]) -> Matrix:
    return [[x * y for y in b] for x in a]


def reduce_two_qubits(c: Matrix) -> Matrix:
    """Phi = (Tr(.) I_2 - id/2) tensor (Tr(.) I_2 - id/2)."""
    if len(c) != 4 or any(len(row) != 4 for row in c):
        raise ValueError("Expected a 4-by-4 matrix")
    out = zeros(4, 4)
    tr = sum((c[a][a] for a in range(4)), Q(0))
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    value = c[2*i+j][2*k+l] / 4
                    if i == k:
                        value -= sum((c[2*a+j][2*a+l] for a in range(2)), Q(0)) / 2
                    if j == l:
                        value -= sum((c[2*i+a][2*k+a] for a in range(2)), Q(0)) / 2
                    if i == k and j == l:
                        value += tr
                    out[2*i+j][2*k+l] = value
    return out


def cochoi(phi: Callable[[Matrix], Matrix], n: int) -> Matrix:
    """Input-first convention: J_hat(phi) = sum E_ab tensor phi(E_ba)."""
    out = zeros(n*n, n*n)
    for a in range(n):
        for b in range(n):
            e = zeros(n, n)
            e[b][a] = Q(1)
            block = phi(e)
            for i in range(n):
                for j in range(n):
                    out[n*a+i][n*b+j] = block[i][j]
    return out


def require_equal(actual: object, expected: object, name: str) -> None:
    # Deliberately not an assert: verification also runs under python -O.
    if actual != expected:
        raise ArithmeticError(f"Exact verification failed: {name}")


def quadratic(v: list[Q], a: Matrix) -> Q:
    return sum((v[i] * a[i][j] * v[j]
                for i in range(len(v)) for j in range(len(v))), Q(0))


def verify() -> dict[str, object]:
    u = list(map(Q, [1, 0, 0, 1]))
    uu = outer(u, u)
    a = reduce_two_qubits(uu)
    a_inverse = add(eye(4), uu, Q(-1, 6))
    require_equal(a, add(eye(4), uu, Q(1, 4)), "A = I + uu*/4")
    require_equal(matmul(a, a_inverse), eye(4), "A A_inverse = I")
    require_equal(matmul(a_inverse, a), eye(4), "A_inverse A = I")

    ell = [reduce_two_qubits(outer(eye(4)[j], u)) for j in range(4)]
    r = cochoi(reduce_two_qubits, 4)
    s = zeros(16, 16)
    for i in range(4):
        for j in range(4):
            # M(E_ji) = ell_j A_inverse ell_i*.
            block = matmul(matmul(ell[j], a_inverse), transpose(ell[i]))
            for k in range(4):
                for l in range(4):
                    s[4*i+k][4*j+l] = block[k][l]
    require_equal(r, transpose(r), "R is symmetric")
    require_equal(s, transpose(s), "S is symmetric")

    v = list(map(Q, [3, 0, 0, 1, 0, 0, 2, 0, 0, 2, 0, 0, 1, 0, 0, 3]))
    vcol = [[x] for x in v]
    rv, sv = matmul(r, vcol), matmul(s, vcol)
    require_equal(sv, [[Q(-11, 9) * x[0]] for x in rv], "S v = -11 R v / 9")
    qr, qs = quadratic(v, r), quadratic(v, s)
    require_equal(qr, Q(9), "v* R v = 9")
    require_equal(qs, Q(-11), "v* S v = -11")
    require_equal(quadratic(v, add(r, s)), Q(-2), "v* (R+S) v = -2")

    # Under the canonical tensor-factor permutation, the four-site co-Choi
    # matrices are R tensor R and S tensor S. The displayed tensor vector
    # has expectation qr^2 - qs^2; no floating eigensolver is involved.
    tensor_value = qr*qr - qs*qs
    require_equal(tensor_value, Q(-40), "tensor-square expectation = -40")
    norm_squared = sum((x*x for x in v), Q(0))
    require_equal(norm_squared, Q(28), "||v||^2 = 28")
    require_equal(tensor_value / (norm_squared**2), Q(-5, 98),
                  "normalized tensor expectation = -5/98")

    return {
        "status": "EXACT_METHOD_CERTIFICATE_COUNTEREXAMPLE_PASS",
        "foundational_target_resolved": False,
        "arithmetic": "Python standard-library fractions.Fraction; no tolerances",
        "reference_u": [int(x) for x in u],
        "witness_v": [int(x) for x in v],
        "v_R_v": str(qr),
        "v_S_v": str(qs),
        "v_R_plus_S_v": "-2",
        "tensor_square_expectation": str(tensor_value),
        "normalized_tensor_square_expectation": "-5/98",
        "scope": "Failure of an entangled-reference co-Choi domination certificate only",
        "not_claimed": ["NPT bound entanglement", "Werner distillability counterexample",
                        "all-copy undistillability", "historical novelty", "formal proof assistant verification"]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional path for an exact JSON receipt")
    args = parser.parse_args()
    result = verify()
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
