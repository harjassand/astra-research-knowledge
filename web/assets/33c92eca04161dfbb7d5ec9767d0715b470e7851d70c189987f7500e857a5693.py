"""One legal complex boundary control plus Fourier parity; no scan.

Run: python3 work/agents/broadcasting_proof_sol/cycle08_pure_boundary_review/exposed_phase_control.py
Dependencies: Python 3, SymPy. Exact algebra, no floating point or file writes.
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


alpha = [sp.Integer(1), sp.Integer(2), sp.Integer(4)]
sigma = sp.diag(1, 4, 16) / 21
s = sp.diag(*alpha) / sp.sqrt(21)
sh = sp.diag(1, sp.sqrt(2), 2) / 21 ** sp.Rational(1, 4)
psi = sp.Matrix([1, sp.sqrt(2), 2]) / sp.sqrt(7)
P = psi * psi.H
w = sp.Matrix([1, sp.I, -1-sp.I])
B = w * w.H
V = sp.Matrix(3, 3, lambda i, j: 22 * B[i, j] / (alpha[i]+alpha[j]))
K = sh * B * sh.inv()
G = sh * V * sh.inv()
u = sh.inv() * psi
C = B * s * B
W = sp.diag(*u).H * C * sp.diag(*u)


def H(X):
    return (V * X + X * V) / 2 - B * X * B


def Ls(X):
    return (G * X + X * G.H) / 2 - K * X * K.H


equal(s*s, sigma)
equal(sh*sh, s)
equal(B.H, B)
equal(V.H, V)
equal(s*V+V*s, 2*C)
equal(G+G.H, 2*K.H*K)
equal(Ls(sigma), sp.zeros(3))
equal(K*psi, sp.zeros(3, 1))
equal(B*u, sp.zeros(3, 1))
equal(W, 11*B/7)
equal(W*sp.ones(3, 1), sp.zeros(3, 1))
equal(sp.im(W[0, 1]), -sp.Rational(11, 7))
equal(sp.trace(P*Ls(P)), 0)
equal(sp.trace(Ls(P)), 0)

W_factors = sp.zeros(3)
for ell in range(3):
    wl = sp.sqrt(s[ell, ell]) * B[:, ell]
    a = wl.conjugate().multiply_elementwise(u)
    equal(sum(a), 0)
    W_factors += a.conjugate() * a.T
equal(W_factors, W)

log_sigma = sp.diag(*[sp.log(sigma[i, i]) for i in range(3)])
J = sp.simplify(sp.expand_log(-sp.trace(Ls(P)*log_sigma), force=True))
Q = sp.simplify((psi.H*V*psi)[0])
m = sp.simplify((psi.H*B*psi)[0])
E = sp.simplify(sp.trace(P*H(P)))
h = sp.Matrix(3, 3, lambda i, j: 2*sp.sqrt(alpha[i]*alpha[j])/(alpha[i]+alpha[j]))
f = sp.Matrix(3, 3, lambda i, j: sp.log(alpha[i]/alpha[j])*(alpha[i]-alpha[j])/(alpha[i]+alpha[j]))
gram_Q = sum(W[i, j]*h[i, j] for i in range(3) for j in range(3))
gram_J = -sum(W[i, j]*f[i, j] for i in range(3) for j in range(3))
equal(sp.expand_log(gram_J, force=True), J)
equal(gram_Q, Q)
equal(E, Q-m*m)
equal(J, sp.Rational(506, 105)*sp.log(2))
equal(Q, sp.Rational(132, 35)-sp.Rational(44, 21)*sp.sqrt(2))
equal(m, 1-sp.Rational(4, 7)*sp.sqrt(2))
equal(E, sp.Rational(519, 245)-sp.Rational(20, 21)*sp.sqrt(2))

# Generic centered complex coefficients at equally spaced log frequencies.
# The imaginary Fourier phase is evaluated at exp(i theta)=i exactly.
a = sp.Matrix([1, sp.I, -1-sp.I])
equal(sum(a), 0)
F_plus = sum(a[j]*sp.I**j for j in range(3))
F_minus = sum(a[j]*(-sp.I)**j for j in range(3))
plus_norm = sp.expand_complex(F_plus*sp.conjugate(F_plus))
minus_norm = sp.expand_complex(F_minus*sp.conjugate(F_minus))
cosine = sp.Matrix(3, 3, lambda i, j: sp.cos((i-j)*sp.pi/2))
equal(plus_norm, 2)
equal(minus_norm, 10)
equal((a.H*cosine*a)[0], (plus_norm+minus_norm)/2)

print(json.dumps({'status':'PASS','exact_assertions':assertions,
                  'sympy':sp.__version__,'physical_J':str(J),
                  'physical_E':str(E),'complex_fourier_modulus_squares':[2,10],
                  'scope':'one exact legal complex jump and parity control; no theorem by sampling'}, indent=2))
