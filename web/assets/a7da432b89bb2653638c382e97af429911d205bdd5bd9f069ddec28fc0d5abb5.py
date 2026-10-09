"""Scoped exact replay of the independent driven-qubit calculation.

This checks the full physical Lindblad formula, Bloch coefficients and
stationarity for this one family. It does not test the universal target.
"""
import json
import sympy as sp

k = sp.symbols("k", positive=True)
g, v, x, z = sp.symbols("g v x z", real=True)
K = sp.Matrix([[g, -v * sp.sqrt(k)], [v / sp.sqrt(k), -g]])
D = K.T * K
q = g * v * (k + 1) ** 2 / (2 * sp.sqrt(k) * (k - 1))
Q = sp.Matrix([[0, sp.I * q], [-sp.I * q, 0]])
rho = sp.Matrix([[(1 + z) / 2, x / 2], [x / 2, (1 - z) / 2]])
drho = K * rho * K.T - (D * rho + rho * D) / 2 - sp.I * (Q * rho - rho * Q)
m = (k**2 - 1) / (k**2 + 1)
xdot = -(2 * g**2 + v**2 * (k + 1) ** 2 / (2 * k)) * x
xdot -= 2 * g * v * (k**2 + 1) * (z - m) / (sp.sqrt(k) * (k - 1))
zdot = 4 * g * v * sp.sqrt(k) * x / (k - 1) - v**2 * (k + 1 / k) * (z - m)
assert sp.simplify(2 * drho[0, 1] - xdot) == 0
assert sp.simplify(2 * drho[0, 0] - zdot) == 0
assert sp.simplify(sp.trace(drho)) == 0
assert sp.simplify(drho.subs({x: 0, z: m})) == sp.zeros(2)
assert sp.simplify(Q.conjugate().T - Q) == sp.zeros(2)
print(json.dumps({"exact_checks": 5, "status": "PASS_SCOPED_FAMILY_ONLY", "sympy": sp.__version__}))
