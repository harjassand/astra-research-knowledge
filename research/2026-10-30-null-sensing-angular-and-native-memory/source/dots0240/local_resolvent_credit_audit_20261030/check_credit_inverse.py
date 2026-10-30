import numpy as np,json
from scipy.linalg import sqrtm
I=np.eye(3,dtype=complex)
def unit(i,j):
 M=np.zeros((3,3),complex);M[i,j]=1;return M
def dis(J,O):
 A=J.conj().T@J;return J.conj().T@O@J-(A@O+O@A)/2
def sop(fn):
 cols=[]
 for i in range(9):
  O=np.zeros(9,complex);O[i]=1;cols.append(fn(O.reshape(3,3)).reshape(-1))
 return np.stack(cols,axis=1)
H=.4*(unit(0,1)+unit(1,0))+.6*(unit(1,2)+unit(2,1))
internal=np.sqrt(.2)*unit(0,1)
terminal=[np.sqrt(.7)*unit(0,2),np.sqrt(.3)*unit(1,2)]
A=sum(a.conj().T@a for a in terminal)
def kill(O):return 1j*(H@O-O@H)+dis(internal,O)-(A@O+O@A)/2
Kmat=sop(kill);R=np.linalg.solve(Kmat,-I.reshape(-1)).reshape(3,3);R=(R+R.conj().T)/2
alpha,raw_Rmax=np.linalg.eigvalsh(R)[[0,-1]];Rmax=1.1*raw_Rmax;beta=.3/Rmax
S=(1-beta*Rmax)*I+beta*R
root=np.asarray(sqrtm(S),complex);rcomp=np.asarray(sqrtm(I-S),complex)
Kdata=[unit(0,0)+unit(1,1),unit(0,2)]
P=lambda O:sum(k.conj().T@O@k for k in Kdata)
V=np.diag([.2,.4,1]);d=V-P(V)
F=np.kron(P(V),I)+np.kron(d,S)
Jcredit=[np.kron(I,root)]+[np.kron(k,rcomp) for k in Kdata]
def T(O):return sum(j.conj().T@O@j for j in Jcredit)
s,W=np.linalg.eigh(S);U=np.kron(I,W)
def Ti(O):
 X=(U.conj().T@O@U).reshape(3,3,3,3);Y=np.empty_like(X)
 for i in range(3):
  for j in range(3):
   Z=X[:,i,:,j];a=np.sqrt(s[i]*s[j]);b=np.sqrt((1-s[i])*(1-s[j]));PZ=P(Z)
   Y[:,i,:,j]=(Z-PZ)/a+PZ/(a+b)
 return U@Y.reshape(9,9)@U.conj().T
HH=np.kron(I,H)
actual=[np.kron(I,internal)]+[np.kron(k,a) for a in terminal for k in Kdata]
LF=1j*(HH@F-F@HH)+sum(dis(j,F) for j in actual)
# dis uses the jump's actual shape, so works on joint 9x9 too.
rng=np.random.default_rng(90210);O=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
# Counterexample to extending F>=s_min V to noncommuting controller factors.
Sc=np.array([[5/8,3/8],[3/8,5/8]],complex);Qc=np.array([[3/4,1/4],[1/4,3/4]],complex)
Bc=np.diag([4.,1.]);Ac=np.diag([.01,1.]);Qcomp=np.asarray(sqrtm(np.eye(2)-Sc),complex)
Kd=[np.array([[1.,0],[0,0]]),np.array([[0,1.],[0,0]])]
f=np.kron(Ac,Bc);jcs=[np.kron(np.eye(2),Qc)]+[np.kron(k,Qcomp) for k in Kd]
Tf=sum(j.conj().T@f@j for j in jcs);neg=Tf-.25*f
# Mutually exclusive controlled credits, even with noncommuting DATA resets.
P0=np.diag([1.,1.,0,0]);P1=np.eye(4)-P0
S0=np.array([[.7,.1],[.1,.8]]);S1=np.array([[.8,-.1],[-.1,.6]])
controlled=[]
plus=np.array([1.,1.])/np.sqrt(2)
KG=[np.outer(plus,np.eye(2)[i]) for i in range(2)]
for start,Sblock,kdata in [(0,S0,Kd),(2,S1,KG)]:
 A0=np.eye(4,dtype=complex);B0=np.zeros((4,4),complex)
 A0[start:start+2,start:start+2]=np.asarray(sqrtm(Sblock),complex)
 B0[start:start+2,start:start+2]=np.asarray(sqrtm(np.eye(2)-Sblock),complex)
 controlled.append([np.kron(np.eye(2),A0)]+[np.kron(k,B0) for k in kdata])
def cp(js,O):return sum(j.conj().T@O@j for j in js)
Q=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8))
commuting_error=np.linalg.norm(cp(controlled[0],cp(controlled[1],Q))-cp(controlled[1],cp(controlled[0],Q)))
# Disjoint DATA is not full support disjointness: shared controller dephasings.
z=np.diag([1.,-1.]);rot=np.array([[np.cos(np.pi/8),-np.sin(np.pi/8)],[np.sin(np.pi/8),np.cos(np.pi/8)]])
Sj=[np.diag([1.,.25]),rot@np.diag([1.,.25])@rot.T]
rootz=np.diag([1.,.5]);rootzc=np.diag([0.,np.sqrt(3)/2]);js=[[rootz,rootzc],[rot@rootz@rot.T,rot@rootzc@rot.T]]
disjoint_data_counter=np.linalg.norm(cp(js[0],cp(js[1],z))-cp(js[1],cp(js[0],z)),2)

report={
 'R_min':float(alpha),'R_max':float(Rmax),'S_min':float(min(s)),
 'killed_generator_max_real_eigenvalue':float(max(np.linalg.eigvals(Kmat).real)),
 'resolvent_identity_error':float(np.linalg.norm(kill(R)+I)),
 'exact_service_error':float(np.linalg.norm(LF-np.kron(d,kill(S)))),
 'CP_credit_identity_error':float(np.linalg.norm(T(np.kron(V,I))-F)),
 'unitality_error':float(np.linalg.norm(T(np.eye(9))-np.eye(9))),
 'local_inverse_left_relative_error':float(np.linalg.norm(Ti(T(O))-O)/np.linalg.norm(O)),
 'local_inverse_right_relative_error':float(np.linalg.norm(T(Ti(O))-O)/np.linalg.norm(O)),
 'noncommuting_extended_factor_bound_counterexample_min_eigenvalue':float(np.linalg.eigvalsh(neg).min()),
 'counterexample_data1_block_determinant':float(np.linalg.det(neg.reshape(2,2,2,2)[1,:,1,:]).real),
 'exclusive_controlled_credit_commutation_error':float(commuting_error),
 'shared_controller_disjoint_DATA_commutator_norm':float(disjoint_data_counter),
 'scope':'Finite-controller exact algebra/inverse; counterexamples to unconditional extended-factor lower comparison and DATA-only disjointness.'}
for key,val in report.items():
 if 'error' in key:assert val<1e-10
assert alpha>0 and min(s)>0 and report['noncommuting_extended_factor_bound_counterexample_min_eigenvalue']<0
print(json.dumps(report,indent=2))
