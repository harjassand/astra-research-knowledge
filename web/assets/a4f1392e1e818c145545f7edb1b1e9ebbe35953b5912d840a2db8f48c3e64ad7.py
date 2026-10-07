"""Exact small-instance diagnostic for ordinary DPP leverage vs hard-pair holes.

For rational orthogonal F, V=[I,F^T] has every column leverage 1/2.
Compute f(U)=sum_{I subset R, |I|=|R|/2}|det F[I,R\\I]|^2,
R=[n]\\U, and its two-hole ratios. This is a bounded falsification probe,
not an asymptotic lower bound or a proof of hardness.
"""
from fractions import Fraction
from itertools import combinations, product
from sympy import Matrix


def perm_matrix(perm):
    n = len(perm)
    return Matrix(n, n, lambda i, j: int(perm[i] == j))


def block_cycle_rotation(u):
    u = Fraction(u)
    den = 1 + u * u
    c, s = (1 - u * u) / den, 2 * u / den
    P = perm_matrix([1, 2, 0])
    top = c * P
    top = top.row_join(-s * P)
    bot = (s * P).row_join(c * P)
    return top.col_join(bot)


def rotation(u):
    u = Fraction(u)
    den = 1 + u * u
    c, s = (1 - u * u) / den, 2 * u / den
    return Matrix([[c, -s], [s, c]])


def two_block_weak(u):
    strong = Matrix([[0, -1], [1, 0]])
    weak = rotation(u)
    zero = Matrix.zeros(2, 2)
    return strong.row_join(zero).col_join(zero.row_join(weak))


def direct_sum(A, B):
    z_ab = Matrix.zeros(A.rows, B.cols)
    z_ba = Matrix.zeros(B.rows, A.cols)
    return A.row_join(z_ab).col_join(z_ba.row_join(B))


def rational_givens(n, i, j, u):
    u = Fraction(u)
    den = 1 + u * u
    c, s = (1 - u * u) / den, 2 * u / den
    M = Matrix.eye(n)
    M[i, i], M[i, j] = c, -s
    M[j, i], M[j, j] = s, c
    return M


def hole_partition(F, holes):
    n = F.rows
    rows = [i for i in range(n) if i not in holes]
    k = len(rows) // 2
    total = Fraction(0)
    for I in combinations(rows, k):
        J = [j for j in rows if j not in I]
        d = F.extract(I, J).det(method="domain-ge")
        total += Fraction(d) ** 2
    return total


def profile(name, F):
    n = F.rows
    assert F * F.T == Matrix.eye(n), name
    z0 = hole_partition(F, ())
    pairs = {(i, j): hole_partition(F, (i, j)) / z0
             for i, j in combinations(range(n), 2)}
    rowmax = [max(pairs[tuple(sorted((i, j)))]
                  for j in range(n) if j != i) for i in range(n)]
    return {
        "name": name,
        "n": n,
        "partition": str(z0),
        "all_column_leverages": "1/2",
        "g_ij": {f"{i},{j}": str(v) for (i, j), v in pairs.items()},
        "rowmax": [str(x) for x in rowmax],
        "rowmax_min": str(min(rowmax)),
        "rowmax_max": str(max(rowmax)),
    }


def parity_sign_diagnostic(F):
    """Exact Rademacher/Fourier filter for even occupancy of every pair."""
    n = F.rows
    A = Matrix.eye(n).row_join(F.T)
    values = []
    for signs in product((-1, 1), repeat=n):
        D = Matrix.diag(*(list(signs) + list(signs)))
        values.append((A * D * A.T).det(method="domain-ge"))
    mean = sum(values) / (2**n)
    second = sum(x * x for x in values) / (2**n)
    partition = hole_partition(F, ())
    assert Fraction(mean) == partition
    return {
        "hard_partition": str(partition),
        "sign_sum_mean": str(mean),
        "sign_sum_abs_over_signed": str(sum(abs(x) for x in values) / abs(sum(values))),
        "uniform_sign_rms_over_mean_squared": str(second / (mean * mean)),
        "signed_determinants": [str(x) for x in values],
    }


def hard_weight_spectrum(F):
    n = F.rows
    vals = set()
    for I in combinations(range(n), n // 2):
        J = [j for j in range(n) if j not in I]
        d = F.extract(I, J).det(method="domain-ge")
        if d:
            vals.add(str(Fraction(d) ** 2))
    return sorted(vals, key=lambda x: Fraction(x))


def hole_support_signature(F):
    n = F.rows
    return tuple((i, j) for i, j in combinations(range(n), 2)
                 if hole_partition(F, (i, j)) > 0)


if __name__ == "__main__":
    n = 6
    cyc = perm_matrix([1, 2, 3, 4, 5, 0])
    rot = block_cycle_rotation(Fraction(1, 2))
    g1 = rational_givens(n, 0, 1, Fraction(1, 2))
    g2 = rational_givens(n, 2, 4, Fraction(2, 3))
    g3 = rational_givens(n, 1, 5, Fraction(1, 3))
    denseish = g3 * g2 * g1 * cyc
    for M in (cyc, rot, denseish):
        print(profile({id(cyc): "six_cycle", id(rot): "block_rotation", id(denseish): "rotated_cycle"}[id(M)], M))
    weak_profiles = []
    for bits in (2, 6, 10):
        u = Fraction(1, 2**bits)
        M = two_block_weak(u)
        weak_profiles.append((hole_support_signature(M), profile(f"two_block_weak_2^-{bits}", M)))
        print(weak_profiles[-1][1])
        print({"sign_diagnostic": f"two_block_weak_2^-{bits}", **parity_sign_diagnostic(M)})
    assert all(sig == weak_profiles[0][0] for sig, _ in weak_profiles)
    print({"weak_block_support_constant_across_bits": list(weak_profiles[0][0])})
    core = block_cycle_rotation(Fraction(1, 2))
    mixed = direct_sum(core, rotation(Fraction(1, 2**6)))
    print({"name": "nonconstant_weight_core_plus_weak_block",
           "core_nonzero_minor_weight_spectrum": hard_weight_spectrum(core),
           "mixed_nonzero_minor_weight_spectrum": hard_weight_spectrum(mixed),
           **profile("mixed", mixed)})
