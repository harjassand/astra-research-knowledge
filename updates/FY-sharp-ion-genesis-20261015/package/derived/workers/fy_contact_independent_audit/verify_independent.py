#!/usr/bin/env python3
"""Exact identities behind the independent oblique-contact reconstruction.

This script writes only alongside itself. Identities supplement the
universal proof; finite symbolic checks do not certify the analytic theorem.
"""
import hashlib
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
PIN = "b32943eeb62d0d79929a9e572a344219a785ebf9"
W = Path("/Users/harjas/Documents/ChatGPT/ultra/work/astra-sharp-ion-20261015")

a, b, c, d = av = s.symbols("a b c d")
t, k, ell, m, alpha = s.symbols("t k ell m alpha", real=True)
eta1, eta2, xi1, xi2 = s.symbols("eta1 eta2 xi1 xi2", real=True)
n = 1 + t**2
u, v, w, j = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
H = ((a-d)**2 + (b+c)**2)**2
L = t*w-j+v
B = v*(j-2*L/n)
G = k*L**2+ell*B+m*v**2
I = {a: 1, b: 0, c: 0, d: 1}
R = s.Matrix((t, 0, 1, 0))
checks = []


def zero(name, expr):
    if isinstance(expr, s.MatrixBase):
        assert all(s.cancel(entry) == 0 for entry in expr), (name, expr)
    else:
        assert s.cancel(expr) == 0, (name, s.factor(expr))
    checks.append(name)


def acoustic(F, direction):
    return s.expand((direction.T*s.hessian(F, av)*direction)[0]/2)


basis = (u*u, v*v, u*v, w*w, u*w, v*w, u*j, v*j, w*j)
fc = s.symbols("f0:9")
F9 = sum(fi*bi for fi, bi in zip(fc, basis))
rv = s.Matrix((eta1*xi1, eta1*xi2, eta2*xi1, eta2*xi2))
P = acoustic(F9, rv)
contact = I | {eta1: t, eta2: 1, xi1: 1, xi2: 0}
eqs = [P.subs(contact)] + [s.diff(P, z).subs(contact)
                                 for z in av+(eta1, eta2, xi1, xi2)]
stationarity = s.linear_eq_to_matrix(eqs, fc)[0]
minor = stationarity[[0, 1, 2, 3, 8], [0, 2, 3, 4, 5]].det()
zero("rank-five stationarity minor valid for every t != 0",
     minor+24*t*n**3*(t*t+3))
hv = s.Matrix((1, 1, 6, -4, 0, 0, -4, -4, 0))
lv = s.Matrix((0, 1, 1, t*t-1, 0, 2*t, 0, -2, -2*t))
bv = s.Matrix((0, -2/n, 0, 0, 0, -2*t/n, 0, 1+2/n, 0))
vv = s.Matrix((0, 1, 0, 0, 0, 0, 0, 0, 0))
gens = s.Matrix.hstack(hv, lv, bv, vv)
for name, coeff, poly in zip(("H", "L2", "B", "v2"),
                            (hv, lv, bv, vv), (H, L*L, B, v*v)):
    zero(f"invariant coefficient vector for {name}",
         sum(coeff[i]*basis[i] for i in range(9))-poly)
zero("all four generators satisfy every acoustic stationarity equation",
     stationarity*gens)
zero("four-generator independence minor is positive for real t",
     gens[[0, 2, 7, 1], :].det()-(n+2)/n)

x = -a+t*(b+c)+d
Q = k*x*x+2*ell*(t*b-3*d)*x/n+(2*m-ell)*b*b+3*(2*m+ell)*d*d
q = s.expand((s.Matrix(av).T*s.hessian(G, av).subs(I)*s.Matrix(av))[0]/2)
zero("exact forced-slope quadratic support", q-3*ell*j-Q)
zero("support matrix annihilates the contact R", s.hessian(Q, av)*R)
PR = acoustic(G, R)
zero("contact acoustic value", PR.subs(I))
zero("contact cubic flatness for every background direction",
     s.Matrix([s.diff(PR, z).subs(I) for z in av]))
for trip in __import__("itertools").combinations_with_replacement(av, 3):
    assert s.diff(H, *trip).subs(I) == 0
checks.append("D3H(I) vanishes identically")

A, C0 = 2*m-ell, 2*m+ell
C3 = s.Matrix(((k, ell*t/n, -3*ell/n),
                (ell*t/n, A, 0), (-3*ell/n, 0, 3*C0)))
Delta = k*n*n*A*C0-ell*ell*(t*t*C0+3*A)
zero("transverse determinant equals 3 Delta/n2", C3.det()-3*Delta/n**2)

r, y = s.symbols("r y", real=True)
ks = r*r*(t*t*(2+r)+3*(2-r))/(n*n*(4-r*r))
Gs = G.subs({m: 1, ell: r, k: ks}, simultaneous=True)
S = 2-r+t*t*(2+r)
Z = s.Matrix((-t*(2+r)*S, -2*r*t*t*(2+r),
               (2-r)*S, 2*r*t*(2-r)))
zero("second kernel direction has determinant zero", Z[0]*Z[3]-Z[1]*Z[2])
zero("second rank-one direction is independent by determinant pairing",
     t*Z[3]-Z[1]-8*r*t*t)
zx = -Z[0]+t*(Z[1]+Z[2])+Z[3]
zero("second contact lies in the PSD-equality kernel",
     C3.subs({m: 1, ell: r, k: ks}, simultaneous=True)*s.Matrix((zx, Z[1], Z[3])))
PZ = acoustic(Gs, Z)
zero("second contact has zero acoustic value", PZ.subs(I))
U = (r+2)**2*y+(r-2)**2*(2*r+1)
V = ((r+2)**3*y*y+2*(r-2)*(r+2)*(3*r-4)*y
     -3*(r-2)**3)
pref = -4*r**3*t**3/((r-2)*n)
gradient = s.Matrix([s.diff(PZ, z).subs(I) for z in av])
expected = pref*s.Matrix((-4*t*U, V, V, 4*t*U)).subs(y, t*t)
zero("exact second-contact acoustic background derivative", gradient-expected)
zero("U,V cannot both vanish in -2<r<2, r != 0",
     (r+2)*V-U*((r+2)**2*y-2*r**3+13*r*r-24*r+12)
     -4*r*r*(r-4)*(r-2)**3)

Z0 = s.Matrix((0, 1, 0, -t))
zero("ell=m=0 additional contact is rank one", Z0[0]*Z0[3]-Z0[1]*Z0[2])
Z0sub = dict(zip(av, Z0))
zero("ell=m=0 additional contact has x=0", x.subs(Z0sub, simultaneous=True))
zero("ell=m=0 additional contact has L=n", L.subs(Z0sub, simultaneous=True)-n)
P0 = acoustic(k*L*L, Z0)
zero("ell=m=0 additional contact has zero acoustic value", P0.subs(I))
zero("ell=m=0 boundary has nonzero background derivative for k>0",
     s.Matrix([s.diff(P0, z).subs(I) for z in av])-2*k*n*s.Matrix((-1,t,t,1)))

# This is a compatibility guard, not a new proof of the inherited heat theorem.
old = {t: 0, k: 1, ell: -s.Rational(1,6), m: s.Rational(1,8)}
zero("trace-free sharp J fixture is on Delta=0", Delta.subs(old))
zero("trace-free sharp J fixture has the inherited column-swapped polynomial",
     G.subs(old)-(j*j-s.Rational(5,2)*v*j+s.Rational(35,24)*v*v))

# Added only after the constructor's new cost claim was communicated.
eta, step = s.symbols("eta step", real=True)
fam = {t: 1, k: s.Rational(1,2)+eta, ell: 1, m: 1}
Zcost = s.Matrix((-1, -s.Rational(1,2), s.Rational(1,3), s.Rational(1,6)))
Ecost = s.Matrix((s.Rational(2,3), -s.Rational(1,2),
                   -s.Rational(1,2), -s.Rational(2,3)))
zero("coefficient-blowup fixed direction is rank one",
     Zcost[0]*Zcost[3]-Zcost[1]*Zcost[2])
background = s.Matrix((1,0,0,1))+step*Ecost
Pcost = acoustic(G.subs(fam)+alpha*H, Zcost).subs(
    dict(zip(av, background)), simultaneous=True)
cost_expected = (eta-s.Rational(5,18)*(18*eta+5)*step
                 +(s.Rational(25,648)*(68*eta+25)
                   +s.Rational(1250,81)*alpha)*step**2)
zero("intrinsic coefficient-blowup exact acoustic polynomial", Pcost-cost_expected)
threshold = 1/(32*eta)+s.Rational(13,80)+s.Rational(47,200)*eta
zero("coefficient-blowup discriminant forces the claimed necessary bound",
     s.discriminant(cost_expected, step)-5000*eta*(threshold-alpha)/81)
Qcost = s.hessian(Q, av).subs(fam)/2
e2cost = sum(Qcost.extract(cs,cs).det()
             for cs in __import__("itertools").combinations(range(4),2))
e3cost = sum(Qcost.extract(cs,cs).det()
             for cs in __import__("itertools").combinations(range(4),3))
zero("coefficient-blowup support e2 equals 3(10eta+7)", e2cost-3*(10*eta+7))
zero("coefficient-blowup support e3 equals 18eta", e3cost-18*eta)

sources = {
    "AGENTS.md": "AGENTS.md",
    "N873.txt": "frontier/dossiers/N873.txt",
    "inherited_stratum_REPORT.md": "updates/FX-global-completion-axis-20261015/package/derived/workers/full_invariant_genesis/REPORT.md",
    "GENERAL_FLAT_COMPLETION.md": "updates/FX-global-completion-axis-20261015/package/derived/workers/full_invariant_genesis/GENERAL_FLAT_COMPLETION.md",
}
source_hashes = {name: {"path": str(W/path),
                         "sha256": hashlib.sha256((W/path).read_bytes()).hexdigest()}
                 for name, path in sources.items()}
result = {
    "status": "PASS_EXACT_IDENTITIES",
    "protected_input_pin": PIN,
    "sympy_version": s.__version__,
    "check_count": len(checks),
    "checks": checks,
    "source_hashes": source_hashes,
    "scope": "Exact polynomial identities supporting the separate universal proof; not formal verification or external review.",
}
receipt = HERE/"EXACT_IDENTITIES.json"
receipt.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"status": result["status"], "check_count": len(checks),
                  "receipt": str(receipt)}, indent=2))
