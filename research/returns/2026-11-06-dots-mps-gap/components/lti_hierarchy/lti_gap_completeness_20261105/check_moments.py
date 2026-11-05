"""Independent finite-matrix checks for Gram limit and facial reduction."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np, scipy.linalg as la, json
from pathlib import Path
from test_repair import block, iso, canonical, local_apply
OUT=Path(__file__).parent

def partial_first(rho,d,n):
 return np.trace(rho.reshape(d,d**(n-1),d,d**(n-1)),axis1=0,axis2=2)
def partial_last(rho,d,n):
 return np.trace(rho.reshape(d**(n-1),d,d**(n-1),d),axis1=1,axis2=3)

def check(A):
 d,D,_=A.shape;_,sigma=canonical(A)
 E=np.einsum('sij,skl->ikjl',A,A.conj()).reshape(D*D,D*D)
 gram_from_transfer=lambda L:np.linalg.matrix_power(E,L).reshape(D,D,D,D).transpose(0,2,1,3).conj().reshape(D*D,D*D)
 g2=block(A,2).conj().T@block(A,2)
 n=4;dim=d**n;V=iso(A,n);P=V@V.conj().T;Q=np.eye(dim)-P
 G=block(A,n);ground=G@np.kron(sigma.T,np.eye(D))@G.conj().T
 rng=np.random.default_rng(93721);X=rng.normal(size=(dim,7))+1j*rng.normal(size=(dim,7));rho=X@X.conj().T
 # Cyclically symmetrize an arbitrary positive matrix; thus exactly LTI.
 perm=np.arange(dim).reshape([d]*n).transpose([n-1]+list(range(n-1))).reshape(-1)
 rr=rho.copy()
 for i in range(1,n):
  rho=rho[perm,:][:,perm];rr+=rho
 V2=iso(A,2);h=np.eye(d*d)-V2@V2.conj().T
 hs=[local_apply(np.eye(dim),h,(i,i+1),d,n) for i in range(n-1)]
 rr/=np.trace(rr@hs[0]).real
 lifted=rr+1e5*ground;mu=Q@lifted@Q
 err=max(abs(np.trace((lifted-mu)@x)) for x in hs)
 err2=max(abs(np.trace((lifted-mu)@x@y)) for x in hs for y in hs)
 H=sum(hs);ev=la.eigvalsh(H);gap=min(ev[ev>1e-8]);m=n-1
 a=np.trace(rr@hs[0]@hs[0]).real
 bs=[np.trace(rr@(hs[0]@z+z@hs[0])).real for z in hs[1:]]
 v=a+sum(bs);second=np.trace(mu@H@H).real
 return {'transfer_gram_L2_error':float(la.norm(gram_from_transfer(2)-g2,2)),
 'correct_gram_limit_L100_error':float(la.norm(gram_from_transfer(100)-np.kron(np.eye(D),sigma),2)),
 'wrong_transposed_limit_L100_error':float(la.norm(gram_from_transfer(100)-np.kron(np.eye(D),sigma.T),2)),
 'ground_state_trace':float(np.trace(ground).real),
 'ground_LTI_error':float(la.norm(partial_first(ground,d,n)-partial_last(ground,d,n),2)),
 'lifted_LTI_error':float(la.norm(partial_first(lifted,d,n)-partial_last(lifted,d,n),2)),
 'lifted_trace':float(np.trace(lifted).real),'projected_trace':float(np.trace(mu).real),
 'local_energy_preservation_error':float(err),'pair_moment_preservation_error':float(err2),
 'projected_LTI_error':float(la.norm(partial_first(mu,d,n)-partial_last(mu,d,n),2)),
 'trace_bound_m_over_open_gap':float(m/gap),
 'exact_H2_moment_error':float(abs(second-(m*v-sum((r+1)*b for r,b in enumerate(bs))))),
 'H2_upper_bound_slack':float(m*v+2-second)}
inputs=np.load(OUT/'mps_inputs.npz');results={name:check(inputs[key]) for name,key in [('AKLT','aklt'),('generic_complex','generic')]}
print(json.dumps(results,indent=2));(OUT/'moment_checks.json').write_text(json.dumps(results,indent=2)+'\n')
