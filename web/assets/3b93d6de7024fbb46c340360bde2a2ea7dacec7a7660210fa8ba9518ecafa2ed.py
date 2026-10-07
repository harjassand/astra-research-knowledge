"""Exact finite diagnostics for c10_l06's quantifier/interface audit.

Standard library only.  These checks verify the two boundary witnesses and
the exact factorial-potential jump ratios; they do not prove the infinite
quantifiers stated in the accompanying audit.
"""

from collections import deque
from fractions import Fraction
from math import factorial, prod
import json


REACTIONS = [
    ((2, 0), (-1, 1), "2A->A+B"),
    ((0, 2), (1, -1), "2B->A+B"),
]


def enabled(x, source):
    return all(a >= b for a, b in zip(x, source))


def successors(x):
    ans = []
    for source, nu, label in REACTIONS:
        if enabled(x, source):
            rate = prod(factorial(n) // factorial(n-k)
                        for n, k in zip(x, source))
            ans.append((tuple(a+b for a, b in zip(x, nu)), label, rate))
    return ans


def reachable(x):
    todo, seen = deque([x]), {x}
    while todo:
        y = todo.popleft()
        for z, _, _ in successors(y):
            if z not in seen:
                seen.add(z)
                todo.append(z)
    return seen


def falling(n, k):
    if n < k:
        return 0
    return prod(range(n-k+1, n+1))


def exp_factorial_potential(x):
    # exp(F(x)) = product_i x_i! / max_{available complex y} x_under_y.
    complexes = ((0, 0, 0), (0, 0, 1), (0, 1, 0),
                 (1, 1, 0), (1, 0, 1))
    max_falling = max(prod(falling(n, k) for n, k in zip(x, y))
                      for y in complexes if enabled(x, y))
    return prod(factorial(n) for n in x) // max_falling


def factorial_witness(a):
    x = (a, 0, 1)
    transitions = [
        ((a, 1, 0), "A+C->A+B", a),
        ((a, 0, 0), "C->0", 1),
        ((a, 0, 2), "0->C", 1),
    ]
    base = exp_factorial_potential(x)
    ratios = []
    for y, label, rate in transitions:
        ratios.append({"reaction": label, "rate": rate,
                       "expF_ratio": Fraction(exp_factorial_potential(y), base)})
    assert [r["expF_ratio"] for r in ratios] == [1, a, 1]
    return ratios


def main():
    # Exact strongly-endotactic sign witnesses for rational w on both sides.
    sign_witnesses = []
    for wa, wb in ((Fraction(2), Fraction(1)),
                   (Fraction(1), Fraction(2)),
                   (Fraction(1), Fraction(1))):
        if wa > wb:
            source, dot = "2A", -wa + wb
        elif wb > wa:
            source, dot = "2B", wa - wb
        else:
            source, dot = "tie", Fraction(0)
        assert dot <= 0
        sign_witnesses.append({"w": [str(wa), str(wb)],
                               "maximal_source": source,
                               "maximal_edge_dot": str(dot)})

    total_one = {(1, 0), (0, 1)}
    assert all(not successors(x) for x in total_one)
    total_two = {(2, 0), (1, 1), (0, 2)}
    reach_a = reachable((2, 0))
    reach_b = reachable((0, 2))
    assert reach_a == {(2, 0), (1, 1)}
    assert reach_b == {(0, 2), (1, 1)}
    assert not successors((1, 1))
    assert all(sum(x) == 2 for x in total_two)

    # The positive deterministic class x_A+x_B=c has a global linear flow
    # dot(a)=c^2-2ca, whose exact equilibrium is c/2.
    c, a0 = Fraction(1), Fraction(1, 4)
    ode_drift = c*c - 2*c*a0
    assert ode_drift == Fraction(1, 2)
    assert Fraction(0) < a0 < c

    # Independently reconstruct N76's exact jump ratios on A+C state (a,0,1).
    f_checks = {str(a): factorial_witness(a) for a in (2, 3, 7, 25)}
    out = {
        "status": "PASS_FINITE_DIAGNOSTICS",
        "network": "2A->A+B; 2B->A+B",
        "direction_sign_witnesses": sign_witnesses,
        "total_one_absorbing": sorted(total_one),
        "total_two_reachability_from_2A": sorted(reach_a),
        "total_two_reachability_from_2B": sorted(reach_b),
        "total_two_center_successors": successors((1, 1)),
        "positive_ode_fixture": {"c": str(c), "a0": str(a0),
                                  "a_dot": str(ode_drift),
                                  "equilibrium_a": str(c/2)},
        "factorial_potential_ratio_checks": f_checks,
        "scope": "finite exact diagnostics only; all-state claims are proved in text",
    }
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
