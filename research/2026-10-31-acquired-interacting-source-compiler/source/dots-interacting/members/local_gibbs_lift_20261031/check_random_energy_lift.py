"""Small spectral diagnostics; eigenvalues do NOT certify a finite-time return norm."""
import json
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,eye,kron
from scipy.sparse.linalg import eigs
rows=[]
rng=np.random.default_rng(93471)
for n in [3,4,5]:
 d=1<<n
 spins=np.array([[1-2*((x>>i)&1) for i in range(n)] for x in range(d)])
 # Periodic bond sum counts both directed bonds when n=2; intentionally recorded.
 energy=rng.normal(size=d)
 for beta in [.5,1,2,4]:
  pi=np.exp(beta*(energy-energy.max()));pi/=pi.sum();psi=np.sqrt(pi)
  A=np.zeros((d,d));Ls=[]
  for i in range(n):
   rate=np.array([pi[x^(1<<i)]/(pi[x]+pi[x^(1<<i)]) for x in range(d)])
   for a in [0,1]:
    L=np.zeros((d,d))
    for x in range(d):
     if (x>>i)&1!=a:continue
     y=x^(1<<i);L[y,x]=np.sqrt(rate[x]);L[y,y]=-np.sqrt(rate[y])
    Ls.append(csr_matrix(L))
   for x in range(d):
    A[x^(1<<i),x]+=rate[x];A[x,x]-=rate[x]
  Id=eye(d,format='csr');Li=csr_matrix((d*d,d*d),dtype=float)
  dark=max(np.linalg.norm(L@psi) for L in Ls)
  for L in Ls:
   M=L.T@L;Li+=kron(L,L)-.5*(kron(Id,M)+kron(M.T,Id))
  vals=eigs(Li,k=min(10,d*d-2),which='LR',return_eigenvectors=False,tol=1e-10,maxiter=30000)
  vals=sorted(vals,key=lambda z:z.real,reverse=True)
  S=(A*pi[None,:]**.5)/pi[:,None]**.5
  cg=-np.linalg.eigvalsh(S)[-2]
  zero=sum(abs(z)<1e-8 for z in vals)
  qg=-max(z.real for z in vals if abs(z)>1e-8)
  r={'n':n,'beta':beta,'classical_gap':float(cg),'sampled_quantum_spectral_gap':float(qg),'ratio':float(qg/cg),'near_zero_among_top10':int(zero),'dark_residual':float(dark)}
  rows.append(r);print(json.dumps(r),flush=True)
  Path(__file__).with_name('random_energy_spectral_checks.json').write_text(json.dumps({'scope':'Small spectral diagnostics, not uniform mixing proof; random full-state energies, not local finite-range','rows':rows},indent=2)+'\n')
