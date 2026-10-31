#!/usr/bin/env python3
"""Actually execute exact ordinary Bellman DP after acquired family admission."""
from pathlib import Path
import hashlib
import json
import math
import sys
import time
import sympy as s

ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from retained_large_acquisition import R
from large_routing_source import RoutingSource


def pack(values,bits):
    out=bytearray((len(values)*bits+7)//8)
    for i,v in enumerate(values):
        assert type(v) is int and 0<=v<1<<bits
        for k in range(bits):
            if (v>>k)&1:out[(i*bits+k)//8]|=1<<((i*bits+k)%8)
    return bytes(out)


def unpack(blob,count,bits):
    return [sum(((blob[(i*bits+k)//8]>>((i*bits+k)%8))&1)<<k for k in range(bits)) for i in range(count)]


def exact_dp(model):
    r=model['rank'];m=model['m'];L=model['length'];parts=model['partition'];c=model['compiled']
    D=math.lcm(*(a['denominator'] for a in c['operators']))
    A=[[[v*(D//a['denominator']) for v in row] for row in a['numerators']] for a in c['operators']]
    assert all(sum(row)==D and min(row)>=0 for M in A for row in M)
    terminal=[model['task_b'][p[0]] for p in parts];value=terminal[:];policies=[];values=[];ops=0;peak=1
    for t in range(1,L+1):
        nxt=[];policy=[]
        for g in range(r):
            candidates=[]
            for a in range(m):
                z=sum(A[a][g][h]*value[h] for h in range(r));ops+=r;peak=max(peak,z.bit_length())
                candidates.append(z)
            chosen=max(range(m),key=lambda a:(candidates[a],-a));policy.append(chosen);nxt.append(candidates[chosen])
        assert all(0<=v<=D**t for v in nxt)
        value=nxt;policies.append(policy);values.append(value[:])
    initial=[R(sum(model['task_ell_numer'][i] for i in p),model['task_ell_denominator']) for p in parts]
    score=sum(w*v for w,v in zip(initial,value))/D**L
    return {'common_denominator':D,'value_numerators_by_remaining_steps':values,
            'policy_by_remaining_steps':policies,'coarse_optimal_value':str(score),
            'scalar_products':ops,'peak_integer_bits':peak,'denominator_final_bits':(D**L).bit_length(),
            'terminal':terminal,'initial_coarse':[str(x) for x in initial]}


def main():
    start=time.perf_counter();model=json.loads((PARENT/'history_sensitive_4096_result.json').read_text())
    norms=json.loads((ROOT/'feedback_norm_results.json').read_text());r=model['rank'];m=model['m'];n=model['n'];L=model['length']
    assert norms['status']=='MODEL_ADMISSION' and norms['base_result_sha256']==hashlib.sha256((PARENT/'history_sensitive_4096_result.json').read_bytes()).hexdigest()
    expected={tuple((mask>>g)&1 for g in range(r)) for mask in range(1<<r)}
    assert {tuple(x['policy']) for x in norms['policies']}==expected and len(norms['policies'])==m**r
    assert all(R(x['certificate']['delta'])==R(model['delta'])/(8*m**r) for x in norms['policies'])
    plan=exact_dp(model);E=R(norms['model_bound']);value=R(plan['coarse_optimal_value']);eps=R(model['epsilon'])
    assert E<=eps
    which=[0]*n
    for g,p in enumerate(model['partition']):
        for i in p:which[i]=g
    mapbits=max(1,(r-1).bit_length());actionbits=max(1,(m-1).bit_length());files={}
    encoded={'block_map.bin':(which,mapbits),'policy_by_remaining_steps.bin':([x for row in plan['policy_by_remaining_steps'] for x in row],actionbits),
             'initial_support.bin':(model['task_ell_numer'],1),'terminal_indicator.bin':(model['task_b'],1)}
    for name,(values,bits) in encoded.items():
        data=pack(values,bits);assert unpack(data,len(values),bits)==values
        (ROOT/name).write_bytes(data);files[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'entry_bits':bits,'entries':len(values)}
    # Posthoc floating source evaluation only, after all policy decisions.
    source=RoutingSource(n);source._tau=float(R(model['fixture_tau']));truth=model['task_b'][:]
    for policy in plan['policy_by_remaining_steps']:
        candidates=[source.apply_truth(a,truth) for a in range(m)]
        truth=[float(candidates[policy[which[i]]][i]) for i in range(n)]
    true_value=sum(truth[i]*model['task_ell_numer'][i] for i in range(n))/model['task_ell_denominator']
    assert abs(true_value-float(value))<=float(E)
    # Exact Bellman optimality check, independent expression with SymPy
    # rationals for a smaller horizon, including full policy enumeration.
    matrices=[s.Matrix(a['numerators'])/a['denominator'] for a in model['compiled']['operators']]
    v=s.Matrix(plan['terminal']);checks=0
    for t in range(1,4):
        cands=[M*v for M in matrices];want=s.Matrix([max(c[g] for c in cands) for g in range(r)])
        assert want==s.Matrix(plan['value_numerators_by_remaining_steps'][t-1])/plan['common_denominator']**t;checks+=1
        for mask in range(m**r):
            policy=[(mask>>g)&1 for g in range(r)];got=s.Matrix([cands[policy[g]][g] for g in range(r)])
            assert all(got[g]<=want[g] for g in range(r));checks+=1
        v=want
    out={'status':'PASS_OFFLINE_BLOCK_MARKOV_POLICY','plan':plan,'model_error_bound':str(E),
         'true_value_interval':[str(max(R(0),value-E)),str(min(R(1),value+E))],
         'regret_within_acquired_block_markov_class':str(2*E),
         'coarse_policy_value_float':float(value),'posthoc_truth_value_float':true_value,
         'posthoc_scope':'Numerical fixture falsification only; not an acquisition input, physical experiment, or exact world proof.',
         'exact_DP_checks':checks,'packed_files':files,'packed_map_policy_task_bytes':sum(x['bytes'] for x in files.values()),
         'coarse_hot_model_bytes':model['compiled_payload_bytes'],
         'retained_source_calls':norms['retained_forward_calls'],'additional_family_norm_integer_products':norms['additional_integer_products'],
         'norm_scope':'All m^r one-step policy operators explicitly acquired; exponential in rank, not silently polynomial.',
         'hypothetical_simulator_episode':{'initial_sampling':'one draw from explicit normalized initial-support mask',
            'ordinary_forward_source_calls':L,'block_map_lookups':L,'policy_action_lookups':L,'destination_label_updates':L,
            'microscopic_label_bits':(n-1).bit_length(),'physical_sensor':'NOT PROVIDED; output is for an explicit-state simulator'},
         'scope':'Ordinary exact coarse-MDP Bellman planner plus the acquired uniform family certificate. No arbitrary microscopic/history policy optimum; no equipment operated; not independently reviewed.',
         'seconds':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'family_norm_receipt_sha256':hashlib.sha256((ROOT/'feedback_norm_results.json').read_bytes()).hexdigest()}
    (ROOT/'feedback_plan_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','coarse_policy_value_float','posthoc_truth_value_float','exact_DP_checks','packed_map_policy_task_bytes','seconds']},indent=2))


if __name__=='__main__':main()
