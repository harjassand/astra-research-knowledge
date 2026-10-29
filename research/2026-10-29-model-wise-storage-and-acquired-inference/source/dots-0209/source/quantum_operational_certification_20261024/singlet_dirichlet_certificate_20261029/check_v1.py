import numpy as np,json,itertools,math
from scipy.linalg import expm,eigh
from functools import reduce
rng=np.random.default_rng(2026102903)
P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1]).astype(complex)]
kron=lambda xs:reduce(np.kron,xs)
def perm_indices(n,p):
 return np.array([sum(((x>>(n-1-p[i]))&1)<<(n-1-i) for i in range(n)) for x in range(2**n)])
def swap(n,i,j):
 p=list(range(n));p[i],p[j]=p[j],p[i];idx=perm_indices(n,p);return np.eye(2**n)[idx]
def partial_choi(Ks,E):
 k=E.shape[1];Bs=[E.conj().T@A@E for A in Ks]
 C=sum(np.outer(B.reshape(-1),B.reshape(-1).conj())/k for B in Bs)
 R=np.eye(k)-sum(B.conj().T@B for B in Bs)
 # reset leakage to logical |0>; normalized Choi order output,input.
 C[:k,:k]+=R.T/k
 return C,Bs
rows=[]
for n in [4,6]:
 d=2**n;J=[sum(kron([P[a] if i==j else P[0] for i in range(n)]) for j in range(n))/2 for a in range(1,4)]
 ev,Z=eigh(sum(A@A for A in J));Es=Z[:,ev<1e-8];k=2**int(np.floor(np.log2(Es.shape[1])));E=Es[:,:k]
 Ss=[swap(n,i,j) for i in range(n) for j in range(i+1,n)]
 # Fixed unknown local basis twist shared by code and probes.
 V=kron([expm(-.2j*np.einsum('a,aij->ij',rng.normal(size=3),np.array(P[1:]))) for _ in range(n)])
 E=V@E;Ss=[V@S@V.conj().T for S in Ss]
 z=kron([P[3]]+[P[0]]*(n-1));h=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));h=(h+h.conj().T)/2/np.sqrt(d)
 gamma=.07;ad=[kron([np.diag([1,np.sqrt(1-gamma)])]+[P[0]]*(n-1)),kron([np.array([[0,np.sqrt(gamma)],[0,0]])]+[P[0]]*(n-1))]
 cases={'identity':[np.eye(d)],'local_phase':[np.sqrt(.93)*np.eye(d),np.sqrt(.07)*z], 'nonunital_damping':ad,'random_coherent':[expm(-.15j*h)],'rare_code_reflection':[np.eye(d)-2*np.outer(E[:,0],E[:,0].conj())]}
 perms=[perm_indices(n,p) for p in itertools.permutations(range(n))]
 for name,Ks in cases.items():
  delta=[float(1-sum(np.trace(S@A.conj().T@S@A).real for A in Ks)/d) for S in Ss]
  comm=sum(np.linalg.norm(S@A-A@S,'fro')**2 for A in Ks for S in Ss)/d
  bars=[]
  for A in Ks:
   B=V.conj().T@A@V;B=sum(B[np.ix_(idx,idx)] for idx in perms)/len(perms);bars.append(V@B@V.conj().T)
  hs=sum(np.linalg.norm(A-B,'fro')**2 for A,B in zip(Ks,bars))/d
  cdev=sum(np.linalg.norm((A-B)@E,'fro')**2 for A,B in zip(Ks,bars))/k
  C,Bs=partial_choi(Ks,E);phi=np.eye(k).reshape(-1)/np.sqrt(k);Fe=float(np.vdot(phi,C@phi).real)
  direct=sum(abs(np.trace(B))**2 for B in Bs)/k**2
  bound=d/k*sum(delta)/n
  logk=int(np.log2(k));ps=[kron([P[a] for a in word]) for word in itertools.product(range(4),repeat=logk)]
  Ct=sum(np.kron(Q.conj().T,Q.T)@C@np.kron(Q.conj().T,Q.T).conj().T for Q in ps)/len(ps)
  bell=np.stack([Q.reshape(-1)/np.sqrt(k) for Q in ps],axis=1);diag=bell.conj().T@Ct@bell
  dist=.5*sum(abs(np.linalg.eigvalsh(Ct-np.outer(phi,phi))))
  off=np.linalg.norm(diag-np.diag(np.diag(diag)))
  assert abs(comm-2*sum(delta))<1e-10 and hs<=sum(delta)/n+1e-10 and 1-direct<=cdev+1e-10 and 1-Fe<=bound+1e-10 and off<1e-10 and abs(dist-(1-Fe))<1e-10
  rows.append({'n':n,'singlet_dimension':Es.shape[1],'logical_dimension':k,'noise':name,'sum_delta':sum(delta),'mean_ancilla_failure':sum(delta)/len(Ss)/2,'normalized_commutator_budget':comm,'normalized_HS_commutant_distance':hs,'code_deviation_bound':cdev,'direct_code_Bell_loss':float(1-direct),'completed_decoder_Bell_loss':1-Fe,'dirichlet_Bell_loss_bound':bound,'twirled_Bell_trace_distance_equals_halfdiamond':float(dist),'twirled_offdiagonal_residual':float(off)})
# Actual interferometric outcome mean via density matrix on control+data for one nonunital case.
n=4;d=16;S=swap(n,0,1);g=.2;Ks=[kron([np.diag([1,np.sqrt(1-g)])]+[P[0]]*3),kron([np.array([[0,np.sqrt(g)],[0,0]])]+[P[0]]*3)]
C=np.block([[np.eye(d),np.zeros((d,d))],[np.zeros((d,d)),S]])
rho=np.kron(np.ones((2,2))/2,np.eye(d)/d);rho=C@rho@C;rho=sum(np.kron(np.eye(2),A)@rho@np.kron(np.eye(2),A.conj().T) for A in Ks);rho=C@rho@C
q=(1-np.trace(np.kron(P[1],np.eye(d))@rho).real)/2;delta=1-sum(np.trace(S@A.conj().T@S@A).real for A in Ks)/d
assert abs(q-delta/2)<1e-12
print(json.dumps({'seed':2026102903,'checks':rows,'actual_controlled_swap_test':{'q_minus':q,'delta_over_two':delta/2}},indent=2))
