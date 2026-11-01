"""Exact finite interface check, standard [[5,1,3]], not recursive family/hardware."""
import numpy as np
import scipy.linalg as la
import json
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=dict(I=I,X=X,Y=Y,Z=Z)
def kron(*v):
 a=np.array([[1.]])
 for b in v:a=np.kron(a,b)
 return a
def word(s):return kron(*(P[a] for a in s))
def tn(a):return float(la.svdvals(a).sum())
S=[word(s) for s in ('XZZXI','IXZZX','XIXZZ','ZXIXZ')];pc=np.eye(32)
for s in S:pc=pc@(np.eye(32)+s)/2
v0=pc[:,0]/la.norm(pc[:,0]);v1=word('XXXXX')@v0
Es=[np.eye(32)]
for j in range(5):
 for p in 'XYZ':
  w=['I']*5;w[j]=p;Es.append(word(w))
D=np.column_stack([E@v for v in (v0,v1) for E in Es]);ps=[E@pc@E.conj().T for E in Es]
Q=[]
for bare in (word('XXXXX'),word('ZZZZZ')):
 signs=[float(np.trace(E@bare@E.conj().T@bare).real/32) for E in Es]
 Q.append(bare@sum(f*s for f,s in zip(signs,ps)))
assert la.norm(Q[0]-D@kron(X,np.eye(16))@D.conj().T)<1e-12
assert la.norm(Q[1]-D@kron(Z,np.eye(16))@D.conj().T)<1e-12
C=[la.block_diag(np.eye(64),kron(q,I)) for q in Q];ha=kron((X+Z)/np.sqrt(2),np.eye(64))
swap=C[0]@ha@C[1]@ha@C[0]
rng=np.random.default_rng(76);H0=sum((np.eye(32)-s)/2 for s in S);H=kron(H0,I)+kron(np.eye(32),.35*(I-Z))
for j in range(5):
 for a in 'XYZ':
  w=['I']*5;w[j]=a
  for b in 'IXYZ':H=H+.01*rng.uniform(-1,1)*kron(word(w),P[b])
rho=la.expm(-6*H);rho/=np.trace(rho);ud=kron(D,I);rd=ud.conj().T@rho@ud
sigma=np.trace(rd.reshape(2,32,2,32),axis1=0,axis2=2)
errs=[]
for i in range(2):
 for j in range(2):
  a=np.zeros((2,2));a[i,j]=1
  evolved=swap@kron(a,rho)@swap.conj().T
  output=np.trace(evolved.reshape(2,64,2,64),axis1=0,axis2=2)
  expected=ud@kron(a,sigma)@ud.conj().T
  errs.append(tn(output-expected))
deph=sum(kron(p,I)@rho@kron(p,I) for p in ps)
dd=ud.conj().T@deph@ud;sd=np.trace(dd.reshape(2,32,2,32),axis1=0,axis2=2)
res={'scope':'ideal decoded Pauli SWAP on standard five-qubit code with one interacting bath qubit; no physical noisy loading claim','matrix_unit_output_errors':errs,'syndrome_measurement_changes_joint_state':tn(deph-rho),'syndrome_measurement_changes_retained_gauge_bath':tn(sd-sigma),'swap_unitarity':float(la.norm(swap.conj().T@swap-np.eye(128)))}
assert max(errs)<1e-12 and res['syndrome_measurement_changes_retained_gauge_bath']>1e-5
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
