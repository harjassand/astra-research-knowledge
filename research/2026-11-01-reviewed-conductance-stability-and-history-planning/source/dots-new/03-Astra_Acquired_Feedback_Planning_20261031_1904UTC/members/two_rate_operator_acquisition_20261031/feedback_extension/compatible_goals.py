#!/usr/bin/env python3
"""Paid ordinary DP for all acquired-block indicator goals; no new observations.

Consumes a received operator certificate; does not itself authenticate/replay
that certificate. See replay_polynomial_feedback.run for full receiving.
"""
from pathlib import Path
import argparse,copy,hashlib,json,sys,time
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from retained_large_acquisition import R
from large_routing_source import RoutingSource
from plan_feedback import exact_dp,pack,unpack


def run():
    start=time.perf_counter();model=json.loads((PARENT/'history_sensitive_4096_result.json').read_text())
    received=json.loads((ROOT/'polynomial_feedback_received.json').read_text())
    assert received['status']=='PASS_POLYNOMIAL_OFFLINE_FEEDBACK'
    assert received['base_result_sha256']==hashlib.sha256((PARENT/'history_sensitive_4096_result.json').read_bytes()).hexdigest()
    n=model['n'];r=model['rank'];m=model['m'];L=model['length'];parts=model['partition'];which=[0]*n
    for g,p in enumerate(parts):
        for i in p:which[i]=g
    E=R(received['model_error_bound']);source=RoutingSource(n);source._tau=float(R(model['fixture_tau']))
    cases=[];checks=0;products=0;maxerr=0.;policybits=[];peak=0
    for mask in range(1<<r):
        goal=[(mask>>g)&1 for g in range(r)];task=copy.deepcopy(model)
        task['task_b']=[goal[which[i]] for i in range(n)]
        plan=exact_dp(task);products+=plan['scalar_products'];peak=max(peak,plan['peak_integer_bits'])
        policybits.extend(a for row in plan['policy_by_remaining_steps'] for a in row)
        # Check exact Bellman equalities/action ties at every stage separately.
        D=plan['common_denominator'];v=goal[:]
        mats=[[[z*(D//A['denominator']) for z in row] for row in A['numerators']] for A in model['compiled']['operators']]
        for t,policy in enumerate(plan['policy_by_remaining_steps']):
            candidates=[[sum(M[g][h]*v[h] for h in range(r)) for g in range(r)] for M in mats]
            want=[max(z[g] for z in candidates) for g in range(r)]
            assert want==plan['value_numerators_by_remaining_steps'][t];checks+=1
            assert all(candidates[policy[g]][g]==want[g] for g in range(r));checks+=1;v=want
        # Posthoc actual-world floating evaluation only, never acquired input.
        truth=task['task_b'][:]
        for policy in plan['policy_by_remaining_steps']:
            values=[source.apply_truth(a,truth) for a in range(m)]
            truth=[float(values[policy[which[i]]][i]) for i in range(n)]
        tasks=[]
        for g,p in enumerate(parts):
            value=R(v[g],D**L);actual=sum(truth[i] for i in p)/len(p);err=abs(float(value)-actual)
            assert err<=float(E);checks+=1;maxerr=max(maxerr,err)
            tasks.append({'initial_block':g,'coarse_value':str(value),'posthoc_truth_float':actual,
                          'value_interval':[str(max(R(0),value-E)),str(min(R(1),value+E))]})
        cases.append({'terminal_block_indicator':goal,'plan':plan,'initial_block_tasks':tasks})
    blob=pack(policybits,max(1,(m-1).bit_length()));assert unpack(blob,len(policybits),1)==policybits;checks+=1
    return {'status':'PASS_COMPATIBLE_GOAL_REUSE','checks':checks,'goals':1<<r,'initial_block_tasks':r*(1<<r),
       'plans':cases,'planning_scalar_products':products,'peak_planning_integer_bits':peak,
       'goal_policy_table_packed_bytes':len(blob),'goal_policy_table_sha256':hashlib.sha256(blob).hexdigest(),
       'goal_indicator_table_packed_bytes':((1<<r)*r+7)//8,'additional_forward_acquisition_calls':0,
       'shared_block_map_packed_bytes':(n*max(1,(r-1).bit_length())+7)//8,
       'initial_block_sampling':'Uniform named-state rejection using retained block map: expected n/|block|=4 draws/lookups in this balanced fixture. No free initial sensor or inverse membership table assumed.',
       'maximum_posthoc_truth_error':maxerr,'uniform_model_error_bound':str(E),
       'regret_within_acquired_block_markov_class':str(2*E),
       'retained_observation_calls':model['logical_forward_calls'],
       'same_information_comparator':'Ordinary exact reduced-MDP Bellman planning plus this acquired operator certificate gives exactly the same plans; no exclusive planner advantage.',
       'scope':'Conditional on previously received operator event. Restricted future block-indicator rewards and block-uniform initials. All 16 DPs executed; truth checks are numerical falsification, not acquisition input or exact full-world proof. 12288 product ledger excludes independent test recomputation and n-state diagnostic work.',
       'seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'received_certificate_sha256':hashlib.sha256((ROOT/'polynomial_feedback_received.json').read_bytes()).hexdigest()}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    out=run();args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','checks','goals','initial_block_tasks','planning_scalar_products','maximum_posthoc_truth_error','seconds']},indent=2))
