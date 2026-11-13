"""Diagonal-frame MPS quantum trajectories. No claim of scalable certified rank."""
import numpy as np,time,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'frame_sampler'))
from sampler import plan,PHI,A,B
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);SWAP=np.eye(4)[[0,2,1,3]]
Q=A*np.eye(4)-1j*B*np.kron(X,X)
def zz(theta):return np.diag(np.exp(1j*theta*np.array([1,-1,-1,1])))
class ResourceLimit(Exception):
 pass
class MPS:
 def __init__(self,n,chi=None,tol=0,strict=False):
  self.strict=strict
  self.ts=[np.array([1,0],complex).reshape(1,2,1) for _ in range(n)];self.center=0;self.chi=chi;self.tol=tol;self.error=0.;self.maxchi=1;self.truncations=0;self.svds=0;self.peakbytes=16*2*n
 def move(self,i):
  while self.center<i:
   j=self.center;t=self.ts[j];l,d,r=t.shape;q,s=np.linalg.qr(t.reshape(l*d,r));self.ts[j]=q.reshape(l,d,-1);self.ts[j+1]=np.einsum('ab,bsc->asc',s,self.ts[j+1]);self.center+=1
  while self.center>i:
   j=self.center;t=self.ts[j];l,d,r=t.shape;q,s=np.linalg.qr(t.reshape(l,d*r).T);self.ts[j]=q.T.reshape(-1,d,r);self.ts[j-1]=np.einsum('asb,bc->asc',self.ts[j-1],s.T);self.center-=1
 def adj(self,i,g):
  self.move(i);t=np.einsum('asb,btc->astc',self.ts[i],self.ts[i+1]);l,_,_,r=t.shape;t=np.einsum('uvst,astb->auvb',g.reshape(2,2,2,2),t).reshape(2*l,2*r)
  u,s,v=np.linalg.svd(t,full_matrices=False);self.svds+=1;w=s*s;total=sum(w);rank=len(s)
  # tol is an amplitude error allowance at EACH SVD (zero means exact).
  if self.tol>0:
   for k in range(1,len(s)+1):
    if sum(w[k:])<=self.tol**2*total:rank=k;break
  if self.chi is not None and rank>self.chi and self.strict:
   raise ResourceLimit(dict(aborted=True,required_bond=rank,max_bond=self.maxchi,path_error_sum=float(self.error),svds=self.svds,peak_array_bytes=self.peakbytes))
  if self.chi is not None:rank=min(rank,self.chi)
  lost=float(sum(w[rank:])/total);self.error+=np.sqrt(max(0,lost));self.truncations+=int(lost>1e-28)
  s=s[:rank]/np.sqrt(max(1e-300,1-lost));self.ts[i]=u[:,:rank].reshape(l,2,rank);self.ts[i+1]=(s[:,None]*v[:rank]).reshape(rank,2,r);self.center=i+1;self.maxchi=max(self.maxchi,rank);self.peakbytes=max(self.peakbytes,sum(x.nbytes for x in self.ts)+t.nbytes+u.nbytes+v.nbytes)
 def pair(self,i,j,g):
  if i>j:i,j=j,i;g=SWAP@g@SWAP
  for k in range(j-1,i,-1):self.adj(k,SWAP)
  self.adj(i,g)
  for k in range(i+1,j):self.adj(k,SWAP)
 def one(self,i,g):self.ts[i]=np.einsum('st,atb->asb',g,self.ts[i])
 def measure(self,i,rng,forced=None):
  self.move(i);p1=float(np.sum(abs(self.ts[i][:,1,:])**2));b=int(rng.random()<np.clip(p1,0,1)) if forced is None else forced;p=p1 if b else 1-p1
  if p<1e-16:raise ArithmeticError('Unsupported zero probability')
  self.ts[i][:,1-b,:]=0;self.ts[i]/=np.sqrt(p);return b,p
 def vector(self):
  v=self.ts[0]
  for t in self.ts[1:]:v=np.tensordot(v,t,axes=(-1,0))
  # reverse tensor axes to little-endian dense vector
  n=len(self.ts);return v.reshape([2]*n).transpose(list(range(n-1,-1,-1))).ravel()
class MPOMPS(MPS):
 def pair(self,i,j,g):
  if i>j:i,j=j,i;g=SWAP@g@SWAP
  if j==i+1:return self.adj(i,g)
  a=np.trace(g)/4
  pp=Z if abs(np.trace(np.kron(Z,Z)@g))>1e-12 else X
  b=np.trace(np.kron(pp,pp)@g)/4
  if np.max(abs(g-a*np.eye(4)-b*np.kron(pp,pp)))>1e-10:raise ValueError('MPO backend only supports I+Pauli product')
  t=self.ts[i];pt=np.einsum('st,atb->asb',pp,t);self.ts[i]=np.concatenate([a*t,b*pt],axis=2)
  for k in range(i+1,j):
   t=self.ts[k];l,d,r=t.shape;z=np.zeros((2*l,d,2*r),complex);z[:l,:,:r]=t;z[l:,:,r:]=t;self.ts[k]=z
  t=self.ts[j];pt=np.einsum('st,atb->asb',pp,t);self.ts[j]=np.concatenate([t,pt],axis=0)
  # Re-establish canonical form after exact MPO application, then compress.
  self.center=len(self.ts)-1;self.move(0)
  for k in range(i,j):self.adj(k,np.eye(4))

def sample(n,layers,r,eps,rng,chi=None,tol=0,validate=False,physical=False,distribution=False,basis_prune=True,strict=False,ordering=None,mpo=False):
 start=time.perf_counter();records,roots,supports,neigh=plan(n,layers,r,eps,rng);m=(MPOMPS if mpo else MPS)(n,chi,tol,strict);counts={tuple(sorted((u,v))):0 for u in range(n) for v in neigh[u] if u<v};direct=np.zeros(1<<n,complex) if validate else None
 if validate:direct[0]=1
 if ordering is not None:
  from ordering_pre_cancellation import OrderedMPS,choose_order
  order=choose_order(n,records,neigh,ordering,physical)
  m=OrderedMPS(m,order)
 bornerr=0.;rare=0;resets=0;known=[0]*n;skipped=0
 def phasepair(u,v,theta):
  nonlocal skipped
  if basis_prune and (known[u] is not None or known[v] is not None):
   skipped+=1
   if known[u] is not None and known[v] is not None:return # irrelevant global phase
   if known[v] is not None:u,v=v,u
   m.one(v,np.diag(np.exp(1j*theta*(1-2*known[u])*np.array([1,-1]))))
  else:m.pair(u,v,zz(theta))
 from sampler import bitphase,qgate,project
 for ev,cuts,before,after in records:
  for (u,v),reset,israre,cand in ev:
   counts[tuple(sorted((u,v)))]+=1
   if physical:phasepair(u,v,PHI)
   if validate:direct*=bitphase(n,[u,v],PHI)
  for (u,v),reset,israre,cand in ev:
   if not israre:continue
   rare+=1;edges=[(e,k) for e,k in counts.items() if k and (u in e or v in e)]
   if not physical:
    for e,k in edges:phasepair(*e,k*PHI)
   m.pair(u,v,Q);known[u]=None;known[v]=None
   if not physical:
    for e,k in reversed(edges):phasepair(*e,-k*PHI)
   if validate:direct=qgate(direct,(1<<u)|(1<<v))
  for (u,v),reset,israre,cand in ev:
   if not reset:continue
   resets+=1;aa=[]
   for s in(u,v):
    a,p=m.measure(s,rng);aa.append(a)
    if validate:direct,pd=project(direct,s,a);bornerr=max(bornerr,abs(pd-p))
   bb=[int(rng.integers(2)),int(rng.integers(2))]
   for s,a,b in zip((u,v),aa,bb):
    known[s]=b
    if a!=b:
     m.one(s,X)
     if validate:direct=direct[np.arange(1<<n)^(1<<s)]
   if not physical:
    for s,a,b in zip((u,v),aa,bb):
     for w in neigh[s]-{u,v}:m.one(w,np.diag(np.exp(1j*counts[tuple(sorted((s,w)))]*PHI*((1-2*a)-(1-2*b))*np.array([1,-1]))))
 stats=dict(skipped_basis_pair_gates=skipped,seconds=time.perf_counter()-start,max_bond=m.maxchi,svds=m.svds,truncations=m.truncations,path_error_sum=m.error,peak_array_bytes=m.peakbytes,rare=rare,resets=resets,born_error=bornerr,max_component=max(map(len,supports.values())))
 if validate or distribution:
  v=m.vector();p=abs(v)**2
  if validate:stats['conditional_TV']=float(sum(abs(p-abs(direct)**2))/2)
  if distribution:
   stats["seconds"]=time.perf_counter()-start
   return p,stats
 result=0
 for s in range(n):b,_=m.measure(s,rng);result|=b<<s
 stats["seconds"]=time.perf_counter()-start
 return result,stats


def safe_sample(*args,**kwargs):
 start=time.perf_counter()
 try:
  x,s=sample(*args,**kwargs);s['aborted']=False;s['seconds']=time.perf_counter()-start;return x,s
 except ResourceLimit as e:
  s=e.args[0];s['seconds']=time.perf_counter()-start;return 0,s
