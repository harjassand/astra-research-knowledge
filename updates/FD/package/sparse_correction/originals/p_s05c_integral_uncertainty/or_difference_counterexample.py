"""Exact counterexamples to W(T) <= |T| |supp F|.

All substantive checks use integer coefficients and exact zeta transforms.
The group witnesses reduce the same integer coefficient vector modulo q.
No random search, numerical tolerance, or guessed modulus is involved.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


def zeta(c, n):
    values = list(c)
    for i in range(n):
        bit = 1 << i
        for x in range(1 << n):
            if x & bit:
                values[x] += values[x ^ bit]
    return values


def pair_coefficients(b):
    """OR on the first block minus OR on the second, over Z."""
    n = 2 * b
    c = [0] * (1 << n)
    for a in range(1, 1 << b):
        sign = 1 if a.bit_count() % 2 else -1
        c[a] = sign
        c[a << b] = -sign
    return c


def tensor_coefficients(b, d):
    local = [(a, c) for a, c in enumerate(pair_coefficients(b)) if c]
    entries = [(0, 1)]
    for j in range(d):
        entries = [(a | (u << (2*b*j)), c*v)
                   for a, c in entries for u, v in local]
    c = [0] * (1 << (2*b*d))
    for a, value in entries:
        assert c[a] == 0
        c[a] = value
    return c


def expected_value(x, b, d):
    mask = (1 << b) - 1
    value = 1
    for j in range(d):
        block = x >> (2*b*j)
        value *= int(bool(block & mask)) - int(bool((block >> b) & mask))
    return value


def check(b, d=1, moduli=(2, 3, 4, 6)):
    n = 2*b*d
    c = tensor_coefficients(b, d)
    values = zeta(c, n)
    assert all(value == expected_value(x, b, d) for x, value in enumerate(values))
    T = [a for a, value in enumerate(c) if value]
    N = [x for x, value in enumerate(values) if value]
    minima = [a for a in T if not any(t != a and (t & a) == t for t in T)]
    W = sum(1 << (n - a.bit_count()) for a in minima)
    m, k = len(T), len(N)
    assert m == k == (2*((1 << b)-1))**d
    assert len(minima) == (2*b)**d
    assert all(a.bit_count() == d for a in minima)
    assert W == (b * (1 << (2*b)))**d
    assert T == N
    assert all(abs(value) == 1 for value in c if value)
    assert all(abs(value) == 1 for value in values if value)
    for modulus in moduli:
        # Since every nonzero integer entry is +/-1, reducing mod q >=2
        # changes neither coefficient nor value support.
        assert [a for a, value in enumerate(c) if value % modulus] == T
        assert [x for x, value in enumerate(values) if value % modulus] == N
    D = sum(sum((a & t) == a for t in T) for a in minima)
    assert D == (b * (1 << b))**d
    return {
        "b": b, "d": d, "n": n, "group": "any nontrivial finite abelian group; choose g != 0 and use coefficients +/-g",
        "m": m, "k": k, "minima_count": len(minima), "minimal_degree": d,
        "W": W, "mk": m*k, "slack_mk_minus_W": m*k-W,
        "mk_over_W": str(Fraction(m*k, W)),
        "S": str(Fraction(W, 1 << n)), "q": str(Fraction(k, 1 << n)),
        "S_over_mq": str(Fraction(W, m*k)),
        "minimal_mixture_proposals": str(Fraction(W, k)),
        "D": D, "D_over_m": str(Fraction(D, m)),
        "strict_counterexample": m*k < W,
        "checked_moduli": list(moduli), "checked_full_truth_table_size": 1 << n,
        "all_coefficients_and_nonzero_values_integer_plus_or_minus_one": True,
        "coefficient_support_equals_value_support": True,
        "T": T if b == 4 and d == 1 else None,
        "N": N if b == 4 and d == 1 else None,
        "minimal_supports": minima if b == 4 and d == 1 else None,
    }


def check_lattice():
    """Exact integral annihilator and HNF certificate for b=4,d=1."""
    from sympy import Matrix, eye
    from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form
    from sympy.polys.domains import ZZ

    n = 8
    c = pair_coefficients(4)
    values = zeta(c, n)
    T = [a for a, value in enumerate(c) if value]
    N = {x for x, value in enumerate(values) if value}
    zero = [x for x in range(1 << n) if x not in N]
    R = Matrix([[int((a & x) == a) for a in T] for x in zero])
    v = Matrix([c[a] for a in T])
    assert R*v == Matrix.zeros(len(zero), 1)
    assert all(abs(int(value)) == 1 for value in v)
    H = hermite_normal_form(R.T)
    # A primitive null vector with all entries +/-1 already proves no unit
    # lies in L. HNF/SNF below additionally identify the universal quotient.
    smith = smith_normal_form(R, domain=ZZ)
    diag = [abs(int(smith[i, i])) for i in range(min(smith.rows, smith.cols)) if smith[i, i]]
    assert H.cols == 29
    assert diag == [1]*29
    assert H.T*v == Matrix.zeros(H.cols, 1)
    # Rank 29 and primitive (torsion-free) image imply L=ker(v dot -).
    # Thus H=Z^30/L is exactly Z, with all units mapping to +/-1.
    # Reducing this quotient modulo any q>=2 yields the explicit witness.
    return {
        "n": n, "m": len(T), "allowed_support_size": len(N),
        "zero_rows": len(zero), "integer_row_lattice_rank": H.cols,
        "smith_diagonal": diag, "torsion_order": 1,
        "universal_group": "Z", "finite_quotient": "Z/q for every integer q>=2",
        "integer_annihilator": [int(value) for value in v],
        "every_coordinate_unit_image": [int(value) for value in v],
        "no_coordinate_unit_in_zero_row_lattice": True,
        "zero_row_dot_annihilator_all_zero": True,
        "lattice_column_HNF": [[int(value) for value in row] for row in H.tolist()],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lattice", action="store_true")
    args = parser.parse_args()
    result = {
        "status": "GLOBAL_M_BOUND_REFUTED_BY_EXPLICIT_ALL_GROUP_FAMILY",
        "base_family": [check(b) for b in range(2, 9)],
        "tensor_amplification": check(4, 2),
        "lattice_certificate": check_lattice() if args.lattice else None,
        "scope": "Exact finite checks support the displayed explicit formulas; formulas for all b,d are proved separately.",
    }
    path = Path(__file__).with_name("or_difference_counterexample_receipt.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"receipt": str(path), "base_b4": result["base_family"][2],
                      "tensor_d2": result["tensor_amplification"],
                      "lattice": {k: v for k, v in (result["lattice_certificate"] or {}).items()
                                  if k != "lattice_column_HNF"}}, indent=2))
