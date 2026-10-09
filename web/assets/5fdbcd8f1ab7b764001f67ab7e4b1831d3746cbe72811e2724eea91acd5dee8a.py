"""One exact noncommuting, complex-noise control; not a state scan.

Uses SymPy 1.14.0. No numerical optimization or approximate matrix logs.
All nodes are integer multiples of log(2), so the hyperbolic kernel is
evaluated as rational/algebraic powers of two.
"""
import json
import sympy as sp

R = sp.Rational
I = sp.I
rt2 = sp.sqrt(2)
rt5 = sp.sqrt(5)
ell = sp.log(2)
eye = sp.eye(2)
py = sp.Matrix([[0, -I], [I, 0]])
pz = sp.diag(1, -1)
s = sp.diag(1, 2) / rt5
d = sp.diag(1, rt2)  # The omitted common scalar cancels in conjugations.
B = sp.Matrix([[1, 1 + I], [1 - I, -1]])
q = (3 * eye + py) / (2 * rt5)
rho = sp.simplify(q * q)
sigma = s * s
V = sp.zeros(2)
BsB = B * s * B
for i in range(2):
    for j in range(2):
        V[i, j] = sp.simplify(2 * BsB[i, j] / (s[i, i] + s[j, j]))
C = sp.simplify(d * V * d.inv())
K = sp.simplify(d * B * d.inv())
assert sp.simplify(C + C.adjoint() - 2 * K.adjoint() * K) == sp.zeros(2)
Lrho = sp.simplify((C * rho + rho * C.adjoint()) / 2 - K * rho * K.adjoint())
Lsigma = sp.simplify((C * sigma + sigma * C.adjoint()) / 2 - K * sigma * K.adjoint())
assert Lsigma == sp.zeros(2)
assert sp.trace(Lrho) == 0
J = sp.simplify(sp.trace(Lrho * (py + pz)) * ell)
Hq = (V * q + q * V) / 2 - B * q * B
E = sp.simplify(sp.trace(q * Hq))
assert sp.simplify(J - (R(57, 10) + R(9, 5) * rt2) * ell) == 0
assert sp.simplify(E - R(13, 10)) == 0

components = {
    -1: sp.Matrix([[0, 1 + I], [0, 0]]),
    0: pz,
    1: sp.Matrix([[0, 0], [1 - I, 0]]),
}
projectors = {0: (eye - py) / 2, 1: (eye + py) / 2}
qvalues = {0: 1 / rt5, 1: 2 / rt5}

def sh(n):
    return (sp.Integer(2) ** R(n, 2) - sp.Integer(2) ** R(-n, 2)) / 2

def ch(n):
    return (sp.Integer(2) ** R(n, 2) + sp.Integer(2) ** R(-n, 2)) / 2

Jgram = sp.Integer(0)
Egram = sp.Integer(0)
for a in projectors:
    for b in projectors:
        for w in components:
            for v in components:
                Uw = projectors[b] * components[w] * projectors[a]
                Uv = projectors[b] * components[v] * projectors[a]
                g = sp.simplify(sp.trace(Uw.adjoint() * Uv))
                x = a - b + w
                y = a - b + v
                Kzero = ell * (x * sh(2 * y) + y * sh(2 * x)) / (2 * ch(x - y))
                Kenergy = sh(x) * sh(y) / ch(x - y)
                Jgram += 2 * qvalues[a] * qvalues[b] * Kzero * g
                Egram += 2 * qvalues[a] * qvalues[b] * Kenergy * g
Jgram = sp.simplify(Jgram)
Egram = sp.simplify(Egram)
assert sp.simplify(Jgram - J) == 0
assert sp.simplify(Egram - E) == 0
assert rho * sigma != sigma * rho
assert C != C.adjoint()

print(json.dumps({
    "status": "EXACT_CONTROL_PASS",
    "sympy_version": sp.__version__,
    "J": str(J),
    "E": str(E),
    "physical_and_spectral_gram_equal": True,
    "noncommuting_rho_sigma": True,
    "complex_noise": True,
    "nonsymmetric_physical_drift": True,
    "finite_control_count": 1,
    "state_scan_or_optimizer": False,
}, indent=2))
