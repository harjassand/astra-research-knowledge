#!/usr/bin/env python3
"""Finite exact algebra for REPORT.md; analytic proofs remain in that report."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import sympy as s

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent.parent / "originals" / "conformal_packet"
checks = []

def check(name, condition, detail=None):
    if not bool(condition):
        raise RuntimeError("FAILED: " + name)
    checks.append({"name": name, "status": "PASS", "detail": detail})
    print("PASS", name, flush=True)

def zero(expr):
    return s.cancel(s.expand(expr)) == 0

a, b, c, d = s.symbols("a b c d", real=True)
r = s.symbols("r", positive=True)
sigma = r + 1
kappa = r * (r + 2) / 3
alpha = 3 * r / (8 * (r + 2))
tau = (2 * r + 1) / 3
u = a*a + c*c
v = b*b + d*d
j = a*d - b*c
w = a*b + c*d
J = alpha*(u+v-2*j)**2 + r*(r-1)*u*u/6 + j*j + r*u*j
q = sigma*a + d
P = q*(2*a*q-(r+2)*a*a+r*c*c-2*b*c)-kappa*a*(a*a+c*c)
check("cubic density equals derivative of unchanged quartic", zero(P-s.diff(J,a)-s.diff(J,d)))

M = s.Matrix([[tau*tau, s.Rational(1,3), 2*tau],
              [s.Rational(1,3), 1, -2],
              [2*tau, -2, s.Rational(16,3)+1/alpha]])
z = s.Matrix([u,v,j])
check("coercivity calibration identity", zero(J-alpha*(z.T*M*z)[0]-4*alpha*w*w/3))
expected_minors = [tau*tau, 4*r*(r+1)/9, 16*(r+1)/27]
check("three positive principal-minor formulas", all(zero(M[:i,:i].det()-e) for i,e in enumerate(expected_minors,1)))
check("trace formula", zero(s.trace(M)-tau*tau-s.Rational(19,3)-1/alpha))
check("positive rational coercivity coefficient formula", zero(2*alpha*M.det()/s.trace(M)**2 - 4*r*(r+1)/(9*(r+2)*s.trace(M)**2)))
check("scalar-row cubic coefficient", zero(P.subs({c:0,d:0})-r*(2*r+1)*a**3/3))

x,y = s.symbols("x y", real=True)
Fpieces = [(x,0,s.Rational(2,3)), (2*(1-x),s.Rational(2,3),1)]
Gpieces = [(2*y,0,s.Rational(1,2)), (2*(1-y),s.Rational(1,2),1)]
integrals = [s.Integer(0),s.Integer(0),s.Integer(0)]
for FF,x0,x1 in Fpieces:
    for GG,y0,y1 in Gpieces:
        aval=s.diff(FF,x)*GG
        bval=FF*s.diff(GG,y)
        sub={a:aval,b:bval,c:0,d:0}
        for i,expr in enumerate([J,q*q+kappa*c*c,P]):
            integrals[i] += s.integrate(s.integrate(s.expand(expr.subs(sub)),(x,x0,x1)),(y,y0,y1))
expected = [r*(12*r*r+12*r+35)/(60*(r+2)), 2*(r+1)**2/3, -r*(2*r+1)/6]
check("exact zero-boundary product-tent integrals", all(zero(a0-b0) for a0,b0 in zip(integrals,expected)), [str(s.factor(v0)) for v0 in integrals])
Ar,Qr,Cr=[s.cancel(v0.subs(r,1)) for v0 in integrals]
check("r=1 template values and squared quotient", [Ar,Qr,Cr]==[s.Rational(59,180),s.Rational(8,3),-s.Rational(1,2)] and Cr*Cr/(4*Ar*Qr)==s.Rational(135,1888))

eps,weight,q0 = s.symbols("eps weight q0", positive=True)
c0 = s.symbols("c0", nonzero=True, real=True)
ell = eps*s.sqrt(weight)/q0
outamp = s.sqrt(eps*weight/q0)
gradamp = s.simplify(outamp/ell)
check("cloud common gradient multiplier", s.simplify(gradamp-s.sqrt(q0/eps))==0)
Ai=s.simplify(ell**2*gradamp**4)
Qi=s.simplify(ell**2*gradamp**2*q0)
Ci=s.simplify(ell**2*gradamp**3*c0)
check("cloud individual A,Q,C formulas", Ai==weight and Qi==eps*weight and s.simplify(Ci-s.sqrt(eps)*weight*c0/s.sqrt(q0))==0)
check("cloud preserves squared quotient", s.simplify((s.sqrt(eps)*c0/s.sqrt(q0))**2/(4*eps)-c0*c0/(4*q0))==0)

weights=[F(9,25),F(16,25)]
radii=[F(3,2000),F(1,500)]
grad=F(20)
qbase=F(4)
cbase=F(2)
aval=sum(l*l*grad**4 for l in radii)
qval=sum(l*l*grad**2*qbase for l in radii)
cval=sum(l*l*grad**3*cbase for l in radii)
check("rational two-copy exact fixture", aval==1 and qval==F(1,100) and cval==F(1,10) and cval*cval/(4*aval*qval)==F(1,4), {"A":str(aval),"Q":str(qval),"C":str(cval)})
check("rational fixture copy weights", all(l*l*grad**4==wi for l,wi in zip(radii,weights)))
check("cloud support area independent of weight partition", s.simplify(ell**2-eps**2*weight/q0**2)==0)
check("cloud pth-moment homogeneity at selected powers", all(s.simplify(ell**2*gradamp**pp-weight*eps**(2-s.Rational(pp,2))*q0**(s.Rational(pp,2)-2))==0 for pp in [2,3,4,6,8]))

lam,amp = s.symbols("lam amp", positive=True)
As=amp**4/lam**2
Qs=amp**2
Cs=amp**3/lam
check("general isotropic quotient invariance", s.cancel(Cs**2/(As*Qs)-1)==0)
check("critical isotropic A,Q,C scaling", s.simplify(As.subs(amp,s.sqrt(lam)))==1 and s.simplify(Qs.subs(amp,s.sqrt(lam)))==lam and s.simplify(Cs.subs(amp,s.sqrt(lam))-s.sqrt(lam))==0)
check("truncation power arithmetic", s.Rational(4)-s.Rational(8,3)==s.Rational(4,3) and s.Rational(4,3)/4==s.Rational(1,3))

pp=s.symbols("p", positive=True)
gamma=(pp-4)/(3*pp-8)
check("higher-moment optimization exponents", zero((1-s.Rational(4)/(3*pp-8))/3-gamma) and zero(4/(3*pp-8)*(pp-4)/4-gamma))
theta,A0,Q0,C0,T0,MM=s.symbols("theta A0 Q0 C0 T0 MM", positive=True)
check("common integration-measure invariance", s.simplify(theta*C0/s.sqrt(theta*A0*theta*Q0)-C0/s.sqrt(A0*Q0))==0 and s.simplify(MM*s.sqrt(theta*Q0)/s.sqrt(theta*A0)-MM*s.sqrt(Q0)/s.sqrt(A0))==0 and s.cancel(theta*T0/(theta*A0)-T0/A0)==0)

receipt={
    "schema":"astra-independent-concentration-audit-exact-checks/1",
    "status":"PASS",
    "groups":len(checks),
    "checks":checks,
    "source_sha256":{name:hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in ["RESEARCH_REPORT.md","verify_compatibility.py"]},
    "self_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "python":sys.version,
    "sympy":s.__version__,
    "scope":"Finite algebra and homogeneity only. Analytic interpolation, density, packing, and weak limits are proved in REPORT.md; no sharp QC inequality, external validation, or priority is certified."
}
(ROOT/"EXACT_CHECKS.json").write_text(json.dumps(receipt,indent=2)+"\n")
print("PASS",len(checks),"finite groups",flush=True)
