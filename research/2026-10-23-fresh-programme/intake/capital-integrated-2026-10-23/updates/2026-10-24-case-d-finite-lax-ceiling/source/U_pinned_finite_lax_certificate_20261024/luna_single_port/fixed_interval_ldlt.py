"""Rigorous no-pivot LDL^T positive-definiteness checker.

The only arithmetic used by the checker is Python's integer arithmetic and
fractions.Fraction for exact endpoint comparisons. A FixedInterval(lo, hi)
represents [lo/2**P, hi/2**P], with one common P supplied to certify_spd.

Certification invariant
-----------------------
At LDL step k, assume each stored interval encloses the corresponding exact
entry of the no-pivot factorization of any symmetric input matrix selected
from the supplied entry intervals. Addition, subtraction, multiplication,
squaring, and division below return enclosing intervals: multiplication
checks all four rectangle corners; squaring uses the exact range of x**2 on
an interval; division is used only when the denominator interval is strictly
positive and encloses all four endpoint quotients. Every result is rounded
outward to the common fixed-point grid.

Consequently the computed pivot interval encloses the exact kth LDL pivot.
If its lower endpoint is positive, that pivot is positive for every matrix
covered by the input intervals, so division in the next step is valid and
the induction continues. At completion the exact factorization is
A = L diag(d) L^T with unit lower-triangular L and all d_k > 0. Congruence
therefore makes A positive definite. A nonpositive/uncertain pivot only
means "not certified"; it is never rounded into a positive decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence, TypeAlias, Union


MatrixEntry: TypeAlias = Union[Fraction, int, "FixedInterval", tuple[int, int]]


@dataclass(frozen=True)
class FixedInterval:
    """Integer endpoints for a real interval on the checker grid 2**(-P)."""

    lo: int
    hi: int

    def __post_init__(self) -> None:
        if not isinstance(self.lo, int) or not isinstance(self.hi, int):
            raise TypeError("fixed-point interval endpoints must be integers")
        if self.lo > self.hi:
            raise ValueError("interval lower endpoint exceeds upper endpoint")

    def as_fractions(self, precision_bits: int) -> tuple[Fraction, Fraction]:
        scale = 1 << precision_bits
        return Fraction(self.lo, scale), Fraction(self.hi, scale)


@dataclass(frozen=True)
class LDLTResult:
    certified: bool
    precision_bits: int
    pivot_intervals: tuple[tuple[Fraction, Fraction], ...]
    positive_pivot_lower_bounds: tuple[Fraction, ...]
    failed_pivot: int | None
    diagnostic: str


def _floor_fraction(x: Fraction) -> int:
    return x.numerator // x.denominator


def _ceil_fraction(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def _to_interval(value: MatrixEntry, scale: int) -> FixedInterval:
    """Enclose one exact Fraction/int or accept an already scaled interval."""
    if isinstance(value, FixedInterval):
        return value
    if isinstance(value, tuple) and len(value) == 2:
        return FixedInterval(value[0], value[1])
    if isinstance(value, int):
        value = Fraction(value)
    if isinstance(value, Fraction):
        scaled = value * scale
        return FixedInterval(_floor_fraction(scaled), _ceil_fraction(scaled))
    raise TypeError(f"unsupported matrix entry {value!r}")


def _add(a: FixedInterval, b: FixedInterval) -> FixedInterval:
    return FixedInterval(a.lo + b.lo, a.hi + b.hi)


def _neg(a: FixedInterval) -> FixedInterval:
    return FixedInterval(-a.hi, -a.lo)


def _sub(a: FixedInterval, b: FixedInterval) -> FixedInterval:
    return _add(a, _neg(b))


def _floor_div(numerator: int, denominator: int) -> int:
    """Floor division with a positive denominator."""
    if denominator <= 0:
        raise ValueError("internal floor division requires positive denominator")
    return numerator // denominator


def _ceil_div(numerator: int, denominator: int) -> int:
    """Ceiling division with a positive denominator."""
    if denominator <= 0:
        raise ValueError("internal ceiling division requires positive denominator")
    return -((-numerator) // denominator)


def _mul(a: FixedInterval, b: FixedInterval, scale: int) -> FixedInterval:
    # A bilinear function on a rectangle reaches its extrema at the corners.
    products = (a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi)
    return FixedInterval(
        _floor_div(min(products), scale),
        _ceil_div(max(products), scale),
    )


def _square(a: FixedInterval, scale: int) -> FixedInterval:
    # The exact square range is tighter than multiplying an interval by itself
    # (which would spuriously admit negative values when a straddles zero).
    if a.lo <= 0 <= a.hi:
        lower = 0
    else:
        lower = min(a.lo * a.lo, a.hi * a.hi)
    upper = max(a.lo * a.lo, a.hi * a.hi)
    return FixedInterval(
        _floor_div(lower, scale),
        _ceil_div(upper, scale),
    )


def _div_positive_denominator(
    numerator: FixedInterval, denominator: FixedInterval, scale: int
) -> FixedInterval:
    if denominator.lo <= 0:
        raise ValueError("division denominator interval is not strictly positive")
    # Real quotient extrema over a rectangle with y>0 occur at corners.
    # Input endpoints represent x/S and y/S; the output grid coordinate is
    # S*(x/S)/(y/S) = S*x/y.
    corners = [
        Fraction(scale * x, y)
        for x in (numerator.lo, numerator.hi)
        for y in (denominator.lo, denominator.hi)
    ]
    return FixedInterval(
        _floor_fraction(min(corners)),
        _ceil_fraction(max(corners)),
    )


def _matrix_input(
    matrix: Sequence[Sequence[MatrixEntry]], precision_bits: int
) -> tuple[list[list[FixedInterval]], int]:
    if not isinstance(precision_bits, int) or precision_bits < 1:
        raise ValueError("precision_bits must be a positive integer")
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be nonempty and square")
    scale = 1 << precision_bits
    intervals = [[_to_interval(value, scale) for value in row] for row in matrix]
    # Treat each symmetric entry as one interval. Requiring the supplied
    # enclosures to match avoids silently changing an asymmetric input.
    for i in range(n):
        for j in range(i):
            if intervals[i][j] != intervals[j][i]:
                raise ValueError(
                    f"matrix enclosures are not symmetric at ({i}, {j})"
                )
    return intervals, scale


def certify_spd(
    matrix: Sequence[Sequence[MatrixEntry]], precision_bits: int = 160
) -> LDLTResult:
    """Certify that a symmetric rational/interval matrix is positive definite.

    Parameters
    ----------
    matrix:
        Symmetric square sequence. Each entry may be an exact Fraction,
        an int, a FixedInterval or an integer (lo, hi) pair. Intervals are
        interpreted at the common scale 2**(-precision_bits).
    precision_bits:
        Number P in the fixed-point scale 2**P. Every arithmetic result is
        rounded outward to this grid.

    Returns
    -------
    LDLTResult:
        certified is true only when every pivot interval has a strictly
        positive lower endpoint. Returned lower bounds are exact Fractions
        and can be recorded as certificate margins.

    Notes
    -----
    No pivoting is attempted. An SPD matrix has positive pivots in this
    ordering, but a non-SPD matrix or interval dependency can make this
    checker inconclusive. That is a safe failure, not evidence of
    non-positive-definiteness.
    """
    A, scale = _matrix_input(matrix, precision_bits)
    n = len(A)
    zero = FixedInterval(0, 0)
    one = FixedInterval(scale, scale)
    L = [[zero for _ in range(n)] for _ in range(n)]
    D = [zero for _ in range(n)]
    pivot_records: list[tuple[Fraction, Fraction]] = []
    positive_lowers: list[Fraction] = []

    def fractions(interval: FixedInterval) -> tuple[Fraction, Fraction]:
        return interval.as_fractions(precision_bits)

    for k in range(n):
        pivot = A[k][k]
        for j in range(k):
            term = _mul(D[j], _square(L[k][j], scale), scale)
            pivot = _sub(pivot, term)
        pivot_records.append(fractions(pivot))

        if pivot.lo <= 0:
            return LDLTResult(
                certified=False,
                precision_bits=precision_bits,
                pivot_intervals=tuple(pivot_records),
                positive_pivot_lower_bounds=tuple(positive_lowers),
                failed_pivot=k,
                diagnostic=(
                    f"pivot {k} is not strictly positive on its enclosure "
                    f"[{pivot.lo}/{scale}, {pivot.hi}/{scale}]"
                ),
            )

        D[k] = pivot
        positive_lowers.append(Fraction(pivot.lo, scale))
        L[k][k] = one

        for i in range(k + 1, n):
            numerator = A[i][k]
            for j in range(k):
                term = _mul(_mul(L[i][j], D[j], scale), L[k][j], scale)
                numerator = _sub(numerator, term)
            L[i][k] = _div_positive_denominator(numerator, pivot, scale)

    return LDLTResult(
        certified=True,
        precision_bits=precision_bits,
        pivot_intervals=tuple(pivot_records),
        positive_pivot_lower_bounds=tuple(positive_lowers),
        failed_pivot=None,
        diagnostic=(
            f"certified SPD by interval LDL^T; minimum pivot lower bound "
            f"is {min(positive_lowers)}"
        ),
    )


__all__ = ["FixedInterval", "LDLTResult", "certify_spd"]
