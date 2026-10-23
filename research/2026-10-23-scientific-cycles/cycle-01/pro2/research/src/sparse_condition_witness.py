"""One certified lower bound on noise amplification for the saved nine directions.

The SVD supplies a sparse symmetric perturbation proposal. The delivered lower
bound uses only its exact dyadic coefficients, exact probe products and Rayleigh
quotient. This does not assert spectral-count ambiguity at a fixed threshold.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json, sys, time, resource
import numpy as np
from scipy.linalg import svd, eigh
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];OWNER=ROOT.parent/'restore_pro2'
sys.path.insert(0,str(OWNER/'src'))
from exact_residual import read_mm_exact,sqrt_hi,fj
VD=2**29;DD=2**40;WD=2**29

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');a=p.parse_args()
 st=time.perf_counter();cpu=time.process_time()
 need=lambda test,msg: None if test else (_ for _ in ()).throw(ValueError(msg))
 kh='5945836beb24009e8a94b58242d9b5c6cfd261117595898149d3fa9c99c084f7'
 xh='e69c119c0cc6ecc3e7cbc9402041c1c606e09eb25e91011040beadedeb2e92b3'
 need(sha(OWNER/'sources/bcsstk08.mtx.gz')==kh,'K source hash')
 need(sha(OWNER/'witnesses/lanczos.npz')==xh,'probe source hash')
 n,ke=read_mm_exact(OWNER/'sources/bcsstk08.mtx.gz')
 core=json.loads((ROOT/'results/eight_probe_core_preliminary.json').read_text())['core_vertices']
 loc={v:i for i,v in enumerate(core)};h=len(core)
 pairs=sorted((min(loc[i],loc[j]),max(loc[i],loc[j])) for i,j in ke if i in loc and j in loc)
 need(len(set(pairs))==len(pairs),'duplicate symmetric coefficient')
 with np.load(OWNER/'witnesses/lanczos.npz',allow_pickle=False) as z:
  b=z['basis'];xi=np.stack([b[ell,:,0] for ell in range(8)]+[b[0,:,1]],axis=1)[core,:]
 need(xi.dtype==np.int64 and xi.shape==(84,9),'expected actual support/query block')
 witness=ROOT/'witnesses/sparse_noise_direction.npz'
 proposal_seconds=0.
 if not a.replay:
  need(not witness.exists(),'refusing overwrite of frozen condition witness')
  ts=time.perf_counter();xf=xi.astype(float)/VD
  op=np.zeros((h*9,len(pairs)))
  for c,(i,j) in enumerate(pairs):
   w=1. if i==j else 1/np.sqrt(2.)
   op[i*9:(i+1)*9,c]+=w*xf[j]
   if i!=j:op[j*9:(j+1)*9,c]+=w*xf[i]
  _,s,v=svd(op,full_matrices=False,check_finite=True,lapack_driver='gesdd')
  di=np.zeros((h,h),dtype=np.int64)
  for val,(i,j) in zip(v[-1],pairs):
   q=int(np.rint(val*(1. if i==j else 1/np.sqrt(2.))*DD))
   di[i,j]=di[j,i]=q
  ev,ve=eigh(di.astype(float)/DD,check_finite=True)
  wi=np.rint(ve[:,np.argmax(np.abs(ev))]*WD).astype(np.int64)
  proposal_seconds=time.perf_counter()-ts
  np.savez_compressed(witness,perturbation=di,rayleigh_vector=wi)
  diagnostic={'smallest_singular_value':float(s[-1]),'largest_singular_value':float(s[0]),
    'SVD_condition_estimate':float(s[0]/s[-1]),'proposal_seconds':proposal_seconds,
    'status':'proposal diagnostic only; acceptance below uses exact arithmetic'}
  (ROOT/'results/sparse_condition_diagnostic.json').write_text(json.dumps(diagnostic,indent=2)+'\n')
 else:
  with np.load(witness,allow_pickle=False) as z:di=z['perturbation'];wi=z['rayleigh_vector']
 need(di.dtype==np.int64 and di.shape==(h,h) and np.array_equal(di,di.T),'symmetric integer perturbation')
 need(wi.dtype==np.int64 and wi.shape==(h,),'integer Rayleigh vector')
 allowed=set(pairs)|{(j,i) for i,j in pairs}
 need(all(not di[i,j] or (i,j) in allowed for i in range(h) for j in range(h)),'offpattern perturbation')
 # All products below use Python arbitrary precision, no int64 multiplication.
 residual=np.zeros((h,9),dtype=object)
 for i,j in allowed:
  if di[i,j]:
   for ell in range(9):residual[i,ell]+=int(di[i,j])*int(xi[j,ell])
 res2=F(sum(int(x)*int(x) for x in residual.flat),(DD*VD)**2)
 need(res2>0,'nonzero measured residual required')
 residual_hi=sqrt_hi(res2)
 wn2=sum(int(x)*int(x) for x in wi)
 need(wn2>0,'zero Rayleigh vector')
 numerator=sum(int(wi[i])*int(di[i,j])*int(wi[j]) for i,j in allowed)
 operator_lo=abs(F(numerator,DD*wn2))
 need(operator_lo>0,'zero perturbation Rayleigh value')
 normF2=F(sum(int(x)*int(x) for x in di.flat),DD**2)
 amplification=operator_lo/residual_hi
 out={'PASS':True,'mode':'replay' if a.replay else 'producer',
  'contract':'Symmetric original-support perturbations D; residual measured by ||D X9||_F and operator error by ||D||_2. X9 contains8saved starting columns and ell0 depth1; no new directions.',
  'core_vertices':core,'independent_symmetric_coefficients':len(pairs),
  'source_sha256':{'K':kh,'lanczos':xh},'witness_sha256':sha(witness),
  'probe_denominator':VD,'perturbation_denominator':DD,'Rayleigh_denominator':WD,
  'perturbation_Frobenius_norm_squared':fj(normF2),
  'action_Frobenius_norm_squared':fj(res2),'action_Frobenius_norm_upper':fj(residual_hi),
  'operator_norm_lower':fj(operator_lo),'operator_per_action_norm_amplification_lower':fj(amplification),
  'proposal_seconds':proposal_seconds,'wall_seconds':time.perf_counter()-st,
  'cpu_seconds':time.process_time()-cpu,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
  'not_claimed':['upper bound on recovery conditioning','spectral count ambiguity at x','full sparse reconstruction','advantage over verified dense input computation']}
 if a.replay:
  old=json.loads((ROOT/'results/sparse_condition_producer.json').read_text())
  for k in ['core_vertices','source_sha256','witness_sha256','perturbation_Frobenius_norm_squared','action_Frobenius_norm_squared','action_Frobenius_norm_upper','operator_norm_lower','operator_per_action_norm_amplification_lower']:
   need(out[k]==old[k],'replay mismatch '+k)
 path=ROOT/'results'/('sparse_condition_replay.json' if a.replay else 'sparse_condition_producer.json')
 path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'PASS':True,'action_norm_upper':float(residual_hi),'operator_norm_lower':float(operator_lo),
 'amplification_lower':float(amplification),'wall_seconds':out['wall_seconds'],'proposal_seconds':proposal_seconds},indent=2))
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
