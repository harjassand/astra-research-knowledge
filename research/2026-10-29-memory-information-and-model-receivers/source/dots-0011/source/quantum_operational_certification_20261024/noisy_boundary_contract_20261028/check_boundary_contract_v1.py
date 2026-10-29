"""Exact code target and independent noisy six-state identity checks."""
from pathlib import Path
import importlib.util,hashlib,json
import sympy as s
import numpy as np
D=Path(__file__).parent;Q=D.parent
source=Q/'five_qubit_acquired_frame_pilot_20261028/code_and_channels.py'
spec=importlib.util.spec_from_file_location('code_source',source);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
V,R=c.exact_encoder_recovery()
W=s.Matrix.hstack(*[r.H for r in R])
assert W.H*W==s.eye(32)
assert W[:,:2]==V
for a,r in enumerate(R):assert W.H[2*a:2*a+2,:]==r
# Equality on all 1024 matrix units follows from the exact Kraus-row equality.
# Exhibit why an arbitrary encoder extension can decode differently on errors.
Z=s.diag(1,-1);change=s.eye(32);change[2:4,2:4]=Z
Wbad=W*change
assert Wbad[:,:2]==V and Wbad.H*Wbad==s.eye(32)
plus=s.Matrix([1,1])/s.sqrt(2);input_on_syndrome_1=W[:,2:4]*plus
bad_output=Wbad.H*input_on_syndrome_1
assert bad_output[2:4,:]==Z*plus
# Test six-state identity, SPAM robustness, and endpoint-composition fidelity bound.
rng=np.random.default_rng(20261028)
P=[np.eye(2),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def random_channel():
 A=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2));U=np.linalg.qr(A)[0];return [U[2*a:2*a+2] for a in range(4)]
def apply(Ks,r):return sum(K@r@K.conj().T for K in Ks)
def td(A):return np.linalg.eigvalsh(A).__abs__().sum()/2
max_gap=0.;max_spam_excess=-1.
for _ in range(100):
 Ks=random_channel();M=np.array([[np.trace(a@apply(Ks,b)).real/2 for b in P] for a in P]);Fe=(1+np.trace(M[1:,1:]))/4
 p=0.;obs=0.;budget=0.
 for j in range(1,4):
  for sign in [-1,1]:
   rho=(P[0]+sign*P[j])/2;effect=P[0]-rho
   # Independent imperfect preparation and binary-effect mixing.
   a,b=rng.uniform(0,.2,2);rr=(1-a)*rho+a*(P[0]-rho);ee=(1-b)*effect+b*(P[0]-effect)
   p+=np.trace(effect@apply(Ks,rho)).real/6;obs+=np.trace(ee@apply(Ks,rr)).real/6
   budget+=(td(rr-rho)+np.linalg.norm(ee-effect,2))/6
 gap=abs(p-2*(1-Fe)/3);max_gap=max(max_gap,gap);assert gap<1e-13
 excess=abs(obs-p)-budget;max_spam_excess=max(max_spam_excess,excess);assert excess<1e-13
out={'status':'PASS_EXACT_TARGET_AND_FLOATING_BOUNDARY_STRESS','unitary_target_exact':True,'Kraus_rows_exact':16,'same_encoder_different_decoder_counterexample':True,'random_qubit_channels':100,'six_state_identity_max_error':max_gap,'max_SPAM_bound_excess':max_spam_excess,'scope':'No hardware circuit or review acceptance asserted','sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,D/'BOUNDARY_REQUIREMENTS_v1.md',Path(__file__)]}}
(D/'check_boundary_contract_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
