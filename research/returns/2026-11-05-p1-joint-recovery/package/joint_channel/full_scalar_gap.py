import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator,eigsh
from math import sqrt
import sys,time

def paths(n):
 D=[()]
 for k in range(n):
  D=[p+(j,) for p in D for j in ((p[-1] if p else 0)+1,(p[-1] if p else 0)-1) if j>=0]
 return D

def adjacent(pp):
 n=len(pp[0]);ind={p:i for i,p in enumerate(pp)};r=len(pp)
 C=[]
 for p in pp:
  a=b=0;cc=[];prev=0
  for j in p:
   if j>prev:a+=1;cc.append(a-1)
   else:b+=1;cc.append(b-2)
   prev=j
  C.append(cc)
 S=[]
 for k in range(n-1):
  rows=[];cols=[];data=[]
  for i,p in enumerate(pp):
   dist=C[i][k+1]-C[i][k]
   rows.append(i);cols.append(i);data.append(1/dist)
   if abs(dist)>1:
    v=list(p);prev=p[k-1] if k else 0;v[k]=2*prev-p[k]
    j=ind[tuple(v)];rows.append(i);cols.append(j);data.append(sqrt(1-1/dist**2))
  S.append(csr_matrix((data,(rows,cols)),shape=(r,r)))
 return S

def monodromy(n,theta):
 bath=paths(n);bp={j:sorted([p for p in bath if p[-1]==j]) for j in range(n%2,n+1,2)}
 full=paths(n+1);blocks={};c=np.cos(theta);s=np.sin(theta)
 for K in range((n+1)%2,n+2,2):
  pp=sorted([p for p in full if p[-1]==K]);adj=adjacent(pp);r=len(pp)
  W=np.eye(r,dtype=complex)
  for bathindex in range(n):
   Z=W
   # swap(bathindex,n): s_i ... s_(n-2) s_(n-1) s_(n-2) ... s_i
   for k in list(range(bathindex,n))+list(range(n-2,bathindex-1,-1)):
    Z=adj[k]@Z
   W=c*W+1j*s*Z
  sub={}
  for j,ps in bp.items():
   idx=[pp.index(p+(K,)) for p in ps if abs(j-K)==1]
   if idx:sub[j]=np.array(idx)
  blocks[K]=(W,sub)
 return bp,blocks

def run(n,theta):
 bp,blocks=monodromy(n,theta);js=sorted(bp);mult={j:len(bp[j]) for j in js};offsets={};size=0
 for j in js:offsets[j]=size;size+=mult[j]**2
 def unpack(v):return {j:v[offsets[j]:offsets[j]+mult[j]**2].reshape(mult[j],mult[j])/sqrt(j+1) for j in js}
 def T(v,star=False):
  X=unpack(v);R={j:np.zeros_like(X[j],dtype=complex) for j in js}
  for K,(W,sub) in blocks.items():
   A=np.zeros_like(W)
   for j,ind in sub.items():A[np.ix_(ind,ind)]=X[j]
   if star:A=W.conj().T@A@W
   else:A=W@A@W.conj().T
   for j,ind in sub.items():R[j]+=(K+1)/(2*(j+1))*A[np.ix_(ind,ind)]
  return np.concatenate([sqrt(j+1)*R[j].reshape(-1) for j in js])
 ident=np.concatenate([sqrt(j+1)*np.eye(mult[j]).reshape(-1) for j in js])/sqrt(2**n)
 def gap(v):return v-T(T(v),True)
 def shifted(v):return gap(v)+2*ident*np.vdot(ident,v)
 L=LinearOperator((size,size),matvec=shifted,dtype=complex)
 if size<=10:val=np.linalg.eigvalsh(np.stack([shifted(v) for v in np.eye(size)],axis=1))
 else:val=eigsh(L,k=min(5,size-2),which='SA',tol=1e-9,maxiter=20000,return_eigenvectors=False)
 val=np.sort(val)
 print('n',n,'theta',theta,'dim',size,'vals',val,'lambda_scaled',val[0]/theta**4,'identerr',np.linalg.norm(gap(ident)),flush=True)

if __name__=='__main__':
 theta=float(sys.argv[1]);ns=list(map(int,sys.argv[2:] or [2,3,4,5,6,7,8]))
 for n in ns:
  st=time.time();run(n,theta);print('seconds',time.time()-st,flush=True)
