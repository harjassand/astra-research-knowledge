from fractions import Fraction as F
from pathlib import Path
import numpy as np,json
rng=np.random.default_rng(113021)
# Rational grid separation probabilities, including degeneracies and boundary hits.
grid_cases=0
for L in [1,2,4,8,16]:
 for aa in range(-8,9):
  for bb in range(-8,9):
   a,b=F(aa,7),F(bb,7);w=F(3,5)
   p=F(sum((a-F(j,L)*w)//w!=(b-F(j,L)*w)//w for j in range(L)),L)
   assert p<=min(F(1),abs(a-b)/w+F(1,L));grid_cases+=1
res={'fixedpoint':0.,'dirichlet':0.,'replication':0.,'telescope':0.};normal=0;sequential=0
for d in [2,3,5,8]:
 for trial in range(12):
  Ds=[]
  for _ in range(3):
   Z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));Ds.append((Z+Z.conj().T)/2)
  K=sum(D@D for D in Ds);e,U=np.linalg.eigh(K);S=(U*np.sqrt(e))@U.conj().T;Sinv=(U*e**(-.25))@U.conj().T
  As=[Sinv@D@Sinv for D in Ds]
  assert max(np.linalg.norm(A,2) for A in As)<=1+1e-10
  sphere=sum(A@A for A in As)-np.eye(d)
  fp=sum(A@S@A for A in As);lhs=sum(np.linalg.norm(A@S-S@A,'fro')**2 for A in As);rhs=2*np.trace(K@sphere).real
  res['fixedpoint']=max(res['fixedpoint'],float(np.linalg.norm(fp-S)));res['dirichlet']=max(res['dirichlet'],float(abs(lhs-rhs)))
  assert lhs<=2*np.linalg.norm(sphere,2)*np.trace(K).real+1e-9
  for r in [2,3]:
   DD=[np.kron(D,np.eye(r)/r) for D in Ds];KK=sum(D@D for D in DD);ee,UU=np.linalg.eigh(KK);SS=(UU*ee**(-.25))@UU.conj().T
   res['replication']=max(res['replication'],float(max(np.linalg.norm(SS@DD[a]@SS-np.kron(As[a],np.eye(r))) for a in range(3))))
  normal+=1
  # Noncommuting three pinchings and explicit right-to-left telescope.
  X=Ds[0];maps=[];bounds=[]
  for j in range(3):
   U=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))[0];vals=rng.normal(size=d);w=.7;offset=.17*j;bins=np.floor((vals-offset)/w);mask=bins[:,None]==bins[None,:]
   def pin(A,U=U,mask=mask):return U@((U.conj().T@A@U)*mask)@U.conj().T
   maps.append(pin);bounds.append(np.linalg.norm(X-pin(X),ord='nuc'))
  out=X.copy()
  for f in maps:out=f(out)
  telescope=np.zeros_like(X)
  for j,f in enumerate(maps):
   term=X-f(X)
   for g in maps[j+1:]:term=g(term)
   telescope+=term
  res['telescope']=max(res['telescope'],float(np.linalg.norm(X-out-telescope)))
  assert np.linalg.norm(X-out,ord='nuc')<=sum(bounds)+1e-9;sequential+=1
assert max(res.values())<1e-9
out={'exact_rational_grid_cases':grid_cases,'normalization_cases':normal,'noncommuting_telescope_cases':sequential,'max_residuals':res,'scope':'Mathematical matrix identities and exact finite-grid boundary probabilities, not spectral acquisition execution'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
