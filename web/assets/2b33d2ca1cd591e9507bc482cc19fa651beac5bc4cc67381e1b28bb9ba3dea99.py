"""Exact checks for the qubit cloner slice-ansatz obstruction."""
import sympy as s

d = s.symbols('d', positive=True, integer=True)
lambda_d = (d + 2) / (2 * (d + 1))
c_slice_d = s.factor((1 - lambda_d**2 / (d + 1)) / (1 - lambda_d))
assert s.factor(c_slice_d - (2 + (3 * d + 4) / (2 * (d + 1)**2))) == 0
assert s.simplify(c_slice_d.subs(d, 2) - s.Rational(23, 9)) == 0
assert s.factor(s.diff((3 * d + 4) / (2 * (d + 1)**2), d) + (3 * d + 5) / (2 * (d + 1)**3)) == 0

I2 = s.eye(2)
sigmas = [
    s.Matrix([[0, 1], [1, 0]]),
    s.Matrix([[0, -s.I], [s.I, 0]]),
    s.Matrix([[1, 0], [0, -1]]),
]
P = [(I2 + sign * q) / 2 for q in sigmas for sign in (1, -1)]
Q = [q / 3 for q in P]

def tau(x):
    return s.trace(x) / 2

def Phi(x):
    return s.Rational(2, 3) * x + s.Rational(1, 3) * tau(x) * I2

def Pmap(x, effects):
    return 2 * sum((tau(q * x) * p for q, p in effects), s.zeros(2))

effects = list(zip(Q, P))
S = s.zeros(3)
for q, p in effects:
    n = s.Matrix([s.trace(p * sig) for sig in sigmas])
    # q=tP with t=Tr(q); S=(1/2) sum t nn^T.
    S += s.trace(q) * (n * n.T) / 2
assert S == s.eye(3) / 3
assert sum((q for q in Q), s.zeros(2)) == I2

# Verify Pmap's action and the composed canonical slice comparator.
for j, sig in enumerate(sigmas):
    assert s.simplify(Pmap(sig, effects) - sig / 3) == s.zeros(2)
    psi_sig = Phi(Pmap(Phi(sig), effects))
    assert s.simplify(psi_sig - s.Rational(4, 27) * sig) == s.zeros(2)

slice_c = s.factor((1 - s.Rational(4, 27)) / (1 - s.Rational(2, 3)))
assert slice_c == s.Rational(23, 9)

# The unrelated six-Pauli measure-and-prepare channel has shrink 1/3.
def pauli_eb(x):
    return sum((s.trace((p / 3) * x) * p for p in P), s.zeros(2))
for sig in sigmas:
    assert s.simplify(pauli_eb(sig) - sig / 3) == s.zeros(2)
assert pauli_eb(I2) == I2
assert 1 - s.Rational(1, 3) == 2 * (1 - s.Rational(2, 3))

# Necessary off-correlated Choi diagonals rule out every branch residual.
u = s.symbols('u', real=True)
v = 1 - u
f01 = s.factor(12 * v - (1 + 4 * u) * (1 + 4 * v))
f10 = s.factor(12 * u - (1 + 4 * u) * (1 + 4 * v))
assert f01 == 16 * u**2 - 28 * u + 7  # same inequality after p0=u
assert f10 == 16 * u**2 - 4 * u - 5
root = (1 + s.sqrt(21)) / 8
upper_from_f01 = (7 - s.sqrt(21)) / 8
assert s.simplify(root - s.Rational(1, 2)) > 0
assert s.simplify(upper_from_f01 - root) < 0

# Check the local Choi principal entries for a general positive effect.
q0, q1 = s.symbols('q0 q1', positive=True)
t = q0 + q1
Qgen = s.diag(q0, q1)
alpha = s.Rational(1, 6)
Egen = alpha * (t * I2 + 4 * Qgen)
units = [s.Matrix([[1, 0], [0, 0]]),
         s.Matrix([[0, 1], [0, 0]]),
         s.Matrix([[0, 0], [1, 0]]),
         s.Matrix([[0, 0], [0, 1]])]
def slice_gen(x):
    return alpha * (t * x + x * Qgen + Qgen * x + s.trace(x) * Qgen)
def prep_gen(x):
    return s.trace(Egen * x) * Egen / t
Jslice = sum((s.kronecker_product(e, slice_gen(e)) for e in units), s.zeros(4))
Jprep = sum((s.kronecker_product(e, prep_gen(e)) for e in units), s.zeros(4))
e0, e1 = Egen[0, 0], Egen[1, 1]
assert s.simplify(Jslice[1, 1] - alpha * q1) == 0
assert s.simplify(Jslice[2, 2] - alpha * q0) == 0
assert s.simplify(Jprep[1, 1] - e0 * e1 / t) == 0
assert s.simplify(Jprep[2, 2] - e0 * e1 / t) == 0

print({
    "pauli_covariance": S,
    "all_d_slice_constant": c_slice_d,
    "canonical_slice_shrink": s.Rational(4, 27),
    "best_slice_constant": slice_c,
    "independent_EB_shrink": s.Rational(1, 3),
    "branch_condition_threshold": root,
    "opposite_branch_upper_threshold": upper_from_f01,
    "general_effect_choi_entries": "verified",
    "result": "PASS_EXACT_SYMBOLIC",
})
