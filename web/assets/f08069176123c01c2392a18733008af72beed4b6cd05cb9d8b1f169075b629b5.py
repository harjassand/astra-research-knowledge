#!/usr/bin/env python3
"""Exact paired-basis exchange check with two-site mismatch registers."""

from itertools import combinations
import json
from pathlib import Path

from basis_exchange_check import det_bareiss


def main():
    d, r = 4, 2
    # F[i,j]=1 iff j=i+1 mod 4; pair block i is (e_i,row_i(F)).
    fmat = [[int(j == (i + 1) % d) for j in range(d)] for i in range(d)]
    vectors = {}
    for i in range(d):
        vectors[('e', i)] = [int(row == i) for row in range(d)]
        vectors[('f', i)] = list(fmat[i])

    def block_basis(sites):
        return [col for i in sorted(sites)
                for col in (('e', i), ('f', i))]

    def determinant(cols):
        return det_bareiss([[vectors[col][row] for col in cols]
                            for row in range(d)])

    def occupancy(cols):
        return {i: sum(1 for kind, index in cols if index == i)
                for i in range(d)}

    weights = {sites: determinant(block_basis(sites))
               for sites in combinations(range(d), r)}
    support = [sites for sites, value in weights.items() if value]
    assert support == [(0, 2), (1, 3)]
    assert all(abs(weights[sites]) == 1 for sites in support)

    direct_paired_edges = 0
    for sites in support:
        for i in sites:
            for j in set(range(d)) - set(sites):
                neighbor = tuple(sorted((set(sites) - {i}) | {j}))
                if weights[neighbor]:
                    direct_paired_edges += 1
    assert direct_paired_edges == 0

    s, t = support
    a, b = block_basis(s), block_basis(t)
    e = next(col for col in a if col not in b)
    epos = a.index(e)
    b_only = [col for col in b if col not in a]
    signed_sum = 0
    square_sum = 0
    nonzero_terms = 0
    mismatched_terms = 0
    term_rows = []
    for g in b_only:
        gpos = b.index(g)
        a2, b2 = list(a), list(b)
        a2[epos] = g
        b2[gpos] = e
        da, db = determinant(a2), determinant(b2)
        product = da * db
        signed_sum += product
        square_sum += product * product
        if product:
            nonzero_terms += 1
            occ_a, occ_b = occupancy(a2), occupancy(b2)
            e_site, g_site = e[1], g[1]
            assert e_site != g_site
            assert occ_a[e_site] == occ_a[g_site] == 1
            assert occ_b[e_site] == occ_b[g_site] == 1
            assert all(occ_a[i] in (0, 2, 1) for i in range(d))
            assert all(occ_b[i] in (0, 2, 1) for i in range(d))
            mismatched_terms += 1
        term_rows.append({
            "exchange_column": list(g),
            "determinant_A_prime": da,
            "determinant_B_prime": db,
            "product": product,
        })

    lhs = determinant(a) * determinant(b)
    assert signed_sum == lhs
    assert lhs * lhs <= len(b_only) * square_sum
    assert nonzero_terms > 0
    assert mismatched_terms == nonzero_terms

    result = {
        "matrix": "4-cycle permutation",
        "ambient_dimension": d,
        "sector_size": r,
        "paired_support": [list(x) for x in support],
        "paired_determinants": [weights[x] for x in support],
        "direct_paired_single_block_exchange_edges": direct_paired_edges,
        "source_pair": [list(s), list(t)],
        "chosen_column_e": list(e),
        "candidate_columns": len(b_only),
        "exchange_terms": term_rows,
        "signed_basis_exchange_identity": "PASS",
        "squared_cauchy_bound": "PASS",
        "nonzero_terms": nonzero_terms,
        "nonzero_terms_with_two_site_mismatches": mismatched_terms,
        "target_product_squared": lhs * lhs,
        "sum_of_exchange_product_squares": square_sum,
        "exchange_factor": len(b_only),
        "scope": "exact integer fixture; universal derivation is in REVISION_01.txt",
    }
    out = Path(__file__).with_name("paired_single_exchange_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
