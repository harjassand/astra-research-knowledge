"""Independent global-potential identities; not a native lifetime simulation."""
import numpy as np
from scipy.linalg import expm,logm,sqrtm,eigvalsh
import json
from pathlib import Path
s=.7;R=5.;delta=.08
# Disjoint corrections have commuting superoperators but nonzero state increments.
V=np.array([np.exp(s*(x+y)) for x in range(2) for y in range(2)])
Phi1=np.zeros((4,4));Phi2=np.zeros((4,4))
for x in range(2):
 for y in range(2):
  Phi1[2*x+y,y]=1;Phi2[2*x+y,2*x]=1
d1=V-Phi1@V;cross=Phi2@d1-d1
comm=np.linalg.norm(Phi1@Phi2-Phi2@Phi1)
expected=-(1-np.exp(-s))**2*V[3]
assert comm==0 and abs(cross[3]-expected)<1e-12 and abs(cross[3])>.1
# Controller good labels0,1; bad2,3. Non-scalar coherent survival coefficient.
I4=np.eye(4);I2=np.eye(2);B=np.diag([0,0,1,1]);U=np.diag([0,1])
S=np.eye(4,dtype=complex);S[2:,2:]=np.array([[.73,.07j],[-.07j,.61]])
smin=float(eigvalsh(S[2:,2:])[0]);kD=-np.log(smin)
def psqrt(M):
 e,v=np.linalg.eigh(M); return (v*np.sqrt(np.maximum(e,0)))@v.conj().T
A=np.kron(psqrt(S),I2);C=np.kron(psqrt(I4-S),I2)
Ainv=np.linalg.inv(A)
def erase(O):return np.kron(I4,O.reshape(4,2,4,2)[0,:,0,:])
def T(O):return A@O@A+C@erase(O)@C
def Ti(O):return Ainv@(O-C@erase(O)@C)@Ainv
E=np.kron(I4,U)+R*np.kron(B,I2);Vg=expm(s*E)
lower=expm(s*np.kron(I4,U)+(s*R-kD)*np.kron(B,I2))
no_jump_min=float(eigvalsh(T(Vg)-lower)[0])
# Positive global controller G, with a nontrivial guarded good-sector block.
X=np.zeros((4,4),complex);X[:2,:2]=np.array([[1,.4j],[-.4j,1]])
G=np.kron(expm(2*delta*X),I2)
full_lower=float(eigvalsh(T(Vg@G)-lower)[0])
assert no_jump_min>-1e-10 and full_lower>-1e-10
rng=np.random.default_rng(1041);Z=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));O=Z+Z.conj().T
inverse_error=float(np.linalg.norm(Ti(T(O))-O))
assert inverse_error<1e-10
# Scalar spectral Jensen with subnormalized state NOT commuting VG.
Z=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));sigma=Z@Z.conj().T;sigma*=.37/np.trace(sigma)
W=Vg@G;logW=np.asarray(logm(W),complex);logG=np.asarray(logm(G),complex)
x=float(np.trace(sigma@W).real);m=float(np.trace(sigma).real)
z=float(np.trace(sigma@W@logW).real);y=float(np.trace(sigma@E@W).real);g=float(eigvalsh(logG)[-1])
jensen=z-x*np.log(x/m);energy=y-x*(np.log(x)-g)/s
assert jensen>-1e-10 and energy>-1e-10
out={'scope':'Independent exact finite algebra for disjoint increments, coherent dirty no-jump comparison, triangular inverse and subnormalized Jensen. Not a controller-service, code-family or lifetime simulation.','disjoint_superoperator_commutator':float(comm),'disjoint_state_increment_at_11':float(cross[3]),'expected_nonzero_increment':float(expected),'dirty_smin':smin,'flag_sensitive_lower_min_eigenvalue':no_jump_min,'weighted_flag_lower_min_eigenvalue':full_lower,'triangular_inverse_error':inverse_error,'state_mass':m,'state_weight_commutator_norm':float(np.linalg.norm(sigma@W-W@sigma)),'spectral_Jensen_slack':jensen,'energy_Jensen_slack':energy}
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
