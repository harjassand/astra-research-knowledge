import numpy as np,json
from scipy.linalg import expm
from itertools import permutations
from pathlib import Path
rng=np.random.default_rng(295132);I=np.eye(2);sig=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def kron(xs):
 a=np.ones((1,1))
 for x in xs:a=np.kron(a,x)
 return a
def kraus(dim,r):
 ks=[rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim)) for _ in range(r)]
 z=sum(k.conj().T@k for k in ks);e,v=np.linalg.eigh(z);z=(v/np.sqrt(e))@v.conj().T
 return [k@z for k in ks]
def rotation():
 q,r=np.linalg.qr(rng.normal(size=(3,3)));q[:,0]*=np.linalg.det(q);return q
mom=[]
for case in range(8):
 ks=kraus(4,3);C=rotation();S=(np.eye(4)+sum(C[a,b]*np.kron(sig[a],sig[b]) for a in range(3) for b in range(3)))/2
 delta=1-sum(np.trace(S@k.conj().T@S@k).real for k in ks)/4
 first=second=0
 for c in range(3):
  for d in range(3):
   for u in [-1,1]:
    for v in [-1,1]:
     rho=np.kron((I+u*sig[c])/2,(I+v*sig[d])/2);out=sum(k@rho@k.conj().T for k in ks)
     for a in range(3):
      for b in range(3):
       for y in [-1,1]:
        for z in [-1,1]:
         prob=np.trace(np.kron((I+y*sig[a])/2,(I+z*sig[b])/2)@out).real/324
         loss=.75-2.25*y*z*C[a,b]-20.25*y*z*u*v*C[a,b]*C[c,d]
         first+=prob*loss;second+=prob*loss*loss
 assert abs(first-delta)<1e-11 and abs(second-(747/16+1.5*delta))<1e-10
 mom.append({'case':case,'delta':delta,'first_residual':abs(first-delta),'second_residual':abs(second-(747/16+1.5*delta))})
n=4;D=16;sw=[]
for i in range(1,n):
 S=np.zeros((D,D))
 for x in range(D):
  bits=[(x>>(n-1-j))&1 for j in range(n)];bits[0],bits[i]=bits[i],bits[0];y=sum(b<<(n-1-j) for j,b in enumerate(bits));S[y,x]=1
 sw.append(S)
L=sum(np.eye(D*D)-np.kron(S,S) for S in sw);spectrum=np.linalg.eigvalsh(L);gap=min(spectrum[spectrum>1e-8]);assert abs(gap-1)<1e-10
J=[sum(kron([sig[a] if i==j else I for i in range(n)]) for j in range(n))/2 for a in range(3)];vals,V=np.linalg.eigh(sum(j@j for j in J));V=V[:,abs(vals)<1e-8];P=V@V.conj().T;d=V.shape[1]
rows=[]
for case in range(20):
 ks=kraus(D*2,3);de=np.zeros((2,2),complex)
 for S in sw:
  Sf=np.kron(S,I);C=sum((Sf@k-k@Sf).conj().T@(Sf@k-k@Sf) for k in ks)
  de+=np.einsum('iaib->ab',C.reshape(D,2,D,2))/(2*D)
 Bs=[np.einsum('ij,jaib->ab',P,k.reshape(D,2,D,2))/d for k in ks]
 H=I-sum(b.conj().T@b for b in Bs);res=np.linalg.eigvalsh(H-D/d*de).max()
 assert res<1e-10
 rows.append({'case':case,'largest_operator_transfer_residual':res,'max_raw_bad_effect':np.linalg.eigvalsh(H).max()})
# Quadratic common-zero approximation: exact collective source, arbitrary nearby frame.
quad=[]
for case in range(20):
 U=expm(-1j*(.7*J[0]+.3*J[2]@J[2]));a=rng.normal(size=3);theta=np.linalg.norm(a);u=expm(-1j*sum(a[j]*sig[j] for j in range(3))/2);W=kron([I,u,I,I]);S=W@sw[0]@W.conj().T
 loss=np.linalg.norm(S@U-U@S,'fro')**2/(2*D);C=np.array([[np.trace(sig[a]@u@sig[b]@u.conj().T).real/2 for b in range(3)] for a in range(3)])
 bound=4.5*np.linalg.norm(C-np.eye(3),'fro')**2;assert loss<=bound+1e-10
 quad.append({'loss':loss,'quadratic_bound':bound})
Path(__file__).with_suffix('.json').write_text(json.dumps({'moment_checks':mom,'star_conjugation_gap':gap,'joint_memory_operator_transfer':rows,'quadratic_common_zero':quad,'scope':'Independent small exact-channel numerical tests, not finite online deployed protocol.'},indent=2));print('PASS 8 moments,20 joint-memory effects,20 quadratic cases; star gap',gap)
