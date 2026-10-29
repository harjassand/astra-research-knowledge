#!/usr/bin/env python3
"""Counts-only cadence selection, then fresh exact-binomial target decision.
Generator/scorer reads physical endpoint maps. Learner does not.
"""
from pathlib import Path
import json,hashlib,itertools,math
import numpy as np
HERE=Path(__file__).parent
SETTINGS=list(itertools.product([1,2,3],[-1,1]));Q=2**52

def draw_counts(M,N,seed):
 p=np.array([(1-M[j,j]-sg*M[j,0])/2 for j,sg in SETTINGS]);assert np.all(p>=-1e-10) and np.all(p<=1+1e-10)
 cuts=np.floor(np.clip(p,0,1)*Q).astype(np.int64);rng=np.random.default_rng(seed)
 setting=rng.integers(6,size=N);coin=rng.integers(Q,size=N,dtype=np.int64);fail=(coin<cuts[setting]).astype(int)
 counts=np.bincount(2*setting+fail,minlength=12).reshape(6,2)
 return counts,cuts.tolist()

def select_policy(counts_by_policy):
 # Sole learner: no model, noise rate, source matrix or generator access.
 return min(counts_by_policy,key=lambda r:(int(counts_by_policy[r][:,1].sum()),-r))

def exact_validation(k,N):
 # Lower tail under rationalnull p=4/15. All integer arithmetic.
 term=11**N;num=term
 for j in range(k):term=term*(N-j)*4//((j+1)*11);num+=term
 den=15**N;passed=3000*num<=den
 digest=lambda v:hashlib.sha256(v.to_bytes((v.bit_length()+7)//8,'big')).hexdigest()
 return {'failures':k,'N':N,'null_probability':'4/15','alpha':'1/3000','lower_tail_integer_test_pass':passed,'tail_numerator_sha256':digest(num),'tail_denominator_sha256':digest(den)}

def main():
 plan_path=HERE/'HOLDOUT_PLAN_v1.json';plan=json.loads(plan_path.read_text());assert not (HERE/'holdout_counts_v1.npz').exists(),'Do not overwrite sampled evidence'
 scored=json.loads((HERE/'results_v2.json').read_text());out=[];raw={};cdf={};sum_native=0;sum_time=0
 for ci,context in enumerate(plan['context_ids']):
  source_integral=[.03,.1,.3][ci]
  # Source information stays in generator map; the selection function receives counts only.
  maps={row['cadence_r']:row for row in scored['rows'] if row['native_uses']==32 and row['background_integral_per_EC_window']==source_integral}
  counts={};natives=0;elapsed=0
  for r in plan['cadence_policies']:
   M=np.array(maps[r]['encoded']['logical_PTM']);seed=plan['selection_seed_base']+100*ci+r
   cc,cuts=draw_counts(M,plan['selection_shots_per_policy'],seed);counts[r]=cc;key=f'{context}_selection_r{r}';raw[key]=cc;cdf[key]={'seed':seed,'cuts':cuts}
   natives+=int(cc.sum())*5*32;elapsed+=int(cc.sum())*maps[r]['elapsed_reference_time']
  chosen=select_policy(counts)
  M=np.array(maps[chosen]['encoded']['logical_PTM']);seed=plan['validation_seed_base']+100*ci+chosen
  cc,cuts=draw_counts(M,plan['independent_validation_shots'],seed);key=f'{context}_validation';raw[key]=cc;cdf[key]={'seed':seed,'cuts':cuts};test=exact_validation(int(cc[:,1].sum()),int(cc.sum()))
  natives+=int(cc.sum())*5*32;elapsed+=int(cc.sum())*maps[chosen]['elapsed_reference_time'];sum_native+=natives;sum_time+=elapsed
  out.append({'context':context,'selection_failure_counts':{str(r):int(a[:,1].sum()) for r,a in counts.items()},'selected_cadence':int(chosen),'validation':test,'actual_native_carrier_exposures':natives,'aggregate_reference_time':elapsed,'post_selection_source_informed_score_not_given_to_learner':{'background_integral':source_integral,'selected_true_numerical_entanglement_fidelity':1-maps[chosen]['encoded']['entanglement_infidelity'],'best_grid_true_numerical_entanglement_fidelity':max(1-row['encoded']['entanglement_infidelity'] for row in maps.values()),'all_adaptive_single_carrier_Fe_upper_for_selected_schedule':maps[chosen]['source_informed_all_adaptive_single_carrier_Fe_upper']}})
 np.savez_compressed(HERE/'holdout_counts_v1.npz',**raw)
 result={'status':'COMPLETED_COUNTS_ONLY_CADENCE_SELECTION_WITH_FRESH_TARGET_HOLDOUT','plan_sha256':hashlib.sha256(plan_path.read_bytes()).hexdigest(),'source_grid_sha256':hashlib.sha256((HERE/'results_v2.json').read_bytes()).hexdigest(),'raw_counts_sha256':hashlib.sha256((HERE/'holdout_counts_v1.npz').read_bytes()).hexdigest(),'contexts':out,'total_new_native_carrier_exposures':sum_native,'aggregate_reference_time':sum_time,'all_new_trajectories':sum(int(x.sum()) for x in raw.values()),'family_failure_budget':'1/1000 for implementedrecordlaw; finiteCDFquantization contribution at most61440/2^52 versus supplied floatingBornprobabilities','source_frame_training':'inherited earlier pilot, separately paid; not erased','numerical_scope':'No outward-rounded certification of quantum channel coefficients. Exact confidence test is on implemented binaryrecordlaw; physicalfidelity interpretation conditional on trustedlogicalinterface and numericalmodel.'}
 (HERE/'holdout_results_v1.json').write_text(json.dumps(result,indent=2)+'\n');(HERE/'holdout_CDFs_v1.json').write_text(json.dumps(cdf,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
