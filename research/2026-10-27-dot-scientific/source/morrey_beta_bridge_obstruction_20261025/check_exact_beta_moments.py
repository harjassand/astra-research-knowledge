#!/usr/bin/env python3
"""Exact conditional-beta moments and polyconvex bridge separator; no search."""
import json, time
from functools import lru_cache
from pathlib import Path
import sympy as s
start=time.perf_counter()
u,v,w,t,eta=s.symbols('u v w t eta', real=True)
@lru_cache(None)
def moment(a,b,c):
    out=s.S.Zero
    for ell in range(c//2+1):
        aa=a+c-2*ell; bb=b+c-2*ell
        if aa%2 or bb%2: continue
        ra=aa//2; rb=bb//2
        out += (s.binomial(c,2*ell)*s.rf(eta+s.Rational(1,2),ell)
                *s.rf(s.Rational(1,2),ell)*s.rf(s.Rational(1,2),ra)
                *s.rf(s.Rational(1,2),rb)
                /(s.rf(eta+1,ra+ell)*s.rf(eta+1,rb+ell)))
    return s.factor(out.subs(eta,1/t-1))
def expect(poly):
    return s.factor(sum(c*moment(*p) for p,c in s.Poly(s.expand(poly),u,v,w).terms()))
q=u*v+u*w+v*w; H=q-u-v-w
M=[expect(H**i) for i in range(1,4)]
assert M[0]==0
assert s.factor(M[1]-3*t*(2-t)/4)==0
assert s.factor(M[2]-3*t*t*(4-t*t)/(4*(1+t)**2))==0
assert s.diff(M[1],t).subs(t,1)==0
assert s.diff(M[2],t).subs(t,1)==s.Rational(3,16)
assert moment(2,2,2)==t**3*(4*t+1)/(8*(t+1)**2)
P=18*M[1]-M[2]
gap=s.factor(P.subs(t,1)-P.subs(t,s.Rational(99,100)))
assert gap==-s.Rational(942849,1584040000)
gap_interior=s.factor(P.subs(t,s.Rational(999,1000))-P.subs(t,s.Rational(99,100)))
assert gap_interior==-s.Rational(266178585850551,632982542404000000)
x=s.symbols('x'); psi=18*x*x-x**3; line=108*x-216
assert all(s.diff(psi-line,x,i).subs(x,6)==0 for i in range(3))
assert s.expand(s.diff(psi,x,2)-(36-6*x))==0
mid=8*(x+3)**3-108*(x+3)+180
left=-108*x-144
assert all(s.diff(left-mid,x,i).subs(x,-3)==0 for i in range(3))
assert all(s.diff(mid-psi,x,i).subs(x,-2)==0 for i in range(3))
assert s.expand(s.diff(mid,x,2)-48*(x+3))==0
vertices=[H.subs({u:a,v:b,w:c}) for a in [-1,1] for b in [-1,1] for c in [-1,1]]
assert (min(vertices),max(vertices))==(-2,6)
A=s.Matrix([[u+w,w],[w,v+w]])
h=A.det()-s.trace(A)+(A[0,1]+A[1,0])/2
assert s.expand(h-H)==0
receipt={
 'all_exact_checks_passed':True,
 'EH2':str(M[1]), 'EH3':str(M[2]),
 'endpoint_derivative_EH2':'0','endpoint_derivative_EH3':'3/16',
 'polyconvex_expectation_gap_t_099_to_1':str(gap),
 'polyconvex_expectation_gap_t_099_to_0999':str(gap_interior),
 'scope':'Exact proposed-bridge obstruction only. No full Morrey resolution, no terminal Jensen counterexample.',
 'elapsed_seconds':time.perf_counter()-start,
}
Path(__file__).with_name('exact_beta_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
