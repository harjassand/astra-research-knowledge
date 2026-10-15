#!/usr/bin/env python3
"""Exact finite checks; these are not an experiment or a formal analytic proof."""
from pathlib import Path
import itertools
import json
import random
import sympy as s

HERE = Path(__file__).resolve().parent
checks = {}


def zero(M):
    return all(s.cancel(x) == 0 for x in M)


def behavior(M0, U, W, H, q):
    Q = s.diag(*q)
    return M0 - U * (s.eye(len(q)) + Q * H).inv() * Q * W


# 1. Recover a one-coordinate rational response from two finite settings.
t, z, h, g = s.symbols("t z h g", nonzero=True)
dt, dz = -t*g/(1+t*h), -z*g/(1+z*h)
hr = (t*dz-z*dt)/(t*z*(dt-dz))
gr = -(1+t*hr)*dt/t
assert s.cancel(hr-h) == 0 and s.cancel(gr-g) == 0
checks["single_load_symbolic_recovery"] = "PASS"

# Exact nonidentifiability from only the baseline and one finite toggle.
Ta = s.Matrix([[2, 1], [1, 1]])
Tb = s.Matrix([[2, 2], [2, 7]])
assert Ta.det() > 0 and Tb.det() > 0
assert Ta[0, 0] > 0 and Tb[0, 0] > 0
qone = s.symbols("qone")
vone, bone = s.Matrix([0, 1]), s.Matrix([1, 0])
ma = (bone.T*(Ta.inv()+qone*vone*vone.T).inv()*bone)[0]
mb = (bone.T*(Tb.inv()+qone*vone*vone.T).inv()*bone)[0]
assert ma.subs(qone, 0) == mb.subs(qone, 0) == 2
assert ma.subs(qone, 1) == mb.subs(qone, 1) == s.Rational(3, 2)
assert s.diff(ma, qone).subs(qone, 0) == -1
assert s.diff(mb, qone).subs(qone, 0) == -4
checks["one_finite_toggle_does_not_determine_derivative"] = "PASS; two reciprocal positive-definite plants"


# 2. Unknown six-state plant; its entire symmetric part is 4I.
n, m = 6, 3
for seed in range(1, 101):
    rng = random.Random(seed)
    R = s.Matrix(n, n, lambda i, j: rng.randrange(-4, 5))
    A = 4*s.eye(n) + (R-R.T)/7
    B = s.eye(n)[:, :2]
    C = B
    V = s.eye(n)[:, 3:6]
    T = A.inv()
    M0, U, W, H = C.T*T*B, C.T*T*V, V.T*T*B, V.T*T*V
    if all(U[:, [i, j]].det() != 0 and W[[i, j], :].det() != 0
           for i, j in itertools.combinations(range(m), 2)):
        break
else:
    raise AssertionError("No pair-observable exact test instance found")
assert A+A.T == 8*s.eye(n)


def measured(q):
    return C.T * (A + V*s.diag(*q)*V.T).inv() * B


Utilde = s.zeros(2, m)
Wtilde = s.zeros(m, 2)
Htilde = s.zeros(m)
settings = [s.zeros(m, 1)]
for i in range(m):
    qi, ri = [s.Integer(0)]*m, [s.Integer(0)]*m
    qi[i], ri[i] = s.Rational(1, 2), s.Rational(3, 2)
    Dq, Dr = measured(qi)-M0, measured(ri)-M0
    pivot = next((r, c) for r in range(2) for c in range(2) if Dq[r, c] != 0)
    r, c = pivot
    dt, dz = Dq[r, c], Dr[r, c]
    ti, zi = qi[i], ri[i]
    hii = s.cancel((ti*dz-zi*dt)/(ti*zi*(dt-dz)))
    Ci = -(1+ti*hii)*Dq/ti
    assert hii == H[i, i] and zero(Ci-U[:, i]*W[i, :])
    p, k = next((p, k) for p in range(2) for k in range(2) if Ci[p, k] != 0)
    ui, wi = Ci[:, k], Ci[p, :]/Ci[p, k]
    assert zero(ui*wi-Ci)
    Utilde[:, i], Wtilde[i, :], Htilde[i, i] = ui, wi, hii
    settings.extend([qi, ri])

for i, j in itertools.combinations(range(m), 2):
    q = [s.Integer(0)]*m
    q[i] = q[j] = s.Rational(1, 2)
    ui, wi = Utilde[:, [i, j]], Wtilde[[i, j], :]
    Z = -ui.inv()*(measured(q)-M0)*wi.inv()
    recovered = Z.inv()-s.diag(1/q[i], 1/q[j])
    assert recovered[0, 0] == H[i, i] and recovered[1, 1] == H[j, j]
    Htilde[i, j], Htilde[j, i] = recovered[0, 1], recovered[1, 0]
    settings.append(q)

D = s.diag(*(s.cancel(Utilde[0, i]/U[0, i]) for i in range(m)))
assert zero(Utilde-U*D)
assert zero(Wtilde-D.inv()*W)
assert zero(Htilde-D.inv()*H*D)
assert len(settings) == 1+2*m+m*(m-1)//2
checks["measured_only_exact_reconstruction"] = {
    "status": "PASS", "n": n, "m": m, "seed": seed,
    "load_settings": len(settings), "source_profiles": 2*len(settings),
    "symmetric_part": "4I", "background_reciprocity": False,
}


# 3. Held-out finite load values and exact control derivatives.
heldout = list(itertools.product([s.Rational(0), s.Rational(2, 3), s.Rational(5, 4)], repeat=m))
for q in heldout:
    actual = measured(q)
    predicted = behavior(M0, Utilde, Wtilde, Htilde, q)
    assert zero(actual-predicted)
    assert zero(actual-behavior(M0, U, W, H, q))
    Tq = (A+V*s.diag(*q)*V.T).inv()
    Lq = (s.eye(m)+s.diag(*q)*Htilde).inv()
    Rq = (s.eye(m)+Htilde*s.diag(*q)).inv()
    for j in range(m):
        predicted_d = -Utilde*Lq[:, j]*Rq[j, :]*Wtilde
        actual_d = -C.T*Tq*V[:, j]*V[:, j].T*Tq*B
        assert zero(predicted_d-actual_d)
checks["heldout_finite_decisions_and_derivatives"] = {
    "status": "PASS", "finite_settings": len(heldout),
    "derivative_matrices": len(heldout)*m,
}


# 4. Gauge cancellation stops for general coupled loads.
Qcoupled = s.Matrix([[0, 1], [1, 0]])
D2 = s.diag(2, 1)
Mtrue = -Qcoupled
Mwrong = -D2*Qcoupled*D2.inv()
assert not zero(Mtrue-Mwrong)
checks["coupled_load_gauge_obstruction"] = {
    "status": "PASS", "difference": str(Mwrong-Mtrue),
}


# 5. Individually invisible controls can have a nonzero joint response,
# even for a strictly accretive real plant.
eps = s.Rational(1, 4)
T4 = s.eye(4)
T4[0, 2] = T4[3, 1] = T4[2, 3] = eps
A4 = T4.inv()
V4 = s.eye(4)[:, [2, 3]]
B4, C4 = s.eye(4)[:, 1], s.eye(4)[:, 0]
symT = (T4+T4.T)/2
assert all(symT[:i, :i].det() > 0 for i in range(1, 5))
assert zero((A4+A4.T)/2 - A4.T*symT*A4)
def invisible(q):
    return (C4.T*(A4+V4*s.diag(*q)*V4.T).inv()*B4)[0]
assert invisible([0, 0]) == invisible([1, 0]) == invisible([0, 1]) == 0
joint = invisible([1, 1])
assert joint == s.Rational(1, 256)
checks["invisible_single_load_not_global_irrelevance"] = {
    "status": "PASS", "joint_response": str(joint),
    "strict_accretivity": "exact Sylvester criterion for inverse; congruence for A",
}


# 6. A reciprocal and a nonreciprocal strictly accretive plant have
# identical responses for the entire diagonal-load family.
Arec = 4*s.eye(4) + s.Matrix([[0, 1, 2, 3], [1, 0, 4, 5],
                             [2, 4, 0, 6], [3, 5, 6, 0]])/10
Dhat = s.diag(1, 1, 2, 3)
Anon = Dhat.inv()*Arec*Dhat
sym_non = (Anon+Anon.T)/2
offrows = [sum(abs(sym_non[i, j]) for j in range(4) if j != i)
           for i in range(4)]
assert max(offrows) == s.Rational(119, 60) < 4
assert Arec == Arec.T and Anon != Anon.T
Brec = Crec = s.eye(4)[:, :2]
Vrec = s.eye(4)[:, 2:4]
q1, q2 = s.symbols("q1 q2")
load = Vrec*s.diag(q1, q2)*Vrec.T
assert zero(Anon+load-Dhat.inv()*(Arec+load)*Dhat)
assert zero(Dhat*Brec-Brec) and zero(Crec.T*Dhat.inv()-Crec.T)
for q in ([0, 0], [1, 0], [0, 2], [1, 3]):
    add = Vrec*s.diag(*q)*Vrec.T
    assert zero(Crec.T*(Anon+add).inv()*Brec-Crec.T*(Arec+add).inv()*Brec)
checks["all_diagonal_loads_do_not_certify_hidden_reciprocity"] = {
    "status": "PASS", "identity": "Exact symbolic similarity for arbitrary q1,q2",
    "largest_symmetric_part_offdiagonal_row_sum": str(max(offrows)),
    "diagonal": 4,
}


# 7. Check the actual time-adjoint paper's displayed RLC intertwiner.
c1, c2, g1, g2, l1, l2, k = s.symbols("c1 c2 g1 g2 l1 l2 k", nonzero=True)
C2, G2 = s.diag(c1, c2), s.diag(g1, g2)
L2 = s.Matrix([[l1, k], [k, l2]])
Z2, I2 = s.zeros(2), s.eye(2)
Hop = (C2.inv()*G2).row_join(C2.inv()).col_join((-L2).row_join(Z2))
Theta = Z2.row_join(I2).col_join(I2.row_join(-G2))
assert zero(Hop*Theta-Theta*Hop.T)
assert Theta.det() != 0
checks["rlc_displayed_intertwiner_identity"] = "PASS; source actuation/readout still a physical obligation"

checks["m30_cost"] = {"load_settings": 496, "two_source_profiles_per_setting": 992,
                        "two_by_two_scalar_readings": 1984,
                        "profile_only_crossover_against_six_per_point": 166}
out = {
    "status": "PASS", "checks": checks,
    "scope": "Exact symbolic identities and finite rational examples only. No experimental acquisition, noise guarantee, historical novelty, global optimization, or formal proof certification.",
}
(HERE/"verification.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out, indent=2))
