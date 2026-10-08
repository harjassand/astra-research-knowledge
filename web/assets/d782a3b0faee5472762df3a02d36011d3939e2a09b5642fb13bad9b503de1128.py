"""Symbolically verify the two-mode observability algebra used in the note."""
import sympy as sp

a, b, lam, mu, r0, d0 = sp.symbols(
    "a b lam mu r0 d0", nonzero=True
)
O = sp.Matrix([[a, b], [a * lam, b * mu]])
y0 = a * r0 + b * d0
y1 = a * lam * r0 + b * mu * d0

assert sp.simplify(O.det() - a * b * (mu - lam)) == 0
assert sp.simplify((mu * y0 - y1) / (a * (mu - lam)) - r0) == 0
assert sp.simplify((y1 - lam * y0) / (b * (mu - lam)) - d0) == 0

# State-coordinate similarity leaves every output unchanged.
S = sp.Matrix([[1, 1], [0, 1]])
z = sp.Matrix([r0, d0])
A = sp.diag(lam, mu)
C = sp.Matrix([[a, b]])
A2 = S * A * S.inv()
C2 = C * S.inv()
z2 = S * z
for t in range(5):
    assert sp.simplify((C2 * A2**t * z2)[0] - (C * A**t * z)[0]) == 0

print("observability determinant/inverse verified; similarity invariance verified for t=0..4")
