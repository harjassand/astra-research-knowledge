from pathlib import Path
ROOT = str(Path(__file__).resolve().parent) + "/"
import numpy as np, sys,json
from scipy.linalg import eigh
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
from singlet_singular import basis,schur

def run(n):
 d=2**n;dat=np.load(f'{ROOT}weak_n{n}.npz'); B=basis(n);H=dat['H'];X=np.einsum('i,ijk->jk',dat['vs'][:,1],B)
 if np.linalg.norm(X-X.conj().T)>np.linalg.norm(X+X.conj().T):X*=1j
 X=(X+X.conj().T)/2;X=X/np.linalg.norm(X)*np.sqrt(d);levels=[]
 for jj,ws in schur(n).items():
  R=np.array([[np.trace(a.T@X@b)/(jj+1) for b in ws] for a in ws]);ee,vv=eigh(R)
  for k,v in enumerate(ee):
   W=sum(vv[a,k]*ws[a] for a in range(len(ws)));levels.append((float(v),jj+1,W@W.conj().T))
 levels.sort(key=lambda v:v[0]);L=len(levels);Ps=np.array([p for v,r,p in levels]);rs=np.array([r for v,r,p in levels]);V=np.einsum('ijk,ljk->li',B.conj(),Ps)
 M=(V.conj()@H@V.T).real/d;M=(M+M.T)/2;edges=[(i,j) for i in range(L) for j in range(i+1,L) if M[i,j]<-1e-12]
 nv=L+len(edges);C=np.zeros(nv);A=lil_matrix((2*len(edges)+1,nv));lo=np.full(2*len(edges)+1,-np.inf);hi=np.zeros(2*len(edges)+1)
 A[0,:L]=rs;lo[0]=hi[0]=d/2
 for k,(i,j) in enumerate(edges):
  z=L+k;C[z]=-2*M[i,j];A[2*k+1,i]=1;A[2*k+1,j]=-1;A[2*k+1,z]=-1;A[2*k+2,i]=-1;A[2*k+2,j]=1;A[2*k+2,z]=-1
 lower=np.zeros(nv);upper=np.ones(nv);lower[0]=1
 res=milp(C,integrality=np.r_[np.ones(L),np.zeros(len(edges))],bounds=Bounds(lower,upper),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':60})
 if res.x is None: print(json.dumps(dict(n=n,status=res.message)),flush=True);return
 x=np.rint(res.x[:L]).astype(int);P=np.einsum('i,ijk->jk',x,Ps);e=float(2*x@M@x)
 print(json.dumps(dict(n=n,energy=e,ranks=[int(rs@x),int(d-rs@x)],status=res.message,selection=x.tolist(),gap=float(dat['eigs'][1]))),flush=True)
 np.savez(f'{ROOT}balanced_cut_n{n}.npz',projectors=np.array([P,np.eye(d)-P]),energy=e)
if __name__=='__main__':
 for n in range(3,int(sys.argv[1])+1):run(n)
