"""Exact finite boundary control; diagnostic, not the theorem's proof.

Run: python3 work/agents/broadcasting_proof_sol/cycle08_pure_boundary_review/exact_control.py
Dependencies: Python 3 and SymPy. No floating point, searches, or file writes.
"""
import json
import sympy as sp

assertions = 0


def equal(a, b):
    global assertions
    if isinstance(a, sp.MatrixBase):
        assert a.shape == b.shape
        assert all(sp.simplify(x) == 0 for x in a - b)
    else:
        assert sp.simplify(a - b) == 0
    assertions += 1


sigma = sp.diag(1, 4) / 5
s = sp.diag(1, 2) / sp.sqrt(5)
s_half = sp.diag(1, sp.sqrt(2)) / 5 ** sp.Rational(1, 4)
s_minus_half = s_half.inv()
B = sp.Matrix([[1, -1], [-1, 1]])
V = sp.Matrix([[3, -2], [-2, sp.Rational(3, 2)]])
psi = sp.Matrix([1, sp.sqrt(2)]) / sp.sqrt(3)
P = psi * psi.H
K = s_half * B * s_minus_half
G = s_half * V * s_minus_half
C = B * s * B
u = s_minus_half * psi
U = sp.diag(*u)
W = U.H * C * U


def H(X):
    return (V * X + X * V) / 2 - B * X * B


def L_star(X):
    return (G * X + X * G.H) / 2 - K * X * K.H


equal(s * s, sigma)
equal(s_half * s_half, s)
equal(s * V + V * s, 2 * C)
equal(G + G.H, 2 * K.H * K)
equal(H(s), sp.zeros(2))
equal(L_star(sigma), sp.zeros(2))
equal((psi.H * psi)[0], 1)
equal(P * P, P)
equal(K * psi, sp.zeros(2, 1))
equal(B * u, sp.zeros(2, 1))
equal((u.H * s * u)[0], 1)
equal(W, sp.Matrix([[1, -1], [-1, 1]]))
equal(W * sp.ones(2, 1), sp.zeros(2, 1))
equal(L_star(P), sp.Matrix([[sp.Rational(1, 3), sp.sqrt(2)/12],
                          [sp.sqrt(2)/12, -sp.Rational(1, 3)]]))
equal(sp.trace(P * L_star(P)), 0)
equal(sp.trace(L_star(P)), 0)
equal(sp.det(V), sp.Rational(1, 2))
log_sigma = sp.diag(sp.log(sp.Rational(1, 5)), sp.log(sp.Rational(4, 5)))
J = sp.expand_log(-sp.trace(L_star(P) * log_sigma), force=True)
E = sp.trace(P * H(P))
Q = (psi.H * V * psi)[0]
m = (psi.H * B * psi)[0]
equal(J, 2 * sp.log(2) / 3)
equal(Q, 2 - 4 * sp.sqrt(2) / 3)
equal(m, (3 - 2 * sp.sqrt(2)) / 3)
equal(E, sp.Rational(1, 9))
equal(Q - m**2, E)
equal(J / E, 6 * sp.log(2))

shift = sp.Symbol('shift', real=True)
B_shift = B - shift * sp.eye(2)
V_shift = V - 2 * shift * B + shift**2 * sp.eye(2)
equal(s * V_shift + V_shift * s, 2 * B_shift * s * B_shift)
for i in range(2):
    for j in range(2):
        X = sp.zeros(2)
        X[i, j] = 1
        equal((V_shift * X + X * V_shift) / 2 - B_shift * X * B_shift, H(X))

print(json.dumps({'status': 'PASS', 'exact_assertions': assertions,
                  'sympy': sp.__version__,
                  'boundary_J': str(J), 'pure_energy': str(sp.simplify(E)),
                  'ratio': str(sp.simplify(J / E)),
                  'stationary_pure_state': False}, indent=2))
