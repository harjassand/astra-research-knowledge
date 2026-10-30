"""Regression of the triangular CP inverse and both activation corrections."""
import numpy as np
from scipy.linalg import expm, norm
from pathlib import Path
import json
rng=np.random.default_rng(530)
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex)
g=np.diag([1,0]).astype(complex); b=I-g
sb=.65*I+.1*X
S=np.kron(g,I)+np.kron(b,sb)
def psqrt(M):
    w,v=np.linalg.eigh(M); assert w.min()>-1e-12
    return (v*np.sqrt(np.maximum(w,0)))@v.conj().T
A=psqrt(S); C=psqrt(np.eye(4)-S); Ai=np.linalg.inv(A); D=Ai@C
B=np.kron(b,I); G=np.eye(4)-B
# reset the private first tensor factor to |0>, retaining the spectator.
def psi(O):return np.kron(I,O[:2,:2])
def T(O):return A@O@A+C@psi(O)@C
def Ti(O):return Ai@O@Ai-D@psi(O)@D
J=np.kron(np.array([[0,1],[0,0]],complex),I)
H=np.kron(g,X)
def L(O):return 1j*(H@O-O@H)+J.conj().T@O@J-.5*(J.conj().T@J@O+O@J.conj().T@J)
M=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)); M=M+M.conj().T
out={'T_inverse_T_residual':float(norm(Ti(T(M))-M)), 'T_T_inverse_residual':float(norm(T(Ti(M))-M))}
f=G+7*B
raw=L(T(f)); out['raw_reset_target_compression_norm']=float(norm(psi(raw)))
rows=[]
for delta in [.1,.01,.001]:
    # all activity is guarded off on B, while its good target is nontrivial.
    xgood=np.kron(g,(I+.4*Z))
    Y=expm(delta*xgood); F=f@Y.conj().T@Y; dF=F-f
    forward=B@(T(F)-T(f))@B
    expected=C@psi(dF)@C
    E=L(T(dF)); inverse_correction=Ti(E)-Ai@E@Ai
    rows.append({'delta':delta,'bad_forward_activation_norm':float(norm(forward)),
      'forward_identity_residual':float(norm(forward-expected)),
      'inverse_target_subtraction_norm':float(norm(inverse_correction)),
      'inverse_identity_residual':float(norm(inverse_correction+D@psi(E)@D)),
      'inverse_correction_off_bad_norm':float(norm(inverse_correction-B@inverse_correction@B))})
assert max(out.values())<1e-11
assert all(r['forward_identity_residual']<1e-11 and r['inverse_identity_residual']<1e-11 and r['inverse_correction_off_bad_norm']<1e-11 for r in rows)
assert all(r['bad_forward_activation_norm']>r['delta']/2 and r['inverse_target_subtraction_norm']>r['delta']/2 for r in rows)
out['activation_checks']=rows
out['scope']='4-dimensional algebra regression; does not replace the actual native generator/source audit.'
Path(__file__).with_name('triangular_inverse_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
