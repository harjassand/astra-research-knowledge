#!/usr/bin/env python3
"""Finite exact diagnostic for a cost-explosive #PM encoding in c_k.

This checks K4 only. The theorem and bit-cost analysis are in revisions/.
"""
from itertools import combinations, permutations
from math import comb, factorial


def det_int(A):
    n = len(A)
    ans = 0
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = (-1 if inv % 2 else 1)
        for i in range(n):
            term *= A[i][p[i]]
        ans += term
    return ans


def balanced_base_coefficients(value, base, length):
    """Recover signed coefficients a_e with |a_e| < base/2 from sum a_e base^e."""
    coeffs = []
    z = value
    for _ in range(length):
        r = z % base
        z //= base
        if 2 * r > base:
            coeffs.append(r - base)
            z += 1
        else:
            coeffs.append(r)
    assert z == 0, "the supplied exponent range was too short"
    return coeffs


def perfect_matching_count(vertices, edges):
    count = 0
    for chosen in combinations(edges, len(vertices) // 2):
        used = set()
        good = True
        for u, v in chosen:
            if u in used or v in used:
                good = False
                break
            used.add(u)
            used.add(v)
        if good and len(used) == len(vertices):
            count += 1
    return count


def check_k4():
    vertices = tuple(range(4))
    edges = tuple((u, v) for u in vertices for v in vertices if u < v)
    k = len(vertices) // 2
    m = len(edges)
    term_bound = comb(2 * k, k) * factorial(k) ** 2
    base = 2 * term_bound + 1
    F = [[0] * len(vertices) for _ in vertices]
    for e, (u, v) in enumerate(edges):
        weight = base ** (3 ** e)
        F[u][v] = weight
        F[v][u] = weight

    total = 0
    for I in combinations(vertices, k):
        Iset = set(I)
        J = tuple(v for v in vertices if v not in Iset)
        total += det_int([[F[i][j] for j in J] for i in I]) ** 2

    # Every product of two determinant monomials has base-3 exponent digits 0,1,2.
    # Hence all possible exponents lie in [0, 3^m - 1].
    coeffs = balanced_base_coefficients(total, base, 3 ** m)
    decoded = 0
    even_slots = 0
    for exponent, coefficient in enumerate(coeffs):
        assert abs(coefficient) <= term_bound
        digits = []
        q = exponent
        for _ in range(m):
            digits.append(q % 3)
            q //= 3
        if all(d in (0, 2) for d in digits) and sum(d == 2 for d in digits) == k:
            even_slots += 1
            selected = [edges[e] for e, d in enumerate(digits) if d == 2]
            used = set()
            is_pm = True
            for u, v in selected:
                if u in used or v in used:
                    is_pm = False
                    break
                used.update((u, v))
            is_pm = is_pm and len(used) == len(vertices)
            assert coefficient == (2 ** k if is_pm else 0), (exponent, coefficient)
            decoded += coefficient

    pm_count = perfect_matching_count(vertices, edges)
    assert pm_count == 3
    assert decoded == (2 ** k) * pm_count == 12
    return {
        "graph": "K4",
        "vertices": len(vertices),
        "edges": m,
        "k": k,
        "term_bound_T": term_bound,
        "balanced_base_B": base,
        "largest_entry_bit_length": max(x.bit_length() for row in F for x in row),
        "c_k_bit_length": total.bit_length(),
        "decoded_even_slots_checked": even_slots,
        "decoded_value": decoded,
        "2^k_times_perfect_matchings": (2 ** k) * pm_count,
        "result": "PASS (finite exact diagnostic only)",
    }


if __name__ == "__main__":
    print(check_k4())
