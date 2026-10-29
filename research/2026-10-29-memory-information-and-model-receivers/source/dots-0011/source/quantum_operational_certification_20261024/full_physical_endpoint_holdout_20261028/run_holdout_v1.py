#!/usr/bin/env python3
"""Fresh endpoint samples and exact binomial acceptance, physical noisy pipeline."""
from pathlib import Path
import json,hashlib,sys,math,numpy as np
HERE=Path(__file__).parent;Q=HERE.parent
sys.path.insert(0,str(Q/'continuous_inverse_control_20261028'));import pulse_pipeline_v1 as pulse
p=json.loads((HERE/'PLAN_v1.json').read_text());src=Q/p['channel_source'];assert hashlib.sha256(src.read_bytes()).hexdigest()==p['channel_sha256']
row=next(x for x in json.loads(src.read_text()) if all(x[k]==v for k,v in p['source_row_parameters'].items()));M=np.array(row['physical_output_PTM']);m=pulse.m
Rin=m.ptm(m.old.rotation(m.old.Y,p['outer_preparation_Y_rotation_angle']));Rout=m.ptm(m.old.rotation(m.old.X,p['outer_measurement_X_rotation_angle']));observed=Rout@M@Rin
probs=[]
for j in [1,2,3]:
 for sign in [-1,1]:probs.append(float((1-observed[j,j]-sign*observed[j,0])/2))
assert all(0<=x<=1 for x in probs)
assert math.sin(abs(p['outer_preparation_Y_rotation_angle'])/2)<=.001
assert math.sin(abs(p['outer_measurement_X_rotation_angle'])/2)<=.001
N=p['N'];bits=p['source_CDF_bits'];cuts=np.floor(np.array(probs)*2**bits).astype(np.uint64)
out=HERE/'raw_trials_v1.npz';assert not out.exists(),'No overwriting or reselection of holdout'
rng=np.random.default_rng(p['seed']);settings=rng.integers(0,6,N,dtype=np.uint8);uniforms=rng.integers(0,2**bits,N,dtype=np.uint64);fail=(uniforms<cuts[settings]);np.savez_compressed(out,settings=settings,failures=fail)
k=int(np.sum(fail));num,den=p['null_observed_failure_probability'];q=den-num;D=pow(den,N);term=pow(q,N);tail=term;critical=-1
for j in range(N+1):
 if tail*1000<=D:critical=j
 else:break
 term=term*(N-j)*num//((j+1)*q);tail+=term
term=pow(q,N);numtail=term
for j in range(k):term=term*(N-j)*num//((j+1)*q);numtail+=term
accepted=numtail*1000<=D
result={'status':'AUTHOR_FRESH_SIMULATED_HOLDOUT','plan_sha256':hashlib.sha256((HERE/'PLAN_v1.json').read_bytes()).hexdigest(),'N':N,'failures':k,'critical_failures':critical,'accept_Fe_at_least_0_8':accepted,'exact_tail_numerator_sha256':hashlib.sha256(hex(numtail).encode()).hexdigest(),'exact_tail_denominator_sha256':hashlib.sha256(hex(D).encode()).hexdigest(),'tail_diagnostic_float':math.exp(math.log(numtail)-math.log(D)),'counts_by_setting':[{'setting':j,'n':int(np.sum(settings==j)),'failures':int(np.sum(fail[settings==j]))} for j in range(6)],'source_failure_probabilities':probs,'CDF_thresholds':cuts.tolist(),'CDF_total_variation_bound':N/2**bits,'trusted_SPAM_budget_sum':.002,'posthoc_physical_Fe':1-row['entanglement_infidelity'],'posthoc_observed_Fe':float(np.trace(observed)/4),'posthoc_mean_failure_probability':float(np.mean(probs)),'new_physical_native_exposures':N*5*p['source_row_parameters']['T'],'physical_pipeline_time_per_trial':row['full_elapsed_time'],'external_time_per_trial':p['external_time_per_trial'],'new_aggregate_reference_time':N*(row['full_elapsed_time']+p['external_time_per_trial']),'scope':'Simulated fresh iid six-state endpoint trials, trusted/calibrated external SPAM, frozen complete pipeline. No hardware measurements; no inherited ideal-logical holdout reused; no policy learning or changed controller inferred.'}
(HERE/'RESULT_v1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
