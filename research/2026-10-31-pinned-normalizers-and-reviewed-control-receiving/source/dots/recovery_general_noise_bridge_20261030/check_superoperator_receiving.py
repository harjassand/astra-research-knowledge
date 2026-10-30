"""Finite algebra tests for two-sided correctable spans and signed trace-defect normalization."""
import numpy as np,json
rng=np.random.default_rng(20261030)
# Three-bit repetition protects the particular bit-flip family, not arbitrary quantum noise.
V=np.zeros((8,2),complex);V[0,0]=V[7,1]=1
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);E=[np.eye(8)]
for j in range(3):
 op=np.array([[1.]])
 for k in range(3):op=np.kron(op,X if j==k else I)
 E.append(op)
# Coherent decoder records which correctable bit-flip occurred.
D=np.zeros((8,8),complex)
for j in range(4):
 for b in range(2):D[b*4+j,:]=(E[j]@V[:,b]).conj()
assert np.linalg.norm(D@D.conj().T-np.eye(8))<1e-12
Aa=[rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)) for _ in range(4)]
Bb=[rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)) for _ in range(4)]
M=sum(np.kron(e,a) for e,a in zip(E,Aa));N=sum(np.kron(e,b) for e,b in zip(E,Bb))
Wa=np.vstack(Aa);Wb=np.vstack(Bb)
psi=rng.normal(size=4)+1j*rng.normal(size=4);psi/=np.linalg.norm(psi);rho=np.outer(psi,psi.conj())
enc=np.kron(V,I);dec=np.kron(D,I)
lhs=dec@M@enc@rho@enc.conj().T@N.conj().T@dec.conj().T
rhs=np.kron(I,Wa)@rho@np.kron(I,Wb).conj().T
res=np.linalg.norm(lhs-rhs)
# Signed K=id-epsilon*{Z,.}/2; actual full map is identity. Bad B=epsilon*{Z,.}/2.
eps=.07
bell=np.array([1,0,0,1],complex)/np.sqrt(2);r=np.outer(bell,bell.conj());zb=np.kron(I,Z)
bad=eps*(zb@r+r@zb)/2;good=r-bad
trb=lambda a:np.einsum('iaja->ij',a.reshape(2,2,2,2))
good_marginal_error=np.linalg.norm(trb(good-r),ord='nuc');bad_marginal=np.linalg.norm(trb(bad),ord='nuc')
# Unnormalized Choi of K has a negative eigenvalue, so positivity cannot be presumed.
J=np.zeros((4,4),complex)
for i in range(2):
 for j in range(2):
  a=np.zeros((2,2),complex);a[i,j]=1;k=a-eps*(Z@a+a@Z)/2
  J[i*2:(i+1)*2,j*2:(j+1)*2]=k
minchoi=np.linalg.eigvalsh(J).min()
assert res<1e-11 and abs(good_marginal_error-eps)<1e-12 and abs(bad_marginal-eps)<1e-12 and minchoi<0
print(json.dumps({'scope':'finite algebra only, not a universal-gadget verification','two_sided_decoder_factorization_residual':float(res),'signed_good_bath_map_min_choi_eigenvalue':float(minchoi),'exact_bad_map_diamond_norm':eps,'correlated_input_good_marginal_error':float(good_marginal_error),'correlated_input_bad_marginal_norm':float(bad_marginal),'actual_total_error':float(np.linalg.norm(good+bad-r,ord='nuc'))},indent=2))
