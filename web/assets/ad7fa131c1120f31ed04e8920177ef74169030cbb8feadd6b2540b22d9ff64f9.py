#!/usr/bin/env python3
"""Exact small checks for the directed-cycle paired-basis obstruction/lift."""

from itertools import combinations, product
from fractions import Fraction
import json
from pathlib import Path

from basis_exchange_check import det_bareiss


def det_for_paired_set(n, sites):
    # Pair block i=(e_i, f_i), with f_i=e_(i+1 mod n).
    columns = []
    for i in sites:
        for row in (i, (i + 1) % n):
            columns.append([int(j == row) for j in range(n)])
    return det_bareiss([[columns[j][i] for j in range(n)] for i in range(n)])


def main():
    rows = []
    for n in (4, 6, 8):
        r = n // 2
        paired = {}
        for sites in combinations(range(n), r):
            paired[sites] = det_for_paired_set(n, sites)
        support = [s for s, value in paired.items() if value]
        alternating = [tuple(range(0, n, 2)), tuple(range(1, n, 2))]
        assert support == alternating
        assert all(abs(paired[s]) == 1 for s in support)

        # A full basis of [I,P] chooses exactly one of the two labeled copies
        # of each standard basis vector, hence one bit per row and 2^n bases.
        assignments = list(product((0, 1), repeat=n))
        assert len(assignments) == 2**n
        # The two paired bases are antipodes in this assignment hypercube.
        x0 = tuple(int(i in support[0]) for i in range(n))
        x1 = tuple(int(i in support[1]) for i in range(n))
        assert all(x1[i] == 1 - x0[i] for i in range(n))

        # Harmonic conductance kernel with D=n^2 and unit basis-pair weights:
        # each of the n valid duplicate-row swaps has probability 1/(2 n^2).
        degree = n
        edge_probability = Fraction(1, 2 * n * n)
        self_loop = 1 - degree * edge_probability
        assert self_loop >= 0
        mu_x = mu_y = 1
        forward_conductance = Fraction(mu_x * mu_y, n * n * (mu_x + mu_y))
        reverse_conductance = Fraction(mu_y * mu_x, n * n * (mu_y + mu_x))
        assert forward_conductance == reverse_conductance

        # Linear Hamming extension g(x)=dist(x,x0)/n has target variance 1/4,
        # ambient variance 1/(4n), and Dirichlet form 1/(4n^3).
        variance_target = Fraction(1, 4)
        variance_extension = Fraction(1, 4 * n)
        dirichlet_extension = Fraction(1, 4 * n**3)
        assert variance_target == n**3 * dirichlet_extension

        def g(x):
            return Fraction(sum(x[j] != x0[j] for j in range(n)), n)

        g_values = [g(x) for x in assignments]
        mean_g = sum(g_values, Fraction(0)) / len(assignments)
        checked_variance = sum((v - mean_g) ** 2 for v in g_values) / len(assignments)
        checked_dirichlet = Fraction(0)
        for x in assignments:
            for j in range(n):
                y = list(x)
                y[j] = 1 - y[j]
                y = tuple(y)
                # Uniform state weights and symmetric exchange probabilities.
                checked_dirichlet += (
                    Fraction(1, 2**n) * edge_probability * (g(x) - g(y)) ** 2 / 2
                )
        assert checked_variance == variance_extension
        assert checked_dirichlet == dirichlet_extension

        rows.append({
            "n": n,
            "paired_support": [list(s) for s in support],
            "paired_determinants": [paired[s] for s in support],
            "ambient_full_basis_count": 2**n,
            "paired_fiber_fraction": f"2/{2**n}",
            "paired_rejection_acceptance": f"1/{2**(n-1)}",
            "two_replica_paired_fraction": f"1/{2**(2*n-2)}",
            "augmented_state_graph": "n-dimensional hypercube",
            "harmonic_exchange_degree": degree,
            "harmonic_exchange_edge_probability": str(edge_probability),
            "harmonic_exchange_self_loop": str(self_loop),
            "target_variance_for_unit_difference": str(variance_target),
            "extension_variance": str(variance_extension),
            "extension_dirichlet": str(dirichlet_extension),
            "enumerated_extension_variance": str(checked_variance),
            "enumerated_extension_dirichlet": str(checked_dirichlet),
            "target_variance_over_extension_dirichlet": n**3,
        })

    result = {
        "family": "n even; F is the directed n-cycle permutation; block i=(e_i,row_i(F))",
        "exact_checks": rows,
        "scope": "finite Bareiss checks plus closed-form hypercube and Dirichlet derivation; not a general paired-energy theorem",
    }
    out = Path(__file__).with_name("cycle_family_lift_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
