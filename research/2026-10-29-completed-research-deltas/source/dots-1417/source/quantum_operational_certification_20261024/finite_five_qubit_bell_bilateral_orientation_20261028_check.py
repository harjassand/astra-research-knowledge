"""Separate actual bilateral Q* (Alice), Q (Bob) circuit verification.
The governing transfer source remains frozen. No source calls or hardware run.
"""
from pathlib import Path
from itertools import product
import hashlib,json
import numpy as np

root=Path(__file__).resolve().parent
source=root/'finite_five_qubit_bell_teleportation_factory_transfer_20261028.md'
governing=root/'finite_five_qubit_bell_teleportation_factory_transfer_20261028_check.json'
data=json.loads(governing.read_text())
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
P=dict(zip('IXYZ',[I,X,Y,Z]));H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
SD=np.diag([1,-1j]);D=32
def kron(*xs):
 out=np.array([[1]],complex)
 for x in xs:out=np.kron(out,x)
 return out
def gate(g):
 name,*idx=g
 if name in ['H','SD']:
  return kron(*[({'H':H,'SD':SD}[name] if i==idx[0] else I) for i in range(5)])
 out=np.zeros((D,D),complex)
 for i in range(D):
  b=[(i>>(4-j))&1 for j in range(5)];s=1
  if name=='CX':b[idx[1]]^=b[idx[0]]
  elif name=='CZ':s=(-1)**(b[idx[0]]*b[idx[1]])
  else:raise ValueError(name)
  j=sum(x<<(4-k) for k,x in enumerate(b));out[j,i]=s
 return out
Q=np.eye(D,dtype=complex)
for g in data['decoder_gates_chronological_zero_based']:Q=gate(g)@Q
mapping={sy:info['logical_correction'] for sy,info in data['syndrome_recovery_table'].items()}
maximum=0.;cases=0;branches=0
for chars in product('IXYZ',repeat=5):
 E=kron(*(P[c] for c in chars))
 # Coefficient matrix of (I tensor E)|Phi_32>, then actual local operations.
 M=Q.conj()@(E.T/np.sqrt(D))@Q.T
 QE=Q@E@Q.conj().T
 # Determine the unique decoder syndrome directly from the two code columns.
 weights=[np.linalg.norm(QE[2*s:2*s+2,:2])**2 for s in range(16)]
 syi=int(np.argmax(weights));sy=format(syi,'04b');corr=P[mapping[sy]]
 logical=corr@QE[2*syi:2*syi+2,:2]
 target=logical.T.reshape(4)/np.sqrt(2)
 target_density=np.outer(target,target.conj())
 for a in range(16):
  for b in range(16):
   block=M[2*a:2*a+2,2*b:2*b+2]
   prob=np.linalg.norm(block)**2
   if b==(a^syi):
    assert abs(prob-1/16)<1e-13
    v=(block@corr.T).reshape(4)
    err=np.linalg.norm(np.outer(v,v.conj())-target_density/16)
    maximum=max(maximum,float(err));branches+=1
   else:assert prob<1e-25
 cases+=1
assert cases==1024 and branches==16384 and maximum<1e-13
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out={'status':'PASS','scope':'Actual bilateral orientation and all retained measurement branches',
 'all_physical_errors':cases,'nonzero_measurement_branches':branches,
 'alice_bits_probability':'1/16 for each four-bit string',
 'bob_bits':'alice XOR actual decoder syndrome',
 'max_retained_density_residual':maximum,
 'sha256':{p.name:sha(p) for p in [source,governing,Path(__file__)]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
