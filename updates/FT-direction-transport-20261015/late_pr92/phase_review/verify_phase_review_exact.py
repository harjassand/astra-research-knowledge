#!/usr/bin/env python3
"""Exact algebra diagnostics for the scoped PR92 review, not its analytic proof."""
from pathlib import Path
from fractions import Fraction as F
import json
import sympy as s

checks=[]
def record(name,detail):
    checks.append({'name':name,'status':'PASS','detail':detail})

h,d=s.symbols('h d',real=True)
D=s.sin(d)+s.sin(h-d)
# Chord real and imaginary numerators at the base phase0. The imaginary
# identity has either sign because both terms change sign together.
assert s.trigsimp(s.expand_trig(s.sin(h-d)+s.sin(d)*s.cos(h)-s.sin(h)*s.cos(d)))==0
assert s.trigsimp(s.expand_trig(D-2*s.sin(h/2)*s.cos(d-h/2)))==0
assert s.trigsimp(s.expand_trig(s.cos(d-h/2)-s.cos(h/2)-2*s.sin(d/2)*s.sin((h-d)/2)))==0
record('exact chord and radial loss identities','Three symbolic identities; geometric interval inequalities are proved in the review.')

# Exact rational state propagation on N4, with both shift orientations.
for direction in (1,-1):
    n,p,t=4,1,F(1,7)
    mu=[F(1),F(0),F(0),F(0)]
    read=[F(1),F(1,2),F(0),F(1,2)]
    lam=(1-s.Rational(t.numerator,t.denominator))*s.I+s.Rational(t.numerator,t.denominator)*s.I**(p+direction)
    for k in range(13):
        assert sum(mu)==1 and all(v>=0 for v in mu)
        out=sum(v*f for v,f in zip(mu,read))
        expected=s.simplify((1+s.re(s.expand_complex(lam**k)))/2)
        assert s.Rational(out.numerator,out.denominator)==expected
        nxt=[F(0)]*n
        for j,w in enumerate(mu):
            nxt[(j+p)%n]+=w*(1-t)
            nxt[(j+p+direction)%n]+=w*t
        mu=nxt
record('row-shift orientation','26 exact rational readouts match the first-character formula for both neighboring shifts; not an irrational-phase error test.')

x,y,A,B=s.symbols('x y A B',real=True)
# q(z)=A+iB; its real part and Re[zq(z)] have full rank if Imz !=0.
M=s.Matrix([[1,0],[x,-y]])
assert M.det()==-y
assert M*s.Matrix([A,B])==s.Matrix([A,x*A-y*B])
record('zero-error two-recurrence elimination','The determinant is -Im(z), nonzero for the specified irrational phase.')

z=s.symbols('z',nonzero=True)
k=s.symbols('k',integer=True,nonnegative=True)
assert s.simplify(z**(-k)*(z**k+z**(-k))/2-(1+z**(-2*k))/2)==0
nn,kap=s.symbols('n kappa',positive=True)
assert s.simplify(16*nn/(4*kap/nn)**2-nn**3/kap**2)==0
record('Fourier normalization constants','Centered probability factor2 and16/(4^2) normalization reproduce n^3/kappa^2.')

pp,qq=s.symbols('p q',real=True,nonzero=True)
alpha=(s.sqrt(5)-1)/2
beta=-(s.sqrt(5)+1)/2
assert s.expand((pp/qq-alpha)*(pp/qq-beta)-(pp**2+pp*qq-qq**2)/qq**2)==0
record('golden Diophantine factorization','Exact conjugate-root identity; nearest-integer interval bound is analytic.')

out={'status':'EXACT_PASS','groups':len(checks),'checks':checks,'scope':'Finite symbolic/rational diagnostics only; not an all-parameter proof, external certification or novelty assessment.'}
Path(__file__).with_name('PHASE_REVIEW_EXACT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
