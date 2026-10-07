#!/usr/bin/env python3
"""Exact mismatch-register check for pair-block volume exchange."""

from itertools import combinations
import json
from pathlib import Path

from basis_exchange_check import det_bareiss


def sign_of_permutation(sequence):
    inversions = sum(
        sequence[i] > sequence[j]
        for i in range(len(sequence))
        for j in range(i + 1, len(sequence))
    )
    return -1 if inversions % 2 else 1


def determinant(columns, vectors, d):
    return det_bareiss([[vectors[col][row] for col in columns]
                        for row in range(d)])


def main():
    d, k = 4, 2
    # F[i,j]=1 iff j=i+1 mod 4.  The pair block at site i is (e_i,row_i(F)).
    f = [[int(j == (i + 1) % d) for j in range(d)] for i in range(d)]
    vectors = {}
    for i in range(d):
        vectors[('e', i)] = [int(row == i) for row in range(d)]
        vectors[('f', i)] = list(f[i])

    def block_columns(sites):
        return [column for i in sorted(sites)
                for column in (('e', i), ('f', i))]

    values = {}
    for sites in combinations(range(d), k):
        values[sites] = determinant(block_columns(sites), vectors, d)
    support = [sites for sites, value in values.items() if value]
    assert support == [(0, 2), (1, 3)]
    assert [abs(values[s]) for s in support] == [1, 1]

    s, t = support
    i = next(x for x in s if x not in t)
    a_rest = [col for col in block_columns(s) if col[1] != i]
    a_i = [('e', i), ('f', i)]
    a_columns = a_rest + a_i
    b_columns = block_columns(t)
    assert determinant(a_columns, vectors, d) == values[s]
    assert determinant(b_columns, vectors, d) == values[t]

    signed_total = 0
    full_mass = 0
    paired_block_mass = 0
    split_block_mass = 0
    term_count = 0
    nonzero_split_terms = 0
    for positions in combinations(range(d), 2):
        k_comp = [j for j in range(d) if j not in positions]
        k_cols = [b_columns[j] for j in positions]
        kc_cols = [b_columns[j] for j in k_comp]
        a_prime = a_rest + k_cols
        b_prime = kc_cols + a_i
        da = determinant(a_prime, vectors, d)
        db = determinant(b_prime, vectors, d)
        product = da * db
        sign = sign_of_permutation(k_comp + list(positions))
        signed_total += sign * product
        term_mass = product * product
        full_mass += term_mass
        term_count += 1
        whole_block = (len({col[1] for col in k_cols}) == 1
                       and {col[0] for col in k_cols} == {'e', 'f'})
        if whole_block:
            paired_block_mass += term_mass
        else:
            split_block_mass += term_mass
            if product:
                nonzero_split_terms += 1

    lhs = values[s] * values[t]
    mismatch_factor = term_count
    assert signed_total == lhs
    assert lhs * lhs <= mismatch_factor * full_mass
    assert paired_block_mass == 0
    assert split_block_mass > 0
    assert nonzero_split_terms > 0

    result = {
        "matrix": "4-cycle permutation",
        "ambient_dimension": d,
        "pair_block_count": d,
        "paired_sector_size": k,
        "paired_support": [list(x) for x in support],
        "paired_basis_determinants": [values[x] for x in support],
        "target_product_squared": lhs * lhs,
        "laplace_terms": term_count,
        "whole_block_exchange_mass": paired_block_mass,
        "split_block_mismatch_mass": split_block_mass,
        "nonzero_split_block_terms": nonzero_split_terms,
        "all_term_mass": full_mass,
        "coarse_cauchy_factor": mismatch_factor,
        "signed_pair_block_laplace_identity": "PASS",
        "mismatch_retention_inequality": "PASS",
        "scope": "exact integer fixture; universal derivation is in INITIAL.txt",
    }
    out = Path(__file__).with_name("paired_block_exchange_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
