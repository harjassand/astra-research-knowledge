"""Matched exact sparse and attractive-coupling local-window comparators."""
from fractions import Fraction as F
import time,json
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as sla
from probe_moments import Ring

def window(n,t,w,boundary,nu=F(1),kappa=F(1)):
    if not 1<=w<=n-2:raise ValueError('window must leave at least two exterior sites')
    start=time.perf_counter();law=Ring(n,F(1),F(t),nu,kappa);P=law.marginal(w);N=1<<w;center=w//2
    rows=[];cols=[];vals=[];rates=[];diags=[]
    for x in range(N):
        local=[];diag=kappa*((x>>center)&1)
        for i in range(w):
            a=((x>>(i-1))&1) if i else boundary
            b=(x>>i)&1
            c=((x>>(i+1))&1) if i<w-1 else boundary
            rt=law.q[(a,b,c)];local.append(rt);diag+=rt
            rows.append(x);cols.append(x^(1<<i));vals.append(-float(rt))
        rates.append(local);diags.append(diag)
        rows.append(x);cols.append(x);vals.append(float(diag))
    K=ss.csr_matrix((vals,(rows,cols)),shape=(N,N));v=sla.spsolve(K,np.ones(N));solve=time.perf_counter()
    vv=[F(float(a)) for a in v]
    residual=[diags[x]*vv[x]-sum(rates[x][i]*vv[x^(1<<i)] for i in range(w))-1 for x in range(N)]
    delta=max(abs(a) for a in residual)
    if delta>=1 or min(vv)<=0:raise ArithmeticError('failed residual certificate')
    mean=sum(p*a for p,a in zip(P,vv));lo=mean/(1+delta);hi=mean/(1-delta)
    end=time.perf_counter()
    return {'n':n,'t':str(t),'window':w,'boundary':boundary,'states':N,'lo':float(lo),'hi':float(hi),
            'lo_exact':str(lo),'hi_exact':str(hi),'delta':float(delta),'solve_s':solve-start,'verify_s':end-solve,'total_s':end-start}

def full(n,t,nu=F(1),kappa=F(1)):
    start=time.perf_counter();law=Ring(n,F(1),F(t),nu,kappa);P=law.marginal(n);N=1<<n
    rows=[];cols=[];vals=[];rates=[];diags=[]
    for x in range(N):
        local=[];diag=kappa*(x&1)
        for i in range(n):
            rt=law.q[((x>>((i-1)%n))&1,(x>>i)&1,(x>>((i+1)%n))&1)];local.append(rt);diag+=rt
            rows.append(x);cols.append(x^(1<<i));vals.append(-float(rt))
        rates.append(local);diags.append(diag)
        rows.append(x);cols.append(x);vals.append(float(diag))
    K=ss.csr_matrix((vals,(rows,cols)),shape=(N,N));v=sla.spsolve(K,np.ones(N));solved=time.perf_counter()
    vv=[F(float(a)) for a in v]
    delta=max(abs(diags[x]*vv[x]-sum(rates[x][i]*vv[x^(1<<i)] for i in range(n))-1) for x in range(N))
    if delta>=1 or min(vv)<=0:raise ArithmeticError('failed residual certificate')
    mean=sum(p*a for p,a in zip(P,vv));lo=mean/(1+delta);hi=mean/(1-delta)
    end=time.perf_counter()
    return {'n':n,'t':str(t),'states':N,'lo':float(lo),'hi':float(hi),'lo_exact':str(lo),'hi_exact':str(hi),
            'delta':float(delta),'solve_s':solved-start,'verify_s':end-solved,'total_s':end-start}

if __name__=='__main__':
    import sys
    dest=sys.argv[1];out={'windows':[],'full':[]}
    for w in [3,5,7,9,11]:
        a=window(24,F(1000),w,1);b=window(24,F(1000),w,0)
        row={'window':w,'lower':a,'upper':b,'ratio':b['hi']/a['lo']};out['windows'].append(row)
        print('window',w,a['lo'],b['hi'],row['ratio'],a['total_s']+b['total_s'],flush=True)
    for n in [6,8,10,12]:
        row=full(n,F(1000));out['full'].append(row);print('full',n,row['lo'],row['hi'],row['total_s'],flush=True)
    json.dump(out,open(dest,'w'))
