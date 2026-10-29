import numpy as np,json,itertools
from scipy.linalg import expm,eigh
from functools import reduce
rng=np.random.default_rng(2026102905)
P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1]).astype(complex)]
kron=lambda xs:reduce(np.kron,xs)
def perm_indices(n,p):return np.array([sum(((x>>(n-1-p[i]))&1)<<(n-1-i) for i in range(n)) for x in range(2**n)])
def swap(n,i,j):
 p=list(range(n));p[i],p[j]=p[j],p[i];return np.eye(2**n)[perm_indices(n,p)]
rows=[]
for n in [4,6]:
 d=2**n;J=[sum(kron([P[a] if i==j else P[0] for i in range(n)]) for j in range(n))/2 for a in range(1,4)];ev,Z=eigh(sum(A@A for A in J));Es=Z[:,ev<1e-8];ds=Es.shape[1];Proj=Es@Es.conj().T;k=2**int(np.floor(np.log2(ds)));E=Es[:,:k]
 Ss=[swap(n,i,j) for i in range(n) for j in range(i+1,n)];perms=[perm_indices(n,p) for p in itertools.permutations(range(n))]
 sing=np.array([0,1,-1,0])/np.sqrt(2);seed=kron([sing]*(n//2));avg=sum(np.outer(seed[idx],seed[idx]) for idx in perms)/len(perms);ensemble_res=np.linalg.norm(avg-Proj/ds)
 assert ensemble_res<1e-12
 gamma=.04;ad=[kron([np.diag([1,np.sqrt(1-gamma)])]+[P[0]]*(n-1)),kron([np.array([[0,np.sqrt(gamma)],[0,0]])]+[P[0]]*(n-1))];h=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));h=(h+h.conj().T)/2/np.sqrt(d)
 cases={'nonunital_damping':ad,'random_coherent':[expm(-.1j*h)],'rare_reflection':[np.eye(d)-2*np.outer(E[:,0],E[:,0].conj())]}
 for name,Ks in cases.items():
  bars=[sum(A[np.ix_(idx,idx)] for idx in perms)/len(perms) for A in Ks]
  deltas=[float(1-sum(np.trace(Proj@S@A.conj().T@S@A).real for A in Ks)/ds) for S in Ss]
  comm=sum(np.linalg.norm((S@A-A@S)@Proj,'fro')**2 for S in Ss for A in Ks)/ds
  dist=sum(np.linalg.norm((A-B)@Proj,'fro')**2 for A,B in zip(Ks,bars))/ds
  Bs=[E.conj().T@A@E for A in Ks];F=sum(abs(np.trace(B))**2 for B in Bs)/k**2
  bound=ds/k*sum(deltas)/n
  # Actual initial Lüders outcome, full N, final projective outcome.
  S=Ss[0];q=0
  for s in [-1,1]:
   Pi=(np.eye(d)+s*S)/2;rho=Pi@avg@Pi;out=sum(A@rho@A.conj().T for A in Ks);q+=np.trace((np.eye(d)-s*S)/2@out).real
  assert abs(comm-2*sum(deltas))<1e-10 and dist<=sum(deltas)/n+1e-10 and 1-F<=bound+1e-10 and abs(q-deltas[0]/2)<1e-10
  rows.append({'n':n,'singlet_dimension':ds,'logical_dimension':k,'noise':name,'random_pair_singlet_ensemble_residual':ensemble_res,'sum_delta_weighted':sum(deltas),'commutator_budget':comm,'weighted_HS_distance':dist,'direct_Bell_loss':float(1-F),'weighted_bound':bound,'first_edge_actual_sign_flip_probability':q,'first_edge_delta_over_two':deltas[0]/2})
 # Rejected input fully resolving Bell measurement breaks singlet support.
 bells=np.array([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]]).T/np.sqrt(2)
 deph=np.zeros((d,d),complex)
 for b in range(4):
  Q=np.kron(np.outer(bells[:,b],bells[:,b]),np.eye(2**(n-2)));deph+=Q@avg@Q
 rows.append({'n':n,'rejected_full_Bell_input_measurement_singlet_leakage':float(1-np.trace(Proj@deph).real)})
print(json.dumps({'seed':2026102905,'checks':rows},indent=2))
