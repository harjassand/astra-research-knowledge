"""Exact/interval diagnostics for critical-spin finite-N certificates.

The sector bound is enclosed with outward-rounded dyadic intervals.  The
matrix-square-root routine uses exact rational 3x3 operations between explicit
dyadic rounding steps, with the perturbation budget stated in
spin_certificates_notes.txt.  It is a mathematical compiler prototype; it does
not prepare physical qubits or certify a hardware gate set.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb, isqrt
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent


def ceil_div(a: int, b: int) -> int:
    assert b > 0
    return -((-a) // b)


def iroot(n: int, degree: int) -> int:
    """Floor integer degree-th root, for the small degrees used here."""
    assert n >= 0 and degree >= 1
    if degree == 1:
        return n
    if degree == 2:
        return isqrt(n)
    lo, hi = 0, 1
    while hi**degree <= n:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**degree <= n:
            lo = mid
        else:
            hi = mid
    return lo


@dataclass(frozen=True)
class Iv:
    """Closed interval [lo,hi] in units 2^-p."""
    lo: int
    hi: int
    p: int

    def __post_init__(self):
        assert self.lo <= self.hi

    @property
    def scale(self) -> int:
        return 1 << self.p

    @classmethod
    def frac(cls, q: Fraction | int, p: int) -> "Iv":
        q = Fraction(q)
        s = 1 << p
        return cls((q.numerator * s) // q.denominator,
                   ceil_div(q.numerator * s, q.denominator), p)

    @classmethod
    def zero(cls, p: int) -> "Iv":
        return cls(0, 0, p)

    def _same(self, other: "Iv") -> None:
        assert self.p == other.p

    def __add__(self, other: "Iv") -> "Iv":
        self._same(other)
        return Iv(self.lo + other.lo, self.hi + other.hi, self.p)

    def __sub__(self, other: "Iv") -> "Iv":
        self._same(other)
        return Iv(self.lo - other.hi, self.hi - other.lo, self.p)

    def __mul__(self, other: "Iv") -> "Iv":
        self._same(other)
        s = self.scale
        products = (self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi)
        return Iv(min(products) // s, ceil_div(max(products), s), self.p)

    def scale_by(self, q: Fraction | int) -> "Iv":
        q = Fraction(q)
        a, b = self.lo * q.numerator, self.hi * q.numerator
        if q.numerator < 0:
            a, b = b, a
        return Iv((a // q.denominator), ceil_div(b, q.denominator), self.p)

    def div_pos(self, other: "Iv") -> "Iv":
        self._same(other)
        assert self.lo >= 0 and other.lo > 0
        s = self.scale
        return Iv((self.lo * s) // other.hi,
                  ceil_div(self.hi * s, other.lo), self.p)

    def div_int_pos(self, n: int) -> "Iv":
        assert n > 0 and self.lo >= 0
        return Iv(self.lo // n, ceil_div(self.hi, n), self.p)

    def recip_pos(self) -> "Iv":
        assert self.lo > 0
        s = self.scale
        return Iv((s * s) // self.hi, ceil_div(s * s, self.lo), self.p)

    def as_fraction_bounds(self) -> tuple[Fraction, Fraction]:
        s = self.scale
        return Fraction(self.lo, s), Fraction(self.hi, s)


def sqrt_iv(q: Fraction | int, p: int, degree: int = 2) -> Iv:
    """Enclose the nonnegative rational root, returning dyadic endpoints."""
    q = Fraction(q)
    assert q >= 0 and degree >= 1
    s = 1 << p
    target_num = q.numerator * s**degree
    k = iroot(target_num // q.denominator, degree)
    exact = k**degree * q.denominator == target_num
    return Iv(k, k if exact else k + 1, p)


def exp_point(x: int, p: int) -> Iv:
    """Certified enclosure of exp(x/2^p) using Taylor and range reduction."""
    s = 1 << p
    if x < 0:
        return exp_point(-x, p).recip_pos()
    if x == 0:
        return Iv(s, s, p)
    # Enclose y=x/2^k in [0,1/2] at the same fixed-point precision.
    k = 0
    while ceil_div(x, 1 << k) > s // 2:
        k += 1
    den = 1 << k
    y = Iv(x // den, ceil_div(x, den), p)
    assert 0 <= y.lo <= y.hi <= s // 2

    # Every Taylor term is nonnegative.  The remaining geometric tail is at
    # most twice the first omitted term because y<=1/2.
    total = Iv(s, s, p)
    term = Iv(s, s, p)
    degree = p + 16
    for n in range(1, degree + 1):
        term = (term * y).div_int_pos(n)
        total = total + term
    next_term = (term * y).div_int_pos(degree + 1)
    value = Iv(total.lo, total.hi + 2 * next_term.hi, p)
    for _ in range(k):
        value = value * value
    return value


def exp_iv(x: Iv) -> Iv:
    """Monotonic interval extension of exp."""
    lo = exp_point(x.lo, x.p)
    hi = exp_point(x.hi, x.p)
    return Iv(lo.lo, hi.hi, x.p)


def root_ratio(num: Fraction, denominator: Iv) -> Iv:
    """Enclose num/(denominator/2^p), in units 2^-p; all values positive."""
    assert num >= 0 and denominator.lo > 0
    s = denominator.scale
    return Iv((num.numerator * s * s) // (num.denominator * denominator.hi),
              ceil_div(num.numerator * s * s,
                       num.denominator * denominator.lo), denominator.p)


def fraction_text(q: Fraction) -> str:
    return f"{q.numerator}/{q.denominator}"


def iv_text(x: Iv) -> dict:
    lo, hi = x.as_fraction_bounds()
    return {"lo": fraction_text(lo), "hi": fraction_text(hi), "dyadic_bits": x.p}


def sector_certificate(N: int, M: Fraction, B: Fraction, p: int = 128) -> dict:
    """Outward-rounded upper bound from the public finite-N sector formula."""
    M, B = Fraction(M), Fraction(B)
    if N < 1 or M < 0 or B < 0:
        raise ValueError("require N>=1 and public bounds M,B>=0")
    if 4 * N <= M * M:
        raise ValueError("excluded size: t0=2/N-M/N^(3/2) is not positive")
    if not isinstance(p, int) or p < 1:
        raise ValueError("require positive integer dyadic precision")
    s = 1 << p
    Miv, Biv = Iv.frac(M, p), Iv.frac(B, p)
    rscale = sqrt_iv(Fraction(N**3), p, degree=4)
    sqrtN = sqrt_iv(Fraction(N), p)
    D, U = Iv.zero(p), Iv.zero(p)
    sector_rows = []
    dimension_sum = 0
    j2_values = range(N % 2, N + 1, 2)
    for j2 in j2_values:
        d = j2 + 1
        k = (N - j2) // 2
        multiplicity = Fraction(d * comb(N + 1, k), N + 1)
        dimension_sum += d * multiplicity
        coeff = d * multiplicity
        base_exp = Fraction(j2 * (j2 + 2), 2 * N)
        a = Iv.frac(coeff, p) * exp_iv(Iv.frac(base_exp, p))
        r = root_ratio(Fraction(j2 + 1, 2), rscale)
        r2 = r * r
        tilt = Miv * r2 + Biv * r
        four_m_r2 = r2.scale_by(4) * Miv
        b_half_r = Biv.scale_by(Fraction(1, 2)) * r
        square_term = four_m_r2 + Biv * r
        P = four_m_r2 + b_half_r + (square_term * square_term).scale_by(Fraction(1, 3))
        d_term = a * exp_iv(Iv( -tilt.hi, -tilt.lo, p))
        u_term = a * exp_iv(tilt) * P
        D, U = D + d_term, U + u_term
        sector_rows.append({"j_twice": j2, "multiplicity": fraction_text(multiplicity),
                            "r": iv_text(r), "tilt": iv_text(tilt),
                            "D_term": iv_text(d_term), "U_term": iv_text(u_term)})
    assert dimension_sum == 1 << N, "Schur-sector multiplicities must sum to 2^N"
    if D.lo <= 0:
        # The exact ratio denominator is positive. This grid cannot resolve
        # it; the PUBLIC clipped certificate still lies in [0,1]. Return a
        # genuine containing interval, not [1,1] and not an unguarded ratio.
        return {
            "N": N, "M": fraction_text(M), "B": fraction_text(B),
            "validity": "exact check 4N>M^2; t0>0",
            "bound_formula": "min(1, 3M/(2 N^(3/2)) * U_N/D_N)",
            "certificate": iv_text(Iv(0, s, p)),
            "unclipped_interval": None,
            "status": "CERTIFIED_TRIVIAL_BOUND; denominator unresolved at requested precision",
            "dimension_identity": fraction_text(dimension_sum),
            "D": iv_text(D), "U": iv_text(U), "sectors": sector_rows,
            "repair_origin": "c07_s01 owned-copy boundary repair; underlying primitive c07_l07",
        }
    if M == 0:
        bound = Iv.zero(p)
    else:
        pref = Iv.frac(Fraction(3 * M, 2 * N), p).div_pos(sqrtN)
        bound = pref * U.div_pos(D)
    one = s
    clipped_hi = min(bound.hi, one)
    clipped = Iv(min(bound.lo, one), clipped_hi, p)
    return {
        "N": N, "M": fraction_text(M), "B": fraction_text(B),
        "validity": "exact check 4N>M^2; t0>0",
        "bound_formula": "min(1, 3M/(2 N^(3/2)) * U_N/D_N)",
        "certificate": iv_text(clipped),
        "unclipped_interval": iv_text(bound),
        "interval_method": "outward dyadic arithmetic; exp Taylor on [0,1/2] after range reduction; exact sector multiplicities",
        "sector_count": len(sector_rows),
        "dimension_identity": fraction_text(dimension_sum),
        "D": iv_text(D), "U": iv_text(U), "sectors": sector_rows,
    }


# Exact rational 3x3 matrix utilities used by the square-root construction.
Matrix = list[list[Fraction]]


def eye(n: int = 3) -> Matrix:
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def m_add(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] + B[i][j] for j in range(3)] for i in range(3)]


def m_scale(c: Fraction, A: Matrix) -> Matrix:
    return [[c * A[i][j] for j in range(3)] for i in range(3)]


def m_mul(A: Matrix, B: Matrix) -> Matrix:
    return [[sum((A[i][k] * B[k][j] for k in range(3)), Fraction(0))
             for j in range(3)] for i in range(3)]


def det(A: Matrix) -> Fraction:
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def inv(A: Matrix) -> Matrix:
    d = det(A)
    if d == 0:
        raise ValueError("singular Newton iterate")
    cof = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            rows = [r for r in range(3) if r != i]
            cols = [c for c in range(3) if c != j]
            minor = A[rows[0]][cols[0]] * A[rows[1]][cols[1]] - A[rows[0]][cols[1]] * A[rows[1]][cols[0]]
            cof[i][j] = (-1 if (i + j) % 2 else 1) * minor
    return [[cof[j][i] / d for j in range(3)] for i in range(3)]


def principal_minors_nonnegative(A: Matrix) -> bool:
    if any(A[i][j] != A[j][i] for i in range(3) for j in range(3)):
        return False
    if any(A[i][i] < 0 for i in range(3)):
        return False
    for i, j in ((0, 1), (0, 2), (1, 2)):
        if A[i][i] * A[j][j] - A[i][j] * A[j][i] < 0:
            return False
    return det(A) >= 0


def leading_minors_positive(A: Matrix) -> bool:
    return (A[0][0] > 0
            and A[0][0] * A[1][1] - A[0][1] * A[1][0] > 0
            and det(A) > 0)


def round_nearest_grid(x: Fraction, bits: int) -> Fraction:
    s = 1 << bits
    n, d = x.numerator * s, x.denominator
    k = (2 * n + d) // (2 * d)
    return Fraction(k, s)


def round_symmetric(A: Matrix, bits: int) -> Matrix:
    out = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(i, 3):
            out[i][j] = out[j][i] = round_nearest_grid(A[i][j], bits)
    return out


def ceil_sqrt_fraction(q: Fraction, bits: int) -> Fraction:
    assert q >= 0
    s = 1 << bits
    target = q.numerator * s * s
    k = isqrt(target // q.denominator)
    if k * k * q.denominator < target:
        k += 1
    return Fraction(k, s)


def newton_schedule(M: Fraction, q: Fraction, gamma: Fraction) -> tuple[int, int, Fraction, int]:
    alpha = (q / 4) ** 2
    # For every eigenvalue lambda in [alpha,2M+alpha], z_0<=4 gamma/q.
    z_bound = 4 * gamma / q
    k0, z = 0, z_bound
    while z > 2:
        z *= Fraction(5, 8)
        k0 += 1
    # Once z<=2, e=z-1<=1 and e_next<=e^2/2.
    k1, e = 0, Fraction(1)
    while gamma * e > q / 4:
        e = e * e / 2
        k1 += 1
    k = k0 + k1
    Lnewt = 1 + 4 * (2 * M + alpha) / alpha
    local_budget = min(q, q / 4) / (16 * k * Lnewt**k)
    round_bits = 0
    while Fraction(3, 2 * (1 << round_bits)) > local_budget:
        round_bits += 1
    return k0, k1, local_budget, round_bits


def sqrt_psd3_guarded(C: Matrix, M: Fraction, q: Fraction) -> tuple[Matrix, dict]:
    """Return a rational X with the proved operator bound ||X-sqrt(C)||<q."""
    M, q = Fraction(M), Fraction(q)
    if M < 0 or q <= 0:
        raise ValueError("require M>=0 and target q>0")
    if not principal_minors_nonnegative(C):
        raise ValueError("C is not exactly positive semidefinite")
    cap = m_scale(2 * M, eye())
    if not principal_minors_nonnegative(m_add(cap, m_scale(Fraction(-1), C))):
        raise ValueError("C does not satisfy 0<=C<=2M I")
    if M == 0:
        # Exact PSD and cap checks imply C=0, so no Newton step or division
        # by a zero iteration count is required.
        return m_scale(Fraction(0), eye()), {
            "formal_operator_error_bound": "0 < q",
            "target_q": fraction_text(q), "total_steps": 0,
            "input_psd_and_cap_certified_exactly": True,
            "repair_origin": "c07_s01 owned-copy zero-input repair; underlying primitive c07_l07",
        }
    alpha = (q / 4) ** 2
    L = 2 * M + alpha
    gamma_bits = 0
    while Fraction(1, 1 << gamma_bits) > q / 4:
        gamma_bits += 1
    gamma = ceil_sqrt_fraction(L, gamma_bits)
    # gamma>=sqrt(L), while the dyadic overshoot is <=q/4<=sqrt(L), hence
    # gamma<=2sqrt(L). This avoids an eigenvalue or spectral-gap computation.
    k0, k1, local_budget, round_bits = newton_schedule(M, q, gamma)
    D = m_add(C, m_scale(alpha, eye()))
    X = m_scale(gamma, eye())
    for _ in range(k0 + k1):
        Xi = inv(X)
        F = m_add(m_scale(Fraction(1, 2), X),
                  m_scale(Fraction(1, 4), m_add(m_mul(D, Xi), m_mul(Xi, D))))
        X = round_symmetric(F, round_bits)
        if not leading_minors_positive(X):
            raise AssertionError("guarded iterate lost positive definiteness")
    return X, {
        "formal_operator_error_bound": "33q/64 < q",
        "target_q": fraction_text(q), "alpha": fraction_text(alpha),
        "gamma": fraction_text(gamma), "warmup_steps": k0,
        "quadratic_steps": k1, "total_steps": k0 + k1,
        "local_rounding_budget": fraction_text(local_budget),
        "rounding_grid_bits": round_bits,
        "max_entry_rounding": fraction_text(Fraction(1, 2 * (1 << round_bits))),
        "norm_charge": "3x3 Frobenius bound: op norm per rounding <= 3/(2*2^bits)",
        "input_psd_and_cap_certified_exactly": True,
    }


def mat_text(A: Matrix) -> list[list[str]]:
    return [[fraction_text(x) for x in row] for row in A]


def rotated_diag(values: Iterable[Fraction]) -> Matrix:
    vals = list(map(Fraction, values))
    R = [[Fraction(3, 5), Fraction(-4, 5), Fraction(0)],
         [Fraction(4, 5), Fraction(3, 5), Fraction(0)],
         [Fraction(0), Fraction(0), Fraction(1)]]
    return m_mul(m_mul(R, [[vals[0], 0, 0], [0, vals[1], 0], [0, 0, vals[2]]]),
                 [[R[j][i] for j in range(3)] for i in range(3)])


def run_fixtures() -> dict:
    M = Fraction(1, 10)
    B = Fraction(1, 5)
    sector_cases = [
        (1, Fraction(199, 100), Fraction(1, 10)),  # close to t0=0
        (2, Fraction(14, 5), Fraction(1, 5)),      # near 2*sqrt(2) boundary
        (8, M, B), (64, M, B),
    ]
    sector = [sector_certificate(N, m, b, 128) for N, m, b in sector_cases]
    rejected = []
    for N, m in ((1, Fraction(2)), (2, Fraction(283, 100))):
        try:
            sector_certificate(N, m, B)
        except ValueError as exc:
            rejected.append({"N": N, "M": fraction_text(m), "reason": str(exc)})
        else:
            raise AssertionError("boundary/excluded t0 fixture was admitted")
    zero_M = sector_certificate(8, Fraction(0), B, 96)
    assert zero_M["certificate"]["hi"] == "0/1"

    sqrt_cases = []
    matrices = [
        ("zero_matrix", [[Fraction(0) for _ in range(3)] for _ in range(3)], Fraction(1, 1 << 10)),
        ("rank_deficient_rotated_tiny_eigenvalue",
         rotated_diag([Fraction(0), Fraction(1, 10**40), Fraction(1, 5)]), Fraction(1, 1 << 12)),
        ("repeated_eigenvalue", [[Fraction(1, 10) if i == j else Fraction(0)
                                  for j in range(3)] for i in range(3)], Fraction(1, 1 << 12)),
    ]
    for name, C, q in matrices:
        X, cert = sqrt_psd3_guarded(C, M, q)
        assert leading_minors_positive(X)
        row = {"name": name, "C": mat_text(C), "X": mat_text(X), **cert}
        if name == "zero_matrix":
            frob2 = sum((x * x for r in X for x in r), Fraction(0))
            assert frob2 < q * q  # exact rational consequence for C=0
            row["exact_fixture_check"] = "sum_ij X_ij^2 < q^2; C=0"
        else:
            row["exact_fixture_check"] = "exact PSD/cap checks; all rounded iterates exactly positive definite"
        sqrt_cases.append(row)
    bad_psd = rotated_diag([Fraction(-1, 1 << 200), Fraction(1, 10), Fraction(1, 5)])
    try:
        sqrt_psd3_guarded(bad_psd, M, Fraction(1, 1 << 12))
    except ValueError as exc:
        psd_rejection = str(exc)
    else:
        raise AssertionError("tiny negative eigenvalue fixture was accepted")
    bad_cap = [[Fraction(200001, 10**6) if i == j else Fraction(0)
                for j in range(3)] for i in range(3)]
    try:
        sqrt_psd3_guarded(bad_cap, M, Fraction(1, 1 << 12))
    except ValueError as exc:
        cap_rejection = str(exc)
    else:
        raise AssertionError("out-of-cap fixture was accepted")
    return {
        "scope": "Exact rational input checks and outward-dyadic certificate generation; no hardware preparation.",
        "sector_certificates": sector,
        "sector_rejections": rejected,
        "zero_M_identity": zero_M,
        "square_root_fixtures": sqrt_cases,
        "square_root_rejections": {"negative_eigenvalue_minus_2^-200": psd_rejection,
                                    "eigenvalue_above_2M": cap_rejection},
        "limitations": ["The finite-N expression certifies the stated separability bound, not optimality.",
                        "Square-root error is certified by the written perturbation proof; fixture checks exercise the guards.",
                        "No local quantum gate compiler, physical execution, or external priority review is supplied."],
    }


if __name__ == "__main__":
    out = run_fixtures()
    target = ROOT / "spin_certificates_fixtures.json"
    target.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    print(f"Saved {target}")
