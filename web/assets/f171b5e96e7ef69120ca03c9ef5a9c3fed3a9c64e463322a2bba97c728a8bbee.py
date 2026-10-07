from fractions import Fraction
from math import comb, log


def H(n):
    return sum((Fraction(1, k) for k in range(1, n + 1)), Fraction())


def tv(p, q):
    return sum((abs(p.get(k, 0) - q.get(k, 0)) for k in p.keys() | q.keys()), Fraction()) / 2


def floor_ceil(N, exceptional):
    h = H(N)
    p = {k: Fraction(1, k) / h for k in range(1, N + 1)}
    q = {}
    for k, mass in p.items():
        if k == 1 and exceptional in ('fixed', 'flag'):
            j = 1 if exceptional == 'fixed' else 'flag'
            q[j] = q.get(j, Fraction()) + mass
        else:
            for j in (k // 2, (k + 1) // 2):
                q[j] = q.get(j, Fraction()) + mass / 2
    return tv(p, q)


def binomial(N):
    h = H(N)
    p = {k: Fraction(1, k) / h for k in range(1, N + 1)}
    q = {j: sum((Fraction(comb(k, j), k * 2**k) for k in range(max(j, 1), N + 1)), Fraction()) / h for j in range(N + 1)}
    assert all(q[j] <= p[j] for j in range(1, N + 1))
    return tv(p, q), q[0]


for N in range(2, 101):
    L = (N - 1) // 2
    coefficient = H(2 * L) - H(L) + Fraction(1, 2 * (2 * L + 1))
    assert floor_ceil(N, 'fixed') == coefficient / H(N)
    assert floor_ceil(N, 'natural') == coefficient / H(N)
    if N >= 3:
        assert floor_ceil(N, 'flag') == (coefficient + Fraction(1, 3)) / H(N)
    btv, q0 = binomial(N)
    assert btv == q0
    assert float(coefficient) < log(2)
    # The truncated dyadic sum rounds to log(2) at large N in binary64.
    assert float(q0 * H(N)) <= log(2) + 1e-15

print('Exact rational checks passed for N=2..100; disjoint-flag formula checked for N=3..100.')
for N in (2, 3, 10, 100):
    btv, _ = binomial(N)
    print(f'N={N}: fixed/natural={float(floor_ceil(N, "fixed")):.9f}, disjoint flag={float(floor_ceil(N, "flag")):.9f}, binomial={float(btv):.9f}, log2/H_N={log(2)/float(H(N)):.9f}')
