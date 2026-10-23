"""Small independent finite checks + linear-size reservoir cost illustrations.
Universal statements are proved analytically in PROOF.txt; no convex-roof solver.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import json,math,time,resource,sys,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def entropy(p):
 p=np.asarray(p,dtype=float);p=p[p>0];return float(-np.dot(p,np.log(p)))
def bell_prefix(X,D,i):
 n=X.shape[0];L=D**i;R=n//L;a=X.reshape(L,R,L,R)
 contracted=np.einsum('aras->rs',a)/math.sqrt(L)
 return float(np.vdot(contracted,contracted).real)
def spectral_prefix(X,D,N):
 roots=np.linalg.svd(X,compute_uv=False)
 return np.array([np.sum(roots.reshape(-1,D**i).sum(1)**2)/(D**i) for i in range(1,N+1)]),entropy(roots**2)
def run():
 start=time.perf_counter();cpu=time.process_time();rng=np.random.default_rng(20261021);cases=[];worst=-1e100;exactmax=0.
 for D,N in [(2,n) for n in range(1,7)]+[(3,n) for n in range(1,4)]:
  n=D**N;C=(2 if D==2 else 2*D)-math.log(D)
  matrices=[]
  for z in range(8):
   X=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));X/=np.linalg.norm(X);matrices.append(('random_complex',X))
  for k in range(N+1):
   # Canonical Schmidt-aligned witness: little-endian prefix blocks.
   c=np.zeros(n);c[:D**k]=D**(-k/2);c=c.reshape([D]*N).transpose(tuple(reversed(range(N)))).ravel();matrices.append((f'aligned_rank_{D**k}',np.diag(c)))
  for name,X in matrices:
   p=np.array([bell_prefix(X,D,i) for i in range(1,N+1)]);b,S=spectral_prefix(X,D,N)
   assert np.max(p-b)<=2e-12,(D,N,name,p,b)
   deficit=math.log(D)*p.sum()-S;assert deficit<=C+2e-12
   worst=max(worst,float(deficit))
   if name.startswith('aligned'):exactmax=max(exactmax,float(np.max(np.abs(p-b))));assert np.max(np.abs(p-b))<2e-12
   cases.append({'D':D,'N':N,'state':name,'entropy':S,'prefix_probabilities':p.tolist(),'simultaneous_Schmidt_upper_bounds':b.tolist(),'deficit':float(deficit)})
 # Check actual MC density matrices independently against formula, D2N<=5.
 reservoir_matrix=[]
 for N in range(1,6):
  D=2;n=D**N;plus=np.ones((D,D))/D;inc=np.eye(D)/D;sigma=np.zeros((n,n))
  for k in range(1,N+1):
   state=np.array([[1.]])
   for j in range(N):state=np.kron(state,plus if j<k else inc)
   sigma+=state/N
  p=[]
  for i in range(1,N+1):
   P=np.kron(np.ones((D**i,D**i))/(D**i),np.eye(D**(N-i)));p.append(float(np.trace(P@sigma)))
  analytic=np.array([(N-i+1+sum(D**(-h) for h in range(1,i)))/N for i in range(1,N+1)])
  assert np.max(np.abs(np.array(p)-analytic))<2e-12
  ev=np.linalg.eigvalsh(sigma);er=N*math.log(D)-entropy(np.maximum(ev,0));formula=resource_row(D,N)
  assert abs(er-formula['E_R_exact_formula'])<2e-12
  reservoir_matrix.append({'D':D,'N':N,'matrix_spectral_E_R':er,'formula_E_R':formula['E_R_exact_formula'],'all_prefix_probability_formula':'PASS'})
 rows=[resource_row(D,N) for D in [2,3,4] for N in [2,8,16,64,256,1024]]
 out={'status':'PASS_FINITE_CHECKS_ONLY','pure_state_cases':len(cases),'largest_checked_pure_deficit':worst,'largest_aligned_dominance_equality_error':exactmax,'matrix_reservoirs':reservoir_matrix,'resource_table':rows,'checks':cases,'not_computed':'no general convex roof, finite-block optimal dilution, tensorization or physical preparation','wall_s':time.perf_counter()-start,'CPU_s':time.process_time()-cpu,'peak_RSS_platform_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'RSS_unit':'bytes' if sys.platform=='darwin' else 'KiB','peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),'python':sys.version,'numpy':np.__version__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (ROOT/'FINITE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','pure_state_cases','largest_checked_pure_deficit','largest_aligned_dominance_equality_error','wall_s','CPU_s','peak_RSS_bytes']}));print(json.dumps([x for x in rows if x['D']==2],indent=2))
def resource_row(D,N):
 m=math.log(D);c=-math.log1p(-1/D)+m/(D-1);C=(2 if D==2 else 2*D)-m;cond=0.
 for ell in range(1,N+1):
  a=math.exp(-ell*m);weight=(1-a)/N if ell<N else (1-a)/(N*(1-1/D))
  h=c+math.log1p(-a)-(ell*m*a/(1-a));cond+=weight*h
 B=(N+1)*m/2;er=B-math.log(N)+cond;G=sum((N-h)*math.exp(-h*m) for h in range(1,N))/N
 return {'D':D,'N':N,'return_half_trace':(-math.expm1(-N*m))/N,'E_R_exact_formula':er,'E_C_lower_bound':max(m,er,B+m*G-C),'E_C_upper_and_exact_factory_cost':B,'E_C_identification':'known MC additivity;bounds not exact convex-roof evaluation','gap_lower':max(0,B+m*G-C-er),'gap_upper':B-er,'ln_N':math.log(N),'fixed_exact_cost_lower':N*m-math.log(N)+math.log1p(-math.exp(-N*m))-math.log1p(-1/D),'fixed_exact_cost_upper':N*m}
if __name__=='__main__':run()
