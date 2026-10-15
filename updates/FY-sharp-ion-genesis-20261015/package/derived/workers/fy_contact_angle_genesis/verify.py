#!/usr/bin/env python3
"""Exact algebraic verification; the analytic proof is in REPORT.md."""

from __future__ import annotations

from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sympy as s

import classify as compiler


ROOT = Path(__file__).resolve().parent
checks = []


def equal(name, lhs, rhs=0):
    residual = s.factor(lhs-rhs)
    assert residual == 0, (name, residual)
    checks.append({"name": name, "passed": True})


def matrix_equal(name, lhs, rhs):
    assert lhs.shape == rhs.shape
    for i in range(lhs.rows):
        for jj in range(lhs.cols):
            equal(name+f" [{i},{jj}]", lhs[i, jj], rhs[i, jj])


def check(name, predicate):
    assert predicate, name
    checks.append({"name": name, "passed": True})


a,b,c,d = compiler.COORDS
xvars = [a,b,c,d]
t = s.symbols("t", nonzero=True, real=True)
k,ell,m = s.symbols("k ell m", real=True)
f = s.symbols("f0:9")
p1,p2,q1,q2 = s.symbols("p1 p2 q1 q2")
u=a*a+c*c
v,w,j,H=compiler.v,compiler.w,compiler.j,compiler.H
n=1+t*t
L=t*w-j+v
Bt=v*(j-2*L/n)
basis=[u*u,u*v,v*v,u*w,v*w,w*w,u*j,v*j,w*j]
all_monomials=s.polys.monomials.itermonomials(xvars, 4)
monomials=sorted([z for z in all_monomials if s.total_degree(z)==4], key=str)


def vec(poly):
    poly=s.Poly(s.expand(poly),xvars)
    return s.Matrix([poly.coeff_monomial(z) for z in monomials])


V=s.Matrix.hstack(*[vec(z) for z in basis])
check("invariant basis dimension nine", V.rank()==9)
equal("H invariant identity",H,u*u+v*v+6*u*v-4*u*j-4*v*j-4*w*w)
F=sum(fi*bi for fi,bi in zip(f,basis))
R=s.Matrix([p1*q1,p1*q2,p2*q1,p2*q2])
h=s.expand((R.T*s.hessian(F,xvars)*R)[0]/2)
contact={a:1,b:0,c:0,d:1,p1:t,p2:1,q1:1,q2:0}
eqs=[h.subs(contact)]+[s.diff(h,z).subs(contact) for z in [*xvars,p1,p2,q1,q2]]
stationary=s.linear_eq_to_matrix(eqs,f)[0]
generators=s.Matrix([[1,0,0,0],[6,1,0,0],[1,1,-2/n,1],[0,0,0,0],
                     [0,2*t,-2*t/n,0],[-4,t*t-1,0,0],[-4,0,0,0],
                     [-4,-2,(t*t+3)/n,0],[0,-2*t,0,0]])
matrix_equal("generator invariant coefficients",V*generators,
             s.Matrix.hstack(*[vec(z) for z in [H,L*L,Bt,v*v]]))
matrix_equal("all contact stationarity equations",stationary*generators,s.zeros(9,4))
equal("independent generator minor",generators.extract([0,8,7,2],[0,1,2,3]).det(),
      -2*t*(t*t+3)/n)
equal("rank-five stationary minor",
      stationary.extract([0,1,2,3,8],[0,1,3,4,5]).det(),
      -24*t*n**3*(t*t+3))
rr=stationary.rref()[0]
expected=s.zeros(9,9)
expected[0,0]=1;expected[0,6]=s.Rational(1,4)
expected[1,1]=1;expected[1,6]=s.Rational(3,2);expected[1,8]=1/(2*t)
expected[2,3]=1
expected[3,4]=1;expected[3,6]=-2*t/(t*t+3);expected[3,7]=2*t/(t*t+3);expected[3,8]=n/(t*t+3)
expected[4,5]=1;expected[4,6]=-1;expected[4,8]=(t*t-1)/(2*t)
matrix_equal("five explicit stationary constraints",rr,expected)
G,C,Q4,A0,B0,Delta=compiler.form(t,k,ell,m)
x=-a+t*(b+c)+d
Q=k*x*x+2*ell*(t*b-3*d)*x/n+A0*b*b+3*B0*d*d
spI={a:1,b:0,c:0,d:1}
equal("forced determinant support",(s.Matrix(xvars).T*s.hessian(G,xvars).subs(spI)*s.Matrix(xvars))[0]/2-3*ell*j,Q)
equal("transverse determinant",C.det(),3*Delta/n**2)
equal("e3 four-dimensional support",compiler.elementary(Q4,3),3*Delta/n)
Rt=s.Matrix([t,0,1,0])
matrix_equal("contact quadratic kernel",Q4*Rt,s.zeros(4,1))
equal("conformal cubic flatness on contact",(Rt.T*s.hessian(G,xvars)*Rt)[0].subs(spI)/2)
for z in xvars:
    equal("conformal acoustic background stationarity "+str(z),s.diff((Rt.T*s.hessian(G,xvars)*Rt)[0]/2,z).subs(spI))
for z in xvars:
    equal("H third-derivative contact flatness "+str(z),s.diff((Rt.T*s.hessian(H,xvars)*Rt)[0]/2,z).subs(spI))
free_x,free_b,free_d=s.symbols("free_x free_b free_d")
free_c=(free_x*free_d-t*free_b*free_d-free_d**2)/(t*free_d-free_b)
free_a=t*(free_b+free_c)+free_d-free_x
equal("dense rank-one parametrization",free_a*free_d-free_b*free_c)
equal("dense parametrization transverse coordinate",-free_a+t*(free_b+free_c)+free_d,free_x)

# Nonzero-coupling singular boundary, with two rank-one lines.
kbd=ell**2*(t*t*B0+3*A0)/(n*n*A0*B0)
Z=s.Matrix([-(B0*t*t+A0)/(2*A0*n),-ell*t/(A0*n),
            (B0*t*t+A0)/(2*t*B0*n),ell/(B0*n)])
equal("second boundary direction rank one",Z[0]*Z[3]-Z[1]*Z[2])
equal("second boundary direction transverse x",-Z[0]+t*(Z[1]+Z[2])+Z[3],1)
matrix_equal("second boundary direction kernel",Q4.subs(k,kbd)*Z,s.zeros(4,1))
factorZ=s.Matrix([-t*B0,A0])*s.Matrix([[B0*t*t+A0,2*ell*t]])/(2*t*A0*B0*n)
matrix_equal("second boundary rank-one factorization",Z.reshape(2,2),factorZ)
P=m*B0*B0*t*t+A0*A0*(2*ell+m)
S=B0**3*t**4+2*(4*m-3*ell)*A0*B0*t*t+3*A0**3
g=ell**3*t*s.Matrix([-4*t*P,S,S,4*t*P])/(A0**3*B0**2*n**3)
hZ=(Z.T*s.hessian(G,xvars)*Z)[0]/2
equal("second boundary contact",hZ.subs(k,kbd).subs(spI))
for i,z in enumerate(xvars):
    equal("second boundary full acoustic gradient "+str(z),s.diff(hZ,z).subs(k,kbd).subs(spI),g[i])
equal("kernel determinant mixed coefficient",t*ell/(n*B0)+ell*t/(n*A0),4*ell*t*m/(n*A0*B0))

# ell=m=0 has its own rank-one obstruction.
Z0=s.Matrix([0,1,0,-t])
hZ0=(Z0.T*s.hessian(k*L**2,xvars)*Z0)[0]/2
equal("square-only kernel rank one",Z0[0]*Z0[3]-Z0[1]*Z0[2])
equal("square-only contact",hZ0.subs(spI))
equal("square-only L(Z0)",L.subs(dict(zip(xvars,Z0))),n)
for i,z in enumerate(xvars):
    equal("square-only acoustic gradient "+str(z),s.diff(hZ0,z).subs(spI),2*k*n*s.Matrix([-1,t,t,1])[i])

# H Bregman square certificates used in the analytic proof.
s0,r0,h0=s.symbols("s0 r0 h0")
remainder=2*s0*r0+4*h0*h0+4*h0*r0+r0*r0
equal("H mixed and quartic lower-bound identity",remainder-s0*r0-r0*r0/5,
      (s0*r0-h0*h0)+5*(h0+2*r0/5)**2)
equal("H pure quartic lower-bound identity",remainder-r0*r0/3,
      2*(s0*r0-h0*h0)+6*(h0+r0/3)**2)

# The completion coefficient must diverge on an explicit interior family.
eta=s.symbols("eta",positive=True)
blowup_G=compiler.form(s.Integer(1),s.Rational(1,2)+eta,s.Integer(1),s.Integer(1))[0]
blowup_Z=s.Matrix([-1,-s.Rational(1,2),s.Rational(1,3),s.Rational(1,6)])
blowup_E=s.Matrix([s.Rational(2,3),-s.Rational(1,2),-s.Rational(1,2),-s.Rational(2,3)])
blowup_h=(blowup_Z.T*s.hessian(blowup_G,xvars)*blowup_Z)[0]/2
blowup_slope=sum(s.diff(blowup_h,z).subs(spI)*blowup_E[i] for i,z in enumerate(xvars))
blowup_quad=compiler.acoustic_at(blowup_G,blowup_E,blowup_Z)
blowup_H=compiler.acoustic_at(H,blowup_E,blowup_Z)
equal("blowup family conformal acoustic",blowup_h.subs(spI),eta)
equal("blowup family acoustic slope",blowup_slope,-5*(18*eta+5)/18)
equal("blowup family acoustic quadratic",blowup_quad,25*(68*eta+25)/648)
equal("blowup family H quadratic",blowup_H,s.Rational(1250,81))
equal("blowup family necessary coefficient",(blowup_slope**2/(4*eta)-blowup_quad)/blowup_H,
      1/(32*eta)+s.Rational(13,80)+s.Rational(47,200)*eta)
equal("blowup family strict support determinant",Delta.subs({t:1,k:s.Rational(1,2)+eta,ell:1,m:1}),12*eta)

# Orthogonal conjugation: use the polynomial numerator to avoid radicals.
U=s.Matrix([[t,1],[1,-t]])
matrix_equal("normalizing orthogonal numerator",U.T*U,n*s.eye(2))
requested=s.Matrix([[t,1],[0,0]])
matrix_equal("requested contact normalization",U*requested*U.T/n,Rt.reshape(2,2))
amat=s.Matrix([[a,b],[c,d]])
conjugated=U*amat*U.T/n
equal("H preserved by normalization",H.subs(dict(zip(xvars,list(conjugated))),simultaneous=True),H)
equal("det preserved by normalization",conjugated.det(),j)

# t=0 sharp family retains a tangent determinant kernel and known QC cases.
r=s.symbols("r",real=True)
special={t:0,k:1,ell:(r+2)/3,m:(r+1)*(r+2)/6}
equal("trace-free sharp polynomial",G.subs(special,simultaneous=True),j*j+r*v*j+r*(r-1)*v*v/6)
Cs=C.subs(special,simultaneous=True)
diagonal=s.Matrix([-(r+1),0,0,1])
Qsharp=Q4.subs(special,simultaneous=True)
matrix_equal("trace-free diagonal kernel",Qsharp*diagonal,s.zeros(4,1))
ss,zz=s.symbols("ss zz")
kernel=ss*s.Matrix([0,0,1,0])+zz*diagonal
equal("trace-free tangent determinant",kernel[0]*kernel[3]-kernel[1]*kernel[2],-(r+1)*zz**2)
GS=G.subs(special,simultaneous=True)
cubic_diagonal=sum(s.diff(GS,x1,x2,x3).subs(spI)*diagonal[i1]*diagonal[i2]*diagonal[i3]
                   for i1,x1 in enumerate(xvars) for i2,x2 in enumerate(xvars) for i3,x3 in enumerate(xvars))/24
equal("trace-free nonflat sharp cubic",cubic_diagonal,-r*(r+2)/12)

# Nonshear limit after the necessary parameter rescaling.
K,E,M=s.symbols("K E M",real=True)
scaled=G.subs({k:K/t**2,ell:E,m:M})
equal("nonshear polynomial limit",s.limit(scaled,t,s.oo),K*w*w+E*v*j+M*v*v)
equal("nonshear determinant limit",s.limit(Delta.subs({k:K/t**2,ell:E,m:M})/t**2,t,s.oo),
      (2*M+E)*(K*(2*M-E)-E*E))

# Isotropic comparison: only H lies in this generic stationary span.
ia,ib,ic=s.symbols("ia ib ic")
norm2=a*a+b*b+c*c+d*d
isotropic=ia*norm2**2+ib*norm2*j+ic*j*j
hi=s.expand((R.T*s.hessian(isotropic,xvars)*R)[0]/2)
ieqs=[hi.subs(contact)]+[s.diff(hi,z).subs(contact) for z in [*xvars,p1,p2,q1,q2]]
IM=s.linear_eq_to_matrix(ieqs,[ia,ib,ic])[0]
check("isotropic stationary intersection dimension one",IM.rank()==2)
matrix_equal("isotropic stationary intersection is H",IM*s.Matrix([1,-4,4]),s.zeros(9,1))

# Exact parser, full decision branches, and instantiated all-alpha witnesses.
check("decimal parser exact",compiler.rational(compiler.load_exact_json('{"x": 0.12345678901234567890123456789}')["x"]) == s.Rational("0.12345678901234567890123456789"))
check("scientific decimal parser exact",compiler.rational(compiler.load_exact_json('{"x": 1.234567890123456789e-18}')["x"]) == s.Rational("1.234567890123456789e-18"))
for bad in [1.25,True,False,Decimal("NaN"),Decimal("Infinity")]:
    try:
        compiler.rational(bad)
    except (ValueError,TypeError,OverflowError):
        check("reject invalid exact input "+repr(bad),True)
    else:
        raise AssertionError("accepted invalid input")
cases=[
    ("strict negative coupling",["1","2","-1","3/4"],"ADMITTED_QC_COMPLETION"),
    ("strict zero coupling",["-2","1","0","1"],"ADMITTED_QC_COMPLETION"),
    ("convex exception",["1","0","0","1"],"ADMITTED_QC_COMPLETION"),
    ("zero exception",["-3","0","0","0"],"ADMITTED_QC_COMPLETION"),
    ("positive coupling singular",["1","1/2","1","1"],"NO_FINITE_ROC_OR_QC_COMPLETION"),
    ("negative coupling singular",["1","5/6","-1","1"],"NO_FINITE_ROC_OR_QC_COMPLETION"),
    ("square-only singular",["-2","3/4","0","0"],"NO_FINITE_ROC_OR_QC_COMPLETION"),
    ("negative k",["1","-1","0","1"],"NO_FINITE_ROC_OR_QC_COMPLETION"),
    ("negative m",["1","0","0","-1"],"NO_FINITE_ROC_OR_QC_COMPLETION"),
    ("zero transverse diagonal",["1","100","1","1/2"],"NO_FINITE_ROC_OR_QC_COMPLETION"),
    ("trace-free excluded",["0","1","-1/3","1/3"],"OUT_OF_SCOPE_TRACE_FREE"),
]
case_outputs={}
for name,values,status in cases:
    data=dict(zip(["t","k","ell","m"],values)) | {"alpha":"12345/7","reserve":"1"}
    result=compiler.classify(data)
    check("classifier "+name,result["status"]==status)
    if "witness" in result:
        wit=result["witness"]
        tm,km,lm,mm=[compiler.rational(z) for z in values]
        poly=compiler.form(tm,km,lm,mm)[0]+s.Rational(data["alpha"])*H
        background=[s.Rational(z) for row in wit["background"] for z in row]
        direction=[s.Rational(z) for row in wit["rank_one_direction"] for z in row]
        equal("instantiated boundary witness direct evaluation "+name,
              compiler.acoustic_at(poly,background,direction),s.Rational(wit["half_acoustic_value"]))
        check("instantiated boundary witness negative "+name,s.Rational(wit["half_acoustic_value"])<0)
    case_outputs[name]=result

result={"status":"PASS","scope":"Exact polynomial identities, fixed-dimensional projection branches, parser boundaries, and explicit acoustic witness evaluations. The universal analytic proof is REPORT.md.",
        "pinned_revision":"b32943eeb62d0d79929a9e572a344219a785ebf9",
        "number_of_assertions":len(checks),"checks":checks,"case_outputs":case_outputs,
        "external_correctness":"UNKNOWN","historical_originality":"UNKNOWN"}
(ROOT/"verification.json").write_text(json.dumps(result,indent=2)+"\n")
receipt={"files":{},"verification_status":"PASS","number_of_assertions":len(checks),
         "scope":"Hashes establish file integrity; exact checks establish their recorded algebraic scope, not external correctness or novelty."}
for file in ["REPORT.md","classify.py","verify.py","verification.json",
             "NORMAL_FORM_AND_COMPOSITION.md","SOURCES.json"]:
    raw=(ROOT/file).read_bytes()
    receipt["files"][file]={"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)}
(ROOT/"RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":"PASS","number_of_assertions":len(checks),"output":str(ROOT/"verification.json")}))
