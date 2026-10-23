"""Exact-source shared-action completion/inertia certificate.

Run: python src/common_action.py --produce [--owner /path/to/old/source]
Replay: python src/common_action.py --replay [--owner /path/to/old/source]
Floating SVD/eigh supply proposals only. All acceptance uses integer/Fraction
products and outward scalar norms. No omitted-complement basis is constructed.
"""
from __future__ import annotations
import argparse, hashlib, json, math, platform, resource, sys, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy
from scipy.sparse import csr_matrix
from threadpoolctl import threadpool_limits, threadpool_info
from exact_matmul import exact_dot

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_OWNER=ROOT.parent/'restore_pro2'
AD=2**32; VD=2**29; CD=2**32; QD=2**40; ZD=VD*CD
X_THRESHOLD=F(12983,536870912)
PINNED={
 'witnesses/lanczos.npz':'e69c119c0cc6ecc3e7cbc9402041c1c606e09eb25e91011040beadedeb2e92b3',
 'results/input_construction.json':'7cde80f10d7a13b8d35d3f5f2a2c9bbb30ed70be7aa57da3fedaa18aaa59f121',
 'sources/bcsstk08.mtx.gz':'5945836beb24009e8a94b58242d9b5c6cfd261117595898149d3fa9c99c084f7',
 'sources/bcsstm08.mtx.gz':'e788b9d4aa072d2de0b15258b4234e54151ddf9f2d4485e4c7ebc5f76855e6a1',
}

def need(p,msg):
 if not p: raise ValueError(msg)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fj(v):return {'numerator':str(v.numerator),'denominator':str(v.denominator)}
def jf(v):return F(int(v['numerator']),int(v['denominator']))
def rss():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
def integer_fit(a):
 lo=min(a.flat,default=0);hi=max(a.flat,default=0)
 need(-(2**63)<=lo and hi<2**63,'int64 construction would overflow')
 return np.asarray(a,dtype=np.int64)
def squares(a):return sum(int(v)*int(v) for v in a.flat)
def array_digest(a):
 need(a.dtype==np.int64,'hash only canonical int64')
 return hashlib.sha256(np.asarray(a,dtype='<i8',order='C').tobytes()).hexdigest()

def sparse_exact(ai,wi):
 """Two/three signed radix sparse products, each with an explicit row bound."""
 need(ai.dtype==np.int64 and wi.dtype==np.int64,'integer sparse action required')
 rowmax=max(sum(abs(int(x)) for x in ai.data[ai.indptr[i]:ai.indptr[i+1]]) for i in range(ai.shape[0]))
 bits=26;mask=(1<<bits)-1
 need(rowmax*mask<2**63,'sparse limb overflow')
 need(int(wi.min())>-(2**63),'signed abs boundary')
 mag=np.abs(wi);sgn=np.where(wi<0,-1,1).astype(np.int64)
 count=(int(mag.max()).bit_length()+bits-1)//bits
 out=np.zeros(wi.shape,dtype=object)
 for j in reversed(range(count)):
  out*=1<<bits
  limb=((mag>>(j*bits))&mask)*sgn
  out+=(ai@limb).astype(object)
 return out,{'limb_bits':bits,'int64_sparse_block_products':count,
             'absolute_partial_sum_bound':str(rowmax*mask)}

def strict_row_bound(ai,Mint):
 """Elementary max-component equality argument on every graph component."""
 n=ai.shape[0];seen=set();components=[]
 for start in range(n):
  if start in seen:continue
  seen.add(start);todo=[start];vertices=[];deficient=[]
  while todo:
   i=todo.pop();vertices.append(i)
   row=sum(abs(int(v)) for v in ai.data[ai.indptr[i]:ai.indptr[i+1]])
   need(row<=Mint,'invalid matrix norm bound')
   if row<Mint:deficient.append(i)
   for j,a in zip(ai.indices[ai.indptr[i]:ai.indptr[i+1]],ai.data[ai.indptr[i]:ai.indptr[i+1]]):
    j=int(j)
    if a and j not in seen:seen.add(j);todo.append(j)
  need(deficient,'support bound is not proved strict')
  components.append({'size':len(vertices),'deficient_row':min(deficient)})
 return {'strict_norm_less_than_M':True,'components':components,'argument':'PROOF.md strict row-sum lemma'}

def main():
 parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
 group.add_argument('--produce',action='store_true');group.add_argument('--replay',action='store_true')
 parser.add_argument('--owner',type=Path,default=DEFAULT_OWNER);args=parser.parse_args()
 owner=args.owner.resolve();sys.path.insert(0,str(owner/'src'))
 from exact_residual import load_exact_generalized,sqrt_hi,sqrt_interval,up,certify_dense
 from scipy.linalg import eigh
 start=time.perf_counter();cpu=time.process_time();stages=[];ops=[]
 def timed(label,fn):
  t=time.perf_counter();c=time.process_time();out=fn()
  stages.append({'stage':label,'wall_seconds':time.perf_counter()-t,'cpu_seconds':time.process_time()-c})
  print(label,round(stages[-1]['wall_seconds'],6),flush=True)
  return out
 for rel,h in PINNED.items():need(sha(owner/rel)==h,'source binding '+rel)
 ai,inp=timed('exact_decimal_input',lambda:load_exact_generalized(owner/'sources'))
 original=json.loads((owner/'results/input_construction.json').read_text())
 for key in ('n','A_denominator','M','tau','input_sha256','scale'):
  need(inp[key]==original[key],'input reconstruction mismatch '+key)
 M=jf(inp['M']);tau=jf(inp['tau']);S=M+tau
 strict=timed('strict_support',lambda:strict_row_bound(ai,int(inp['max_integer_abs_row_sum'])))
 with np.load(owner/'witnesses/lanczos.npz') as z:
  basis=z['basis'];need(basis.dtype==np.int64 and basis.shape==(8,1074,64),'saved basis binding')
  xi=np.concatenate(list(basis),axis=1)
 n,d=xi.shape
 cp=ROOT/'witnesses/common_action_preconditioner.npz'
 need(cp.exists(),'missing frozen SVD preconditioner; run exploration once')
 with np.load(cp,allow_pickle=False) as z:
  ci=z['C'];need(ci.dtype==np.int64 and ci.shape==(d,d),'preconditioner shape/dtype')
 def transform():
  zz,info=exact_dot(xi,ci,return_info=True);ops.append({'operation':'X C',**info})
  return integer_fit(zz)
 zi=timed('exact_coordinate_change',transform)
 shift=ZD//QD;need(shift*QD==ZD,'integer rounding ratio')
 # Nearest integer with ties upward, executed in Python integers.
 wi=integer_fit((zi.astype(object)+shift//2)//shift)
 discrepancy=zi.astype(object)-wi.astype(object)*shift
 delta=sqrt_hi(F(squares(discrepancy),ZD**2))
 def multiply(a,b,name):
  r,info=exact_dot(a,b,return_info=True);ops.append({'operation':name,**info});return r
 gg=timed('exact_Gram',lambda:multiply(wi.T,wi,'W^T W'))
 gm=gg.copy();gm[np.diag_indices(d)]-=QD**2
 gamma=sqrt_hi(F(squares(gm),QD**4))
 need(gamma<1,'rounded change of coordinates not full rank')
 sigma_lo=sqrt_interval(1-gamma)[0]
 need(delta<sigma_lo,'exact coordinate change not full rank')
 wn=sqrt_hi(1+gamma);zn=wn+delta
 yy,sparse_ops=timed('exact_shared_action',lambda:sparse_exact(ai,wi));ops.append({'operation':'Abar W',**sparse_ops})
 tt=timed('exact_cross_action',lambda:multiply(wi.T,yy,'W^T Abar W'))
 hh=timed('exact_action_Gram',lambda:multiply(yy.T,yy,'(Abar W)^T Abar W'))
 need(np.array_equal(tt,tt.T),'joint action is not symmetric')
 need(np.array_equal(gg,gg.T) and np.array_equal(hh,hh.T),'bad Gram symmetry')
 certs={};pinned_matrices={};common={
  'threshold':fj(X_THRESHOLD),'M':fj(M),'tau':fj(tau),'S':fj(S),
  'exact_coordinate_denominator':str(ZD),'rounded_coordinate_denominator':str(QD),
  'gamma_W':fj(gamma),'coordinate_rounding_F':fj(delta),
  'sigma_min_W_lower':fj(sigma_lo),'norm_Z_upper':fj(zn),
  'rank_X':d,'rank_argument':'sigma_min(W)>||Z-W||, Z=X C; hence Z,X,C have full rank',
  'strict_support':strict,
 }
 for label,b in [('lower_operator',-S),('upper_operator',S)]:
  t=X_THRESHOLD
  def make_pencil():
   coeff=[F(1,(AD*QD)**2),-(b+t)/F(AD*QD**2),b*t/F(QD**2)]
   den=math.lcm(*(c.denominator for c in coeff))
   integers=[c.numerator*(den//c.denominator) for c in coeff]
   numer=hh*integers[0]+tt*integers[1]+gg*integers[2]
   need(den%AD==0,'pencil quantization denominator')
   q=den//AD
   pi=integer_fit((numer+q//2)//q)
   need(np.array_equal(pi,pi.T),'rounded pencil not symmetric')
   residual=numer-pi.astype(object)*q
   rounding=sqrt_hi(F(squares(residual),den**2))
   source=up(zn**2*tau*(2*M+tau+abs(b+t)))
   coordinate=up(delta*(2*wn+delta)*(M+abs(b))*(M+abs(t)))
   budget=up(rounding+source+coordinate)
   return pi,{'compressed_rounding_F':fj(rounding),'exact_input_allowance':fj(source),
     'coordinate_allowance':fj(coordinate),'total_pencil_allowance':fj(budget)}
  pi,bud=timed(label+'_pencil',make_pencil)
  pinned_matrices[label]=array_digest(pi)
  witness=ROOT/'witnesses'/('inertia_'+label+'.npz')
  if args.produce:
   need(not witness.exists(),'refusing to overwrite frozen eigenproposal '+label)
   def propose():
    ev,ve=eigh(pi.astype(float)/AD,driver='evd',check_finite=True)
    return np.rint(ve*VD).astype(np.int64),np.rint(ev*AD).astype(np.int64)
   vv,dd=timed(label+'_eigenproposal',propose)
   np.savez_compressed(witness,basis=vv,diagonal=dd)
  else:
   with np.load(witness,allow_pickle=False) as z:vv,dd=z['basis'],z['diagonal']
  def verify():
   result=certify_dense(csr_matrix(pi),vv,dd,jf(bud['total_pencil_allowance']))
   e=jf(result['operator_error'])
   negative=sum(F(int(v),AD)+e<0 for v in dd)
   positive=sum(F(int(v),AD)-e>0 for v in dd)
   need(negative+positive==d,'inertia unresolved at given budgets; no automatic precision sweep')
   margin=min(abs(F(int(v),AD))-e for v in dd)
   return {'negative':negative,'zero':0,'positive':positive,'sign_margin':fj(margin),
    'numeric_certificate':result,'error_components':bud,
    'pencil_int_sha256':array_digest(pi),'witness_sha256':sha(witness)}
  certs[label]=timed(label+'_verification',verify)
 lo=certs['upper_operator']['positive'];hi=n-d+certs['lower_operator']['negative']
 need(hi-lo==n-d,'pointwise ambiguity did not attain global bound')
 result={'PASS':True,'mode':'producer' if args.produce else 'replay',
  'contract':'All real symmetric B with B X=A X for all512 saved basis columns of X and -(M+tau)I<=B<=(M+tau)I; A is exact-decimal original generalized matrix.',
  'source_hashes':PINNED,'preconditioner_sha256':sha(cp),'preconditioner_array_sha256':array_digest(ci),
  'n':n,'d':d,'common':common,'inertias':certs,
  'inclusive_CDF_count_minimum':lo,'inclusive_CDF_count_maximum':hi,
  'inclusive_CDF_minimum':fj(F(lo,n)),'inclusive_CDF_maximum':fj(F(hi,n)),
  'exact_pointwise_ambiguity':fj(F(hi-lo,n)),
  'exact_all_threshold_maximum_ambiguity':fj(F(n-d,n)),
  'no_threshold_eigenvalue':True,'no_random_draws':True,'new_Krylov_steps':0,
  'exact_sparse_actions_columns':d,'arithmetic_operations':ops,'stages':stages,
  'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
  'peak_rss_bytes':rss(),'python':platform.python_version(),'numpy':np.__version__,
  'scipy':scipy.__version__,'threads':threadpool_info(),
  'cost_exclusions':'Prior SVD exploration, original checkpoint construction, proof/research/authoring, independent challenges, packaging and service/model costs are separately charged; this is not all-in programme cost.'}
 path=ROOT/'results'/('common_action_producer.json' if args.produce else 'common_action_replay.json')
 if args.replay:
  expected=json.loads((ROOT/'results/common_action_producer.json').read_text())
  for key in ('n','d','source_hashes','preconditioner_sha256','common','inclusive_CDF_count_minimum','inclusive_CDF_count_maximum','exact_pointwise_ambiguity','exact_all_threshold_maximum_ambiguity'):
   need(result[key]==expected[key],'replay differs: '+key)
  for label in certs:
   for key in ('negative','zero','positive','sign_margin','error_components','pencil_int_sha256','witness_sha256'):
    need(certs[label][key]==expected['inertias'][label][key],'replay certificate differs')
 path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'PASS':True,'minimum_count':lo,'maximum_count':hi,'width':float(F(hi-lo,n)),
  'wall_seconds':result['wall_seconds'],'cpu_seconds':result['cpu_seconds'],'peak_rss_bytes':rss()},indent=2),flush=True)

if __name__=='__main__':
 with threadpool_limits(limits=1):main()
