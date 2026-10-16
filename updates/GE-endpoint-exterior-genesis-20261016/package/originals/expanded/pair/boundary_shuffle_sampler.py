"""Own implementation of standard conditional-uniform boundary averaging.
Chosen six-vertex path: rates [1,10,100,1000,10000], horizon1.
Fast block {2,3,4,5}; retain {0,1} and boundary attempts at rates1,10.
Sampling is an approximate endpoint of the original process, not its trajectory.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import itertools,json,time,math
import numpy as np
from scipy.linalg import eigh
from scipy.stats import chi2
from pathlib import Path
OUT=Path(__file__).resolve().parent

def sample(n_samples,seed=727,initial=(0,1,2,3,4,5)):
    rng=np.random.default_rng(seed)
    x=np.tile(np.asarray(initial,dtype=np.int64),(n_samples,1))
    counts=rng.poisson(11,size=n_samples)
    for j in range(int(counts.max(initial=0))):
        ids=np.flatnonzero(counts>j)
        boundary=rng.integers(11,size=len(ids))!=0 # rates 10 versus1 exactly
        ids0=ids[~boundary];v=x[ids0,0].copy();x[ids0,0]=x[ids0,1];x[ids0,1]=v
        ids1=ids[boundary]
        # A uniform label from the block is the label at its uniformly shuffled port.
        # Keep a lazy internal order; it is unobservable until the final shuffle.
        positions=rng.integers(2,6,size=len(ids1));v=x[ids1,1].copy()
        x[ids1,1]=x[ids1,positions];x[ids1,positions]=v
    # Exact Fisher-Yates shuffle of the retained block, preserving its full label set.
    ids=np.arange(n_samples)
    for pos in range(5,2,-1):
        j=rng.integers(2,pos+1,size=n_samples);v=x[:,pos].copy();x[:,pos]=x[ids,j];x[ids,j]=v
    return x,counts

def exact_averaged():
    # Quotient states are the two ordered labels at vertices0,1, hence30 states.
    small=list(itertools.permutations(range(6),2));idx={s:i for i,s in enumerate(small)}
    L=np.zeros((30,30))
    for i,(a,b) in enumerate(small):
        L[i,i]+=1;L[i,idx[(b,a)]]-=1
        for c in range(6):
            if c not in (a,b):L[i,i]+=2.5;L[i,idx[(a,c)]]-=2.5
    lam,V=eigh(L);p=V@(np.exp(-np.maximum(lam,0))*V[idx[(0,1)],:])
    full=list(itertools.permutations(range(6)))
    return full,np.array([p[idx[s[:2]]]/24 for s in full])

def validate(N=200000):
    t=time.perf_counter();x,c=sample(N);seconds=time.perf_counter()-t
    full,p=exact_averaged();idx={s:i for i,s in enumerate(full)}
    counts=np.bincount(np.fromiter((idx[tuple(s)] for s in x),dtype=np.int64,count=N),minlength=720)
    expected=N*p;common=expected>=5
    obs=np.r_[counts[common],counts[~common].sum()];ex=np.r_[expected[common],expected[~common].sum()]
    valid=ex>0;stat=float(((obs[valid]-ex[valid])**2/ex[valid]).sum());df=int(valid.sum()-1)
    own=np.load(OUT/'graded_path_generators.npz')['p']
    files=[str(f.name) for f in OUT.glob('graded_path*')]
    result=dict(sample_count=N,seed=727,seconds=seconds,mean_boundary_attempts=float(c.mean()),expected_boundary_attempts=11,expected_original_attempts=11111,all_labels_conserved=bool(np.all(np.sort(x,axis=1)==np.arange(6))),empirical_TV_to_exact_averaged=float(.5*abs(counts/N-p).sum()),chi_square_statistic=stat,chi_square_df=df,chi_square_pvalue=float(chi2.sf(stat,df)),quotient_states=30,full_states=720,exact_averaged_mass_defect=float(abs(p.sum()-1)),nearby_files=files)
    np.save(OUT/'boundary_shuffle_exact_endpoint.npy',p)
    if own is not None:result['exact_averaged_TV_to_original']=float(.5*abs(p-own).sum())
    print(json.dumps(result),flush=True);(OUT/'boundary_shuffle_sampler_results.json').write_text(json.dumps(result,indent=2))

if __name__=='__main__':validate()
