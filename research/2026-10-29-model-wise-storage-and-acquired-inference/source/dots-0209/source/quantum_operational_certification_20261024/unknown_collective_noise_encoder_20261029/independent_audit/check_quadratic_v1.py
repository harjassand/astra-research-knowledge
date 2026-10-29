import numpy as np,json
from scipy.linalg import expm,block_diag
from pathlib import Path
rng=np.random.default_rng(129381)
def unitary(d):
 a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));q,r=np.linalg.qr(a);return q
D=7;r=3;k=2;b=2
E=np.eye(D,dtype=complex)[:,:k];Q=np.diag([0]*r+[1]*(D-r));Pi=np.eye(D)-Q
max_identity_error=0.;max_good_ratio=0.;max_bad_ratio=0.
rows=[]
for trial in range(200):
 U0=unitary(b);UQ=unitary((D-r)*b);U=block_diag(np.kron(np.eye(r),U0),UQ)
 h=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));h=(h+h.conj().T)/2;h/=np.linalg.norm(h,2)
 t=float(10**rng.uniform(-3,-.1));W=expm(1j*t*h);S=W@E;L=Q@S;ell=np.linalg.norm(L,2)
 Sk=np.kron(S,np.eye(b));A=Sk.conj().T@U@Sk;ideal=np.kron(np.eye(k),U0)
 Lq=np.kron(L[r:,:],np.eye(b));expected=Lq.conj().T@(UQ-np.kron(np.eye(D-r),U0))@Lq
 err=np.linalg.norm(A-ideal-expected,2);max_identity_error=max(max_identity_error,float(err));assert err<1e-12
 good=np.linalg.norm(A-ideal,2)/(2*ell**2);assert good<=1+1e-9;max_good_ratio=max(max_good_ratio,float(good))
 bad=np.kron(np.eye(D)-S@S.conj().T,np.eye(b))@U@Sk
 br=np.linalg.norm(bad,2)/(2*ell);assert br<=1+1e-9;max_bad_ratio=max(max_bad_ratio,float(br))
 # Bell input and bath |0>: code contribution is exact for orthogonal erasure.
 bell=Sk@np.kron(np.eye(k),np.array([[1.],[0.]])) # columns map logical to system,bath
 out=U@bell;dec=Sk.conj().T@out
 kraus=[dec.reshape(k,b,k)[:,j,:] for j in range(b)]
 Fe=sum(abs(np.trace(x))**2 for x in kraus)/(k*k)
 assert 1-Fe<=8*ell**2+1e-12
 if trial<3:rows.append({'t':t,'ell':float(ell),'Fe_erasure':float(Fe),'diamond_bound':float(8*ell**2)})
# Independent DP rank/unrank exact exhaustiveness for small even n.
import math
for n in range(2,18,2):
 f=np.zeros((n+1,n+2),dtype=object);f[0,0]=1
 for m in range(1,n+1):
  for h in range(n+1):f[m,h]=f[m-1,h+1]+(f[m-1,h-1] if h else 0)
 cat=math.comb(n,n//2)//(n//2+1);assert f[n,0]==cat
 def unrank(x):
  h=0;path=[]
  for m in range(n,0,-1):
   dd=f[m-1,h-1] if h else 0
   if x<dd:h-=1;path.append(-1)
   else:x-=dd;h+=1;path.append(1)
  assert x==0 and h==0;return path
 def rank(path):
  h=0;x=0
  for m,step in zip(range(n,0,-1),path):
   if step==1:x+=f[m-1,h-1] if h else 0
   h+=step;assert h>=0
  return x
 for x in range(cat):assert rank(unrank(x))==x
out={'seed':129381,'quadratic_cases':200,'max_identity_roundoff':max_identity_error,'max_good_amplitude_bound_ratio':max_good_ratio,'max_leakage_amplitude_bound_ratio':max_bad_ratio,'examples':rows,'dyck_exhaustive_even_n_through':16,'all_passed':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
