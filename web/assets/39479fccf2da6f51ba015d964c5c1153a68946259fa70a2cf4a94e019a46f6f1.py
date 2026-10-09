"""Targeted discovery gate, never a final certificate by solver status alone."""
import json
from pathlib import Path
import numpy as np
import cvxpy as cp

OUT=Path(__file__).resolve().parent
d=3
I=np.eye(d,dtype=complex)
w=np.exp(2j*np.pi/3)
Z=np.diag([1,w,w*w])
X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
def quad(U):
    return [(U+U.conj().T)/np.sqrt(2),(U-U.conj().T)/(1j*np.sqrt(2))]
basis=sum([quad(U) for U in [Z,X,X@Z,X@Z@Z]],[])
frame=basis[:5]
assert np.max(np.abs(np.array([[np.trace(A@B)/d for B in basis] for A in basis])-np.eye(8)))<1e-12
def kron3(A,B,C): return np.kron(np.kron(A,B),C)
W=sum([kron3(A.T,A,I)+kron3(A.T,I,A) for A in frame])
P=np.zeros((27,27))
for a in range(3):
 for b in range(3):
  for c in range(3):
   P[a*9+c*3+b,a*9+b*3+c]=1
R=cp.Variable((27,27),hermitian=True)
expect=lambda O: cp.real(cp.trace(R@O))
constraints=[R>>0,cp.trace(R)==1,R==P@R@P]
for A in basis:
    for O in [kron3(A,I,I),kron3(I,A,I),kron3(I,I,A)]:
        constraints.append(expect(O)==0)
for i,A in enumerate(basis):
    for j in range(i):
        B=basis[j]
        constraints.append(expect(kron3(A.T,B,I)-kron3(B.T,A,I))==0)
problem=cp.Problem(cp.Maximize(expect(W)),constraints)
print('bare_max',np.linalg.eigvalsh(W)[-1], 'exact_C2_threshold',7,flush=True)
problem.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8,max_iter=150)
r=np.array(R.value)
data={'status':problem.status,'objective':float(problem.value),
      'min_eigenvalue':float(np.linalg.eigvalsh(r)[0]),
      'max_constraint_violation':float(max(np.max(np.abs(c.violation())) for c in constraints)),
      'bare_max':float(np.linalg.eigvalsh(W)[-1]),'V':5,'k':2,
      'note':'Numerical discovery only. Fixed singleton marginals, equal receivers, and HS-self-adjoint marginal imposed.'}
dual_t=float(np.real(constraints[1].dual_value))
dual_lambdas=np.array([float(c.dual_value) for c in constraints[3:]])
data['dual_trace_multiplier']=dual_t
data['dual_zero_moment_multipliers']=dual_lambdas.tolist()
np.savez(OUT/'mub_rank5_gate.npz',R=r,W=W,basis=np.array(basis),frame=np.array(frame),dual_t=dual_t,dual_lambdas=dual_lambdas)
(OUT/'mub_rank5_gate.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2),flush=True)
