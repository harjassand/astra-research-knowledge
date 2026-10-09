#!/usr/bin/env python3
"""Independent exact consistency check for the balanced 4-gate split example.

No imports from the candidate implementation.  Uses integer truth tables and
Walsh transforms, plus separate combinatorial checks of every influence.
All returned numerical data, including entropy for these dyadic spectra, are
exact fractions.  This finite test does not replace the all-depth proof.
"""
from fractions import Fraction
import json


def h(positive_mask):
    return 1 if positive_mask.bit_count() >= 3 or positive_mask in (3, 12, 5) else -1


def table(depth):
    assert depth in (1, 2)
    if depth == 1:
        return [h(mask) for mask in range(16)]
    return [h(sum((h((mask >> (4 * j)) & 15) == 1) << j for j in range(4)))
            for mask in range(1 << 16)]


def integer_fourier(values):
    # Input index has x_i=2*bit_i-1.  The difference b-a, rather than a-b,
    # makes these coefficients match the characters product(x_i) exactly.
    a = list(values)
    step = 1
    while step < len(a):
        for start in range(0, len(a), 2 * step):
            for offset in range(step):
                lo, hi = start + offset, start + offset + step
                x, y = a[lo], a[hi]
                a[lo], a[hi] = x + y, y - x
        step *= 2
    return a


def metrics(values):
    N = len(values)
    n = N.bit_length() - 1
    assert N == 1 << n
    assert sum(values) == 0
    w = integer_fourier(values)
    assert sum(v * v for v in w) == N * N
    rows = []
    for i in range(n):
        bit = 1 << i
        # Check monotonicity independently in the truth table.
        assert all(values[m] <= values[m | bit] for m in range(N) if not m & bit)
        influence = Fraction(sum(values[m] != values[m ^ bit] for m in range(N)), N)
        spectral_influence = Fraction(sum(v * v for m, v in enumerate(w) if m & bit), N * N)
        assert influence == spectral_influence == Fraction(w[bit], N)
        A = Fraction(sum(abs(w[m] * w[m | bit]) for m in range(N) if not m & bit), N * N)
        rows.append((A, influence, A / influence))
    # All nonzero coefficient magnitudes happen to be powers of two here.
    assert all(v == 0 or abs(v) & (abs(v) - 1) == 0 for v in w)
    entropy = sum((Fraction(v * v, N * N) * (2*n - 2*(abs(v).bit_length()-1))
                   for v in w if v), Fraction(0))
    return w, rows, entropy


def main():
    vals = table(1)
    w, rows, entropy = metrics(vals)
    # Independent direct definition of the 4-variable Fourier transform.
    direct = [sum(v * (-1 if ((~m) & S).bit_count() % 2 else 1)
                  for m, v in enumerate(vals)) for S in range(16)]
    assert w == direct
    expected_spectrum = {1: 8, 2: 4, 3: 4, 4: 8, 6: -4, 7: -4,
                         8: 4, 9: -4, 12: 4, 13: -4}
    assert {m: v for m, v in enumerate(w) if v} == expected_spectrum
    ai = [Fraction(1, 4)] * 4
    ii = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)]
    ratios = [Fraction(1, 2), Fraction(1), Fraction(1, 2), Fraction(1)]
    assert rows == list(zip(ai, ii, ratios))
    assert entropy == 3
    _, rows16, entropy16 = metrics(table(2))
    expected16 = []
    for j in range(4):
        for r in range(4):
            expected16.append((ii[j] * ai[r] + ii[r] * ai[j],
                               ii[j] * ii[r], ratios[j] + ratios[r]))
    assert rows16 == expected16
    assert entropy16 == Fraction(15, 2)
    A16 = sum(row[0] for row in rows16)
    I16 = sum(row[1] for row in rows16)
    assert A16 == 3 and I16 == Fraction(9, 4)
    out = {
        'status': 'PASS: exact arithmetic',
        'seed': {'spectrum': {str(m): str(Fraction(v, 16)) for m, v in enumerate(w) if v},
                 'rows_A_I_ratio': [[str(x) for x in row] for row in rows],
                 'H': str(entropy)},
        'depth2': {'rows_A_I_ratio': [[str(x) for x in row] for row in rows16],
                   'A': str(A16), 'I': str(I16), 'H': str(entropy16),
                   'min_ratio': str(min(row[2] for row in rows16))},
        'all_depths': 'Proof, not enumeration: n=4^d, min_i A_i/I_i=d/2; H/I=6*(1-(2/3)^d).'
    }
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
