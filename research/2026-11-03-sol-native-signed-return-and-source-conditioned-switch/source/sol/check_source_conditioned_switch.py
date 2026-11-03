#!/usr/bin/env python3
"""Exact actual two-stage activation switch; no entrance-law assumption.

The all-parameter proof is SOURCE_CONDITIONED_CORE_SWITCH.md. Each test
starts at the real empty endpoint B=0, with arbitrary finite peer inventory.
"""
from fractions import Fraction as F
from pathlib import Path
import json

P=Path(__file__).resolve().parent

def tri(lo,di,up,rhs):
    n=len(di);d=list(di);r=list(rhs)
    for j in range(1,n):
        t=lo[j]/d[j-1];d[j]-=t*up[j-1];r[j]-=t*r[j-1]
    out=[F(0)]*n;out[-1]=r[-1]/d[-1]
    for j in range(n-2,-1,-1):out[j]=(r[j]-up[j]*out[j+1])/d[j]
    return out

def build(q,s1,s2,alpha1=5,alpha2=3,beta1=2,beta2=4,B0=3,kf=2,kb=1,post=None):
    bs=list(range(0,q+1,2));lo=[];di=[];up=[];h1=[];h2=[];k=[];birth=[];death=[]
    for b in bs:
        e=q-b;c=b+s1;f=e+s2
        a=d=1
        if post==0:a=2;c+=1
        if post==1:d=2;f+=1
        left=F(kf*a*d*b*(b-1)*c*(c-1)) if b>=2 else F(0)
        right=F(kb*a*d*e*(e-1)*f*(f-1)) if e>=2 else F(0)
        hh1=F(alpha1*b);hh2=F(beta1*e)
        if post is None:kill=hh1+hh2+B0
        else:
            fast=F(2*(alpha2 if post==0 else beta2)*(b if post==0 else e)*(c if post==0 else f))
            enemy=(hh2 if post==0 else hh1)+B0
            kill=fast+enemy;k.append(enemy)
        lo.append(-left);up.append(-right);di.append(left+right+kill)
        h1.append(hh1);h2.append(hh2);birth.append(right);death.append(left)
    return bs,lo,di,up,h1,h2,k,birth,death

def probe(q,s1,s2):
    alpha1,alpha2,beta1,beta2,B0=5,3,2,4,3
    bs,lo,di,up,h1,h2,_,birth,death=build(q,s1,s2)
    size=len(bs)
    lot=[F(0)]*size;upt=[F(0)]*size
    for j in range(1,size):lot[j]=up[j-1]
    for j in range(size-1):upt[j]=lo[j+1]
    delta=[F(int(j==0)) for j in range(size)]
    nu=tri(lot,di,upt,delta)
    mu=[F(1)]
    for j in range(size-1):mu.append(mu[-1]*birth[j]/death[j+1])
    f=[v/m for v,m in zip(nu,mu)]
    assert all(f[j]>=f[j+1] for j in range(size-1))
    H=[h1[j]+h2[j]+B0 for j in range(size)]
    assert sum(nu[j]*H[j] for j in range(size))==1
    n=min(s1,s2);out=[]
    for port in (0,1):
        vals=build(q,s1,s2,post=port)
        _,lp,dp,upost,_,_,enemy,bp,dep=vals
        u=tri(lp,dp,upost,enemy)
        assert all(0<=z<=1 for z in u)
        if port==0:assert all(u[j]>=u[j+1] for j in range(size-1))
        else:assert all(u[j]<=u[j+1] for j in range(size-1))
        h=h1 if port==0 else h2
        prob=sum(nu[j]*h[j]*u[j] for j in range(size))
        D=[(b+s1+1) if port==0 else (q-b+s2+1) for b in bs]
        mup=[mu[j]/D[j] for j in range(size)]
        E=F(0);Ep=F(0)
        for j in range(size-1):
            cp=mu[j]*birth[j];cpp=mup[j]*bp[j]
            assert cpp<=F(2,n)*cp
            assert mup[j]*bp[j]==mup[j+1]*dep[j+1]
            prod=(f[j]-f[j+1])*(u[j]-u[j+1])
            E+=cp*prod;Ep+=cpp*prod
        assert abs(E)<=1 and abs(Ep)<=F(2,n)*abs(E)
        a1,a2=(alpha1,alpha2) if port==0 else (beta1,beta2)
        rhs=F(a1,2*a2)*(sum(nu[j]*enemy[j]*(1-u[j])/D[j] for j in range(size))-Ep)
        assert prob==rhs
        bound=F(3*a1,2*a2*n)
        assert prob<=bound,(q,s1,s2,port,prob,bound)
        out.append({'port':port,'exact_upper_probability':str(prob),'probability_float':float(prob),
                    'proved_bound':str(bound),'pre_dirichlet':str(E),'post_dirichlet':str(Ep)})
    return {'minority_total':q,'majority_gaps':[s1,s2],'core_states':size,'orders':out}

def main():
    rows=[]
    for q in (1,2,3,10,21,100):
        for s1,s2 in ((100,100),(100,10**12),(10**12,100),(10,10)):
            rows.append(probe(q,s1,s2))
    (P/'results/source_conditioned_switch_checks.json').write_text(json.dumps({'scope':'Exact finite full two-stage kernels and identities. Uniform all-population proof is separate.','cases':rows},indent=2)+'\n')
    print(json.dumps({'cases':len(rows),'two_stage_orders':2*len(rows),
                      'largest_minor_total':max(r['minority_total'] for r in rows),
                      'largest_majority_gap':10**12,
                      'worst_probability_times_min_gap':max(v['probability_float']*min(r['majority_gaps']) for r in rows for v in r['orders'])},indent=2))

if __name__=='__main__':main()
