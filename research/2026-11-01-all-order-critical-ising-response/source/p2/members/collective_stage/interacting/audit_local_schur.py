"""Adversarial full-state audit of the local conditional-Schur response bound."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.special import expit
from conditional_decimation import SP, prefactors

def pinv_psd(K,nullity):
    e,U=eigh((K+K.T)/2)
    return (U[:,nullity:]/e[nullity:])@U[:,nullity:].T

def finite_matrices(J,rates,fields=None):
    n=len(rates);N=1<<n
    S=np.array([[1 if x>>i&1 else -1 for i in range(n)] for x in range(N)])
    X=np.c_[np.ones(N),S,np.ones(N)]
    fields=np.zeros(n) if fields is None else np.asarray(fields)
    lp=np.sum(J[None,:]*X[:,:-1]*X[:,1:],axis=1)+S@fields
    p=np.exp(lp-lp.max());p/=p.sum();g=np.sqrt(p)
    KF=np.zeros((N,N));KS=np.zeros_like(KF)
    for x in range(N):
        for i in range(n):
            r=rates[i,int(X[x,i]>0),int(X[x,i+1]>0),int(X[x,i+2]>0)]
            K=KF if i%2==0 else KS
            K[x,x]+=r;K[x,x^(1<<i)]-=r
    KF=g[:,None]*KF/g[None,:];KS=g[:,None]*KS/g[None,:]
    slow=[i for i in range(n) if i%2]
    group=np.array([sum(((x>>site)&1)<<j for j,site in enumerate(slow)) for x in range(N)])
    ps=np.bincount(group,weights=p,minlength=1<<len(slow))
    U=np.zeros((N,len(ps)))
    U[np.arange(N),group]=g/np.sqrt(ps[group])
    return KF,KS,U,g,S

def local_theta(J,rates,use_variance=True,fields=None):
    n=len(rates);a=prefactors(rates);maximum=0.
    fields=np.zeros(n) if fields is None else np.asarray(fields)
    for i in range(1,n,2):
        for L in SP:
            for sidx,S in enumerate(SP):
                for R in SP:
                    # Including impossible fixed-boundary values is conservative.
                    lidx=int(L>0);ridx=int(R>0)
                    gl=a[i-1,lidx,sidx];gr=a[i+1,sidx,ridx]
                    if use_variance:
                        pl=np.array([expit(2*x*(fields[i-1]+J[i-1]*L+J[i]*S)) for x in SP])
                        pr=np.array([expit(2*x*(fields[i+1]+J[i+1]*S+J[i+2]*R)) for x in SP])
                        pp=pl[:,None]*pr[None,:];ww=rates[i,:,sidx,:]
                        mean=np.sum(pp*ww);var=np.sum(pp*(ww-mean)**2)
                        ratio=var/(mean*min(gl,gr))
                    else:ratio=float(rates[i].max())/min(gl,gr)
                    maximum=max(maximum,float(ratio))
    return 4*maximum  # 2 from Dirichlet form, d_*=2 overlap on a chain

def local_theta_components(J,rates,fields=None):
    n=len(rates);a=prefactors(rates);maximum=0.
    fields=np.zeros(n) if fields is None else np.asarray(fields)
    for i in range(1,n,2):
        dleft=1 if i==1 else 2;dright=1 if i==n-2 else 2
        for l,L in enumerate(SP):
            for s,S in enumerate(SP):
                for r,R in enumerate(SP):
                    p=expit(2*(fields[i-1]+J[i-1]*L+J[i]*S))
                    q=expit(2*(fields[i+1]+J[i+1]*S+J[i+2]*R))
                    pl=np.array([1-p,p]);pr=np.array([1-q,q]);w=rates[i,:,s,:]
                    mean=np.sum(pl[:,None]*pr[None,:]*w)
                    uleft=np.sqrt(p*(1-p))*((w[1]-w[0])@pr)
                    uright=np.sqrt(q*(1-q))*(pl@(w[:,1]-w[:,0]))
                    uboth=np.sqrt(p*(1-p)*q*(1-q))*(w[1,1]-w[1,0]-w[0,1]+w[0,0])
                    gl=a[i-1,l,s];gr=a[i+1,s,r]
                    val=2*(dleft*uleft**2/gl+dright*uright**2/gr+uboth**2/(gl+gr))/mean
                    maximum=max(maximum,float(val))
    return maximum

def run():
    rng=np.random.default_rng(202611012)
    records=[]
    for n in [3,5,7]:
        for trial in range(5):
            J=rng.uniform(-1.3,1.8,n+1)
            clocks=np.exp(rng.uniform(-2,2,n))
            if trial==4:clocks[1::2]*=1e-5
            modifiers=np.exp(rng.uniform(-1.2,1.2,(n,2,2)))
            rates=np.empty((n,2,2,2))
            for i in range(n):
                for l,L in enumerate(SP):
                    for s,S in enumerate(SP):
                        for r,R in enumerate(SP):
                            rates[i,l,s,r]=clocks[i]*modifiers[i,l,r]*expit(-2*S*(J[i]*L+J[i+1]*R))
            F,KS,U,g,spins=finite_matrices(J,rates);K=F+KS
            P=U@U.T;Q=np.eye(len(g))-P
            A=U.T@KS@U;Ai=pinv_psd(A,1)
            Fi=pinv_psd(F,U.shape[1]);Ki=pinv_psd(K,1)
            B=Q@KS@U
            ev,V=eigh(A);Aih=(V[:,1:]/np.sqrt(ev[1:]))@V[:,1:].T
            T=Aih@B.T@Fi@B@Aih
            theta_exact=max(float(eigh((T+T.T)/2,eigvals_only=True)[-1]),0)
            theta=local_theta(J,rates,True);theta_sup=local_theta(J,rates,False)
            samples=[]
            for st in range(5):
                f=(spins.sum(axis=1)*g if st==0 else rng.normal(size=len(g)))
                f-=g*(g@f)
                if st==1:f=P@f
                if st==2:f=Q@f
                p=U.T@f;q=Q@f
                aa=float(p@Ai@p);bb=float(q@Fi@q);chi=float(f@Ki@f)
                upper=(1+theta)*aa+bb+2*np.sqrt(max(theta*aa*bb,0))
                samples.append(dict(kind=st,a=aa,b=bb,chi=chi,lower=aa,upper=upper,
                    pass_bound=bool(aa<=chi*(1+1e-7) and chi<=upper*(1+1e-7))))
            records.append(dict(n=n,trial=trial,theta_exact=theta_exact,theta_local=theta,
                theta_sup=theta_sup,local_bound_pass=theta_exact<=theta*(1+1e-7),sources=samples))
    out={'scope':'Independent dense symmetrized physical generator; arbitrary disorder, clocks, non-Gaussian multipliers, slow/fast/mixed sources.',
        'all_pass':all(x['local_bound_pass'] and all(y['pass_bound'] for y in x['sources']) for x in records),
        'records':records}
    Path(__file__).with_name('audit_local_schur_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'all_pass':out['all_pass'],'models':len(records),'sources':5*len(records),
        'max_theta_exact_over_bound':max(x['theta_exact']/x['theta_local'] for x in records)},indent=2))

if __name__=='__main__':run()
