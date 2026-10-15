"""Exact finite checks for UNIVERSAL_PROFILE_OBSTRUCTIONS.md.

Run with Python 3 and SymPy. No optimization results, prior verifier output,
or downloaded manuscripts are inputs. These checks do not formalize the
high-frequency localization, Sobolev weak-convergence, or convex-duality proofs.
"""
from __future__ import annotations

import json
from pathlib import Path
from itertools import product
import sympy as s

ROOT = Path(__file__).resolve().parent
REPORT: dict[str, object] = {
    "status": "running",
    "scope": "exact finite algebra only; analytic proofs are in the note",
    "groups": [],
}

def zero(expr: s.Expr) -> None:
    assert s.simplify(s.expand(expr)) == 0, s.simplify(expr)

def passed(name: str, **data: object) -> None:
    item = {"name": name, "passed": True, **data}
    REPORT["groups"].append(item)
    print(f"PASS {len(REPORT['groups'])}: {name}", flush=True)

def exponents(n: int, degree: int):
    for ex in product(range(degree + 1), repeat=n):
        if sum(ex) == degree:
            yield ex

def mono(xs, ex):
    return s.prod(x**e for x, e in zip(xs, ex))

# 1. Column identity, including every homogeneous planar quartic monomial.
a, b, c, d = x = s.symbols("a b c d", real=True)
p1, p2, q1, q2 = s.symbols("p1 p2 q1 q2", real=True)
P = s.Matrix([p1, 0, p2, 0])
Q = s.Matrix([0, q1, 0, q2])
X = s.Matrix(x)
count = 0
for ex in exponents(4, 4):
    f = mono(x, ex)
    df = s.Matrix([s.diff(f, xi) for xi in x])
    shifted = lambda vec: f.subs(dict(zip(x, vec)), simultaneous=True)
    dfq = df.subs(dict(zip(x, X + Q)), simultaneous=True)
    R1 = shifted(X + Q + P) - shifted(X + Q) - dfq.dot(P)
    R2 = shifted(X + Q) - f - df.dot(Q)
    zero(shifted(X + P + Q) - f - R1 - R2 - dfq.dot(P) - df.dot(Q))
    count += 1
assert count == 35
passed("two-column circulation bookkeeping", homogeneous_monomials=count)

# 2. Euler derivative: the second-jet coefficient really is -p_qq.
z = s.symbols("z1 z2", real=True)
q = s.symbols("q1 q2", real=True)
h = s.symbols("h1 h2", real=True)
v = s.symbols("v1 v2", real=True)
w = s.symbols("w1 w2", real=True)
xs = z + q
count = 0
for deg in range(5):
    for ex in exponents(4, deg):
        p = mono(xs, ex)
        first = sum(s.diff(p,z[i])*v[i]+s.diff(p,q[i])*w[i] for i in range(2))
        flux = sum(s.diff(p,q[i])*v[i] for i in range(2))
        total_derivative = sum(s.diff(flux,z[i])*q[i]+s.diff(flux,q[i])*h[i]+s.diff(flux,v[i])*w[i] for i in range(2))
        euler = [s.diff(p,z[i])-sum(s.diff(p,q[i],z[j])*q[j]+s.diff(p,q[i],q[j])*h[j] for j in range(2)) for i in range(2)]
        zero(first-total_derivative-sum(euler[i]*v[i] for i in range(2)))
        for i in range(2):
            for j in range(2):
                zero(s.diff(euler[i],h[j])+s.diff(p,q[i],q[j]))
        count += 1
assert count == 70
kap, f1, f2 = s.symbols("kap f1 f2", real=True)
p = f1*z[0]+f2*z[1]+kap*(z[0]*q[1]-z[1]*q[0])/2
euler = [s.diff(p,z[i])-sum(s.diff(p,q[i],z[j])*q[j] for j in range(2)) for i in range(2)]
zero(euler[0]-f1-kap*q[1]); zero(euler[1]-f2+kap*q[0])
passed("local first-jet Euler derivative and oriented area variation", monomials=count)

# 3. Determinant-affine support transforms into an affine lift correctly.
B = s.Matrix(2,2,s.symbols("B0:4",real=True))
Y = s.Matrix(2,2,s.symbols("Y0:4",real=True))
cof = s.Matrix([[B[1,1],-B[1,0]],[-B[0,1],B[0,0]]])
zero((B+Y).det()-B.det()-s.trace(cof.T*Y)-Y.det())
passed("minor-support lift algebra")

# 4. Independently verify the Dacorogna-Marcellini endpoint ROC quadratic.
norm2 = sum(t*t for t in x)
det = a*d-b*c
DM = norm2**2 - 4/s.sqrt(3)*norm2*det
acoustic = s.diff(DM,a,2)
squares = 12*(a-d/s.sqrt(3))**2 + 2*(1+1/s.sqrt(3))*(b+c)**2 + 2*(1-1/s.sqrt(3))*(b-c)**2
zero(acoustic-squares)
DM_I = s.simplify(DM.subs({a:1,b:0,c:0,d:1}))
assert DM_I < 0
passed("Dacorogna-Marcellini rank-one acoustic squares", value_at_identity=str(DM_I))

# 5. Negative entry/return strip and scale-invariant trace obstruction.
t = s.symbols("t", real=True)
r = t/2
energy = (s.Rational(1,4)+r*r)**2 - 4/s.sqrt(3)*(s.Rational(1,4)+r*r)*(r/2)
action = s.simplify(s.integrate(energy,(t,0,2)))
zero(action-(s.Rational(103,120)-s.sqrt(3)/2))
assert s.Rational(3,4)-s.Rational(103,120)**2 == s.Rational(191,14400)
zero(DM.subs({xi:-xi for xi in x},simultaneous=True)-DM)
trace_exponent=s.symbols("trace_exponent",real=True)
scale_exp=4*(1-trace_exponent)-1
zero(scale_exp.subs(trace_exponent,s.Rational(3,4)))
passed("negative compatible entry and reversed exit; critical scaling",
       action=str(action),positive_squared_sign_margin="191/14400",trace_power="3/4")

# 6. General spiral construction: derivative columns and determinant sign.
al, be, n = s.symbols("alpha beta n",real=True)
v0 = s.Matrix(s.symbols("v01 v02",real=True))
J = s.Matrix([[0,-1],[1,0]])
Aspiral = s.Matrix.hstack(al*v0+be*J*v0,n*J*v0)
zero(Aspiral.det()-al*n*v0.dot(v0))
passed("rotation-exponential compatible negative-entry algebra")

# 7. Perspective convexity identity and the exact duration stationarity equation.
tau=s.symbols("tau",positive=True)
w0,p0=s.symbols("w0 p0",real=True)
co=s.symbols("f0:5",real=True)
xscalar=s.symbols("z",real=True)
f=sum(co[j]*xscalar**j for j in range(5))
W=tau*f.subs(xscalar,w0+p0/tau)
zero(s.diff(W,tau,2)-p0**2/tau**3*s.diff(f,xscalar,2).subs(xscalar,w0+p0/tau))
ed=s.symbols("a0:5",real=True)
W=sum(ed[j]*tau**(1-j) for j in range(5))
zero(tau**4*s.diff(W,tau)-(ed[0]*tau**4-ed[2]*tau**2-2*ed[3]*tau-3*ed[4]))
passed("perspective timing and quartic stationarity")

# 8. Exact failure of the fixed Poisson storage on a convex quartic.
rho,lam,coef,vel = s.symbols("rho lam coef vel",real=True)
Frho=(a*a+c*c+rho*rho*(b*b+d*d)-2*rho*det)**2
odd=s.expand((Frho-Frho.subs({c:-c,d:-d},simultaneous=True))/2)
zero(odd+4*rho*det*(a*a+c*c+rho*rho*(b*b+d*d)))
res=(vel-rho)**4+2*coef*rho*(lam*lam+rho*rho)*vel
explicit=s.factor(res.subs({rho:s.Rational(1,4),lam:1,coef:1,vel:-s.Rational(1,12)}))
assert explicit == -s.Rational(331,10368)
zero(res.subs(vel,rho)-2*coef*rho*rho*(lam*lam+rho*rho))
zero(s.expand(res.subs(vel,-rho/3)).coeff(rho,2)+s.Rational(2,3)*coef*lam**2)
passed("fixed Poisson storage fails for an explicitly convex quartic",residual=str(explicit))

# 9. A multi-frequency failure for the DM endpoint, all exact Laurent algebra.
zz,rr=s.symbols("zz rr")
ii=s.I
cs=lambda k:(zz**k+zz**(-k))/2
sn=lambda k:(zz**k-zz**(-k))/(2*ii)
dy=lambda f:s.expand(ii*zz*s.diff(f,zz))
dx=lambda f:s.expand(rr*s.diff(f,rr))
mean=lambda f:s.expand(f).coeff(zz,0)
def half_integral(poly):
    terms=s.Poly(mean(poly),rr).terms()
    assert all(ex[0]>0 for ex,_ in terms)
    return s.simplify(sum(c/s.Integer(ex[0]) for ex,c in terms))
ff=rr*cs(1)-s.Rational(1,5)*rr**2*sn(2)-s.Rational(1,6)*rr**3*cs(3)
hh=-s.Rational(3,8)+s.Rational(7,6)*rr*sn(1)+s.Rational(1,10)*rr**2*cs(2)-s.Rational(1,2)*rr**3*sn(3)
fx,fy,hx,hy=dx(ff),dy(ff),dx(hh),dy(hh)
dI=half_integral((fx*hy-hx*fy)*(fx*fx+fy*fy))
assert dI == s.Rational(265631,360000)
p=fy.subs(rr,1); vv=hh.subs(rr,1)
n4=s.simplify(mean((vv*vv+p*p)**2))
L=s.simplify(mean((vv*vv+p*p)**2+4/s.sqrt(3)*vv*p*(vv*vv+p*p)))
DP=-2/s.sqrt(3)*dI
res=s.simplify(L-DP)
aa=s.Rational(550762363,69120000);bb=s.Rational(6118187,1296000)
zero(res-aa+bb*s.sqrt(3))
assert aa>0 and bb>0 and 3*bb*bb-aa*aa>0
assert n4==aa
passed("coupled-frequency failure of DM Poisson candidate",integral=str(dI),residual=str(res),norm_fourth=str(n4),ratio_decimal=str(s.N(res/n4,18)))

# 10. G has an exact global rank-one-convexity certificate independent of searches.
u=a*a+c*c;v=b*b+d*d
G=3*(u+v-2*det)**2+s.Rational(35,24)*u*u+det*det-s.Rational(5,2)*det*u
M11=s.hessian(s.diff(G,a,2),x)/2
M12=s.hessian(s.diff(G,a,b),x)/2
M22=s.hessian(s.diff(G,b,2),x)/2
K=s.zeros(4)
for (i,j),val in zip([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)], [11,s.Rational(91,6),0,0,11,s.Rational(41,3)]):
    K[i,j]=val;K[j,i]=-val
Gram=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
minors=[Gram[:j,:j].det() for j in range(1,7)]
assert minors==[s.Rational(107,2),642,s.Rational(1605,8),s.Rational(8445,16),s.Rational(2815,8),s.Rational(26865,4)]
C=Gram[:6,:6];E=Gram[:6,6:];D=Gram[6:,6:]
assert D-E.T*C.inv()*E==s.zeros(2)
ss,tt=s.symbols("ss tt",real=True)
xx=s.Matrix(x); bil=ss*xx; bil=bil.col_join(tt*xx)
rankdir=s.Matrix([ss,tt,0,0])
zero((bil.T*Gram*bil)[0]-(rankdir.T*s.hessian(G,x)*rankdir)[0])
rotder=s.diff(G,a)*(-c)+s.diff(G,b)*(-d)+s.diff(G,c)*a+s.diff(G,d)*b
zero(rotder)
assert G.subs({a:1,b:0,c:0,d:1})==-s.Rational(1,24)
passed("independent rational acoustic certificate for G",rank=6,leading_minors=[str(z) for z in minors])

REPORT["status"]="all_checks_passed"
REPORT["group_count"]=len(REPORT["groups"])
(ROOT/"universal_verification.json").write_text(json.dumps(REPORT,indent=2)+"\n")
print(f"ALL {REPORT['group_count']} GROUPS PASSED",flush=True)
