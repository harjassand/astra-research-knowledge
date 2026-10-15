#!/usr/bin/env python3
"""Exact local derivative certificate for an ordinary-polyconvexity obstruction.

The convex-analysis implication, including arbitrary convex lifts, is written
in EXACT_NONPOLYCONVEX_COMPLETION.md. No producer code or certificate is read.
"""
import json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
a,b,c,d,alpha,r,minor_slope,scale,t=s.symbols('a b c d alpha r minor_slope scale t',real=True)
x=s.Matrix([a,b,c,d])
u=a*a+c*c;j=a*d-b*c;H=((a-d)**2+(b+c)**2)**2
P=alpha*H+r*(r-1)*u*u/6+j*j+r*u*j
I={a:1,b:0,c:0,d:1}
checks=[]
def check(label,value,**fields):
    assert bool(value),label
    checks.append(dict(label=label,status='EXACT_PASS',**fields))
    print('PASS:',label)
def zero(M):return all(s.cancel(v)==0 for v in M)
for degree in range(4):
    from itertools import combinations_with_replacement
    for inds in combinations_with_replacement(range(4),degree):
        der=H
        for i in inds:der=s.diff(der,x[i])
        check('H Taylor derivative '+str(inds),der.subs(I)==0)
G=P-minor_slope*j
check('zero e12 pure Hessian',s.diff(G,b,2).subs(I)==0)
check('e12-e21 row forces minor slope',s.diff(G,b,c).subs(I)==minor_slope-r-2)
G=G.subs(minor_slope,r+2)
V=s.Matrix([1,0,0,-r-1])
check('lifted Hessian annihilates V for every alpha',zero(s.hessian(G,x).subs(I)*V))
curve={a:1+t,b:0,c:0,d:1-(r+1)*t}
grad=s.Matrix([s.diff(G,xi).subs(I) for xi in x])
gap=s.expand(G.subs(curve)-G.subs(I)-t*grad.dot(V))
check('constant linear quadratic terms vanish',all(gap.coeff(t,k)==0 for k in range(3)))
check('unavoidable cubic',s.factor(gap.coeff(t,3))==-r*(r+2)/3,cubic=str(s.factor(gap.coeff(t,3))))
check('exact quartic remainder',s.factor(gap.coeff(t,4)-alpha*(r+2)**4-(r+2)*(r+3)/6)==0)
check('finite alpha enters only quartic here',s.factor(s.diff(gap,alpha))==(r+2)**4*t**4)
scaled=scale*P
scaled_lift=scaled-scale*(r+2)*j
scaled_gap=s.expand(scaled_lift.subs(curve)-scaled_lift.subs(I)-t*s.Matrix([s.diff(scaled_lift,xi).subs(I) for xi in x]).dot(V))
check('scaled boundary cubic',s.factor(scaled_gap.coeff(t,3))==-scale*r*(r+2)/3)
beta,gamma,delta=s.symbols('beta gamma delta',real=True)
boundary_beta=delta*(delta-gamma)/(6*gamma)
F=alpha*H+boundary_beta*u*u+gamma*j*j+delta*u*j
check('every nonzero rank-one first-LMI boundary scales to curved family',s.cancel(F-gamma*P.subs(alpha,alpha/gamma).subs(r,delta/gamma))==0)
receipt=dict(schema='astra-no-finite-H-polyconvex-completion-v1',status='EXACT_DERIVATIVE_PASS',checks=checks,ordinary_polyconvexity=True,excluded_lifts='Every ordinary finite convex lift in (A,det A), including nonsmooth and nonpolynomial lifts.',parameter_scope='r(r+2)>0; arbitrary finite real alpha. Scaled form gamma>0. Projected nonzero rank-one first-LMI boundary has no finite-H polyconvex completion.',flat_extension='Any everywhere-finite correction C3 near I with zero Taylor jet through degree 3 at I leaves the obstruction. D2=D3=0 also suffices after removing affine terms.',scope='Exact derivatives plus the explicit convex-support proof; internal reconstruction, not external verification or formal proof-assistant verification.')
(HERE/'NONPOLYCONVEX_COMPLETION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('EXACT_DERIVATIVE_PASS')
