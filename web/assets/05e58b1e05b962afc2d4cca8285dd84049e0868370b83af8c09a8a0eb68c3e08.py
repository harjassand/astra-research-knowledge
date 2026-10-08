"""Exact symbolic audit of the SU(3) Gram scalar factorization.

This verifies substitution/factorization only. The representation-independent
identity is proved in quadratic_adjoint_gram.txt.
"""

import sympy as sp

a, b = sp.symbols("a b", integer=True, positive=True)
c2 = (a**2 + a * b + b**2 + 3 * a + 3 * b) / 3
c3 = (a - b) * (2 * a + b + 3) * (a + 2 * b + 3) / 18
delta = sp.factor(c2 * (c2 / 3 + sp.Rational(1, 4)) - c3**2 / c2)
claimed = (
    a * b * (a + 2) * (b + 2) * (a + b + 1) * (a + b + 3)
    / (4 * (a**2 + a * b + b**2 + 3 * a + 3 * b))
)
assert sp.simplify(delta - claimed) == 0

for aa in range(1, 13):
    for bb in range(1, 13):
        value = claimed.subs({a: aa, b: bb})
        assert value > 0

print("PASS: exact Delta factorization and positivity for a,b=1,...,12")
