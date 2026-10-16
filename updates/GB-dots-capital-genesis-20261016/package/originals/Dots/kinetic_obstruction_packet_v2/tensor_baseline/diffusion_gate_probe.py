"""Actual cap-162 isolated diffusion gate. No full evolution/certificate."""
import json,time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply
from scipy.stats import binom

def block(total, stop=False):
    lo=max(0,total-162); hi=min(162,total); n=np.arange(lo,hi+1)
    H=diags([8.2207*(total-n[:-1]), -8.2207*total*np.ones(len(n)), 8.2207*n[1:]],[-1,0,1],shape=(len(n),len(n)),format='csc')
    if stop:
        frozen=(n<=15)&(total-n<=15)
        H=H@diags((~frozen).astype(float))
    return n,H

records=[]
n,H=block(100); v=np.zeros(len(n));v[50-n[0]]=1
for h in [1e-5,1e-4,1e-3,1e-2,1e-1]:
    t=time.perf_counter();p=expm_multiply(h*H,v);elapsed=time.perf_counter()-t
    # Full 163x163 gate output is anti-diagonal, so singular values are abs(p).
    sv=np.sort(np.abs(p))[::-1]; ranks={}; l1ranks={}
    same=(1+np.exp(-2*8.2207*h))/2
    oracle=np.convolve(binom.pmf(np.arange(51),50,same),binom.pmf(np.arange(51),50,1-same))
    for tol in [1e-8,1e-10,1e-12]:
        for rank in range(1,len(sv)+1):
            if np.linalg.norm(sv[rank:])<=tol: ranks[str(tol)]=rank;break
        for rank in range(1,len(sv)+1):
            if sv[rank:].sum()<=tol: l1ranks[str(tol)]=rank;break
    records.append(dict(h=h,block_size=len(n),mass=float(p.sum()),min_p=float(p.min()),
                        retained_ranks_absolute_l2=ranks,retained_ranks_l1_mass=l1ranks,
                        tails_at_l2_rank_1e10=dict(rank=ranks["1e-10"],l1=float(sv[ranks["1e-10"]:].sum()),l2=float(np.linalg.norm(sv[ranks["1e-10"]:]))),
                        independent_binomial_check=dict(max_entry_error=float(np.max(np.abs(p-oracle))),l1_error=float(np.abs(p-oracle).sum()),oracle_mass=float(oracle.sum())),seconds=elapsed))
n,H=block(324);out=expm_multiply(.0001*H,np.ones(1))[0]
print(json.dumps(dict(cap=162,local_dim=163,initial_pair=[50,50],
    environment='isolated diffusion subflow only',full_evolution=False,rigorous_certificate=False,
    probes=records,overflow_check=dict(initial_pair=[162,162],h=.0001,
        computed_mass=float(out),analytic_mass=float(np.exp(-8.2207*324*.0001)))),indent=2))
