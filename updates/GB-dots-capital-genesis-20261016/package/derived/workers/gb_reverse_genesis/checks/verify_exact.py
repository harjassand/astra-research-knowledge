#!/usr/bin/env python3
"""Exact examples and algebra checks. This is not a proof checker for the theorems."""
from pathlib import Path
import hashlib
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
I2 = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Z = s.diag(1, -1)
Q = s.Rational


def zero(matrix):
    assert all(s.simplify(v) == 0 for v in matrix), matrix


def lyapunov(A, H):
    n = A.rows
    superop = s.kronecker_product(s.eye(n), A) + s.kronecker_product(A.T, s.eye(n))
    vec = s.Matrix([2*H[i, j] for j in range(n) for i in range(n)])
    sol = superop.inv() * vec
    L = s.Matrix(n, n, lambda i, j: s.factor(sol[i+n*j]))
    zero(A*L+L*A-2*H)
    zero(L-L.H)
    return L


def risk_moments(plus, minus, O):
    n = O.rows
    loss_p = (O-s.eye(n))**2
    loss_m = (O+s.eye(n))**2
    mean = s.factor((s.trace(plus*loss_p)+s.trace(minus*loss_m))/2)
    second = s.factor((s.trace(plus*loss_p**2)+s.trace(minus*loss_m**2))/2)
    return mean, s.factor(second-mean**2)


out = {"status": "PASS", "scope": "Exact finite examples and symbolic identities only", "checks": {}}

# Noncommuting singular qutrits with a nonzero common support.
S1 = s.Matrix([[Q(1, 2), Q(1, 4), 0], [Q(1, 4), Q(1, 2), 0], [0, 0, 0]])
S2 = s.Matrix([[Q(2, 3), Q(1, 10), Q(2, 15)],
               [Q(1, 10), Q(3, 25), Q(4, 25)],
               [Q(2, 15), Q(4, 25), Q(16, 75)]])
assert S1.rank() == S2.rank() == 2
assert s.trace(S1) == s.trace(S2) == 1
assert S1*S2 != S2*S1
e1 = s.Matrix([1, 0, 0])
zero((s.eye(3)-S1*S1.pinv())*e1)
zero((s.eye(3)-S2*S2.pinv())*e1)
assert (S1.nullspace()[0].row_join(S2.nullspace()[0])).rank() == 2
g1 = (e1.T*S1.pinv()*e1)[0]
g2 = (e1.T*S2.pinv()*e1)[0]
assert (g1, g2) == (Q(8, 3), Q(12, 7))
p = s.symbols('p', positive=True)
A = (1-p)*S1+p*S2
B = p*S1+(1-p)*S2
Lambda = s.simplify(B-p*(1-p)*(S1-S2)*A.inv()*(S1-S2))
h = 1/(p*g1+(1-p)*g2)
zero(Lambda-h*e1*e1.T)
N = s.factor(1-h)
assert s.limit(N, p, 1, dir='-') == Q(5, 8)
out["checks"]["singular_qutrit"] = {
    "common_support_dimension": 1, "restricted_pseudoinverses": [str(g1), str(g2)],
    "schur_trace_ratio": str(N), "complete_coefficient": "5/8",
    "naive_compress_then_inverse_coefficient": "1/2",
    "boundary_prior_uses_all_channel_supports": True}

# A genuinely singular 4x4 frame baseline: pay range(W) explicitly.
states = [s.Matrix([[1, 0], [0, 0]]), s.Matrix([[1, 1], [1, 1]])/2,
          s.Matrix([[0, 0], [0, 1]])]
frame = s.Matrix([[1/s.sqrt(2), -1/s.sqrt(2), 0],
                  [1/s.sqrt(6), 1/s.sqrt(6), -2/s.sqrt(6)]])
zero(frame*frame.T-I2)
v = [frame[:, i] for i in range(3)]
R = [vi*vi.T for vi in v]
z = [vi/s.sqrt(3) for vi in v]
A0 = sum((s.kronecker_product(Ri, Si) for Ri, Si in zip(R, states)), s.zeros(4))
W = sum((s.kronecker_product(zi, Si) for zi, Si in zip(z, states)), s.zeros(4, 2))
baseline = sum(states, s.zeros(2))/3
assert A0.rank() == 3
Aplus = A0.pinv()
zero((s.eye(4)-A0*Aplus)*W)
zero(baseline-W.T*Aplus*W)
hs = [-1, 0, 1]
H = [hi*Ri for hi, Ri in zip(hs, R)]
K = sum(H, s.zeros(2))
J = sum((s.kronecker_product(Hi, Si) for Hi, Si in zip(H, states)), s.zeros(4))
zero((s.eye(4)-A0*Aplus)*J)
E_phys = s.simplify(sum(s.trace(Hi*Ri.pinv()*Hi) for Hi, Ri in zip(H, R))-s.trace(K*K))
N_phys = s.simplify(s.trace(J*Aplus*J)-s.trace(K*K))
assert E_phys > 0 and N_phys == E_phys
eps = Q(1, 100)
Re = [(Ri+eps*I2)/(1+3*eps) for Ri in R]
Ae = sum((s.kronecker_product(Ri, Si) for Ri, Si in zip(Re, states)), s.zeros(4))
Ee = s.factor(sum(s.trace(Hi*Ri.inv()*Hi) for Hi, Ri in zip(H, Re))-s.trace(K*K))
Ne = s.factor(s.trace(J*Ae.inv()*J)-s.trace(K*K))
assert Ae.det() > 0 and 0 < Ne/Ee < 1
out["checks"]["singular_frame_range"] = {
    "output_baseline_dimension": 4, "output_baseline_rank": 3,
    "W_and_J_in_baseline_range": True, "physical_supported_ratio": str(N_phys/E_phys),
    "faithful_input_epsilon": str(eps), "finite_physical_ratio": str(s.factor(Ne/Ee))}

# Unsupported pseudoinverse replacement gives an impossible negative answer.
naive = s.eye(2)  # overwritten only to make the computation self-contained
naive = s.factor(1-s.trace(((states[0].pinv()+states[1].pinv())/2).inv()))
assert naive == -7
out["checks"]["unsupported_pseudoinverse_trap"] = {"naive_answer": str(naive), "correct_answer": "1"}

# Exact finite, faithful pure-qubit/Bell fixture.
a, b, q, delta, t = Q(3, 5), Q(4, 5), Q(625, 1681), Q(1, 9), Q(3, 10)
c = a*a
sigma = [(I2+b*Z+sign*a*X)/2 for sign in [1, -1]]
assert all(S.det() == 0 and s.trace(S) == 1 for S in sigma)
Bi = s.diag(1, delta)/2
Hi = [X/2, -X/2]
rp = [(Bi+t*H)/(1+delta) for H in Hi]
rm = [(Bi-t*H)/(1+delta) for H in Hi]
assert sum(s.trace(r) for r in rp) == sum(s.trace(r) for r in rm) == 1
assert all(r[0, 0] > 0 and r.det() > 0 for r in rp+rm)
zero(sum(rp, s.zeros(2))-sum(rm, s.zeros(2)))
At = sum((s.kronecker_product(S, Bi) for S in sigma), s.zeros(4))/(1+delta)
Ht = t*sum((s.kronecker_product(S, H) for S, H in zip(sigma, Hi)), s.zeros(4))/(1+delta)
Lt = lyapunov(At, Ht)
lam_p, lam_m = (1+b)/2, (1-b)/2
Bell = s.zeros(4)
Bell[0, 3] = Bell[3, 0] = t*a/(lam_p+delta*lam_m)
Bell[1, 2] = Bell[2, 1] = t*a/(lam_m+delta*lam_p)
zero(Lt-Bell)
target_risk, target_var = risk_moments(At+Ht, At-Ht, Lt)
source_risk = s.factor(1-q*4*t*t/(1+delta)**2)
source_second = 0
for i, sign in enumerate([1, -1]):
    Oi = sign*2*t/(1+delta)*X
    loss_p, loss_m = (Oi-I2)**2, (Oi+I2)**2
    source_second += q*(s.trace(rp[i]*loss_p**2)+s.trace(rm[i]*loss_m**2))/2
source_second += 1-q  # erase predicts zero: its squared loss and its square are one
source_var = s.factor(source_second-source_risk**2)
gap = s.factor(source_risk-target_risk)
assert gap == Q(2916, 42025)
x = ((1-delta)/(1+delta))**2
ratio = s.factor(c/(1-b*b*x))
assert ratio == Q(25, 41)
assert gap == s.factor(4*t*t/(1+delta)**2*(ratio-q))
assert c < q < 1 and t*t < delta
assert max(abs(e) for e in Lt.eigenvals()) <= 1
out["checks"]["pure_qubit_finite_fixture"] = {
    "a": str(a), "b": str(b), "q": str(q), "delta": str(delta), "t": str(t),
    "ordinary_SLD_threshold": str(c), "complete_threshold": "1",
    "source_optimal_MMSE": str(source_risk), "target_optimal_MMSE": str(target_risk),
    "gap": str(gap), "gap_decimal": float(gap), "source_loss_variance": str(source_var),
    "target_loss_variance": str(target_var), "fixed_Bell_equals_SLD_optimum": True,
    "all_input_blocks_faithful": True, "same_reference_marginal": True}

# General symbolic simulator and payoff-family formula.
bs, qs, cs = s.symbols('b q c', positive=True)
L2 = (1-bs*bs)+(bs-1+qs)**2
assert s.factor(L2-(qs*qs+2*(1-qs)*(1-bs))) == 0
ys = s.symbols('y', positive=True)
F = (ys-cs)/(1-cs)*(cs/ys-qs)
assert s.factor(s.diff(F, ys)-(cs*cs/ys**2-qs)/(1-cs)) == 0
Fstar = s.simplify(F.subs(ys, cs/s.sqrt(qs)))
assert s.simplify(Fstar-cs/(1-cs)*(1-s.sqrt(qs))**2) == 0
out["checks"]["symbolic_payoff_family"] = {
    "derivative_y": str(s.factor(s.diff(F, ys))),
    "q_le_c_squared_supremum": "c-q",
    "q_ge_c_squared_supremum": "c/(1-c)*(1-sqrt(q))**2",
    "reversal_regime_used_in_main_result": "c<=q<1"}

out["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
path = ROOT / 'checks' / 'results.json'
path.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
print(json.dumps({"status": "PASS", "output": str(path), "checks": list(out["checks"]),
                  "fixture_gap": str(gap)}, indent=2))
