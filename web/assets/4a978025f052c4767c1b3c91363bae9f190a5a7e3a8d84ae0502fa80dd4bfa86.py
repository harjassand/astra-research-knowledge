from itertools import combinations, product
from random import Random
from fractions import Fraction


def det(a):
    a = [list(map(int, row)) for row in a]
    n = len(a)
    if n == 0:
        return 1
    sign = 1
    prev = 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * p - a[i][k] * a[k][j]) // prev
        for i in range(k + 1, n):
            a[i][k] = 0
        prev = p
    return sign * a[n - 1][n - 1]


def hole_coeffs(F):
    n = len(F)
    allv = frozenset(range(n))
    ans = {}
    for rsize in range(0, n + 1, 2):
        for R0 in combinations(range(n), rsize):
            R = frozenset(R0)
            s = 0
            for I0 in combinations(R0, rsize // 2):
                I = frozenset(I0)
                J = tuple(sorted(R - I))
                I = tuple(sorted(I))
                s += det([[F[i][j] for j in J] for i in I]) ** 2
            U = allv - R
            ans[U] = s
    return ans


def rayleigh_coeff(a, n, i, j, x):
    # R(z)=sum_U (-1)^((n-|U|)/2) a_U z^U; x gives all variables except i,j
    vals = [0, 0, 0, 0]  # A,B,C,D in A+B zi+C zj+D zi zj
    for U, val in a.items():
        if i in U or j in U:
            continue
        deg = len(U)
        sg = -1 if ((n - deg) // 2) % 2 else 1
        base = sg * val
        mult = 1
        for v in U:
            mult *= x[v]
        vals[0] += base * mult
    for U, val in a.items():
        if i in U and j not in U:
            U0 = U - {i}
            deg = len(U)
            sg = -1 if ((n - deg) // 2) % 2 else 1
            mult = 1
            for v in U0:
                mult *= x[v]
            vals[1] += sg * val * mult
        if j in U and i not in U:
            U0 = U - {j}
            deg = len(U)
            sg = -1 if ((n - deg) // 2) % 2 else 1
            mult = 1
            for v in U0:
                mult *= x[v]
            vals[2] += sg * val * mult
        if i in U and j in U:
            U0 = U - {i, j}
            deg = len(U)
            sg = -1 if ((n - deg) // 2) % 2 else 1
            mult = 1
            for v in U0:
                mult *= x[v]
            vals[3] += sg * val * mult
    A, B, C, D = vals
    return B * C - A * D, vals


def main():
    rng = Random(20261007)
    n = 6
    vals = (-1, 0, 1)
    # deterministic low-cost search over sparse integer matrices
    for trial in range(1, 10001):
        density = (0.30, 0.45, 0.60, 0.75)[(trial - 1) % 4]
        F = [[rng.choice(vals) if rng.random() < density else 0 for _ in range(n)] for _ in range(n)]
        f = hole_coeffs(F)
        a = {U: z*z for U, z in f.items()}
        for i, j in combinations(range(n), 2):
            rem = [v for v in range(n) if v not in (i, j)]
            for choices in product((-1, 1), repeat=len(rem)):
                x = [1] * n
                for v, xv in zip(rem, choices):
                    x[v] = xv
                d, abc = rayleigh_coeff(a, n, i, j, x)
                if d < 0:
                    print({"trial": trial, "F": F, "i": i, "j": j, "x": x, "delta": d, "ABCD": abc, "f": {''.join(map(str, sorted(U))): z for U,z in f.items()}})
                    return
    print("NO_WITNESS")

if __name__ == '__main__':
    main()
