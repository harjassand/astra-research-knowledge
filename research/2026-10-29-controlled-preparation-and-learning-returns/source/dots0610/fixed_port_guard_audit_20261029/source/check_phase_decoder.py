import numpy as np,json
from pathlib import Path
from itertools import product
from collections import Counter
from construct_inner import rbasis,sp,array,transform,low_errors,syndrome
from received_algebra_compiler_v1 import compile_algebra,unitary,pauli
ROOT=Path(__file__).parent
# Exact uniform flag multiplicities, n3,k1,r2.
n=3;counts=Counter()
for v in range(1,1<<(2*n)):
 for w in range(1,1<<(2*n)):
  if w!=v and sp(v,w,n)==0:
   # unique nonzero span set, independent of generating order
   counts[tuple(sorted((v,w,v^w)))]+=1
assert len(counts)==315 and set(counts.values())=={6}
# For fixed nonzero e, exactly75/315 subspaces have e in S-perp.
assert sum(all(sp(1,v,n)==0 for v in key) for key in counts)==75
# Known perfect five-qubit code, used only as small dense decoder fixture.
strings=['XZZXI','IXZZX','XIXZZ','ZXIXZ'];n=5;k=1;r=4
rows=[]
for st in strings:
 rows.append(sum((1<<j if c in 'XY' else 0)|(1<<(n+j) if c in 'ZY' else 0) for j,c in enumerate(st)))
out=compile_algebra(array(rows,n),n);gates=out['gates'];U=np.eye(2**n,dtype=complex)
for g in gates:U=unitary(g,n)@U
E=U.conj().T[:,:2]
errors=list(low_errors(n,1));table={};ops=[];phase_error=0.
for e in errors:
 v0=array([e],n)[0];phase=(e&(e>>n)).bit_count()%4;P=(1j**phase)*pauli(v0,n);ops.append(P)
 q,ph=transform(e,phase,gates,n);Q=(1j**ph)*pauli(array([q],n)[0],n)
 phase_error=max(phase_error,float(np.linalg.norm(U@P@U.conj().T-Q)))
 sy=q&15;logical=(q>>4)&1|(((q>>9)&1)<<1)
 assert sy not in table;table[sy]=logical
assert len(table)==16
# Decoder CP maps: U then measure ancillas, apply inverse logical representative.
# No postselection, all16 outcomes defined.
X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);I=np.eye(2)
def correction(sy):
 l=table.get(sy,0);return np.linalg.matrix_power(Z,(l>>1)&1)@np.linalg.matrix_power(X,l&1)
# Matrix element QEC check: all correctable-pair compressed products scalar I.
kl=0
for P in ops:
 for Q in ops:
  A=E.conj().T@P.conj().T@Q@E;kl=max(kl,float(np.linalg.norm(A-np.trace(A)*I/2)))
rng=np.random.default_rng(53329);maxerr=0.;maxnorm=0.
for case in range(12):
 # Arbitrary L:M:R entanglement, not a product-state-only test.
 psi=rng.normal(size=(2,2,4))+1j*rng.normal(size=(2,2,4));psi/=np.linalg.norm(psi)
 w=rng.random(16);w/=w.sum();bath=[]
 for j in range(16):
  A=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));Q,R=np.linalg.qr(A);bath.append(Q)
 encoded=np.einsum('al,lmr->amr',E,psi)
 acted=sum(np.sqrt(w[j])*np.einsum('ab,mu,bur->amr',ops[j],bath[j],encoded) for j in range(16))
 maxnorm=max(maxnorm,float(abs(np.linalg.norm(acted)-1)))
 after=np.einsum('ab,bmr->amr',U,acted).reshape(16,2,2,4)
 got=np.zeros((16,16),complex)
 for sy in range(16):
  vec=np.einsum('ij,jmr->imr',correction(sy),after[sy]).reshape(-1);got+=np.outer(vec,vec.conj())
 target=np.zeros((16,16),complex)
 for j in range(16):
  vec=np.einsum('mu,lur->lmr',bath[j],psi).reshape(-1);target+=w[j]*np.outer(vec,vec.conj())
 maxerr=max(maxerr,float(np.linalg.norm(got-target)))
assert max(phase_error,kl,maxerr,maxnorm)<1e-12
res={'uniform_isotropic_flag_exact':{'n':3,'k':1,'subspaces':315,'ordered_flags_each':6,'normalizer_contains_fixed_vector':75},'dense_five_qubit_fixture':{'correctable_paulis':16,'all_syndromes_total':True,'phase_conjugation_residual':phase_error,'KL_scalar_residual':kl,'coherent_joint_memory_cases':12,'correlated_LMR_output_residual':maxerr,'restricted_isometry_norm_residual':maxnorm},'scope':'Exact GF2 enumeration plus floating dense coherent quantum checks; not an execution of the large concatenated outer code.'}
(ROOT/'phase_decoder_results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
