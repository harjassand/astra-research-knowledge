import numpy as np,json,hashlib
from pathlib import Path
rng=np.random.default_rng(93481)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);ps={'I':I,'X':X,'Y':Y,'Z':Z}
def kron(s):
 a=np.array([[1.]])
 for p in s:a=np.kron(a,ps[p])
 return a
P=np.eye(32,dtype=complex)
for g in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']:
 P=P@(np.eye(32)+kron(g))/2
P=P@(np.eye(32)+kron('ZZZZZ'))/2
w,U=np.linalg.eigh(P);v=U[:,-1];enc=np.stack([v,kron('XXXXX')@v],axis=1)
errs=[np.eye(32)]
for j in range(5):
 for p in 'XYZ':
  st=['I']*5;st[j]=p;errs.append(kron(st))
W=np.concatenate([E@enc for E in errs],axis=1);dec=W.conj().T
unit=float(np.linalg.norm(W.conj().T@W-np.eye(32)))
# six coherent routing branches: fully swapped, or exactly one unfinished column.
# Arbitrary ancilla jointly entangles all spare qubits, routing branch and env.
rows=[]
for trial in range(12):
 anc=rng.normal(size=(32,6,2))+1j*rng.normal(size=(32,6,2));anc/=np.linalg.norm(anc)
 out=[]
 for c in range(6):
  psi=np.einsum('ql,be->lqbe',enc/np.sqrt(2),anc[:,c,:])
  ten=psi.reshape((2,)+(2,)*10+(2,))
  for j in range(5):
   if c!=j+1:ten=ten.swapaxes(1+j,6+j)
  ten=ten.reshape(2,32,32,2)
  # decode physical B; output index is syndrome*2 + logical
  decoded=np.einsum('db,rqbe->rqde',dec,ten).reshape(2,32,16,2,2)
  out.append(decoded)
 # overlap of reference/logical Bell, summed over every retained ancillary branch
 bproj=sum(np.linalg.norm((x[0,:,:,0,:]+x[1,:,:,1,:])/np.sqrt(2))**2 for x in out)
 norm=sum(np.linalg.norm(x)**2 for x in out)
 rows.append({'trial':trial,'norm':float(norm),'bell_fidelity':float(bproj),'logical_leak':float(norm-bproj)})
assert unit<1e-10
assert max(abs(x['bell_fidelity']-1) for x in rows)<1e-10
# Initialization warning: all routing clocks start 1 but bare input is Q.
# G-frame protection then treats B as protected; physical B has no initial input.
# At t=0 B=|00000>, its fixed decoder cannot yield arbitrary unknown input.
print(json.dumps({'decoder_unitarity_error':unit,'coherent_partial_swap_trials':rows,'scope':'At most one missing physical column; arbitrary entangled spare/clock/env; common five-qubit decoder, no clock-dependent recovery.'},indent=2))
