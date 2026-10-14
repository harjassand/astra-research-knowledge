#!/usr/bin/env python3
"""Fresh exact delta audit of the deflation minimum and stability bounds.

Reconstructs the Fourier averages directly from independent sine/cosine
moments; does not import or execute the root/worker checker scripts.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import sympy as s

OUT = Path(__file__).resolve().parent
sx,cx,sy,cy,e = s.symbols("sx cx sy cy eps", real=True)
trig_ideal=s.groebner((sx**2+cx**2-1,sy**2+cy**2-1),sx,cx,sy,cy,order="lex",domain="EX")

def one_angle_moment(ps: int, pc: int):
    if ps % 2 or pc % 2:
        return s.S.Zero
    m,n=ps//2,pc//2
    return s.Rational(math.factorial(2*m)*math.factorial(2*n),
                      4**(m+n)*math.factorial(m)*math.factorial(n)*math.factorial(m+n))

def avg(poly):
    P=s.Poly(s.expand(poly),sx,cx,sy,cy,domain="EX")
    out=s.S.Zero
    for powers,coef in P.terms():
        out += coef*one_angle_moment(powers[0],powers[1])*one_angle_moment(powers[2],powers[3])
    return s.factor(out)

def assert_zero(x):
    assert s.factor(s.cancel(x)) == 0, s.factor(s.cancel(x))

def assert_trig_zero(x):
    rem=trig_ideal.reduce(s.expand(x))[1]
    assert s.expand(rem)==0,s.factor(rem)

def assert_matrix_zero(M):
    for entry in M:
        assert_zero(entry)

X0=s.Matrix([[cx*cy,-sx*sy],[sx*sy,-cx*cy]])
Y=s.diag(-(cx**2-sx**2)/2,-(cy**2-sy**2)/2)
Z=s.Matrix([[0,cy],[cx,0]])
X=(X0+e*Y+e**2*Z).applyfunc(s.expand)
q0=s.expand(X0.det());q=s.expand(X.det())
assert_trig_zero(q0+(cx**2-sx**2+cy**2-sy**2)/2)
assert avg(q0**2)==s.Rational(1,4)
assert_trig_zero(s.trace(X)-e*q0)
assert avg(q)==0

v=s.Matrix([X[0,0],X[0,1],X[1,0],X[1,1]])
C=s.Matrix(4,4,lambda i,j:avg(v[i]*v[j]))
aa,bb,cc,dd=s.symbols("a b c d",real=True)
v0=s.Matrix([aa,bb,cc,dd]);vars=(aa,bb,cc,dd)
qfun=aa*dd-bb*cc
F=qfun**2
gradF=s.Matrix([s.diff(F,t) for t in vars])
hessF=s.hessian(F,vars)
sub=dict(zip(vars,list(v)))
bvec=s.Matrix([avg(t.subs(sub, simultaneous=True)) for t in gradF])
H=s.Matrix(4,4,lambda i,j:avg(hessF[i,j].subs(sub, simultaneous=True)))
c=avg(q**2)

C_expected=s.Matrix([[s.Rational(1,4)+e**2/8,0,0,-s.Rational(1,4)],
                      [0,s.Rational(1,4)+e**4/2,-s.Rational(1,4),0],
                      [0,-s.Rational(1,4),s.Rational(1,4)+e**4/2,0],
                      [-s.Rational(1,4),0,0,s.Rational(1,4)+e**2/8]])
b_expected=s.Matrix([e/4+e**4/2,0,0,e/4-e**4/2])
c_expected=s.Rational(1,4)+e**2/32+9*e**4/64+e**8/4
K=s.hessian(qfun,vars)
assert_matrix_zero(C-C_expected)
assert_matrix_zero(bvec-b_expected)
assert_zero(c-c_expected)
assert_matrix_zero(H-2*K*C*K)
assert s.factor(C.det())==e**6*(e**2+4)*(e**4+1)/256
eigenvalues=[e**2/8,s.Rational(1,2)+e**2/8,e**4/2,s.Rational(1,2)+e**4/2]
lam_eig=s.symbols("lambda")
assert_zero(C.charpoly(lam_eig).as_expr()-s.prod(lam_eig-z for z in eigenvalues))
assert C.subs(e,0).rank()==2

# Exact minimization, not only a trial-background upper bound.
minimum=s.factor(c-(bvec.T*H.inv()*bvec)[0]/2)
minimum_expected=e**2/32+9*e**4/64+e**10/(4*(e**2+4))
assert_zero(minimum-minimum_expected)
Bstar=(-H.inv()*bvec).applyfunc(s.factor)
B_expected=s.Matrix([-1/e-2*e**4/(e**2+4),0,0,-1/e+2*e**4/(e**2+4)])
assert_matrix_zero(Bstar-B_expected)
assert s.limit(minimum,e,0,dir="+")==0
assert all(s.limit(s.Abs(z),e,0,dir="+")==s.oo for z in (Bstar[0],Bstar[3]))
assert H.subs(e,0).rank()==2 and bvec.subs(e,0)==s.zeros(4,1) and c.subs(e,0)==s.Rational(1,4)

# Verify the displayed test gap independently using B=-I/eps.
Bmat=-s.eye(2)/e
test_gap=s.factor(avg((Bmat+X).det()**2)-e**-4)
test_expected=e**2/32+9*e**4/64+e**8/4
assert_zero(test_gap-test_expected)
assert s.factor(minimum-test_gap)==-e**8/(e**2+4)

# Check strict ROC compactification constants for N(A)=|A|^4.
vsyms=s.symbols("x0:4",real=True)
N=sum(t*t for t in vsyms)**2
HN=s.hessian(N,vsyms)
assert HN==8*s.Matrix(vsyms)*s.Matrix(vsyms).T+4*sum(t*t for t in vsyms)*s.eye(4)
# The expected lower bound is 4*m2*I after averaging; the omitted 8C term is PSD.

# Residual bridge on a common range: verify the identity exactly in a symbolic
# diagonal model. The report supplies the general inverse-order argument.
h1,h2,c1,c2,b1,b2,v1,v2,v3=s.symbols("h1 h2 c1 c2 b1 b2 v1 v2 v3",positive=True)
HD=s.diag(h1,h2,0); CD=s.diag(c1,c2,0)
BD=s.Matrix([b1,b2,0]); VD=s.Matrix([v1,v2,v3]); RD=BD-HD*VD
HDdag=s.diag(1/h1,1/h2,0); CDdag=s.diag(1/c1,1/c2,0)
bridge=(BD.T*HDdag*BD)[0]-(2*(BD.T*VD)[0]-(VD.T*HD*VD)[0]+(RD.T*HDdag*RD)[0])
assert_zero(bridge)
inverse_order=(RD.T*(CDdag-HDdag)*RD)[0]
order_expected=RD[0]**2*(h1-c1)/(h1*c1)+RD[1]**2*(h2-c2)/(h2*c2)
assert_zero(inverse_order-order_expected)
assert HD*HDdag*BD==BD  # b lies in the shared range.
assert HD*HDdag*s.Matrix([b1,b2,1])!=s.Matrix([b1,b2,1])  # reject a nullspace load.

# Verify the worker's stated rare/common law, moment identity, and simple bound.
r,w,vv,ss=s.symbols("r w v s",real=True)
qabs=w**2+2*r*vv-ss**2
Pabs=vv**2+ss**2
Cabs=r*w**2
p=e**4
rare=(1/e,1/e,0,0)
vcommon=-e**2/(2*(1-p))
common=(1,0,vcommon,0)
def eval_poly(poly,point):
    return s.expand(poly.subs(dict(zip((r,w,vv,ss),point)),simultaneous=True))
Eq=s.factor(p*eval_poly(qabs,rare)+(1-p)*eval_poly(qabs,common))
delta=s.factor(p*eval_poly(Pabs,rare)+(1-p)*eval_poly(Pabs,common))
Ec=s.factor(p*eval_poly(Cabs,rare)+(1-p)*eval_poly(Cabs,common))
M4=s.factor(p*sum(t*t for t in rare)**2+(1-p)*sum(t*t for t in common)**2)
bracket=-1+1/(2*(1-p))+p/(16*(1-p)**3)
assert_zero(Eq)
assert_zero(delta-e**4/(4*(1-e**4)))
assert_zero(Ec-e)
assert_zero(M4-5-p*bracket)
assert s.Rational(8,15)+s.Rational(16,3375)==s.Rational(1816,3375)<1
pt=s.symbols("p",real=True)
f1=1/(2*(1-pt)); f2=pt/(16*(1-pt)**3)
assert_zero(s.diff(f1,pt)-1/(2*(1-pt)**2))
assert_zero(s.diff(f2,pt)-(1+2*pt)/(16*(1-pt)**4))
assert_zero(f1.subs(pt,s.Rational(1,16))-s.Rational(8,15))
assert_zero(f2.subs(pt,s.Rational(1,16))-s.Rational(16,3375))
assert_zero(Ec**4/delta-4*(1-e**4))
assert_zero(M4-5-p*bracket)

# Quartic-integrability identity required by Q_A=D C_A[A]. The worker's
# proposed C_A is not compatible with its displayed Q_A=P+lambda*q.
ar,aw,av,ass=s.symbols("A_r A_w A_v A_s",real=True)
directional=s.diff(Cabs,r)*ar+s.diff(Cabs,w)*aw+s.diff(Cabs,vv)*av+s.diff(Cabs,ss)*ass
lam=s.symbols("lam",real=True)
post=Pabs+lam*qabs
assert s.Poly(s.expand(directional-post),r,w,vv,ss).coeff_monomial(vv**2)==-1

results={
 "status":"PASS",
 "independent_method":"direct exact sine/cosine moments; no producer script imported or executed",
 "full_path_covariance":str(C),
 "full_path_b":list(map(str,bvec)),
 "full_path_c":str(c),
 "full_path_H_det":str(s.factor(H.det())),
 "full_path_C_eigenvalues":list(map(str,eigenvalues)),
 "exact_optimized_minimum":str(minimum),
 "exact_optimizer":list(map(str,Bstar)),
 "trial_gap":str(test_gap),
 "min_gap_minus_trial_gap":str(s.factor(minimum-test_gap)),
 "singular_limit_minimum":"1/4",
 "smallest_C_eigenvalue_for_0_lt_eps_le_1_over_2":"eps^4/2; globally min(eps^2/8,eps^4/2)",
 "strict_ROC_compactification":"D^2|A|^4=8 vec(A)vec(A)^T+4|A|^2 I, so H_F>=4 delta m2 I",
 "residual_bridge":"exact symbolic common-range check; general inverse order requires 0<C<=H and ker(C)=ker(H)",
 "worker_m4_excess_identity":"p*(-1+1/(2*(1-p))+p/(16*(1-p)^3))",
 "uniform_bracket_upper_bound":"-1559/3375 < 0",
 "worker_exponent_ratio":"4(1-eps^4) -> 4",
 "worker_model_quartic_integrability":"FAIL: D C_A[A] cannot equal P+lambda q; v^2 coefficient mismatch",
 "reduced_sharpness_scope":"The fixed-decomposition law is not quartic-integrable: it cannot establish sharpness under full quartic assumptions. The worker note states this limitation.",
 "scope":"exact root formulas, compactification and conditional quantitative algebra checked independently; not a global near-face theorem or full-cone quasiconvexity result"
}
(OUT/"DELTA_INDEPENDENT_CHECKS.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
