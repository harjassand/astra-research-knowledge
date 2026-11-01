#!/usr/bin/env python3
"""Exact small algebra/counterfactual tests plus real acquisition/deployment replay."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import copy,hashlib,json,math,time
import sympy as s
import population as p
ROOT=Path(__file__).resolve().parent

def strip(x):
    if isinstance(x,dict):return {k:strip(v) for k,v in x.items() if k!='seconds'}
    if isinstance(x,list):return list(map(strip,x))
    return x

def small():
    checks=0
    def ck(x):
        nonlocal checks
        assert x;checks+=1
    # Pure rational proof constant: exp(.7)>2 already at a finite partial sum.
    ck(sum(F(7,10)**j/F(math.factorial(j)) for j in range(7))>2)
    # Counterfactual coupling, with state/action dependent kernels and adaptive
    # occupancy-selected block action tables. No oracle in implementation.
    A=[[[F(1,2),F(1,2)],[F(0),F(1)]],[[F(1),F(0)],[F(1,2),F(1,2)]]]
    tables=list(product(range(2),repeat=2));words=list(product(tables,repeat=2));true={}
    for word in words:
        law=[F(1,2),F(1,2)];path=[law]
        for table in word:
            law=[sum(law[g]*A[table[g]][g][h] for g in range(2)) for h in range(2)];path.append(law)
        true[word]=path
    def trajectory(bits,word):
        states=list(bits[:2]);path=[states[:]]
        for t,table in enumerate(word):
            states=[int(F(bits[2+2*t+j],2)>=A[table[g]][g][0]) for j,g in enumerate(states)];path.append(states[:])
        return path
    for bits in product(range(2),repeat=6):
        states=list(bits[:2]);actual=[states[:]];word=[]
        for t in range(2):
            table=(0,1) if sum(states)==1 else ((1,1) if sum(states)==0 else (0,0));word.append(table)
            states=[int(F(bits[2+2*t+j],2)>=A[table[g]][g][0]) for j,g in enumerate(states)];actual.append(states[:])
        word=tuple(word);ck(actual==trajectory(bits,word))
        allmax=max(abs(F(sum(trajectory(bits,w)[t]),2)-true[w][t][1]) for w in words for t in range(3))
        ck(all(abs(F(sum(actual[t]),2)-true[word][t][1])<=allmax for t in range(3)))
    # Unequal block geometry: table row selection preserves EACH incoming-TV,
    # outgoing dual-norm and fine bound, rather than a fictitious contraction.
    n=5;parts=[[0,1],[2,3,4]];Z=s.zeros(n,2);W=s.zeros(2,n)
    for g,part in enumerate(parts):
        for i in part:Z[i,g]=1;W[g,i]=s.Rational(1,len(part))
    P=Z*W;Q=s.eye(n)-P
    mats=[]
    for a in range(3):
        vals=[[((i+2)*(j+3)+3*a+i*j)%11+1 for j in range(n)] for i in range(n)]
        mats.append(s.Matrix([[s.Rational(x,sum(row)) for x in row] for row in vals]))
    def constants(M):
        B=W*M*Z;c=max(sum(abs(x) for x in (M*Z-Z*B).row(i))/2 for i in range(n));e2=max(n*sum(x*x for x in (W*M*Q).row(g)) for g in range(2))
        return c,e2,B
    triples=[constants(M) for M in mats];c=max(x[0] for x in triples);e2=max(x[1] for x in triples)
    for table in product(range(3),repeat=2):
        M=s.Matrix([list(mats[table[0 if i<2 else 1]].row(i)) for i in range(n)]);ci,ei,B=constants(M)
        ck(ci<=c and ei<=e2);ck(B==s.Matrix([list(triples[table[g]][2].row(g)) for g in range(2)]))
    # Ordinary Bellman exactly dominates all fixed tables at small horizons.
    ops=[x[2] for x in triples];plan=p.integer_plan(ops,[s.Rational(1,2)]*2,['1/3','1'],3)
    value=s.Rational(plan['coarse_value']);w=s.Matrix([s.Rational(1,3),1])
    for word in product(list(product(range(3),repeat=2)),repeat=3):
        v=w
        for table in reversed(word):v=s.Matrix([sum(ops[table[g]][g,h]*v[h] for h in range(2)) for g in range(2)])
        ck((v[0]+v[1])/2<=value)
    # Exact obstruction: shared Bernoulli noise yields deviation 1/2 always.
    for N in (1,2,1000,1000000):
        ck(all(abs(F(N*b,N)-F(1,2))==F(1,2) for b in (0,1)))
    # Full product transcripts amplify a local epsilon despite aggregate task.
    for N in (1,2,7,100):
        e=F(1,100);tv=1-(1-e)**N;ck(tv>=e and tv<=N*e)
    # Tiny changes in deterministic mean cross a discontinuous threshold.
    for k in (10,100,10000):ck((F(1,2)-F(1,k)<F(1,2)) and not(F(1,2)+F(1,k)<F(1,2)))
    for N in (10,1000,1000000):
        q=p.concentration(N,24,4,2,s.Rational(1,10**9));ck(s.Rational(q['eta'])**2>=s.Rational(q['log_union_upper'])/(2*N))
    return checks

def run():
    start=time.perf_counter();checks=small();reject=0
    task=copy.deepcopy(p.TASK);out=p.run(task=task,expected_task_digest=p.digest(task));saved=json.loads((ROOT/'population_plan.json').read_text());assert strip(out)==strip(saved);checks+=out['receiving_checks']+1
    dep=p.deploy(out['plan'],task['workers'],seed=7319001);assert strip(dep)==strip(json.loads((ROOT/'population_deployment.json').read_text()));checks+=1
    mc=p.mc_baseline(out['plan']);assert strip(mc)==strip(json.loads((ROOT/'population_mc_baseline.json').read_text()));checks+=1
    assert mc['same_exact_policy_as_tagged_plan'] and mc['passes_60_percent'] and out['status']=='PASS_CONDITIONAL_POPULATION_SERVICE';checks+=1
    for key,val in [('length',True),('length',23),('generators',1),('workers',True),('learning_confidence','1/100'),('deployment_risk',.1),('model_tolerance',True),('reward',[0,1,0,1.0]),('source_task_sha256','x'),('broadcast_interface','microscopic'),('initial_law','correlated')]:
        bad=copy.deepcopy(task);bad[key]=val
        try:p.validate(bad)
        except (AssertionError,TypeError,ValueError):reject+=1
        else:raise AssertionError(('accepted invalid task',key))
    try:p.run(task=task,expected_task_digest='0'*64)
    except AssertionError:reject+=1
    else:raise AssertionError('accepted digest')
    # Threshold substitution binds the query, not an unconditional claim.
    harder=copy.deepcopy(task);harder['minimum_service_fraction']='7/10';refused=p.run(task=harder,expected_task_digest=p.digest(harder));assert refused['status']=='REFUSED_POPULATION_SERVICE';checks+=1
    return {'status':'PASS_AUTHOR_POPULATION_REPLAY','exact_checks':checks,'preflight_refusals':reject,'source_receiving_runs':2,'actual_regenerated_worker_updates':dep['logical_forward_calls_actually_executed']+mc['logical_forward_calls_actually_executed'],'no_new_independent_evidence_from_replay':True,'ordinary_single_goal_baseline_also_passes':True,'baseline_prospective_calls':mc['prospective_calls_with_proposal'],'reusable_prospective_calls':out['prospective_source_calls_to_used_prefix'],'scope':'New unreviewed deterministic/concentration algebra and simulator replay. Sampling ideality/provenance/independence external. Actual 1e-9 failure frequency is not tested.','seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
if __name__=='__main__':
    out=run();(ROOT/'population_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
