"""Independent GF/weighted-design/decoder algebra checks, not a recovery circuit."""
from pathlib import Path
import hashlib,itertools,json,math
import numpy as np

P=Path(__file__).parent
rng=np.random.default_rng(202610271858)
def mul(a,b,mod,degree):
 # Polynomial multiplication followed by long division (not Horner table generation).
 z=0
 for bit in range(degree):
  if (b>>bit)&1:z^=a<<bit
 for bit in range(2*degree-2,degree-1,-1):
  if (z>>bit)&1:z^=mod<<(bit-degree)
 return z

def field(Q,mod):
 d=Q.bit_length()-1
 tab=np.array([[mul(a,b,mod,d) for b in range(Q)] for a in range(Q)])
 inv=[0]+[int(np.flatnonzero(tab[a]==1)[0]) for a in range(1,Q)]
 assert all(np.count_nonzero(tab[a])==Q-1 for a in range(1,Q))
 return tab,inv

def rank(A,tab,inv):
 A=A.copy();r=0
 for col in range(A.shape[1]):
  piv=next((i for i in range(r,len(A)) if A[i,col]),None)
  if piv is None:continue
  A[[r,piv]]=A[[piv,r]];A[r]=tab[A[r],inv[A[r,col]]]
  for i in range(len(A)):
   if i!=r and A[i,col]:A[i]^=tab[A[r],A[i,col]]
  r+=1
  if r==len(A):break
 return r

T4,I4=field(4,7);T16,I16=field(16,19);T64,I64=field(64,67)
rank_checks=0
for q,Q,tab,inv in [(4,4,T4,I4),(9,16,T16,I16),(17,64,T64,I64)]:
 V=np.array([[1,x,tab[x,x],tab[tab[x,x],x]] for x in range(q)])
 for d in range(1,5):
  for js in itertools.combinations(range(q),d):
   assert rank(V[list(js)],tab,inv)==d;rank_checks+=1

# Enumerate all 16^4 seeds, but use a different binary projection and phase bijection.
A=np.indices((16,16,16,16)).reshape(4,-1).T
phasecols=[]
for x in range(9):
 vals=A[:,0]^T16[A[:,1],x]^T16[A[:,2],T16[x,x]]^T16[A[:,3],T16[T16[x,x],x]]
 projected=(vals&1)|((vals>>1)&2) # binary coordinates 0 and 2, not 0 and 1
 phasecols.append(np.array([2,0,3,1])[projected])
phases=np.stack(phasecols,axis=1)
subset_checks=0
for d in range(1,5):
 for js in itertools.combinations(range(9),d):
  code=sum(phases[:,j]*4**a for a,j in enumerate(js))
  assert np.all(np.bincount(code,minlength=4**d)==len(A)//(4**d))
  subset_checks+=1

# All index-multiplicity patterns needed by the fourth moment, independently of q.
pattern_checks=0
for inds in itertools.product(range(4),repeat=4):
 a,b,c,d=inds
 powers=(phases[:,a]+phases[:,b]-phases[:,c]-phases[:,d])%4
 counts=np.bincount(powers,minlength=4)
 val=(int(counts[0])-int(counts[2]),int(counts[1])-int(counts[3]))
 target=int(sorted([a,b])==sorted([c,d]))
 assert val==(target*len(A),0);pattern_checks+=1

def kraus(di,do,r):
 z=rng.normal(size=(do*r,di))+1j*rng.normal(size=(do*r,di));u,_=np.linalg.qr(z)
 return [u[j*do:(j+1)*do] for j in range(r)]
def choi(ks):
 return sum(np.outer(k.T.reshape(-1),k.T.reshape(-1).conj()) for k in ks)

def ptr(C,k,q):return np.trace(C.reshape(k,q,k,q),axis1=1,axis2=3)
rows=[]
for q in [2,3,5,6,9]:
 k=q+1;E=kraus(q,k,3);Dec=kraus(k,q,2);Ks=[d@e for d in Dec for e in E]
 vectors=(1j**phases[:,:q])/np.sqrt(q)
 phase_avg=sum(np.mean(np.abs(np.einsum('ni,ij,nj->n',vectors.conj(),a,vectors))**2) for a in Ks)
 basis_avg=sum(np.sum(np.abs(np.diag(a))**2) for a in Ks)/q
 favg=basis_avg/(q+1)+phase_avg*q/(q+1)
 fe=sum(abs(np.trace(a))**2 for a in Ks)/(q*q)
 residual=abs(favg-(q*fe+1)/(q+1));assert residual<1e-12
 # Explicit q-aware positivity/TP repair, with an arbitrary worst-direction perturbation.
 b=(q+1)/q;eta=.01;lam=eta/(8*b);kap=eta/(128*b*q);er=eta/(128*b*q)
 C=choi(Dec);mixed=(1-lam)*C+lam*np.eye(q*k)/q
 noise=rng.normal(size=(q*k,q*k))+1j*rng.normal(size=(q*k,q*k));noise=(noise+noise.conj().T)/2
 noise*=er/max(abs(np.linalg.eigvalsh(noise)))
 rounded=mixed+noise;fixed=rounded-np.kron(ptr(rounded,k,q)-np.eye(k),np.eye(q)/q)
 tp=float(np.linalg.norm(ptr(fixed,k,q)-np.eye(k),2))
 mineig=float(min(np.linalg.eigvalsh(fixed)));margin=lam/(2*q)
 assert tp<1e-12 and mineig>=margin-1e-12
 assert (1+1/q)*kap+2*er<=lam/(2*q)
 rows.append({'q':q,'k':k,'finite_design_Favg_Fent_residual':float(residual),'affine_TP_residual':tp,'repaired_min_eigenvalue':mineig,'required_margin':margin})

out={'status':'PASS','seed':202610271858,'finite_field_Vandermonde_rank_checks':rank_checks,'exact_nonstandard_projection_4wise_subset_checks':subset_checks,'exact_fourth_moment_pattern_checks':pattern_checks,'source_addendum_sha256':hashlib.sha256((P/'GENERAL_Q_DESIGN_ADDENDUM.md').read_bytes()).hexdigest(),'channel_and_q_dependent_repair_checks':rows,'scope':'Independent exact finite-field rank and integer-count tests, weighted design fidelity identity, and numerical q-dependent affine TP repair; not an implementation of the quantum recovery circuit or an optimized design-cardinality claim.'}
(P/'general_q_design_independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
