#!/usr/bin/env python3
"""Exact rational fixtures for the symmetric MPO and rare-herald filter.

The N=4 dense-matrix replay checks the count-pair MPO entry rule against an
independently assembled Dicke-projector mixture, then applies the explicit
prefix-zero/CNOT Kraus map. The N=20 fixture uses exact combinatorial sector
counts and a bond-2 CNOT decomposition to exhibit an exponentially small
nonzero event. These checks do not implement a generic MPO contractor or
validate the Cycle-3 mixture theorem.
"""

from fractions import Fraction as F
from math import comb


def tv(p, q):
    return sum((abs(x - y) for x, y in zip(p, q)), F(0)) / 2


def normalized(v):
    z = sum(v, F(0))
    assert z > 0
    return [x / z for x in v]


def dicke_mixture_matrix(weights, n):
    """Dense exact matrix for sum_k weights[k] |D_k><D_k|."""
    dim = 1 << n
    out = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for k, weight in enumerate(weights):
        denom = comb(n, k)
        strings = [x for x in range(dim) if x.bit_count() == k]
        for x in strings:
            for y in strings:
                out[x][y] += weight / denom
    return out


def count_pair_mpo_entry(q, x, y, n):
    """Run the deterministic (ket-count,bra-count) MPO automaton."""
    a = b = 0
    for i in range(n):
        shift = n - 1 - i
        a += (x >> shift) & 1
        b += (y >> shift) & 1
    return q[a] / comb(n, a) if a == b else F(0)


def cnot_output(x, n):
    """CNOT on the last pair, with the penultimate bit as control."""
    control = (x >> 1) & 1
    target = x & 1
    if control:
        target ^= 1
    return (x & ~0b11) | (control << 1) | target


def mpo_rank_and_n4_replay():
    # The CNOT operator has Schmidt rank two across its control/target cut.
    # Reshape K[o0 o1,i0 i1] into rows (o0,i0), columns (o1,i1).
    cnot = [[0 for _ in range(4)] for _ in range(4)]
    for x in range(4):
        cnot[cnot_output(x, 2)][x] = 1
    reshaped = [[cnot[(o0 << 1) | o1][(i0 << 1) | i1]
                 for o1, i1 in ((0, 0), (0, 1), (1, 0), (1, 1))]
                for o0, i0 in ((0, 0), (0, 1), (1, 0), (1, 1))]
    nonzero_rows = [row for row in reshaped if any(row)]
    assert len(nonzero_rows) == 2 and nonzero_rows[0] != nonzero_rows[1]
    # Exact rank by checking the explicit two-term operator-Schmidt form:
    # |0><0| tensor I + |1><1| tensor X.
    assert cnot[0][0] == cnot[1][1] == cnot[2][3] == cnot[3][2] == 1
    # Verify the two-term decomposition entrywise to establish rank <= 2.
    for o0 in range(2):
        for i0 in range(2):
            for o1 in range(2):
                for i1 in range(2):
                    lhs = cnot[(o0 << 1) | o1][(i0 << 1) | i1]
                    rhs = ((int(o0 == i0 == 0) * int(o1 == i1)) +
                           (int(o0 == i0 == 1) * int(o1 == (i1 ^ 1))))
                    assert lhs == rhs

    n = 4
    f = [F(2**(k - n)) for k in range(n + 1)]
    g = [w * (F(17, 16) if k % 2 else F(15, 16))
         for k, w in enumerate(f)]
    q = normalized(g)
    dense = dicke_mixture_matrix(q, n)
    dim = 1 << n
    # K = CNOT_(n-1,n) (|0><0|^(tensor n-2) tensor I tensor I).
    K = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for x in range(dim):
        if (x >> 2) == 0:
            K[cnot_output(x, n)][x] = F(1)
    for x in range(dim):
        for y in range(dim):
            effect_xy = sum((K[z][x] * K[z][y] for z in range(dim)), F(0))
            assert effect_xy == (F(1) if x == y and (x >> 2) == 0 else F(0))
    out = [[sum((K[a][x] * dense[x][y] * K[b][y]
                 for x in range(dim) for y in range(dim)), F(0))
            for b in range(dim)] for a in range(dim)]
    for x in range(dim):
        for y in range(dim):
            assert dense[x][y] == count_pair_mpo_entry(q, x, y, n)
    actual_masses = [out[x][x] for x in range(dim)]
    expected = [F(0) for _ in range(dim)]
    for x in range(dim):
        tail = cnot_output(x, n) & 0b11
        # Prefix-zero support leaves only output strings with zero prefix.
        if (x >> 2) == 0:
            expected[(x & ~0b11) | tail] += q[x.bit_count()] / comb(n, x.bit_count())
    assert actual_masses == expected
    assert sum(actual_masses, F(0)) == sum(
        (q[k] * F(comb(2, k), comb(n, k)) for k in range(3)), F(0))

    # A pair-singlet projector annihilates the entire symmetric sector; this
    # gives an exact zero-event control for the same rational input.
    Kzero = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for x in range(dim):
        prefix = x & ~0b11
        tail = x & 0b11
        for row_tail in range(4):
            # P_-=(I-SWAP)/2 on the final two sites.
            swap_tail = ((tail & 1) << 1) | ((tail >> 1) & 1)
            value = (F(1, 2) if row_tail == tail else F(0)) - (
                F(1, 2) if row_tail == swap_tail else F(0))
            Kzero[prefix | row_tail][x] = value
    zero_output = [[sum((Kzero[a][x] * dense[x][y] * Kzero[b][y]
                         for x in range(dim) for y in range(dim)), F(0))
                    for b in range(dim)] for a in range(dim)]
    assert all(value == 0 for row in zero_output for value in row)
    for a in range(dim):
        for b in range(dim):
            square = sum((Kzero[a][x] * Kzero[x][b] for x in range(dim)), F(0))
            assert square == Kzero[a][b]
    return n, sum((dense[x][x] for x in range(dim)), F(0)), sum(actual_masses, F(0)), True


def rare_bond2_cnot_filter_fixture():
    n = 20
    delta = F(1, 16)
    # Positive rational sector weights with O(n)-bit descriptions.
    f = [F(1, 1 << (n - k)) for k in range(n + 1)]
    g = [w * (1 + (delta if k % 2 else -delta))
         for k, w in enumerate(f)]

    # K = CNOT_(n-1,n) (|0><0|^(tensor n-2) tensor I tensor I).
    # The prefix projector is a product MPO. CNOT has operator-Schmidt rank
    # two, so K has bond two. Its effect K^T K is the prefix-zero projector.
    # Only k=0,1,2 survive; the tail bit outcomes are 00, 01/11, 10.
    def masses(weights):
        return [weights[0], weights[1] / n,
                weights[2] / comb(n, 2), weights[1] / n]

    rho_z, sigma_z = sum(f, F(0)), sum(g, F(0))
    p_success = sum(masses(f), F(0)) / rho_z
    q_success = sum(masses(g), F(0)) / sigma_z
    assert 0 < p_success < F(1, 1 << n)
    assert q_success > 0

    p_out = normalized(masses(f))
    q_out = normalized(masses(g))
    L = (1 + delta) / (1 - delta)
    bound = L * L - 1
    assert tv(p_out, q_out) <= bound

    # Finite-bit conditional CDF: b-bit floors on the four-category CDF
    # give the checked 2K/2^b total-variation upper bound.
    gamma = F(1, 1000)
    b = 0
    while F(2 * len(q_out), 1 << b) > gamma / 4:
        b += 1
    rounded_cdf = []
    cdf = F(0)
    previous = 0
    for probability in q_out[:-1]:
        cdf += probability
        scaled = cdf * (1 << b)
        point = scaled.numerator // scaled.denominator
        rounded_cdf.append(point - previous)
        previous = point
    rounded_cdf.append((1 << b) - previous)
    sampled = [F(count, 1 << b) for count in rounded_cdf]
    rounding_error = tv(sampled, q_out)
    assert rounding_error <= F(2 * len(q_out), 1 << b) <= gamma / 4
    return p_success, q_success, tv(p_out, q_out), bound, b, rounding_error


if __name__ == "__main__":
    n4, trace, success, zero_event = mpo_rank_and_n4_replay()
    p, q, d, bound, b, rounderr = rare_bond2_cnot_filter_fixture()
    print("dense Dicke/count-pair MPO replay: N=", n4,
          "trace=", trace, "success=", success,
          "exact symmetric-sector zero event:", zero_event)
    print("bond-2 CNOT filter success mass < 2^-20:", p < F(1, 1 << 20),
          "input success numerator bits:", p.numerator.bit_length(),
          "denominator bits:", p.denominator.bit_length())
    print("approx success mass positive:", q > 0)
    print("4-outcome conditional TV / Loewner bound:", d, bound)
    print("finite-bit CDF bits / rounding error:", b, rounderr)
