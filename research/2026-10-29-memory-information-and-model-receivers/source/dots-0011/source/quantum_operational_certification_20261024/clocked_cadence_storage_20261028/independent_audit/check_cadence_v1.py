#!/usr/bin/env python3
"""Independent cadence/record audit, conditional on the separate F-map review.
No author cadence or selection/test routines are invoked. Originals not written.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import numpy as np,json,math,hashlib,itertools,sys
HERE=Path(__file__).parent;SRC=HERE.parent;Q=SRC.parent
sys.path.insert(0,str(Q/'clocked_flagged_storage_20261028'));import clocked_channel_v1 as primitive
P=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]

def exact_tail(k,N):
 # Different integer evaluation: factor11^(N-k) out of a degree-k polynomial.
 choose=1;power4=1;power11=11**k;poly=0
 for j in range(k+1):
  poly+=choose*power4*power11
  if j<k:choose=choose*(N-j)//(j+1);power4*=4;power11//=11
 return poly*11**(N-k),15**N

def digest(i):return hashlib.sha256(i.to_bytes((i.bit_length()+7)//8,'big')).hexdigest()

def main():
 plan=json.loads((SRC/'HOLDOUT_PLAN_v1.json').read_text());grid=json.loads((SRC/'results_v2.json').read_text());claimed=json.loads((SRC/'holdout_results_v1.json').read_text());cdf=json.loads((SRC/'holdout_CDFs_v1.json').read_text());raw=np.load(SRC/'holdout_counts_v1.npz')
 # Independently construct full Pauli basis and encoded operators from matrices.
 basis=[np.ones((1,1),complex)]
 for _ in range(5):basis=[np.kron(a,p) for a in basis for p in P]
 basis=np.array(basis);Enc,Rec=primitive.c.exact_encoder_recovery();Enc=np.array(Enc,complex);Rec=[np.array(R,complex) for R in Rec]
 encops=np.array([Enc@p@Enc.conj().T for p in P]);initial=np.einsum('wij,bji->wb',basis,encops).real
 def decode(A):
  rho=np.einsum('wb,wij->bij',A,basis)/32
  logical=np.array([sum((R@a@R.conj().T for R in Rec),np.zeros((2,2),complex)) for a in rho])
  return np.array([[np.trace(p@b).real/2 for b in logical] for p in P])
 assert np.max(abs(decode(initial)-np.eye(4)))<1e-13
 natives=primitive.native();N=np.ones((1,1))
 for M in natives:N=np.kron(N,M)
 clock=grid['clock'];maxdiff=0.;maxbase=0.;rows_checked=0;order_counterexample=0.
 for integral in grid['plan']['background_integral_per_EC_window']:
  F,timing=primitive.build_ec(grid['plan']['eta'],integral/201,clock)
  assert timing['total_EC_time']==201
  idle=np.diag([1,np.exp(-integral),np.exp(-integral),1])
  for r in grid['plan']['cadences']:
   A=initial.copy()
   for t in range(1,65):
    # Direct every-native-use step, no power of local maps or decoded channels.
    A=N@A
    if t%r==0:A=F@A
    if t not in (32,64):continue
    row=next(x for x in grid['rows'] if x['background_integral_per_EC_window']==integral and x['cadence_r']==r and x['native_uses']==t)
    actual=decode(A);maxdiff=max(maxdiff,float(np.max(abs(actual-np.array(row['encoded']['logical_PTM'])))));rows_checked+=1
    assert row['EC_windows']==t//r and row['elapsed_reference_time']==2*t+201*(t//r)
    assert row['encoded_native_carrier_exposures']==5*t and row['unencoded_native_carrier_exposures_per_site']==t
    for site,M in enumerate(natives):
     B=np.eye(4)
     for u in range(1,t+1):
      B=M@B
      if u%r==0:B=idle@B
     maxbase=max(maxbase,float(np.max(abs(B-np.array(row['same_elapsed_unencoded'][site]['logical_PTM'])))))
     wrong=np.linalg.matrix_power(idle,t//r)@np.linalg.matrix_power(M,t)
     order_counterexample=max(order_counterexample,float(np.max(abs(B-wrong))))
  print('audited primitive-conditioned cadence',integral,flush=True)
 assert maxdiff<3e-11 and maxbase<3e-12
 # Version1 was preserved; version2 only casts bool and changes output path.
 v1=(SRC/'cadence_sweep_v1.py').read_text();v2=(SRC/'cadence_sweep_v2.py').read_text()
 expected=v1.replace("'encoded_Fe_exceeds_all_adaptive_single_carrier_ceiling':1-score['entanglement_infidelity']>adaptive_ceiling", "'encoded_Fe_exceeds_all_adaptive_single_carrier_ceiling':bool(1-score['entanglement_infidelity']>adaptive_ceiling)").replace('results_v1.json','results_v2.json')
 assert expected==v2
 # Independently replay all settings/coins/counts from immutable CDF records.
 settings=list(itertools.product([1,2,3],[-1,1]));Q52=2**52;total_native=0;total_time=0.;total_trials=0;seeds=[];outcomes=[];allcuts_match=True
 for ci,context in enumerate(plan['context_ids']):
  integral=[.03,.1,.3][ci];maps={x['cadence_r']:x for x in grid['rows'] if x['background_integral_per_EC_window']==integral and x['native_uses']==32}
  failure_counts={}
  def replay(key,N,M):
   nonlocal total_trials,allcuts_match
   cdfrow=cdf[key];seed=cdfrow['seed'];seeds.append(seed)
   probs=[(1-M[j,j]-sg*M[j,0])/2 for j,sg in settings]
   assert all(0<=p<=1 for p in probs)
   cuts=[math.floor(p*Q52) for p in probs];assert cuts==cdfrow['cuts'];allcuts_match &= cuts==cdfrow['cuts']
   rng=np.random.Generator(np.random.PCG64(seed));ss=rng.integers(low=0,high=6,size=N);uu=rng.integers(low=0,high=Q52,size=N,dtype=np.int64);counts=np.zeros((6,2),int)
   for s,u in zip(ss,uu):counts[int(s),int(u<cuts[int(s)])]+=1
   assert np.array_equal(counts,raw[key]);total_trials+=N
   return int(counts[:,1].sum())
  native=0;elapsed=0.
  for r in plan['cadence_policies']:
   key=f'{context}_selection_r{r}';Nsel=plan['selection_shots_per_policy'];M=np.array(maps[r]['encoded']['logical_PTM']);failure_counts[r]=replay(key,Nsel,M)
   assert cdf[key]['seed']==plan['selection_seed_base']+100*ci+r
   native+=Nsel*5*32;elapsed+=Nsel*(64+201*(32//r))
  chosen=sorted(failure_counts,key=lambda r:(failure_counts[r],-r))[0]
  key=f'{context}_validation';Nv=plan['independent_validation_shots'];k=replay(key,Nv,np.array(maps[chosen]['encoded']['logical_PTM']))
  assert cdf[key]['seed']==plan['validation_seed_base']+100*ci+chosen
  num,den=exact_tail(k,Nv);ok=3000*num<=den;cr=claimed['contexts'][ci];val=cr['validation']
  assert cr['selected_cadence']==chosen
  assert val['failures']==k and val['lower_tail_integer_test_pass']==ok
  assert digest(num)==val['tail_numerator_sha256'] and digest(den)==val['tail_denominator_sha256']
  native+=Nv*5*32;elapsed+=Nv*(64+201*(32//chosen));total_native+=native;total_time+=elapsed
  assert cr['actual_native_carrier_exposures']==native and cr['aggregate_reference_time']==elapsed
  outcomes.append({'context':context,'chosen':chosen,'validation_failures':k,'pass':ok,'native_uses':native,'summed_trajectory_elapsed_time':elapsed})
 assert len(set(seeds))==len(seeds)
 assert total_native==claimed['total_new_native_carrier_exposures']==9830400
 assert total_time==claimed['aggregate_reference_time']==127838208
 assert total_trials==claimed['all_new_trajectories']==61440
 # Exact threshold boundary, separately obtained by forward binomial weights.
 Ntest=8192;term=11**Ntest;num=term;den=15**Ntest;critical=-1
 for k in range(Ntest+1):
  if 3000*num<=den:critical=k
  else:break
  term=term*(Ntest-k)*4//((k+1)*11);num+=term
 assert 3000*exact_tail(critical,Ntest)[0]<=den<3000*exact_tail(critical+1,Ntest)[0]
 result={'status':'PASS_INDEPENDENT_CADENCE_RECORD_SCOPE_CONDITIONAL_ON_PRIMITIVE_EC_MAP','physical_grid_rows':rows_checked,'max_encoded_PTM_difference':maxdiff,'max_baseline_PTM_difference':maxbase,'max_difference_if_background_order_incorrectly_collapsed':order_counterexample,'all_61440_binary_trials_reproduced':True,'all_CDFs_recomputed':allcuts_match,'independent_exact_tail_digests_match':True,'exact_pass_failure_count_maximum_for_N8192':critical,'outcomes':outcomes,'native_exposure_total':total_native,'summed_trajectory_elapsed_time':total_time,'not_qubit_time':True,'v1_v2_change_only_documented_serialization':True,'oracle_and_adaptive_ceiling_theorems':'Not independently reviewed by this task; reliance only at their separately accepted scope.'}
 (HERE/'check_cadence_v1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
