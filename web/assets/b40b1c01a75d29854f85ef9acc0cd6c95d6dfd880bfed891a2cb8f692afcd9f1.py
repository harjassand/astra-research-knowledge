"""Exact rational check for the two-phase TCR-observation alias witness.

This is a finite symbolic-algebra diagnostic, not a biological model fit.
The all-time identity follows from the checked similarity relation.
"""

import json

import sympy as sp


t, delta = sp.symbols("t delta", nonnegative=True)
TA = sp.Matrix([[-3, 1], [0, -1]])
rA = sp.Matrix([2, 1])
alphaA = sp.Matrix([[1, 0]])
S = sp.Matrix([[1, 0], [sp.Rational(1, 4), sp.Rational(3, 4)]])
TB = S.inv() * TA * S
rB = S.inv() * rA
alphaB = alphaA * S
one = sp.ones(2, 1)

assert TB == sp.Matrix(
    [
        [-sp.Rational(11, 4), sp.Rational(3, 4)],
        [sp.Rational(7, 12), -sp.Rational(5, 4)],
    ]
)
assert rB == sp.Matrix([2, sp.Rational(2, 3)])
assert alphaB == alphaA
assert TA * one + rA == sp.zeros(2, 1)
assert TB * one + rB == sp.zeros(2, 1)
assert TA[0, 1] > 0 and TA[1, 0] == 0
assert TB[0, 1] > 0 and TB[1, 0] > 0
assert all(x > 0 for x in rA)
assert all(x > 0 for x in rB)

# The Laplace transform of the activation-time density is the success
# probability before an independent Exp(delta) ligand-off clock.
I = sp.eye(2)
laplaceA = sp.factor((alphaA * (delta * I - TA).inv() * rA)[0])
laplaceB = sp.factor((alphaB * (delta * I - TB).inv() * rB)[0])
assert sp.simplify(laplaceA - laplaceB) == 0
assert sp.simplify(laplaceA - ((sp.Rational(3, 2) / (delta + 3)) + (sp.Rational(1, 2) / (delta + 1)))) == 0

# An extra phase-2 occupancy observation differs. The similarity implies the
# B-model occupancy row equals the A-model occupancy row times S.
rowA = alphaA * sp.exp(TA * t)
rowB = alphaB * sp.exp(TB * t)
assert sp.simplify(rowB - rowA * S) == sp.zeros(1, 2)
qA = sp.simplify(rowA[0, 1])
qB = sp.simplify(rowB[0, 1])
assert sp.simplify(qA - (sp.exp(-t) - sp.exp(-3 * t)) / 2) == 0
assert sp.simplify(qB - sp.Rational(3, 4) * qA) == 0
t_star = sp.log(3) / 2
gap = sp.simplify((qA - qB).subs(t, t_star))
assert gap == 1 / (12 * sp.sqrt(3))

print(
    json.dumps(
        {
            "TB": [[str(x) for x in row] for row in TB.tolist()],
            "rB": [str(x) for x in rB],
            "alphaB": [str(x) for x in alphaB],
            "laplace_transform": str(laplaceA),
            "activation_density": "3*exp(-3*t)/2 + exp(-t)/2",
            "phase2_occupancy_A": "(exp(-t)-exp(-3*t))/2",
            "phase2_occupancy_B": "3/4 * phase2_occupancy_A",
            "max_phase2_gap": str(gap),
            "max_gap_time": "log(3)/2",
            "scope": "exact algebraic witness only; no biological validation",
        },
        indent=2,
    )
)
