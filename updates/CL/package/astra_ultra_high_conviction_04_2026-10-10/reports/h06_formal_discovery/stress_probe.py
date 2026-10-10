#!/usr/bin/env python3
"""Exact stress probe for the candidate differential identity certificate.

Family: x^(2^k)-1 = (x-1) * product_{j<k}(x^(2^j)+1).
The script measures the dense expansion pressure and asks Z3's QF_NRA
solver whether the two real polynomials can differ, for fixed k.
This is a diagnostic comparison, not a proof-complexity theorem.
"""

from time import perf_counter

import sympy as sp
from z3 import Real, SolverFor, unsat


def family(k):
    x = sp.Symbol("x")
    powers = [x ** (2**j) for j in range(k + 1)]
    p = powers[k] - 1
    factors = [powers[j] + 1 for j in range(k)]
    a_expanded = sp.expand(sp.prod(factors))
    q = (x - 1) * sp.prod(factors)
    return x, p, q, a_expanded


def z3_check(k):
    x = Real(f"x_{k}")
    powers = [x]
    for _ in range(k):
        powers.append(powers[-1] * powers[-1])
    p = powers[k] - 1
    a = 1
    for j in range(k):
        a = a * (powers[j] + 1)
    q = (x - 1) * a
    solver = SolverFor("QF_NRA")
    solver.set(timeout=5000)
    solver.add(p != q)
    start = perf_counter()
    result = solver.check()
    elapsed = perf_counter() - start
    return result, elapsed


def main():
    print("k,degree,expanded_product_terms,expanded_lhs_rhs_terms,z3_qf_nra,seconds")
    for k in range(1, 13):
        x, p, q, a_expanded = family(k)
        rhs_expanded = sp.Poly(sp.expand((x - 1) * a_expanded), x)
        lhs_expanded = sp.Poly(sp.expand(p), x)
        assert rhs_expanded == lhs_expanded
        assert len(sp.Poly(a_expanded, x).terms()) == 2**k
        result, elapsed = z3_check(k)
        assert result == unsat
        print(
            f"{k},{2**k},{2**k},{len(rhs_expanded.terms())},"
            f"{result},{elapsed:.6f}"
        )


if __name__ == "__main__":
    main()
