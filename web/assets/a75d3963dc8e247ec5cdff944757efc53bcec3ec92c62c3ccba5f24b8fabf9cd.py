#!/usr/bin/env python3
"""Exact SymPy checks for a periodic determinant-one Sol mapping-torus path."""
import json
import sympy as sp


t, H, a, b = sp.symbols("t H a b", real=True)
pi = sp.pi
u = a * sp.sin(2 * pi * t)
v = b * sp.sin(2 * pi * t)
up = sp.diff(u, t)
vp = sp.diff(v, t)
A = 2 * H + up

g11 = sp.exp(2 * H * t + u)
g12 = v
g22 = sp.exp(-2 * H * t - u) * (1 + v**2)
G = sp.Matrix([[g11, g12], [g12, g22]])
Gdot = G.diff(t)
C = sp.simplify(G.inv() * Gdot)
kappa2_from_matrix = sp.simplify(C[0, 0] ** 2 + C[0, 1] * C[1, 0])
s2_from_matrix = sp.simplify(kappa2_from_matrix / 4)
s2_from_upper_half_plane = sp.simplify((A**2 + (A * v - vp) ** 2) / 4)
speed_identity = sp.trigsimp(sp.simplify(s2_from_matrix - s2_from_upper_half_plane))

integral_s2 = sp.simplify(sp.integrate(s2_from_upper_half_plane, (t, 0, 1)))
defect_formula = sp.simplify(
    integral_s2 - H**2 - (pi**2 * a**2 / 2 + b**2 * H**2 / 2 + pi**2 * b**2 / 2 + pi**2 * a**2 * b**2 / 8)
)

det_identity = sp.simplify(sp.det(G) - 1)
A_matrix = sp.diag(sp.exp(H), sp.exp(-H))
endpoint_identity = sp.simplify(G.subs(t, 1) - A_matrix.T * G.subs(t, 0) * A_matrix)

result = {
    "status": "PASS" if speed_identity == 0 and defect_formula == 0 and det_identity == 0 and endpoint_identity == sp.zeros(2) else "FAIL",
    "checks": {
        "det_G_equals_one": det_identity == 0,
        "endpoint_gluing_for_A_diag_exp_H": endpoint_identity == sp.zeros(2),
        "hyperbolic_speed_equals_2s": speed_identity == 0,
        "exact_integrated_power_defect": defect_formula == 0,
    },
    "squared_speed": str(sp.factor(s2_from_upper_half_plane)),
    "integral_s_squared": str(sp.factor(integral_s2)),
    "power_defect": str(sp.factor(integral_s2 - H**2)),
    "scope": "Exact symbolic identities for the explicit sinusoidal path only; not a proof of the general projective or CAT(0) statements, nor a certified numerical interval.",
}
print(json.dumps(result, indent=2, sort_keys=True))
if result["status"] != "PASS":
    raise SystemExit(1)
