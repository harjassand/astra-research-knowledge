import numpy as np,itertools,json,hashlib,math
from pathlib import Path
r=Path(__file__).resolve().parent;rng=np.random.default_rng(281045)
cases=0;groups=0;enums=0;minloewner=1.;maxviol=0.;maxrelaxgap=0.
for n in [2,4,7,10]:
 for rep in range(16):
  p=2.**(-rng.uniform(0,24,n));p[0]=1. if rep%3==0 else p[0]
  V=rng.normal(size=(n,n+2));V/=np.linalg.norm(V,axis=1,keepdims=True);Y=V@V.T
  sd=np.sqrt(p*(1-p));M=np.zeros((n+1,n+1));M[0,0]=1;M[0,1:]=M[1:,0]=p;M[1:,1:]=np.outer(p,p)+(sd[:,None]*Y)*sd[None,:]
  assert np.linalg.eigvalsh(M)[0]>-1e-12 and np.max(abs(np.diag(M)[1:]-p))<1e-12
  L=rng.normal(size=(n+3,n+1));L[:,0]*=(0 if rep%4==0 else 1);A=L.T@L;a=max(1.,np.linalg.norm(A,2));m=2.**(-rng.uniform(0,20));w=2.**rng.uniform(-5,5,n)
  cost=m+w@p;S=np.sum(A*M);F=S/cost;R0=A[0,0]/m;delta=min(.5,m/(64*a*n));keep=np.where(p>=delta)[0];tail=np.where(p<delta)[0]
  St=np.sum(A[np.ix_(tail+1,tail+1)]*M[np.ix_(tail+1,tail+1)]) if len(tail) else 0
  Sk=np.sum(A[np.ix_(keep+1,keep+1)]*M[np.ix_(keep+1,keep+1)]) if len(keep) else 0
  assert St<=m/64+1e-10
  assert S<=2*A[0,0]+4*Sk+m/16+1e-9
  dic={}
  for i in keep:
   exponent=int(np.ceil(np.log2(p[i])));dic.setdefault(exponent,[]).append(i)
  Ng=len(dic);best=0.;meanratio=R0
  for exp,inds in dic.items():
   pp=2.**exp;ix=np.array(inds);Mi=M[np.ix_(ix+1,ix+1)];Ai=A[np.ix_(ix+1,ix+1)]
   Yi=Mi/pp+np.diag(1-p[ix]/pp);Yi=(Yi+Yi.T)/2
   assert np.linalg.eigvalsh(Yi)[0]>-1e-12
   Ess=(2/np.pi)*np.arcsin(np.clip(Yi,-1,1));Ezz=pp/4*(np.ones_like(Ess)+Ess);Ez=np.ones(len(ix))*pp/2
   low=np.linalg.eigvalsh(Ezz-Mi/(2*np.pi))[0];minloewner=min(minloewner,low);assert low>-1e-11
   SI=np.sum(Ai*Mi);ci=m+w[ix]@p[ix];hom=np.sum(Ai*Ezz);actual=A[0,0]+2*A[0,ix+1]@Ez+hom;ec=m+w[ix]@Ez
   assert hom>=SI/(2*np.pi)-1e-10
   assert ec<=ci+1e-12
   assert max(R0,actual/ec)>=SI/(8*np.pi*ci)-1e-9
   best=max(best,SI/ci);meanratio=max(meanratio,actual/ec);groups+=1
  if F>=1 and R0<F/4:
   assert Ng and best>=F/(16*Ng*Ng)-1e-10
   assert meanratio>=F/(128*np.pi*Ng*Ng)-1e-10
  # Exhaustive feasible cube comparison; no source state or SDP solve is used.
  Z=np.array(list(itertools.product([0.,1.],repeat=n)));XX=np.c_[np.ones(len(Z)),Z]
  nums=np.einsum('ni,ij,nj->n',XX,A,XX);costs=m+Z@w;opt=max(nums/costs)
  if Ng and F>=1:assert opt>=F/(4096*Ng*Ng)-1e-10
  maxrelaxgap=max(maxrelaxgap,F/opt if opt else 0);enums+=1;cases+=1
out={'status':'PASS_AUTHOR_GATED_POSITIVE_COST_ROUNDING','feasible_moment_cases':cases,'dyadic_group_Loewner_checks':groups,'exhaustive_cube_comparisons':enums,'minimum_rounding_Loewner_eigenvalue':minloewner,'maximum_test_relaxation_ratio':maxrelaxgap,'source_sha256':hashlib.sha256((r/'ordinary_classical_positive_cost_gated_rounding_20261028.md').read_bytes()).hexdigest(),'scope':'Analytic moment/cost diagnostics and small exact-menu comparisons; no production SDP, full rare-gate repeat cap, generic CPTP extension or independent receipt.'}
(r/'ordinary_classical_positive_cost_gated_rounding_20261028_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
