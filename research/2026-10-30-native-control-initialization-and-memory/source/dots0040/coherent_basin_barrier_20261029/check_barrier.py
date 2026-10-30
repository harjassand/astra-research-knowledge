import numpy as np,itertools,json
rng=np.random.default_rng(29)
n=6; theta=.03; a=.3; eta=.4; lam=1.
animals=[]
for m in range(1,n+1):
 for A in itertools.combinations(range(n),m):
  seen={A[0]}
  while True:
   nxt=seen|{v for v in A if (v-1)%n in seen or (v+1)%n in seen}
   if nxt==seen:break
   seen=nxt
  if len(seen)==len(A):animals.append(A)
xs=np.array(list(itertools.product([0,1],repeat=n)))
F=np.array([[np.exp(a*len(A))*theta**(len(A)-sum(x[list(A)])) for A in animals] for x in xs])
v=F.sum(1);w=F@np.array([len(A) for A in animals]);V=np.diag(v)
k=np.array([[sum(x[list(A)]) for A in animals] for x in xs]);drift=-lam*(1-theta)*(F*k).sum(1)
kappa=lam*(1-theta)*eta
sparse=(F*np.array([len(A) for A in animals])*(k<eta*np.array([len(A) for A in animals]))).sum(1)
assert np.max(drift+kappa*w-kappa*sparse)<1e-8
# physical Z={0,1}: same last 4 bits defines orbit; local operator via kron
osc=np.zeros(2**n)
for suffix in itertools.product([0,1],repeat=n-2):
 inds=[i for i,x in enumerate(xs) if tuple(x[2:])==suffix]
 osc[inds]=max(v[inds])-min(v[inds])
Omega=np.diag(osc);A=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));h=(A+A.conj().T)/2
K=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
H=np.kron(h,np.eye(2**(n-2)));J=np.kron(K,np.eye(2**(n-2)))
comm=1j*(H@V-V@H);diss=J.conj().T@V@J-(J.conj().T@J@V+V@J.conj().T@J)/2
rh=2*np.linalg.norm(h,2)*Omega-comm;rk=2*np.linalg.norm(K,2)**2*Omega-diss
out={'n':n,'animals':len(animals),'Hamiltonian_Loewner_min_eigenvalue':float(np.linalg.eigvalsh(rh).min()),'Lindblad_Loewner_min_eigenvalue':float(np.linalg.eigvalsh(rk).min()),'independent_healing_drift_max_violation':float(np.max(drift+kappa*w-kappa*sparse)),'initial_V_over_N':float(v[0]/n),'max_required_b_finite_example':float(np.max(drift+kappa*w)/n)}
assert out['Hamiltonian_Loewner_min_eigenvalue']>-1e-8
assert out['Lindblad_Loewner_min_eigenvalue']>-1e-8
print(json.dumps(out,indent=2))
