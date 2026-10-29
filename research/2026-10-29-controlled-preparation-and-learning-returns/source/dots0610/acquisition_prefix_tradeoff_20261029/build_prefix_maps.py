import numpy as np,json,math
from pathlib import Path
from functools import reduce
from scipy.linalg import expm,eigh,null_space
from scipy.spatial.transform import Rotation
here=Path(__file__).parent;a=np.load(here/'prefix_bank.npz');P=a['P'];U=a['U0'];D=16
kron=lambda xs:reduce(np.kron,xs)
def su(R):return expm(-.5j*np.einsum('a,aij->ij',Rotation.from_matrix(R).as_rotvec(),P[1:]))
def polar(A):
 u,s,v=np.linalg.svd(A);return u@np.diag([1,1,np.linalg.det(u@v)])@v
def rounding(v):
 A=np.sqrt(3)*v.reshape(3,3);R1=polar(A);R2=polar(-A);return R1 if np.linalg.norm(R1-A)<=np.linalg.norm(R2+A) else R2
Js=[sum(kron([P[b] if i==j else P[0] for i in range(4)]) for j in range(4))/2 for b in [1,2,3]]
vals,Z=eigh(sum(J@J for J in Js));Ebase=Z[:,vals<1e-8]
def superof(fun):return np.stack([fun(z.reshape(2,2)).reshape(-1) for z in np.eye(4)],axis=1)
def effect(T):return (T.conj().T@np.eye(2).reshape(-1)).reshape(2,2)
def ptrD(r):return np.einsum('abad->bd',r.reshape(D,2,D,2))
matchings=[[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]
canonical=[]
for M in matchings:
 v=np.zeros(D)
 for x in range(D):
  bits=[(x>>(3-j))&1 for j in range(4)]
  if all(bits[i]!=bits[j] for i,j in M):v[x]=np.prod([1 if bits[i]==0 else -1 for i,j in M])/2
 canonical.append(v)
archive={};rows=[]
for m in [100,1000,10000,100000,1000000]:
 frames=[np.eye(3)];svs=[]
 for S in a[f'sums_{m}']:
  _,sv,vt=np.linalg.svd(S/m-a['Jembed']);frames.append(rounding(vt[-1]));svs.append(sv)
 V=kron([su(R) for R in frames]);E=V@Ebase;Ds=[E.conj().T]+[np.outer(np.array([1,0]),q.conj()) for q in null_space(E.conj().T).T]
 As=[np.kron(A,np.eye(2))@U@np.kron(E,np.eye(2)) for A in Ds]
 phis=[]
 for pauli in P:
  Bs=[np.einsum('aiaj->ij',(np.kron(pauli.conj().T,np.eye(2))@A).reshape(2,2,2,2))/2 for A in As]
  phis.append(superof(lambda sig,Bs=Bs:sum(B@sig@B.conj().T for B in Bs)))
 good,bad=phis[0],sum(phis[1:]);sigma=np.outer(a[f'bath_{m}'],a[f'bath_{m}'].conj())
 six=[]
 for fail in [False,True]:
  Ks=[]
  for paul in P[1:]:
   _,basis=np.linalg.eigh(paul)
   for b in [0,1]:
    ket=basis[:,b];outket=basis[:,1-b if fail else b]
    for A in As:Ks.append(np.einsum('a,aibj,b->ij',outket.conj(),A.reshape(2,2,2,2),ket)/math.sqrt(6))
  six.append(superof(lambda sig,Ks=Ks:sum(K@sig@K.conj().T for K in Ks)))
 matching=[]
 for fail in [False,True]:
  def fun(sig):
   out=np.zeros((2,2),complex)
   for v0 in canonical:
    v=V@v0;rho=np.outer(v,v.conj());F=np.eye(D)-rho if fail else rho;Y=np.kron(F,np.eye(2));out+=ptrD(Y@U@np.kron(rho,sig)@U.conj().T@Y)/3
   return out
  matching.append(superof(fun))
 checks={'sixstate_effect_identity':float(np.linalg.norm(1.5*effect(six[1])-effect(bad))),'matching_hazard_slack':float(np.linalg.eigvalsh(2*effect(matching[1])-effect(bad)).min()),'service_TP':float(np.linalg.norm(effect(good+bad)-np.eye(2))),'sixstate_TP':float(np.linalg.norm(effect(sum(six))-np.eye(2))),'matching_TP':float(np.linalg.norm(effect(sum(matching))-np.eye(2)))}
 assert checks['sixstate_effect_identity']<1e-11 and checks['matching_hazard_slack']>-1e-11
 for k,val in {'good':good,'bad':bad,'six_pass':six[0],'six_fail':six[1],'matching_pass':matching[0],'matching_fail':matching[1],'sigma':sigma,'E':E,'Vhat':V}.items():archive[f'{k}_{m}']=val
 rows.append({'calibration_calls':m,'last_training_variant_for_next_source':int(a[f'lastparity_{m}']),'deployment_variant':0,'checks':checks,'candidate_singular_values':[s.tolist() for s in svs]})
np.savez(here/'prefix_maps.npz',**archive)
print(json.dumps({'scope':'Actual same seeded no-reset bank prefixes; only counters used to learn frames. Deployment uses U0 and actual retained bath state. Exact supplied-generator CP maps, not physical bath access.','rows':rows},indent=2))
