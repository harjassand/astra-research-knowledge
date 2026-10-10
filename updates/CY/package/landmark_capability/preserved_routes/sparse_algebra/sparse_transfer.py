"""Exact huge-index scalar transfer queries over a prime field.

Given sparse A and vectors u,v over F_p, return u^T A^n v.  The code
deterministically discovers a vector Krylov relation, reduces it to the
minimal recurrence of the scalar sequence, then uses binary polynomial
reduction.  This is a compact reference implementation, not an optimized
finite-field package.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass
class SparseMatrix:
    n: int
    p: int
    rows: list[list[tuple[int, int]]]

    @classmethod
    def from_entries(
        cls, n: int, p: int, entries: Iterable[tuple[int, int, int]]
    ) -> "SparseMatrix":
        rows: list[dict[int, int]] = [dict() for _ in range(n)]
        for i, j, value in entries:
            if not (0 <= i < n and 0 <= j < n):
                raise ValueError("matrix index out of range")
            value %= p
            rows[i][j] = (rows[i].get(j, 0) + value) % p
            if rows[i][j] == 0:
                del rows[i][j]
        return cls(n, p, [list(row.items()) for row in rows])

    def matvec(self, x: Sequence[int]) -> list[int]:
        if len(x) != self.n:
            raise ValueError("vector dimension mismatch")
        p = self.p
        return [sum(a * x[j] for j, a in row) % p for row in self.rows]

    def transpose(self) -> "SparseMatrix":
        entries = ((j, i, a) for i, row in enumerate(self.rows) for j, a in row)
        return SparseMatrix.from_entries(self.n, self.p, entries)


def _inner(u: Sequence[int], v: Sequence[int], p: int) -> int:
    return sum(a * b for a, b in zip(u, v)) % p


class _KrylovTracker:
    """Incremental first-dependence finder for one Krylov sequence."""

    def __init__(self, A: SparseMatrix, start: Sequence[int], observe: Sequence[int]):
        self.A = A
        self.p = A.p
        self.observe = [x % A.p for x in observe]
        self.x = [x % A.p for x in start]
        self.index = 0
        self.samples: list[int] = []
        self.basis: dict[int, tuple[list[int], list[int]]] = {}

    def step(self):
        """Consume the next vector; return its first-dependence relation, if any."""
        p = self.p
        j = self.index
        residual = self.x[:]
        representation = [0] * j + [1]
        for pivot in sorted(self.basis):
            bvec, brep = self.basis[pivot]
            factor = residual[pivot]
            if factor:
                residual = [(r - factor * b) % p for r, b in zip(residual, bvec)]
                for k, value in enumerate(brep):
                    representation[k] = (representation[k] - factor * value) % p
        pivot = next((i for i, value in enumerate(residual) if value), None)
        if pivot is None:
            return j, [(-representation[i]) % p for i in range(j)]
        inv = pow(residual[pivot], -1, p)
        residual = [(value * inv) % p for value in residual]
        representation = [(value * inv) % p for value in representation]
        self.basis[pivot] = (residual, representation)
        self.samples.append(_inner(self.observe, self.x, p))
        self.x = self.A.matvec(self.x)
        self.index += 1
        return None


def _berlekamp_massey(sequence: Sequence[int], p: int) -> list[int]:
    """Return C with C[0]=1 and sum_i C[i] s[n-i]=0 for all n >= len(C)-1."""
    C, B = [1], [1]
    L, shift, last_discrepancy = 0, 1, 1
    for n, value in enumerate(sequence):
        discrepancy = value % p
        for i in range(1, L + 1):
            if i < len(C):
                discrepancy = (discrepancy + C[i] * sequence[n - i]) % p
        if discrepancy == 0:
            shift += 1
            continue
        old_C = C[:]
        scale = discrepancy * pow(last_discrepancy, -1, p) % p
        needed = len(B) + shift
        if len(C) < needed:
            C.extend([0] * (needed - len(C)))
        for i, value_B in enumerate(B):
            C[i + shift] = (C[i + shift] - scale * value_B) % p
        if 2 * L <= n:
            L = n + 1 - L
            B = old_C
            last_discrepancy = discrepancy
            shift = 1
        else:
            shift += 1
    return C[: L + 1]


def _mul_mod_poly(a: Sequence[int], b: Sequence[int], q: Sequence[int], p: int):
    """Multiply modulo monic q (low-to-high coefficients), using O(d^2)."""
    d = len(q) - 1
    if d == 0:
        return []
    product = [0] * (2 * d - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    product[i + j] = (product[i + j] + ai * bj) % p
    for k in range(len(product) - 1, d - 1, -1):
        lead = product[k]
        if lead:
            for j in range(d):
                product[k - d + j] = (product[k - d + j] - lead * q[j]) % p
    return product[:d]


def _linear_recurrence_term(initial: Sequence[int], C: Sequence[int], n: int, p: int):
    """Evaluate a linearly recurrent sequence via x^n modulo its polynomial."""
    d = len(C) - 1
    if d == 0:
        return 0
    if n < d:
        return initial[n] % p
    # C[0] s_k + C[1] s_{k-1} + ... + C[d] s_{k-d} = 0.
    # Thus q(x)=x^d+C[1]x^(d-1)+...+C[d].
    q = list(reversed(C))
    result = [0] * d
    result[0] = 1
    base = [0] * d
    if d == 1:
        base[0] = (-q[0]) % p
    else:
        base[1] = 1
    exponent = n
    while exponent:
        if exponent & 1:
            result = _mul_mod_poly(result, base, q, p)
        exponent >>= 1
        if exponent:
            base = _mul_mod_poly(base, base, q, p)
    return sum(a * b for a, b in zip(result, initial)) % p


def transfer_term(A: SparseMatrix, u: Sequence[int], v: Sequence[int], n: int):
    """Compute u^T A^n v exactly in F_p; return value and acquired recurrence.

    The recurrence is learned from A and both vectors.  The algorithm stops
    when either the forward or transpose-side Krylov sequence first becomes
    dependent.
    """
    if len(u) != A.n or len(v) != A.n:
        raise ValueError("vector dimension mismatch")
    if n < 0:
        raise ValueError("n must be nonnegative")
    u = [value % A.p for value in u]
    v = [value % A.p for value in v]
    # Interleave the reachable sequence from v with the observable sequence
    # from u under A^T.  Either first dependence bounds the scalar recurrence;
    # stopping at the first one gives d=min(d_v,d_u) up to one interleaved
    # iteration, with no supplied recurrence or random projection.
    forward = _KrylovTracker(A, v, u)
    reverse = _KrylovTracker(A.transpose(), u, v)
    tracker = None
    relation = None
    while relation is None:
        relation = forward.step()
        if relation is not None:
            tracker = forward
            break
        relation = reverse.step()
        if relation is not None:
            tracker = reverse
            break
    d, vector_recurrence = relation
    if d == 0:
        return 0, [1]

    # The vector relation gives an order-d recurrence.  Generate 2d scalar
    # terms so Berlekamp-Massey can recover the minimal scalar recurrence.
    scalar = tracker.samples[:]
    a = vector_recurrence
    for _ in range(d):
        scalar.append(sum(a[i] * scalar[-d + i] for i in range(d)) % A.p)
    C = _berlekamp_massey(scalar, A.p)
    return _linear_recurrence_term(scalar, C, n, A.p), C


def direct_term(A: SparseMatrix, u: Sequence[int], v: Sequence[int], n: int) -> int:
    """Reference O(n*m) evaluator used only by finite checks."""
    x = [value % A.p for value in v]
    for _ in range(n):
        x = A.matvec(x)
    return _inner(u, x, A.p)

