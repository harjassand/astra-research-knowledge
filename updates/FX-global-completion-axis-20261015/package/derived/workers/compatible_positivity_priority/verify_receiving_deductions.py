#!/usr/bin/env python3
"""Exact algebra for the priority/applicability report; no QC oracle.

The analytic Iwaniec--Kristensen, matrix-factorization, density and flow
arguments remain written proofs.  This verifier checks only their receiving
identities and the new elementary contact/heat calculations.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "derived"
OUT.mkdir(exist_ok=True)
checks = []


def check(name, expression):
    value = sp.simplify(expression)
    if value != 0:
        raise AssertionError((name, value))
    checks.append(name)


a, b, c, d, n, m, t, h, k = sp.symbols("a b c d n m t h k", real=True)
x = sp.Matrix([a, b, c, d])
f = sp.symbols("f0:9", real=True)
u, v, w, j = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
basis = [u*u, v*v, u*v, w*w, u*w, v*w, u*j, v*j, w*j]
F = sum(fi*bi for fi, bi in zip(f, basis))
H = (u+v-2*j)**2
Q = n*n*sp.diff(F, a, 2)+2*n*m*sp.diff(F, a, b)+m*m*sp.diff(F, b, 2)
check("invariant relation uv=w2+j2", u*v-w*w-j*j)

# Full acoustic Gram receiving identity: six skew freedoms in an 8 by 8 PSD.
M11 = sp.hessian(sp.diff(F, a, 2), x)/2
M12 = sp.hessian(sp.diff(F, a, b), x)/2
M22 = sp.hessian(sp.diff(F, b, 2), x)/2
ks = sp.symbols("k0:6", real=True)
K = sp.zeros(4)
for value, (i, q) in zip(ks, ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))):
    K[i,q], K[q,i] = value, -value
G8 = M11.row_join(M12+K).col_join((M12-K).row_join(M22))
z8 = (n*x).col_join(m*x)
check("full acoustic 8x8 six-skew Gram identity", (z8.T*G8*z8)[0]-Q)

# All conformal backgrounds reduce to a 2 by 2 biform.
Qc = sp.expand(Q.subs({a:h, b:-k, c:k, d:h}))
coeffs = sp.Poly(Qc, h, k, n, m)
Mc = sp.Matrix([[sp.expand(co).coeff(fi) for fi in f]
                for monomial, co in coeffs.terms()])
assert Mc.rank() == 6
checks.append("conformal acoustic image rank six")
C11 = sp.hessian(sp.expand(Qc).coeff(n,2), (h,k))/2
C12 = sp.hessian(sp.expand(Qc).coeff(n,1).coeff(m,1)/2, (h,k))/2
C22 = sp.hessian(sp.expand(Qc).coeff(m,2), (h,k))/2
kap = sp.symbols("kappa", real=True)
K2 = sp.Matrix([[0,kap],[-kap,0]])
G4 = C11.row_join(C12+K2).col_join((C12-K2).row_join(C22))
z4 = sp.Matrix([n*h,n*k,m*h,m*k])
check("conformal acoustic 4x4 one-skew Gram identity", (z4.T*G4*z4)[0]-Qc)
Hcoeff = sp.Matrix([1,1,6,-4,0,0,-4,-4,0])
assert Mc*Hcoeff == sp.zeros(Mc.rows,1)
checks.append("H invisible to conformal acoustic restriction")

# Necessary critical-contact subspace at I, e1 tensor (t,1).
contact = {a:1,b:0,c:0,d:1,n:t,m:1}
rows = [sp.expand(q.subs(contact)) for q in
        [Q]+[sp.diff(Q, y) for y in (a,b,c,d,n,m)]]
M = sp.Matrix([[row.coeff(fi) for fi in f] for row in rows])
N = sp.Matrix([
    [-1,-(t*t+6),3,t*t],
    [-t**4,-3*t*t,2*t*t-3,-3*t*t],
    [-2*t*t,-6*(t*t+2),-6,-2*(2*t*t+3)],
    [-4*t*t,12,4*t*t,2*(t**4+2*t*t+3)],
    [4*t,8*t,-8*t,-4*t*(t*t+1)],
    [4*t**3,0,0,0],
    [0,4*(t*t+3),0,0],
    [0,0,4*(t*t+3),0],
    [0,0,0,4*t*(t*t+3)],
])
assert sp.simplify(M*N) == sp.zeros(7,4)
checks.append("universal polynomial contact basis annihilates all seven rows")
check("contact system positive five-minor", M[[1,2,3,4,5],[1,3,4,5,8]].det()
      -768*(t**4+2*t*t+3))
check("contact basis positive four-minor", N[[0,2,6,7],:].det()
      -32*(t*t+3)**2*(t**4+2*t*t+3))
assert M.rank() == 5 and N.rank() == 4
checks.append("contact rank five and nullity four for every real t by positive minors")
shear = sp.Matrix.hstack(Hcoeff, sp.eye(9)[:,0],
                         sp.Matrix([0,0,1,-1,0,0,0,0,0]), sp.eye(9)[:,6])
assert sp.Matrix.hstack(N.subs(t,0),shear).rank() == 4
checks.append("t zero contact space equals H,u2,j2,uj")
radial = {a:1,b:0,c:0,d:1,n:1,m:0}
radial_rows = [sp.expand(q.subs(radial)) for q in
               [Q]+[sp.diff(Q,y) for y in (a,b,c,d,n,m)]]
Mr = sp.Matrix([[row.coeff(fi) for fi in f] for row in radial_rows])
Nr = sp.Matrix.hstack(Hcoeff,sp.eye(9)[:,1],sp.eye(9)[:,3],sp.eye(9)[:,7])
assert Mr.rank() == 5 and Nr.rank() == 4 and Mr*Nr == sp.zeros(7,4)
checks.append("pure stretch contact space equals H,v2,w2,vj")

# H rank-one curvature, the preliminary classical completion channel.
p, q, r, s = sp.symbols("p q r s", real=True)
R = sp.Matrix([p*r,p*s,q*r,q*s])
CR = sp.Matrix([R[0]-R[3],R[1]+R[2]])
CA = sp.Matrix([a-d,b+c])
check("CR rank-one norm identity", (CR.T*CR)[0]-(R.T*R)[0])
Hcurv = (R.T*sp.hessian(H,x)*R)[0]
check("H exact rank-one Hessian identity", Hcurv
      -4*(CA.T*CA)[0]*(R.T*R)[0]-8*(CA.T*CR)[0]**2)

# The isotropic-orbit receiving bound plus the common shear contact.
aa0, bb0, cc0, ty, tz = sp.symbols("A0 B0 C0 ty tz", real=True)
qt = (1-ty)*u+ty*v+2*tz*w
Eorbit = aa0*qt*qt+bb0*qt*j+cc0*j*j
orb_contact = sp.diff(Eorbit,b,2).subs({a:1,b:0,c:0,d:1})
check("isotropic orbit shear-contact identity",
      orb_contact-(aa0*(8*tz*tz+4*ty)+2*bb0*ty))
rr, alp, lam = sp.symbols("r alpha lambda", real=True)
Pr = alp*H+rr*(rr-1)*u*u/6+j*j+rr*u*j
check("PC support multiplier forced independently of alpha",
      sp.diff(Pr-lam*j,b,c).subs({a:1,b:0,c:0,d:1})-(lam-rr-2))
I = {a:1,b:0,c:0,d:1}
DFI = sp.Matrix([sp.diff(Pr,xi).subs(I) for xi in x])
gap = Pr-Pr.subs(I)-(DFI.T*(x-sp.Matrix([1,0,0,1])))[0]\
      -(rr+2)*(j-1-(a-1)-(d-1))
linegap = sp.Poly(sp.expand(gap.subs({a:1+t,b:0,c:0,d:1-(rr+1)*t})),t)
low = sum(linegap.coeff_monomial(t**i)*t**i for i in range(4))
check("arbitrary alpha determinant-support cubic obstruction",
      low+rr*(rr+2)*t**3/3)

# Constant-Jacobian initial data for every nonlinear convex minor energy.
xx, yy, s0, shift = sp.symbols("x y s0 shift", real=True)
vv = sp.Matrix([s0*(xx+sp.sin(yy)), yy+sp.sin(xx+sp.sin(yy))])
AA = vv.jacobian((xx,yy))
JJ = sp.simplify(AA.det())
check("composition-of-shears determinant exactly s0", JJ-s0)
lapAA = AA.diff(xx,2)+AA.diff(yy,2)
Jdot = AA[1,1]*lapAA[0,0]+AA[0,0]*lapAA[1,1]\
       -AA[1,0]*lapAA[0,1]-AA[0,1]*lapAA[1,0]
expected = 2*s0*sp.sin(yy)*sp.cos(yy)*sp.sin(xx+sp.sin(yy))
check("heat derivative of determinant", sp.trigsimp(Jdot-expected))
check("determinant heat evolution identity", Jdot
      -(sp.diff(JJ,xx,2)+sp.diff(JJ,yy,2)-2*(AA.diff(xx).det()+AA.diff(yy).det())))
avgx = sp.integrate(sp.sin(xx+shift)**2,(xx,0,2*sp.pi))/(2*sp.pi)
avgy = sp.integrate(sp.sin(yy)**2*sp.cos(yy)**2,(yy,0,2*sp.pi))/(2*sp.pi)
check("normalized squared Jacobian derivative s0 squared over four",
      4*s0*s0*avgx*avgy-s0*s0/4)

data = {
    "basis": [str(x) for x in basis],
    "contact_ordering": ["Q","Q_a","Q_b","Q_c","Q_d","Q_n","Q_m"],
    "contact_matrix": [[str(y) for y in row] for row in M.tolist()],
    "universal_contact_basis": [[str(y) for y in row] for row in N.tolist()],
    "conformal_acoustic_polynomial": str(Qc),
    "conformal_kernel": [[str(y) for y in vec] for vec in Mc.nullspace()],
    "full_acoustic_matrices": {name:[[str(y)for y in row]for row in val.tolist()]
                               for name,val in (("M11",M11),("M12",M12),("M22",M22))},
    "conformal_acoustic_matrices": {name:[[str(y)for y in row]for row in val.tolist()]
                               for name,val in (("C11",C11),("C12",C12),("C22",C22))},
}
(OUT/"RECEIVING_ALGEBRA.json").write_text(json.dumps(data,indent=2)+"\n")
receipt = {
    "status":"PASS",
    "checks":checks,
    "number_of_checks":len(checks),
    "scope":"Exact symbolic receiving identities only. Not a QC verifier, historical priority clearance, or formal proof.",
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "algebra_sha256":hashlib.sha256((OUT/"RECEIVING_ALGEBRA.json").read_bytes()).hexdigest(),
}
(OUT/"RECEIVING_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":"PASS","number_of_checks":len(checks)},sort_keys=True))
