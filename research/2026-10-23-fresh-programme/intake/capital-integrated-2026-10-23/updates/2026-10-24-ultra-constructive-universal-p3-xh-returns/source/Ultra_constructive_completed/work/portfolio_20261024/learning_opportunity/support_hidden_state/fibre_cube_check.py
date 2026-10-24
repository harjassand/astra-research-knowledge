#!/usr/bin/env python3
"""Exact, dependency-free checks for the bounded F_2 fibre-sampler audit."""

from itertools import product


def gf8_mul(x, y):
    # Bit i is the coefficient of alpha**i; alpha**3 = alpha + 1.
    out = 0
    for i in range(3):
        if (y >> i) & 1:
            out ^= x << i
    for i in range(5, 2, -1):
        if (out >> i) & 1:
            out ^= (1 << i) | (1 << (i - 2)) | (1 << (i - 3))
    return out & 7


def bits3(x):
    return tuple((x >> i) & 1 for i in range(3))


def cube_formula(a, b, c):
    return (a ^ b ^ c ^ (b & c), b ^ (a & b) ^ (a & c), c ^ (a & b))


def xor_vec(*xs):
    out = [0] * len(xs[0])
    for x in xs:
        out = [u ^ v for u, v in zip(out, x)]
    return tuple(out)


def polar(f, u, v):
    zero = f((0, 0, 0))
    return xor_vec(f(u), f(v), f(tuple(a ^ b for a, b in zip(u, v))), zero)


def rank_f2(rows):
    if not rows:
        return 0
    a = [list(row) for row in rows]
    nr, nc = len(a), len(a[0])
    r = 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(nr):
            if i != r and a[i][c]:
                a[i] = [x ^ y for x, y in zip(a[i], a[r])]
        r += 1
        if r == nr:
            break
    return r


def q_test(x):
    a, b, c = x
    return (a, b ^ (a & c), c)


def all_bits(n):
    return list(product((0, 1), repeat=n))


def check_fibre_sampler():
    xs = all_bits(3)
    assert len({q_test(x) for x in xs}) == 8
    # This fixture has a known affine coordinate and nonlinear quadratic term;
    # verify the exact equal-size feasible-core identity for every prefix.
    for t in range(1, 4):
        # The common radical of the prefix polar forms, by exhaustive search.
        L = []
        for v in xs:
            if all(
                all(polar(lambda x, i=i: (q_test(x)[i],), u, v) == (0,)
                    for u in xs)
                for i in range(t)
            ):
                L.append(v)
        # Compute r from |L|; the complementary core is represented by
        # lexicographically first representatives modulo L.
        assert len(L) in (1, 2, 4, 8)
        nL = len(L).bit_length() - 1
        r = 3 - nL
        cosets = []
        seen = set()
        for x in xs:
            if x in seen:
                continue
            coset = {tuple(a ^ b for a, b in zip(x, v)) for v in L}
            seen |= coset
            cosets.append(x)
        assert len(cosets) == 2**r
        # A(v)=F(v)+F(0), rank s is the rank of its truth-table image span.
        F0 = q_test((0, 0, 0))[:t]
        Avs = [tuple(a ^ b for a, b in zip(q_test(v)[:t], F0)) for v in L]
        # Rank of a linear map is log_2 of its image size.
        s = len(set(Avs)).bit_length() - 1
        for y in all_bits(t):
            full_fibre = [x for x in xs if q_test(x)[:t] == y]
            assert len(full_fibre) == 2 ** (3 - t)
            feasible = []
            per_core = []
            for z in cosets:
                Fz = q_test(z)[:t]
                sols = [v for v in L if tuple(a ^ b for a, b in zip(Avs[L.index(v)], Fz)) == y]
                # Above, Av(v) xor F(z) = y is the affine fibre equation.
                if sols:
                    feasible.append(z)
                    per_core.append(len(sols))
            assert per_core and len(set(per_core)) == 1
            assert per_core[0] == 2 ** (nL - s)
            assert len(feasible) == 2 ** (r + s - t)
            # Reconstruct the sampler support and ensure it is exactly the fibre.
            sampled_support = {
                tuple(a ^ b for a, b in zip(z, v))
                for z in feasible for v in L
                if tuple(a ^ b for a, b in zip(Avs[L.index(v)], q_test(z)[:t])) == y
            }
            assert sampled_support == set(full_fibre)
            assert len(sampled_support) == len(feasible) * per_core[0]
        assert r + s >= t


def check_f8_cube():
    cube_values = []
    for x in range(8):
        z3 = gf8_mul(gf8_mul(x, x), x)
        a, b, c = bits3(x)
        assert bits3(z3) == cube_formula(a, b, c)
        cube_values.append(z3)
    assert len(set(cube_values)) == 8  # gcd(3,7)=1, checked exhaustively too.

    basis = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    forms = [lambda x, i=i: (cube_formula(*x)[i],) for i in range(3)]
    # Pair order is (01,02,12); each row gives the upper-triangle coefficients
    # of one alternating polar form.
    polar_rows = []
    for f in forms:
        vals = [polar(f, basis[i], basis[j])[0]
                for i, j in ((0, 1), (0, 2), (1, 2))]
        polar_rows.append(vals)
    assert polar_rows == [[0, 0, 1], [1, 1, 0], [1, 0, 0]]
    assert rank_f2(polar_rows) == 3
    assert all(any(v for v in __import__("functools").reduce(
        lambda acc, item: [a ^ (item[0] & b) for a, b in zip(acc, item[1])],
        zip(lam, polar_rows), [0, 0, 0])) for lam in product((0, 1), repeat=3) if any(lam))
    # Common radical is zero: enumerate directly from the three polar forms.
    common_radical = []
    for v in all_bits(3):
        if all(polar(f, u, v) == (0,) for f in forms for u in all_bits(3)):
            common_radical.append(v)
    assert common_radical == [(0, 0, 0)]


def check_nonbijective_warning():
    # F(a,b)=ab has fibres of sizes 3 and 1, showing why Q's bijection promise
    # is needed for the power-of-two feasible-core count.
    vals = [a & b for a, b in all_bits(2)]
    assert vals.count(0) == 3 and vals.count(1) == 1


if __name__ == "__main__":
    check_fibre_sampler()
    check_f8_cube()
    check_nonbijective_warning()
    print("PASS: fibre identities, F8 cube polars, and non-bijection counterexample")
