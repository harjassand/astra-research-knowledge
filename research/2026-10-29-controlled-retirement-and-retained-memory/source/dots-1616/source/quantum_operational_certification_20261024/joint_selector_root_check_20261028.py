"""Independent physical CP-gauge checks. Deterministic algebra; zero source samples."""
import numpy as np,itertools,json,hashlib
from pathlib import Path
rng=np.random.default_rng(281541)
I=np.eye(2);P=[I,np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def iso(n,m):return np.linalg.qr(rng.normal(size=(n,m))+1j*rng.normal(size=(n,m)))[0][:,:m]
def sqrtpsd(A):
 w,v=np.linalg.eigh(A);return (v*np.sqrt(np.maximum(w,0)))@v.conj().T
phi=np.array([1,0,0,1])/np.sqrt(2)
maxres=0.;mineig=1.;cases=0
for m in (2,3,4):
 for trial in range(8):
  n=2*m;raw=[rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)) for _ in range(3)]
  total=sum(K.conj().T@K for K in raw);scale=np.sqrt(.3/np.linalg.norm(total,2));Ks=[scale*K for K in raw]
  H=sqrtpsd(np.eye(n)-2*sum(K.conj().T@K for K in Ks));U=iso(4,4)
  V=iso(8,4);Dks=[V.reshape(2,4,4)[:,j,:] for j in range(4)]
  oracle=[np.eye(4)[[j,2+j],:]@U.conj().T for j in range(2)]
  if trial%3==0:Dks=oracle
  elif trial%3==1:Dks=[np.sqrt(.001)*K for K in Dks]+[np.sqrt(.999)*K for K in oracle]
  vv=iso(2,2);sigma=vv@np.diag([.8,.2])@vv.conj().T
  def gauges(x):
   inp=np.kron(np.outer(x,x),sigma)
   def reduce(K):
    out=K@inp@K.conj().T
    return np.trace(out.reshape(2,m,2,m),axis1=1,axis2=3)
   gs=[reduce(K) for K in Ks];return [sum(gs)+reduce(H),*gs]
  def channel(x,rho):
   gs=gauges(x);out=U@sum(np.kron(a@rho@a.conj().T,g) for a,g in zip(P,gs))@U.conj().T
   return sum(K@out@K.conj().T for K in Dks)
  def bell(x):
   J=np.zeros((4,4),complex)
   for a in range(2):
    for b in range(2):
     e=np.zeros((2,2));e[a,b]=1;J+=np.kron(e,channel(x,e))/2
   return float((phi@J@phi).real)
  def risk(x):return np.trace(gauges(x)[0]).real-bell(x)
  B=np.diag([risk(np.eye(m)[i]) for i in range(m)])
  for i in range(m):
   for j in range(i):
    x=(np.eye(m)[i]+np.eye(m)[j])/np.sqrt(2);B[i,j]=B[j,i]=risk(x)-(B[i,i]+B[j,j])/2
  mineig=min(mineig,float(np.linalg.eigvalsh(B).min()))
  assert np.linalg.eigvalsh(B).min()>-1e-11
  for _ in range(15):
   x=rng.normal(size=m);x/=np.linalg.norm(x)
   maxres=max(maxres,abs(risk(x)-x@B@x));assert risk(x)<=np.trace(B)+1e-11
  # Reconstruct actual selector test effect and fourth-design expectation.
  A=np.diag([(2/3)*(1-bell(np.eye(m)[i])) for i in range(m)])
  for i in range(m):
   for j in range(i):
    x=(np.eye(m)[i]+np.eye(m)[j])/np.sqrt(2)
    A[i,j]=A[j,i]=(2/3)*(1-bell(x))-(A[i,i]+A[j,j])/2
  des=[(2/(m*(m+2)),np.eye(m)[i]) for i in range(m)]
  des +=[(m/((m+2)*2**m),np.array(s)/np.sqrt(m)) for s in itertools.product((-1,1),repeat=m)]
  moment=np.zeros((m,m))
  for pr,x in des:
   mismatch=1-sum(np.trace(r@channel(x,r)).real for r in [(I+s*pp)/2 for pp in P[1:] for s in (-1,1)])/6
   moment+=pr*mismatch*(m*(m+2)*np.outer(x,x)/2-m*np.eye(m)/2)
  maxres=max(maxres,float(np.linalg.norm(moment-A)))
  cases+=1
assert maxres<1e-10
q=Path(__file__).parent;s=q/'ordinary_joint_selector_decoder_prequential_20261028.md'
out={'kind':'independent physical algebra, zero source samples','physical_cases':cases,'selector_dimensions':[2,3,4],'output_dimension':4,'min_excess_eigenvalue':mineig,'max_identity_residual':maxres,'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'pass':True}
(q/'joint_selector_root_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
