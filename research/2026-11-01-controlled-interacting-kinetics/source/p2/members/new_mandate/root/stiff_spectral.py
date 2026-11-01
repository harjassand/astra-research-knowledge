"""Stiff Gaussian reference: 90-digit Decimal algebra, no extra dependencies.
Two slow pair-flip edges separate fast parity sectors. Small system explicitly
compares with a conventional high-precision full-state solve. No speedup claim.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS","1")
from decimal import Decimal as D, localcontext
import numpy as np
import json,time
from pathlib import Path
from gaussian_kinetics import model


def eye(n):
    x=np.full((n,n),D(0),dtype=object)
    for i in range(n):x[i,i]=D(1)
    return x


def solve(A,b):
    A=A.copy();b=b.copy();n=len(A)
    if b.ndim==1:b=b[:,None]
    for k in range(n):
        p=max(range(k,n),key=lambda i:abs(A[i,k]))
        if p!=k:A[[p,k]]=A[[k,p]];b[[p,k]]=b[[k,p]]
        pivot=A[k,k]
        A[k,k:]=A[k,k:]/pivot;b[k,:]=b[k,:]/pivot
        for i in range(n):
            if i==k:continue
            z=A[i,k];A[i,k:]-=z*A[k,k:];b[i,:]-=z*b[k,:]
    return b


def determinant(A):
    A=A.copy();n=len(A);v=D(1)
    for k in range(n):
        p=max(range(k,n),key=lambda i:abs(A[i,k]))
        if p!=k:A[[p,k]]=A[[k,p]];v=-v
        pivot=A[k,k];v*=pivot
        if not pivot:return D(0)
        for i in range(k+1,n):A[i,k+1:]-=A[i,k]/pivot*A[k,k+1:]
    return v


def jacobi(A):
    A=A.copy();n=len(A);V=eye(n)
    for iteration in range(100*n*n):
        p,q=max(((i,j) for i in range(n) for j in range(i+1,n)),key=lambda x:abs(A[x]))
        if abs(A[p,q])<D('1e-80'):break
        tau=(A[q,q]-A[p,p])/(2*A[p,q])
        sign=D(1) if tau>=0 else D(-1)
        t=sign/(abs(tau)+(1+tau*tau).sqrt());c=1/(1+t*t).sqrt();s=t*c
        ap=A[p,p];aq=A[q,q];off=A[p,q]
        A[p,p]=ap-t*off;A[q,q]=aq+t*off;A[p,q]=A[q,p]=D(0)
        for j in range(n):
            if j==p or j==q:continue
            x,y=A[j,p],A[j,q]
            A[j,p]=A[p,j]=c*x-s*y;A[j,q]=A[q,j]=s*x+c*y
        vp=V[:,p].copy();vq=V[:,q].copy();V[:,p]=c*vp-s*vq;V[:,q]=s*vp+c*vq
    else:raise RuntimeError("Jacobi did not converge")
    order=sorted(range(n),key=lambda i:A[i,i])
    return [A[i,i] for i in order],V[:,order],iteration


def run():
    begin=time.perf_counter()
    with localcontext() as ctx:
        ctx.prec=90;n=6;J=[D('.4')]*n;nu=[D(1)]*n
        nu[1]=nu[4]=D('1e-40')
        normal=np.full((n,n),D(0),dtype=object);pair=normal.copy()
        c=[];a=[];d=[];e=[]
        for i in range(n):
            j=(i+1)%n
            c.append(nu[i]/(1+(2*(J[i]+J[j])).exp()));a.append(nu[i]-c[-1])
            d.append(nu[i]/(1+(2*(J[j]-J[i])).exp()));e.append(nu[i]-d[-1])
            normal[i,i]+=c[i]-d[i];normal[j,j]+=c[i]-e[i]
            sg=1 if j>i else -1
            normal[i,j]+=sg*(d[i]*e[i]).sqrt();normal[j,i]+=sg*(d[i]*e[i]).sqrt()
            pair[i,j]+=sg*(c[i]*a[i]).sqrt();pair[j,i]-=sg*(c[i]*a[i]).sqrt()
        H=np.block([[-normal,-pair],[pair,normal.T]])
        ev,O,it=jacobi(H);eps=ev[n:];U=O[:n,n:];V=O[n:,n:];Z=-solve(U,V)
        gap=eps[0]+eps[1]
        # Explicit equilibrium law in the even sector.
        states=[s for s in range(1<<n) if s.bit_count()%2==0];ind={s:i for i,s in enumerate(states)}
        p=[(-sum(2*J[i]*((s>>i)&1) for i in range(n))).exp() for s in states];tot=sum(p);p=[x/tot for x in p];pi=p[0]
        def ret(t):
            W=Z.copy()
            for i in range(n):
                for j in range(n):W[i,j]*=(-(eps[i]+eps[j])*t/2).exp()
            return pi*determinant(eye(n)+W.T@W).sqrt()
        Q=np.full((len(states),len(states)),D(0),dtype=object)
        for col,s in enumerate(states):
            for i in range(n):
                j=(i+1)%n;x=(s>>i)&1;y=(s>>j)&1
                r=c[i] if (x,y)==(0,0) else a[i] if (x,y)==(1,1) else d[i] if (x,y)==(1,0) else e[i]
                row=ind[s^(1<<i)^(1<<j)];Q[row,col]+=r;Q[col,col]-=r
        times=solve(-Q[1:,1:].T,np.full(len(states)-1,D(1),dtype=object))[:,0]
        mean=sum(p[i]*times[i-1] for i in range(1,len(states)))/(1-pi)
        dp=model(np.full(n,.4),np.array([float(x) for x in nu]))
        out={'n':n,'precision_digits':90,'jacobi_iterations':it,'attempt_rates':[str(x) for x in nu],
             'gap_high_precision':str(gap),'gap_double_precision':dp['gap'],
             'double_gap_relative_error':str(abs(D(str(dp['gap']))/gap-1)),
             'target_probability':str(pi),'physical_mean_dense_high_precision':str(mean),
             'gaussian_return_samples':[{'t':f'1e{k}','return':str(ret(D(10)**k))} for k in [0,10,20,30,40,42]],
             'gaussian_normalization_error':str(abs(ret(D(0))-1)),
             'spectral_condition_upper':str(2*sum(nu)/gap),
             'seconds':time.perf_counter()-begin,
             'scope':'Two slow interfaces preserve segment parity for long times; finite six-site test. Dense inversion succeeds. A conventional four-sector averaging model captures the leading stiff limit.'}
    Path(__file__).with_name('stiff_spectral_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

if __name__=='__main__':run()
