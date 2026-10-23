"""One bounded diagnostic on the saved shared basis; floats are proposals only."""
import json, time, sys, resource
from pathlib import Path
import numpy as np
import scipy.linalg as la
from threadpoolctl import threadpool_limits
OWNER=Path(__file__).resolve().parents[2]/'restore_pro2'
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNER/'src'))
from exact_residual import load_exact_generalized, AD, VD
start=time.perf_counter();cpu=time.process_time()
with threadpool_limits(limits=1):
 ai,info=load_exact_generalized(OWNER/'sources')
 with np.load(OWNER/'witnesses/lanczos.npz') as z:
  xi=np.concatenate([v for v in z['basis']],axis=1)
 X=xi.astype(float)/VD
 st=time.perf_counter()
 W,s,Z=la.svd(X,full_matrices=False,check_finite=True,lapack_driver='gesdd')
 svdtime=time.perf_counter()-st
 C=Z.T/s
 Cint=np.rint(C*(2.**32)).astype(np.int64)
 A=ai.astype(float)/AD
 Y=A@W
 G=W.T@W; T=W.T@Y; H=Y.T@Y
 M=info['max_integer_abs_row_sum'];S=int(M)/AD
 x=12983/536870912
 pl=H-(-S+x)*T-S*x*G
 pu=H-(S+x)*T+S*x*G
 evl=la.eigvalsh(pl);evu=la.eigvalsh(pu)
 d=X.shape[1];n=X.shape[0]
 out={'status':'diagnostic only; no floating quantities are certified',
  'n':n,'d':d,'smallest_singular_values':s[-16:].tolist(),
  'largest_singular_value':float(s[0]),'condition':float(s[0]/s[-1]),
  'svd_seconds':svdtime,'preconditioner_max_int':int(np.abs(Cint).max()),
  'preconditioner_denominator':2**32,
  'P_L_neg':int(np.count_nonzero(evl<0)), 'P_U_pos':int(np.count_nonzero(evu>0)),
  'P_L_min_abs_eigenvalue':float(np.min(np.abs(evl))),
  'P_U_min_abs_eigenvalue':float(np.min(np.abs(evu))),
  'cdf_lower_count_proposal':int(np.count_nonzero(evu>=0)),
  'cdf_upper_count_proposal':n-d+int(np.count_nonzero(evl<=0)),
  'pointwise_dimension_floor_count':n-2*d,
  'exact_global_floor_count_if_full_rank_interior':n-d,
  'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
  'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}
 np.savez_compressed(ROOT/'witnesses/common_action_preconditioner.npz',C=Cint)
 (ROOT/'results/common_action_exploration.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
