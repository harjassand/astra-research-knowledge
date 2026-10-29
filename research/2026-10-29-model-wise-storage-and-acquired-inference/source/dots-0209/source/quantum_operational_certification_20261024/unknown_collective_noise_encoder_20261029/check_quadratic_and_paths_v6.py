import numpy as np,json,math
from functools import reduce,lru_cache
from scipy.linalg import expm,eigh
rng=np.random.default_rng(2026102902)
@lru_cache(None)
def F(m,h):
 if h<0 or h>m:return 0
 if m==0:return int(h==0)
 return F(m-1,h+1)+(F(m-1,h-1) if h else 0)
def unrank(n,x):
 h=0;p=[]
 for m in range(n,0,-1):
  d=F(m-1,h-1) if h else 0
  if x<d:p.append(-1);h-=1
  else:p.append(1);h+=1;x-=d
 assert x==h==0
 return p
def rank(p):
 x=h=0
 for i,a in enumerate(p):
  if a==1:x+=F(len(p)-i-1,h-1) if h else 0
  h+=a
 return x
paths=[]
for n in range(2,20,2):
 count=F(n,0);assert count==math.comb(n,n//2)//(n//2+1)
 for x in range(count):assert rank(unrank(n,x))==x
 paths.append({'n':n,'paths':count,'logical_qubits':count.bit_length()-1})
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
kron=lambda xs:reduce(np.kron,xs)
n=4;J=[sum(kron([P[a] if i==j else np.eye(2) for i in range(n)]) for j in range(n))/2 for a in range(3)]
v,Z=eigh(sum(x@x for x in J));E=Z[:,v<1e-9];Proj=E@E.conj().T;Q=np.eye(16)-Proj
H=sum(np.kron(J[a],P[a]) for a in range(3))+np.kron(np.eye(16),.3*P[2]);U0=lambda t:expm(-1j*t*.3*P[2])
axes=rng.normal(size=(4,3));axes/=np.linalg.norm(axes,axis=1)[:,None]
rows=[]
for scale in [.001,.003,.01,.03,.1]:
 W=kron([expm(-.5j*scale*np.einsum('a,aij->ij',ax,P)) for ax in axes]);S=W@E;L=Q@S;ell=np.linalg.norm(L,2)
 for t in [1,10,100]:
  U=expm(-1j*t*H);A=np.kron(S.conj().T,np.eye(2))@U@np.kron(S,np.eye(2))
  ideal=np.kron(np.eye(2),U0(t))
  rhs=np.kron(L.conj().T,np.eye(2))@(U-np.kron(np.eye(16),U0(t)))@np.kron(L,np.eye(2))
  residual=np.linalg.norm(A-ideal-rhs,2)
  bad=np.kron(np.eye(16)-S@S.conj().T,np.eye(2))@U@np.kron(S,np.eye(2))
  good=np.linalg.norm(A-ideal,2);badn=np.linalg.norm(bad,2)
  assert residual<1e-11 and good<=2*ell**2+1e-11 and badn<=2*ell+1e-11
  rows.append({'scale':scale,'time':t,'ell':float(ell),'return_amplitude_error':float(good),'quadratic_upper_bound':float(2*ell**2),'leakage_amplitude':float(badn),'identity_residual':float(residual)})
print(json.dumps({'seed':2026102902,'dyck_all_ranks_checked':paths,'quadratic_checks':rows},indent=2))
