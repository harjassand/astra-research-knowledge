"""Dense small-dimensional checks; not a succinct implementation or proof."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(3110)
rows=[]
for d in range(2,8):
 rates=rng.uniform(.1,1,(d,d));np.fill_diagonal(rates,0)
 A=rates-np.diag(rates.sum(axis=0))
 mat=A.copy();mat[-1,:]=1;rhs=np.zeros(d);rhs[-1]=1;pi=np.linalg.solve(mat,rhs)
 psi=np.sqrt(pi);P=np.outer(psi,psi);Q=np.eye(d)-P
 H=np.zeros((d,d),complex);Ls=[]
 for x in range(d):
  for y in range(d):
   if x==y:continue
   H[x,y]=-.5j*(rates[y,x]*np.sqrt(pi[x]/pi[y])-rates[x,y]*np.sqrt(pi[y]/pi[x]))
   L=np.zeros((d,d));L[y,x]=np.sqrt(rates[y,x]);L[y,y]=-np.sqrt(rates[y,x]*pi[x]/pi[y]);Ls.append(L)
 def dual(D):
  out=1j*(H@D-D@H)
  for L in Ls:
   M=L.T@L;out=out+L.T@D@L-(M@D+D@M)/2
  return out
 def forward(R):
  out=-1j*(H@R-R@H)
  for L in Ls:
   M=L.T@L;out=out+L@R@L.T-(M@R+R@M)/2
  return out
 C=sum(L.T@P@L for L in Ls)
 errors=[np.linalg.norm(H-H.conj().T),np.linalg.norm(H@psi),np.linalg.norm(forward(P)),np.linalg.norm(dual(Q)+C)]
 for j in range(d):
  D=np.diag(np.eye(d)[j]);expected=np.diag(A.T@np.eye(d)[j]);errors.append(np.linalg.norm(dual(D)-expected))
 S=np.diag(np.sqrt(pi))@A.T@np.diag(1/np.sqrt(pi));g=np.linalg.eigvalsh(-(S+S.T)/2)[1]
 c=np.linalg.eigvalsh(C)[1];assert c>=2*pi.min()*g-1e-10
 assert max(errors)<1e-10
 rows.append({'dimension':d,'max_identity_residual':float(max(errors)),'actual_return_rate':float(c),'gap_lower_bound':float(2*pi.min()*g)})
for d in range(2,9):
 C=sum((np.outer(np.eye(d)[x]-np.eye(d)[y],np.eye(d)[x]-np.eye(d)[y])/d**2 for x in range(d) for y in range(d) if x!=y))
 assert np.allclose(C,2/d*(np.eye(d)-np.ones((d,d))/d))
r={'scope':'Dense algebraic diagnostics only; no novelty or scalable circuit claim','cases':rows,'complete_refresh_dimensions':list(range(2,9))}
Path(__file__).with_name('edge_lift_checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
