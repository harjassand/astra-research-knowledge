import numpy as np,math,json
from pathlib import Path
here=Path(__file__).parent;a=np.load(here/'prefix_maps.npz');tr=np.array([1,0,0,1]);J=155;payload=35

def terminal(tp,tf,service,s):
 G=np.linalg.inv(np.eye(4)-(1-s)*tp);S=s*service@G;F=(1-s)*tf@G
 V=np.eye(4,dtype=complex);Sum=np.zeros((4,4),complex)
 for _ in range(J):Sum+=V;V=S@V
 acc=V;end=V+F@Sum;cost=tr@G@Sum
 assert np.linalg.norm(tr@end-tr)<1e-10
 return acc,end,cost
rows=[];terminal_data={}
for m in [100,1000,10000,100000,1000000]:
 sigma=a[f'sigma_{m}'].reshape(-1)
 for method,C in [('six',1.5),('matching',2.)]:
  s=1/(C+1);acc,end,cost=terminal(a[f'{method}_pass_{m}'],a[f'{method}_fail_{m}'],a[f'good_{m}']+a[f'bad_{m}'],s)
  cap=math.ceil((2*J+256)/s);percap=math.exp(-cap*s/8);calltail=percap/(-math.expm1(-s/8))
  for k,v in {'acc':acc,'end':end,'cost':cost}.items():terminal_data[f'{method}_{k}_{m}']=v
  q=sigma.copy();Ac=0.;Ec=0.;records=[]
  for batches in range(1,1001):
   Ac+=float((tr@acc@q).real);Ec+=float((cost@q).real);q=end@q
   if batches in [1,10,100,1000]:
    # Entire repeated experiment differs from uncapped by at most A*percap.
    # Each lost event can affect up to A attempts; conservative totalaccepted-count difference A²*percap.
    # Expectedtotalcall difference uses deterministicfinitecap A*cap plusuncappedtail conservatively.
    records.append({'guard_attempts':batches,'expected_accepted_attempts_uncapped':Ac,'expected_guard_calls_uncapped':Ec,'expected_total_calls_including_calibration':m+Ec,'accepted_payload_qubits_per_total_fullarray_call':payload*Ac/(m+Ec),'accepted_payload_qubits_per_physical_qubit_exposure':payload*Ac/(4*(m+Ec)),'average_acceptance':Ac/batches,'finite_vs_uncapped_path_coupling_error_upper':batches*percap,'finite_vs_uncapped_accepted_count_error_upper':batches*batches*percap})
  rows.append({'calibration_calls':m,'test':method,'C':C,'service_probability':s,'J':J,'payload_qubits':payload,'test_failures_allowed':0,'t':6,'accepted_subnormalized_per_operation_bound':1/128,'finite_cap_per_attempt':cap,'per_attempt_cap_probability_upper':percap,'per_attempt_expected_tail_upper':calltail,'records':records})
np.savez(here/'terminal_memory_maps.npz',**terminal_data)
print(json.dumps({'scope':'Conditional sameone traininghistory; actual retained bath, noreset between deployment attempts. Fixed futureU0 mathematical source, not acquiredpromise. CPsourcegenerator evaluator, not experimentaldata. R1,b0,t6,J155 fixed for allprefixes. Sourceexposures only; trustedcontrols/storage excluded.','results':rows},indent=2))
