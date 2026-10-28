"""Exact off-graph slice of the finite moment lift, no SDP accuracy premise."""
from fractions import Fraction as F
from pathlib import Path
import math,json,time
OUT=Path(__file__).resolve().parent
p0=F(55220381,10**10);p2=F(114430029,625000000)
p3=-F(801761987,5000000000);ell=F(118849817,4000000000)
ky=p0/2+(p2+p3)/4;c0=2*p0+p2
assert p0>0 and ky>0 and p0*c0-ell*ell/4>0
coefficient=c0-ell*ell/(4*p0);S=1<<100
def sqrt_interval(q):
    assert q>=0
    k=math.isqrt(q.numerator*S*S//q.denominator)
    return F(k,S),F(k+1,S)
def solve(s,eps):
    assert s>0 and eps>0
    low=-ell*s/(2*p0);high=F(0);steps=0
    for _ in range(80):
        mid=(low+high)/2;sl,sh=sqrt_interval(mid*mid+4*s*s)
        dl=2*p0*mid+ell*s+eps*mid/sl;dh=2*p0*mid+ell*s+eps*mid/sh
        assert dl<=dh
        if dh<0:low=mid
        elif dl>0:high=mid
        else:break
        steps+=1
    def quad(x):return p0*x*x+ell*s*x+c0*s*s
    # Quadratic increases and norm decreases on this root bracket.
    nl,_=sqrt_interval(high*high+4*s*s);_,nh=sqrt_interval(low*low+4*s*s)
    lower=quad(low)+eps*nl;upper=quad(high)+eps*nh
    assert lower<=upper
    return {'s':str(s),'epsilon':str(eps),'root_lower':str(low),'root_upper':str(high),
            'value_lower':str(lower),'value_upper':str(upper),'bisection_steps':steps,
            'display_only_value':float((lower+upper)/2),'display_only_width':float(upper-lower)}
start=time.monotonic()
rows=[solve(s,F(1,100)) for s in [F(1,100),F(1,10),F(1),F(10)]]
result={'status':'EXACT_OFF_GRAPH_SLICE_OPERATION','model':'degree2-moment convex representative of accepted F+epsilon norm^2 at B=0',
        'Hopf_quadratic_positive_determinant':str(p0*c0-ell*ell/4),'Hopf_y_coefficient':str(ky),
        'epsilon0_slice_coefficient':str(coefficient),'epsilon0_formula':'g_F(0,s)=coefficient*s^2',
        'positive_epsilon_formula':'min_x p0*x^2+L*s*x+c0*s^2+epsilon*sqrt(x^2+4*s^2)',
        'rows':rows,'seconds':time.monotonic()-start,
        'scope':'Exact slice. Full five-minor SDP is separate; maximal lift nonsmooth vertically at zero for epsilon>0.'}
(OUT/'SLICE_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'rows':[{k:r[k] for k in ['s','display_only_value','display_only_width']} for r in rows],'seconds':result['seconds']},indent=2))
