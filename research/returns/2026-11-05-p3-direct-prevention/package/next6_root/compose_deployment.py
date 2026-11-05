"""Exact finite composition, using recorded binary data; no new observations.

Physical one-bit read service and operating warm-up costs are evaluated,
not executed on hardware. All issuing arithmetic is Fraction/integer.
"""
from pathlib import Path
from fractions import Fraction as F
import json
from decision_certificate import structural,display

def main():
    root=Path(__file__).parent
    data=json.loads((root/'direct_decision_execution.json').read_text())
    read_error=F(1,4000); delay=F(1,1000); healthy_floor=F(3,16)
    accept=(1-read_error)*healthy_floor
    initial_failure=(read_error+F(1,4)*delay)/accept
    abort=F(1,1000); tries=1
    while (1-accept)**tries>abort: tries+=1
    # Warm-up at least 2: exp(.8)>1+.8+.8^2/2>2,
    # hence recovery probability exceeds 3/16 under the given bounds.
    time_cap=tries*(F(2001,1000)+delay)
    rows=[]
    for row in data['results']:
        c,x=structural(row['structural']['N'])
        N=c['N']; L=c['L_analysis_only']; p=x['p_upper']; ell=x['q0S_lower']
        tail=F(1,1<<c['binary_tail_exponent'])/x['g']
        A=(1-x['return_bound'])*(1-p)*(1-x['remainder']/ell)
        B=1+(L*p+tail)/ell
        km=F(row['kminus']); kp=F(row['kplus']); bias=F(row['conditional_bias_budget'])
        intervals={}
        for u,e in row['envelopes'].items():
            lo=F(e['mean_lower_fraction']); hi=F(e['mean_upper_fraction'])
            intervals[u]=(max(F(0),(lo-bias)/kp),(hi+bias)/km)
        chosen=row['chosen']
        eq={u:ell/x['q0S_upper']*v[0]/intervals[chosen][1]
            for u,v in intervals.items() if u!=chosen}
        safe={u:v*A/B for u,v in eq.items()}
        actual={u:v*(1-initial_failure) for u,v in safe.items()}
        warm_failure=F(13,16)**N+N*F(1,4)*F(1,1000)*F(13,16)**(N-1)
        warm={u:v*(1-warm_failure) for u,v in safe.items()}
        overall=min([F(1),*actual.values()])
        rows.append({'N':N,'safe_start_lower':display(A),'safe_start_upper':display(B),
          'lower_ratio_to_each_competitor_any_safe_start':{u:display(v) for u,v in safe.items()},
          'lower_ratio_to_each_competitor_one_bit_preparation':{u:display(v) for u,v in actual.items()},
          'selected_to_best_successful_preparation_lower':display(overall),
          'selected_to_best_abort_zero_lower':display((1-abort)*overall),
          'certifies_best_after_one_bit_preparation':all(v>1 for v in actual.values()),
          'no_inspection_warmup_initial_failure_upper':display(warm_failure),
          'no_inspection_warmup_selected_to_best_lower':display(min([F(1),*warm.values()])),
          'no_inspection_warmup_system_time_cap':'2.001',
          'no_inspection_warmup_component_exposure_cap':display(N*F(2001,1000)),
          'system_warmup_and_latency_cap':display(time_cap),
          'summed_component_exposure_cap':display(N*time_cap)})
    result={'status':'exact composition of existing executed data and evaluated, unexecuted physical service',
      'service':{'capture_read_error':str(read_error),'max_capture_to_mission_delay':str(delay),
        'warmup_interval':['2','2.001'],'certified_working_probability_floor':str(healthy_floor),
        'acceptance_floor':str(accept),'conditional_initial_failure_upper':str(initial_failure),
        'attempt_cap':tries,'abort_upper':str(abort),
        'additional_costs':'One actual-system noninvasive capture/read per attempt; timer, setup, installation, propagation, finite slew and settling are paid separately.'},
      'rows':rows,'statistical_confidence_from_record':data['statistical_confidence_all_four_runs'],
      'arithmetic':'Fraction/integer throughout; displayed decimals are rounded.'}
    (root/'deployment_composition.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
