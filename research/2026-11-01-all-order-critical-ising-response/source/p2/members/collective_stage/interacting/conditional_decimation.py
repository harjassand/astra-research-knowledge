"""Conditional response decimation of a genuine interacting Ising chain.

Every averaging coefficient and fast response is calculated from local rates and
Gibbs transfer matrices. Bounds are proved operator comparisons evaluated in
floating point, not interval arithmetic. Dense solves are independent checks.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import json, math, time
from pathlib import Path
import numpy as np
from scipy.special import expit
from scipy.linalg import solve

SP=np.array([-1.,1.])

def initial_model(n,J,alpha,facilitation=2.):
    assert n>=1 and (n+1)&n==0
    bonds=np.full(n+1,float(J))
    clocks=np.array([float(alpha)**((i&-i).bit_length()-1) for i in range(1,n+1)])
    rates=np.empty((n,2,2,2))
    for i in range(n):
        for l,L in enumerate(SP):
            for s,S in enumerate(SP):
                for r,R in enumerate(SP):
                    A=.5+facilitation*(L==1 and R==1)
                    rates[i,l,s,r]=clocks[i]*A*expit(-2*S*(bonds[i]*L+bonds[i+1]*R))
    return bonds,rates,np.ones(n)/math.sqrt(n),clocks

def edge_marginals(bonds):
    n=len(bonds)-1
    T=np.exp(bonds[:,None,None]*SP[None,:,None]*SP[None,None,:])
    left=np.empty((n+2,2));right=np.empty_like(left)
    left[0]=[0,1]
    for i in range(n+1):
        v=left[i]@T[i]
        if i==n:v*=np.array([0,1])
        left[i+1]=v/v.sum()
    right[-1]=[0,1]
    for i in range(n,-1,-1):
        v=T[i]@right[i+1]
        if i==0:v*=np.array([0,1])
        right[i]=v/v.sum()
    pairs=left[:-1,:,None]*T*right[1:,None,:]
    pairs/=pairs.sum(axis=(1,2))[:,None,None]
    return pairs

def source_variance(bonds,weights):
    z=np.array([0.,1.]);a=np.zeros(2);b=np.zeros(2)
    n=len(weights)
    for i,J in enumerate(bonds):
        T=np.exp(J*SP[:,None]*SP[None,:])
        w=weights[i] if i<n else 0.
        zn=z@T
        an=a@T+w*SP*zn
        bn=b@T+2*w*SP*(a@T)+w*w*zn
        if i==n:
            zn[0]=an[0]=bn[0]=0
        norm=zn.sum();z=zn/norm;a=an/norm;b=bn/norm
    return float(a.sum()),float(b.sum()-a.sum()**2)

def prefactors(rates):
    return rates[:,:,0,:]+rates[:,:,1,:]

def one_decimation(bonds,rates,weights):
    n=len(weights);assert n>1 and n%2
    nn=(n-1)//2
    bnew=np.arctanh(np.tanh(bonds[0::2])*np.tanh(bonds[1::2]))
    pairs=edge_marginals(bnew)
    wnew=weights[1::2].copy()
    fast=0.
    for k,j in enumerate(range(0,n,2)):
        JL,JR=bonds[j],bonds[j+1]
        means=np.tanh(JL*SP[:,None]+JR*SP[None,:])
        af=prefactors(rates)[j]
        fast+=weights[j]**2*np.sum(pairs[k]*(1-means**2)/af)
        al=.5*(math.tanh(JL+JR)+math.tanh(JL-JR))
        ar=.5*(math.tanh(JL+JR)-math.tanh(JL-JR))
        if k>0:wnew[k-1]+=weights[j]*al
        if k<nn:wnew[k]+=weights[j]*ar
    rnew=np.empty((nn,2,2,2))
    for k,j in enumerate(range(1,n,2)):
        for l,L in enumerate(SP):
            for s,S in enumerate(SP):
                for r,R in enumerate(SP):
                    pl=np.array([expit(2*x*(bonds[j-1]*L+bonds[j]*S)) for x in SP])
                    pr=np.array([expit(2*x*(bonds[j+1]*S+bonds[j+2]*R)) for x in SP])
                    rnew[k,l,s,r]=np.sum(pl[:,None]*pr[None,:]*rates[j,:,s,:])
    a=prefactors(rates)
    gfast=float(a[0::2].min())
    lambdaslow=float(a[1::2].max(axis=(1,2)).sum())
    theta=lambdaslow/gfast
    factor=1+theta/2+math.sqrt(theta*theta+4*theta)/2
    balance=0.
    for i in range(nn):
        for l,L in enumerate(SP):
            for r,R in enumerate(SP):
                expected=-2*(bnew[i]*L+bnew[i+1]*R)
                balance=max(balance,abs(math.log(rnew[i,l,1,r]/rnew[i,l,0,r])-expected))
    return bnew,rnew,wnew,dict(n=n,fast_response=float(fast),gfast=gfast,
        slow_norm_bound=lambdaslow,theta=theta,factor=factor,
        detailed_balance_log_error=balance)

def response(bonds,rates,weights):
    begin=time.perf_counter()
    original_variance=source_variance(bonds,weights)[1]
    levels=[]
    while len(weights)>1:
        bonds,rates,weights,record=one_decimation(bonds,rates,weights)
        levels.append(record)
    v=1-math.tanh(float(bonds.sum()))**2
    a=float(prefactors(rates)[0,1,1])
    last=weights[0]**2*v/a
    low=high=central=last
    for rec in reversed(levels):
        low=(rec['fast_response']+low)/rec['factor']
        high=(rec['fast_response']+high)*rec['factor']
        central+=rec['fast_response']
    return dict(estimate=float(central),lower=float(low),upper=float(high),
        relative_width=float((high-low)/low),levels=levels,
        source_variance=original_variance,
        final_slow_projection_variance=float(weights[0]**2*v),
        final_slow_projection_fraction=float(weights[0]**2*v/original_variance),
        final_slow_prefactor=a,seconds=time.perf_counter()-begin)

def dense_response(bonds,rates,weights):
    n=len(weights);S=np.array([[1 if s>>i&1 else -1 for i in range(n)] for s in range(1<<n)])
    full=np.c_[np.ones(len(S)),S,np.ones(len(S))]
    lp=np.sum(bonds[None,:]*full[:,:-1]*full[:,1:],axis=1);p=np.exp(lp-lp.max());p/=p.sum()
    K=np.zeros((len(S),len(S)))
    for s in range(len(S)):
        for i in range(n):
            l=int(full[s,i]>0);x=int(full[s,i+1]>0);r=int(full[s,i+2]>0)
            rate=rates[i,l,x,r]
            K[s,s]+=rate;K[s,s^(1<<i)]-=rate
    f=S@weights;f-=p@f
    u=solve(K+np.ones((len(S),1))*p[None,:],f,assume_a='gen')
    return float((p*f)@u)

def decimal_dense(n,J,alpha,prec=75,facilitation=2.):
    """Independent direct spin-space calculation using Decimal Gaussian elimination."""
    from decimal import Decimal as D, localcontext
    with localcontext() as ctx:
        ctx.prec=prec
        JJ=D(str(J));aa=D(str(alpha));FF=D(str(facilitation));one=D(1);zero=D(0)
        states=[[D(1) if s>>i&1 else D(-1) for i in range(n)] for s in range(1<<n)]
        weights=[];rates=[];obs=[]
        normn=D(n).sqrt()
        for st in states:
            full=[one]+st+[one]
            weights.append((JJ*sum((full[i]*full[i+1] for i in range(n+1)),zero)).exp())
            rr=[]
            for i in range(n):
                ii=i+1;nu=aa**((ii&-ii).bit_length()-1)
                A=D('.5')+(FF if full[i]==one and full[i+2]==one else zero)
                rr.append(nu*A/(one+(2*st[i]*JJ*(full[i]+full[i+2])).exp()))
            rates.append(rr);obs.append(sum(st,zero)/normn)
        Z=sum(weights,zero);p=[x/Z for x in weights]
        mean=sum((x*y for x,y in zip(p,obs)),zero);f=[x-mean for x in obs]
        size=len(states);A=[[p[j] for j in range(size)]+[f[i]] for i in range(size)]
        for i in range(size):
            for site,rate in enumerate(rates[i]):
                A[i][i]+=rate;A[i][i^(1<<site)]-=rate
        for k in range(size):
            pivot=max(range(k,size),key=lambda i:abs(A[i][k]))
            A[k],A[pivot]=A[pivot],A[k]
            pivotval=A[k][k]
            for i in range(k+1,size):
                if not A[i][k]:continue
                fac=A[i][k]/pivotval;A[i][k]=zero
                for j in range(k+1,size+1):A[i][j]-=fac*A[k][j]
        sol=[zero]*size
        for i in range(size-1,-1,-1):
            sol[i]=(A[i][-1]-sum((A[i][j]*sol[j] for j in range(i+1,size)),zero))/A[i][i]
        return str(sum((p[i]*f[i]*sol[i] for i in range(size)),zero))

def main():
    checks=[]
    for n,J,alpha in [(3,.8,1e-2),(7,1.2,1e-3),(7,1.2,1e-6)]:
        b,r,w,nu=initial_model(n,J,alpha)
        out=response(b,r,w)
        exact=float(decimal_dense(n,J,alpha))
        checks.append(dict(n=n,J=J,alpha=alpha,exact_decimal=exact,
            response=out,contains=out['lower']<=exact<=out['upper'],
            estimate_relative_error=abs(out['estimate']/exact-1)))
    collective=[]
    for n in [31,127,511,2047]:
        J=.5*math.log(n+1)
        alpha=1e-10/(n+1)
        b,r,w,nu=initial_model(n,J,alpha)
        out=response(b,r,w)
        collective.append(dict(n=n,J=J,alpha=alpha,clock_log10_span=-float(np.log10(nu.min())),response=out))
    payload={'scope':'Constructed finite relative-response bounds; floating evaluations, no interval arithmetic. Explicit hierarchical clock separation; conventional averaging is a strong comparator.',
        'small_independent_decimal_checks':checks,'collective':collective}
    dest=Path(__file__).with_name('conditional_decimation_results.json')
    dest.write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload,indent=2))

if __name__=='__main__':main()
