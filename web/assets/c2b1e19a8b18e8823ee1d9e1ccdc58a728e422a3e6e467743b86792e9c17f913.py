#!/usr/bin/env python3
"""Exact Fraction checks for the two certificate fixtures in the leaf report.

This verifies the displayed arithmetic only; it is not an LP solver, a proof
of the general inequalities, or a recurrence checker.
"""

from fractions import Fraction as F


def check_feasible_shared_substrate_example():
    # Two catalysts, one shared substrate; delta=beta_minus=1,
    # beta_plus=gamma_plus=3/4, k=1, epsilon=1/100.
    lam = [F(1), F(1)]
    v = F(4, 5)
    eps = F(1, 100)
    p = [x - F(3, 4) * v for x in lam]
    q = [v - F(3, 4) * x - eps for x in lam]
    assert p == [F(2, 5), F(2, 5)]
    assert q == [F(1, 25), F(1, 25)]
    assert v > F(3, 4) * max(lam)
    assert all(x > F(3, 4) * v for x in lam)

    # Natural summed comparison matrix M has all entries 9/16.
    # Its eigenvalues are 9/8 and 0, so rho(M)=9/8>1 despite LP feasibility.
    assert 2 * F(9, 16) == F(9, 8)


def check_infeasible_unit_gain_dual():
    # z=(lambda,v,t). Rows Gz>=0: lambda-v-t, v-lambda-t,
    # lambda-t, v-t. The first two rows with multipliers (1/2,1/2)
    # give -G^T u = (0,0,1) = e_t, proving t<=0 in the dual.
    rows = [
        (F(1), F(-1), F(-1)),
        (F(-1), F(1), F(-1)),
        (F(1), F(0), F(-1)),
        (F(0), F(1), F(-1)),
    ]
    multipliers = [F(1, 2), F(1, 2), F(0), F(0)]
    minus_gt_u = tuple(
        -sum(multipliers[r] * rows[r][c] for r in range(len(rows)))
        for c in range(3)
    )
    assert minus_gt_u == (F(0), F(0), F(1))


if __name__ == "__main__":
    check_feasible_shared_substrate_example()
    check_infeasible_unit_gain_dual()
    print("PASS: exact feasible primal slacks and exact zero-margin dual")
