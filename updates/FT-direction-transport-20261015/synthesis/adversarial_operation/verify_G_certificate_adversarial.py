#!/usr/bin/env python3
"""Reconstruct exact G certificate algebra from JSON alone.

No acquisition or other verifier is imported. This checks finite algebra;
the heat-to-quasiconvexity analytic proof is in G_HEAT_REVIEW.md.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time
import sympy as s

started = time.monotonic()
root = Path(__file__).resolve().parent
certpath = root.parent / "nonlinear_qc" / "G_EXACT_HEAT_CERTIFICATE.json"
raw = certpath.read_bytes()
data = json.loads(raw)
checks = []


def record(name, detail):
    checks.append({"name": name, "status": "PASS", "detail": detail})


assert data["matrix_entry_order"] == ["a", "b", "c", "d"]
assert data["jet_order"] == ["phi1_xx", "phi1_xy", "phi1_yy", "phi2_xx", "phi2_xy", "phi2_yy"]
assert data["bilinear_order"] == "A_i jet_j, A index outer, jet index inner"
assert data["omega_pair_order"] == [[i,j] for i in range(4) for j in range(i+1,4)]
assert data["quadratic_coefficient_order"] == [[i,j] for i in range(4) for j in range(i,4)]
record("coordinate conventions", "Output-row matrix order and both compatible Hessian columns reconstructed.")

B = [[F(v) for v in row] for row in data["basis"]]
R = [[F(v) for v in row] for row in data["reduced_gram"]]
Q = [[F(v) for v in row] for row in data["gram"]]
assert len(B)==24 and all(len(row)==18 for row in B)
assert len(R)==18 and all(len(row)==18 for row in R)
assert len(Q)==24 and all(len(row)==24 for row in Q)
assert R == list(map(list, zip(*R)))
assert Q == list(map(list, zip(*Q)))
BR = [[sum(B[i][k]*R[k][j] for k in range(18)) for j in range(18)] for i in range(24)]
assert all(Q[i][j] == sum(BR[i][k]*B[j][k] for k in range(18)) for i in range(24) for j in range(24))
L = [[F(i==j) for j in range(18)] for i in range(18)]
pivots = []
for i in range(18):
    dd = R[i][i] - sum(L[i][k]**2*pivots[k] for k in range(i))
    assert dd > 0
    pivots.append(dd)
    for j in range(i+1,18):
        L[j][i]=(R[j][i]-sum(L[j][k]*L[i][k]*pivots[k] for k in range(i)))/dd
assert pivots == [F(v) for v in data["ldl_diagonal"]]
assert all(R[i][j] == sum(L[i][k]*pivots[k]*L[j][k] for k in range(18)) for i in range(18) for j in range(18))
record("positive Gram", "All576 basis/reduced/full Gram entries and324 LDL entries checked using Fraction;18 exact positive pivots.")

a,b,c,d = x = s.symbols("a b c d")
jets = s.symbols("j0:6")
Ax = s.Matrix([jets[0],jets[1],jets[3],jets[4]])
Ay = s.Matrix([jets[1],jets[2],jets[4],jets[5]])
u,v,det = a*a+c*c, b*b+d*d, a*d-b*c
G = 3*(u+v-2*det)**2+s.Rational(35,24)*u*u+det*det-s.Rational(5,2)*det*u
assert all(sum(p)==4 for p,co in s.Poly(G,*x).terms())
omega = {}
for pair, coeffs in zip(data["omega_pair_order"],data["omega_coefficients"]):
    omega[tuple(pair)] = sum(s.Rational(co)*x[i]*x[j] for co,(i,j) in zip(coeffs,data["quadratic_coefficient_order"]))


def om(i,j):
    return s.Integer(0) if i==j else omega[i,j] if i<j else -omega[j,i]


for i in range(4):
    for j in range(i+1,4):
        for k in range(j+1,4):
            assert s.expand(s.diff(om(j,k),x[i])-s.diff(om(i,k),x[j])+s.diff(om(i,j),x[k]))==0
primitive = [sum(x[j]*om(j,i) for j in range(4))/4 for i in range(4)]
for i in range(4):
    for j in range(i+1,4):
        assert s.expand(s.diff(primitive[j],x[i])-s.diff(primitive[i],x[j])-om(i,j))==0
record("closed form and primitive", "All four closedness triples and all six d-alpha coefficients verified with the declared orientation.")

diff = [[s.Rational(vv) for vv in row] for row in data["diffusion"]]
assert diff == [[s.Rational(4897,5000),0],[0,s.Rational(5103,5000)]]
H = s.hessian(G,x)
heat = diff[0][0]*(Ax.T*H*Ax)[0]+diff[1][1]*(Ay.T*H*Ay)[0]
pullback = sum(om(i,j)*(Ax[i]*Ay[j]-Ax[j]*Ay[i]) for i in range(4) for j in range(i+1,4))
Z = [xx*jj for xx in x for jj in jets]
gram_poly = sum(s.Rational(Q[i][i].numerator,Q[i][i].denominator)*Z[i]**2 for i in range(24))
gram_poly += sum(2*s.Rational(Q[i][j].numerator,Q[i][j].denominator)*Z[i]*Z[j] for i in range(24) for j in range(i+1,24))
identity = s.Poly(s.expand(gram_poly-heat-pullback),*(x+jets))
assert identity.is_zero
record("complete compatible heat identity", "Every polynomial coefficient of Gram minus anisotropic heat minus pullback vanishes exactly.")

GI = G.subs({a:1,b:0,c:0,d:1})
GJ = G.subs({a:1,b:0,c:0,d:-1})
assert GI == -s.Rational(1,24) and GJ == s.Rational(1271,24)
law = [(s.diag(36,36),s.Rational(1,2594)),(-s.diag(36,36),s.Rational(1,2594)),
       (s.diag(1,-1),s.Rational(648,1297)),(-s.diag(1,-1),s.Rational(648,1297))]
assert sum(p for A,p in law)==1
assert sum((p*A for A,p in law),s.zeros(2,2))==s.zeros(2,2)
assert sum(p*A.det() for A,p in law)==0
meanG=sum(p*G.subs({a:A[0,0],b:A[0,1],c:A[1,0],d:A[1,1]}) for A,p in law)
assert meanG == -s.Rational(1350,1297) < 0
record("nonpolyconvex lifted law", "Four explicit atoms have zero matrix/determinant barycenter and strictly negative G average−1350/1297.")

pp,qq,rr,ss=s.symbols("p q r amplitude",real=True)
Gsoft=s.expand(G.subs({a:1+s.Rational(2,3)*ss*qq,b:s.Rational(2,3)*ss*rr,c:ss*pp,d:1+ss*qq})-GI)
K=(8667*pp**4+18792*pp**3*rr+576*pp**2*qq**2+16416*pp**2*rr**2+1440*pp*qq**2*rr+6912*pp*rr**3+56*qq**4+576*qq**2*rr**2+1152*rr**4)/1944
soft=-s.Rational(5,18)*ss*qq+ss**2*(5*pp**2+4*pp*rr-4*qq**2)/12-s.Rational(5,162)*ss**3*qq*(9*pp**2+4*qq**2)+ss**4*K
assert s.expand(Gsoft-soft)==0
assert s.simplify(s.Rational(5,3)*(s.Rational(162,5))**2)==s.Rational(8748,5)
assert K.subs({pp:1,qq:0,rr:-s.Rational(3,2)})==-s.Rational(1,24)
rankprobe=s.expand(G.subs({a:1,b:ss,c:0,d:1})-s.Rational(1,100)*(2+ss**2)**2)
assert s.diff(rankprobe,ss,2).subs(ss,0)==-s.Rational(8,100)
record("complete soft action and strict-subtraction obstruction", "All cubic/quartic K coefficients, discriminant constant8748/5, negative pointwise K, and acoustic second derivative checked.")

aa,bb,cc=s.symbols("a_iso b_iso c_iso",real=True)
iso=aa*(u+v)**2+bb*(u+v)*det+cc*det**2
ih=s.hessian(iso,x)
sheardir=s.Matrix([c,d,0,0])
probe=(sheardir.T*ih*sheardir)[0]
expected=8*aa*(a*c+b*d)**2+(4*aa*(u+v)+2*bb*det)*(c*c+d*d)
assert s.expand(probe-expected)==0
decomp=(4*aa+bb)/8*(u+v+2*det)**2+(4*aa-bb)/8*(u+v-2*det)**2+(cc-4*aa)*det**2
assert s.expand(iso-decomp)==0
assert ih[0,0].subs({a:1,b:0,c:0,d:1})==16*aa+6*bb+2*cc
assert ih[0,0].subs({a:1,b:0,c:0,d:-1})==16*aa-6*bb+2*cc
record("isotropic orbit separation algebra", "Exact shear probe, convex/polyconvex decomposition and both necessary diagonal acoustic inequalities.")

fv=u*u+v*v+4*(a*b+c*d)**2+s.Rational(7,2)*det*det-s.Rational(29,10)*det*(u+v)
fH=s.hessian(fv,x)
m11=s.hessian(fH[0,0],x)/2
m12=s.hessian(fH[0,1],x)/2
m22=s.hessian(fH[1,1],x)/2
skew=s.zeros(4)
for (i,j),val in zip([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
                     [s.Rational(1,2),s.Rational(17,10),0,0,s.Rational(17,10),s.Rational(23,10)]):
    skew[i,j]=val
    skew[j,i]=-val
fq=m11.row_join(m12+skew).col_join((m12-skew).row_join(m22))
sd,td=s.symbols("sd td",real=True)
fdir=s.Matrix([sd,td,0,0])
fz=s.Matrix([sd*xx for xx in x]+[td*xx for xx in x])
assert s.expand((fdir.T*fH*fdir)[0]-(fz.T*fq*fz)[0])==0
shift=fq-s.eye(8)/16
assert all(shift[:i,:i].det()>0 for i in range(1,9))
record("mixed-cone Fstar strict acoustic premise", "Pinned prior Fstar explicit8x8 Gram reconstructed directly from Hessian; all eight shifted principal minors positive.")

coef=s.symbols("A0 B0 C0 E0 G0 H0 L0 M0 N0")
ww=a*b+c*d
inv=sum(co*mon for co,mon in zip(coef,[u*u,v*v,u*v,ww*ww,u*ww,v*ww,u*det,v*det,ww*det]))
ih=s.hessian(inv,x)
am11=s.hessian(ih[0,0],x)/2
am22=s.hessian(ih[1,1],x)/2
recover=[am11[0,0]/12,am22[1,1]/12,am11[3,3]/2,
         am11[1,1]/2-am11[3,3]/2,am11[0,1]/3,am22[0,1]/3,
         am11[0,3]/3,am22[0,3],am11[1,3]]
assert all(s.expand(left-right)==0 for left,right in zip(recover,coef))
assert s.expand(s.trace(am11)+s.trace(am22)-16*(coef[0]+coef[1])-8*coef[2]-4*coef[3])==0
record("compact acoustic section algebra", "All nine invariant coefficients recovered from two acoustic quadratic forms; positive-trace normalization identity exact.")

assert certpath.read_bytes()==raw
out={"status":"EXACT_PASS","certificate_sha256":hashlib.sha256(raw).hexdigest(),
     "groups":len(checks),"checks":checks,"seconds":time.monotonic()-started,
     "scope":"Finite exact algebra only; heat analytic implication in separate review; no external certification or historical novelty."}
root.joinpath("G_ADVERSARIAL_CHECKS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="checks"},indent=2))
