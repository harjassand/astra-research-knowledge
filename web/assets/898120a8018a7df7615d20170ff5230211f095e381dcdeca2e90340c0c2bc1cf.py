"""Exact scoped checks for the split three-qubit parent Hamiltonian.

These checks certify finite matrix identities, not paper soundness or priority.
"""
import json
from pathlib import Path
import sympy as S
import mpmath as mp

d = S.symbols("delta", positive=True)
x = d**2
a, b = (1+d)/2, (1-d)/2
n, s = (1+x)/2, (1+3*x)/2
I2, I8 = S.eye(2), S.eye(8)
phi = S.Matrix([1, 0, 0, 1])/S.sqrt(2)
Q12 = phi*phi.T + d*(S.eye(4)-phi*phi.T)
Q = S.kronecker_product(Q12, I2)
bad = S.Matrix([b, 0, 0, -a])
ten = S.Matrix([0, 0, 1, 0])
h_init = S.kronecker_product(bad*bad.T/n + ten*ten.T, I2)
v0 = S.Matrix([a,0,0,d,0,0,b,0])
v1 = S.Matrix([0,b,0,0,d,0,0,a])
h_gate = I8-(v0*v0.T+v1*v1.T)/s
h_out = S.diag(1,0,1,0,1,0,1,0)
w = S.Matrix([0,1,0,0,0,0,0,1])/S.sqrt(2)

def zero(A):
    return all(S.simplify(z)==0 for z in A)

assert zero(Q12*phi-phi)
assert zero(h_init*h_init-h_init)
assert zero(h_gate*h_gate-h_gate)
assert zero(h_out*h_out-h_out)
init_basis = [S.eye(8)[:,j] for j in range(4)]
gate_basis = [S.kronecker_product(S.eye(2)[:,j],phi) for j in range(2)]
assert all(zero(h_init*Q*v) for v in init_basis)
assert all(zero(h_gate*Q*v) for v in gate_basis)
assert zero(h_init*v0)
assert zero(h_gate*v0)
assert zero(h_gate*v1)

def expectation(h, v):
    return S.factor((v.T*h*v)[0]/(v.T*v)[0])

actual = {
    "w_init": expectation(h_init,w),
    "w_gate": expectation(h_gate,w),
    "w_out": expectation(h_out,w),
    "w_H": expectation((h_init+h_gate+h_out)/3,w),
    "v1_init": expectation(h_init,v1),
    "v1_gate": expectation(h_gate,v1),
    "v1_out": expectation(h_out,v1),
    "v1_H": expectation((h_init+h_gate+h_out)/3,v1),
    "v0_out": expectation(h_out,v0),
}
expected = {
    "w_init": x/(1+x),
    "w_gate": 3*x/(1+3*x),
    "w_out": 0,
    "w_H": 2*x*(2+3*x)/(3*(1+x)*(1+3*x)),
    "v1_init": 2*x*(3+x)/((1+x)*(1+3*x)),
    "v1_gate": 0,
    "v1_out": 2*x/(1+3*x),
    "v1_H": 4*x*(2+x)/(3*(1+x)*(1+3*x)),
    "v0_out": (1+x)/(1+3*x),
}
assert all(S.simplify(actual[k]-v)==0 for k,v in expected.items())

# Grouped one-vertex support projector corresponding to Eq. (116).
h_group = I8-v0*v0.T/s
assert zero(h_group*h_group-h_group)
assert zero(h_group*v0)
lam = S.symbols("lambda")
group_char = S.factor((h_group+h_out).charpoly(lam).as_expr())
group_expected = (lam-1)**3*(lam-2)**3*((lam-1)**2-2*x/(1+3*x))
assert S.simplify(group_char-group_expected)==0

# A literal naive two-vertex placement must not be called faithful:
# Eq. (116) with Q_vertex=I gives |1><1| on input 1.
naive_vertex = S.kronecker_product(S.diag(0,1),S.eye(4))
naive_vertex_energy = expectation(naive_vertex,v0)
assert S.simplify(naive_vertex_energy-(1-d)**2/(2*(1+3*x)))==0

# Numerical spectrum diagnostics at exact rational parameters.
spectra = []
H = (h_init+h_gate+h_out)/3
for val in [S.Rational(1,2), S.Rational(1,8), S.Rational(1,32)]:
    evaluated = H.subs(d,val).evalf(50)
    with mp.workdps(40):
        numeric = mp.matrix([[mp.mpf(str(evaluated[i,j])) for j in range(8)]
                             for i in range(8)])
        eigs = [float(z) for z in mp.eigsy(numeric,eigvals_only=True)]
    spectra.append({"delta":str(val), "lambda_min":min(eigs),
                    "w_upper":float(expected["w_H"].subs(d,val))})

out = {"status":"PASS", "identities":{k:str(v) for k,v in actual.items()},
       "group_characteristic":str(group_char),
       "naive_vertex_energy":str(naive_vertex_energy), "spectral_diagnostics":spectra}
Path(__file__).with_name("check_exact.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
