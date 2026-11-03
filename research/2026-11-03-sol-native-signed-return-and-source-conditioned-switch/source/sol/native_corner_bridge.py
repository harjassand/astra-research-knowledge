#!/usr/bin/env python3
"""Exact raw corner and complete signed-workload bridge.

Completed predecessor files are imported read-only. Each corner inverse
is acquired on the actual full finite core fibres, with all block exits,
physical time and noncore count. No stationary entrance is substituted.
"""
from fractions import Fraction as F
from collections import deque,defaultdict
from functools import lru_cache
from pathlib import Path
import json

P=Path(__file__).resolve().parent
Y=((0,0,0),(1,1,0),(2,1,1),(3,2,2))

def ff(x,y):
    out=1
    for a,s in zip(x,y):
        if a<s:return 0
        for j in range(s):out*=a-j
    return out

def psi(x,w=20):
    ans=0
    for a,b,c in (x[:3],x[3:]):
        r=b-c;t=min(b,c)
        ans+=3*max(r,0)+w*max(-r,0)+2*(t%2)+t//2
    return ans

def channels(x,alpha=(1,1,1,1),beta=(1,1,1,1),core=(2,1)):
    for block,rates in enumerate((alpha,beta)):
        o=3*block
        for s in range(4):
            rate=F(rates[s])*ff(x[o:o+3],Y[s])
            if rate:
                out=list(x)
                for j in range(3):out[o+j]+=Y[(s+1)%4][j]-Y[s][j]
                yield tuple(out),rate,('block',block,s)
    for donor,k in enumerate(core):
        o=3*donor;t=3*(1-donor)
        rate=F(k)*x[0]*x[3]*ff(x[o+1:o+3],(2,2))
        if rate:
            out=list(x);out[o+1]-=2;out[o+2]-=2;out[t+1]+=2;out[t+2]+=2
            yield tuple(out),rate,('core',donor)

def solve_many(matrix,rhs):
    n=len(matrix);cols=len(rhs[0]);a=[list(row)+list(r) for row,r in zip(matrix,rhs)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if a[i][j]);a[j],a[pivot]=a[pivot],a[j]
        z=a[j][j];a[j]=[v/z for v in a[j]]
        for i in range(n):
            if i==j or not a[i][j]:continue
            z=a[i][j];a[i]=[v-z*t for v,t in zip(a[i],a[j])]
    return [row[n:n+cols] for row in a]

@lru_cache(maxsize=None)
def corner(root,w=20,alpha=(1,1,1,1),beta=(1,1,1,1),core=(2,1)):
    assert root[0]<=2 and root[3]<=2
    xs=[root];seen={root};todo=deque([root]);edges={}
    while todo:
        x=todo.popleft();row=list(channels(x,alpha,beta,core));edges[x]=row
        for out,rate,label in row:
            if out[0]<=2 and out[3]<=2 and out not in seen:
                seen.add(out);xs.append(out);todo.append(out)
    groups=defaultdict(list)
    for x in xs:
        a,b,c,d,e,f=x
        key=(a,d,b-c,e-f,b+e,b%2)
        if not(a*d):key=key+(b,)
        groups[key].append(x)
    values={};maxblock=0
    for key,states in sorted(groups.items(),key=lambda z:z[0][0]+z[0][1],reverse=True):
        size=len(states);maxblock=max(maxblock,size);ind={x:i for i,x in enumerate(states)}
        matrix=[[F(0) for _ in states] for _ in states]
        rhs=[[F(0) for _ in range(4)] for _ in states]
        for x,i in ind.items():
            rhs[i][0]=1
            for out,rate,label in edges[x]:
                matrix[i][i]+=rate
                if label[0]=='core':
                    assert out in ind
                    matrix[i][ind[out]]-=rate
                else:
                    rhs[i][1]+=rate
                    if out[0]<=2 and out[3]<=2:
                        val=values[out]
                    else:
                        po=psi(out,w);val=(F(0),F(0),F(po),F(po*po))
                    for k in range(4):rhs[i][k]+=rate*val[k]
        sol=solve_many(matrix,rhs)
        for x,i in ind.items():values[x]=tuple(sol[i])
    time,count,mean,second=values[root]
    pin=psi(root,w)
    assert 0<time<=F(5,alpha[0]+beta[0])
    assert 1<=count<=5
    return {'time':time,'count':count,'mean_psi':mean,'second_psi':second,
            'mean_delta':mean-pin,'second_delta':second-2*pin*mean+pin*pin,
            'states':len(xs),'largest_core_block':maxblock}

def complete_bridge(c,e=0,f=None,w=20,alpha=(1,1,1,1),beta=(1,1,1,1),core=(2,1),attach_corner=True):
    if f is None:f=c+e
    root=(3,1,c,0,e,f)
    chain=[root,(4,2,c+1,0,e,f),(1,0,c-1,0,e,f),
           (2,1,c-1,0,e,f),(3,2,c,0,e,f)]
    continuing=(('block',0,2),('block',0,3),('block',0,0),('block',0,2),('block',0,3))
    val=None;corners={};all_outputs=[]
    for i in range(4,-1,-1):
        x=chain[i];row=list(channels(x,alpha,beta,core));q=sum(rate for _,rate,_ in row)
        result=[F(1,q),F(1),F(0),F(0)]
        for out,rate,label in row:
            if label==continuing[i] and i<4:
                assert out==chain[i+1];z=val
            else:
                if attach_corner and out[0]<=2 and out[3]<=2:
                    k=corner(out,w,alpha,beta,core);corners[out]=k
                    z=(k['time'],k['count'],k['mean_psi'],k['second_psi'])
                else:
                    pp=psi(out,w);z=(F(0),F(0),F(pp),F(pp*pp))
                all_outputs.append(out)
            for k in range(4):result[k]+=rate/q*z[k]
        val=tuple(result)
    time,count,mean,second=val;pin=psi(root,w)
    return {'root':root,'weight':w,'time':time,'count':count,'mean_delta':mean-pin,
            'second_delta':second-2*pin*mean+pin*pin,'psi_in':pin,
            'corners':corners,'trace_halo_outputs':all_outputs}

def small(v):
    if isinstance(v,F):return {'exact':str(v),'float':float(v)}
    if isinstance(v,dict):return {str(k):small(t) for k,t in v.items()}
    if isinstance(v,(list,tuple)):return [small(t) for t in v]
    return v

def main():
    out=[]
    for n in (10,100,10000):
        for e in (0,2,10):
            for f in (n+e,10**10+n+e):
                full=complete_bridge(n,e,f)
                bare=complete_bridge(n,e,f,attach_corner=False)
                out.append({'complete':small(full),'bare_mean_delta':small(bare['mean_delta'])})
                print(json.dumps({'n':n,'e':e,'f':f,'bare':float(bare['mean_delta']),
                                  'common_corner_bridge':float(full['mean_delta']),
                                  'physical':float(full['time']),'count':float(full['count']),
                                  'corner_states':sum(k['states'] for k in full['corners'].values())}),flush=True)
    rates=(((2,5,3,7),(1,2,3,4)),((1,1000,1,1),(10,1,100,1)))
    for alpha,beta in rates:
        w=int(4+8*(alpha[0]+beta[0])/min(alpha[0],beta[0]))
        full=complete_bridge(10**5,10,10**12,w,alpha,beta)
        out.append({'rates':[alpha,beta],'complete':small(full)})
        print(json.dumps({'rates':[alpha,beta],'w':w,'mean_delta':float(full['mean_delta'])}),flush=True)
    target=P/'results/native_corner_bridge_checks.json'
    target.write_text(json.dumps({'scope':'Exact finite actual raw kernels including EVERY corner/peer output. Analytic all-population scope is separate.','cases':out},indent=2)+'\n')

if __name__=='__main__':main()
