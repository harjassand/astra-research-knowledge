"""Exact Laurent check of the supplied three-wave compatible profile.

This is a finite example check only; it does not certify a global theorem.
All output stays beside this script in the assigned worker directory.
"""

import json
from pathlib import Path

import sympy as sp


z, w = sp.symbols("z w", nonzero=True)
I = sp.I
ca = (z + z**-1) / 2
cb = (w + w**-1) / 2
cc = (z * w + (z * w) ** -1) / 2

# psi = cos(x+y) + cos(x+2y) + cos(2x+3y), with phases z, w, zw.
# x1=cos(x+y), x2=cos(x+2y), x3=cos(2x+3y).
psi_xx = -(ca + cb + 4 * cc)
psi_xy = -(ca + 2 * cb + 6 * cc)
psi_yy = -(ca + 4 * cb + 9 * cc)

# phi = (psi_y/(3/2), psi_x), so X = D phi in row-major order.
X = sp.Matrix([sp.Rational(2, 3) * psi_xy,
               sp.Rational(2, 3) * psi_yy,
               psi_xx,
               psi_xy])
a, b, c, d = sp.symbols("a b c d", real=True)
variables = sp.Matrix([a, b, c, d])
u = a**2 + c**2
v = b**2 + d**2
q = a * d - b * c
G = 3 * (u + v - 2 * q) ** 2 + sp.Rational(35, 24) * u**2 + q**2 - sp.Rational(5, 2) * q * u
grad_G = sp.Matrix([sp.diff(G, x) for x in variables])
hess_G = sp.hessian(G, variables)


def average(expr):
    """Torus average over independent phases (x+y, x+2y)."""
    expanded = sp.expand(expr * z**8 * w**8)
    return sp.factor(sp.Poly(expanded, z, w).coeff_monomial(z**8 * w**8))


def sub_field(expr):
    return sp.expand(expr.subs(dict(zip(variables, X))))


c_value = average(sub_field(G))
b_value = sp.Matrix([average(sub_field(term)) for term in grad_G])
H_value = sp.Matrix(4, 4, lambda i, j: average(sub_field(hess_G[i, j])))
C_value = sp.Matrix(4, 4, lambda i, j: average(X[i] * X[j]))
det_H = sp.factor(H_value.det())
leading = [sp.factor(H_value[:k, :k].det()) for k in range(1, 5)]
gap = sp.factor(c_value - (b_value.T * H_value.inv() * b_value)[0] / 2)
B_opt = sp.simplify(-H_value.inv() * b_value)

# Transverse-to-e12 fourth mass and line fourth mass.
s = X[1]
Y2_pointwise = X[0] ** 2 + X[2] ** 2 + X[3] ** 2
Y4 = average(Y2_pointwise**2)
s2 = average(s**2)
s4 = average(s**4)
Y2 = average(Y2_pointwise)
det_X = sp.expand(X[0] * X[3] - X[1] * X[2])
norm2_X = sp.expand(sum(entry**2 for entry in X))
det2 = average(det_X**2)
norm4 = average(norm2_X**2)

result = {
    "profile": "psi=cos(x+y)+cos(x+2y)+cos(2x+3y); phi=(2/3 psi_y, psi_x)",
    "frequencies": [[1, 1], [1, 2], [2, 3]],
    "resonance": "(1,1)+(1,2)=(2,3)",
    "integrand": "G=3(u+v-2q)^2+(35/24)u^2+q^2-(5/2)qu",
    "c": str(c_value),
    "b": [str(x) for x in b_value],
    "H": [[str(H_value[i, j]) for j in range(4)] for i in range(4)],
    "covariance_C": [[str(C_value[i, j]) for j in range(4)] for i in range(4)],
    "covariance_rank": str(C_value.rank()),
    "covariance_eigenvalues_numeric": [float(sp.re(ev)) for ev in C_value.evalf().eigenvals().keys()],
    "H_leading_principal_minors": [str(x) for x in leading],
    "det_H": str(det_H),
    "optimized_gap": str(gap),
    "optimized_gap_over_E_normX4": str(sp.factor(gap / norm4)),
    "optimal_background_row_major": [str(x) for x in B_opt],
    "e12_L2_transverse_to_line_ratio_squared": str(sp.factor(Y2 / s2)),
    "e12_L4_transverse_to_line_ratio_fourth_power": str(sp.factor(Y4 / s4)),
    "E_detX_squared": str(det2),
    "E_normX_fourth": str(norm4),
    "universal_L4_distance_to_any_rank_one_line_lower_bound": str(sp.factor(sp.sqrt(det2 / norm4))),
    "source_cubic_mean_DG_I": str(average(sub_field(grad_G[0] + grad_G[3]))),
    "scope": "Exact finite Fourier integration of one compatible profile; not a uniform estimate or proof of quasiconvexity.",
}

Path(__file__).with_name("exact_resonant_profile.json").write_text(
    json.dumps(result, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, indent=2))
