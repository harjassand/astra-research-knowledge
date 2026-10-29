"""Independent six-state/SPAM calculation, raw-record replay and integer-tail polynomial."""
from pathlib import Path
import json,hashlib,math,numpy as np
D=Path(__file__).parent;A=D.parent;Q=A.parent
plan=json.loads((A/'PLAN_v1.json').read_text());result=json.loads((A/'RESULT_v1.json').read_text());raw=np.load(A/'raw_trials_v1.npz');source=Q/plan['channel_source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==plan['channel_sha256']
row=next(r for r in json.loads(source.read_text()) if all(r[k]==v for k,v in plan['source_row_parameters'].items()));M=np.array(row['physical_output_PTM'])
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[I,X,Y,Z]
a=plan['outer_preparation_Y_rotation_angle'];b=plan['outer_measurement_X_rotation_angle'];U=np.cos(a/2)*I-1j*np.sin(a/2)*Y;V=np.cos(b/2)*I-1j*np.sin(b/2)*X
probs=[];preperr=[];effecterr=[]
for axis in [1,2,3]:
 for sign in [-1,1]:
  rho=(I+sign*P[axis])/2;actual=U@rho@U.conj().T;effect=(I-sign*P[axis])/2;actualeffect=V.conj().T@effect@V
  coeff=np.array([np.trace(p@actual).real for p in P]);outcoeff=M@coeff;out=sum(outcoeff[j]*P[j]/2 for j in range(4));probs.append(float(np.trace(actualeffect@out).real))
  preperr.append(float(np.linalg.eigvalsh(actual-rho).__abs__().sum()/2));effecterr.append(float(np.linalg.norm(actualeffect-effect,2)))
assert max(preperr)<.001 and max(effecterr)<.001
prob_error=float(np.max(abs(np.array(probs)-result['source_failure_probabilities'])));print("probability discrepancy",prob_error,probs);assert prob_error<1e-12
# Exact law is declared floor-CDF of the stored floating source probabilities.
cuts=np.floor(np.array(result['source_failure_probabilities'])*2**plan['source_CDF_bits']).astype(np.uint64);assert cuts.tolist()==result['CDF_thresholds']
N=plan['N'];rng=np.random.default_rng(plan['seed']);settings=rng.integers(0,6,N,dtype=np.uint8);uniforms=rng.integers(0,2**plan['source_CDF_bits'],N,dtype=np.uint64);failure=uniforms<cuts[settings]
assert np.array_equal(settings,raw['settings']) and np.array_equal(failure,raw['failures'])
k=int(failure.sum());assert k==4026==result['failures']
# Independent integer polynomial instead of the author's full-binomial-mass recurrence.
def numerator(k):
 c=1;power=1;poly=1
 for j in range(1,k+1):
  c=c*(N-j+1)//j;power*=197;poly=1303*poly+c*power
 return 1303**(N-k)*poly
num=numerator(k);den=1500**N
assert hashlib.sha256(hex(num).encode()).hexdigest()==result['exact_tail_numerator_sha256'];assert hashlib.sha256(hex(den).encode()).hexdigest()==result['exact_tail_denominator_sha256']
assert num*1000<=den and numerator(4115)*1000<=den and numerator(4116)*1000>den
assert result['critical_failures']==4115 and result['accept_Fe_at_least_0_8']
assert result['new_physical_native_exposures']==N*5*32==5242880
elapsed=N*(row['full_elapsed_time']+sum(plan['external_time_breakdown'].values()));assert abs(elapsed-result['new_aggregate_reference_time'])<1e-7
# Algebraic null conversion and exact union/coupling contribution.
from fractions import Fraction as F
assert F(2,3)*(1-F(4,5))-F(1,1000)-F(1,1000)==F(197,1500)
assert result['CDF_total_variation_bound']==N/2**52
files=[A/'PLAN_v1.json',A/'run_holdout_v1.py',A/'GOVERNING_HOLDOUT_v1.md',A/'RESULT_v1.json',A/'raw_trials_v1.npz',source,Path(__file__)]
out={'status':'PASS_FRESH_PHYSICAL_ENDPOINT_IMPLEMENTED_RECORD_LAW','trials_replayed':N,'failures':k,'critical_failures':4115,'independent_density_probability_error':prob_error,'actual_external_preparation_max_trace_distance':max(preperr),'actual_external_effect_max_operator_error':max(effecterr),'new_native_exposures':N*160,'aggregate_trajectory_time':elapsed,'new_acquisition_draws':0,'sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(D/'check_holdout_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
