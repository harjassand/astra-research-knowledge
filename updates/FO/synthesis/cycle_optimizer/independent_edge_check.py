#!/usr/bin/env python3
"""Independent edge-action reconstruction from the source's closed formulas."""
from fractions import Fraction as Q
import json
from pathlib import Path
import sympy as S
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'incoming_resonant'))
from search_exact_cycles import energy
from profile_algebra import edge_coeffs,edge_value

t=S.symbols('t',real=True)
def direct(n,m,start,end,tau,lam=Q(11,100)):
    r0,s0=map(S.Rational,start); r1,s1=map(S.Rational,end); h=S.Rational(tau)
    dr,ds=r1-r0,s1-s0
    rr=r0+t*dr; ss=s0+t*ds; p1=dr/h; p2=ds/h
    u2=p1**4+p2**4+4*p1**2*p2**2
    v2=n**4*rr**4+m**4*ss**4+4*n**2*m**2*rr**2*ss**2
    uv=(p1**2+p2**2)*(n**2*rr**2+m**2*ss**2)+2*n*m*rr*ss*p1*p2
    w2=(n*rr*p2-m*ss*p1)**2/S.Integer(2)
    qu=n*rr*p1**3+m*ss*p2**3+2*m*ss*p1**2*p2+2*n*rr*p1*p2**2
    qv=n**3*rr**3*p1+m**3*ss**3*p2+2*m*n**2*rr**2*ss*p2+2*n*m**2*ss**2*rr*p1
    avg=u2+v2+(S.Rational(7,2)-S.Rational(lam))*uv+(S.Rational(1,2)+S.Rational(lam))*w2-S.Rational(29,10)*(qu+qv)
    return S.factor(h*S.integrate(avg,(t,0,1)))

lam=Q(11,100)
cases=[
    (1,-1,(Q(1),Q(2)),(Q(2),Q(1)),Q(1,2)),
    (1,-1,(Q(1),Q(2)),(Q(2),Q(1)),Q(4,7)),
    (1,3,(Q(3,2),Q(3,4)),(Q(2),Q(2)),Q(1,4)),
    (1,-3,(Q(3,2),Q(2)),(Q(2),Q(3,4)),Q(1,4)),
    (3,-1,(Q(3,4),Q(2)),(Q(2),Q(3,2)),Q(1,4)),
    (1,5,(Q(7,4),Q(1)),(Q(2),Q(2)),Q(1,8)),
]
records=[]
for n,m,start,end,h in cases:
    expected=direct(n,m,start,end,h,lam)
    poly,_=energy(n,m,lam)
    helper=edge_value(edge_coeffs(__import__('profile_algebra').poly_terms(poly),start,end),h)
    assert expected==S.Rational(helper.numerator,helper.denominator)
    records.append({'carriers':[n,m],'from':list(map(str,start)),'to':list(map(str,end)),
                    'width':str(h),'direct_formula_action':str(expected),'Laurent_action':str(helper),'match':True})
out={'status':'EXACT PASS','determinant_subtraction':str(lam),'cases':records,
     'independent_formula':'Section 7.3 invariant average identities; direct exact integration in normalized strip coordinate'}
(ROOT/'edge_formula_crosscheck.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
