"""Global exponential dirty credit with actual CP inverse/target activation.
Finite six-dimensional algebra fixture only, not the native controller theorem.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm,eigvalsh
I2=np.eye(2,dtype=complex);I3=np.eye(3,dtype=complex)
def kb(i,j):
 a=np.zeros((3,3),complex);a[i,j]=1;return a
s=.7;R=4.;Sbad=.7
S=np.diag([1.,1.,Sbad]);A=np.diag(np.sqrt(np.diag(S)));Ai=np.linalg.inv(A);C=np.diag(np.sqrt(1-np.diag(S)))
A6=np.kron(I2,A);Ai6=np.kron(I2,Ai);C6=np.kron(I2,C)
U=(1/np.sqrt(2))*np.array([[1,1],[1,-1]],complex)
J=np.kron(U,kb(0,2));H=np.kron(I2,.8*(kb(0,1)+kb(1,0)))
B=np.kron(I2,kb(2,2))
Vdata=np.diag([1,np.exp(s)]);V=np.kron(Vdata,np.diag([1,1,np.exp(s*R)]));V0=np.kron(Vdata,I3)
Delta=np.kron(Vdata,np.diag([np.exp(s*R)-1]*3))
Vi=np.diag(1/np.sqrt(np.diag(V)))
def erase_star(O):
 O00=O.reshape(2,3,2,3)[:,0,:,0]
 return np.kron(O00,I3)
def T(O):return A6@O@A6+C6@erase_star(O)@C6
def Ti(O):return Ai6@(O-C6@erase_star(O)@C6)@Ai6
def L(O):
 jj=J.conj().T@J
 return 1j*(H@O-O@H)+J.conj().T@O@J-.5*(jj@O+O@jj)
def Lhat(O):return Ti(L(T(O)))
raw=Lhat(V);q=(np.exp(s)-1)/(np.exp(s*R)-1)
raw_drift=eigvalsh(raw+.5*B@Delta)[-1]
X=np.array([[1,.4j,0],[-.4j,1,0],[0,0,0]],complex)
rows=[]
for delta in [.1,.03,.01,.003]:
 G=np.kron(I2,expm(2*delta*X));VG=V@G
 O=L(T(VG));exact=Ti(O);wrong=Ai6@O@Ai6
 forward=T(VG)-T(V)
 forward_bad=np.linalg.norm(B@forward@B)
 inverse_subtraction=np.linalg.norm(exact-wrong)
 remainder=exact-raw
 ratio=np.linalg.norm(Vi@remainder@Vi,2)/delta
 lower=eigvalsh(T(VG)-V0)[0]
 rows.append({'delta':delta,'forward_erasure_activation_norm':float(forward_bad),'inverse_target_subtraction_norm':float(inverse_subtraction),'relative_remainder_over_delta':float(ratio),'flag_sensitive_lower_bound_min_eigenvalue':float(lower),'inverse_roundtrip_error':float(np.linalg.norm(T(Ti(O))-O))})
assert q<Sbad and raw_drift<1e-10
assert all(x['forward_erasure_activation_norm']>0 and x['inverse_target_subtraction_norm']>0 for x in rows)
assert all(x['flag_sensitive_lower_bound_min_eigenvalue']>-1e-10 and x['inverse_roundtrip_error']<1e-11 for x in rows)
assert max(x['relative_remainder_over_delta'] for x in rows)<10
out={'dimension':6,'s':s,'R':R,'S_bad':Sbad,'reset_surplus_ratio':float(q),'raw_half_Delta_drift_max_eigenvalue':float(raw_drift),'samples':rows,'scope':'Local global-exponential CP/dirty-cavity algebra only; no native service or basin theorem is inferred.'}
Path(__file__).with_name('global_exponential_dirty_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
