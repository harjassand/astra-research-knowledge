"""Exact integer check of the octonionic Spin(9) grade-three moments.

The basis is 1,e1,...,e7 and the oriented Fano triples are the ones listed
in pure_orbits.md.  This independently checks the real symmetric Cl_9 model,
the two grade-three coefficient counts, and the resulting s3 formula.
"""

from itertools import combinations

N = 16


def zero(n=N):
    return [[0 for _ in range(n)] for _ in range(n)]


def identity(n=8):
    a = zero(n)
    for i in range(n):
        a[i][i] = 1
    return a


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b, c=1):
    return [[a[i][j] + c * b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def octonion_left_multiplications():
    # Each oriented triple (a,b,c) means e_a e_b=e_c, e_b e_c=e_a,
    # e_c e_a=e_b; reversing an ordered pair changes the sign.
    triples = [(1, 2, 3), (1, 4, 5), (1, 7, 6), (2, 4, 6),
               (2, 5, 7), (3, 4, 7), (3, 6, 5)]
    table = {}
    for a, b, c in triples:
        for i, j, k in ((a, b, c), (b, c, a), (c, a, b)):
            table[(i, j)] = (1, k)
            table[(j, i)] = (-1, k)
    out = []
    for a in range(8):
        L = zero(8)
        for b in range(8):
            if a == 0:
                L[b][b] = 1
            elif b == 0:
                L[a][0] = 1
            elif a == b:
                L[0][b] = -1
            else:
                sign, c = table[(a, b)]
                L[c][b] = sign
        out.append(L)
    return out


def gamma_model():
    L = octonion_left_multiplications()
    gammas = []
    for a in range(8):
        # Gamma_a(z0,z1)=(bar(a) z1, a z0).
        bar_sign = 1 if a == 0 else -1
        G = zero()
        for i in range(8):
            for j in range(8):
                G[i][8 + j] = bar_sign * L[a][i][j]
                G[8 + i][j] = L[a][i][j]
        gammas.append(G)
    G8 = zero()
    for i in range(8):
        G8[i][i] = 1
        G8[8 + i][8 + i] = -1
    gammas.append(G8)
    return gammas


def main():
    gamma = gamma_model()
    I = zero()
    for i in range(N):
        I[i][i] = 1
    for i, Gi in enumerate(gamma):
        assert transpose(Gi) == Gi, ("not symmetric", i)
        for j, Gj in enumerate(gamma):
            product = matmul(Gi, Gj)
            target = [[2 * I[a][b] if i == j else 0 for b in range(N)]
                      for a in range(N)]
            assert add(product, matmul(Gj, Gi)) == target, ("Clifford", i, j)

    x = 0       # (1,0) in O + O
    y7 = 1      # (e1,0)
    y8 = 8      # (0,1)
    got7, got8 = [], []
    for A in combinations(range(9), 3):
        P = I
        for a in A:
            P = matmul(P, gamma[a])
        c7, c8 = P[x][y7], P[x][y8]
        if c7:
            got7.append((A, c7))
        if c8:
            got8.append((A, c8))

    expected7 = {(0, 1, 8), (2, 3, 8), (4, 5, 8), (6, 7, 8)}
    expected8 = {(1, 2, 3), (1, 4, 5), (1, 6, 7), (2, 4, 6),
                 (2, 5, 7), (3, 4, 7), (3, 5, 6)}
    assert {A for A, _ in got7} == expected7, got7
    assert {A for A, _ in got8} == expected8, got8
    assert all(abs(v) == 1 for _, v in got7 + got8)
    print("PASS: exact real symmetric Cl_9 model; 9 squares and 36 cross-anticommutators")
    print("y7 grade-3 nonzero sets:", sorted(A for A, _ in got7))
    print("y8 grade-3 nonzero sets:", sorted(A for A, _ in got8))
    print("B3 vertical=4, horizontal=7; s3=(1-p)(7-3t)")


if __name__ == "__main__":
    main()
