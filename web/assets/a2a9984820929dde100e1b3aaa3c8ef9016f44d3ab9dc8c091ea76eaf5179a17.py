#!/usr/bin/env python3
"""Exact finite check of the stochastic-top-tier subset D-top-tier condition.

The checker uses only Fraction arithmetic. For each nonempty set I of
coordinates tending to infinity, and each bounded-coordinate value b below
the coordinatewise complex maxima, enabled source complexes are selected.
It tests whether an enabled source y can maximize the stochastic monomial
order while some unavailable source z has strictly larger deterministic
monomial order. The latter is a bounded rational LP; its vertices are
enumerated exactly.

This checks the sufficient hypothesis in Theorem 6.1 of
Anderson--Cappelletti--Kim, arXiv:1904.08967v2, on the whole lattice. It is
not a decision procedure for weakly reversible positive recurrence.
"""

from fractions import Fraction as Q
from itertools import combinations, product
import json


COMPLEXES = (
    (1, 0, 0, 3),  # A + 3D
    (1, 1, 0, 3),  # A + B + 3D
    (1, 0, 1, 3),  # A + C + 3D
    (0, 0, 1, 3),  # C + 3D
    (0, 2, 0, 3),  # 2B + 3D
)


def solve_square(A, b):
    """Solve A x=b over Q; return None if singular."""
    n = len(b)
    M = [[Q(v) for v in A[i]] + [Q(b[i])] for i in range(n)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if M[r][col]), None)
        if pivot is None:
            return None
        M[col], M[pivot] = M[pivot], M[col]
        scale = M[col][col]
        M[col] = [v / scale for v in M[col]]
        for r in range(n):
            if r == col or not M[r][col]:
                continue
            scale = M[r][col]
            M[r] = [M[r][j] - scale * M[col][j] for j in range(n + 1)]
    return tuple(M[i][-1] for i in range(n))


def lp_has_positive_margin(y, z, active, I):
    """Is there w>0 with y top on active and z strictly above y globally?

    Normalize sum(w)=1. A common margin delta encodes w_i>0 and
    w.(z-y)>0. The compact feasible polytope has a positive-delta point iff
    one of its vertices does.
    """
    p = len(I)
    nvar = p + 1  # weights followed by delta
    constraints = []  # a dot u >= b

    # 0 <= delta <= 1; w_i >= delta.
    a = [Q(0)] * p + [Q(1)]
    constraints.append((tuple(a), Q(0)))
    a = [Q(0)] * p + [Q(-1)]
    constraints.append((tuple(a), Q(-1)))
    for i in range(p):
        a = [Q(0)] * nvar
        a[i], a[-1] = Q(1), Q(-1)
        constraints.append((tuple(a), Q(0)))

    # y maximizes w dot source over the enabled set.
    for u in active:
        a = [Q(y[j] - u[j]) for j in I] + [Q(0)]
        constraints.append((tuple(a), Q(0)))

    # A source z outside the enabled set beats y by at least delta.
    a = [Q(z[j] - y[j]) for j in I] + [Q(-1)]
    constraints.append((tuple(a), Q(0)))

    # Equality sum(w)=1 plus p active inequalities gives a vertex.
    eq = [Q(1)] * p + [Q(0)]
    for chosen in combinations(range(len(constraints)), p):
        A = [eq] + [constraints[k][0] for k in chosen]
        b = [Q(1)] + [constraints[k][1] for k in chosen]
        sol = solve_square(A, b)
        if sol is None:
            continue
        if all(sum(a[j] * sol[j] for j in range(nvar)) >= rhs
               for a, rhs in constraints):
            if sol[-1] > 0:
                return True, tuple(sol)
    return False, None


def check_top_tier_inclusion(complexes):
    d = len(complexes[0])
    # Enabled-source sets change only when a bounded coordinate crosses a
    # source exponent. This is bit-size robust in the exponent values.
    levels = [sorted(set([0] + [y[i] for y in complexes])) for i in range(d)]
    cases = 0
    lp_tests = 0
    for mask in range(1, 1 << d):
        I = tuple(i for i in range(d) if (mask >> i) & 1)
        bounded = tuple(i for i in range(d) if i not in I)
        ranges = [levels[i] for i in bounded]
        for bvals in product(*ranges):
            b = dict(zip(bounded, bvals))
            active = tuple(y for y in complexes
                           if all(y[i] <= b[i] for i in bounded))
            if not active:
                continue  # this asymptotic stratum has no enabled reaction
            cases += 1
            if len(active) == len(complexes):
                continue
            for y in active:
                for z in complexes:
                    if z in active:
                        continue
                    lp_tests += 1
                    witness, weights = lp_has_positive_margin(y, z, active, I)
                    if witness:
                        return {
                            "accepted": False,
                            "dimension": d,
                            "complexes": len(complexes),
                            "bounded_values": b,
                            "diverging_coordinates": list(I),
                            "enabled_sources": [list(v) for v in active],
                            "stochastic_top_candidate": list(y),
                            "deterministic_higher_source": list(z),
                            "positive_rational_weight_witness": [str(v) for v in weights],
                            "strata_checked": cases,
                            "lp_tests": lp_tests,
                        }
    return {
        "accepted": True,
        "dimension": d,
        "complexes": len(complexes),
        "strata_checked": cases,
        "lp_tests": lp_tests,
        "method": "exact rational vertex enumeration",
    }


if __name__ == "__main__":
    result = check_top_tier_inclusion(COMPLEXES)
    result["fixture"] = "A+3D -> A+B+3D -> A+C+3D -> C+3D -> 2B+3D -> A+3D"
    result["rates"] = [1, 1, 2, 1, 1]
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["accepted"]:
        raise SystemExit(1)
