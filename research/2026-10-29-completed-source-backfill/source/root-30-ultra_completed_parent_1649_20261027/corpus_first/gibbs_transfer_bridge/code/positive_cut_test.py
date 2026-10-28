"""Actual tensor-cut compression test: support certificates plus scaled SVD diagnostics."""
import sys
sys.dont_write_bytecode=True
import numpy as np,json,time
from pathlib import Path
from scipy.linalg import svdvals
from positive_gate import BASE

def fooling_set(M,seed,restarts=100):
 rng=np.random.default_rng(seed);support=M>0;locations=np.argwhere(support);best=[]
 # A nonnegative rectangle cannot cover two selected entries if at least one
 # cross entry is zero. Every found set is independently replayed below.
 for repeat in range(restarts):
  order=rng.permutation(len(locations));chosen=[]
  for index in order:
   i,j=map(int,locations[index])
   if all(not(support[i,b] and support[a,j]) for a,b in chosen):chosen.append((i,j))
  if len(chosen)>len(best):best=chosen
 for i,j in best:assert support[i,j]
 for k,(i,j) in enumerate(best):
  assert all(not(support[i,b] and support[a,j]) for a,b in best[k+1:])
 return best

def run():
 t=time.monotonic();C=np.load(BASE/'results/positive_local_delta001.npz')['C'].reshape(9,9,25,25)
 records=[]
 for cut,perm in [('x_a_z_b',(0,2,1,3)),('x_b_z_a',(0,3,1,2))]:
  M=C.transpose(perm).reshape(225,225);balance=M.copy();r=np.ones(225);c=np.ones(225)
  for _ in range(30):
   rr=np.max(balance,axis=1);rr[rr==0]=1;balance/=rr[:,None];r/=rr
   cc=np.max(balance,axis=0);cc[cc==0]=1;balance/=cc[None,:];c/=cc
  s=svdvals(balance);norm=np.linalg.norm(s)
  found=fooling_set(M,917,100)
  # Uniform relative entrywise error implies the same Frobenius-relative
  # error after any positive row/column scaling. Eckart-Young is diagnostic
  # here because SVD has not been interval-certified.
  tails={str(k):float(np.linalg.norm(s[k:])/norm) for k in (9,16,25,32,48,64,81,100,128,160,200)}
  records.append(dict(cut=cut,shape=list(M.shape),support_nonzeros=int(np.count_nonzero(M)),
   fooling_set_size=len(found),fooling_set=found,
   positive_rank_lower_bound_for_any_entrywise_relative_error_below_one=len(found),
   balanced_svd_relative_tail_diagnostics=tails,
   singular_values=s.tolist()))
  print(cut,'support-certified lower bound',len(found),'rank32 balanced tail',tails['32'],flush=True)
 result=dict(delta=.001,records=records,
  target_logZ_error=.001,target_L=128,target_beta=64,
  source_quad_slices=2387589,
  per_local_tensor_relative_budget=.001/(128*2387589),
  interpretation='Fooling sets certify support-preserving positive factor rank. Scaled SVD tails are diagnostics only. Neither proves a no-go for trace-specific, signed, or absolute-error compression.',elapsed_seconds=time.monotonic()-t)
 (BASE/'results/POSITIVE_CUT_TEST.json').write_text(json.dumps(result,indent=2)+'\n')
 print('elapsed',result['elapsed_seconds'])

if __name__=='__main__':run()
