#!/usr/bin/env python3
"""Actual physical killed Green kernel on the nonlinear conservative fiber.

No stationary-fiber substitution. Source receivers are exactly invariant along
the raw lattice; the exit weights/time are acquired from the true killed chain.
Finite kernels do not prove the global coupled recurrence claim.
"""
from fractions import Fraction as F
from math import prod
from pathlib import Path
import mpmath as mp
import json

mp.mp.dps=80
P=Path(__file__).resolve().parent
W=(0,-2,-2,0,2,2)
def ff(a,b):return 0 if a<b else prod(range(a-b+1,a+1))
def falling(x,y):return prod(ff(a,b) for a,b in zip(x,y))
def mv(a):return mp.mpf(a.numerator)/a.denominator if isinstance(a,F) else mp.mpf(a)
def shift(x,k):return tuple(a+k*b for a,b in zip(x,W))
def bounds(x):return -(min(x[4],x[5])//2),min(x[1],x[2])//2
def canonical(x):
    assert min(x)>=0
    lo,hi=bounds(x)
    # H(k+1)-H(k) has the sign of numerator-denominator below.
    a,b=lo,hi
    while a<b:
        k=(a+b)//2;v=shift(x,k)
        numerator=(v[4]+1)*(v[4]+2)*(v[5]+1)*(v[5]+2)
        denominator=v[1]*(v[1]-1)*v[2]*(v[2]-1)
        assert denominator>0
        if numerator>=denominator:b=k
        else:a=k+1
    return shift(x,a)
def factorial_ratio(x,y):
    out=F(1)
    for a,b in zip(x,y):
        if a>b:out*=prod(range(b+1,a+1))
        elif a<b:out/=prod(range(a+1,b+1))
    return out
def raw_network(coupling_forward=F(2)):
    C=[(0,0,0),(1,1,0),(2,1,1),(3,2,2)];raw=[]
    for j,y in enumerate(C):raw.append((y+(0,0,0),C[(j+1)%4]+(0,0,0),F(1)))
    for j,y in enumerate(C):raw.append(((0,0,0)+y,(0,0,0)+C[(j+1)%4],F(1)))
    s=(1,2,2,1,0,0);u=(1,0,0,1,2,2)
    return raw+[(s,u,F(coupling_forward)),(u,s,F(1))]
def tridiagonal(lower,diag,upper,rhs):
    n=len(diag);cp=[F(0)]*n;dp=[F(0)]*n
    for i in range(n):
        pivot=diag[i]-(lower[i]*cp[i-1] if i else 0);assert pivot>0
        cp[i]=upper[i]/pivot if i+1<n else F(0)
        dp[i]=(rhs[i]-(lower[i]*dp[i-1] if i else 0))/pivot
    ans=[F(0)]*n
    for i in reversed(range(n)):ans[i]=dp[i]-(cp[i]*ans[i+1] if i+1<n else 0)
    return ans
def source_phase_interval(x,s):
    if x[0]<s[0] or x[3]<s[3]:return None
    lo,hi=bounds(x)
    lo=max(lo,-((x[4]-s[4])//2),-((x[5]-s[5])//2))
    hi=min(hi,(x[1]-s[1])//2,(x[2]-s[2])//2)
    return (lo,hi) if lo<=hi else None

def acquire(x,t,coupling_forward=F(2),phase_budget=401,save_joint=False):
    x,t=tuple(x),tuple(t);assert min(a-b for a,b in zip(x,t))>=0
    raw=raw_network(coupling_forward);lo,hi=bounds(x);n=hi-lo+1
    if n>phase_budget:return {'status':'REFUSED_BUDGET','physical_fiber_states':n}
    states=[shift(x,k) for k in range(lo,hi+1)];start=-lo
    forward=[raw[8][2]*falling(v,raw[8][0]) for v in states]
    backward=[raw[9][2]*falling(v,raw[9][0]) for v in states]
    hazards=[[k*falling(v,s) for s,u,k in raw[:8]] for v in states]
    killed=[sum(h) for h in hazards];assert min(killed)>=2
    # Solve A^T occupation=e_start, with A=-Q_core+diag(killing).
    diag=[f+b+h for f,b,h in zip(forward,backward,killed)]
    lower=[F(0)]+[-forward[i-1] for i in range(1,n)]
    upper=[-backward[i+1] for i in range(n-1)]+[F(0)]
    rhs=[F(int(i==start)) for i in range(n)]
    occupation=tridiagonal(lower,diag,upper,rhs);assert min(occupation)>=0
    for i in range(n):
        lhs=diag[i]*occupation[i]
        if i:lhs+=lower[i]*occupation[i-1]
        if i+1<n:lhs+=upper[i]*occupation[i+1]
        assert lhs==rhs[i]
    time=sum(occupation);assert time<=F(1,2)
    probabilities=[sum(occupation[i]*hazards[i][j] for i in range(n)) for j in range(8)]
    assert sum(probabilities)==1
    root=canonical(tuple(a-b for a,b in zip(x,t)));H=1+sum(mp.loggamma(a+1) for a in root)
    receivers=[];expected=mp.mpf(0);identity_checks=0
    for j,(s,u,k) in enumerate(raw[:8]):
        interval=source_phase_interval(x,s)
        if interval is None:
            assert probabilities[j]==0;continue
        v=shift(x,interval[0]);res=tuple(a-b for a,b in zip(v,s));opt=canonical(res)
        for i,v in enumerate(states):
            if hazards[i][j]:
                assert canonical(tuple(a-b for a,b in zip(v,s)))==opt;identity_checks+=1
        delta=mp.log(mv(factorial_ratio(opt,root)));change=delta+delta*delta/(2*H)
        expected+=mv(probabilities[j])*change
        receivers.append({'noncore_channel':j,'source':s,'actual_product':u,'probability_exact':str(probabilities[j]),
                          'canonical_residual_receiver':opt,'log_energy_change':mp.nstr(delta,30)})
    core_jumps=sum(o*(f+b) for o,f,b in zip(occupation,forward,backward))
    result={'status':'ACTUAL_FINITE_PHYSICAL_KERNEL_ACQUIRED','input':x,'actual_mark':t,
            'physical_fiber_states':n,'time_exact':str(time),'expected_core_jumps_exact':str(core_jumps),
            'receiving_identity_exact_checks':identity_checks,'source_receivers':receivers,
            'physical_time_plus_power_change_over_2V':mp.nstr(expected+mv(time)/(2*H),35),
            'scope':'Exact finite physical Green/exit law and exact receiving identities; multiprecision energy evaluation is diagnostic, not a global return proof.'}
    if save_joint:
        result['complete_joint_exit_weights']=[{'pre_exit_population':v,'noncore_channel':j,'probability_exact':str(occupation[i]*hazards[i][j]),
                 'actual_output_population':tuple(a-b+c for a,b,c in zip(v,raw[j][0],raw[j][1])),'actual_output_mark':raw[j][1]}
                  for i,v in enumerate(states) for j in range(8) if occupation[i]*hazards[i][j]]
    return result

if __name__=='__main__':
    (P/'results').mkdir(exist_ok=True);rows=[]
    for n in [10,30,100]:
        x=(1,n+1,n,1,n+1,n);t=(0,0,0,1,1,0)
        ans=acquire(x,t,save_joint=(n==10));rows.append(ans)
        print(json.dumps({k:ans[k] for k in ['input','physical_fiber_states','time_exact','expected_core_jumps_exact','physical_time_plus_power_change_over_2V']}),flush=True)
    (P/'results/conservative_fiber_kernel.json').write_text(json.dumps(rows,indent=2)+'\n')
