"""Exact small examples used by the fermionic-algorithms research note.

This is a self-contained demonstration script, not an implementation of the
general Gaussian sampler or the Chen–Liu FPRAS. It uses only Python's standard
library and prints exact rational outcomes.
"""
from fractions import Fraction
from itertools import product


def parity_coset_example():
    # Two rational Slater orbital choices (3/5,4/5), each with p=16/25.
    p = Fraction(16, 25)
    weights = {}
    for x in product((0, 1), repeat=2):
        prob = Fraction(1)
        for bit in x:
            prob *= p if bit else 1 - p
        syndrome = (x[0] + x[1]) % 2
        weights.setdefault(syndrome, Fraction(0))
        weights[syndrome] += prob
    print("H=[1 1], p=16/25")
    print("even syndrome probability:", weights[0])
    print("odd syndrome probability:", weights[1])


def fixed_fugacity_code_example():
    # Rational unit vector (3/5,4/5) gives p=16/25 and odds z=16/9.
    alpha, beta = Fraction(3, 5), Fraction(4, 5)
    p = beta * beta
    z = p / (alpha * alpha)
    print("rational Slater orbital:", (alpha, beta))
    print("occupation probability:", p)
    print("code-enumerator fugacity:", z)


def same_support_different_weights():
    # A two-mode pair matrix [[0,t],[-t,0]] has support {empty, {1,2}}.
    for t in (Fraction(1, 2), Fraction(2)):
        weights = (t * t, Fraction(1))
        normalizer = sum(weights)
        print("t =", t, "support = {empty, {1,2}}",
              "weights =", weights,
              "normalized =", tuple(w / normalizer for w in weights))


def one_block_cnf_filter():
    # The 3-mode BCS block has four equiprobable occupation sets; the first
    # mode is occupied in two of them, so filtering on x=1 has probability 1/2.
    patterns = ((), (1, 2), (0, 1), (0, 2))
    accepted = sum(0 in pattern for pattern in patterns)
    print("3-mode BCS block patterns:", patterns)
    print("single literal x=1 acceptance:", Fraction(accepted, len(patterns)))


if __name__ == "__main__":
    parity_coset_example()
    fixed_fugacity_code_example()
    same_support_different_weights()
    one_block_cnf_filter()
