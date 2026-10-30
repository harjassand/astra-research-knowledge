"""Independent whole-Hilbert regression for 2 guarded onsite-reset hubs.
Not a proof of the asymptotic theorem. All 18 joint states, dirty/illegal included.
"""
import numpy as np, json
from scipy.linalg import sqrtm, expm
I2=np.eye(2,dtype=complex);I3=np.eye(3,dtype=complex);I=np.eye(18,dtype=complex)
def unit(d,a,b):
 x=np.zeros((d,d),complex);x[a,b]=1;return x
def embed(D,A,B):return np.kron(np.kron(D,A),B)
def aux(A,h):return embed(I2,A,I3) if h==0 else embed(I2,I3,A)
def idx(d,a,b):return 9*d+3*a+b
Ks0=[unit(2,0,0),unit(2,0,1)]
K=[embed(k,I3,I3) for k in Ks0]
P=[aux(unit(3,0,0),h) for h in range(2)];Q=[I-p for p in P]
R=[aux(unit(3,1,1),h) for h in range(2)]
# Explicit XOR then controlled-X completion, constructed on every basis vector.
Us=[]
for h in range(2):
 U=np.zeros_like(I)
 for d in range(2):
  for a in range(3):
   for b in range(3):
    z=[a,b];outd=d;out=z.copy()
    if z[h] and z[1-h]==0:
     label=(z[h]-1)^d
     outd=d^label;out[h]=label+1
    U[idx(outd,*out),idx(d,a,b)]=1
 Us.append(U)
U=Us[0]@Us[1]
Ls=[[U.conj().T@aux(unit(3,0,s+1),h)@U for s in range(2)] for h in range(2)]
C=[Q[h]-P[1-h]@R[h] for h in range(2)]
a=[P[1-h]@aux(unit(3,0,1),h) for h in range(2)]
Y=[1j*(x-x.conj().T) for x in a]
nu=.003; tau=1e-7; f0=5.;r=.05;theta=.01;u=.02;tokens=2
B=[Q[h]+2*nu*Y[h]+nu**2*f0*(P[1-h]+r*Q[1-h]) for h in range(2)]
roots=[np.asarray(sqrtm(b),complex) for b in B]
H=nu*sum(x+x.conj().T for x in a)
def dissipator(J,O):
 W=J.conj().T@J;return J.conj().T@O@J-(W@O+O@W)/2
def L(O):return 1j*(H@O-O@H)+sum(dissipator(j,O) for ls in Ls for j in ls)
def Z(h,O):return sum(dissipator(roots[h]@k,O) for k in K)
# Complete 5-vertex animal graph: one syndrome and two token copies per flag.
occ=[embed(unit(2,1,1),I3,I3)]+[C[h] for h in range(2) for _ in range(tokens)]
V=I.copy();W=np.zeros_like(I)
# prod(1+w_v)-1 and sum_v w_v prod_{j !=v}(1+w_j).
weights=[theta**u*((I-p)+p/theta) for p in occ]
for w in weights:V=V@(I+w)
V-=I
for i,w in enumerate(weights):
 term=w.copy()
 for j,v in enumerate(weights):
  if j!=i:term=term@(I+v)
 W+=term
Phi=lambda O:sum(k.conj().T@O@k for k in K)
d=V-Phi(V)
raw=L(V)
bad=sum(-C[h]@sum(dissipator(j,V) for j in Ls[h]) for h in range(2))
base=sum((Q[h]-C[h])@d for h in range(2))
comm=[L(Z(h,V))-Z(h,L(V)) for h in range(2)]
first=raw+tau*sum(comm)
# Conservative service test, not claimed to identify optimal constants.
res=first+.25*base+.25*bad+(.001*tau*nu**2)*(2*d)
herm=lambda M:(M+M.conj().T)/2
norm=lambda M:float(np.linalg.norm(M,2))
clean=(I-C[0])@(I-C[1]);dirty=I-clean
B0=Q
Z0=lambda h,O:sum(dissipator(Q[h]@k,O) for k in K)
L0=lambda O:sum(dissipator(j,O) for ls in Ls for j in ls)
cross0=[norm(clean@(L0(Z0(h,V))-Z0(h,L0(V)))@dirty) for h in range(2)]
# Exact CP gates via 324x324 superoperators (column convention).
def superop(fun):
 out=np.empty((324,324),complex)
 for j in range(324):
  e=np.zeros((18,18),complex);e[j%18,j//18]=1
  out[:,j]=fun(e).reshape(-1,order='F')
 return out
Gates=[expm(tau*superop(lambda O,h=h:Z(h,O))) for h in range(2)]
T=Gates[0]@Gates[1]
F=(T@V.reshape(-1,order='F')).reshape(18,18,order='F')
# No-jump lower bound with two gates. Animal-specific proof is in written receipt.
# Verify on all 31 nonempty animals independently, max relative negative defect.
maxlower=0.
for mask in range(1,32):
 f=I.copy()
 for j,w in enumerate(weights):
  if mask>>j&1:f=f@w
 Tf=(T@f.reshape(-1,order='F')).reshape(18,18,order='F')
 floor=np.exp(-tau*sum(norm(b) for b in B))*f
 maxlower=max(maxlower,-float(np.linalg.eigvalsh(herm(Tf-floor)).min()))
results={
 'dimension':18,'theta':theta,'u':u,'nu':nu,'tau':tau,
 'explicit_gauge_unitarity_error':norm(U.conj().T@U-I),
 'all_flag_credit_commutators':max(norm(b@c-c@b) for b in B for c in C),
 'raw_drift_decomposition_error_relative':norm(raw+base+bad)/norm(V),
 'raw_drift_maxeig_relative':float(np.linalg.eigvalsh(herm(raw)).max())/norm(V),
 'B_min_eigenvalues':[float(np.linalg.eigvalsh(b).min()) for b in B],
 'first_order_test_maxeig_relative':float(np.linalg.eigvalsh(herm(res)).max())/norm(V),
 'zero_drive_clean_dirty_cross_norms':cross0,
 'dressed_flag_commutator_relative':max(norm(F@c-c@F) for c in C)/norm(V),
 'per_animal_nojump_bound_max_negative_defect_relative':maxlower/norm(V),
 'dressed_potential_monotonicity_maxeig_relative':float(np.linalg.eigvalsh(herm(F-V)).max())/norm(V),
 'note':'Exact structural fixture plus floating-point inequalities; does not prove general coverage or threshold.'}
assert results['raw_drift_decomposition_error_relative']<1e-12
assert results['raw_drift_maxeig_relative']<1e-12
assert results['first_order_test_maxeig_relative']<1e-12
assert max(cross0)<1e-12
assert results['per_animal_nojump_bound_max_negative_defect_relative']<1e-12
print(json.dumps(results,indent=2))
