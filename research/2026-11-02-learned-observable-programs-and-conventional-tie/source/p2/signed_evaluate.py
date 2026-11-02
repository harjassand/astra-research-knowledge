import json,hashlib,math
from pathlib import Path
from signed_execute import common_programs,growth_and_error,intervention_schedule,SignedInterpreter
from signed_reference import reference
ROOT=Path(__file__).parent
if __name__=='__main__':
    v1=json.loads((ROOT/'frozen_programs.json').read_text())
    v2bytes=(ROOT/'signed_frozen_v2.json').read_bytes()
    assert hashlib.sha256(v2bytes).hexdigest()=='893cbb5ca0cf8790d5abb28ea54e5f2069a61534b4ecdc8372826fd04bf7be96'
    v2=json.loads(v2bytes)
    prog=common_programs(v1,v2)
    spec=json.loads((ROOT/'signed_heldout_contract.json').read_text())
    interp=SignedInterpreter(prog)
    result=[]
    for j,job in enumerate(spec['cases']):
        n=job['n'];q=job['query'];schedule=intervention_schedule(n,job['schedule'],q[0]);T=sum(x[0] for x in schedule)
        run=interp.estimate(n,q,schedule,job['paths'],seed=9171+j,delta=.001/len(spec['cases']))
        cert=growth_and_error(prog,T,len(q))
        assert cert['valid']
        width=cert['model_error']+run['MC_halfwidth']
        run.update(name=job['name'],schedule=job['schedule'],model_error=cert['model_error'],
                   combined_interval=[run['estimator']-width,run['estimator']+width],
                   combined_halfwidth=width,large_state_space=f'2^{n}')
        if n<=9:
            exact=reference(n,q,schedule)
            run['reference']=exact
            run['observed_discrepancy']=abs(exact-run['estimator'])
            assert abs(exact-run['estimator'])<=width
        if len(q)==1:
            p=[(v+1)/2 for v in run['combined_interval']]
            threshold=spec['threshold_probability_plus']
            run['prob_plus_interval']=p
            run['decision']='above' if p[0]>threshold else 'below' if p[1]<threshold else 'unresolved'
        result.append(run)
        print(job['name'],'estimated',round(run['estimator'],6),'interval',list(map(lambda x:round(x,5),run['combined_interval'])),
              'truth',run.get('reference'), 'prob_plus',run.get('prob_plus_interval'), 'decision',run.get('decision'),
              'events',run['counters']['events'],'neg',run['counters']['negative_transitions'])
    out={'v2_frozen_hash':hashlib.sha256(v2bytes).hexdigest(),'extension_model_certificate':growth_and_error(prog,1.2,1),
         'heldout_spec':spec,'results':result,'total_events':sum(q['counters']['events'] for q in result),
         'total_wall_seconds':sum(q['wall_seconds'] for q in result),
         'joint_source_failure':'<48*exp(-22) (<1.4e-8)',
         'joint_MC_failure':'<=0.001'}
    (ROOT/'signed_heldout_results.json').write_text(json.dumps(out,indent=2,sort_keys=True))
