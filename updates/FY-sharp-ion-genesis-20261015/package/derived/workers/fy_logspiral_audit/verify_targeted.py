#!/usr/bin/env python3
"""Targeted exact identities supporting the independent analytic audit.

No candidate search, numerical optimization, or source script is rerun.
The universal heat identity and limiting arguments remain analytic inputs.
"""
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parent
checks=[]


def check(name,value):
    assert sp.factor(value)==0, (name,sp.factor(value))
    checks.append(name)


r=sp.symbols('r',real=True)
alpha=3*r/(8*(r+2));beta=r*(r-1)/6;C=r*(r+2)/3
a,b,c,d,tau,p,w,z=sp.symbols('a b c d tau p w z',real=True)
u=a*a+c*c;j=a*d-b*c
J=alpha*((a-d)**2+(b+c)**2)**2+beta*u*u+j*j+r*u*j
inc={a:1+tau*p,b:tau*b,c:tau*w,d:1+tau*z}
exp=sp.Poly(sp.expand(J.subs(inc,simultaneous=True)),tau)
e=(r+1)*p+z
check('contact quadratic coefficient',exp.coeff_monomial(tau**2)
      -(e*e+C*w*w+(r+2)*(p*z-b*w)))
cubic=2*p*e*e+(-2*b*w-(r+2)*p*p+r*w*w)*e-C*p*(p*p+w*w)
check('contact cubic coefficient',exp.coeff_monomial(tau**3)-cubic)

eps,P,S,Q=sp.symbols('epsilon P S Q',real=True)
q=sp.Matrix([[eps*P,S],[eps**2*Q,-(r+1)*eps*P]])
X=sp.Matrix([[a,b],[c,d]])
Xq=X+tau*q
poly=sp.Poly(sp.expand(J.subs(dict(zip((a,b,c,d),list(Xq))),simultaneous=True)),tau)
M=poly.coeff_monomial(tau**2)
L=poly.coeff_monomial(tau**3)
K=poly.coeff_monomial(tau**4)
II={a:1,b:0,c:0,d:1}
mP2,mS2,mQ2,mPS,mPQ=sp.symbols('mP2 mS2 mQ2 mPS mPQ',real=True)
mom={(2,0,0):mP2,(0,2,0):mS2,(0,0,2):mQ2,
     (1,1,0):mPS,(1,0,1):mPQ,(0,1,1):-(r+1)*mP2}


def average_quadratic(v):
    terms=sp.Poly(sp.expand(v),P,S,Q).terms()
    return sp.factor(sum(coeff*mom[monomial] for monomial,coeff in terms if coeff!=0))


check('slow-fast I quadratic moment',average_quadratic(M.subs(II))-C*eps**4*mQ2)
cross_diag=(sp.diff(M,a)-sp.diff(M,d)).subs(II)/2
cross_b=sp.diff(M,b).subs(II)/2
cross_c=sp.diff(M,c).subs(II)/2
check('slow-fast I tracefree diagonal block',average_quadratic(cross_diag)
      -(-r*eps**2*mP2+r*(r-1)*eps**4*mQ2/3))
check('slow-fast I e12 block',average_quadratic(cross_b))
check('slow-fast I e21 block',average_quadratic(cross_c)+C*eps**3*mPQ)
check('slow-fast I cubic coefficient',L.subs(II)+C*eps**3*(P**3+eps**2*P*Q**2))
check('limiting full affine quadratic',M.subs(eps,0)
      -S*S*(2*alpha*(a-d)**2+6*alpha*(b+c)**2+c*c))
check('limiting full affine cubic',L.subs(eps,0)-4*alpha*(b+c)*S**3)
check('limiting soft shear quartic',K.subs(eps,0)-alpha*S**4)

# Acoustic determinant gives the fixed Fourier mode's epsilon^4 bound.
pp,qq=sp.symbols('pp qq',real=True)
acoustic=(pp*pp*sp.diff(J,a,2)+2*pp*qq*sp.diff(J,a,b)+qq*qq*sp.diff(J,b,2))/2
acoustic_matrix=sp.hessian(acoustic,(a,b,c,d))/2
check('full acoustic determinant',acoustic_matrix.det()-9*pp**4*qq**4*r**4/16)

# Radial second-column derivative for the high-frequency calibration.
al,be,nu,ct,st,sigma=sp.symbols('alpha beta nu cos_theta sin_theta sigma',real=True)
qt=ct-nu*st
rankone_poly=al*(1+nu*nu)**2+be*qt**4
radial_poly=al*(1+nu*nu+tau*tau+2*sigma*tau)**2\
            +be*(tau*tau*st*st+qt*qt)**2+tau*tau\
            -r*sigma*tau*(tau*tau*st*st+qt*qt)
mu=sigma*(4*al*(1+nu*nu)-r*qt*qt)
for sign in (-1,1):
    check('logspiral radial derivative sign '+str(sign),
          (sp.diff(radial_poly,tau).subs(tau,0)-mu).subs(sigma,sign))
check('rank-one-column minimizer equation',sp.diff(rankone_poly,nu)
      -4*(al*nu*(1+nu*nu)-be*st*qt**3))
stationary=al*nu*(1+nu*nu)-be*st*qt**3
partial_theta=-st*sp.diff(stationary,ct)+ct*sp.diff(stationary,st)
den=al*(1+3*nu*nu)+3*be*st*st*qt*qt
numerator=be*qt*qt*(ct*ct-3*st*st-4*nu*st*ct)
check('minimizer derivative denominator',sp.diff(stationary,nu)-den)
check('minimizer derivative numerator',-partial_theta-numerator)

out={'status':'PASS','exact_check_groups':len(checks),'checks':checks,
     'interpretation':'Targeted exact algebra only; written audit supplies compactness, scaling, bounds, and asymptotic reasoning.',
     'candidate_or_numerical_reruns':False,'historical_novelty':'UNKNOWN'}
(ROOT/'TARGETED_EXACT_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','exact_check_groups':len(checks)},indent=2))
