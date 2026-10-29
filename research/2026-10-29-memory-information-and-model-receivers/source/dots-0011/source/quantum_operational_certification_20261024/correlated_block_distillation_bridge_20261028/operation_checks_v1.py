#!/usr/bin/env python3
"""Independent matrix-level five-code distillation analogue, not25-qubit hardware."""
import numpy as np,itertools,json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex);P={'I':I,'X':X,'Y':Y,'Z':Z}
def kronword(s):
 a=np.ones((1,1),complex)
 for x in s:a=np.kron(a,P[x])
 return a
Gs=[kronword(s) for s in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']]
XL=kronword('XXXXX');ZL=kronword('ZZZZZ');Id=np.eye(32)
Proj=Id.copy()
for g in Gs:Proj=Proj@(Id+g)/2
v=Proj@(Id+ZL)[:,0]/2;v/=np.linalg.norm(v);V=np.column_stack((v,XL@v))
assert np.max(abs(V.conj().T@V-np.eye(2)))<1e-12
errs=[Id]+[kronword('I'*i+p+'I'*(4-i)) for i in range(5) for p in 'XYZ']
def syndrome(e):return tuple(int(np.max(abs(g@e-e@g))>1e-9) for g in Gs)
lookup={syndrome(e):e for e in errs};assert len(lookup)==16
phi=np.eye(2).reshape(-1)/np.sqrt(2);target=np.outer(phi,phi.conj());worst=0.;tp=0.
# All16 correctable Bell labels, all16 Alice syndromes, actual bilateral maps.
for e in errs:
 corr=lookup[syndrome(e)];out=np.zeros((4,4),complex)
 for a in errs:
  C=V.conj().T@a
  Alice=C.conj();Bob=C@corr
  amp=(Alice@e.T@Bob.T/np.sqrt(32)).reshape(-1)
  out+=np.outer(amp,amp.conj())
 worst=max(worst,float(np.max(abs(out-target))));tp=max(tp,float(abs(np.trace(out)-1)))
# Four-Pauli bilateral twirl dephases arbitrary pair/environment state.
rng=np.random.default_rng(284997);v=rng.normal(size=8)+1j*rng.normal(size=8);v/=np.linalg.norm(v);rho=np.outer(v,v.conj());actual=np.zeros((8,8),complex)
for p in [I,X,Y,Z]:
 u=np.kron(np.kron(p.conj(),p),I);actual+=u@rho@u.conj().T/4
bell=[np.kron(I,p)@phi for p in [I,X,Y,Z]];ideal=np.zeros((8,8),complex)
for b in bell:
 q=np.kron(np.outer(b,b.conj()),I);ideal+=q@rho@q
res={'five_code_all_correctable_bilateral_branches':256,'maximum_output_entry_error':worst,'maximum_trace_error':tp,'twirl_joint_environment_entry_error':float(np.max(abs(actual-ideal))),'scope':'floating matrix sanity checks supplement exact algebra, not interval proof; no source draws','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
assert max(worst,tp,res['twirl_joint_environment_entry_error'])<1e-12
(D/'operation_checks_v1.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
