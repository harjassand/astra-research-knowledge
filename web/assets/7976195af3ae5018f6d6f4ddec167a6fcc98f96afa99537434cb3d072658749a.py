#!/usr/bin/env python3
"""Exhaustive F_2 matrix-code orbit search for T21.

Enumerates 2-dimensional subspaces of M_2(F_2) under left-right equivalence
and compares simple local signatures.  All arithmetic is exact over F_2.
"""
from itertools import combinations


def mat_mul(a, b):
    out = 0
    for i in range(2):
        for j in range(2):
            bit = 0
            for k in range(2):
                bit ^= ((a >> (2 * i + k)) & 1) & ((b >> (2 * k + j)) & 1)
            out |= bit << (2 * i + j)
    return out


def mat_add(a, b):
    return a ^ b


def det(a):
    return ((a >> 0) & 1) * ((a >> 3) & 1) ^ (((a >> 1) & 1) * ((a >> 2) & 1))


def inv(a):
    assert det(a)
    # For 2x2 matrices over F_2, the adjugate equals the inverse when det=1.
    return (((a >> 3) & 1) << 0) | (((a >> 1) & 1) << 1) | (((a >> 2) & 1) << 2) | (((a >> 0) & 1) << 3)


GL2 = [a for a in range(16) if det(a)]


def span2(a, b):
    return tuple(sorted({0, a, b, a ^ b}))


def canonical_subspaces():
    ans = set()
    for a, b in combinations(range(1, 16), 2):
        if a != b:
            ans.add(span2(a, b))
    return sorted(ans)


def rank(a):
    if a == 0:
        return 0
    return 2 if det(a) else 1


def act(code, p, q):
    pi, qi = inv(p), inv(q)
    return tuple(sorted(mat_mul(mat_mul(p, a), qi) for a in code))


def orbit(code):
    return min(act(code, p, q) for p in GL2 for q in GL2)


def rref_rank(rows, ncols):
    rows = [x for x in rows if x]
    piv = 0
    for col in range(ncols):
        found = next((i for i in range(piv, len(rows)) if (rows[i] >> col) & 1), None)
        if found is None:
            continue
        rows[piv], rows[found] = rows[found], rows[piv]
        for i in range(len(rows)):
            if i != piv and ((rows[i] >> col) & 1):
                rows[i] ^= rows[piv]
        piv += 1
        if piv == len(rows):
            break
    return piv


def adjoint_dimension(code):
    # Variables are entries of X followed by entries of Y; impose XA=AY.
    eqs = []
    for a in code:
        for i in range(2):
            for j in range(2):
                row = 0
                for k in range(2):
                    # (X A)[i,j] coefficient of X[i,k]
                    row ^= ((a >> (2 * k + j)) & 1) << (2 * i + k)
                    # (A Y)[i,j] coefficient of Y[k,j]
                    row ^= ((a >> (2 * i + k)) & 1) << (4 + 2 * k + j)
                eqs.append(row)
    return 8 - rref_rank(eqs, 8)


def generated_algebra_dimension(code):
    # Compute the unital associative algebra spanned by products of generators.
    basis = {1 << 0, 1 << 3}  # identity matrix in the bit encoding
    basis.update(code)
    changed = True
    while changed:
        changed = False
        current = list(basis)
        for a in current:
            for b in current:
                c = mat_mul(a, b)
                if c not in basis:
                    # Add c only if it increases the F_2-span.
                    old = rref_rank(list(basis), 4)
                    new = rref_rank(list(basis) + [c], 4)
                    if new > old:
                        basis.add(c)
                        changed = True
    return rref_rank(list(basis), 4)


def signature(code):
    counts = tuple(sum(rank(a) == r for a in code) for r in range(3))
    # The distribution of determinant-zero elements is equivalent to rank counts here.
    return counts, adjoint_dimension(code), generated_algebra_dimension(code)


def main():
    codes = canonical_subspaces()
    reps = {}
    for code in codes:
        reps.setdefault(orbit(code), code)
    buckets = {}
    for rep in reps:
        buckets.setdefault(signature(rep), []).append(rep)
    print(f"2D subspaces: {len(codes)}; left-right orbits: {len(reps)}")
    print("signature buckets with multiple orbits:")
    found = 0
    for sig, orbit_reps in sorted(buckets.items(), key=lambda x: (x[0], x[1])):
        if len(orbit_reps) > 1:
            print(f"  {sig}: {orbit_reps}")
            found += 1
    if not found:
        print("  none")


if __name__ == "__main__":
    main()
