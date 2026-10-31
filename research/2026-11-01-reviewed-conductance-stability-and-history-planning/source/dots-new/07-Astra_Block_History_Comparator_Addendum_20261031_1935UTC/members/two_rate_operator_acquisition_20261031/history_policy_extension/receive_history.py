#!/usr/bin/env python3
"""Full inherited receiving then deterministic all-history implication.

Fixed original n4096 task prototype. New tolerance is externally requested;
no arbitrary-microscopic/history inference, authenticated randomness, or
standalone independence claim. No frozen source is edited.
"""
from pathlib import Path
import argparse,json,hashlib,sys,time
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent
sys.path.insert(0,str(PARENT/'feedback_extension'))
import replay_polynomial_feedback as old
from retained_large_acquisition import R,sqrt_up


def constants(model,local):
    n=model['n'];parts=model['partition'];ein=R(model['cross_rounds'][-1]['enter'])
    eout=R(model['cross_rounds'][-1]['leave']);t=R(model['coarse_spectral_radius'])
    U=[[R(v) for v in row] for row in local['comparison_matrix']]
    incoming=[ein*sqrt_up(R(n,len(pg))) for pg in parts]
    gains=[sum(sqrt_up(R(len(ph),len(pg)))*U[g][h] for h,ph in enumerate(parts))+
           t*sqrt_up(R(n,len(pg))) for g,pg in enumerate(parts)]
    c=max(incoming);k=max(gains);z=R(0);tail=R(0);zs=[]
    for _ in range(model['length']):
        zs.append(str(z));tail+=eout*z;z=min(R(1),c+k*z)
    fine=R(model['fine_rounds'][-1]['propagated_bound'])
    return {'local_incoming_bounds':[str(x) for x in incoming],'local_residual_gains':[str(x) for x in gains],
       'c':str(c),'kappa':str(k),'residual_caps_before_each_step':zs,
       'compression_bound':str(tail),'fine_bound':str(fine),'history_error_bound':str(tail+fine)}


def run(*,expected_b,expected_ell_num,expected_ell_den,expected_length=24,expected_history_tolerance=R(1,20),expected_confidence=R(1,1000),expected_generators=2):
    timer=time.perf_counter()
    assert type(expected_length) is int and expected_length==24
    assert type(expected_generators) is int and expected_generators==2
    assert not isinstance(expected_confidence,(bool,float)) and R(expected_confidence)==R(1,1000)
    assert not isinstance(expected_history_tolerance,(bool,float)) and R(expected_history_tolerance)>0
    model_bytes=(PARENT/'history_sensitive_4096_result.json').read_bytes()
    local_bytes=(PARENT/'feedback_extension'/'block_comparison_results.json').read_bytes()
    assert hashlib.sha256(model_bytes).hexdigest()==old.BASE_SHA
    model=json.loads(model_bytes);local=json.loads(local_bytes)
    assert (model['task_b'],model['task_ell_numer'],model['task_ell_denominator'])==(expected_b,expected_ell_num,expected_ell_den)
    assert all(type(v) is int and v in (0,1) for v in expected_b+expected_ell_num)
    assert type(expected_ell_den) is int and sum(expected_ell_num)==expected_ell_den>0
    assert model['length']==expected_length and model['m']==expected_generators and R(model['delta'])==R(expected_confidence)
    z=constants(model,local)
    # Preflight only: this can cheaply refuse, but cannot admit before full
    # inherited replay of all sample/probe/model/interface arithmetic.
    assert R(z['history_error_bound'])<=R(expected_history_tolerance)
    received=old.run()
    assert (PARENT/'history_sensitive_4096_result.json').read_bytes()==model_bytes
    assert (PARENT/'feedback_extension'/'block_comparison_results.json').read_bytes()==local_bytes
    assert received['status']=='PASS_POLYNOMIAL_OFFLINE_FEEDBACK'
    assert local['base_result_sha256']==received['base_result_sha256']==old.BASE_SHA
    assert (R(received['confidence']),received['length'],received['generators'])==(R(expected_confidence),expected_length,expected_generators)
    # Recompute after receiving; no selected minimum of distinct norm events.
    z=constants(model,local);E=R(z['history_error_bound']);chosen=R(received['model_error_bound'])
    assert E<=R(expected_history_tolerance)
    v=R(received['plan']['coarse_optimal_value']);regret=E+chosen
    return {'status':'PASS_CANDIDATE_HISTORY_EXTENSION','history_constants':z,
      'requested_history_tolerance':str(expected_history_tolerance),'confidence':str(expected_confidence),
      'horizon':expected_length,'generators':expected_generators,'chosen_policy_error':str(chosen),
      'regret_against_all_block_history_policies':str(regret),'history_error_float':float(E),'regret_float':float(regret),
      'true_history_optimum_upper':str(min(R(1),v+E)),'chosen_policy_true_value_lower':str(max(R(0),v-chosen)),
      'inherited_exact_checks':received['checks'],'inherited_preflight_rejections':received['adversarial_preflight_rejections'],
      'receiving_norm_integer_products':received['this_receiving_norm_integer_products'],
      'new_source_observations':0,'new_norm_probes':0,'new_Bellman_products':received['plan']['scalar_products'],
      'stored_policy_interface':'Same accepted Markov table/map/task masks; no history tree stored or deployed.',
      'scope':'New theorem/receiving extension not independently reviewed yet. Conditional on inherited operator event; fixed original task and offline explicit-state simulator with block observations. Competitors may use all block/action history and private randomness, NOT microscopic-state feedback. Actual chosen planner remains ordinary Markov Bellman DP.',
      'seconds':time.perf_counter()-timer,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'base_receiving_source_sha256':hashlib.sha256((PARENT/'feedback_extension'/'replay_polynomial_feedback.py').read_bytes()).hexdigest(),
      'base_model_sha256':old.BASE_SHA,'local_norm_record_sha256':hashlib.sha256((PARENT/'feedback_extension'/'block_comparison_results.json').read_bytes()).hexdigest()}


def fixture_task():
    raw=(PARENT/'history_sensitive_4096_result.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==old.BASE_SHA
    model=json.loads(raw)
    return dict(expected_b=model['task_b'],expected_ell_num=model['task_ell_numer'],expected_ell_den=model['task_ell_denominator'])


def negative_checks():
    count=0;task=fixture_task()
    for kwargs in [dict(expected_length=23),dict(expected_length=True),dict(expected_generators=1),
                   dict(expected_confidence=R(1,100)),dict(expected_confidence=.001),
                   dict(expected_history_tolerance=0),dict(expected_history_tolerance=.05),
                   dict(expected_history_tolerance=R(1,100))]:
        try:run(**task,**kwargs)
        except AssertionError:count+=1
        else:raise AssertionError('invalid/easier task binding accepted')
    for key,v in [('expected_b',[0]*len(task['expected_b'])),('expected_ell_num',[0]*len(task['expected_ell_num'])),('expected_ell_den',1)]:
        bad=task.copy();bad[key]=v
        try:run(**bad)
        except AssertionError:count+=1
        else:raise AssertionError('changed reward/initial task accepted')
    return count


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    negatives=negative_checks();out=run(**fixture_task());out['additional_history_interface_rejections']=negatives;args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','history_error_float','regret_float','inherited_exact_checks','seconds']},indent=2))
