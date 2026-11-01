#!/usr/bin/env python3
"""Paid ordinary Bellman + finite-population service certificate, new work."""
from pathlib import Path
import hashlib,json,math,sys,time
import sympy as s
import numpy as np
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent/'two_rate_operator_acquisition_20261031'
sys.path.insert(0,str(BASE/'tagged_pool_retention'));sys.path.insert(0,str(BASE))
import receive_tagged as received
from joint_source import TaggedPoolSource
from retained_large_acquisition import R,clog2,sqrt_up,eb_radius
TASK={'length':24,'generators':2,'workers':1000000,'learning_confidence':'1/1000','deployment_risk':'1/1000000000','model_tolerance':'1/50','reward':['0','1','0','0'],'minimum_service_fraction':'3/5','source_task_sha256':received.TASK_SHA,'broadcast_interface':'block_action_table','initial_law':'frozen_original_uniform_support'}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate(task):
    assert type(task) is dict and set(task)==set(TASK)
    for k in ('length','generators','workers'):assert type(task[k]) is int and task[k]>0
    assert task['length']==24 and task['generators']==2
    for k in ('learning_confidence','deployment_risk','model_tolerance','minimum_service_fraction'):
        assert type(task[k]) in (str,int) and 0<R(task[k])<1
    assert R(task['learning_confidence'])==R(1,1000)
    assert type(task['reward']) is list and len(task['reward'])==4 and all(type(v) in (str,int) and 0<=R(v)<=1 for v in task['reward'])
    assert task['source_task_sha256']==received.TASK_SHA and task['broadcast_interface']=='block_action_table' and task['initial_law']=='frozen_original_uniform_support'

def integer_plan(operators,initial,reward,L):
    m=len(operators);r=len(initial);A=[s.Matrix(x) for x in operators];w=list(map(R,reward));p=list(map(R,initial))
    assert type(L) is int and L>=0 and len(w)==r and min(w)>=0 and max(w)<=1 and min(p)>=0 and sum(p)==1
    assert all(M.shape==(r,r) and min(M)>=0 and M*s.ones(r,1)==s.ones(r,1) for M in A)
    D=math.lcm(*(int(x.q) for M in A for x in M));F=math.lcm(*(int(x.q) for x in w));mats=[[[int(x*D) for x in M.row(g)] for g in range(r)] for M in A]
    v=[int(x*F) for x in w];tables=[];values=[];products=0;peak=F.bit_length()
    for j in range(1,L+1):
        nxt=[];table=[]
        for g in range(r):
            cs=[sum(mats[a][g][h]*v[h] for h in range(r)) for a in range(m)];products+=m*r
            peak=max(peak,*(x.bit_length() for x in cs));a=max(range(m),key=lambda a:(cs[a],-a));nxt.append(cs[a]);table.append(a)
        v=nxt;tables.append(table);values.append(v[:]);assert min(v)>=0 and max(v)<=F*D**j
    score=sum(x*y for x,y in zip(p,v))/(F*D**L)
    return {'denominator':D,'reward_denominator':F,'coarse_value':str(score),'policy_by_remaining_steps':tables,'value_numerators':values,'scalar_products':products,'peak_integer_bits':peak,'final_denominator_bits':(F*D**L).bit_length()}

def concentration(N,L,r,m,delta,*,mode='adaptive_tables'):
    assert all(type(x) is int and x>0 for x in (N,L,r,m)) and not isinstance(delta,(bool,float)) and 0<R(delta)<1
    assert mode in ('adaptive_tables','adaptive_actions','fixed_terminal_goal')
    if mode=='fixed_terminal_goal':K=R(7,10)*clog2(1/R(delta))
    else:K=R(7,10)*(r+L*clog2(m)*(r if mode=='adaptive_tables' else 1)+clog2((L+1)/R(delta)))
    eta=sqrt_up(K/(2*N),bits=40);assert eta*eta>=K/(2*N)
    return {'mode':mode,'log_union_upper':str(K),'eta':str(eta),'eta_float':float(eta),'sqrt_rounding_bits':40}

def run(*,task,expected_task_digest):
    start=time.perf_counter();assert type(expected_task_digest) is str and digest(task)==expected_task_digest;validate(task)
    rec=received.run(expected_length=task['length'],expected_generators=task['generators'],expected_confidence=R(task['learning_confidence']),expected_record_tolerance=R(task['model_tolerance']),expected_task_sha256=task['source_task_sha256'])
    assert rec['first_admitted_prefix'] is not None
    attempt=rec['attempts'][rec['first_admitted_prefix']];E=R(attempt['record_error_bound'])
    # Select operators FROM THE SAME admitted prefix; never combine cheap earlier
    # acquisition cost with later improved operators or certificate.
    model=json.loads((BASE/'history_sensitive_4096_result.json').read_text());parts=model['partition'];r=len(parts);n=model['n'];L=task['length'];m=task['generators'];N=task['workers']
    initial=[R(sum(model['task_ell_numer'][i] for i in part),model['task_ell_denominator']) for part in parts]
    plan=integer_plan(attempt['coarse_operators'],initial,task['reward'],L);value=R(plan['coarse_value']);kappa=max(map(R,task['reward']))-min(map(R,task['reward']))
    uniform=concentration(N,L,r,m,R(task['deployment_risk']));scalar=concentration(N,L,r,m,R(task['deployment_risk']),mode='fixed_terminal_goal')
    eta=R(uniform['eta']);etas=R(scalar['eta']);theta=R(task['minimum_service_fraction']);indicator=all(R(x) in (0,1) for x in task['reward'])
    lower=max(R(0),value-E-etas);admit=indicator and lower>theta
    return {'status':'PASS_CONDITIONAL_POPULATION_SERVICE' if admit else 'REFUSED_POPULATION_SERVICE','task':task,'task_sha256':expected_task_digest,'prefix_used':attempt['prefix'],'plan':plan,'model_error':str(E),'acquisition_confidence':task['learning_confidence'],'acquisition_failure_budget_upper':rec['failure_budget_upper'],'population_uniform':uniform,'fixed_policy_scalar_tail':scalar,'fixed_policy_service_lower_with_probability_1_minus_risk':str(lower) if indicator else None,'adaptive_population_expected_regret_upper':str(min(1,2*kappa*(E+eta)+2*R(task['deployment_risk']))),'conditional_deployment_risk':task['deployment_risk'],'unconditional_joint_bad_event_upper':str(R(task['learning_confidence'])+R(task['deployment_risk'])),'prospective_source_calls_to_used_prefix':attempt['prospective_total_calls'],'actual_new_calls_all_prefixes':rec['new_logical_source_calls_actually_generated'],'actual_prior_full_acquisition_not_refunded':rec['actual_prior_full_acquisition_not_refunded'],'receiving_checks':rec['checks'],'receiving_norm_products':0,'coarse_model_entries':m*r*r,'partition_lookup_entries':n,'nominal_packed_partition_bytes':(n*max(1,(r-1).bit_length())+7)//8,'nominal_packed_policy_bytes':(L*r*max(1,(m-1).bit_length())+7)//8,'initial_support_mask_bytes':(n+7)//8,'deployment_source_calls':N*L,'deployment_initial_draws':N,'deployment_map_and_action_lookups_each':N*L,'population_count_updates':N*(L+1),'scope':'Ordinary Bellman plus acquired same-prefix local certificate and finite-class population concentration. Unknown physical independence/sensor/source truth not certified. Risk is conditional on valid learning, not unconditional 1e-9. No superior single-goal acquisition claim. New unreviewed work.','seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'receiver_sha256':hashlib.sha256((BASE/'tagged_pool_retention/receive_tagged.py').read_bytes()).hexdigest()}

class PopulationSimulator:
    """Source-side fixture only; private wiring never used by the planner."""
    def __init__(self,seed):self.q=TaggedPoolSource(seed=seed);self.calls=0;self.max_categorical_array_entries=0
    def step(self,states,actions):
        assert states.dtype==actions.dtype==np.int64 and states.ndim==actions.ndim==1 and len(states)==len(actions)
        assert np.all((states>=0)&(states<self.q.n)) and np.all((actions>=0)&(actions<self.q.m))
        br=self.q.rng.multinomial(1,self.q.branch,size=len(states));self.max_categorical_array_entries=max(self.max_categorical_array_entries,br.size)
        kind=br.argmax(axis=1);del br
        out=np.empty_like(states)
        for k in range(4):
            ix=np.flatnonzero(kind==k);ss=states[ix];aa=actions[ix];nn=len(ix)
            if k==0:out[ix]=self.q.adj[aa,ss,self.q.rng.integers(self.q.degree,size=nn)]
            elif k==1:out[ix]=self.q.groups[self.q.actions[aa,self.q.which[ss]],self.q.rng.integers(self.q.n//4,size=nn)]
            elif k==2:out[ix]=self.q.glob[aa,ss]
            else:out[ix]=self.q.reset[aa,self.q.rng.integers(self.q.n//2,size=nn)]
        self.calls+=len(states);return out

def deploy(plan,N,*,seed):
    start=time.perf_counter();assert type(N) is int and N>0
    model=json.loads((BASE/'history_sensitive_4096_result.json').read_text());parts=model['partition'];which=np.empty(model['n'],dtype=np.int64)
    for g,part in enumerate(parts):which[part]=g
    support=np.flatnonzero(np.asarray(model['task_ell_numer']));assert all(model['task_ell_numer'][i]==1 for i in support) and len(support)==model['task_ell_denominator']
    source=PopulationSimulator(seed);states=support[source.q.rng.integers(len(support),size=N)];counts=[np.bincount(which[states],minlength=len(parts)).tolist()]
    for table in reversed(plan['policy_by_remaining_steps']):
        actions=np.asarray(table,dtype=np.int64)[which[states]];states=source.step(states,actions);counts.append(np.bincount(which[states],minlength=len(parts)).tolist())
    assert source.calls==N*len(plan['policy_by_remaining_steps']) and all(sum(row)==N for row in counts)
    return {'workers':N,'logical_forward_calls_actually_executed':source.calls,'initial_draws':N,'counts_by_time':counts,'max_categorical_array_entries':source.max_categorical_array_entries,'max_single_categorical_array_bytes':8*source.max_categorical_array_entries,'memory_scope':'Largest categorical array only, NOT process peak memory; state/action/index arrays and runtime also exist.','seed':seed,'seconds':time.perf_counter()-start,'source_branch_exact':[str(x) for x in source.q.branch_exact],'scope':'One simulator realization, not empirical proof of the 1e-9 tail or physical equipment execution.'}

def mc_baseline(plan,*,episodes=250000,confidence=R(1,1000)):
    out=deploy(plan,episodes,seed=7319123);c=out['counts_by_time'][-1][1];K=R(7,10)*clog2(2/confidence);lower=max(0,R(c,episodes)-eb_radius(c,episodes,K))
    eta=R(concentration(TASK['workers'],24,4,2,R(TASK['deployment_risk']),mode='fixed_terminal_goal')['eta'])
    out.update({'kind':'ordinary_fixed_policy_goal_MC','successes':c,'one_sided_K':str(K),'mean_lower':str(lower),'population_service_lower':str(max(0,lower-eta)),'passes_60_percent':bool(lower-eta>R(3,5)),'confidence':str(confidence),'no_model_certificate_required':True,'policy_proposal_source_calls':31588352,'prospective_calls_with_proposal':31588352+out['logical_forward_calls_actually_executed'],'scope':'Ordinary cheaper one-goal feasibility baseline, NOT adaptive-policy near-optimality. Same chosen table is given equally; using a cheaper independent proposal can only improve its bill. Counts for other blocks can also be retained, not discarded.'})
    return out

if __name__=='__main__':
    result=run(task=TASK,expected_task_digest=digest(TASK));(ROOT/'population_plan.json').write_text(json.dumps(result,indent=2)+'\n')
    dep=deploy(result['plan'],TASK['workers'],seed=7319001);(ROOT/'population_deployment.json').write_text(json.dumps(dep,indent=2)+'\n')
    mc=mc_baseline(result['plan']);(ROOT/'population_mc_baseline.json').write_text(json.dumps(mc,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'value':float(R(result['plan']['coarse_value'])),'E':float(R(result['model_error'])),'uniform_eta':result['population_uniform']['eta_float'],'scalar_eta':result['fixed_policy_scalar_tail']['eta_float'],'service_lower':float(R(result['fixed_policy_service_lower_with_probability_1_minus_risk'])),'actual_service_fraction':dep['counts_by_time'][-1][1]/TASK['workers'],'ordinary_MC_lower':float(R(mc['population_service_lower'])),'actual_updates':dep['logical_forward_calls_actually_executed']+mc['logical_forward_calls_actually_executed']},indent=2))
