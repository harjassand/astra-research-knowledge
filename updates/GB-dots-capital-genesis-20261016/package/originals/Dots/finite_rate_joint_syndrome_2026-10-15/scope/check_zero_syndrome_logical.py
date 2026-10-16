import numpy as np
from scipy.linalg import expm
from scipy.sparse import csr_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply
from functools import reduce
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex);pa={'I':I,'X':X,'Y':Y,'Z':Z}
def P(s):return reduce(np.kron,[pa[c] for c in s])
gens=[P(s) for s in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']];E=np.eye(32);Pc=reduce(np.matmul,[(E+g)/2 for g in gens])
Lx=P('IYYIX');Lz=P('ZZZZZ');rho0=Pc@(E+Lz)/2;Pm=Pc@(E-Lz)/2
assert abs(np.trace(rho0)-1)<1e-12
errors=[E]
for site in range(5):
 for p in 'XYZ':
  word=['I']*5;word[site]=p;errors.append(P(''.join(word)))
projectors=[e@Pc@e for e in errors]
assert np.linalg.norm(sum(projectors)-E)<1e-12
Dobs=sum(e@Pm@e for e in errors)
h=.2;gamma=.4;t=1.;H=h*(P('IYIII')+P('IIYII')+P('IIIIX'))
vec=lambda x:x.reshape(-1,order='F');Id=eye(32,format='csr',dtype=complex);Is=eye(1024,format='csr',dtype=complex)
Hs=csr_matrix(H);base=-1j*(kron(Id,Hs)-kron(Hs.T,Id))
for g in gens:
 gs=csr_matrix(g);base+=gamma*(kron(gs.conj(),gs)-Is)
for kappa in [0.,.7]:
 L=base.copy()
 for e,Pi in zip(errors[1:],projectors[1:]):
  j=np.sqrt(kappa)*e@Pi;n=j.conj().T@j;js=csr_matrix(j);ns=csr_matrix(n)
  L+=kron(js.conj(),js)-.5*kron(Id,ns)-.5*kron(ns.T,Id)
 out=expm_multiply(t*L,vec(rho0)).reshape((32,32),order='F');out=(out+out.conj().T)/2
 K=np.exp(-2*gamma*t)*Pc@expm(t*(-1j*H-kappa/2*(E-Pc)))@Pc
 a=np.trace(Pc@K)/2;b=np.trace(Lx@K)/2
 assert np.linalg.norm(K-a*Pc-b*Lx@Pc)<1e-11
 lower=np.trace(Pm@K@rho0@K.conj().T).real
 pzero=np.trace(Pc@out).real;pwrongzero=np.trace(Pm@out).real;pdecoded=np.trace(Dobs@out).real
 assert lower>0 and pwrongzero+1e-13>=lower
 if kappa==0:
  exact=np.exp(-4*gamma*t)*np.sin(h*t)**6
  assert abs(lower-exact)<1e-12
  assert np.linalg.norm(K-np.exp(-2*gamma*t)*(np.cos(h*t)**3*Pc+1j*np.sin(h*t)**3*Lx@Pc))<1e-12
 print(f'kappa={kappa:.1f}: P(final syndrome nonzero)={1-pzero:.12g}; P(zero syndrome AND logical-Z flip)={pwrongzero:.12g}; P(decoded logical-Z flip)={pdecoded:.12g}')
 print(f'  zero-flag no-jump Kraus a={a:.12g}, b={b:.12g}; positive lower bound={lower:.12g}; conditional P(logical flip | zero syndrome)={pwrongzero/pzero:.12g}')
print('PASS finite-rate five-qubit distance-three example, with and without autonomous ideal syndrome correction.')
print('Endpoint zero flags fail to certify all histories; this does not refute error suppression or a memory threshold.')
