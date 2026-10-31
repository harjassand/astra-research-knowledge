#!/usr/bin/env python3
"""Construct a passive-equivalent pair and attack work-prediction ambiguity.

Exploratory master-equation calculations; no experimental records. Floating
work signs are proposals pending an independent rational enclosure.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import sys
import time
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/interventional_generator'
sys.path.insert(0,str(ROOT/'work'))
from coherent_generator_control import identity,mm,inverse,mv


def ring(n=8):
    labels=[1 if i<n//2 else -1 for i in range(n)]
    q=[[F(1,n) if i!=j else F(0) for j in range(n)] for i in range(n)]
    for i in range(n):q[i][(i+1)%n]+=10;q[i][(i-1)%n]+=1
    for i in range(n//2):
        for j in range(n//2,n):q[i][j]+=F((i+1)*(j+1),10000);q[j][i]+=F((i+1)*(j+1),10000)
    for i in range(n):q[i][i]=-sum(q[i])
    return q,[F(1,n)]*n,labels


def gauge(q,epsilon=F(1,500),pair=(2,3)):
    n=len(q);S=identity(n);i,j=pair
    S[i][i]=S[j][j]=1-epsilon;S[i][j]=S[j][i]=epsilon
    Si=inverse(S);other=mm(mm(Si,q),S)
    assert all(other[i][j]>0 for i in range(n) for j in range(n) if i!=j)
    assert all(sum(row)==0 for row in other)
    assert all(sum(other[i][j] for i in range(n))==0 for j in range(n))
    return other,S,Si


def controlled(q,labels,t):
    n=len(q);out=[[F(0)]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i!=j:out[i][j]=q[i][j]*(t**((labels[j]-labels[i])//2))
        out[i][i]=-sum(out[i])
    return out


def array(q):return np.array([[float(x) for x in row] for row in q])


def susceptibility(q,pi,f,w):
    g=-.5*(q@f+(q.T@(pi*f))/pi)
    return np.dot(pi*g,np.linalg.solve(-1j*w*np.eye(len(q))-q,f))


def cycle(q,pi,f,ratios,dt):
    qs=[array(controlled(q,list(map(int,f)),t)) for t in ratios]
    kernels=[expm(float(dt)*z) for z in qs];K=np.eye(len(q))
    for E in kernels:K=K@E
    A=K.T-np.eye(len(q));A[-1,:]=1;b=np.zeros(len(q));b[-1]=1
    p=np.linalg.solve(A,b);initial=p.copy();work=0;fuel_lo=fuel_hi=0
    base=array(q);affinity=np.zeros_like(base)
    for i in range(len(q)):
        for j in range(len(q)):
            if i!=j:affinity[i,j]=math.log(base[i,j]/base[j,i])
    for k,(t,z,E) in enumerate(zip(ratios,qs,kernels)):
        delta=math.log(float(t))-math.log(float(ratios[k-1]))
        work-=delta*float(p@f)
        power=(np.maximum(z,0)*affinity).sum(axis=1)
        fuel_lo+=float(dt)*power.min();fuel_hi+=float(dt)*power.max()
        p=p@E
    return {'work_on':work,'fuel_input_interval':[fuel_lo,fuel_hi],
            'periodic_residual_L1':float(abs(p-initial).sum()),'periodic_initial':list(initial),
            'period':float(dt)*len(ratios)}


def main():
    start=time.perf_counter();OUT.mkdir(exist_ok=True,parents=True)
    q,pi,labels=ring();other,S,Si=gauge(q);n=len(q)
    A,B=array(q),array(other);p=np.array(list(map(float,pi)));f=np.array(labels)
    roots=[]
    for name,z in [('source',A),('passive_equivalent',B)]:
        ws=np.geomspace(.001,40,400);vals=[susceptibility(z,p,f,w).imag for w in ws]
        crosses=[]
        for a,b,va,vb in zip(ws[:-1],ws[1:],vals[:-1],vals[1:]):
            if va*vb<0:crosses.append(brentq(lambda w:susceptibility(z,p,f,w).imag,a,b,xtol=1e-14))
        roots.append({'name':name,'roots':crosses,'imag_at_0.01':susceptibility(z,p,f,.01).imag})
    protocols=[]
    if all(row['roots'] for row in roots):
        w=sum(row['roots'][0] for row in roots)/2
        for steps in (16,32,64):
            # Positive rational field multipliers t=exp(h); h=log(t).
            # Rounding fixes the ACTUAL protocol instead of assigning an
            # ideal cosine or a zero-duration smooth-control approximation.
            dt=F(2*math.pi/(w*steps)).limit_denominator(100000000)
            ratios=[F(1+.001*math.cos(2*math.pi*k/steps)).limit_denominator(100000000) for k in range(steps)]
            protocols.append({'steps':steps,'candidate_omega':w,'step_duration':str(dt),
                              'field_multipliers':list(map(str,ratios)),
                              'source':cycle(q,p,f,ratios,dt),
                              'passive_equivalent':cycle(other,p,f,ratios,dt)})
    data={'status':'EXPLORATORY_INTERVENTION_OPENING','synthetic_acquisitions':0,'physical_experiments':0,
          'Q':[[str(x) for x in row] for row in q],'Q_gauge':[[str(x) for x in row] for row in other],
          'S':[[str(x) for x in row] for row in S],'stationary_pi':list(map(str,pi)),'labels':labels,
          'passive_identity_exact':mm(mm(Si,q),S)==other,
          'label_projectors_commute_with_S':all(S[i][j]==0 for i in range(n) for j in range(n) if labels[i]!=labels[j]),
          'linear_response_roots':roots,'finite_protocols':protocols,
          'elapsed_wall_seconds':time.perf_counter()-start,
          'unacquired':['calibrated field-rate law','physical apparatus','controller energy and clock','reset/preparation device'],
          'strong_incumbent':'ordinary master equation and optimal control supplied with the same actual generator'}
    (OUT/'opening_receipt.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ['Q','Q_gauge','S','finite_protocols']}|{
        'finite_protocols':[{'steps':x['steps'],'work_on_source':x['source']['work_on'],
                            'work_on_gauge':x['passive_equivalent']['work_on'],
                            'fuel_source':x['source']['fuel_input_interval']} for x in protocols]},indent=2))


if __name__=='__main__':main()
