"""Independent finite algebra diagnostics, not a service/QCA threshold simulation."""
import numpy as np
from scipy.linalg import expm
import json
from itertools import combinations
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);sm=np.array([[0,1],[0,0]],complex)
def kron(*xs):
 a=np.ones((1,1),complex)
 for x in xs:a=np.kron(a,x)
 return a
def ham(H):return lambda O:-1j*(H@O-O@H)
def diss(J):
 K=J.conj().T@J
 return lambda O:J@O@J.conj().T-(K@O+O@K)/2
n=3;d=2**n
H0=.31*kron(I+Z,X,I)+.19*kron(X,Z,I)+.11*kron(I,I,Y)
Hnoise=.23*kron(Y,I,X)
Ds=diss(np.sqrt(.7)*kron(sm,I,I));Da=diss(np.sqrt(.4)*kron(I,sm,I));Dj=diss(.27*kron(Z,sm,X))
L0=lambda O:ham(H0)(O)+Ds(O)+Da(O)
# Actual noise cancels the nominal reset at S and adds joint system/bath terms.
N=lambda O:ham(Hnoise)(O)-Ds(O)+Dj(O)
L=lambda O:L0(O)+N(O)
def perm(X,S):
 C=[i for i in range(n) if i not in S];ax=list(S)+C+[i+n for i in S]+[i+n for i in C]
 return X.reshape([2]*(2*n)).transpose(ax).reshape(2**len(S),2**len(C),2**len(S),2**len(C)),ax

def unperm(X,S):
 C=[i for i in range(n) if i not in S];ax=list(S)+C+[i+n for i in S]+[i+n for i in C]
 return X.reshape([2]*(2*n)).transpose(np.argsort(ax)).reshape(d,d)
def reduce(M,S,O):
 ds=2**len(S)
 inop=unperm(np.kron(np.eye(ds)/ds,O),S)
 a,_=perm(M(inop),S)
 return np.einsum('aiaj->ij',a)
def expectation(M,S):
 def out(O):
  a,_=perm(O,S);z=np.zeros_like(a)
  for i in range(a.shape[0]):
   for j in range(a.shape[2]):z[i,:,j,:]=reduce(M,S,a[i,:,j,:])
  return unperm(z,S)
 return out
def matrix(M,dim=d):
 cols=[]
 for i in range(dim):
  for j in range(dim):
   a=np.zeros((dim,dim),complex);a[i,j]=1;cols.append(M(a).reshape(-1))
 return np.array(cols).T
E0N=expectation(N,[0]);cavity=lambda O:L0(O)+E0N(O)
E0L=expectation(L,[0])
Htouch=.31*kron(I+Z,X,I)+.19*kron(X,Z,I)
barH=.31*kron(I,X,I)
recon=lambda O:E0L(O)+Ds(O)+ham(Htouch-barH)(O)
wrong=lambda O:E0L(O)+Ds(O)+ham(Htouch)(O)
C=matrix(cavity);R=matrix(recon)
proj_res=float(np.linalg.norm(matrix(expectation(expectation(N,[0]),[1]))-matrix(expectation(N,[0,1])),2))
M=expm(.4*C)
blocks=[]
for i in range(d):
 row=[]
 for j in range(d):row.append(M[:,i*d+j].reshape(d,d))
 blocks.append(row)
choi=np.block(blocks)
choi_min=float(np.linalg.eigvalsh((choi+choi.conj().T)/2).min())
trace_vector=np.eye(d).reshape(-1)
trace_res=float(np.linalg.norm(trace_vector@C))
assert np.linalg.norm(C-R)<1e-11 and proj_res<1e-11
assert choi_min>-1e-11 and trace_res<1e-11
# Boolean identity with arbitrary compatible within-cavity classical instruments.
rng=np.random.default_rng(121)
def powers(U):
 U=sorted(U)
 return [frozenset(c) for k in range(len(U)+1) for c in combinations(U,k)]
F=frozenset(range(5));law={}
for U in powers(F):
 events=powers(U);p=rng.random(len(events));p/=p.sum();law[U]=dict(zip(events,p))
def success(U,V):return sum(p for event,p in law[U].items() if V<=event)
def fail(U,S):return sum(p for event,p in law[U].items() if not(event&S))
lhs=sum((-1)**len(A)*success(A,A) for A in powers(F))
rhs=0.
for Rset in powers(F):
 S=F-Rset
 for D in powers(Rset):rhs+=(-1)**(len(Rset)-len(D))*fail(F-D,S)
assert abs(lhs-rhs)<1e-11
# Necessity of excluding nominal system/bath dissipators: actual L=0,
# nominal J=Z_S tensor lowering_B, cavity is D[J]-Id_S tensor D[lowering].
J=kron(Z,sm);Jbar=kron(I,sm)
Lc=lambda O:diss(J)(O)-diss(Jbar)(O)
plus=np.array([1,1],complex)/np.sqrt(2);one=np.array([0,1],complex);zero=np.array([1,0],complex)
v=np.kron(plus,one);w=np.kron(plus,zero);rho=np.outer(v,v.conj())
negative=float(np.vdot(w,Lc(rho)@w).real)
assert negative<-.99
out=dict(scope='Finite cavity/projection/Boolean diagnostics only; no actual native service or semantic QCA simulation',
 reconstruction_residual=float(np.linalg.norm(C-R,2)),
 omitted_Hamiltonian_correction_error=float(np.linalg.norm(C-matrix(wrong),2)),
 commuting_union_projection_residual=proj_res,
 cavity_channel_min_Choi_eigenvalue=choi_min,
 generator_trace_preservation_residual=trace_res,
 five_label_mixed_Boolean_residual=float(abs(lhs-rhs)),
 excluded_joint_bath_nominal_dissipator_counterexample_derivative=negative)
print(json.dumps(out,indent=2))
