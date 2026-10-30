import numpy as np, json
from pathlib import Path
rng=np.random.default_rng(20261030)
n=3; D=2**n; K=2; bath=3
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex)
def pauli(x,z):
 out=np.array([[1]],complex)
 for i in range(n): out=np.kron(out,np.linalg.matrix_power(X,(x>>(n-1-i))&1)@np.linalg.matrix_power(Z,(z>>(n-1-i))&1))
 return out
V=np.zeros((D,K),complex);V[0,0]=1;V[-1,1]=1
def synd(j):
 bits=[(j>>(n-1-i))&1 for i in range(n)]
 return ((bits[0]^bits[1])<<1)|(bits[1]^bits[2])
Pis=[np.diag([int(synd(j)==s) for j in range(D)]).astype(complex) for s in range(4)]
# Correlated source error, resource-relative error, signed gauge and a common bath.
# Every total E*F is either identity or one X; repetitions are intentional.
pairs=[(0,0),(4,0),(0,2),(1,0),(0,4)]
coef=rng.normal(size=(len(pairs),4,bath))+1j*rng.normal(size=(len(pairs),4,bath))
kin=np.zeros((D,D,D,bath,K),complex)
for t,(e,f) in enumerate(pairs):
 ev=pauli(e,0)@V
 for s in range(4):
  om=Pis[s]/np.sqrt(K)
  fom=om@pauli(f,0).T
  kin+=np.einsum('ql,ab,c->qabcl',ev,fom,coef[t,s])
gram=kin.reshape(-1,K).conj().T@kin.reshape(-1,K)
assert np.linalg.norm(gram-gram[0,0]*np.eye(K))<1e-10
kin/=np.sqrt(gram[0,0].real)
# Ordinary repetition-code X-error canonical extraction, independent of Bell mask.
C=np.zeros((K,4,D),complex)
for j in range(D):
 s=synd(j); corr=next(x for x in [0,1,2,4] if synd(x)==s)
 jj=j^corr; assert jj in [0,D-1]
 C[int(jj==D-1),s,j]=1
max_factor=0.; norm_sum=0.; max_exact=0.
for x in range(D):
 for z in range(D):
  P=pauli(x,z); beta=P/np.sqrt(D)
  kp=np.einsum('qa,qabcl->bcl',beta.conj(),kin)
  out=np.einsum('db,bcl->dcl',P,kp)
  canon=np.einsum('lsd,dci->lsci',C,out)
  a=(canon[0,:,:,0]+canon[1,:,:,1])/2
  ideal=np.zeros_like(canon);ideal[0,:,:,0]=a;ideal[1,:,:,1]=a
  max_factor=max(max_factor,float(np.linalg.norm(canon-ideal)))
  norm_sum+=float(np.vdot(a,a).real)
  # Exact transfer per incoming coefficient, including the coherent gauge label.
  for e,f in pairs:
   for s in range(4):
    lhs=P@pauli(f,0)@Pis[s]@P.conj().T@pauli(e,0)@V
    overlap=np.trace(pauli(f,0).conj().T@P@pauli(f,0)@P.conj().T)/D
    rhs=overlap*pauli(f,0)@pauli(e,0)@V if s==synd(x^e) else np.zeros_like(V)
    max_exact=max(max_exact,float(np.linalg.norm(lhs-rhs)))
# Partial Bell measurement: leave column0 Q/A unmeasured and RETAIN it coherently.
# Set its actual mask to I, so its virtual outcome is not communicated/applied.
# Compare every retained-output coefficient with one common output error module.
J=0
mats=[]
for e,f in pairs:
 for xx,zz in [(0,0),(4,0),(0,4),(4,4)]: mats.append((pauli(xx,zz)@pauli(f,0)@pauli(e,0)@V).reshape(-1))
M=np.column_stack(mats); U,sv,_=np.linalg.svd(M,full_matrices=False); U=U[:,sv>1e-10]
max_partial=0.; partial_norm=0.
for xo in range(4):
 for zo in range(4):
  x=xo;z=zo; P=pauli(x,z)
  # Bell bras only on the last two columns, Q0/A0 retained as 4 output states.
  bm=np.kron(np.linalg.matrix_power(X,(xo>>1)&1)@np.linalg.matrix_power(Z,(zo>>1)&1),np.linalg.matrix_power(X,xo&1)@np.linalg.matrix_power(Z,zo&1))/2
  kp=np.zeros((2,2,D,bath,K),complex)
  for q0 in range(2):
   for a0 in range(2): kp[q0,a0]=np.einsum('qa,qabcl->bcl',bm.conj(),kin[q0*4:(q0+1)*4,a0*4:(a0+1)*4])
  out=np.einsum('db,uabcl->uadcl',P,kp)
  partial_norm+=float(np.vdot(out,out).real/K)
  for q0 in range(2):
   for a0 in range(2):
    for c in range(bath):
     v=out[q0,a0,:,c,:].reshape(-1)
     max_partial=max(max_partial,float(np.linalg.norm(v-U@(U.conj().T@v))))
# A dense wrong mask NOT covered by J can defeat the one-error canonical interface.
logical_bad=pauli(7,0)@V
bad_canon=np.einsum('lsd,di->lsi',C,logical_bad)
# H=(pi/2)(I-P) implements Hermitian physical Pauli P exactly; real XZ is not Hermitian.
from scipy.linalg import expm
Y=1j*X@Z
pulse_res=max(float(np.linalg.norm(expm(-1j*np.pi/2*(I-P))-P)) for P in [I,X,Y,Z])
result=dict(incoming_isometry_residual=float(np.linalg.norm(kin.reshape(-1,K).conj().T@kin.reshape(-1,K)-np.eye(K))),all_64_bell_outcome_common_factor_residual=max_factor,corrected_channel_scalar=norm_sum,exact_correlated_coefficient_identity_residual=max_exact,partial_measurement_retained_output_common_span_residual=max_partial,partial_channel_normalization=partial_norm,partial_module_rank=int(U.shape[1]),hermitian_pauli_pulse_residual=pulse_res,real_XZ_nonhermiticity=float(np.linalg.norm(X@Z-(X@Z).conj().T)),dense_wrong_mask_logical_offdiag=float(abs(bad_canon[1,0,0])),scope='3-qubit repetition CSS diagnostic; exact joint algebra and X-error extraction only, not Tanner hardware or full-distance theorem')
assert max_factor<1e-12 and abs(norm_sum-1)<1e-12 and max_exact<1e-12 and max_partial<1e-12 and abs(partial_norm-1)<1e-12 and pulse_res<1e-12
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
