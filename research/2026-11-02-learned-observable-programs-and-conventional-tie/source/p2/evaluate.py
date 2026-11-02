"""Second stage: frozen program tested on withheld systems and mode schedules.
Source truth rates are used solely in the heldout full-state reference (n<=9).
"""
import json,math,hashlib
from pathlib import Path
from execute import LearnedInterpreter, make_schedule, model_error_envelope
from reference import exact_reference
from source_device import BATHS # EVALUATION ONLY, never used in learner/executor

ROOT=Path(__file__).parent
if __name__=='__main__':
    original=(ROOT/'frozen_programs.json').read_bytes()
    frozen_hash=hashlib.sha256(original).hexdigest()
    frozen=json.loads(original)
    programs=frozen['programs']
    spec=json.loads((ROOT/'heldout_contract.json').read_text())
    assert frozen_hash=='3581c7c1f8de3d8db9e11e634cc38c15b7f38a2574d0d3df8897f4becbdbde95'
    interpreter=LearnedInterpreter(programs)
    results=[]
    for ix,job in enumerate(spec['holdouts']):
        n=job['n'];query=job['query'];policy=job['policy']
        schedule=make_schedule(n,policy,query[0])
        T=sum(t for t,_ in schedule)
        prediction=interpreter.monte_carlo(n,query,schedule,job['trajectories'],seed=223000+ix,
                                             confidence_failure=.001/len(spec['holdouts']))
        model=model_error_envelope(programs,T,len(query))
        prediction.update(name=job['name'],policy=policy,
              model_error=model['model_error_upper'],
              total_halfwidth=prediction['statistical_halfwidth']+model['model_error_upper'],
              total_interval=[prediction['sample_mean']-prediction['statistical_halfwidth']-model['model_error_upper'],
                              prediction['sample_mean']+prediction['statistical_halfwidth']+model['model_error_upper']],
              predicted_event_prob=(prediction['sample_mean']+1)/2 if len(query)==1 else None,
              n_native_states=f'2^{n}',
              errors_under_joint_event=True)
        if n<=9:
            truth=exact_reference(n,query,schedule,BATHS)
            prediction['heldout_full_CTMC_truth']=truth
            prediction['observed_error']=abs(prediction['sample_mean']-truth)
            assert prediction['observed_error']<=prediction['total_halfwidth'],prediction
        if len(query)==1:
            prediction['prob_plus_interval']=[(z+1)/2 for z in prediction['total_interval']]
            prediction['decision_threshold']=spec['decision_threshold_probability_plus']
            prediction['certified_decision']=('above_threshold' if prediction['prob_plus_interval'][0]>prediction['decision_threshold']
                                              else 'below_threshold' if prediction['prob_plus_interval'][1]<prediction['decision_threshold']
                                              else 'undetermined')
        results.append(prediction)
        print(job['name'],'result=',round(prediction['sample_mean'],6),'interval=',list(map(lambda x:round(x,5),prediction['total_interval'])),
              'event_prob=',prediction.get('prob_plus_interval'), 'reference=',prediction.get('heldout_full_CTMC_truth'),
              'decision=',prediction.get('certified_decision'), 'events=',prediction['total_events'],
              'wall=',round(prediction['wall_seconds'],2))
    out={'frozen_sha256':frozen_hash,'heldout_contract':spec,'dual_growth_certificate':model_error_envelope(programs,1.2,1),
         'results':results,'total_events':sum(v['total_events'] for v in results),
         'total_dual_wall_seconds':sum(v['wall_seconds'] for v in results),
         'confidence_statement':'16-source-cell failure probability <32exp(-22); MC 6 tasks joint <=0.001 by union bound, excluding RNG finite machine defects'}
    (ROOT/'heldout_results.json').write_text(json.dumps(out,indent=2,sort_keys=True))
    assert hashlib.sha256((ROOT/'frozen_programs.json').read_bytes()).hexdigest()==frozen_hash
