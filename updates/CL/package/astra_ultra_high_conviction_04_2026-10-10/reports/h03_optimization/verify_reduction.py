"""Exact symbolic check of the frozen three-variable reduction example."""
import sympy as sp

x, y, z = sp.symbols("x y z")
vars_ = (x, y, z)
u = sp.Matrix([1, 1, 1])
Q0 = sp.diag(2, 3, 4)
t = x + y + z
f = (sp.Matrix(vars_).T * Q0 * sp.Matrix(vars_))[0] / 2 + t**4 - 2 * t**2
H = sp.hessian(f, vars_)

# Coefficient matrices of nonconstant Hessian monomials span the active space.
poly_entries = [sp.Poly(H[i, j], *vars_) for i in range(3) for j in range(3)]
monomials = sorted(set().union(*(set(p.monoms()) for p in poly_entries)))
active_columns = []
for mon in monomials:
    if mon == (0, 0, 0):
        continue
    coeff_matrix = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            coeff_matrix[i, j] = sp.Poly(H[i, j], *vars_).coeff_monomial(mon)
    active_columns.extend(coeff_matrix.columnspace())
active_rank = sp.Matrix.hstack(*active_columns).rank()
assert active_rank == 1
assert sp.simplify(H - Q0 + 4 * (u * u.T) - 12 * t**2 * (u * u.T)) == sp.zeros(3, 3)

G = (u.T * Q0.inv() * u)[0]
T = sp.symbols("T")
F = sp.expand(T**4 - 2 * T**2 + T**2 / (2 * G))
critical = sp.solve(sp.diff(F, T), T)
minimizers = [r for r in critical if sp.simplify(F.subs(T, r) - sp.Rational(-100, 169)) == 0]
assert sp.simplify(G - sp.Rational(13, 12)) == 0
assert sp.simplify(F - (T**4 - sp.Rational(20, 13) * T**2)) == 0
assert len(minimizers) == 2
assert sp.simplify(minimizers[0]**2 - sp.Rational(10, 13)) == 0
assert sp.simplify(minimizers[1]**2 - sp.Rational(10, 13)) == 0

print("active_dimension=", active_rank)
print("G=", G)
print("reduced_objective=", F)
print("global_value=", -sp.Rational(100, 169))
print("minimizers_t=", minimizers)
