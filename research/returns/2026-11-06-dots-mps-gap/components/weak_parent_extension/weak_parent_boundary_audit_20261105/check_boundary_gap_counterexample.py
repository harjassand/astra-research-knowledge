"""Finite spectra and trial-state checks for the closing-open-gap example."""
import numpy as np
from pathlib import Path
from scipy.sparse import csr_matrix,kron,eye
from scipy.sparse.linalg import eigsh
import json
q=.5; lam=[0,q,1/q]; d=3
h=np.zeros((9,9)); vac=np.zeros(9); vac[0]=1
for s in [1,2]:
 p=np.zeros(9); p[s]=1; p[3*s]=-lam[s]; p/=np.linalg.norm(p); h+=np.outer(p,p)
for s in [1,2]:
 for t in [1,2]:h[3*s+t,3*s+t]=1
alpha=np.array([0, q*q/(1+q*q),1/(1+q*q)])
# X_s=alpha_s-1/2 for occupied species; X_0=0
X=np.diag([0,alpha[1]-.5,alpha[2]-.5]); number=np.diag([0,1,1]); g=(1-q)**2/(1+q*q)
hprime=h-np.kron(X,np.eye(3))+np.kron(np.eye(3),X)
margin=hprime-g/2*(np.kron(number,np.eye(3))+np.kron(np.eye(3),number))
results={'q':q,'g':g,'h_eigenvalues':np.linalg.eigvalsh(h).tolist(),'hprime_eigenvalues':np.linalg.eigvalsh(hprime).tolist(),'local_bound_eigenvalues':np.linalg.eigvalsh(margin).tolist(),'sizes':[]}
def opbond(N,i,j):
 rows=[];cols=[];vals=[]
 for a in range(3**N):
  digits=[a//3**(N-1-r)%3 for r in range(N)]
  ij=digits[i]*3+digits[j]
  for kl in range(9):
   if abs(h[kl,ij])>1e-14:
    b=a+(kl//3-digits[i])*3**(N-1-i)+(kl%3-digits[j])*3**(N-1-j)
    rows.append(b);cols.append(a);vals.append(h[kl,ij])
 return csr_matrix((vals,(rows,cols)),shape=(3**N,3**N))
for N in range(3,8):
 H=sum(opbond(N,i,i+1) for i in range(N-1)); Hp=H+opbond(N,N-1,0)
 ev=np.linalg.eigvalsh(H.toarray())
 ep=np.linalg.eigvalsh(Hp.toarray())
 psi=np.zeros(3**N)
 for x in range(N):
  for y in range(x+1,N):psi[3**(N-1-x)+2*3**(N-1-y)]=q**(x+N-1-y)
 psi/=np.linalg.norm(psi)
 E=float(psi@H@psi); formula=(N-1)*q**(2*N-4)/sum((k+1)*q**(2*k) for k in range(N-1))
 results['sizes'].append({'N':N,'open_first_eigenvalues':ev[:8].tolist(),'periodic_first_eigenvalues':ep[:5].tolist(),'trial_energy':E,'formula':formula})
print(json.dumps(results,indent=2))
(Path(__file__).resolve().parent/'boundary_gap_counterexample_results.json').write_text(json.dumps(results,indent=2)+'\n')
