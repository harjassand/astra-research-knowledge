#!/usr/bin/env python3
"""Nonmutating exact diagnostics and full generation/receiving replay."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb
import contextlib,copy,hashlib,io,json,re,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
import interval_comparator as ic
import goal_hazard as gh
import check_source_transport as st
R=ic.R

def equal_payload(actual,expected):
    a=copy.deepcopy(actual);b=copy.deepcopy(expected)
    a.pop('seconds',None);b.pop('seconds',None)
    # JSON text equality is deliberate: Python's bool/int and int/float aliases
    # must not silently turn a changed saved record into the same certificate.
    assert json.dumps(a,sort_keys=True)==json.dumps(b,sort_keys=True)

def diagnostics():
    checks=0
    for lo,hi in [([R(0)]*3,[R(1)]*3),([R(1,10),R(2,10),R(3,10)],[R(5,10),R(6,10),R(7,10)]),([R(1,3)]*3,[R(1,3)]*3)]:
        vertices=[]
        for free in range(3):
            other=[i for i in range(3) if i!=free]
            for ends in product((0,1),repeat=2):
                p=[R(0)]*3
                for i,e in zip(other,ends):p[i]=(lo,hi)[e][i]
                p[free]=1-sum(p)
                if lo[free]<=p[free]<=hi[free]:vertices.append(p)
        for value in product((R(-1),R(0),R(1)),repeat=3):
            scores=[sum(x*y for x,y in zip(p,value)) for p in vertices]
            for maximize in (False,True):
                assert ic.extremize(lo,hi,value,maximize)==(max(scores) if maximize else min(scores));checks+=1
    # Exact finite-binomial coverage checks for the monotone maximum wrapper.
    zeta=R(1,10);K=R(7,10)*ic.clog2(2/zeta)
    for N in (20,50,100):
        U=[R(1) if 2*c>N else min(R(1),R(c,N)+ic.eb_radius(c,N,K)) for c in range(N+1)]
        assert all(x<=y for x,y in zip(U,U[1:]));checks+=N
        for p in (R(1,20),R(1,5),R(2,5),R(7,10),R(19,20)):
            failure=sum(R(comb(N,c))*p**c*(1-p)**(N-c) for c in range(N+1) if U[c]<p)
            assert failure<=zeta;checks+=1
        ps=[R(1,5),R(2,5),R(3,5)];threshold=[c for c in range(N+1) if U[c]<max(ps)]
        # All rows independently low is the exact failure event of U(max C).
        joint=R(1)
        for p in ps:joint*=sum(R(comb(N,c))*p**c*(1-p)**(N-c) for c in threshold)
        assert joint<=zeta;checks+=1
    # Arbitrary microstate/history optimality is covered by full-state Bellman.
    rng=np.random.default_rng(6831)
    for _ in range(12):
        matrices=[]
        for a in range(2):
            M=[]
            for i in range(4):
                row=list(map(int,rng.integers(1,10,size=4)));M.append([R(v,sum(row)) for v in row])
            matrices.append(M)
        lower=[[[min(sum(matrices[a][i][j] for j in (2*h,2*h+1)) for i in (2*g,2*g+1)) for h in range(2)] for g in range(2)] for a in range(2)]
        upper=[[[max(sum(matrices[a][i][j] for j in (2*h,2*h+1)) for i in (2*g,2*g+1)) for h in range(2)] for g in range(2)] for a in range(2)]
        for L in range(6):
            plan=ic.plan_interval(lower,upper,[R(0),R(1)],L);opt=[R(0),R(0),R(1),R(1)];chosen=opt[:]
            for policy in plan['policy_by_remaining_steps']:
                opt=[max(sum(matrices[a][i][j]*opt[j] for j in range(4)) for a in range(2)) for i in range(4)]
                chosen=[sum(matrices[policy[i//2]][i][j]*chosen[j] for j in range(4)) for i in range(4)]
            for i in range(4):
                assert R(plan['lower'][i//2])<=chosen[i]<=opt[i]<=R(plan['upper'][i//2]);checks+=1
    return checks

def max_rational_bits(x):
    if isinstance(x,str) and re.fullmatch(r'-?\d+(?:/\d+)?',x):
        q=F(x);return max(q.numerator.bit_length(),q.denominator.bit_length())
    if type(x) is int:return x.bit_length()
    if isinstance(x,dict):return max([0]+[max_rational_bits(v) for v in x.values()])
    if isinstance(x,list):return max([0]+[max_rational_bits(v) for v in x])
    return 0

def run():
    start=time.perf_counter();checks=diagnostics()
    with contextlib.redirect_stdout(io.StringIO()):generated=ic.run()
    saved=json.loads((ROOT/'interval_comparison_results.json').read_text());equal_payload(generated,saved);checks+=1
    # Full actual replay happened before the following cached negative checks.
    transport=st.run();equal_payload(transport,json.loads((ROOT/'source_transport_checks.json').read_text()));checks+=transport['checks']
    result=gh.run();equal_payload(result,json.loads((ROOT/'goal_hazard_results.json').read_text()));checks+=1
    negatives=0
    for kwargs in [dict(expected_length=23),dict(expected_length=True),dict(expected_generators=1),dict(expected_confidence=R(1,10)),dict(expected_confidence=.001),dict(expected_regret=True),dict(expected_regret=-1),dict(expected_task_sha256='bad')]:
        try:gh.run(**kwargs)
        except (AssertionError,ValueError,TypeError):negatives+=1
        else:raise AssertionError('task alias accepted')
    for path,value in [(('attempts',2,'prospective_total_calls'),1),(('attempts',2,'per_row_samples'),93185),(('attempts',2,'fresh_policy_evaluation','successes'),155966),(('attempts',2,'fresh_policy_evaluation','episodes'),250001),(('attempts',2,'fresh_policy_evaluation','outcome_bits_sha256'),'bad'),(('attempts',2,'plan','policy_by_remaining_steps',0,0),True),(('confidence',),'1/10'),(('actual_fresh_simulated_transitions',),1)]:
        mutant=copy.deepcopy(saved);v=mutant
        for k in path[:-1]:v=v[k]
        v[path[-1]]=value
        try:equal_payload(generated,mutant)
        except AssertionError:negatives+=1
        else:raise AssertionError('mutated payload accepted')
    assert result['first_admitted_prefix']==2 and R(result['attempts'][2]['certified_regret'])<R('0.05650530389526265');checks+=2
    countfile=ic.PARENT/'history_sensitive_4096_observations.json.gz'
    return {'status':'PASS_FULL_ORDINARY_COMPARATOR_REPLAY','exact_checks':checks,'negative_checks':negatives,'fresh_transitions_reexecuted':generated['actual_fresh_simulated_transitions'],'acquisition_attempts':3,'source_calls_are_not_refunded':True,'proposal_plus_row_plus_fresh_calls':result['attempts'][2]['prospective_total_calls'],'goal_regret':result['attempts'][2]['certified_regret'],'goal_regret_float':result['attempts'][2]['regret_float'],'interval_regret_float':generated['attempts'][2]['regret_float'],'max_serialized_rational_component_bits':max(max_rational_bits(result),max_rational_bits(saved)),'interval_bellman_products_all_attempts':sum(z['plan']['bellman_scalar_products'] for z in generated['attempts']),'retained_sizes':{'full_compressed_original_transcript_conservative_bytes':countfile.stat().st_size,'interval_result_bytes':(ROOT/'interval_comparison_results.json').stat().st_size,'hazard_result_bytes':(ROOT/'goal_hazard_results.json').stat().st_size,'endpoint_bit_bytes':sum((ROOT/f'policy_outcomes_prefix{j}.bin').stat().st_size for j in range(3))},'scope':'Full nonmutating replay, then explicit cached payload-negative tests. Source truth/iid/provenance not authenticated. Count and packed policy/map/task interface storage additional to scalar table. Exact diagnostics are fixtures, not a proof of all possible inputs.','seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    out=run();(ROOT/'comparator_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='goal_regret'},indent=2))
