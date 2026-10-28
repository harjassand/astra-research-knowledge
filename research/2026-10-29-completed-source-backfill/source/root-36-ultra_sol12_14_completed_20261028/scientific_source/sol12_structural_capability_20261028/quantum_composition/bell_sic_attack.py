"""Bell/SIC reduction and finite conditional-curvature attack; no global proof."""
import numpy as np
from pathlib import Path
import json,time
OUT=Path(__file__).resolve().parent/'outputs';OUT.mkdir(exist_ok=True)
w=np.exp(2j*np.pi/3);S=[];B=[]
for a in range(3):
 for b in range(3):
  v=np.zeros(3,dtype=complex);v[(a+1)%3]=1/np.sqrt(2);v[(a+2)%3]=-w**(-b)/np.sqrt(2)
  S.append(np.outer(v,v.conj()));q=np.zeros((3,3),dtype=complex)
  for j in range(3):q[j,(j+a)%3]=w**(b*j)/np.sqrt(3)
  B.append(np.outer(q.ravel(),q.ravel().conj()))
S=np.array(S);B=np.array(B)
def N(X):return (np.kron(np.eye(3),np.einsum('ibic->bc',X.reshape(3,3,3,3)))-X.reshape(3,3,3,3).transpose(2,1,0,3).reshape(9,9))/2
perm=[3*((u+d)%3)+(u+2*d)%3 for u in range(3) for d in range(3)]
for i in range(9):assert np.max(np.abs(N(B[i])[np.ix_(perm,perm)]-np.kron(np.eye(3)/3,S[i])))<2e-15
def curvature(p):
 M=np.einsum('i,ijk->jk',p,S);e,U=np.linalg.eigh(M)
 d=e[:,None]-e[None,:];l=np.log(e);q=np.empty((3,3));near=np.abs(d)<1e-10
 np.divide(l[:,None]-l[None,:],d,out=q,where=~near);q[near]=2/(e[:,None]+e[None,:])[near]
 T=np.einsum('ab,ibc,cd->iad',U.conj().T,S,U)
 gram=np.real(np.einsum('iab,jab,ab->ij',T.conj(),T,q))
 h=np.diag(1/p)-2*gram;head=int(np.argmax(p));ix=[i for i in range(9) if i!=head];D=np.zeros((9,7))
 for j in range(7):D[ix[j],j]=1;D[ix[-1],j]=-1
 ev,V=np.linalg.eigh(D.T@h@D);direction=D@V[:,0];direction/=np.linalg.norm(direction)
 return float(ev[0]),head,direction
if __name__=='__main__':
 start=time.perf_counter();rng=np.random.default_rng(123489);worst=None;seen=0
 for _ in range(5000):
  alpha=10**rng.uniform(-1.2,1.2);p=rng.dirichlet(np.full(9,alpha))
  if min(p)<1e-12:continue
  val,head,direction=curvature(p);seen+=1
  if worst is None or val<worst['minimum_eigenvalue']:
   worst={'probabilities':p.tolist(),'head':head,'direction':direction.tolist(),'minimum_eigenvalue':val}
 result={'status':'FLOATING_DIAGNOSTIC_NOT_CERTIFIED','samples':seen,'worst_conditional_curvature':worst,
  'elapsed_seconds':time.perf_counter()-start,'scope':'head fixed; other probabilities sum fixed; no global WH3 conclusion'}
 (OUT/'SIC_CURVATURE_DIAGNOSTIC.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
