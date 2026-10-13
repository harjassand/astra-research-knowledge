"""Exact common-radical certificate and sampler for quadratic F_2 maps.

Representation of a Boolean quadratic q:
    (constant_bit, linear_mask, quadratic_pairs)
where each pair (j, ell) denotes x_j*x_ell, 0 <= j < ell < n.
All vectors are packed into Python integers, with coordinate j in bit j.
"""

from __future__ import annotations

import random
from typing import Iterable, Sequence

Form = tuple[int, int, tuple[tuple[int, int], ...]]


def q_eval(n: int, q: Form, x: int) -> int:
    constant, linear, pairs = q
    value = constant ^ ((linear & x).bit_count() & 1)
    for j, ell in pairs:
        value ^= ((x >> j) & 1) & ((x >> ell) & 1)
    return value


def q_normalized(n: int, q: Form, x: int) -> int:
    """Return Q(x)=q(x)+q(0), so Q(0)=0."""
    return q_eval(n, q, x) ^ q[0]


def polar_rows(n: int, q: Form) -> list[int]:
    """Rows of the matrix M such that B_q(x,y)=x^T M y over F_2."""
    rows = [0] * n
    for j, ell in q[2]:
        rows[j] |= 1 << ell
        rows[ell] |= 1 << j
    return rows


def bilinear(n: int, q: Form, x: int, y: int) -> int:
    return (sum(((row & x).bit_count() & 1) * ((y >> j) & 1)
                for j, row in enumerate(polar_rows(n, q))) & 1)


def rref(rows: Iterable[int], nvars: int) -> tuple[list[int], list[int]]:
    """Reduced row echelon form over F_2, represented as integer bit rows."""
    a = [row & ((1 << nvars) - 1) for row in rows if row]
    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(nvars):
        found = next((i for i in range(pivot_row, len(a)) if (a[i] >> col) & 1), None)
        if found is None:
            continue
        a[pivot_row], a[found] = a[found], a[pivot_row]
        for i in range(len(a)):
            if i != pivot_row and ((a[i] >> col) & 1):
                a[i] ^= a[pivot_row]
        pivot_cols.append(col)
        pivot_row += 1
    return a[:pivot_row], pivot_cols


def nullspace_basis(rows: Iterable[int], nvars: int) -> list[int]:
    a, pivots = rref(rows, nvars)
    pivot_set = set(pivots)
    basis: list[int] = []
    for free in range(nvars):
        if free in pivot_set:
            continue
        v = 1 << free
        for i, pivot in enumerate(pivots):
            if (a[i] >> free) & 1:
                v |= 1 << pivot
        basis.append(v)
    return basis


def solve_gf2(rows: Sequence[int], rhs: int, nvars: int) -> int | None:
    """Solve rows*x=rhs over F_2, choosing free variables zero."""
    aug = [((row & ((1 << nvars) - 1)) | (((rhs >> i) & 1) << nvars))
           for i, row in enumerate(rows)]
    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(nvars):
        found = next((i for i in range(pivot_row, len(aug)) if (aug[i] >> col) & 1), None)
        if found is None:
            continue
        aug[pivot_row], aug[found] = aug[found], aug[pivot_row]
        for i in range(len(aug)):
            if i != pivot_row and ((aug[i] >> col) & 1):
                aug[i] ^= aug[pivot_row]
        pivot_cols.append(col)
        pivot_row += 1
    rhs_bit = 1 << nvars
    for row in aug:
        if not (row & ((1 << nvars) - 1)) and (row & rhs_bit):
            return None
    answer = 0
    for i, col in enumerate(pivot_cols):
        if (aug[i] & rhs_bit) >> nvars:
            answer |= 1 << col
    return answer


def output(n: int, forms: Sequence[Form], x: int) -> int:
    return sum(q_eval(n, q, x) << i for i, q in enumerate(forms))


def common_radical_basis(n: int, forms: Sequence[Form]) -> list[int]:
    rows = [row for q in forms for row in polar_rows(n, q)]
    return nullspace_basis(rows, n)


def common_radical_certificate(n: int, forms: Sequence[Form]) -> list[int] | None:
    """Return d_j with d_j in every rad(B_i), Q_i(d_j)=delta_ij, or None."""
    k = len(forms)
    r_basis = common_radical_basis(n, forms)
    # L columns are the k-bit images of the chosen common-radical basis.
    l_columns = [sum(q_normalized(n, q, v) << i for i, q in enumerate(forms))
                 for v in r_basis]
    # Solve L(coefficients)=e_j, one target basis vector at a time.
    equation_rows = [sum(((col >> i) & 1) << s for s, col in enumerate(l_columns))
                     for i in range(k)]
    cert: list[int] = []
    for j in range(k):
        coeffs = solve_gf2(equation_rows, 1 << j, len(r_basis))
        if coeffs is None:
            return None
        v = 0
        for s, r in enumerate(r_basis):
            if (coeffs >> s) & 1:
                v ^= r
        cert.append(v)
    return cert


def verify_certificate(n: int, forms: Sequence[Form], cert: Sequence[int]) -> bool:
    k = len(forms)
    if len(cert) != k:
        return False
    for i, q in enumerate(forms):
        rows = polar_rows(n, q)
        for j, v in enumerate(cert):
            if any((row & v).bit_count() & 1 for row in rows):
                return False
            if q_normalized(n, q, v) != (i == j):
                return False
    return True


def sample_fiber(n: int, forms: Sequence[Form], target: int,
                 cert: Sequence[int], rng: random.Random | None = None) -> int:
    """One-shot exact uniform sample from F^{-1}(target), given a valid cert."""
    if not verify_certificate(n, forms, cert):
        raise ValueError("invalid common-radical certificate")
    rng = rng or random.SystemRandom()
    x = rng.getrandbits(n)
    delta = target ^ output(n, forms, x)
    correction = 0
    for j, v in enumerate(cert):
        if (delta >> j) & 1:
            correction ^= v
    return x ^ correction


def balance_count(n: int, q: Form) -> int:
    return sum(q_eval(n, q, x) for x in range(1 << n))


def radical_balance_test(n: int, q: Form) -> bool:
    r = nullspace_basis(polar_rows(n, q), n)
    return any(q_normalized(n, q, v) for v in r)


def all_outputs(n: int, forms: Sequence[Form]) -> list[int]:
    return [output(n, forms, x) for x in range(1 << n)]


def combinations_are_balanced(n: int, forms: Sequence[Form]) -> bool:
    """Exact direct check of all nonzero output combinations, for small n,k."""
    k = len(forms)
    if k == 0:
        return True
    for mask in range(1, 1 << k):
        combined: list[Form] = []
        c = 0
        l = 0
        pair_coeffs: set[tuple[int, int]] = set()
        for i, q in enumerate(forms):
            if (mask >> i) & 1:
                c ^= q[0]
                l ^= q[1]
                for pair in q[2]:
                    if pair in pair_coeffs:
                        pair_coeffs.remove(pair)
                    else:
                        pair_coeffs.add(pair)
        qsum: Form = (c, l, tuple(sorted(pair_coeffs)))
        if balance_count(n, qsum) != (1 << (n - 1)):
            return False
    return True


def combine_forms(forms: Sequence[Form], mask: int) -> Form:
    """Return the XOR of coordinate forms selected by mask."""
    c = 0
    linear = 0
    pairs: set[tuple[int, int]] = set()
    for i, q in enumerate(forms):
        if (mask >> i) & 1:
            c ^= q[0]
            linear ^= q[1]
            for pair in q[2]:
                if pair in pairs:
                    pairs.remove(pair)
                else:
                    pairs.add(pair)
    return c, linear, tuple(sorted(pairs))


def vectorial_balanced_radical_test(n: int, forms: Sequence[Form]) -> bool:
    """Test equal-fiber condition by checking every nonzero component radical."""
    for mask in range(1, 1 << len(forms)):
        if not radical_balance_test(n, combine_forms(forms, mask)):
            return False
    return True

