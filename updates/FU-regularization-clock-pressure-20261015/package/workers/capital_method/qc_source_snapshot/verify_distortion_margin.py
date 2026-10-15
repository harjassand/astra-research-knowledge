"""Exact algebra for the degenerate G distortion-margin theorem.

Reads only the copied source certificate and this file. No optimizer,
floating-point positivity decision, or source-worktree mutation is used.
The separate REPORT.md supplies the analytic implications.
"""
from pathlib import Path
import hashlib
import json
import time
import sympy as S

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "inputs/G_EXACT_HEAT_CERTIFICATE.json"
SOURCE_HASH = "4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000"
tick = time.monotonic()
cert = json.loads(SOURCE.read_text())
checks = []


def record(name, detail):
    checks.append({"name": name, "status": "PASS", "detail": detail})
    print("PASS:", name, flush=True)


def matrix(rows):
    return S.Matrix([[S.Rational(v) for v in row] for row in rows])


def serial_matrix(M):
    return [[str(v) for v in row] for row in M.tolist()]


assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
assert cert["schema"] == "astra-G-closed-anisotropic-heat/1"
assert cert["matrix_entry_order"] == ["a", "b", "c", "d"]
assert cert["jet_order"] == ["phi1_xx", "phi1_xy", "phi1_yy",
                             "phi2_xx", "phi2_xy", "phi2_yy"]
x = S.symbols("a b c d")
a, b, c, d = x
z = S.symbols("z0:6")
u = a*a+c*c
v = b*b+d*d
j = a*d-b*c
r = a-d
s = b+c
H = (r*r+s*s)**2
G = 3*(u+v-2*j)**2+S.Rational(35, 24)*u*u+j*j-S.Rational(5, 2)*j*u
assert S.expand(H-(u+v-2*j)**2) == 0
d1, d2 = S.Rational(4897, 5000), S.Rational(5103, 5000)
assert matrix(cert["diffusion"]) == S.diag(d1, d2)
C = matrix(cert["basis"])
S0 = matrix(cert["reduced_gram"])
Q0 = matrix(cert["gram"])
assert C.shape == (24, 18) and C.rank() == 18
assert S0 == S0.T and Q0 == C*S0*C.T
L0, D0 = S0.LDLdecomposition(hermitian=False)
assert all(v > 0 for v in D0.diagonal())
assert L0*D0*L0.T == S0
record("Copied source hash, conventions, exact PSD factor", SOURCE_HASH)

pairs = [(i, k) for i in range(4) for k in range(i+1, 4)]
monpairs = [(i, k) for i in range(4) for k in range(i, 4)]
assert cert["omega_pair_order"] == [list(p) for p in pairs]
assert cert["quadratic_coefficient_order"] == [list(p) for p in monpairs]
Omega = S.zeros(4)
for (i, k), row in zip(pairs, cert["omega_coefficients"]):
    val = sum(S.Rational(co)*x[l]*x[m] for co, (l, m) in zip(row, monpairs))
    Omega[i, k], Omega[k, i] = val, -val


def check_closed(O):
    for i in range(4):
        for k in range(i+1, 4):
            for l in range(k+1, 4):
                assert S.expand(S.diff(O[k, l], x[i])-S.diff(O[i, l], x[k])
                                + S.diff(O[i, k], x[l])) == 0


check_closed(Omega)
alpha = -(Omega*S.Matrix(x))/4
for i, k in pairs:
    assert S.expand(S.diff(alpha[k], x[i])-S.diff(alpha[i], x[k])-Omega[i, k]) == 0
B1 = S.Matrix([z[0], z[1], z[3], z[4]])
B2 = S.Matrix([z[1], z[2], z[4], z[5]])
Z = S.Matrix([xx*zz for xx in x for zz in z])


def heat(F):
    Hess = S.hessian(F, x)
    return d1*(B1.T*Hess*B1)[0]+d2*(B2.T*Hess*B2)[0]


source_identity = S.Poly(S.expand((Z.T*Q0*Z)[0]-heat(G)-(B1.T*Omega*B2)[0]), *(x+z))
assert source_identity.is_zero
record("Full source heat identity, closedness, polynomial primitive", "Exact reconstruction")

ell = C.T*Z
v1 = S.zeros(18, 1)
v1[0], v1[12], v1[16] = 1, -1, 1
v2 = S.zeros(18, 1)
v2[13], v2[17] = -1, 1
assert S.expand((v1.T*ell)[0]-r*(z[0]-z[4])) == 0
assert S.expand((v2.T*ell)[0]-r*(z[1]-z[5])) == 0
K = 12*(d1*v1*v1.T+d2*v2*v2.T)
assert S.expand((ell.T*K*ell)[0]-heat(r**4)) == 0
record("Rank-two convex subtraction lies in the Heat18 factor", {
    "v1": "e0-e12+e16", "v2": "-e13+e17", "epsilon": "1/2000"})

epsilon = S.Rational(1, 2000)
Se = S0-epsilon*K
Le, De = Se.LDLdecomposition(hermitian=False)
pivots = list(De.diagonal())
assert all(p > 0 for p in pivots)
assert Le*De*Le.T == Se
V = S.Matrix.hstack(v1, v2)
R = V.T*S0.inv()*V
T0 = 12*(d1*R[0, 0]+d2*R[1, 1])
assert R[0, 1] == R[1, 0] == 0
assert 0 < T0 < 2000
Qe = C*Se*C.T
assert S.Poly(S.expand((Z.T*Qe*Z)[0]-heat(G-epsilon*r**4)
                      -(B1.T*Omega*B2)[0]), *(x+z)).is_zero
record("Updated exact positive Gram and heat identity", {
    "positive_LDL_pivots": len(pivots), "T0_less_than_2000": True})

A = S.Matrix([[a, b], [c, d]])
sqrt2 = S.sqrt(2)
rotations = [S.eye(2), S.Matrix([[1, -1], [1, 1]])/sqrt2,
             S.Matrix([[0, -1], [1, 0]]),
             S.Matrix([[-1, -1], [1, -1]])/sqrt2]
Qbar = S.zeros(24)
Obar = S.zeros(4)
avg = 0
Ts = []
for rot in rotations:
    xr = S.Matrix(list(rot*A))
    sub = dict(zip(x, xr))
    assert S.expand(G.xreplace(sub)-G) == 0
    M = xr.jacobian(x)
    N = S.kronecker_product(rot, S.eye(3))
    T = S.kronecker_product(M, N)
    assert all(val.is_Rational for val in T)
    Ts.append(T)
    Qbar += T.T*Qe*T/4
    Or = Omega.applyfunc(lambda p: p.xreplace(sub))
    Obar += (M.T*Or*M)/4
    avg += (G-epsilon*r**4).xreplace(sub)/4
kappa = S.Rational(3, 16000)
assert S.expand(avg-(G-kappa*H)) == 0
assert all(val.is_Rational for val in Qbar)
Obar = Obar.applyfunc(S.expand)
check_closed(Obar)
assert S.Poly(S.expand((Z.T*Qbar*Z)[0]-heat(G-kappa*H)
                      -(B1.T*Obar*B2)[0]), *(x+z)).is_zero
record("Four rotations and averaged rational distortion certificate", {
    "kappa": str(kappa), "PSD_reason": "average of four exact positive-factor Grams",
    "closedness": "exact", "full_polynomial_identity": "exact"})

xx, yy, hh, kk = S.symbols("xx yy hh kk")
xx2, hh2, dot = xx*xx+yy*yy, hh*hh+kk*kk, xx*hh+yy*kk
remainder = ((xx+hh)**2+(yy+kk)**2)**2-xx2**2-4*xx2*dot-S.Rational(1, 3)*hh2**2
sos = 6*(dot+hh2/3)**2+2*(xx*kk-yy*hh)**2
assert S.expand(remainder-sos) == 0
gamma = S.Rational(1, 2500000)
assert kappa*S.Rational(1, 3)*S.Rational(4, 625) == gamma
assert S.Rational((24+1)**2, 4) == S.Rational(625, 4)
record("Exact quartic Bregman SOS and elliptic-constant arithmetic", {
    "Beurling_squared_bound_external_input": 24, "Korn_fourth_power_bound": "625/4",
    "gamma": str(gamma), "analytic_estimate_verified_here": False})

t, eta = S.symbols("t eta", real=True)
Geta = G-eta*H
Ivals = {a: 1, b: t, c: 0, d: 1}
assert S.expand(Geta.subs(Ivals)+S.Rational(1, 24)-(3-eta)*t**4) == 0
norm4 = (a*a+b*b+c*c+d*d)**2
ep = S.symbols("ep", positive=True)
assert S.diff((G-ep*norm4).subs(Ivals), t, 2).subs(t, 0) == -8*ep
Nscale = S.symbols("Nscale", positive=True)
J0energy = Geta.subs({a: 1, b: 0, c: 0, d: -1})
assert S.expand(J0energy-(S.Rational(1271, 24)-16*eta)) == 0
law = (Nscale**4*(-S.Rational(1, 24))+Nscale**2*J0energy)/(1+Nscale**2)
assert S.factor(law-Nscale**2*(1271-384*eta-Nscale**2)/(24*(1+Nscale**2))) == 0
assert S.Rational(4, 1875)*(kappa/2) == S.Rational(1, 5000000)
record("Degenerate family, rank-one obstruction, lifted-law constants", {
    "eta_upper_QC": str(kappa), "uniform_interval_upper": str(kappa/2),
    "uniform_gamma": "1/5000000"})

rho, slope, q = S.symbols("rho slope q", real=True)
radial = S.expand(G.subs({a: slope, b: 0, c: 0, d: rho}))
assert S.expand(radial-(3*(slope-rho)**4+S.Rational(35, 24)*slope**4
                       +slope*slope*rho*rho-S.Rational(5, 2)*slope**3*rho)) == 0
a0 = S.Rational(1, 4)
entry = S.integrate(radial.subs({slope: a0, rho: a0*q}), (q, 0, 1))
exp_part = S.integrate((-rho**4/S.Integer(24))/rho, (rho, a0, 1))
delta0 = S.Rational(727, 122880)
assert entry == S.Rational(137, 120)*a0**4
assert exp_part == -(1-a0**4)/96
assert entry+exp_part == -delta0
gradient_energy = S.integrate(a0**4*(1+q*q)**2, (q, 0, 1)) + (1-a0**4)
assert gradient_energy == S.Rational(3853, 3840)
entry_eta = entry+exp_part-eta*S.integrate((a0-a0*q)**4, (q, 0, 1))
assert S.expand(entry_eta+delta0+eta/S.Integer(1280)) == 0
assert S.Rational(-3, 4)*4+4-1 == 0
record("Exact compatible negative entry and critical scaling", {
    "action": str(-delta0), "fourth_gradient_energy": str(gradient_energy),
    "entry_family_action": "-727/122880-eta/1280",
    "quartic_action_scaling_exponent": 0})

assert S.Rational(144)+S.Rational(35, 2)+3+15 == S.Rational(359, 2) < 180
assert 180*S.Rational(1, 2) == 90
assert 180*S.Rational(1, 3) == 60
assert 180*S.Rational(1, 12) == 15
record("Growth-envelope constant arithmetic", {
    "Hessian_bound": "(359/2)|A|^2", "C0": 120, "C1": 180,
    "scope": "triangle and operator-norm estimates are explained in REPORT.md"})

derived = {
    "schema": "astra-G-elliptic-distortion-margin/1",
    "source_sha256": SOURCE_HASH,
    "epsilon": str(epsilon), "kappa": str(kappa), "gamma": str(gamma),
    "updated_reduced_gram": serial_matrix(Se),
    "updated_LDL_diagonal": [str(p) for p in pivots],
    "rank_two_inverse_pair_matrix": serial_matrix(R), "trace_bound_T0": str(T0),
    "averaged_gram": serial_matrix(Qbar),
    "averaged_omega_coefficients": [
        [str(S.Poly(Obar[i, k], *x).coeff_monomial(x[l]*x[m])) for l, m in monpairs]
        for i, k in pairs],
    "PSD_factor_description": "1/4 sum_theta T_theta^T C S_epsilon C^T T_theta, theta=0,pi/4,pi/2,3pi/4",
    "external_analytic_input": {
        "source": "Banuelos-Janakiraman Theorem 1.1",
        "url": "https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf",
        "claim_used": "complex L4 Beurling norm at most sqrt(24)"},
    "historical_novelty": "UNKNOWN", "external_review": "UNKNOWN"}
(ROOT/"DISTORTION_MARGIN_CERTIFICATE.json").write_text(json.dumps(derived, indent=2)+"\n")
receipt = {"schema": "astra-qc-genesis-verification/1", "status": "EXACT_PASS",
           "checks": checks, "groups": len(checks), "seconds": time.monotonic()-tick,
           "scope": "exact finite algebra; analytic arguments remain in REPORT.md",
           "source_sha256": SOURCE_HASH, "external_review": "UNKNOWN",
           "historical_novelty": "UNKNOWN"}
(ROOT/"VERIFICATION.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps({k: v for k, v in receipt.items() if k != "checks"}, indent=2), flush=True)
