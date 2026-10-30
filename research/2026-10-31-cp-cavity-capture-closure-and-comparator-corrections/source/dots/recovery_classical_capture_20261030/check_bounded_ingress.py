"""Two-qubit concurrent-copy example; numerical corroboration, not the proof."""
import numpy as np
from scipy.linalg import expm
import json
I=np.eye(2); X=np.array([[0,1],[1,0]]); P1=np.diag([0,1]);g=1.;J=2*g;T=np.pi/(2*g)
H=g*np.kron(P1,X)
def reset(A):
 a=A.reshape(2,2,2,2);rest=np.einsum('iaib->ab',a)
 return np.kron(I/2,rest)
def gen(A,lam):return -1j*(H@A-A@H)+lam*(reset(A)-A)
def superop(lam):
 cols=[]
 for k in range(16):
  a=np.zeros(16,dtype=complex);a[k]=1;cols.append(gen(a.reshape(4,4),lam).reshape(16))
 return np.stack(cols,axis=1)
rows=[]
for lam in [.001,.01,.1,1.]:
 S=expm(T*superop(lam));diff=np.diag([1,0,-1,0]);d=(S@diff.reshape(16)).reshape(4,4)
 error=(1-.5*np.linalg.norm(d,ord='nuc'))/2
 tau=min(T,1/(2*J));lower=(1-np.exp(-lam*tau))/4
 assert error+1e-10>=lower
 rows.append(dict(reset_rate=lam,optimal_final_error=float(error),proved_lower_bound=float(lower)))
print(json.dumps({'scope':'concurrent controlled-X Hamiltonian, inaccessible resetting reservoir, all two-qubit output available','J':J,'T':T,'tests':rows},indent=2))
