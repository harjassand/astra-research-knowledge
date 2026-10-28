from pathlib import Path
import hashlib,json
from fractions import Fraction as F
import numpy as np
rng=np.random.default_rng(728212)
errs={k:0. for k in ['cost_identity','partial_trace','odd_cost','parallelogram','contraction_polynomial']}
mins={k:0. for k in ['choi_eigenvalue','m_minus_m0','contraction_slack','H_inequality','polynomial_slack']}
def cmat(n,m):return rng.normal(size=(n,m))+1j*rng.normal(size=(n,m))
def herm(a):return (a+a.conj().T)/2
def root(a):
 w,v=np.linalg.eigh(herm(a));return (v*np.sqrt(np.maximum(w,0)))@v.conj().T
count=0
for k in range(1,7):
 for case in range(24):
  qq,_=np.linalg.qr(cmat(k,k));eig=rng.uniform(0,1,k)
  if case%4==0:eig[0]=0
  if case%4==1:eig[-1]=1
  A=(qq*eig)@qq.conj().T;Ar=root(A);Dr=root(np.eye(k)-A)
  ww=cmat(2*k,2*k);W=ww@ww.conj().T/(2*k);m0=2**(-(case%12)-2)
  left,sv,right=np.linalg.svd(Dr@W[k:,:k]@Ar)
  S=np.diag(sv);R=right.conj().T;L=left
  zz=cmat(k,k);u,_,v=np.linalg.svd(zz);V=(u*rng.uniform(0,1,k))@v
  def C(v):
   B=-Ar@R@v@L.conj().T@Dr
   return np.block([[A,B],[B.conj().T,np.eye(k)-A]])
  base=m0+np.trace(W[:k,:k]@A+W[k:,k:]@(np.eye(k)-A)).real-2*sv.sum()
  cc=C(V);direct=m0+np.trace(W@cc).real
  canon=base+2*np.trace(S@(np.eye(k)-herm(V))).real
  errs['cost_identity']=max(errs['cost_identity'],abs(direct-canon))
  errs['partial_trace']=max(errs['partial_trace'],np.linalg.norm(cc[:k,:k]+cc[k:,k:]-np.eye(k)))
  mins['choi_eigenvalue']=min(mins['choi_eigenvalue'],np.linalg.eigvalsh(cc).min())
  mins['m_minus_m0']=min(mins['m_minus_m0'],base-m0)
  X=herm(V);H=(V-V.conj().T)/(2j)
  mins['H_inequality']=min(mins['H_inequality'],np.linalg.eigvalsh(2*(np.eye(k)-X)-H@H).min())
  hh=herm(cmat(k,k));hh*=.5/max(1,np.linalg.norm(hh,2))
  ev=np.eye(k)-2*hh@hh;vp=ev+1j*hh;vm=ev-1j*hh
  slack=np.eye(k)-vp.conj().T@vp
  errs['contraction_polynomial']=max(errs['contraction_polynomial'],np.linalg.norm(slack-(3*hh@hh-4*hh@hh@hh@hh)))
  mins['polynomial_slack']=min(mins['polynomial_slack'],np.linalg.eigvalsh(herm(slack)).min())
  for vv in [vp,vm]:
   cost=m0+np.trace(W@C(vv)).real
   errs['odd_cost']=max(errs['odd_cost'],abs(cost-(base+4*np.trace(S@hh@hh).real)))
   mins['choi_eigenvalue']=min(mins['choi_eigenvalue'],np.linalg.eigvalsh(C(vv)).min())
  # Generic real-linear numerator on the actual channel, including affine offset.
  ops=[herm(cmat(2*k,2*k)) for _ in range(5)];offset=rng.normal(size=5)
  zplus=offset+np.array([np.trace(o@C(vp)).real for o in ops])
  zminus=offset+np.array([np.trace(o@C(vm)).real for o in ops])
  odd=np.array([np.trace(o@(C(vp)-C(vm))/2).real for o in ops])
  even=(zplus+zminus)/2
  errs['parallelogram']=max(errs['parallelogram'],abs((zplus@zplus+zminus@zminus)/2-(odd@odd+even@even)))
  assert max(zplus@zplus,zminus@zminus)+1e-10>=odd@odd
  count+=1
# Exact scalar feasibility polynomial and finite-round ratio constant checks.
exact=0
for a in range(-50,51):
 h=F(a,100);assert 1-((1-2*h*h)**2+h*h)==3*h*h-4*h**4>=0;exact+=1
for rr in range(1,40):
 for mm in [F(1,2**p) for p in (0,4,12,40)]:
  for qq in [F(0),F(1,3),F(2**12)]:
   assert 128*rr*rr*mm+3072*qq+4*mm<=256*rr*rr*mm+3072*qq
   exact+=1
assert max(errs.values())<1e-10,errs
assert min(mins.values())>-1e-10,mins
source=Path(__file__).with_name('ordinary_fixed_effect_decoder_positive_cost_geometry_20261028.md')
out={'status':'PASS author finite identities; not independent receiving or executed SDP/source acquisition','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'physical_fixed_slice_cases':count,'exact_scalar_cases':exact,'max_residuals':errs,'minimum_psd_slacks':mins,'source_calls':0,'scope':'Checks complex polar cost reduction, singular fixed effects, actual full-CPTP completion, noncommuting real/imag inequality, polynomial odd completion and conservative finite ratio constants. Does not test concentration probabilities or solve moving-A optimization.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
