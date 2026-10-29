import numpy as np,json
from scipy.linalg import expm
from pathlib import Path
rng=np.random.default_rng(329)
rows=[]
for d in [2,3,4]:
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));tau=z@z.conj().T;tau/=np.trace(tau)
 S=np.zeros((d*d,d*d));
 for a in range(d):
  for b in range(d):S[a*d+b,b*d+a]=1
 P=np.diag([0,1]);H=np.kron(P,S);h=np.kron(P,tau);q=2*d
 def trace_sample(A):return np.einsum('iaja->ij',A.reshape(q,d,q,d))
 residual=0
 for a in range(q):
  for b in range(q):
   E=np.zeros((q,q),complex);E[a,b]=1;J=np.kron(E,tau)
   got=trace_sample(-1j*(H@J-J@H));want=-1j*(h@E-E@h)
   residual=max(residual,float(np.linalg.norm(got-want)))
 assert residual<1e-13
 # Explicit clean parity-flag circuit. Order flag, control, target, sample.
 Had=np.array([[1,1],[1,-1]])/np.sqrt(2);fH=np.kron(Had,np.eye(q*d))
 CS=np.kron(np.diag([1,0]),np.eye(q*d))+np.kron(np.diag([0,1]),np.kron(np.eye(2),S))
 parity=fH@CS@fH
 circuit_res=0
 for t in [-2.3,-.2,.0,.7,4.1]:
  phase=np.eye(2*q*d,dtype=complex)
  for flag in range(2):
   for c in range(2):
    start=(flag*2+c)*d*d
    phase[start:start+d*d,start:start+d*d]*=np.exp(-1j*t*c*((-1)**flag))
  W=parity@phase@parity
  desired=expm(-1j*t*H)
  circuit_res=max(circuit_res,float(np.linalg.norm(W[:q*d,:q*d]-desired)),float(np.linalg.norm(W[q*d:,:q*d])))
 assert circuit_res<1e-12
 rows.append(dict(d=d,matrix_unit_checks=q*q,controlled_generator_residual=residual,clean_parity_circuit_residual=circuit_res))
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
