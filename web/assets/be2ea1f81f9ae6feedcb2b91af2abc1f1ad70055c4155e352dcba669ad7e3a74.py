"""Ridge-volume constrained sampling experiments.

Research implementation, NOT a certified finite-time FPRAS.
All production kernels have the stated invariant measure in exact arithmetic.
The adaptive calibration is frozen before collecting production samples.
Floating-point determinant evaluation is not interval certified.
"""
from __future__ import annotations
import math
import numpy as np
from numba import njit

@njit(cache=True)
def log_volume(G, mask, beta):
    n=G.shape[0]//2
    ix=np.empty(n,np.int64); j=0
    for k in range(2*n):
        if (mask>>k)&1:
            if j>=n: return -np.inf
            ix[j]=k; j+=1
    if j!=n: return -np.inf
    K=np.empty((n,n))
    for i in range(n):
        for j in range(n): K[i,j]=beta*G[ix[i],ix[j]]+(1.0 if i==j else 0.0)
    sign,ld=np.linalg.slogdet(K)
    if sign<=0: return -np.inf
    return ld

@njit(cache=True)
def mask_from_bits(bits,n):
    mask=0
    for i in range(n): mask|=1<<(2*i+((bits>>i)&1))
    return mask

@njit(cache=True)
def bits_from_mask(mask,n):
    bits=0
    for i in range(n):
        if (mask>>(2*i+1))&1: bits |=1<<i
    return bits

@njit(cache=True)
def state_type(mask,n):
    h=-1; d=-1
    for i in range(n):
        c=((mask>>(2*i))&1)+((mask>>(2*i+1))&1)
        if c==0:
            if h>=0: return -1
            h=i
        elif c==2:
            if d>=0: return -1
            d=i
    if h<0 and d<0: return 0
    if h<0 or d<0: return -1
    return 1+h*n+d

@njit(cache=True)
def propose_valid(mask,n,typ):
    if typ==0:
        i=np.random.randint(n); j=np.random.randint(n)
        a=2*i+(0 if (mask>>(2*i))&1 else 1)
        b=2*j+(1 if (mask>>(2*j))&1 else 0)
        return mask ^ (1<<a) ^ (1<<b), n*n
    h=(typ-1)//n; d=(typ-1)%n
    singles=np.empty(n-2,np.int64); k=0
    for i in range(n):
        if i!=h and i!=d: singles[k]=i; k+=1
    r=np.random.randint(5*n-6)
    if r<n-2:
        i=singles[r]
        return mask ^ (3<<(2*i)),5*n-6
    r-=n-2
    if r<4:
        a=2*d+(r//2); b=2*h+(r%2)
    else:
        r-=4
        if r<2*(n-2):
            i=singles[r//2]; a=2*d+(r%2)
            b=2*i+(1 if (mask>>(2*i))&1 else 0)
        else:
            r-=2*(n-2); i=singles[r//2]
            a=2*i+(0 if (mask>>(2*i))&1 else 1); b=2*h+(r%2)
    return mask ^ (1<<a) ^ (1<<b),5*n-6

@njit(cache=True)
def worm_run(G,beta,steps,seed,logmult,mask=-1,calibrate=False,target_mass=0.5,gain=0.1):
    """Return target visits, frozen parameters/state, and work counters.
    Calibration uses stochastic approximation, not exact type partition sums.
    """
    np.random.seed(seed); n=G.shape[0]//2
    if mask<0: mask=mask_from_bits(0,n)
    typ=state_type(mask,n); ld=log_volume(G,mask,beta)
    out=np.empty(steps,np.int64); count=0; accepts=0; evaluations=1
    lm=logmult.copy(); counts=np.zeros(n*n+1,np.int64)
    for it in range(steps):
        if np.random.random()<0.5:
            proposal,degree=propose_valid(mask,n,typ)
            nt=state_type(proposal,n)
            nd=n*n if nt==0 else 5*n-6
            nld=log_volume(G,proposal,beta); evaluations+=1
            loga=nld-ld+lm[nt]-lm[typ]+math.log(degree/nd)
            if math.log(np.random.random())<min(0.0,loga):
                mask=proposal; ld=nld; typ=nt; accepts+=1
        counts[typ]+=1
        if calibrate:
            gamma=gain/((1.0+it/2000.0)**0.6)
            pd=(1.0-target_mass)/(n*(n-1))
            common=gamma*(pd-target_mass+(1.0 if typ==0 else 0.0))
            for i in range(n):
                for j in range(n):
                    if i!=j: lm[1+i*n+j]+=common
            if typ!=0: lm[typ]-=gamma
        elif typ==0:
            out[count]=bits_from_mask(mask,n); count+=1
    return out[:count],lm,mask,counts,accepts,evaluations

@njit(cache=True)
def target_run(G,beta,steps,seed,method=0,bits=0):
    """method 0: one-pair Gibbs; 1: two-pair Gibbs; 2: Gibbs plus multiscale flips."""
    np.random.seed(seed); n=G.shape[0]//2
    ld=log_volume(G,mask_from_bits(bits,n),beta)
    out=np.empty(steps,np.int64); evaluations=1
    for it in range(steps):
        if method==2 and np.random.random()<0.25:
            k=1+np.random.randint(n)
            ids=np.random.permutation(n)
            nb=bits
            for j in range(k): nb^=1<<ids[j]
            nl=log_volume(G,mask_from_bits(nb,n),beta); evaluations+=1
            if math.log(np.random.random())<min(0.,nl-ld): bits=nb; ld=nl
        elif method==1:
            i=np.random.randint(n); j=np.random.randint(n-1)
            if j>=i: j+=1
            base=bits & ~(1<<i) & ~(1<<j)
            vals=np.empty(4); opts=np.empty(4,np.int64)
            for k in range(4):
                opts[k]=base | ((k&1)<<i) | (((k>>1)&1)<<j)
                vals[k]=log_volume(G,mask_from_bits(opts[k],n),beta)
            evaluations+=4
            mx=np.max(vals); probs=np.exp(vals-mx); r=np.random.random()*np.sum(probs)
            acc=0.; choice=3
            for k in range(4):
                acc+=probs[k]
                if r<acc: choice=k; break
            bits=opts[choice]; ld=vals[choice]
        else:
            i=np.random.randint(n); nb=bits ^ (1<<i)
            nl=log_volume(G,mask_from_bits(nb,n),beta); evaluations+=1
            diff=nl-ld
            p=1/(1+math.exp(-min(700.,max(-700.,diff))))
            if np.random.random()<p: bits=nb; ld=nl
        out[it]=bits
    return out,bits,evaluations

@njit(cache=True)
def tempering_run(G,beta,sweeps,seed,temps,bits0=0):
    """Replica exchange using powers of target determinant, single-pair Gibbs.
    Includes ALL replica determinant evaluations in the work counter.
    """
    np.random.seed(seed); n=G.shape[0]//2; r=len(temps)
    bits=np.full(r,bits0,np.int64); logw=np.empty(r)
    for j in range(r): logw[j]=log_volume(G,mask_from_bits(bits[j],n),beta)
    out=np.empty(sweeps,np.int64); evaluations=r; swaps=0
    for it in range(sweeps):
        for j in range(r):
            i=np.random.randint(n); nb=bits[j] ^ (1<<i)
            nl=log_volume(G,mask_from_bits(nb,n),beta); evaluations+=1
            diff=temps[j]*(nl-logw[j]); diff=min(700.,max(-700.,diff))
            if np.random.random()<1/(1+math.exp(-diff)): bits[j]=nb; logw[j]=nl
        for j in range(it%2,r-1,2):
            loga=(temps[j]-temps[j+1])*(logw[j+1]-logw[j])
            if math.log(np.random.random())<min(0.,loga):
                b=bits[j]; bits[j]=bits[j+1]; bits[j+1]=b
                l=logw[j]; logw[j]=logw[j+1]; logw[j+1]=l; swaps+=1
        out[it]=bits[-1]
    return out,bits[-1],evaluations,swaps

@njit(cache=True)
def enumerate_target(G,beta):
    n=G.shape[0]//2; logs=np.empty(1<<n)
    for i in range(1<<n): logs[i]=log_volume(G,mask_from_bits(i,n),beta)
    mx=np.max(logs); p=np.exp(logs-mx); z=np.sum(p)
    return p/z,mx+np.log(z),logs

def validate_gram(G:np.ndarray,beta:float)->np.ndarray:
    G=np.asarray(G,dtype=np.float64)
    if G.ndim!=2 or G.shape[0]!=G.shape[1] or G.shape[0]%2:
        raise ValueError('G must be a square 2n-by-2n matrix')
    if not 2<=G.shape[0]//2<=30: raise ValueError('This implementation supports 2 <= n <= 30')
    if not np.all(np.isfinite(G)) or not np.allclose(G,G.T,rtol=1e-12,atol=1e-12):
        raise ValueError('G must be finite and symmetric')
    if not np.isfinite(beta) or beta<0: raise ValueError('beta must be finite and nonnegative')
    if np.linalg.eigvalsh(G)[0]<-1e-10*max(1.,np.linalg.norm(G,2)):
        raise ValueError('G must be positive semidefinite')
    return np.ascontiguousarray(G)

def calibrate_worm(G,beta,steps=100000,seed=1,target_mass=0.5):
    G=validate_gram(G,beta); n=G.shape[0]//2
    if steps<100: raise ValueError('Calibration budget is too small')
    lm=np.zeros(n*n+1)
    for i in range(n):
        for j in range(n):
            if i!=j: lm[1+i*n+j]=math.log(4*(1-target_mass)/(target_mass*n*(n-1)))
    levels=np.concatenate([np.geomspace(max(beta*1e-4,1e-12),max(beta,1e-12),6),[beta]])
    budgets=[steps//12]*6+[steps-6*(steps//12)]
    mask=-1; evals=0; diagnostics=[]
    for j,(b,t) in enumerate(zip(levels,budgets)):
        _,lm,mask,counts,acc,ev=worm_run(G,float(b),int(t),seed+j*7919,lm,mask,True,target_mass,0.12)
        evals+=ev; diagnostics.append(dict(beta=float(b),steps=int(t),target_fraction=float(counts[0]/t)))
    return lm,mask,evals,diagnostics
