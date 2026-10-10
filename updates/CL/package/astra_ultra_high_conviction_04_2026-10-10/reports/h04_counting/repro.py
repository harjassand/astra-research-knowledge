#!/usr/bin/env python3
"""Exact neighborhood-union DP and K_{n,n} phase check (stdlib only)."""
from fractions import Fraction
from itertools import product


def union_dp(neighborhoods, n_right, lam):
    """Return final coefficients A[U] = sum_{S:N(S)=U} lam**|S|."""
    table = {0: Fraction(1)}
    state_counts = [1]
    for neighborhood in neighborhoods:
        next_table = {}
        for union, weight in table.items():
            next_table[union] = next_table.get(union, Fraction(0)) + weight
            joined = union | neighborhood
            next_table[joined] = next_table.get(joined, Fraction(0)) + lam * weight
        table = next_table
        state_counts.append(len(table))
    full = (1 << n_right) - 1
    z = sum(weight * (1 + lam) ** (n_right - union.bit_count())
            for union, weight in table.items())
    return z, table, state_counts, full


def brute_force(neighborhoods, n_right, lam):
    z = Fraction(0)
    for bits in product((0, 1), repeat=len(neighborhoods)):
        union = 0
        left_weight = Fraction(1)
        for bit, neighborhood in zip(bits, neighborhoods):
            if bit:
                union |= neighborhood
                left_weight *= lam
        z += left_weight * (1 + lam) ** (n_right - union.bit_count())
    return z


def brute_configurations(neighborhoods, n_right, lam):
    """Enumerate all left/right bit strings and retain independent sets."""
    z = Fraction(0)
    for left_bits in product((0, 1), repeat=len(neighborhoods)):
        union = 0
        left_size = sum(left_bits)
        for bit, neighborhood in zip(left_bits, neighborhoods):
            if bit:
                union |= neighborhood
        for right_bits in product((0, 1), repeat=n_right):
            right_mask = sum(bit << j for j, bit in enumerate(right_bits))
            if union & right_mask:
                continue
            z += lam ** (left_size + sum(right_bits))
    return z


def main():
    for n in range(1, 9):
        full = (1 << n) - 1
        neighborhoods = [full] * n
        z, coeffs, counts, _ = union_dp(neighborhoods, n, Fraction(1))
        assert z == 2 ** (n + 1) - 1
        assert brute_force(neighborhoods, n, Fraction(1)) == z
        assert counts[-1] == 2
        assert coeffs[0] == 1
        assert coeffs[full] == 2**n - 1
        marginal_exit = Fraction(1, 2**n + 1)
        local_conductance = Fraction(1, 4 * (2**n - 1))
        print(f"n={n}: q={counts[-1]}, Z={z}, phase_weights=({2**n},{2**n-1}), "
              f"marginal_exit_from_empty={marginal_exit}, "
              f"original_local_conductance={local_conductance}")

    # A tiny irregular case checks that the same recurrence is not special to K_n,n.
    neighborhoods = [0b001, 0b011, 0b100, 0b110]
    z, _, _, _ = union_dp(neighborhoods, 3, Fraction(2, 3))
    assert z == brute_force(neighborhoods, 3, Fraction(2, 3))
    assert z == brute_configurations(neighborhoods, 3, Fraction(2, 3))
    print(f"irregular_case: exact_dp_matches_independent_set_enumeration, Z={z}")


if __name__ == "__main__":
    main()
