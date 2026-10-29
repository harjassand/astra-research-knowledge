from fractions import Fraction as F
import numpy as np,json,math
from pathlib import Path
here=Path(__file__).parent
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);P=[I,X,Z,X@Z];phi=np.array([1,0,0,1],complex)/np.sqrt(2)
# Actual Bell-measurement/correction Kraus maps D,R,B,M -> B,M.
Ks=[]
for Q in P:
 beta=np.kron(I,Q)@phi
 K=np.kron(Q.T,np.eye(2))@np.kron(beta.conj().reshape(1,4),np.eye(4));Ks.append(K)
assert np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(16))<1e-12
rng=np.random.default_rng(2026102945)
trnorm=lambda A:np.linalg.svd(A,compute_uv=False).sum()
rows=[]
for case in range(30):
 A=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));rho=A@A.conj().T;rho/=np.trace(rho)
 # rho_DM tensor Phi_RB, reordered D,M,R,B -> D,R,B,M
 initial=np.kron(rho,np.outer(phi,phi.conj())).reshape([2]*8).transpose(0,2,3,1,4,6,7,5).reshape(16,16)
 H=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));H=(H+H.conj().T)/2
 from scipy.linalg import expm
 U=np.kron(I,expm(1j*(case+1)/200*H));actual=U@initial@U.conj().T
 ideal_branches=[K@initial@K.conj().T for K in Ks];actual_branches=[K@actual@K.conj().T for K in Ks]
 assert max(np.linalg.norm(z-rho/4) for z in ideal_branches)<1e-12
 before=trnorm(actual-initial)/2;after=sum(trnorm(a-b) for a,b in zip(actual_branches,ideal_branches))/2
 assert after<=before+1e-12
 rows.append({'case':case,'initial_correlated_input_memory':True,'resource_joint_distance':float(before),'output_with_public_feedforward_record_distance':float(after)})
each=F(2,5)**7;total=4*each;assert total<F(1,128)
rows_bad=[]
for count in [1,4,100,1000]:
 bad=1-(1-each)**count;assert bad<=count*each
 rows_bad.append({'attempts':count,'first_accept_bad_probability':float(bad),'sum_bound':float(count*each),'accepted_resource_conditional_bad_probability':1})
out={'actual_teleportation_checks':rows,'finite_schedule':{'attempts':4,'payload_qubits':35,'services':155,'t':6,'b':0,'R':'2/3','per_attempt_error':str(each),'total_error':str(total),'target':'1/128','sixstate_service_probability':'4/13','sixstate_call_cap':1840,'matching_service_probability':'1/4','matching_call_cap':2264,'max_acquisition_calls':1000000},'rare_bad_acceptance_counterexample':rows_bad,'scope':'Teleportation CP map with retained classical Bell outcome tested on arbitrary correlated input-memory states. No full155-service quantum resource state simulated; finiteguard soundness is a governing proof dependency.'}
(here/'check_compiler.json').write_text(json.dumps(out,indent=2));print(json.dumps({'checks':30,'total_error':str(total),'max_contraction_residual':max(x['output_with_public_feedforward_record_distance']-x['resource_joint_distance'] for x in rows)},indent=2))
