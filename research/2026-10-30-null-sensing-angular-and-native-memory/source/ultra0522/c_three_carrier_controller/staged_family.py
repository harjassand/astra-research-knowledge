#!/usr/bin/env python3
"""Literal staged circuit's distinct-live-tag Kraus, stdlib exact rationals.

Tag names:0 original target,1/2 old other carriers,3 fresh source tag.
Basis: all six live tag arrangements times known M (dimension12).
No tag is exposed to the physical controller. This is an ANALYSIS
unravelling of discarded physical junk in the no-live-collision sector.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations

ARRANGEMENTS = tuple(permutations(range(3)))
WHERE = {p: i for i, p in enumerate(ARRANGEMENTS)}
DIM = 12


def permute_positions(labels, i, j):
    labels = list(labels)
    labels[i], labels[j] = labels[j], labels[i]
    return tuple(labels)


def paths(old):
    # (new M before H, source A, R, coefficient of a, coefficient of b)
    yield old, old, old, 0, 2
    yield old, 1 - old, 1 - old, 1, 1
    yield 1 - old, 1 - old, old, -1, 1


def linear_kraus():
    """Every entry is a pair(ca,cb), amplitude ca*a+cb*b.

    Kraus labels are(source logical A traced for the reduced tag walk,
    discarded known R, discarded physical tag). Logical data on a tag is
    not measured by the controller. Tracing it here commutes with future
    tag-only controlled permutations until a live-tag collision.
    """
    result = defaultdict(dict)
    for labels in ARRANGEMENTS:
        for old in (0, 1):
            col = 2 * WHERE[labels] + old
            for new, source, rr, ca, cb in paths(old):
                pp = labels + (3,)
                if old:
                    pp = permute_positions(pp, 0, 1)
                if new:
                    pp = permute_positions(pp, 0, 1)
                if rr:
                    pp = permute_positions(pp, 1, 3)
                if new:
                    pp = permute_positions(pp, 1, 2)
                discarded = pp[3]
                survivors = pp[:3]
                if discarded == 0:
                    rename = {x: x - 1 for x in (1, 2, 3)}
                else:
                    others = sorted(set(survivors) - {0})
                    assert len(others) == 2
                    rename = {0: 0, others[0]: 1, others[1]: 2}
                out = tuple(rename[x] for x in survivors)
                assert out in WHERE
                for final in (0, 1):
                    row = 2 * WHERE[out] + final
                    sign = -1 if new * final else 1
                    ij = (row, col)
                    a0, b0 = result[source, rr, discarded].get(ij, (F(0), F(0)))
                    # One sqrt2 from the port and one from final H.
                    result[source, rr, discarded][ij] = (a0 + F(sign * ca, 2), b0 + F(sign * cb, 2))
    return {label: {ij: ab for ij, ab in mat.items() if any(ab)}
            for label, mat in result.items()}


def qualify_symbolic_normalization(kraus=None):
    """Check sum K* K=(a^2+3b^2) I as an exact polynomial identity."""
    kraus = linear_kraus() if kraus is None else kraus
    gram = defaultdict(lambda: [F(0), F(0), F(0)])
    for mat in kraus.values():
        by_row = defaultdict(list)
        for (row, col), ab in mat.items():
            by_row[row].append((col, ab))
        for entries in by_row.values():
            for i, (ai, bi) in entries:
                for j, (aj, bj) in entries:
                    gram[i, j][0] += ai * aj
                    gram[i, j][1] += ai * bj + bi * aj
                    gram[i, j][2] += bi * bj
    for i in range(DIM):
        for j in range(DIM):
            assert gram[i, j] == ([F(1), 0, F(3)] if i == j else [0, 0, 0]), (i, j, gram[i, j])
    return True


def substitute(a, b, kraus=None):
    a, b = F(a), F(b)
    assert a * a + 3 * b * b == 1
    kraus = linear_kraus() if kraus is None else kraus
    return {label: {ij: x * a + y * b for ij, (x, y) in mat.items() if x * a + y * b}
            for label, mat in kraus.items()}


def dual_apply(kraus, matrix, *, survival=True):
    """S*(G)=sum K* G K, retaining all coherences, not population drift."""
    out = defaultdict(F)
    for label, mat in kraus.items():
        if survival and label[2] == 0:
            continue
        by_col = defaultdict(list)
        for (row, col), value in mat.items():
            by_col[col].append((row, value))
        for i, left in by_col.items():
            for j, right in by_col.items():
                val = sum(ci * matrix.get((u, v), 0) * cj
                          for u, ci in left for v, cj in right)
                if val:
                    out[i, j] += val
    return {ij: val for ij, val in out.items() if val}


def identity():
    return {(i, i): F(1) for i in range(DIM)}


def integer_common(kraus):
    from math import lcm
    den = 1
    for mat in kraus.values():
        for value in mat.values():
            den = lcm(den, value.denominator)
    return den, {label: {ij: int(v * den) for ij, v in mat.items()}
                 for label, mat in kraus.items()}


def symmetric_lyapunov_system(kraus):
    """Integer linear system for G-S*(G)=I on real symmetric G."""
    den, ints = integer_common(kraus)
    dim = DIM
    basis = [(i, j) for i in range(dim) for j in range(i, dim)]
    index = {ij: z for z, ij in enumerate(basis)}
    n = len(basis)
    system = [[0] * n for _ in range(n)]
    rhs = [0] * n
    square = den * den
    for z, (i, j) in enumerate(basis):
        system[z][z] = square
        rhs[z] = square if i == j else 0
    for label, mat in ints.items():
        if label[2] == 0:
            continue
        by_col = defaultdict(list)
        for (row, col), value in mat.items():
            by_col[col].append((row, value))
        for z, (i, j) in enumerate(basis):
            for u, ci in by_col[i]:
                for v, cj in by_col[j]:
                    system[z][index[min(u, v), max(u, v)]] -= ci * cj
    return basis, system, rhs, den


def solve_bareiss(matrix, rhs):
    """Self-contained fraction-free elimination, followed by rational backsolve."""
    n = len(rhs)
    aug = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    prev = 1
    largest_bits = 1
    swaps = 0
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if aug[i][k]), None)
        if pivot_row is None:
            raise ValueError(f"Singular Lyapunov system at pivot{k}")
        if pivot_row != k:
            aug[k], aug[pivot_row] = aug[pivot_row], aug[k]
            swaps += 1
        pivot = aug[k][k]
        for i in range(k + 1, n):
            entry = aug[i][k]
            for j in range(k + 1, n + 1):
                numerator = pivot * aug[i][j] - entry * aug[k][j]
                value, remainder = divmod(numerator, prev)
                assert remainder == 0
                aug[i][j] = value
                largest_bits = max(largest_bits, abs(value).bit_length())
            aug[i][k] = 0
        prev = pivot
    if not aug[-1][-2]:
        raise ValueError("Singular final Lyapunov pivot")
    solution = [F(0)] * n
    for i in range(n - 1, -1, -1):
        solution[i] = (F(aug[i][n]) - sum(aug[i][j] * solution[j] for j in range(i + 1, n))) / aug[i][i]
    return solution, {"dimension": n, "row_swaps": swaps,
                      "largest_fraction_free_integer_bits": largest_bits}


def exact_ldl(matrix):
    """Strict rational LDL without a numerical eigensolve."""
    n = DIM
    ll = [[F(0)] * n for _ in range(n)]
    dd = []
    for i in range(n):
        ll[i][i] = F(1)
        d = matrix.get((i, i), 0) - sum(ll[i][j] ** 2 * dd[j] for j in range(i))
        assert d > 0, (i, d)
        dd.append(d)
        for k in range(i + 1, n):
            ll[k][i] = (matrix.get((k, i), 0) - sum(ll[k][j] * ll[i][j] * dd[j] for j in range(i))) / d
    return dd
