#!/usr/bin/env python3
"""Exact raw-list constructor for INCOMPATIBLE_GATE_CALIBRATION.md.

This sufficient graph rule is an ordinary Foster calibration. It is not a
general recurrence decider and does not compute a stationary normalizer.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json
from support_receiver_certificate import canon, enc

P=Path(__file__).resolve().parent
def ceilq(x):
    x=F(x);return -(-x.numerator//x.denominator)
def sqrtceil(x):
    x=F(x);n=isqrt(x.numerator//x.denominator)
    return n if n*n*x.denominator==x.numerator else n+1

def inspect(raw):
    d,raw=canon(raw)
    if d<2:raise ValueError('need at least one hidden vertex')
    rates={(y,z):c for y,z,c in raw};zero=(0,)*d
    def complex(*entries):
        x=[0]*d
        for i,n in entries:x[i]+=n
        return tuple(x)
    A=complex((0,1));AA=complex((0,2))
    try:lam,mu=rates[(zero,A)],rates[(A,zero)]
    except KeyError:raise ValueError('missing sole port')
    used={(zero,A),(A,zero)};arms=[];edges=[];adj={i:set() for i in range(1,d)}
    for i in range(1,d):
        mix=complex((0,1),(i,1))
        if (AA,mix) in rates or (mix,AA) in rates:
            if (AA,mix) not in rates or (mix,AA) not in rates:raise ValueError('one-way root arm')
            arms.append((i,rates[(AA,mix)],rates[(mix,AA)]));used.update([(AA,mix),(mix,AA)])
    for i in range(1,d):
        for j in range(i+1,d):
            ii=complex((i,2));jj=complex((j,2));mix=complex((i,1),(j,1))
            keys=[(ii,mix),(mix,ii),(jj,mix),(mix,jj)]
            if any(k in rates for k in keys):
                if not all(k in rates for k in keys):raise ValueError('incomplete hidden three-complex edge')
                edges.append((i,j,*[rates[k] for k in keys]));used.update(keys);adj[i].add(j);adj[j].add(i)
    if used!=set(rates):raise ValueError('unsupported extra genuine channel')
    roots={i for i,p,b in arms};seen=set(roots);todo=list(roots)
    while todo:
        i=todo.pop()
        for j in adj[i]-seen:seen.add(j);todo.append(j)
    if seen!=set(adj):raise ValueError('a hidden component has no port arm')
    return {'d':d,'raw':raw,'lambda':lam,'mu':mu,'arms':arms,'edges':edges}

def acquire(raw,u=F(21,20),t=F(11,10),bit_budget=200000):
    try:info=inspect(raw)
    except (ValueError,TypeError,ZeroDivisionError) as e:return {'scope_status':'UNKNOWN','reason':str(e)}
    u,t=F(u),F(t)
    if not 1<u<t:return {'scope_status':'RAW_GRAPH_MATCH','quantitative_status':'INVALID_PARAMETERS'}
    if info['d']>16 or any(max(c.numerator.bit_length(),c.denominator.bit_length())>bit_budget for y,z,c in info['raw']):
        return {'scope_status':'RAW_GRAPH_MATCH','quantitative_status':'REFUSED_BUDGET'}
    p=1
    while 2**p<2*t:
        p+=1
        if p>32:return {'scope_status':'RAW_GRAPH_MATCH','quantitative_status':'REFUSED_BUDGET'}
    h=info['d']-1;lam,mu=info['lambda'],info['mu'];dt=1-1/t;zeta=1-u/t
    oriented=[];CH=F(0)
    for i,j,alpha,beta,gamma,delta in info['edges']:
        for receiver,donor,aa,dd,gg in [(i,j,alpha,delta,gamma),(j,i,gamma,beta,alpha)]:
            ci=gg/4;Ci=aa+(dd+gg/2)**2/gg;CH+=Ci
            oriented.append((receiver,donor,ci,Ci))
    B=sum(b for i,a,b in info['arms']);PP=sum(a for i,a,b in info['arms'])
    cc=4*(t-1+1/lam);ee=min(F(1,h),1/(1+CH),mu*dt/(4*B))
    C0=lam*(t-1)*(1+ee*h)+lam*cc*t+mu*cc/t+cc*p*PP+ee*CH
    KA=max(2,ceilq(4*(C0+1)/(mu*dt)))
    bS=cc*min(b for i,a,b in info['arms'])*p/F((KA+2)**(p+1))
    RR=max([1]+[sqrtceil((C0+1)/(ee*ci)) for i,j,ci,Ci in oriented])
    MM=ceilq((C0+1)/bS)+1;Mlevels=[MM]
    for _ in range(h):MM=RR*(MM+1);Mlevels.append(MM)
    K=sum(c for y,z,c in info['raw']);Cq=4*(1+lam+mu+K)
    head=max(KA+h*MM,ceilq((4/zeta)**2),ceilq(4*Cq/zeta))+1
    bits=max(head.bit_length(),*(max(v.numerator.bit_length(),v.denominator.bit_length()) for v in [bS,C0,cc,ee]))
    if bits>bit_budget:return {'scope_status':'RAW_GRAPH_MATCH','quantitative_status':'REFUSED_BUDGET'}
    return {'scope_status':'RAW_GRAPH_MATCH','quantitative_status':'GLOBAL_FOSTER_HEAD_ACQUIRED',
            'theorem':'INCOMPATIBLE_GATE_CALIBRATION.md','raw':{'d':info['d'],'rates':[{'source':y,'product':z,'rate':enc(c)} for y,z,c in info['raw']]},
            'u':enc(u),'t':enc(t),'p':p,'c':enc(cc),'e':enc(ee),'C_H':enc(CH),'C_0':enc(C0),
            'K_A':KA,'b_S':enc(bS),'ratio_bound':RR,'propagated_bounds':Mlevels,
            'head_N':enc(head),'head_bits':head.bit_length(),
            'contract':'L[t^N*(1+c/(A+1)^p+e*sum_i 1/(Xi+1))] <= -(1+q)*u^N - t^N/2 outside acquired head.',
            'finite_head_trace_and_stationary_normalizer':'NOT_ACQUIRED; theorem closes true finite trace existentially.',
            'unrestricted_weak_reversibility':'NOT_ACHIEVED'}

def diagnostic(hidden_count=2):
    d=hidden_count+1
    def v(*entries):
        x=[0]*d
        for i,n in entries:x[i]+=n
        return tuple(x)
    zero=(0,)*d;A=v((0,1));AA=v((0,2));AB=v((0,1),(1,1))
    raw=[(zero,A,1),(A,zero,1),(AA,AB,1),(AB,AA,1)]
    for i in range(1,hidden_count):
        mix=v((i,1),(i+1,1));ii=v((i,2));jj=v((i+1,2))
        raw.extend([(ii,mix,2 if i==1 else 1),(mix,ii,1),(jj,mix,1),(mix,jj,1)])
    return raw

if __name__=='__main__':
    rows=[]
    for h in [1,2,3]:
        cert=acquire(diagnostic(h));assert cert['quantitative_status']=='GLOBAL_FOSTER_HEAD_ACQUIRED'
        f=P/'results'/('reciprocal_bath_hidden'+str(h)+'.json');f.write_text(json.dumps(cert,indent=2)+'\n')
        rows.append({'hidden_count':h,'head_bits':cert['head_bits'],'file':f.name})
    print(json.dumps(rows,indent=2))
