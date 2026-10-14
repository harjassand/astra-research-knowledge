from fractions import Fraction as F
import os,time,json
import numpy as np
from tt_ops import *
from model import *


def inverse_reference(c,rhs,rank,sweeps=2):
    b=transform(rhs,[U.T for U in c.evecs]);v=solve_sum_diagonal(c.evals,b,rank,sweeps)
    return rounded(transform(v,c.evecs),rank,1e-14)

def solve(c,rank=8,iterations=14,sweeps=2,source=None,verbose=False):
    source=c.source if source is None else source
    omega=2/(1+float(c.R));v=scale(inverse_reference(c,source,rank,sweeps),omega);log=[]
    for it in range(iterations+1):
        Av=apply_terms(c.terms,v,rank=max(rank*2,24),tol=1e-15)
        r=rounded(add(source,scale(Av,-1)),max(rank*2,24),1e-15)
        nrm=inner(r,r);ev=inner(v,Av);bv=inner(source,v);lo=2*bv-ev
        # Floating diagnostic ONLY. The independent rational verifier provides the certificate.
        alpha=min(x.min() for x in c.evals if x.min()>0)
        hi=lo+nrm/alpha
        rec={'iteration':it,'lower_float':lo/float(c.Z),'upper_float':hi/float(c.Z),'ratio_float':hi/lo if lo>0 else None,'residual_sq_float':nrm,'coefficients':sum(x.size for x in v),'max_rank':max(x.shape[2] for x in v)};log.append(rec)
        if verbose:print(rec,flush=True)
        if it==iterations:break
        z=inverse_reference(c,r,rank,sweeps);v=rounded(add(v,scale(z,omega)),rank,1e-14)
    return v,log

if __name__=='__main__':
    t=time.perf_counter();truth=fixture(B=3,m=4,rarity=1);learn,trans=acquire(truth);groups=partition(learn);c=Compiler(learn,groups)
    print('groups',groups,'R',c.R,'terms',len(c.terms),'Z',float(c.Z),'evals',[l[:4].tolist() for l in c.evals],flush=True)
    v,log=solve(c,rank=8,iterations=8,verbose=True)
    print('seconds',time.perf_counter()-t)
    np.savez('/mnt/data/astra_unknown_slow/pilot_witness.npz',**{str(i):a for i,a in enumerate(v)})
    open('/mnt/data/astra_unknown_slow/pilot.json','w').write(json.dumps(log,indent=2))

def pcg_tensor(c,rank=8,iterations=8,sweeps=2,source=None,verbose=False,target_ratio=None):
    """Standard truncated preconditioned CG comparator; not a new CG algorithm.
    Ranks/rounding can break exact conjugacy. Final certification is independent.
    """
    source=c.source if source is None else source
    x=scale(source,0);r=source;z=inverse_reference(c,r,rank,sweeps);p=z;rz=inner(r,z);log=[]
    for it in range(iterations):
        ap=apply_terms(c.terms,p,max(2*rank,24),1e-15);den=inner(p,ap)
        if den<=0 or rz<=0:break
        step=rz/den;x=rounded(add(x,scale(p,step)),rank,1e-14)
        ax=apply_terms(c.terms,x,max(2*rank,24),1e-15);r=rounded(add(source,scale(ax,-1)),max(2*rank,24),1e-15)
        lo=2*inner(source,x)-inner(x,ax);rr=inner(r,r);alpha=min(v.min() for v in c.evals if v.min()>0)
        hi=lo+rr/alpha;rec={'iteration':it+1,'lower_float':lo/float(c.Z),'upper_float':hi/float(c.Z),'ratio_float':hi/lo if lo>0 else None,'residual_sq_float':rr,'coefficients':sum(a.size for a in x)};log.append(rec)
        if verbose:print(rec,flush=True)
        if target_ratio is not None and lo>0 and hi/lo<=target_ratio:break
        z=inverse_reference(c,r,rank,sweeps);newrz=inner(r,z)
        if newrz<=0:break
        p=rounded(add(z,scale(p,newrz/rz)),rank,1e-14);rz=newrz
    return x,log
