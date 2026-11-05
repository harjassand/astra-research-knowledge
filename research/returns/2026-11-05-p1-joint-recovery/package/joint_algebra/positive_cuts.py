from pathlib import Path
ROOT = str(Path(__file__).resolve().parent) + "/"
import numpy as np, sys, json
from scipy.linalg import eigh
from singlet_singular import basis, schur, singlet_T

def cuts(n):
 d=2**n; m=d//2; dat=np.load(f'{ROOT}weak_n{n}.npz'); B=basis(n); H=dat['H']
 X=np.einsum('i,ijk->jk',dat['vs'][:,1],B)
 if np.linalg.norm(X-X.conj().T)>np.linalg.norm(X+X.conj().T): X=X*1j
 X=(X+X.conj().T)/2; X=X/np.linalg.norm(X)*np.sqrt(d)
 levels=[]
 for jj,ws in schur(n).items():
  R=np.array([[np.trace(a.T@X@b)/(jj+1) for b in ws] for a in ws]); ee,vv=eigh(R)
  for k,v in enumerate(ee):
   W=sum(vv[a,k]*ws[a] for a in range(len(ws)))
   levels.append((float(v),jj+1,W@W.conj().T))
 levels.sort(key=lambda item:item[0])
 def energy(Ps):
  v=np.array([np.einsum('ijk,jk->i',B.conj(),P) for P in Ps])
  return float(np.einsum('xi,ij,xj->',v.conj(),H,v).real/d)
 bins=[]; cur=np.zeros((d,d),complex);rank=0; ranks=[]
 if max(r for v,r,P in levels)<=m:
  for val,r,P in levels:
   if rank+r>m: bins.append(cur);ranks.append(rank);cur=np.zeros((d,d),complex);rank=0
   cur+=P;rank+=r
  bins.append(cur);ranks.append(rank)
 else: bins=[]
 qcuts=[];P=np.zeros((d,d),complex);rank=0
 for idx,(val,r,p) in enumerate(levels[:-1]):
  P+=p;rank+=r
  qcuts.append(dict(cut=idx,rank=rank,rankfrac=rank/d,gap=levels[idx+1][0]-val,energy=energy([P,np.eye(d)-P])))
 best_unbalanced=min(qcuts,key=lambda v:v['energy'])
 largest_gap=max(qcuts,key=lambda v:v['gap'])
 out=dict(n=n,gamma=float(dat['eigs'][1]),mincut=best_unbalanced,gapcut=largest_gap,balanced_ranks=ranks,balanced_energy=energy(bins) if bins else None,levels=[[v,r] for v,r,P in levels])
 # finite-angle exact H = I - T T*, using reversed physical cut if needed; energy on Hermitian real invariant cuts insensitive transpose orientation summed.
 if bins:
  v=np.array([np.einsum('ijk,jk->i',B.conj(),P) for P in bins]); out['finite']=[]
  for th in [.03,.1,.3,.7]:
   T=singlet_T(n,th,B); hp=np.eye(len(B))-T.conj().T@T
   e=float(np.einsum('xi,ij,xj->',v.conj(),hp,v).real/d)
   out['finite'].append([th,e,e/th**4])
 print(json.dumps(out),flush=True)

if __name__=='__main__':
 for n in range(2,int(sys.argv[1])+1): cuts(n)
