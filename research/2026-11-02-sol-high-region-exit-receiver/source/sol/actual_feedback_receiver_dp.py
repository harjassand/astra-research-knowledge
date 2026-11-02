#!/usr/bin/env python3
"""Actual first-noncore feedback with a physical global receiving quantity.

No stationary reset: the complete conservative Green operator retains each
actual successor location. Finite diagnostics only, never a global proof.
"""
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path
import sys,json
import mpmath as mp

P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'astra-sol-subgeometric-synthesis-20261102'))
from conservative_fiber_kernel import canonical,bounds,shift,raw_network,falling,mv

mp.mp.dps=80
class Budget(Exception):pass

def coordinates(x):
    a,b,c,d,e,f=x
    m=lambda n:(0,2,4)[n] if n<3 else 7
    return 15+sum(x)-m(a)-m(d),b-c-int(a==1),e-f-int(d==1)

def run(root,lam=F(3),max_h=8,fiber_budget=5000,phase_budget=151,receiver_scale=F(1)):
    raw=raw_network();root=tuple(root);z0,r0,s0=coordinates(root);scale=2*z0
    stats={'physical_fibers':0,'green_value_vectors':0,'largest_fiber':0,'receiving_evaluations':0}
    @lru_cache(None)
    def geometry(key):
        stats['physical_fibers']+=1
        if stats['physical_fibers']>fiber_budget:raise Budget('physical fiber budget')
        lo,hi=bounds(key);states=[shift(key,k) for k in range(lo,hi+1)];n=len(states)
        stats['largest_fiber']=max(stats['largest_fiber'],n)
        if n>phase_budget:raise Budget('finite physical phase budget')
        forward=[raw[8][2]*falling(x,raw[8][0]) for x in states]
        back=[raw[9][2]*falling(x,raw[9][0]) for x in states]
        hazards=[[k*falling(x,s) for s,u,k in raw[:8]] for x in states]
        diag=[f+b+sum(h) for f,b,h in zip(forward,back,hazards)]
        lower=[F(0)]+[-back[i] for i in range(1,n)]
        upper=[-forward[i] for i in range(n-1)]+[F(0)]
        cp=[F(0)]*n;inv=[F(0)]*n
        for i in range(n):
            pivot=diag[i]-(lower[i]*cp[i-1] if i else 0);assert pivot>0
            inv[i]=1/pivot;cp[i]=upper[i]/pivot if i+1<n else F(0)
        return lo,states,hazards,[mv(a) for a in lower],[mv(a) for a in cp],[mv(a) for a in inv]
    def index(x,key,lo):
        k=(key[1]-x[1])//2;assert shift(key,k)==tuple(x)
        return k-lo
    @lru_cache(None)
    def receiving(key):
        stats['receiving_evaluations']+=1
        z,r,s=coordinates(key);dz,dr,ds=z-z0,r-r0,s-s0
        delta=2*z0*dz+dz*dz+lam*(2*r0*dr+dr*dr+2*s0*ds+ds*ds)
        return mv(F(delta,scale))
    @lru_cache(None)
    def continuation(key,h):
        assert h>=1;stats['green_value_vectors']+=1
        lo,states,hazards,lower,cp,inv=geometry(key);n=len(states)
        rhs=[mp.mpf(1)/scale/mv(receiver_scale) for _ in states]
        for r,(source,product,kappa) in enumerate(raw[:8]):
            active=[i for i in range(n) if hazards[i][r]]
            if not active:continue
            after=tuple(a-b+c for a,b,c in zip(states[active[0]],source,product))
            nextkey=canonical(after);now=receiving(nextkey)
            future=continuation(nextkey,h-1) if h>1 else None
            nextlo=geometry(nextkey)[0]
            for i in active:
                after=tuple(a-b+c for a,b,c in zip(states[i],source,product))
                idx=index(after,nextkey,nextlo)
                value=now if future is None else min(now,future[idx])
                rhs[i]+=mv(hazards[i][r])*value
        dp=[mp.mpf(0)]*n
        for i in range(n):dp[i]=(rhs[i]-(lower[i]*dp[i-1] if i else 0))*inv[i]
        answer=[mp.mpf(0)]*n
        for i in reversed(range(n)):answer[i]=dp[i]-(cp[i]*answer[i+1] if i+1<n else 0)
        return tuple(answer)
    rows=[];key=canonical(root)
    try:
        lo=geometry(key)[0];idx=index(root,key,lo)
        for h in range(1,max_h+1):
            v=continuation(key,h)[idx]
            rows.append({'genuine_noncore_horizon':h,'time_plus_receiving_change_over_2Z':mp.nstr(v,30)})
        status='FINITE_ACTUAL_FEEDBACK_DIAGNOSTIC_COMPLETED'
    except Budget as e:status='REFUSED_BUDGET: '+str(e)
    return {'status':status,'input':root,'lambda_exact':str(lam),'receiver_scale_exact':str(receiver_scale),'rows':rows,'costs':stats,
            'scope':'Actual full finite Green feedback, numerical energy/DP only. No global recurrence or asymptotic certificate.'}

if __name__=='__main__':
    (P/'results').mkdir(exist_ok=True)
    n=30
    roots=((0,n,0,0,0,0),(0,0,n,0,0,0),(0,0,0,0,n,n),
           (3,2,2,0,n,0),(3,1,n+2,0,0,0),(3,n,0,0,0,0),
           (4,n,1,0,0,0),(n,0,0,0,0,0),(n,0,0,n,0,0),
           (0,n,0,0,0,n),(0,0,n,0,0,n))
    out=[]
    for root in roots:
        row=run(root,max_h=8);out.append(row)
        negative=next((v['genuine_noncore_horizon'] for v in row['rows'] if mp.mpf(v['time_plus_receiving_change_over_2Z'])<0),None)
        print(json.dumps({'input':root,'status':row['status'],'first_negative':negative,
                          'last_value':row['rows'][-1] if row['rows'] else None,'costs':row['costs']}),flush=True)
        (P/'results/actual_feedback_receiver_dp.json').write_text(json.dumps(out,indent=2)+'\n')
