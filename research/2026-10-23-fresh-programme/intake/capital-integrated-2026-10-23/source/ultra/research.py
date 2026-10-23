"""Reproduce finite, synthetic checks. Only NumPy plus Python standard library.
No physical observations, external model calls, or paid services.
"""
from pathlib import Path
import json, hashlib, time
import numpy as np
ROOT=Path(__file__).resolve().parent

def channel_maps(H):
 n=len(H[0]);pairs=[(i,j) for i in range(n) for j in range(i+1,n)];index={x:k for k,x in enumerate(pairs)}
 maps=[];signs=[]
 for h in H:
  assert np.array_equal(h,h.T) and np.array_equal(h@h,np.eye(n,dtype=int))
  assert np.count_nonzero(h)==n
  p=np.argmax(np.abs(h),axis=1);sg=h[np.arange(n),p]
  mp=[];ss=[]
  for i,j in pairs:
   a,b=int(p[i]),int(p[j]);mp.append(index[min(a,b),max(a,b)]);ss.append(int(sg[i]*sg[j]*(1 if a<b else -1)))
  maps.append(np.array(mp));signs.append(np.array(ss,dtype=np.int64))
 return maps,signs

def certify(H,kmax=20):
 maps,signs=channel_maps(H);d=len(H);m=len(maps[0]);P=np.eye(m,dtype=np.int64)
 # Bound d**k <= 8**20 < 2**63: every partial signed sum has abs entry <= d**k.
 assert d**kmax < 2**63
 for k in range(1,kmax+1):
  P=sum((sg[:,None]*P[mp,:] for mp,sg in zip(maps,signs)),start=np.zeros_like(P))
  # Individual row absolute sums <= d**k, so int64 summation cannot overflow either.
  r=max(int(x) for x in np.abs(P).sum(axis=1));assert r<=d**k
  # Exact integers establish ||Phi**k||_infinity <= (7/8)**k.
  if r*8**k<=d**k*7**k:return {'power':k,'max_row_abs_sum':r,'denominator':d**k,'rho_upper':'7/8','s0_lower':'1/2','certificate_arithmetic':'exact signed int64 matrix powers; final comparison Python integers'}
 return None

def lyap(F,Q):
 n=len(F);L=np.kron(np.eye(n),F)+np.kron(F,np.eye(n))
 C=np.linalg.solve(L,(2*Q).reshape(-1,order='F')).reshape((n,n),order='F')
 return (C+C.T)/2

def design_matrix(C):
 n=len(C[0]);cols=[]
 for i in range(n*n):
  E=np.zeros((n,n));E.flat[i]=1
  cols.append(np.concatenate([(E@c+c@E.T).reshape(-1) for c in C])/np.sqrt(len(C)))
 return np.array(cols).T

def decode(C,D,gamma):
 M=design_matrix(C);rhs=np.concatenate([2*gamma*(c-d).reshape(-1) for c,d in zip(C,D)])/np.sqrt(len(C))
 v,_,_,s=np.linalg.lstsq(M,rhs,rcond=None);return v.reshape(C[0].shape),float(s[-1]),float(np.linalg.norm(M@v-rhs))

def covariance_from_draws(C,N,rng):
 z=rng.standard_normal((N,len(C)))@np.linalg.cholesky(C).T;z-=z.mean(axis=0)
 return z.T@z/(N-1)

def run():
 begin=time.perf_counter();rows=json.loads((ROOT/'expander_designs.json').read_text());rng=np.random.default_rng(170023)
 result={'status':'finite exact certificates plus synthetic numerical diagnostics; no physical validation or novelty claim','seed':170023,'certificates':[],'exact_covariance_diagnostics':[],'raw_snapshot_comparison':[]}
 for row in rows:
  H=[np.array(x,dtype=np.int64) for x in row['H']];cert=certify(H);assert cert is not None;result['certificates'].append({'n':row['n'],**cert})
  n=row['n'];I=np.eye(n);Ds=[I+sign*h for h in H for sign in [1,-1]]
  # Pair-correlated realization: one independent scalar driver per matched pair.
  for h,d in zip([h for h in H for _ in [1,-1]],Ds):assert np.linalg.eigvalsh(d).min()>-1e-12
  if n>16:continue
  X=rng.standard_normal((n,n));A=(X-X.T);A/=np.linalg.norm(A,2);gamma=17.;F=gamma*I-A
  C=[lyap(F,gamma*d) for d in Ds];Ah,s,res=decode(C,Ds,gamma)
  err=float(np.linalg.norm(Ah-A));assert err<1e-10 and s>=.25-1e-10
  # Direct confirmation of the symmetric/skew cross-term cancellation.
  E=rng.standard_normal((n,n));S=(E+E.T)/2;K=(E-E.T)/2
  cross=max(abs(float(np.sum((S@h+h@S)*(K@h-h@K)))) for h in H);assert cross<1e-9
  result['exact_covariance_diagnostics'].append({'n':n,'error_F':err,'sigma_min_measured_float':s,'sigma_min_theorem':.25,'residual':res,'cross_term_abs':cross})
  if n!=8:continue
  C0=lyap(F,gamma*I);R=.15*I+.05*np.ones((n,n))/n;obs=[C0+R]+[C0+R+c for c in C]
  q=(1-1/gamma)**2;Finv=np.linalg.inv(F);mean_added=float(gamma**2*q*np.trace(Finv@Finv.T));assert mean_added<=n+1e-10
  for Nper in [1000,10000]:
   N=17*Nper;noise_errors=[];mean_errors=[];sigmas=[]
   for repeat in range(6):
    hats=[covariance_from_draws(c,Nper,rng) for c in obs];deltas=[c-hats[0] for c in hats[1:]]
    An,sn,rn=decode(deltas,Ds,gamma);noise_errors.append(float(np.linalg.norm(An-A)));sigmas.append(sn)
    # Strong control: every label is known and all N observations are used in multivariate regression.
    labels=gamma*np.sqrt(q)*rng.standard_normal((N,n));x=labels@Finv.T+rng.standard_normal((N,n))@np.linalg.cholesky(C0+R).T
    M=np.linalg.solve(labels.T@labels,labels.T@x).T
    Am=gamma*I-np.linalg.inv(M);mean_errors.append(float(np.linalg.norm(Am-A)))
   result['raw_snapshot_comparison'].append({'n':n,'total_snapshots_each':N,'replicates':6,'noise_RMS_F':float(np.sqrt(np.mean(np.square(noise_errors)))),'mean_RMS_F':float(np.sqrt(np.mean(np.square(mean_errors)))),'noise_errors_F':noise_errors,'mean_errors_F':mean_errors,'noise_min_fitted_sigma':min(sigmas),'noise_added_stationary_trace':float(n),'mean_added_stationary_trace':mean_added,'common_readout_covariance_trace':float(np.trace(R)),'noise_settings_including_baseline':17,'mean_labels':'independent Gaussian known forces; reprogrammed for each independent sample','physical_preparation_and_switching_cost':'UNKNOWN; iid Gaussian sampling is a synthetic interface'})
 # Negative control: 8 diagonal signs cannot distinguish all 512 coordinate words.
 n=512;words=rng.integers(0,2,(n,8));seen={};duplicate=None
 for i,w in enumerate(words):
  key=tuple(w.tolist())
  if key in seen:duplicate=[seen[key],i];break
  seen[key]=i
 assert duplicate is not None
 i,j=duplicate
 result['negative_controls']={'diagonal_8_masks_n512':{'duplicate_coordinates':duplicate,'identical_words':words[i].tolist(),'invisible_skew_pair_exact':True,'reason':'At A=0, covariance responses equal diagonal designs; a skew matrix on equal column words commutes with every design.'},'unforced_ambiguity':'For C0=I and diffusion gamma I, all skew A give the same baseline covariance; no passive snapshot decoder identifies A.'}
 result['wall_seconds']=time.perf_counter()-begin
 (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
