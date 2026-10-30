"""Independent overlapping-witness test of exact relative-drift cone algebra.
Three damping qubits; Zi has off-diagonal action on a neighbour, so neither
raw-energy commutation nor preservation of other Qi is assumed.
"""
from pathlib import Path
import numpy as np,json
from scipy.linalg import expm,eigvalsh
I2=np.eye(2);I=np.eye(8);Q=np.diag([0.,1.]);X=np.array([[0.,1.],[1.,0.]]);D=np.array([[0.,1.],[0.,0.]])
def at(a,i):
 v=np.array([[1.]])
 for j in range(3):v=np.kron(v,a if i==j else I2)
 return v
qs=[at(Q,i) for i in range(3)];xs=[at(X,i) for i in range(3)];ds=[at(D,i) for i in range(3)]
a=.6;b=.1;s=.7;k=np.exp(-s);delta=.04
zs=[qs[0]@(a*I+b*xs[1]),qs[1]@(a*I+b*xs[0]),qs[2]@(a*I+b*xs[1])]
deltas=[(1-k)*q for q in qs]
def lw(e,O):return k*ds[e].T@O@ds[e]-(qs[e]@O+O@qs[e])/2
def lc(e,O):return k*(ds[e].T@O@ds[e]-(qs[e]@O+O@qs[e])/2)
def l0(O):return sum(ds[e].T@O@ds[e]-(qs[e]@O+O@qs[e])/2 for e in range(3))
Y=np.eye(8)
fs=[expm(delta*z/2) for z in zs]
# Left-to-right factors 0,1,2: in conjugating a bundle at qubit0, factor2
# cancels FIRST, although it would overlap the later expanded support.
for f in fs:Y=Y@f
Ye=fs[0]@fs[1]
def rel(y,e):
 inv=np.linalg.inv(y);return inv.T@lw(e,y.T@y)@inv
M=rel(Y,0);Me=rel(Ye,0)
Zsum=zs[0]+zs[1]
deriv=lc(0,Zsum)
R=Me+deltas[0]-delta*deriv
P=(I-qs[0])@(I-qs[1]);B=I-P
herm=lambda O:(O+O.T)/2
norm=lambda O:float(np.linalg.norm(O,2))
r=k*(a-1.5*b)
V=expm(s*sum(qs));rootV=expm(s*sum(qs)/2);S=Y@rootV;W=S.T@S
rhs=S.T@(-sum(deltas)-delta*r/2*sum(qs))@S
res={
 'delta':delta,'s':s,'r':r,
 'max_Z_other_Q_commutator':max(norm(z@q-q@z) for z in zs for q in qs),
 'max_Z_raw_energy_commutator':max(norm(z@sum(qs)-sum(qs)@z) for z in zs),
 'max_own_witness_drift_violation':max(float(eigvalsh(herm(sum(lc(e,z) for e in range(3))+r*q))[-1]) for z,q in zip(zs,qs)),
 'causal_subcircuit_identity_error':norm(M-Me),
 'discarded_gate_does_not_fix_local_zero_range':norm((fs[2]-I)@P),
 'relative_increment_zero_corner_error':norm((Me+deltas[0])@P),
 'remainder_zero_corner_error':norm(R@P),
 'remainder_norm_over_delta_squared':norm(R)/delta**2,
 'max_global_weighted_drift_violation':float(eigvalsh(herm(l0(W)-rhs))[-1]),
 'minimum_W_minus_V':float(eigvalsh(herm(W-V))[0]),
 'scope':'finite noncommuting-witness and causal-cone algebra; not the actual native machine or useful DATA service'}
assert res['max_Z_other_Q_commutator']>.01
assert res['causal_subcircuit_identity_error']<1e-11
assert res['discarded_gate_does_not_fix_local_zero_range']>.001
assert res['relative_increment_zero_corner_error']<1e-11
assert res['remainder_zero_corner_error']<1e-11
assert res['max_own_witness_drift_violation']<1e-11
assert res['max_global_weighted_drift_violation']<1e-11
assert res['minimum_W_minus_V']>-1e-11
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
