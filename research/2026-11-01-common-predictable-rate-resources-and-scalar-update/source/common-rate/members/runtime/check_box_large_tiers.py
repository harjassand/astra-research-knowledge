"""Actual common-multiplier interval drift, maximized over the FULL rate box.
Enormous count states, no enormous q power expansion. Same-author controls only.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json,hashlib
import common_box as C
root=Path(__file__).resolve().parent
p=C.construct(C.fixture());r=p['raw'];fs=C.faces(p);precision=8192
counts={'uniform_full_box_foster':0,'channel_upper_endpoint_terms':0,'channel_lower_endpoint_terms':0,'ambiguous_endpoint_signs':0}
@lru_cache(maxsize=20000)
def zinterval(k):
    # k=resource+M. Small exact powers are charged by BOTH configured budgets.
    try:
        value=(1-C.power(p['q'],-k,max_exponent=20000,max_bits=200000))/k
        return value,value
    except C.BudgetRefusal:
        bits=min(k//p['M'],precision)
        return (1-F(1,1<<bits))/k,F(1,k)
@lru_cache(maxsize=20000)
def h_interval(x):
    N=sum(x);A=x[r['A']];Q=sum(x[u]*x[v] for u,v in r['edges'])
    lo=hi=1-p['e']*A/(N+1)+(p['H'] if A==0 and Q==0 else 0)
    for weights,w in fs:
        k=sum(a*b for a,b in zip(weights,x))+p['M'];l,h=zinterval(k);lo+=w*l;hi+=w*h
    return lo,hi

def box_drift_interval(x):
    xl,xh=h_interval(x);lo=hi=F(0)
    for u,v,kl,kh in r['channels']:
        prop=C.propensity(u,x)
        if not prop:continue
        y=tuple(a-b+c for a,b,c in zip(x,u,v));yl,yh=h_interval(y);tt=p['t']**(sum(v)-sum(u))
        cl=prop*(tt*yl-xh);ch=prop*(tt*yh-xl)
        lo+=max(kl*cl,kh*cl);hi+=max(kl*ch,kh*ch)
        if ch<=0:counts['channel_lower_endpoint_terms']+=1
        elif cl>=0:counts['channel_upper_endpoint_terms']+=1
        else:counts['ambiguous_endpoint_signs']+=1
    return lo,hi
N=p['Nstar']+10;T=p['T'];U=T+2
states=[(0,N,0,0,0,0),(1,N,0,0,0,0),(0,N,0,0,N//10,0),
        (0,N,0,0,N//(10*T),0),(1,N,0,0,N//(10*T),0),
        (0,N,1,0,N//(10*T),0),(0,N,0,0,N//(10*T),1),
        (0,N,N,0,0,0),(N,N,0,0,0,0),(0,N,0,0,U,U),
        (1,N,0,0,T+1,0),(0,N,T,0,T+1,1),
        (0,N,0,0,1,1),(1,N,0,0,1,1)]
for i,x in enumerate(states):
    assert sum(x)>=p['Nstar']
    lo,hi=box_drift_interval(x)
    assert lo<=hi and hi<=-p['nu'],('whole-box Foster failure',i)
    counts['uniform_full_box_foster']+=1
    print('certified worst full box, state',i,'total bits',sum(x).bit_length(),flush=True)
assert counts['channel_lower_endpoint_terms'] and counts['channel_upper_endpoint_terms']
result=dict(status='PASS_AUTHOR_INTERVAL_FULL_BOX_DRIFT_NOT_INDEPENDENT',counts=counts,faces_evaluated=len(fs),channels=len(r['channels']),Nstar_bits=p['Nstar'].bit_length(),precision_bits=precision,
            exponent_budget=20000,power_bit_budget=200000,stationary_fiber_solves=0,
            bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['common_box.py','COMMON_PREDICTABLE_BOX_THEOREM.md','check_box_large_tiers.py']})
(root/'box_large_tier_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
