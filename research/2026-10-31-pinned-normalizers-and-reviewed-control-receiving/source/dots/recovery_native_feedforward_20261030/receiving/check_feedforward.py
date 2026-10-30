"""Finite algebra diagnostics only, not a test of the native many-body theorem."""
import itertools, math, json
import numpy as np
from pathlib import Path
out={}
# Exact cardinality indicator identity at all small cardinalities.
cases=0
for M in range(1,16):
 for K in range(1,M+1):
  for n in range(M+1):
   v=sum((-1)**(s-K)*math.comb(s-1,K-1)*math.comb(n,s) for s in range(K,n+1))
   assert v==int(n>=K); cases+=1
out['exact_cardinality_cases']=cases
# OR on disjoint bad predicates, including correlated (not independent) flags.
cases=0
for n in range(1,10):
 for bits in itertools.product([0,1], repeat=n):
  v=sum((-1)**(len(S)+1)*math.prod(bits[i] for i in S)
    for r in range(1,n+1) for S in itertools.combinations(range(n),r))
  assert v==int(any(bits)); cases+=1
out['exact_OR_cases']=cases
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex); Y=1j*X@Z
ps={'I':I,'X':X,'Y':Y,'Z':Z}
def word(w):
 a=np.ones((1,1),complex)
 for c in w: a=np.kron(a,ps[c])
 return a
# Perfect five-qubit code: common quantum-error module, not classical repetition.
proj=np.eye(32,dtype=complex)
for s in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']:
 proj=proj@(np.eye(32)+word(s))/2
vals,vecs=np.linalg.eigh(proj)
V=vecs[:,vals>.5]
zl=V.conj().T@word('ZZZZZ')@V
w,u=np.linalg.eigh(zl); V=V@u[:,::-1]
errors=[np.eye(32,dtype=complex)]
for i in range(5):
 for c in 'XYZ': errors.append(word('I'*i+c+'I'*(4-i)))
D=np.concatenate([E@V for E in errors],axis=1)
assert np.linalg.norm(D.conj().T@D-np.eye(32))<1e-10
res=0.; cases=0
for pw in ['IIIII','XXXXX','ZZZZZ','YYYYY']:
 P=word(pw); PL=V.conj().T@P@V
 for E in errors:
  decoded=(D.conj().T@P@E@V).reshape(16,2,2)
  # Each syndrome block is scalar times the same logical Pauli.
  for blk in decoded:
   c=np.trace(PL.conj().T@blk)/2
   res=max(res,float(np.linalg.norm(blk-c*PL)))
  cases+=1
out['five_qubit_common_Pauli_module_cases']=cases
out['maximum_common_logical_factor_residual']=res
assert res<1e-10
# Independent physical-output error is correctable; a single bad broadcast is logical.
psi=V[:,0]
rho=np.outer(psi,psi.conj())
def logical_decode(r):
 a=(D.conj().T@r@D).reshape(16,2,16,2)
 return np.einsum('aiaj->ij',a)
base=logical_decode(rho)
local=word('XIIII'); dense=word('XXXXX'); p=.03
local_out=logical_decode((1-p)*rho+p*local@rho@local)
broadcast_out=logical_decode((1-p)*rho+p*dense@rho@dense)
local_distance=float(np.linalg.svd(local_out-base,compute_uv=False).sum())
broadcast_distance=float(np.linalg.svd(broadcast_out-base,compute_uv=False).sum())
assert local_distance<1e-10 and abs(broadcast_distance-2*p)<1e-10
out['local_output_error_logical_trace_distance']=local_distance
out['single_master_broadcast_logical_trace_distance']=broadcast_distance
# H6 always no larger than the previously received conservative CNOT bound.
cases=0
for r,m,f,a,ell in itertools.product(range(5), repeat=5):
 pauli=r+4*f*m+2*(1+f*a)*ell
 cnot=2*r+6*f*m+2*(1+f*a)*ell
 assert pauli<=cnot; cases+=1
out['conservative_live_prefix_comparison_cases']=cases
out['scope']='Finite indicator and five-qubit KL algebra checks only; not hardware or threshold simulation.'
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
