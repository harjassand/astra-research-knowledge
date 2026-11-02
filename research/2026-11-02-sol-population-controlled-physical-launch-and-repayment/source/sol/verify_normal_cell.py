#!/usr/bin/env python3
"""Exact normal-reference checks; finite floating first-kill diagnostics.

The all-N proof is BALANCED_NORMAL_CELL_PHYSICAL_EPISODE.md. Numerical
first-kill solves do not assert global recurrence or independent audit.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
import numpy as np

P=Path(__file__).resolve().parent
Y=((0,0,0),(1,1,0),(2,1,1),(3,2,2))

def ff(x,s):
    out=1
    for a,b in zip(x,s):
        if a<b:return 0
        for v in range(a-b+1,a+1):out*=v
    return out

def m(a):return (0,2,4)[a] if a<3 else 7
def z(x):return 15+sum(x)-m(x[0])-m(x[3])
def state(base,i,j,k):
    b,c,e,f=base
    return (i,b-2*k+Y[i][1],c-2*k+Y[i][2],
            j,e+2*k+Y[j][1],f+2*k+Y[j][2])

def cell(base,alpha=(1,1,1,1),beta=(1,1,1,1)):
    b,c,e,f=base;N=sum(base)
    keys=[];xs=[]
    for k in range(-((min(e,f)+2)//2),(min(b,c)+2)//2+1):
        for i in range(4):
            for j in range(4):
                x=state(base,i,j,k)
                if min(x)>=0:keys.append((i,j,k));xs.append(x)
    ind={a:t for t,a in enumerate(keys)}
    edges=[[] for _ in keys];kills=[[] for _ in keys];mu=[]
    for a,(key,x) in enumerate(zip(keys,xs)):
        i,j,k=key
        den=alpha[i]*beta[j]
        for v in x:den*=factorial(v)
        mu.append(F(2)**k/den)
        assert z(x)==N+15
        for block,(cur,rates) in enumerate(((i,alpha),(j,beta))):
            off=3*block
            for s in range(4):
                raw=F(rates[s])*ff(x[off:off+3],Y[s])
                if not raw:continue
                out=list(x)
                for q in range(3):out[off+q]+=Y[(s+1)%4][q]-Y[s][q]
                assert min(out)>=0
                if s==cur:
                    target=((i+1)%4,j,k) if block==0 else (i,(j+1)%4,k)
                    bidx=ind[target]
                    assert tuple(out)==xs[bidx] and z(out)==z(x)
                    edges[a].append((bidx,raw,('block',block,s)))
                else:
                    delta=z(out)-z(x)
                    kind='repaying' if delta<0 else 'neutral' if delta==0 else 'harmful'
                    assert (cur,s,delta) in ((1,0,0),(2,0,-1),(2,1,-1),(3,0,2),(3,1,2),(3,2,3))
                    kills[a].append((kind,raw,delta,block,s))
        forward=2*x[0]*x[3]*ff(x[1:3],(2,2))
        backward=x[0]*x[3]*ff(x[4:6],(2,2))
        if forward:edges[a].append((ind[(i,j,k+1)],F(forward),('core',1)))
        if backward:edges[a].append((ind[(i,j,k-1)],F(backward),('core',-1)))
    flux=[F(0) for _ in keys]
    incoming=[[] for _ in keys]
    for a,row in enumerate(edges):
        for bidx,rate,label in row:
            flux[a]-=mu[a]*rate;flux[bidx]+=mu[a]*rate
            incoming[bidx].append((a,mu[a]*rate/mu[bidx],label))
    assert all(v==0 for v in flux)
    # Exact reverse I/II edge rate equals forward outgoing rate at its phase.
    for a,(i,j,k) in enumerate(keys):
        for bidx,rate,label in incoming[a]:
            if label[0]=='block':
                block=label[1];cur=(i,j)[block];rates=(alpha,beta)[block];off=3*block
                assert rate==rates[cur]*ff(xs[a][off:off+3],Y[cur])
            else:
                assert any(v==bidx and r==rate for v,r,_ in edges[a])
    return keys,xs,edges,kills,mu,incoming

def graph_checks():
    checked=0
    phi_b=lambda i,j:-int(i==3)-int(j==3)
    phi_h=lambda i,j:int(i==2)+int(j==2)
    for i in range(4):
        for j in range(4):
            for block,cur in enumerate((i,j)):
                ni,nj=((i+1)%4,j) if block==0 else (i,(j+1)%4)
                assert int(cur==3)-int(cur==2)<=phi_b(ni,nj)-phi_b(i,j)
                assert int(cur==1)-int(cur==2)<=phi_h(ni,nj)-phi_h(i,j)
                checked+=1
    return checked

def probe(n):
    keys,xs,edges,kills,mu,_=cell((n,n,n,n))
    size=len(keys);B=np.eye(size);q=np.zeros(size)
    for a in range(size):
        q[a]=float(sum(r for _,r,_ in edges[a])+sum(r for _,r,*_ in kills[a]))
        for bidx,rate,_ in edges[a]:B[a,bidx]-=float(rate)/q[a]
    roots=[('central',max((a for a,k in enumerate(keys) if k[:2]==(0,0)),key=lambda a:mu[a])),
           ('cold',max((a for a,k in enumerate(keys) if k[:2]==(0,0)),key=lambda a:xs[a][1]))]
    rhs=np.zeros((size,len(roots)))
    for j,(_,root) in enumerate(roots):rhs[root,j]=1
    visits=np.linalg.solve(B.T,rhs)
    residual=float(np.max(np.abs(B.T@visits-rhs)))
    assert residual<1e-6 and np.min(visits)>-1e-6,(n,residual,float(np.min(visits)))
    out=[]
    for col,(name,root) in enumerate(roots):
        occ=visits[:,col]/q;prob={k:0. for k in ('repaying','neutral','harmful')};mean_delta=0.;second=0.
        for a,row in enumerate(kills):
            for kind,rate,delta,*_ in row:
                v=occ[a]*float(rate);prob[kind]+=v;mean_delta+=v*delta;second+=v*delta*delta
        assert abs(sum(prob.values())-1)<1e-6,(n,prob)
        clock=float(np.sum(occ));Z=4*n+15
        out.append({'input':name,'state':xs[root],'cell_states':size,'physical_mean_first_unexpected':clock,
                    'exit_probabilities':prob,'mean_mass_increment':mean_delta,'second_mass_increment':second,
                    'mean_unscaled_quadratic_change':2*Z*mean_delta+second,
                    'occupation_equation_max_abs_residual':residual})
    return out

def main():
    exact=[]
    for base in ((0,0,0,0),(1,1,1,1),(3,2,4,3),(8,8,8,8),(8,6,7,9)):
        for alpha,beta in (((1,1,1,1),(1,1,1,1)),((1,2,3,5),(2,1,4,3))):
            keys,*_=cell(base,alpha,beta)
            exact.append({'base':base,'alpha':alpha,'beta':beta,'states':len(keys)})
    out={'exact_reference_balance_and_reverse_rate_cases':exact,
         'exact_joint_crossing_edges':graph_checks(),
         'finite_float_first_kill_diagnostics':sum((probe(n) for n in (5,10,20)),[]),
         'scope':'Exact identities plus finite numerical diagnostics. The all-N episode proof is separate; no global recurrence or independent audit.'}
    (P/'results/normal_cell_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'exact_cases':len(exact),'graph_edges':out['exact_joint_crossing_edges'],
                     'probes':[{'input':v['input'],'N':sum(v['state']),'time':v['physical_mean_first_unexpected'],
                                'mass_drift':v['mean_mass_increment'],'probabilities':v['exit_probabilities']}
                               for v in out['finite_float_first_kill_diagnostics']]},indent=2))

if __name__=='__main__':main()
