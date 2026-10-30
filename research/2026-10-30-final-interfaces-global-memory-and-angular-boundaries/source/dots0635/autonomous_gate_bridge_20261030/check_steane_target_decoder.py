"""Two Steane blocks: fixed code-identity decoder, one missing local CNOT.
Only an ideal-code sanity test, NOT a native clock/noise/lifetime simulation.
"""
import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(30918)
n=7;N=1<<(2*n);inds=np.arange(N,dtype=np.int64)
H=[0b1010101,0b1100110,0b1111000]
words=sorted({(H[0] if x&1 else 0)^(H[1] if x&2 else 0)^(H[2] if x&4 else 0) for x in range(8)})
E=np.zeros((N,4),complex)
for a in [0,1]:
 for b in [0,1]:
  for x in words:
   for y in words:E[(x^(127*a))+((y^(127*b))<<7),2*a+b]=1/8
assert np.linalg.norm(E.conj().T@E-np.eye(4))<1e-12
UL=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
permall=(inds&127)+((((inds>>7)&127)^(inds&127))<<7)
def applyperm(v,p):
 out=np.empty_like(v);out[p]=v;return out
def missingperm(i):return inds^(((inds>>i)&1)<<(7+i))
def pauli(v,x=0,z=0):
 signs=np.array([1-2*((int(j)&z).bit_count()%2) for j in inds])
 out=np.empty_like(v);out[inds^x]=signs[:,None]*v;return out
# Deterministic fixed base syndrome recovery: measure all six stabilizers/block.
def base_decode(v):
 branches=[(v,[[0,0],[0,0]])]
 for block in range(2):
  for typ in range(2): # typ0 X checks detect Z errors; typ1 Z checks detect X
   for r,h in enumerate(H):
    new=[];mask=h<<(7*block)
    for w,sy in branches:
     sw=pauli(w,x=mask if typ==0 else 0,z=mask if typ==1 else 0)
     for bit in [0,1]:
      w1=(w+(1-2*bit)*sw)/2
      if np.linalg.norm(w1)>1e-11:
       sy1=[s.copy() for s in sy];sy1[block][typ]|=bit<<r
       new.append((w1,sy1))
    branches=new
 out=np.zeros((4*v.shape[1],4*v.shape[1]),complex);leak=0.
 for w,sy in branches:
  x=z=0
  for block,(sz,sx) in enumerate(sy):
   if sx:x^=1<<(7*block+sx-1)
   if sz:z^=1<<(7*block+sz-1)
  wc=pauli(w,x,z);c=E.conj().T@wc
  leak+=np.linalg.norm(wc-E@c)**2
  cf=c.reshape(-1);out+=np.outer(cf,cf.conj())
 return out,len(branches),float(leak)
def target_decode(physical):
 # Fixed target recovery, no program label or missing-set input.
 d,branches,leak=base_decode(applyperm(physical,permall))
 u=np.kron(UL,np.eye(physical.shape[1]))
 return u@d@u.conj().T,branches,leak
# Logical two-qubit input entangled with one reference qubit.
v=rng.normal(size=8)+1j*rng.normal(size=8);v/=np.linalg.norm(v)
encoded=E@v.reshape(4,2);rho=np.outer(v,v.conj());ur=np.kron(UL,np.eye(2));goal=ur@rho@ur.conj().T
initial,bi,li=target_decode(encoded)
done,bd,ld=target_decode(applyperm(encoded,permall))
partial=[]
for i in range(7):
 physical=applyperm(applyperm(encoded,missingperm(i)),permall)
 d,b,l=target_decode(physical)
 partial.append({'missing_column':i,'trace_norm_error':float(np.linalg.svd(d-goal,compute_uv=False).sum()),'syndrome_branches':b,'code_leakage':l})
# Bell witness from |+>_logical_A |0>_logical_B.
p=np.array([1,0,1,0],complex)/np.sqrt(2);enc=E@p[:,None]
bell=np.array([1,0,0,1],complex)/np.sqrt(2)
dbell,_,_=target_decode(applyperm(applyperm(enc,missingperm(0)),permall))
dzero,_,_=target_decode(enc)
out={'physical_DATA_qubits':14,'code':'two [[7,1,3]] Steane CSS blocks','reference_qubits':1,'time_zero_identity_trace_norm_error':float(np.linalg.svd(initial-rho,compute_uv=False).sum()),'fully_completed_gate_trace_norm_error':float(np.linalg.svd(done-goal,compute_uv=False).sum()),'single_missing_columns':partial,'partial_gate_Bell_fidelity':float(np.vdot(bell,dbell@bell).real),'time_zero_Bell_fidelity':float(np.vdot(bell,dzero@bell).real),'decoder_input':'fixed physical state only; never receives missing column/program phases','scope':'Ideal-code/decoder sanity only. No native apparatus, continuous-noise threshold or completion probability is simulated.'}
assert out['time_zero_identity_trace_norm_error']<1e-10
assert out['fully_completed_gate_trace_norm_error']<1e-10
assert max(x['trace_norm_error'] for x in partial)<1e-10
assert abs(out['partial_gate_Bell_fidelity']-1)<1e-10
assert abs(out['time_zero_Bell_fidelity']-.25)<1e-10
Path(__file__).with_name('steane_target_decoder_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
