#!/usr/bin/env python3
"""Genuinely alternative learner: no inherited per-round acquired frame.
Source truth creates endpoint Born records and scores results; fit sees counts.
"""
from pathlib import Path
import numpy as np,json,sys,hashlib
import oracle_and_endpoint_fit_v1 as o
HERE=Path(__file__).parent;Q=HERE.parent
sys.path.insert(0,str(Q/'five_qubit_acquired_frame_pilot_20261028'))
import code_and_channels as c

def main():
 scenarios=[('zero_clock_v1',0.),('rate_0.01_v1',.01),('rate_0.1_v1',.1)]
 plan={'status':'EXPLORATORY_FIXED_BEFORE_DRAWING_THIS_PILOT_NOT_A_CONFIRMATORY_TEST','budgets_total_native_uses':[20480,102400],'horizons':[1,8,32],'all_sites':list(range(5)),'scenarios':scenarios,'seed_base':720000,'per_round_control':'identity; no acquired inverse or inherited training data','estimator':'balanced ordinary±Pauli endpoint experiments, empirical3x3Bloch matrix, properProcrustes terminalunitary','source_informed_scoring_only':True}
 pp=HERE/'DIRECT_ENDPOINT_PLAN_v2.json'
 if pp.exists():assert json.loads(pp.read_text())==json.loads(json.dumps(plan))
 else:pp.write_text(json.dumps(plan,indent=2)+'\n')
 srcs=c.generator_sources();rawlocal=[np.array(s['PTM'],float) for s in srcs]
 raw={};runs=[];oracle_rows=[]
 for si,(label,strength) in enumerate(scenarios):
  clockpath=Q/'clocked_flagged_storage_20261028'/f'{label}.json';clock=json.loads(clockpath.read_text());tau=clock['timing']['total_EC_time'];roundtime=tau+2
  idle=np.diag([1,np.exp(-strength),np.exp(-strength),1]);perround=[idle@M for M in rawlocal]
  ends={(i,T):np.linalg.matrix_power(perround[i],T) for i in range(5) for T in plan['horizons']}
  oracle_rows.append({'scenario':label,'sites':[{'site':i,'results':[{'T':T,'raw_endpoint_PTM':ends[i,T].tolist(),'raw_no_final_correction_infidelity':1-o.fe(ends[i,T]),'full_CPTP_final_oracle_infidelity':1-o.oracle(ends[i,T])[1]} for T in plan['horizons']]} for i in range(5)]})
  for B in plan['budgets_total_native_uses']:
   for T in plan['horizons']:
    N=B//(5*T);rr={'scenario':label,'budget_total_native_uses':B,'T':T,'endpoint_shots_per_site':N,'actual_native_uses':5*N*T,'native_uses_for_prior_inverse_training':0,'duration_per_endpoint_round_reference_units':roundtime,'aggregate_channel_elapsed_time_reference_units':5*N*T*roundtime,'ideal_five_site_parallel_channel_time_reference_units':N*T*roundtime,'endpoint_preparation_readout_and_terminal_pulse_time':'not included; must be separately charged','sites':[]}
    for i in range(5):
     seed=plan['seed_base']+si*100000+B+100*T+i;key=f'{label}_B{B}_T{T}_site{i}';M=ends[i,T];counts=o.sample_counts(M,N,seed);raw[key]=counts;R,Ahat=o.fit(counts);opt=o.oracle(M)[1];score=o.fe(R@M)
     assert score<=opt+1e-12
     rr['sites'].append({'site':i,'seed':seed,'counts_key':key,'fitted_Bloch_matrix':Ahat.tolist(),'fitted_terminal_recovery_PTM':R.tolist(),'scorer_true_entanglement_infidelity':1-score,'source_informed_full_CPTP_oracle_infidelity':1-opt,'scorer_regret_vs_oracle':opt-score})
    runs.append(rr)
 rawp=HERE/'direct_endpoint_counts_v2.npz'
 if rawp.exists():
  prev=np.load(rawp);assert set(prev.files)==set(raw);assert all(np.array_equal(prev[k],v) for k,v in raw.items())
 else:np.savez(rawp,**raw)
 out={'status':'EXPLORATORY_ORDINARY_ENDPOINT_ACQUISITION_WITH_NO_PER_ROUND_LEARNED_INVERSE','source_generator_sha256':hashlib.sha256((Q/'five_qubit_acquired_frame_pilot_20261028/code_and_channels.py').read_bytes()).hexdigest(),'raw_counts_sha256':hashlib.sha256(rawp.read_bytes()).hexdigest(),'oracle_rows':oracle_rows,'runs':runs,'scope':'Each run separately satisfies its stated total native-calibration budget. Runs are alternative experiments, not jointly within one budget. True infidelities are simulator scores, not statistical confidence bounds. No adaptive site selection or extra candidate tuning. Constant2unit nativephase duration is inherited from clockmodel; its identity per-roundcontrol replaces learnedinverse without changing declared total window.'}
 (HERE/'direct_endpoint_no_per_round_inverse_v2.json').write_text(json.dumps(out,indent=2)+'\n')
 for r in runs:
  if r['T']==32:print(r['scenario'],r['budget_total_native_uses'],'fit_range',min(s['scorer_true_entanglement_infidelity'] for s in r['sites']),max(s['scorer_true_entanglement_infidelity'] for s in r['sites']),'oracle_range',min(s['source_informed_full_CPTP_oracle_infidelity'] for s in r['sites']),max(s['source_informed_full_CPTP_oracle_infidelity'] for s in r['sites']))
if __name__=='__main__':main()
