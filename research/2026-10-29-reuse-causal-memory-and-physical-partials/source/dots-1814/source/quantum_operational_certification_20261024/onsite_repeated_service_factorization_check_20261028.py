"""Author algebra fixtures, not acquired source data or physical experiments."""
import numpy as np,json,hashlib
from pathlib import Path
rng=np.random.default_rng(281037)
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex);P=[I,X,Y,Z]
def kron(a):
 o=np.array([[1]],complex)
 for x in a:o=np.kron(o,x)
 return o
def embed(a,j):return kron([a if k==j else I for k in range(3)])
def apply(r,ks):return sum((k@r@k.conj().T for k in ks),np.zeros_like(r))
res=[]
for case in range(32):
 u=rng.normal(size=4);u/=np.linalg.norm(u);W=u[0]*I-1j*sum((u[k+1]*P[k+1] for k in range(3)),np.zeros((2,2),complex))
 a,b=rng.uniform(.05,.95,2);K=[np.diag(np.sqrt([a,b])),X@np.diag(np.sqrt([1-a,1-b]))]
 # Two noncommuting memory Kraus operators; no memory reset between slots.
 A=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));rho=A@A.conj().T;rho/=np.trace(rho)
 exact=rho.copy();learned=rho.copy()
 for slot in [0,1]:
  ek=[embed(P[j],slot)@embed(K[j],2) for j in range(2)]
  lk=[embed(Q.conj().T@W@P[j]@Q,slot)@embed(K[j],2)/2 for Q in P for j in range(2)]
  exact=apply(exact,ek);learned=apply(learned,lk)
 predicted=exact
 for slot in [0,1]:predicted=apply(predicted,[embed(Q.conj().T@W@Q,slot)/2 for Q in P])
 er=float(np.max(np.abs(predicted-learned)));assert er<2e-14
 # Pauli coefficients and exact two-distinct-output identity mass.
 probs=np.array([abs(np.trace(Q.conj().T@W)/2)**2 for Q in P]);assert abs(probs.sum()-1)<2e-14
 e=1-probs[0];assert 1-(1-e)**2<=2*e+1e-14
 res.append({'factorization_max_abs':er,'single_identity_probability':float(probs[0]),'two_output_extra_failure':float(1-probs[0]**2)})
p=Path(__file__).resolve().parent
out={'status':'PASS_AUTHOR_FLOATING_ALGEBRA_FIXTURES','cases':len(res),'maximum_residual':max(x['factorization_max_abs'] for x in res),'source_calls':0,'acquisition_outcomes':0,'initial_state':'arbitrary full-rank correlated two-input plus memory density','retained_memory_reset':False,'not_claimed':['formal floating certificate','gate synthesis','calibration simulation','hardware'],'cases_detail':res,'source_sha256':hashlib.sha256((p/'ordinary_onsite_repeated_service_factorization_20261028.md').read_bytes()).hexdigest()}
(p/'onsite_repeated_service_factorization_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['maximum_residual'])
