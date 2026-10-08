"""Exact small-sector check for open hard-core bosons with range-1/2 repulsion."""

import sympy as sp


J = sp.Integer(1)
U = sp.Integer(1)  # V_{i,i+1}
V = sp.Integer(2)  # V_{i,i+2}

# N=3, m=2, ordered particle configurations |1,2>, |1,3>, |2,3>.
H0 = sp.Matrix([
    [8, -2, 0],
    [-2, 8, -2],
    [0, -2, 8],
])
W = sp.diag(U, V, U)
HV = H0 + W
x = sp.Symbol("x")

assert sp.simplify(H0.charpoly(x).as_expr() - (x - 8) * ((x - 8) ** 2 - 8)) == 0
assert W == sp.diag(1, 2, 1) and all(v >= 0 for v in W.diagonal())
assert HV - H0 == W
assert all(v == 1 for v in H0.eigenvals().values())
assert {sp.simplify(e) for e in H0.eigenvals()} == {
    sp.Integer(8), 8 - 2 * sp.sqrt(2), 8 + 2 * sp.sqrt(2)
}

print("PASS: N=3,m=2 free spectrum is 8-2√2, 8, 8+2√2; added finite-range repulsion is PSD.")
print(f"Interacting exact matrix: {HV.tolist()}")
