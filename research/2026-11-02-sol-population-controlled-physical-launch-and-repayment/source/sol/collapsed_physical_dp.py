#!/usr/bin/env python3
"""Actual-feedback finite-horizon DP after complete conservative-core episodes.

Each Green solve retains the physical entry coordinate. Successor coordinates
are mapped exactly; no stationary or fixed landing profile is inserted.
Only the finite diagnostic energy arithmetic uses mpmath.
"""
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path
import json
import mpmath as mp
from conservative_fiber_kernel import canonical,bounds,shift,raw_network,falling,factorial_ratio,mv,W

mp.mp.dps=80
P=Path(__file__).resolve().parent
class Budget(Exception):pass

def run(root,mark,max_h=8,fiber_budget=3000,phase_budget=201):
    raw=raw_network();root,mark=tuple(root),tuple(mark)
    base=canonical(tuple(a-b for a,b in zip(root,mark)));H=1+sum(mp.loggamma(a+1) for a in base);scale=2*H
    stats={'physical_fibers':0,'green_value_vectors':0,'largest_fiber':0,'source_receiver_evaluations':0}
    @lru_cache(None)
    def geometry(key):
        stats['physical_fibers']+=1
        if stats['physical_fibers']>fiber_budget:raise Budget('physical fiber budget')
        lo,hi=bounds(key);states=[shift(key,k) for k in range(lo,hi+1)];n=len(states)
        stats['largest_fiber']=max(stats['largest_fiber'],n)
        if n>phase_budget:raise Budget('finite physical phase budget')
        forward=[raw[8][2]*falling(x,raw[8][0]) for x in states];back=[raw[9][2]*falling(x,raw[9][0]) for x in states]
        hazards=[[k*falling(x,s) for s,u,k in raw[:8]] for x in states]
        diag=[f+b+sum(h) for f,b,h in zip(forward,back,hazards)]
        lower=[F(0)]+[-back[i] for i in range(1,n)];upper=[-forward[i] for i in range(n-1)]+[F(0)]
        cp=[F(0)]*n;inv=[F(0)]*n
        for i in range(n):
            pivot=diag[i]-(lower[i]*cp[i-1] if i else 0);assert pivot>0
            inv[i]=1/pivot;cp[i]=upper[i]/pivot if i+1<n else F(0)
        return lo,states,hazards,[mv(a) for a in lower],[mv(a) for a in cp],[mv(a) for a in inv]
    def position(x,key,lo):
        k=(key[1]-x[1])//2
        assert shift(key,k)==tuple(x)
        return k-lo
    @lru_cache(None)
    def energy(key,t):
        stats['source_receiver_evaluations']+=1
        lo,states,hh,ll,cp,inv=geometry(key)
        x=next(x for x in states if all(a>=b for a,b in zip(x,t)))
        opt=canonical(tuple(a-b for a,b in zip(x,t)));delta=mp.log(mv(factorial_ratio(opt,base)))
        return delta+delta*delta/scale
    @lru_cache(None)
    def cont(key,h):
        assert h>=1
        stats['green_value_vectors']+=1
        lo,states,hazards,lower,cp,inv=geometry(key);n=len(states)
        rhs=[1/scale for _ in states]
        for r,(s,u,kappa) in enumerate(raw[:8]):
            active=[i for i in range(n) if hazards[i][r]]
            if not active:continue
            first=states[active[0]];after=tuple(a-b+c for a,b,c in zip(first,s,u));nextkey=canonical(after)
            now=energy(nextkey,tuple(u));future=cont(nextkey,h-1) if h>1 else None
            nextlo=geometry(nextkey)[0]
            for i in active:
                after=tuple(a-b+c for a,b,c in zip(states[i],s,u))
                idx=position(after,nextkey,nextlo)
                value=now if future is None else min(now,future[idx])
                rhs[i]+=mv(hazards[i][r])*value
        dp=[mp.mpf(0)]*n
        for i in range(n):dp[i]=(rhs[i]-(lower[i]*dp[i-1] if i else 0))*inv[i]
        answer=[mp.mpf(0)]*n
        for i in reversed(range(n)):answer[i]=dp[i]-(cp[i]*answer[i+1] if i+1<n else 0)
        return tuple(answer)
    key=canonical(root);lo=geometry(key)[0];idx=position(root,key,lo);rows=[]
    try:
        for h in range(1,max_h+1):
            value=cont(key,h)[idx];rows.append({'macro_horizon':h,'physical_time_plus_coarse_power_change_over_2V':mp.nstr(value,35)})
        status='FINITE_ACTUAL_FEEDBACK_DIAGNOSTIC_COMPLETED'
    except Budget as e:status='REFUSED_BUDGET: '+str(e)
    return {'status':status,'input':root,'mark':mark,'rows':rows,'costs':stats,
            'scope':'Complete finite-fiber physical Green operations, actual successor coordinate retained; floating energy/DP diagnostic only, no global or asymptotic recurrence theorem.'}

if __name__=='__main__':
    (P/'results').mkdir(exist_ok=True);out=[]
    for n in [5,10,20]:
        root=(0,n,n,0,n,n);r=run(root,(0,0,0,0,0,0),max_h=8)
        out.append(r);print(json.dumps(r),flush=True)
        (P/'results/collapsed_physical_dp.json').write_text(json.dumps(out,indent=2)+'\n')
