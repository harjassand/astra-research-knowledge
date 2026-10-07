from fractions import Fraction as F

cases = 0
for L in range(2, 11):
    m = 2 ** (L - 1)
    for K in range(1, m + 1):
        r = K.bit_length() - 1
        a = 2 ** (r + 1) - K
        b = 2 * K - 2 ** (r + 1)
        assert a >= 0 and b >= 0 and a + b == K
        pure = [F(0) for _ in range(L)]
        replacement = F(0)
        for j in range(L):
            n = 2 ** j
            if j <= r:
                assert n <= K
                pure[0] += F(n, K * L)
                replacement += F(K - n, K * L)
            else:
                assert a * 2 ** (j - r) + b * 2 ** (j - r - 1) == n
                pure[j-r] += F(a, K * L)
                pure[j-r-1] += F(b, K * L)
        phi = F(r + 2) - F(2 ** (r + 1), K)
        assert sum(pure) + replacement == 1
        assert pure[0] == F(2 * K - 1, K * L)
        assert replacement == F(r + 1, L) - F(2 ** (r + 1) - 1, K * L)
        assert pure[0] >= F(1, L) and replacement >= 0
        assert all(q <= F(1, L) for q in pure[1:])
        bottom_excess = pure[0] + replacement - F(1, L)
        top_deficits = sum(F(1, L) - q for q in pure[1:])
        assert bottom_excess == top_deficits == phi / L
        if K < m:
            boundary = L - r - 1
            assert boundary >= 1
            for ell in range(1, boundary):
                assert pure[ell] == F(1, L)
            assert pure[boundary] == F(a, K * L)
            assert all(q == 0 for q in pure[boundary + 1:])
        else:
            assert r == L - 1
            assert all(q == 0 for q in pure[1:])
        s = L - r - 1
        unified_numerator = F(L - s + 1) - F(1, 2**s) - F(2*m-1, K * 2**s)
        assert unified_numerator == phi - F(2**r, m) * (1 - F(1, K))
        cases += 1
print(f'Passed exact rational flag, allocation, trace-error, and lower-bound algebra checks for {cases} cases, L=2,...,10 and 1<=K<=2^(L-1).')
