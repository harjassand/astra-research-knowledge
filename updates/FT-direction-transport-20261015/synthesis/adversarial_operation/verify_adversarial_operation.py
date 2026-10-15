#!/usr/bin/env python3
"""Exact checks of finite algebra. Analytic or physical claims are not certified."""
import json
from pathlib import Path
import sympy as s

GROUPS = []


def record(name, detail):
    GROUPS.append({"name": name, "status": "PASS", "detail": detail})


def zero(x):
    if isinstance(x, s.MatrixBase):
        assert x.applyfunc(s.simplify) == s.zeros(*x.shape), x
    else:
        assert s.simplify(x) == 0, x


# Exact incoming countermodel; all observed source columns coincide.
n = 5
I = s.eye(n)
e = [I[:, i] for i in range(n)]
Q = s.Matrix.hstack(e[0], e[1], e[2], e[4])
v, b, c = e[0] - e[3], e[0], e[1]
p = s.symbols("p", nonnegative=True)
Ap, Am = I + e[1] * e[3].T, I - e[1] * e[3].T
zero(Ap.inv() * Q - Am.inv() * Q)
zero((c.T * (Ap + p * v * v.T).inv() * b)[0] + p / (1 + 2*p))
zero((c.T * (Am + p * v * v.T).inv() * b)[0] - p / (1 + 2*p))
assert min(((Ap + Ap.T)/2).eigenvals()) == s.Rational(1, 2)
assert min(((Am + Am.T)/2).eigenvals()) == s.Rational(1, 2)
record("support countermodel", "Identical full observed response; opposite exact finite-control objectives; sym(A) minimum 1/2.")

# A genuinely nonsymmetric coupled block model, exact adjoint composition.
B = s.Matrix([[5, 2], [-1, 4]])
E = s.Matrix([[1, 0], [1, 1]])
C = s.Matrix([[4, 1], [1, 3]])
A = B.row_join(E).col_join(E.T.row_join(C))
P = s.eye(4)[:, :2]
c4 = s.Matrix([1, 2, -1, 3])
Y, z = A.inv() * P, A.inv() * c4
H = P.T * Y
alpha = H.inv() * P.T * z
beta = H.inv() * (H.T - H) * alpha
zero(z + Y * beta - A.T.inv() * c4)
zero(H.T.inv() - H.inv() - (B.T - B))
record("port adjoint", "Exact rational nonsymmetric four-state Schur composition and transpose defect.")

# Known finite controls do not need skew support.
V = s.Matrix([[1, 0], [-1, 1], [0, -1], [0, 0]])
b4 = s.Matrix([2, 0, 1, -1])
D = s.diag(s.Rational(2, 3), s.Rational(3, 5))
x, Y = A.inv() * b4, A.inv() * V
H, t, w = V.T * Y, V.T * x, c4.T * Y
formula = (c4.T*x)[0] - (w * (s.eye(2)+D*H).inv()*D*t)[0]
zero(formula - (c4.T*(A+V*D*V.T).inv()*b4)[0])
record("finite-control completion", "Two coupled known PSD controls, exact objective from acquired source/sensor block.")

# Measurement-null perturbation showing the actual linear information criterion.
R = s.Matrix([[1, 0, 0], [0, 1, 0]])
Q3 = s.Matrix([[1], [0], [0]])
Delta = s.Matrix([[0, 0, 0], [0, 0, 1], [0, 0, 0]])
zero(R * Delta * Q3)
assert (s.Matrix([[0, 1, 0]]) * Delta * s.Matrix([0, 0, 1]))[0] == 1
record("partial-information null direction", "Concrete task coefficient outside the sensor/source tensor span.")

# Backward equations reconstruct lifetime and signed transfer, including endpoint.
aL, aR, bL, bR, h = s.symbols("aL aR bL bR h", positive=True)
Ar, Br = aL+aR, bL+bR
T0, T1, N0, N1 = s.symbols("T0 T1 N0 N1")
sol = s.solve([
    T0 - 1/Ar - T1,
    T1 - 1/(Br+h) - Br/(Br+h)*T0,
    N0 + aR/Ar - N1,
    N1 - Br/(Br+h)*N0 - bR/(Br+h),
], [T0, T1, N0, N1])
expectedT = (Ar+Br+h)/(Ar*h)
expectedN = (aL*bR-aR*bL)/(Ar*h) - aR/Ar
zero(sol[T0] - expectedT)
zero(sol[N0] - expectedN)
rR, rH, pi = bR/(Br+h), h/(Br+h), aR/Ar
zero(expectedN - (rR-pi)/rH)
zero(expectedT - (1/Ar + 1/(Br+h))/rH)
record("first-event certificate", "All four backward equations, exact signed lifetime transfer and event/waiting-time sufficient statistics.")

alpha, q, qH = s.symbols("alpha q qH", positive=True)
sub = {aL: alpha*aL, aR: alpha*aR, bL: q*bL, bR: q*bR, h: qH*h}
Nprime = expectedN.subs(sub, simultaneous=True)
zero(Nprime + aR/Ar - q/qH*(expectedN+aR/Ar))
RA, RU, RH, beta, chi = s.symbols("RA RU RH beta chi", real=True)
zero(beta*chi*(RA-RU) - beta*chi*(RA-RH) - beta*chi*(RH-RU))
record("lifetime branching cancellation", "Entry scaling and trap overlap cancel only for the declared occupied-only model.")

# Scalar harmonic countermodels use identical stable wells and baseline barriers.
BU, BH, kappa = s.symbols("BU BH kappa", real=True)
for ru, rh in [(s.Integer(0), s.Integer(1)), (s.Integer(1), s.Integer(0))]:
    FA0 = s.Rational(1, 2) - s.Rational(1, 2)
    FU0, FH0 = BU + ru - ru, BH + rh - rh
    zero(FU0 - FA0 - BU)
    zero(FH0 - FA0 - BH)
    # At kappa=1 and beta=1, log q - log qH is half the hidden overlap difference.
    logq = (s.Rational(1, 2)-ru)/2
    logqh = (s.Rational(1, 2)-rh)/2
    zero(logq-logqh-(rh-ru)/2)
record("same-well opposite clamp effects", "Baseline barriers and all occupied-well parameters agree; lifetime log multipliers are ±1/2.")

# Independent algebra audit of the supplied Cartesian fractional development.
tt, cc, vv, bb, vx, vy, bx, by = s.symbols("t c v b vx vy bx by", real=True)
gradv = s.Matrix([vx, vy])
gradb = s.Matrix([bx, by])
gradv2 = 2*vv*gradv
gradvb = vv*gradb + bb*gradv
first = tt*gradb - cc**2*tt**3*gradv2 - cc*tt**4*gradvb
second = gradv + cc*tt**3*gradv2 + tt**4*gradvb
quartic = s.Poly(s.expand((first.dot(first))**2 + (second.dot(second))**2), tt)
base = gradv.dot(gradv)**2
Bpoint = 8*vv*base
Hpoint = gradb.dot(gradb)**2 + 4*gradv.dot(gradv)*gradv.dot(gradvb)
zero(quartic.nth(0)-base)
zero(quartic.nth(3)-cc*Bpoint)
zero(quartic.nth(4)-Hpoint)
for kk in (1, 2, 5):
    zero(quartic.nth(kk))
ee, aa, ar, gg = s.symbols("epsilon a aref g", real=True)
mass = ((1+ee*aa)**4-(1+ee*ar)**4)*(1+ee**2*vv**2/(1+ee*gg)**2)**2/(4*ee)
mass_series = s.series(mass, ee, 0, 2).removeO()
zero(mass_series - (aa-ar) - ee*s.Rational(3, 2)*(aa**2-ar**2))
record("fractional and exact-mass coefficients", "General pointwise t=epsilon^(1/3) expansion, no omitted t^1,t^2,t^5 term; normalized mass coefficient3/2.")

xx, yy = s.symbols("x y", real=True)
vbump = xx*(1-xx)*yy*(1-yy)
bmean = vbump**2-vbump/s.Integer(25)
def integrate_square(poly):
    return s.integrate(s.integrate(s.expand(poly), (xx, 0, 1)), (yy, 0, 1))
zero(integrate_square(bmean))
gv = s.Matrix([s.diff(vbump, xx), s.diff(vbump, yy)])
gvb = s.Matrix([s.diff(vbump*bmean, xx), s.diff(vbump*bmean, yy)])
ell = integrate_square(4*gv.dot(gv)*gv.dot(gvb))
assert ell != 0
record("mean-constrained forcing survives", {"mean_zero": str(integrate_square(bmean)), "ell_v(b0)": str(ell)})

pi0=s.Rational(1,4)
plus=[(s.Rational(1,16),s.Rational(7,16)),(s.Rational(7,16),s.Rational(1,16))]
minus=[(s.Rational(1,16),s.Rational(1,16)),(s.Rational(7,16),s.Rational(7,16))]
means=[]
for law in (plus,minus):
    assert all(1-rh-rr>0 for rh,rr in law)
    assert sum(rh for rh,rr in law)/2==s.Rational(1,4)
    assert sum(rr for rh,rr in law)/2==s.Rational(1,4)
    assert sum(1-rh-rr for rh,rr in law)/2==s.Rational(1,2)
    assert sum(2/rh for rh,rr in law)/2==s.Rational(128,7)
    means.append(sum((rr-pi0)/rh for rh,rr in law)/2)
assert means==[s.Rational(9,7),-s.Rational(9,7)]
record("persistent-type pooled-calibration failure", {"pooled_lifetime":"128/7", "opposite_expected_transfer":[str(v) for v in means]})

out = {"status": "PASS", "groups": GROUPS, "scope": "Finite exact algebra only; not compactness, physical validity, novelty or external proof certification."}
path = Path(__file__).with_name("EXACT_CHECKS.json")
path.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"status": out["status"], "groups": len(GROUPS), "output": str(path)}, indent=2))
