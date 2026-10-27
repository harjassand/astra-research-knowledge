"""Finite checks of the comparator's alternating-core repair, not FGP execution.

Python 3, standard library only. Matrices are lists of integer-encoded rows.
The prior Fomin--Golovach--Panolan approximation algorithm is NOT implemented.
"""
import json
import math
from pathlib import Path


def row_basis(rows):
    basis = {}
    indices = []
    for i, row in enumerate(rows):
        v = row
        while v:
            p = v.bit_length() - 1
            if p in basis:
                v ^= basis[p]
            else:
                basis[p] = v
                indices.append(i)
                break
    return indices


def rank(rows):
    return len(row_basis(rows))


def transpose(rows):
    n = len(rows)
    return [sum(((rows[j] >> i) & 1) << j for j in range(n)) for i in range(n)]


def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]


def weight(rows):
    return sum(row.bit_count() for row in rows)


def restrict(rows, indices):
    return [sum(((rows[i] >> j) & 1) << p for p, j in enumerate(indices))
            for i in indices]


def alternating(rows):
    return rows == transpose(rows) and all(not ((row >> i) & 1)
                                           for i, row in enumerate(rows))


def symmetric_matrices(n, zero_diagonal=False):
    positions = [(i, j) for i in range(n) for j in range(i if not zero_diagonal else i + 1, n)]
    for bits in range(1 << len(positions)):
        rows = [0] * n
        for p, (i, j) in enumerate(positions):
            if (bits >> p) & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
        yield rows


def support_cover(d, delta):
    """Cover support of an alternating matrix by heavy vertices and basis supports."""
    n = len(d)
    h = {i for i in range(n) if d[i].bit_count() > delta}
    light = [i for i in range(n) if i not in h]
    dl = restrict(d, light)
    basis = row_basis(dl)
    neighbors = 0
    for i in basis:
        neighbors |= dl[i]
    j = {light[p] for p in range(len(light)) if (neighbors >> p) & 1}
    cover = h | j
    remaining = [i for i in range(n) if i not in cover]
    assert not weight(restrict(d, remaining))
    edges = weight(d) // 2
    assert len(h) * (delta + 1) <= 2 * edges
    assert len(j) <= rank(dl) * delta
    return cover


def repair(x, b):
    n = len(x)
    d = xor(x, transpose(x))
    k = weight(xor(x, b))
    t = rank(x)
    assert alternating(d)
    assert rank(d) <= 2 * t
    assert weight(d) // 2 <= k
    delta = max(1, math.isqrt(k // max(t, 1)))
    e0 = support_cover(d, delta)
    diagonal = {i for i in range(n) if (x[i] >> i) & 1}
    e = e0 | diagonal
    remaining = [i for i in range(n) if i not in e]
    xr = restrict(x, remaining)
    br = restrict(b, remaining)
    assert alternating(xr)
    assert rank(xr) <= t
    assert weight(xor(xr, br)) <= k
    return remaining


def main():
    diagonal_checks = 0
    cover_checks = 0
    promised_repairs = 0
    nonempty_cores = 0
    for n in range(1, 5):
        for y in symmetric_matrices(n):
            d = sum((y[i] >> i) & 1 for i in range(n))
            assert d * d <= rank(y) * weight(y)
            diagonal_checks += 1
        for d in symmetric_matrices(n, zero_diagonal=True):
            for delta in range(1, n + 1):
                support_cover(d, delta)
                cover_checks += 1

    # Exhaust all n<=3 alternating hidden A, sparse symmetric errors S, and
    # arbitrary binary X that obey the common rank cap and error budget.
    for n in range(1, 4):
        alts = list(symmetric_matrices(n, zero_diagonal=True))
        for a in alts:
            for s in alts:
                b = xor(a, s)
                m = weight(s) // 2
                for bits in range(1 << (n * n)):
                    x = [(bits >> (i * n)) & ((1 << n) - 1) for i in range(n)]
                    k = weight(xor(x, b))
                    if k > 2 * m:
                        continue
                    r = max(rank(a), rank(x))
                    y = xor(x, a)
                    diagonal_count = sum((x[i] >> i) & 1 for i in range(n))
                    # X+A need not be symmetric globally. The diagonal estimate
                    # is applied after making X symmetric, where A stays alternating.
                    d = xor(x, transpose(x))
                    delta = max(1, math.isqrt(k // max(rank(x), 1)))
                    e0 = support_cover(d, delta)
                    light = [i for i in range(n) if i not in e0]
                    yl = restrict(y, light)
                    assert yl == transpose(yl)
                    diagonal_count_l = sum((yl[i] >> i) & 1 for i in range(len(light)))
                    assert diagonal_count_l ** 2 <= rank(yl) * weight(yl) <= 8 * r * m
                    remaining = repair(x, b)
                    assert weight(xor(restrict(x, remaining), restrict(b, remaining))) // 2 <= m
                    promised_repairs += 1
                    nonempty_cores += bool(remaining)
    result = {
        "scope": "Finite algebra checks of an elementary alternating-core repair; not execution of the cited FGP algorithm",
        "symmetric_diagonal_inequalities": diagonal_checks,
        "threshold_row_basis_covers": cover_checks,
        "exhaustive_promised_repairs_n_le_3": promised_repairs,
        "repairs_retaining_a_nonempty_core": nonempty_cores,
        "passed": True,
    }
    path = Path(__file__).with_name("mixed_interface_prior_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
