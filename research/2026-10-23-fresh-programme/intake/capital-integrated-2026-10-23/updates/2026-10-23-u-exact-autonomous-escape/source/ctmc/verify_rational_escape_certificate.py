#!/usr/bin/env python3
"""Independent exact checker for a rational balanced-CTMC returned-bit certificate.

All matrix/scalar data must be JSON integers or rational strings. No floating
point tolerance is used. This script checks the CTMC constraints, flat-sign
column, exact rank, exact intertwining, and the exact four-frequency identity
(K^2 + I)(K^2 + 9 I) = 0. The last identity implies exp(pi K) = -I.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

DEFAULT_CERT = (
    Path(__file__).resolve().parents[1]
    / "interface_invention"
    / "AUTONOMOUS_ESCAPE_RATIONAL_CERTIFICATE.json"
)


def rational(value: Any, where: str) -> Fraction:
    if isinstance(value, bool):
        raise ValueError(f"{where}: booleans are not rational entries")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"{where}: invalid rational string {value!r}") from exc
    raise ValueError(
        f"{where}: expected an integer or rational string, got {type(value).__name__}"
    )


def matrix(value: Any, name: str) -> list[list[Fraction]]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{name}: expected a nonempty list of rows")
    if any(not isinstance(row, list) for row in value):
        raise ValueError(f"{name}: every row must be a list")
    width = len(value[0])
    if width == 0 or any(len(row) != width for row in value):
        raise ValueError(f"{name}: matrix is empty or ragged")
    return [
        [rational(entry, f"{name}[{i}][{j}]") for j, entry in enumerate(row)]
        for i, row in enumerate(value)
    ]


def shape(a: Sequence[Sequence[Fraction]]) -> tuple[int, int]:
    return len(a), len(a[0])


def matmul(
    a: Sequence[Sequence[Fraction]], b: Sequence[Sequence[Fraction]]
) -> list[list[Fraction]]:
    ar, ac = shape(a)
    br, bc = shape(b)
    if ac != br:
        raise ValueError(f"matrix multiply shape mismatch {(ar, ac)} x {(br, bc)}")
    out = [[Fraction(0) for _ in range(bc)] for _ in range(ar)]
    for i in range(ar):
        for k in range(ac):
            aik = a[i][k]
            if aik:
                for j in range(bc):
                    if b[k][j]:
                        out[i][j] += aik * b[k][j]
    return out


def exact_rank(a: Sequence[Sequence[Fraction]]) -> int:
    rows = [list(row) for row in a]
    nr, nc = shape(rows)
    pivot_row = 0
    for col in range(nc):
        pivot = next((r for r in range(pivot_row, nr) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][col]
        for r in range(pivot_row + 1, nr):
            if rows[r][col]:
                factor = rows[r][col] / pivot_value
                for c in range(col, nc):
                    rows[r][c] -= factor * rows[pivot_row][c]
        pivot_row += 1
        if pivot_row == nr:
            break
    return pivot_row


def max_abs(a: Sequence[Sequence[Fraction]]) -> Fraction:
    return max((abs(x) for row in a for x in row), default=Fraction(0))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=DEFAULT_CERT,
        help="JSON rational certificate (default: coordinated n=48 certificate)",
    )
    args = parser.parse_args()
    path = args.certificate
    raw_bytes = path.read_bytes()
    cert = json.loads(raw_bytes)

    if cert.get("schema") != "rational-balanced-ctmc-returned-bit-v1":
        raise ValueError(f"unexpected certificate schema: {cert.get('schema')!r}")
    n = cert.get("n")
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0 or n % 2:
        raise ValueError("n must be a positive even integer")

    q = matrix(cert.get("Q"), "Q")
    u = matrix(cert.get("U"), "U")
    k = matrix(cert.get("K"), "K")
    a = rational(cert.get("a"), "a")

    if shape(q) != (n, n):
        raise ValueError(f"Q must be {n}x{n}, got {shape(q)}")
    nu, m = shape(u)
    if nu != n:
        raise ValueError(f"U must have {n} rows, got {nu}")
    if shape(k) != (m, m):
        raise ValueError(f"K must be {m}x{m}, got {shape(k)}")
    if m == 0:
        raise ValueError("U must have at least one column")
    if not (Fraction(0) < a < Fraction(1)):
        raise ValueError("require exact 0 < a < 1 for a contrast above exp(-pi)")

    offdiag = [
        q[i][j] for i in range(n) for j in range(n) if i != j
    ]
    negative_offdiag = [(i, j, q[i][j]) for i in range(n) for j in range(n)
                        if i != j and q[i][j] < 0]
    if negative_offdiag:
        i, j, val = negative_offdiag[0]
        raise AssertionError(f"negative off-diagonal Q[{i},{j}]={val}")

    row_sums = [sum(row, Fraction(0)) for row in q]
    col_sums = [
        sum((q[i][j] for i in range(n)), Fraction(0)) for j in range(n)
    ]
    if any(row_sums):
        bad = next(i for i, value in enumerate(row_sums) if value)
        raise AssertionError(f"row balance fails at row {bad}: {row_sums[bad]}")
    if any(col_sums):
        bad = next(j for j, value in enumerate(col_sums) if value)
        raise AssertionError(f"column balance fails at column {bad}: {col_sums[bad]}")

    z = [Fraction(1) if i < n // 2 else Fraction(-1) for i in range(n)]
    if any(u[i][0] != z[i] for i in range(n)):
        bad = next(i for i in range(n) if u[i][0] != z[i])
        raise AssertionError(f"U first column is not canonical flat z at index {bad}")
    if "z" in cert:
        stored_z = [rational(x, f"z[{i}]") for i, x in enumerate(cert["z"])]
        if stored_z != z:
            raise AssertionError("stored z differs from canonical balanced flat sign vector")

    rank = exact_rank(u)
    if rank != m:
        raise AssertionError(f"U is not full column rank: exact rank {rank} < {m}")

    k_minus_a_i = [row[:] for row in k]
    for i in range(m):
        k_minus_a_i[i][i] -= a
    qu = matmul(q, u)
    u_k_minus_a_i = matmul(u, k_minus_a_i)
    residual = [
        [qu[i][j] - u_k_minus_a_i[i][j] for j in range(m)]
        for i in range(n)
    ]
    if any(x for row in residual for x in row):
        raise AssertionError(f"QU=U(K-aI) fails; exact max residual {max_abs(residual)}")

    # This square-free polynomial identity certifies the exact half-turn:
    # eigenvalues of K lie in {+/-i, +/-3i}, with no Jordan blocks, hence e^(pi K)=-I.
    k2 = matmul(k, k)
    k2_plus_i = [row[:] for row in k2]
    k2_plus_9i = [row[:] for row in k2]
    for i in range(m):
        k2_plus_i[i][i] += 1
        k2_plus_9i[i][i] += 9
    four_frequency_residual = matmul(k2_plus_i, k2_plus_9i)
    if any(x for row in four_frequency_residual for x in row):
        raise AssertionError(
            "K does not satisfy (K^2+I)(K^2+9I)=0; "
            f"exact max residual {max_abs(four_frequency_residual)}"
        )

    if cert.get("T") != "pi":
        raise ValueError("certificate must declare T='pi'")
    positive_rates = [x for x in offdiag if x > 0]
    if not positive_rates:
        raise AssertionError("Q has no positive off-diagonal rates")
    min_positive = min(positive_rates)
    zero_offdiag = sum(x == 0 for x in offdiag)

    construction = cert.get("construction", {})
    source_path = path.parent / str(construction.get("source", ""))
    source_hash_status = "not available"
    if construction.get("source_sha256") and source_path.is_file():
        actual_source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
        source_hash_status = "matches" if actual_source_hash == construction["source_sha256"] else "MISMATCH"
        if source_hash_status != "matches":
            raise AssertionError(
                f"source hash mismatch for {source_path}: {actual_source_hash}"
            )

    print("EXACT CERTIFICATE CHECK: PASS")
    print(f"certificate: {path}")
    print(f"sha256: {hashlib.sha256(raw_bytes).hexdigest()}")
    print(f"dimensions: Q {n}x{n}; U {n}x{m}; K {m}x{m}; exact rank(U)={rank}")
    print(f"off-diagonal rates: all >= 0; positive count={len(positive_rates)}; zero count={zero_offdiag}")
    print(f"minimum positive rate: {min_positive} ({float(min_positive):.12g})")
    print("row balance: exact; column balance: exact")
    print("U[:,0] = canonical (+1,...,+1,-1,...,-1): exact")
    print("QU = U(K-aI): exact")
    print("(K^2+I)(K^2+9I)=0: exact; therefore exp(pi K)=-I")
    print(f"a = {a} ({float(a):.16g}); 0<a<1: exact")
    print("therefore exp(pi Q)z = -exp(-pi a)z on the certified invariant subspace")
    print(f"pinned float source hash: {source_hash_status}")


if __name__ == "__main__":
    main()
