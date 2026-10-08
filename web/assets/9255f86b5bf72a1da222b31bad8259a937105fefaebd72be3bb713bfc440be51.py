#!/usr/bin/env python3
"""Exact, standard-library check of the BJSW seed pair and BMVZ singleton layer.

The circuit matrices are evaluated in Q(sqrt(2)); the repeated violation-term
row counts are computed from the exact support formula, without constructing
the exponentially large 32**R by 32**R matrices.
"""

from __future__ import annotations

import csv
from itertools import product
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path


@dataclass(frozen=True)
class Qsqrt2:
    """a + b*sqrt(2), with exact rational coefficients."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other: "Qsqrt2") -> "Qsqrt2":
        return Qsqrt2(self.a + other.a, self.b + other.b)

    def __sub__(self, other: "Qsqrt2") -> "Qsqrt2":
        return Qsqrt2(self.a - other.a, self.b - other.b)

    def __mul__(self, other: "Qsqrt2") -> "Qsqrt2":
        return Qsqrt2(
            self.a * other.a + 2 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def __neg__(self) -> "Qsqrt2":
        return Qsqrt2(-self.a, -self.b)

    def __bool__(self) -> bool:
        return bool(self.a or self.b)


ZERO = Qsqrt2()
ONE = Qsqrt2(Fraction(1))
HALF = Qsqrt2(Fraction(1, 2))
SQRT2_OVER_2 = Qsqrt2(Fraction(0), Fraction(1, 2))


def matmul(left: list[list[Qsqrt2]], right: list[list[Qsqrt2]]) -> list[list[Qsqrt2]]:
    rows, inner, cols = len(left), len(right), len(right[0])
    return [
        [
            sum_q((left[i][k] * right[k][j] for k in range(inner)))
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def sum_q(values) -> Qsqrt2:
    total = ZERO
    for value in values:
        total = total + value
    return total


def identity(dim: int) -> list[list[Qsqrt2]]:
    return [[ONE if i == j else ZERO for j in range(dim)] for i in range(dim)]


def one_qubit_gate(n: int, qubit: int, entries: list[list[Qsqrt2]]) -> list[list[Qsqrt2]]:
    dim = 1 << n
    result = [[ZERO for _ in range(dim)] for _ in range(dim)]
    bit = 1 << (n - 1 - qubit)
    for col in range(dim):
        input_bit = 1 if col & bit else 0
        base = col & ~bit
        for output_bit in (0, 1):
            row = base | (bit if output_bit else 0)
            result[row][col] = entries[output_bit][input_bit]
    return result


H = [[SQRT2_OVER_2, SQRT2_OVER_2], [SQRT2_OVER_2, -SQRT2_OVER_2]]
Z = [[ONE, ZERO], [ZERO, -ONE]]
X = [[ZERO, ONE], [ONE, ZERO]]


def cnot(n: int, control: int, target: int) -> list[list[Qsqrt2]]:
    dim = 1 << n
    result = [[ZERO for _ in range(dim)] for _ in range(dim)]
    control_bit = 1 << (n - 1 - control)
    target_bit = 1 << (n - 1 - target)
    for col in range(dim):
        row = col ^ target_bit if col & control_bit else col
        result[row][col] = ONE
    return result


def cz(n: int, first: int, second: int) -> list[list[Qsqrt2]]:
    dim = 1 << n
    result = [[ZERO for _ in range(dim)] for _ in range(dim)]
    first_bit = 1 << (n - 1 - first)
    second_bit = 1 << (n - 1 - second)
    for col in range(dim):
        result[col][col] = -ONE if col & first_bit and col & second_bit else ONE
    return result


def q3_cliffords() -> tuple[list[list[Qsqrt2]], list[list[Qsqrt2]]]:
    # C_phi = ZH on q0, as in BJSW equation (6).
    c_phi = matmul(one_qubit_gate(3, 0, Z), one_qubit_gate(3, 0, H))

    # C_psi maps |000> to (|000>-|011>-|101>-|110>)/2.
    # Read right-to-left: H0 H1, CNOT(0->2), CNOT(1->2), Z0 Z1, CZ(0,1).
    c_psi = identity(8)
    for gate in (
        one_qubit_gate(3, 0, H),
        one_qubit_gate(3, 1, H),
        cnot(3, 0, 2),
        cnot(3, 1, 2),
        one_qubit_gate(3, 1, Z),
        one_qubit_gate(3, 0, Z),
        cz(3, 0, 1),
    ):
        c_psi = matmul(gate, c_psi)
    return c_phi, c_psi


def column(matrix: list[list[Qsqrt2]], col: int) -> list[Qsqrt2]:
    return [matrix[row][col] for row in range(len(matrix))]


def conjugate_transpose_real(matrix: list[list[Qsqrt2]]) -> list[list[Qsqrt2]]:
    # All gates above are real, so transpose is the adjoint.
    return [list(row) for row in zip(*matrix)]


def append_clock_suffix(matrix3: list[list[Qsqrt2]]) -> list[list[Qsqrt2]]:
    """Extend a 3-qubit preparation by identity on |00>, then X on q3 for |10>."""
    result = [[ZERO for _ in range(32)] for _ in range(32)]
    for clock in range(4):
        for row in range(8):
            for col in range(8):
                result[row * 4 + clock][col * 4 + clock] = matrix3[row][col]
    return matmul(one_qubit_gate(5, 3, X), result)


def abs_squared(value: Qsqrt2) -> Fraction:
    # The tested W entries have either a=0 or b=0, so this is exact in Q(sqrt(2)).
    return value.a * value.a + 2 * value.b * value.b


def seed_data() -> tuple[dict[int, int], dict[int, int]]:
    """Return basis-index -> sign dictionaries for the 5-qubit seed kets.

    Qubits are big-endian q0...q4. The common BJSW outer clock pattern is |10>.
    """
    phi5 = {0b00010: +1, 0b10010: -1}
    psi5 = {
        0b00010: +1,
        0b01110: -1,
        0b10110: -1,
        0b11010: -1,
    }
    return phi5, psi5


def local_projector_entry(signed_support: dict[int, int], x: int, y: int) -> Fraction:
    size = len(signed_support)
    if x not in signed_support or y not in signed_support:
        return Fraction(0)
    return Fraction(signed_support[x] * signed_support[y], size)


def amplified_entry(
    signed_support: dict[int, int], x: tuple[int, ...], y: tuple[int, ...]
) -> Fraction:
    """Entry of I - (I-|v><v|)^{tensor R} for R five-qubit blocks."""
    if len(x) != len(y):
        raise ValueError("row and column must have the same number of blocks")
    product = Fraction(1)
    for xb, yb in zip(x, y):
        delta = Fraction(int(xb == yb))
        product *= delta - local_projector_entry(signed_support, xb, yb)
    return Fraction(int(x == y)) - product


def row_nnz_formula(signed_support: dict[int, int], x: tuple[int, ...]) -> int:
    # If xb is outside the seed support, the local factor forces yb=xb.
    # If xb is in support, there are exactly |support| choices for yb.
    support_size = len(signed_support)
    active_blocks = sum(xb in signed_support for xb in x)
    # When every block is outside support, the identity diagonal cancels the
    # complement-projector diagonal exactly, so the entire row is zero.
    return 0 if active_blocks == 0 else support_size**active_blocks


def ceil_one_plus_sqrt_power(r: int) -> int:
    # ceil(1 + 2^(3r/2)), evaluated with integer arithmetic.
    q_floor = isqrt(1 << (3 * r))
    q_is_integer = (q_floor * q_floor == (1 << (3 * r)))
    return q_floor + (1 if q_is_integer else 2)


def main() -> None:
    c_phi, c_psi = q3_cliffords()
    phi_target = [ZERO for _ in range(8)]
    phi_target[0] = SQRT2_OVER_2
    phi_target[4] = -SQRT2_OVER_2
    psi_target = [ZERO for _ in range(8)]
    psi_target[0] = HALF
    psi_target[3] = -HALF
    psi_target[5] = -HALF
    psi_target[6] = -HALF
    assert column(c_phi, 0) == phi_target
    assert column(c_psi, 0) == psi_target

    relative = matmul(conjugate_transpose_real(c_psi), c_phi)
    assert all(abs_squared(entry) == Fraction(1, 8) for row in relative for entry in row)
    mu_squared = max(abs_squared(entry) for row in relative for entry in row)
    assert mu_squared == Fraction(1, 8)

    c_phi5 = append_clock_suffix(c_phi)
    c_psi5 = append_clock_suffix(c_psi)
    relative5 = matmul(conjugate_transpose_real(c_psi5), c_phi5)
    nonzero5 = [entry for row in relative5 for entry in row if entry]
    assert len(nonzero5) == 256
    assert all(abs_squared(entry) == Fraction(1, 8) for entry in nonzero5)
    assert all(abs_squared(entry) == 0 for row in relative5 for entry in row if not entry)

    phi5, psi5 = seed_data()
    assert len(phi5) == 2 and len(psi5) == 4
    assert set(phi5) & set(psi5) == {0b00010}

    # Exhaustively verify every local (R=1) row against the support formula.
    for support in (phi5, psi5):
        for x0 in range(32):
            row_count = sum(
                amplified_entry(support, (x0,), (y0,)) != 0 for y0 in range(32)
            )
            assert row_count == row_nnz_formula(support, (x0,))

    # Exhaustively verify the exact row-union count of the two added terms for
    # R=1,2. Base-family summands are identity on this ancilla and therefore
    # cannot affect the off-diagonal columns counted here.
    common = 0b00010
    for r in (1, 2):
        x = (common,) * r
        full_added_row_count = 0
        for y in product(range(32), repeat=r):
            entry = (
                amplified_entry(phi5, x, y) + amplified_entry(psi5, x, y)
            ) / 4
            full_added_row_count += entry != 0
        assert full_added_row_count == 2**r + 4**r - 1

    # All blocks in the seed support attain the maximum s**R row count.
    table_rows = []
    for r in (1, 2, 4, 8, 16, 32, 64, 128):
        phi_max = row_nnz_formula(phi5, (0b00010,) * r)
        psi_max = row_nnz_formula(psi5, (0b00010,) * r)
        assert phi_max == 2**r
        assert psi_max == 4**r
        table_rows.append(
            {
                "copies_R": r,
                "local_qubits": 5 * r,
                "phi_seed_support": len(phi5),
                "psi_seed_support": len(psi5),
                "phi_Q_max_row_nnz": phi_max,
                "psi_Q_max_row_nnz": psi_max,
                "augmented_full_output_row_lower_bound": phi_max + psi_max - 1,
                "relative_basis_mu": "1/(2*sqrt(2))",
                "bare_two_branch_enforcer_row_lower_bound": ceil_one_plus_sqrt_power(r),
                "enforcer_bound_exact_form": f"ceil(1+2^({3*r}/2))",
            }
        )

    out = Path(__file__).with_name("bmvz_bjsw_seed_pair_table.csv")
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table_rows[0]))
        writer.writeheader()
        writer.writerows(table_rows)

    print("PASS: BJSW 3-qubit seed kets are exact Clifford images of |000>.")
    print("PASS: max relative-basis entry is exactly 1/(2*sqrt(2)); squared magnitude = 1/8.")
    print("PASS: the five-qubit preparations with common |10> suffix have 256 nonzero relative entries, all squared magnitude 1/8.")
    print("PASS: all 32 local rows match the exact amplified-term support formula for each seed.")
    print("PASS: the two 5-qubit seed supports intersect only at |00010>, so the full-output row union is exact.")
    print("PASS: exhaustive R=1,2 row scans give 2^R+4^R-1 nonzeros for the added pair sum.")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
