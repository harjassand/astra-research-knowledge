#!/usr/bin/env python3
"""Exact positive-monomial proof ledger; no floating asymptotics or simulation.

Domain: T>=1 and 1<=r<=sqrt(T). A monomial T^a*r^b is at most
one if a+max(b,0)/2<=0. The printed sums therefore certify the stated
constant envelopes for every point of this domain, not a finite sample.
"""
from fractions import Fraction as F
from pathlib import Path
import json

checks = []
def check(name, condition, detail=None):
    if not condition:
        raise AssertionError((name, detail))
    checks.append({'name': name, 'passed': True, 'detail': detail})

class P:
    def __init__(self, terms=None):
        self.terms = {k:F(v) for k,v in (terms or {}).items() if v}
    def __add__(self, other):
        if not isinstance(other,P): other=mono(other)
        z=dict(self.terms)
        for k,v in other.terms.items(): z[k]=z.get(k,F(0))+v
        return P(z)
    __radd__=__add__
    def __mul__(self, other):
        if not isinstance(other,P): other=mono(other)
        z={}
        for (a,b),c in self.terms.items():
            for (d,e),f in other.terms.items():
                k=(a+d,b+e); z[k]=z.get(k,F(0))+c*f
        return P(z)
    __rmul__=__mul__
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=mono(1)
        for _ in range(n): out=out*self
        return out

def mono(c=1,a=0,b=0): return P({(F(a),F(b)):F(c)})
def div(poly,a=0,b=0): return poly*mono(1,-F(a),-F(b))
def ceiling(poly,a,b,name):
    """Return sum of coefficients after termwise domination by T^a r^b."""
    total=F(0); terms=[]
    for (x,y),c in sorted(poly.terms.items()):
        assert c>=0
        dx=x-F(a);dy=y-F(b)
        exponent=dx+max(dy,F(0))/2
        check(name+' monomial '+str((x,y)),exponent<=0,
              {'coefficient':str(c),'ratio_T_exponent':str(dx),
               'ratio_r_exponent':str(dy),'worst_T_exponent':str(exponent)})
        total+=c
        terms.append({'T':str(x),'r':str(y),'coefficient':str(c)})
    return {'ceiling':str(total),'terms':terms}

T=mono(1,1,0); N=mono(1,5,0); m=mono(1,1,1); w=mono(1,3,F(1,2))
H=mono(10**4,-2,F(1,2)); d=mono(16,1,F(-3,2)); J=m*H
U=d+H+F(5,2)*m*H+2*w*H
W=J+2*w*H
VE=J+4*w*H+8*m*m*d
VL=d+H+4*m*H+2*w*H
Qh=4*w*w*(d+H+6*m*H+4*m*m*d+2*N*H)+16*w*w*J+40*w*w*w*H+128*w*w*m*m*d
Hh=2*w*d+24*m*w*H+9*m*m*H+8*m*m*d+2*w*H*(10*T+2*w+8*m+2)

rate_ledgers={}
for name,p,a,b in [('U',U,1,1),('W',W,1,1),('VE',VE,3,F(1,2)),
                    ('VL',VL,1,1),('Qh',Qh,9,F(3,2))]:
    rate_ledgers[name]=ceiling(p,a,b,name)
    check(name+' C0=1e7',F(rate_ledgers[name]['ceiling'])<=10**7)

# Explicit derivative constants from the independently received cone formulas.
g=F(1,32)
kle=g**-3+F(9,14)*g**-4+F(3,14)*g**-6
kee=F(3,10)*g**-3+(F(3,2)+1/(2*g*g))*kle
D_constants={
 'b_l':3**5/(5*g**3), 'b_e':3**4/(2*g**2),
 'b_ll':3**8/(7*g**4), 'b_le':3**6*kle, 'b_ee':3**5*kee}
D=10**14
for name,v in D_constants.items():check(name+' common D',v<=D,str(v))
check('padded cone g=1/32',F(1,3)>=g*9)
check('m/2-1>=m/3 at m>=100',F(1,2)-F(1,100)>=F(1,3))
check('w/2-1>=w/3 at w>=100',F(1,2)-F(1,100)>=F(1,3))
check('2w+1<=3w at w>=100',2+F(1,100)<=3)
check('clock-tail constant<=200',1/(6*g*g)<=200)

fl=mono(D,0,F(-5,2));fe=mono(D,0,-2)
fll=mono(D,0,F(-7,2));fle=mono(D,0,-3);fee=mono(D,0,F(-5,2))
hplus=3*m*w
R1=div(fl*(1+4*m)*H,1)
R2=div(fe*(J+4*w*H+8*m*H),3)
R3=div(fl*Hh,6)
Taylor=div(fll*U*F(1,2),2)+div(fle*W,4)+div(fee*VE*F(1,2),6)
Product=div(fll*hplus*VL,7)+div(fle*hplus*VE,9)
residual_ledgers={}
residual_total=F(0)
for name,p in [('R1',R1),('R2',R2),('R3',R3),('Product',Product)]:
    residual_ledgers[name]=ceiling(p,-2,-1,name)
    residual_total+=F(residual_ledgers[name]['ceiling'])
residual_ledgers['Taylor']=ceiling(Taylor,-1,F(-5,2),'Taylor')
check('residual lower-order constant<=1e23',residual_total<=10**23,str(residual_total))
check('residual Taylor constant<=1e23',F(residual_ledgers['Taylor']['ceiling'])<=10**23)

a=div(fl,1)+div(hplus*fll,7)
b=div(fe,3)+div(hplus*fle,9)
c=div(fl,6)
V=2*(a*a*U+2*a*b*W+b*b*VE)+2*c*c*Qh
bracket=ceiling(V,-1,-4,'bracket')
check('full corrected bracket constant<=1e40',F(bracket['ceiling'])<=10**40,bracket['ceiling'])
jumps=ceiling(a+b+4*c*w,-1,F(-5,2),'jumps')
check('jump constant<=1e16',F(jumps['ceiling'])<=10**16,jumps['ceiling'])
endpoint=ceiling(div(2*m*w*fl,6),-2,-1,'endpoint')
check('endpoint constant<=1e16',F(endpoint['ceiling'])<=10**16,endpoint['ceiling'])
omission=ceiling(11*m*H,-1,F(3,2),'omission')
check('geometric omission price<4e5',2*F(omission['ceiling'])<400000)
# 2^(-3/2)<1/2, so the increasing geometric sum costs less than 2.
check('geometric increasing ratio proof',F(1,8)<F(1,4))

# Hh is bounded by C0 times the five printed monomials. Each monomial is
# assigned to an exactly matching or domain-dominating base; sums per base
# are explicitly checked, without evaluating T or r numerically.
h_bases=[(F(4),F(-1)),(F(2),F(2)),(F(0),F(5,2)),(F(3),F(1,2)),(F(4),F(3,2))]
h_coeffs=[F(0)]*len(h_bases); h_assignments=[]
for (x,y),coef in Hh.terms.items():
    candidates=[i for i,(a0,b0) in enumerate(h_bases) if x-a0+max(y-b0,F(0))/2<=0]
    check('Hh base exists '+str((x,y)),bool(candidates))
    exact=[i for i in candidates if h_bases[i]==(x,y)]
    i=(exact or candidates)[0]
    h_coeffs[i]+=coef; h_assignments.append({'term':[str(x),str(y)],'coefficient':str(coef),'base':i})
for i,coef in enumerate(h_coeffs):check('Hh base C0 '+str(i),coef<=10**7,str(coef))

out={
 'status':'PASS_EXACT_UNIVERSAL_MONOMIAL_ENVELOPES_NOT_INDEPENDENT_THEOREM_REVIEW',
 'domain':'T>=1, 1<=r<=sqrt(T); stage geometry also uses m,w>=100',
 'checks':len(checks), 'constants':{'D':D,'C0':10**7,'residual':10**23,'bracket':10**40,'jump':10**16},
 'derivative_exact_constants':{k:str(v) for k,v in D_constants.items()},
 'rate_ledgers':rate_ledgers,'residual_ledgers':residual_ledgers,
 'residual_lower_order_coefficient_sum':str(residual_total),
 'bracket':bracket,'jumps':jumps,'endpoint':endpoint,'omission':omission,
 'h_residual_assignments':h_assignments,'h_residual_base_coefficients':list(map(str,h_coeffs)),
 'assertions':checks}
path=Path(__file__).with_name('TAIL_CHECK_RESULTS.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'checks':len(checks),'output':str(path),
                  'residual_lower_order_sum':str(residual_total),
                  'bracket_sum':bracket['ceiling'],'jump_sum':jumps['ceiling']},indent=2))
