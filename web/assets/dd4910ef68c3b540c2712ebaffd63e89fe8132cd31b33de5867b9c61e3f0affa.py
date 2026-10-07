"""Finite fixtures for the pair-copy / spliced-Walsh counterexample.

The mathematical argument, not these finite checks, proves the general result.
Uses only the Python standard library and rational transition probabilities.
"""

from fractions import Fraction
from itertools import product
from math import isclose, log


def probabilities(k, gamma, word, delta=Fraction(0)):
    p = Fraction(1)
    q = Fraction(1)
    for j, bit in enumerate(word):
        # j is zero based: fresh bit at even j; copy previous bit at odd j.
        if j % 2:
            p *= 1 - delta if bit == word[j - 1] else delta
            q *= 1 - gamma if bit == word[j - 1] else gamma
        else:
            p *= Fraction(1, 2)
            if j == 4 * k and word[2 * k - 2] == 0 and word[2 * k - 1] == 1:
                left = word[0:2 * k - 2:2]
                right = word[2 * k:4 * k - 2:2]
                parity = sum(a * b for a, b in zip(left, right)) % 2
                p1 = Fraction(3, 4) if parity == 0 else Fraction(1, 4)
                q *= p1 if bit else 1 - p1
            else:
                q *= Fraction(1, 2)
    return p, q


def rank(matrix):
    matrix = [[Fraction(x) for x in row] for row in matrix]
    nrows, ncols = len(matrix), len(matrix[0])
    pivot_row = 0
    for col in range(ncols):
        pivot = next((r for r in range(pivot_row, nrows) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        factor = matrix[pivot_row][col]
        matrix[pivot_row] = [x / factor for x in matrix[pivot_row]]
        for r in range(nrows):
            if r != pivot_row and matrix[r][col]:
                factor = matrix[r][col]
                matrix[r] = [a - factor * b for a, b in zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def check():
    gamma = Fraction(1, 1000)
    for k in range(1, 4):
        total_p, total_q, total_abs = Fraction(0), Fraction(0), Fraction(0)
        kl = 0.0
        for word in product((0, 1), repeat=4 * k + 2):
            p, q = probabilities(k, gamma, word)
            total_p += p
            total_q += q
            total_abs += abs(p - q)
            if p:
                assert q / p == (1 - gamma) ** (2 * k + 1)
                kl += float(p) * log(float(p / q))
        assert total_p == total_q == 1
        assert total_abs / 2 == 1 - (1 - gamma) ** (2 * k + 1)
        assert isclose(kl, -(2 * k + 1) * log(float(1 - gamma)), abs_tol=1e-12)
        print(f"k={k}: joint TV identity and KL identity verified")

    # The same logit-rank obstruction persists with a strictly positive source.
    delta = gamma ** 2
    k = 2
    total_p, total_q, kl = Fraction(0), Fraction(0), 0.0
    for word in product((0, 1), repeat=4 * k + 2):
        p, q = probabilities(k, gamma, word, delta)
        assert p > 0 and q > 0
        total_p += p
        total_q += q
        kl += float(p) * log(float(p / q))
    bernoulli_kl = float(delta) * log(float(delta / gamma)) + float(1 - delta) * log(float((1 - delta) / (1 - gamma)))
    target_kl = (2 * k + 1) * bernoulli_kl + float(delta / 2) * (log(4 / 3) / 2)
    assert total_p == total_q == 1
    assert isclose(kl, target_kl, abs_tol=1e-12)
    print("Strictly positive source: exact KL chain-rule formula verified")

    for k in range(1, 7):
        strings = list(product((0, 1), repeat=k - 1))
        walsh = [[(-1) ** (sum(a * b for a, b in zip(x, z)) % 2) for z in strings] for x in strings]
        n = len(strings)
        for i in range(n):
            for j in range(n):
                assert sum(walsh[i][t] * walsh[j][t] for t in range(n)) == (n if i == j else 0)
        assert rank(walsh) == n
        print(f"k={k}: spliced logit submatrix has rank {n}")
    print("ALL_FIXTURES_PASSED")


if __name__ == "__main__":
    check()
