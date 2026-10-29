#!/usr/bin/env python3
"""Exact population checks, not acquired data or apparatus validation."""
from fractions import Fraction as F
from itertools import combinations
from math import comb, pi, log
from pathlib import Path
import hashlib, json

def rot(x,k):
    k %= len(x)
    return x[k:]+x[:k]

def balanced(n):
    out=[]
    for plus in combinations(range(n),n//2):
        x=[-1]*n
        for j in plus:x[j]=1
        out.append(tuple(x))
    return out

def matching(x,a):
    y=rot(x,1)
    if y[0]==1:return [(F(1),y,1)]
    level=-1
    for j in range(1,len(x)):
        z=rot(y,j); level+=z[0]
        if level==0:return [(1-a,y,1),(a,z,j+1)]
    raise AssertionError('unmatched balanced word')

def thinning(x,a):
    remain=F(1); out=[]
    for j in range(1,len(x)+1):
        y=rot(x,j); accept=(1+a*y[0])/(1+a)
        out.append((remain*accept,y,j)); remain*=1-accept
        if not remain:break
    assert not remain
    return out

def law(states,controller):
    rho={x:F(0) for x in states}; costs={}
    for x in states:
        rows=controller(x)
        assert sum(p for p,y,k in rows)==1
        for p,y,k in rows:
            rho[y]+=p/len(states)
            costs[k]=costs.get(k,F(0))+p/len(states)
    return rho,costs

def tv(p,q):return sum(abs(p[x]-q[x]) for x in p)/2

def check_bound(states,target,rho,costs,a):
    error=tv(rho,target)
    fluctuations=[]
    for n in range(1,len(states[0])+1):
        f=a*sum(abs(sum(x[:n])) for x in states)/len(states)
        assert f/2<=sum(min(k,n)*p for k,p in costs.items())+n*error
        fluctuations.append(f)
    return error,fluctuations

def inverse(a):
    n=len(a); rows=[list(a[i])+[F(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        k=next(k for k in range(j,n) if rows[k][j])
        rows[j],rows[k]=rows[k],rows[j]
        pivot=rows[j][j]; rows[j]=[x/pivot for x in rows[j]]
        for k in range(n):
            if k!=j:
                z=rows[k][j]; rows[k]=[x-z*y for x,y in zip(rows[k],rows[j])]
    return [r[n:] for r in rows]

def pair_failure(a):
    states=[(p,c) for p in (-1,1) for c in (-1,1)]
    accepts=[(1+a*c)/(1+a) for p,c in states]
    q=[[F(0)]*4 for _ in range(4)]
    for i,(p,c) in enumerate(states):
        for b in (-1,1):q[i][states.index((c,b))]+=(1-accepts[i])/2
    resolvent=inverse([[F(i==j)-q[i][j] for j in range(4)] for i in range(4)])
    occupation=[sum(resolvent[i][j] for i in range(4))/4 for j in range(4)]
    rho={states[j]:occupation[j]*accepts[j] for j in range(4)}
    target={(p,c):(1+a*c)/4 for p,c in states}
    assert sum(rho.values())==1 and sum(occupation)==1+a
    assert tv(rho,target)==a/(2*(1+a))
    repaired={(p,c):sum(rho[old,c] for old in (-1,1))/2 for p,c in states}
    assert repaired==target
    return {'a':str(a),'mean_calls':str(sum(occupation)),
            'past_bit_tv':str(tv(rho,target)),'actual_law':{str(k):str(v) for k,v in rho.items()}}

def baker(x):
    u,v=x; b=int(2*u)
    return 2*u-b,(v+b)/2

def baker_inv(x):
    u,v=x; b=int(2*v)
    return (u+b)/2,2*v-b

def main():
    rings=[]; inequalities=0
    for length in (2,4,6,8,10,12):
        states=balanced(length)
        for a in (F(1,2),F(1,3)):
            target={x:(1+a*x[0])/len(states) for x in states}
            rho,costs=law(states,lambda x:matching(x,a))
            cost=sum(k*p for k,p in costs.items())
            m=length//2
            assert rho==target
            assert cost==1+a*(F(4**m,comb(2*m,m))-1)/2
            assert max(costs)<=length
            _,fluct=check_bound(states,target,rho,costs,a)
            raw,rawcosts=law(states,lambda x:thinning(x,a))
            rawerror,_=check_bound(states,target,raw,rawcosts,a)
            def informed(x):
                j=max(range(-2,3),key=lambda j:(sum(rot(x,j)[:length//2]),-abs(j),-j))
                return [(F(1),rot(x,j),abs(j))]
            r,c=law(states,informed); check_bound(states,target,r,c,a)
            inequalities+=3*length
            rings.append({'length':length,'states':len(states),'a':str(a),
                          'exact_mean':str(cost),'cap':max(costs),'full_tv':'0',
                          'first_thinning_full_tv':str(rawerror),
                          'half_block_fluctuation':str(fluct[length//2-1])})
    survival={-1:F(1)}; ballot=[]
    for n in range(15):
        q=F(comb(n,n//2),2**n)
        assert sum(survival.values())==q
        ballot.append(str(q)); nxt={}
        for level,p in survival.items():
            for step in (-1,1):
                if level+step<0:nxt[level+step]=nxt.get(level+step,F(0))+p/2
        survival=nxt
    precision=[]; a=F(1,2)
    for n in (10,100,1000,10000):
        q=F(comb(n,n//2),2**n); summed=(2*n+1)*q-1
        if n<=100:assert summed==sum(F(comb(j,j//2),2**j) for j in range(n))
        eps=a*q/2; cost=1+a*summed/2
        precision.append({'total_cap':n+1,'tv_upper':float(eps),'mean_calls':float(cost),
                          'epsilon_times_mean':float(eps*cost)})
    for u in (F(1,3),F(2,5),F(7,11)):
        for v in (F(1,5),F(3,7),F(5,9)):
            x=u,v
            for _ in range(20):
                assert baker_inv(baker(x))==x and baker(baker_inv(x))==x
                x=baker(x)
    heat=[]
    for eps in (F(1,10),F(1,100),F(1,1000),F(1,1000000)):
        q=eps/2; bound=q/(1-q**3)
        assert bound<eps
        heat.append({'epsilon':str(eps),'tv_bound':float(bound),
                     'Dmin_times_t':log(2/float(eps))/(4*pi*pi)})
    actual={(r,v):F(r==v,2) for r in (0,1) for v in (0,1)}
    ideal={(r,v):F(1,4) for r in (0,1) for v in (0,1)}
    assert tv(actual,ideal)==F(1,2)
    result={'scope':'Exact population checks; no acquired data or apparatus validation',
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'rings':rings,'transport_inequalities':inequalities,'ballot_survival':ballot,
      'matching_precision':precision,'ordinary_thinning_failures':[pair_failure(F(1,2)),pair_failure(F(1,3))],
      'heat_bounds':heat,'retained_noise_record_joint_tv':'1/2','baker_inverse_checks':180,
      'all_assertions_passed':True}
    path=Path(__file__).with_name('PREPARATION_MEMORY_CHECKS.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'ring_cases':len(rings),'transport_inequalities':inequalities,
                      'all_assertions_passed':True,'output':str(path)},indent=2))

if __name__=='__main__':main()
