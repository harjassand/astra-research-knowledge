import numpy as np,json
from scipy.linalg import expm
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);Id=np.eye(8);IdS=np.eye(64)
kron=lambda a,b,c:np.kron(np.kron(a,b),c)
S=[kron(Z,Z,I),kron(I,Z,Z)];F=kron(X,I,I)
ad=lambda A:np.kron(A.conj(),A)
def diss(K):
 A=K.conj().T@K
 return ad(K)-.5*(np.kron(Id,A)+np.kron(A.T,Id))
# One actual syndrome-read/conditional-Pauli feedback channel.
plus=(Id+S[0])/2;minus=(Id-S[0])/2
L=ad(plus)+ad(F@minus)-IdS
kap=2.3;D=kap*sum(ad(s)-IdS for s in S)
P=[]
for delta in range(4):
 proj=np.zeros((64,64))
 for g in range(4):
  U=Id.copy()
  for j in range(2):
   if g>>j&1:U=U@S[j]
  proj+=(-1)**((g&delta).bit_count())*ad(U)/4
 P.append(proj)
rng=np.random.default_rng(29);K0=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));K=kron(K0,I,I)
Ks=[]
for delta in range(4):
 A=np.zeros((8,8),complex)
 for g in range(4):
  U=Id.copy()
  for j in range(2):
   if g>>j&1:U=U@S[j]
  A+=(-1)**((g&delta).bit_count())*U@K@U/4
 Ks.append(A)
noise=diss(K);diag=sum(diss(A) for A in Ks)
errs={
 'SSF_covariance_max':max(np.linalg.norm(L@p-p@L) for p in P),
 'dephasing_character_identity_max':max(np.linalg.norm(D@p+2*kap*d.bit_count()*p) for d,p in enumerate(P)),
 'propagator_factorization_max':max(np.linalg.norm(expm(.31*(L+D))@p-np.exp(-2*kap*d.bit_count()*.31)*expm(.31*L)@p) for d,p in enumerate(P)),
 'diagonal_noise_equality':np.linalg.norm(P[0]@(noise-diag)@P[0]),
 'offdiagonal_no_charge_preserving_block_max':max(np.linalg.norm(p@(noise-diag)@p) for p in P),
 'covariant_noise_commutator_max':max(np.linalg.norm(diag@p-p@diag) for p in P)}
assert max(errs.values())<1e-10
print(json.dumps(errs,indent=2))
