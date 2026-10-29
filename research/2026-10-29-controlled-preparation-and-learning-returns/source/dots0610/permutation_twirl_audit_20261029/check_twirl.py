import itertools,json,numpy as np
from pathlib import Path
rng=np.random.default_rng(20261029)
def matching(xs):
 if not xs:yield [];return
 a=xs[0]
 for j in range(1,len(xs)):
  for rest in matching(xs[1:j]+xs[j+1:]):yield[(a,xs[j])]+rest
def singlet(n,M):
 v=np.zeros(2**n)
 for x in range(2**n):
  z=1.
  for a,b in M:
   ba=(x>>a)&1;bb=(x>>b)&1
   if ba==bb:z=0;break
   z*=(-1)**ba/np.sqrt(2)
  v[x]=z
 return v
def randomiso(a,b):return np.linalg.qr(rng.normal(size=(a,b))+1j*rng.normal(size=(a,b)))[0]
def apply(J,rho,o,i):return np.einsum('aibj,ij->ab',J.reshape(o,i,o,i),rho)
def effect(J,o,i):return np.einsum('aiaj->ij',J.reshape(o,i,o,i)).T
n=6;D=64;mem=2
S=np.array([singlet(n,M) for M in matching(list(range(n)))]).T
V,s,_=np.linalg.svd(S,full_matrices=False);d=sum(s>1e-9);V=V[:,:d];dim=d*mem
W=randomiso(dim,dim);J=np.zeros((dim*dim,dim*dim),complex)
for perm in itertools.permutations(range(n)):
 ix=[sum(((x>>j)&1)<<perm[j] for j in range(n)) for x in range(D)]
 pv=np.zeros_like(V);pv[ix,:]=V;U=V.conj().T@pv;U=np.kron(U,np.eye(mem));A=U.conj().T@W@U
 z=A.reshape(-1);J+=np.outer(z,z.conj())/720
B=np.einsum('aiaj->ij',W.reshape(d,mem,d,mem))/d
Agood=np.kron(np.eye(d),B);Jgood=np.outer(Agood.reshape(-1),Agood.reshape(-1).conj());Jbad=J-Jgood
H=np.eye(mem)-B.conj().T@B
err_effect=np.linalg.norm(effect(Jbad,dim,dim)-np.kron(np.eye(d),H))
# B_bad memory marginal obtained from fixed maximally mixed logical input
basis=[]
for z in np.eye(mem*mem):
 x=apply(Jbad,np.kron(np.eye(d)/d,z.reshape(mem,mem)),dim,dim)
 basis.append(np.einsum('aiaj->ij',x.reshape(d,mem,d,mem)).reshape(-1))
Bmem=np.stack(basis,axis=1)
v=randomiso(dim,1)[:,0];rho=np.outer(v,v.conj())
out=apply(Jbad,rho,dim,dim);sigma=np.einsum('aiaj->ij',rho.reshape(d,mem,d,mem))
ns=np.linalg.norm(np.einsum('aiaj->ij',out.reshape(d,mem,d,mem))-(Bmem@sigma.reshape(-1)).reshape(mem,mem))
# matching test on untwirled source: physical singlets expressed in logical P
Hfail=np.eye(mem,dtype=complex)
for v in (V.conj().T@S).T:
 b=np.einsum('a,aibj,b->ij',v.conj(),W.reshape(d,mem,d,mem),v)
 Hfail-=b.conj().T@b/S.shape[1]
slack=np.linalg.eigvalsh((n+2)/(n-1)*Hfail-H).min()
# Restrict to K=4 and reset logical leakage. Choi from Kraus bad eigendecomposition.
K=4;dimq=K*mem;Jq=np.zeros((dimq*dimq,dimq*dimq),complex)
evals,evecs=np.linalg.eigh((Jbad+Jbad.conj().T)/2)
for i,e in enumerate(evals):
 if e<1e-12:continue
 A=np.sqrt(e)*evecs[:,i].reshape(d,mem,d,mem)[:,:,:K,:]
 maps=[A[:K].reshape(dimq,dimq)]
 for a in range(K,d):
  for j in range(K):
   R=np.zeros((K,mem,K,mem),complex);R[j]=A[a]/np.sqrt(K);maps.append(R.reshape(dimq,dimq))
 for R in maps:
  z=R.reshape(-1);Jq+=np.outer(z,z.conj())
qeffect=np.linalg.norm(effect(Jq,dimq,dimq)-np.kron(np.eye(K),H))
report={'n':n,'d':int(d),'K':K,'memory_dimension':mem,'permutations':720,'bad_choi_min_eigenvalue':float(evals.min()),'bad_effect_tensor_error':float(err_effect),'correlated_input_memory_nonsignalling_error':float(ns),'matching_hazard_min_slack':float(slack),'proper_subcode_same_bad_effect_error':float(qeffect),'scope':'Floating exact finite-group diagnostic of operator identities; not a proof or hardware experiment'}
assert evals.min()>-1e-11 and err_effect<1e-11 and ns<1e-11 and slack>-1e-11 and qeffect<1e-11
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
