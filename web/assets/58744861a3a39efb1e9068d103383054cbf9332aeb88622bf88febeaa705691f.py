#!/usr/bin/env python3
"""Small exact checks for the cycle-3 product-vector / Pauli-Sidon note.

This is finite arithmetic evidence only; the all-K endpoint proof is in
DERIVATION.txt. No channel matrices or input-state optimization are done.
"""
from collections import Counter
from fractions import Fraction
from math import comb, log, sqrt


def gf8_mul(a: int, b: int) -> int:
    """Multiply in GF(8)=F2[z]/(z^3+z+1), represented by three bits."""
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 0b1000:
            a ^= 0b1011
    return out


def gf8_cube(x: int) -> int:
    return gf8_mul(gf8_mul(x, x), x)


def gf8_trace(x: int) -> int:
    x2 = gf8_mul(x, x)
    x4 = gf8_mul(x2, x2)
    t = x ^ x2 ^ x4
    assert t in (0, 1)
    return t


def checked_square_inequalities() -> None:
    # e > 1+1+1/2+1/6 = 8/3, so exp(1/(4e)) < exp(3/32) < 32/29.
    assert 18 * 18 * 2 < 29 * 29  # 18 sqrt(2) < 29
    assert 128 * 128 * 2 < 261 * 261  # 128 sqrt(2) < 261
    assert Fraction(7, 3) > Fraction(9, 4)


def gf8_gold_fixture() -> dict[str, object]:
    # G=GF(8)^2 ~= F2^6, n=8, N=64, K=8.
    branches = [(x, gf8_cube(x)) for x in range(8)]
    encoded = [x | (y << 3) for x, y in branches]

    ordered_sums = Counter(a ^ b for a in encoded for b in encoded)
    assert ordered_sums[0] == 8
    nonzero_multiplicities = [v for g, v in ordered_sums.items() if g]
    assert len(nonzero_multiplicities) == comb(8, 2) == 28
    assert set(nonzero_multiplicities) == {2}
    assert len(ordered_sums) == 29

    # Walsh transform of graph indicator under the 6-bit dot-product pairing.
    walsh = {}
    for a in range(8):
        for b in range(8):
            total = 0
            for x in range(8):
                exponent = gf8_trace(gf8_mul(a, x) ^ gf8_mul(b, gf8_cube(x)))
                total += 1 if exponent == 0 else -1
            walsh[(a, b)] = total

    assert walsh[(0, 0)] == 8
    beta_num = max(abs(v) for k, v in walsh.items() if k != (0, 0))
    assert beta_num == 4

    N, K, n = 64, 8, 8
    energy = 3 * K * K - 2 * K
    R = Fraction(N * energy - K**4, K * (N - K))
    assert R == 16
    beta_sq = Fraction(beta_num * beta_num, K * K)
    assert beta_sq == Fraction(R, K * K) == Fraction(1, 4)

    purity = Fraction(1, n) + Fraction(n - 1, n) * beta_sq
    assert purity == Fraction(11, 32)

    # Exact Bell eigenvalue profile: 1/8 once, 1/32 twenty-eight times.
    bell_probs = [Fraction(1, K)] + [Fraction(2, K * K)] * comb(K, 2)
    assert sum(bell_probs) == 1
    assert bell_probs[0] == Fraction(1, 8)
    assert set(bell_probs[1:]) == {Fraction(1, 32)}

    h_bell = -sum(float(p) * log(float(p)) for p in bell_probs)
    h2_lower = -log(float(purity))
    gap_lower = 2 * h2_lower - h_bell
    assert gap_lower < 0
    return {
        "branches": len(branches),
        "input_dimension_n": n,
        "pauli_label_count_N": N,
        "sidon_pair_sums": len(nonzero_multiplicities),
        "max_nontrivial_walsh": beta_num,
        "R_energy_lower_bound": str(R),
        "purity_upper_bound": str(purity),
        "single_entropy_lower_nats": h2_lower,
        "bell_entropy_nats": h_bell,
        "purity_gap_lower_nats": gap_lower,
    }


def check_endpoint_formula_fixtures() -> None:
    # Spot-check the analytic R_K(N), derivative sign, and endpoint formulae.
    # The proof itself covers all integer K>=3 and real N>=N0.
    for K in range(3, 101):
        N0 = 1 + comb(K, 2)

        def R(N: float) -> float:
            return (N * (3 * K - 2) - K**3) / (N - K)

        assert abs(R(N0) - (K - 2)) < 1e-10
        for N in (N0, N0 * 1.5, 4 * K * K, 100 * K * K):
            r = R(N) / K**2
            f = 1 / sqrt(N) + (1 - 1 / sqrt(N)) * r
            hb = 2 * log(K) - log(2) - log(K / 2) / K
            threshold = exp_minus_half(hb)
            assert f > threshold
        # The derivative numerator must switch + to - around the larger root.
        x_plus = K + sqrt(K * (K - 1))
        assert 2 * K * (sqrt(N0) - 1) > N0 - K
        assert 2 * K * (2 * x_plus - 1) < (2 * x_plus) ** 2 - K


def exp_minus_half(h: float) -> float:
    from math import exp

    return exp(-h / 2)


if __name__ == "__main__":
    checked_square_inequalities()
    check_endpoint_formula_fixtures()
    print(gf8_gold_fixture())
    print("PASS: exact GF(8) and rational checks; numerical endpoint spot checks only")
