#!/usr/bin/env python3
"""Exact primary-margin proof checks; reads the saved real protocol without rerunning it."""
from pathlib import Path
import itertools,json,hashlib,copy,time
from math import lcm
import sympy as S
from sympy.solvers.simplex import linprog
import control as C
from check_control import cert_from_exact
ROOT=Path(__file__).resolve().parent

def true_optimum(actions,Z,g,gamma):
    n=Z.rows;A=[];b=[];reward=(1-gamma)*Z*g
    for Aa in actions:
        M=gamma*Aa-S.eye(n)
        A.extend([list(M.row(i)) for i in range(n)]);b.extend([-x for x in reward])
    _,v=linprog(S.ones(1,n)/n,S.Matrix(A),S.Matrix(b),bounds=(None,None));v=S.Matrix(v)
    assert v==reward+gamma*S.Matrix([max((Aa*v)[i] for Aa in actions) for i in range(n)])
    return v

def fabricated_endpoint_record(actions,parts,gamma,delta='1/1000000'):
    E=C.exact_effects(actions,parts,gamma);P=[Aa*E['H'] for Aa in actions]
    D=lcm(*(int(x.q) for Pa in P for x in Pa));N=D*10**24
    design={'n':P[0].rows,'m':len(P),'gamma':str(gamma),'parts':parts,'N':N,'cap':128,'delta':delta,'root_bits':128,'source_id':'fabricated-refinement-unit-counts-NOT-observations'}
    rows=[[[int(x*N) for x in Pa.row(i)] for i in range(Pa.rows)] for Pa in P]
    return {'design':design,'counts':rows}

def run():
    start=time.perf_counter();checks=0
    def ck(x):
        nonlocal checks
        assert x;checks+=1
    parts=[[0,1],[2,3]];Z,W,_=C.partitions(parts,4);J=S.ones(4)/4;P=Z*W;perm=S.zeros(4)
    for i,j in enumerate([0,2,1,3]):perm[i,j]=1
    gamma=S.Rational(9,10);A0=S.Rational(9,10)*perm+J/10;A1=S.Rational(9,10)*perm+P/10;E=C.exact_effects([A0,A1],parts,gamma)
    cert=cert_from_exact(E,gamma);ad=C.uniform_admission(cert,expected_certificate_sha256=C.digest(cert),expected_tolerance='0');ck(ad['status']=='PASS_ALL_GOAL_LP_ADMISSION')
    for goal in [['0','0'],['1','0'],['0','1'],['1/3','2/3'],['1','1']]:
        out=C.margin_plan(cert,goal,expected_certificate_sha256=C.digest(cert),expected_goal_sha256=C.digest(goal),expected_tolerance='0')
        ck(out['status']=='PASS_POLICY_REGRET');ck(S.Rational(out['rho'])==0);ck(min(S.Rational(x) for x in out['dual_group_weights'])>=S.Rational(ad['objective_margin']))
    # Uniform representative-selector checks with nonzero signed effects.
    for p0,p1 in itertools.product([S.Rational(k,4) for k in range(5)],repeat=2):
        M=S.eye(2)-gamma/(1-gamma)*S.diag(p0,p1)*E['B'][1];inv=M.inv()
        ck(C.row_l1(inv)<=1/S.Rational(ad['d']));ck(min(E['h']*inv)>=S.Rational(ad['objective_margin']))
    # Arbitrary positive objective is NOT enough, even with exact effects.
    hb=S.Matrix([[S.Rational(99,100),S.Rational(1,100)]]);goalx=S.Matrix([1,0]);AA=[];bb=[]
    for B in E['B']:
        for j in range(2):AA.append([gamma/(1-gamma)*B[j,k]-int(j==k) for k in range(2)]);bb.append(-gamma/(1-gamma)*(B*goalx)[j])
    _,yb=linprog(hb,S.Matrix(AA),S.Matrix(bb),bounds=(None,None));yb=S.Matrix(yb);wb=goalx+yb
    badrho=max(abs(yb[j]-gamma/(1-gamma)*max((B*wb)[j] for B in E['B'])) for j in range(2));ck(badrho>0)
    # The preconditioned reduced fixed-point iteration can diverge even for an
    # ordinary two-state MDP; the actual LP consumer succeeds.
    E2=C.exact_effects([S.eye(2),S.Matrix([[0,1],[1,0]])],[[0],[1]],gamma);c2=cert_from_exact(E2,gamma);yy=S.zeros(2,1);gg=S.Matrix([1,0]);sizes=[]
    for _ in range(4):yy=gamma/(1-gamma)*S.Matrix([max((B*(gg+yy))[j] for B in E2['B']) for j in range(2)]);sizes.append(C.norminf(yy))
    ck(all(sizes[j+1]>sizes[j] for j in range(3)))
    gglist=['1','0'];p2=C.margin_plan(c2,gglist,expected_certificate_sha256=C.digest(c2),expected_goal_sha256=C.digest(gglist),expected_tolerance='0');ck(p2['status']=='PASS_POLICY_REGRET')
    # Unequal blocks and nonsymmetric effects retain the earned geometry.
    pu=[[0],[1,2],[3,4]];ZU,WU,_=C.partitions(pu,5);Au=S.ones(5)/10+S.eye(5)/2;Du=S.Matrix([[1,-1,0],[0,2,-2],[-1,0,1]])/100;Aup=Au+ZU*Du*WU;gu=S.Rational(3,4)
    Eu=C.exact_effects([Au,Aup],pu,gu);cu=cert_from_exact(Eu,gu);adu=C.uniform_admission(cu,expected_certificate_sha256=C.digest(cu),expected_tolerance='0');ck(Eu['eta']==0)
    for mix in itertools.product([S.Rational(0),S.Rational(1,2),S.Rational(1)],repeat=3):
        M=S.eye(3)-gu/(1-gu)*S.diag(*mix)*Eu['B'][1];inv=M.inv();ck(C.row_l1(inv)<=1/S.Rational(adu['d']));ck(min(Eu['h']*inv)>=S.Rational(adu['objective_margin']))
    # Approximate closure, not exactly closed: micro-dependent action effects
    # average to zero. The chosen baseline policy is actually suboptimal.
    gamma=S.Rational(1,2);A0=perm/2+J/2;delta=S.Rational(1,10000)
    A1=A0+delta*S.Matrix([1,-1,0,0])*S.Matrix([[1,0,0,-1]])
    Ee=C.exact_effects([A0,A1],parts,gamma);eta=Ee['eta'];ck(eta>0);ck(Ee['B'][1]==S.zeros(2))
    approximate=cert_from_exact(Ee,gamma,eta=eta);goal=['1','0'];ad=C.uniform_admission(approximate,expected_certificate_sha256=C.digest(approximate),expected_tolerance='1/100')
    ck(ad['status']=='PASS_ALL_GOAL_LP_ADMISSION');out=C.margin_plan(approximate,goal,expected_certificate_sha256=C.digest(approximate),expected_goal_sha256=C.digest(goal),expected_tolerance='1/100');ck(out['status']=='PASS_POLICY_REGRET')
    g=S.Matrix([1,0]);vo=true_optimum([A0,A1],Z,g,gamma);vb=Ee['H']*g;actual=max(vo-vb)
    ck(actual>0);ck(actual<=S.Rational(out['normalized_pointwise_regret_bound']));ck(out['policy']==[0,0])
    # Directly check all deterministic AND mixed selector inverse and flow bounds.
    q=gamma/(1-gamma)*eta;kappa=(1-gamma)/(1+gamma);d=kappa-q;margin=S.Rational(ad['objective_margin'])
    for p0,p1 in itertools.product([S.Rational(k,4) for k in range(5)],repeat=2):
        Bpi=S.diag(p0,p1)*Ee['B'][1];M=S.eye(2)-gamma/(1-gamma)*Bpi;inv=M.inv();row=Ee['h']*inv
        ck(C.row_l1(inv)<=1/d);ck(min(row)>=margin)
    # Saved real finite observations are received; no new source calls here.
    observed=json.loads((ROOT/'episode_protocol_checks.json').read_text());record=observed['record'];design=record['design']
    route=C.receive_refinement_attempts([record],expected_native_features=[['1'],['1'],['0'],['0']],expected_n=4,expected_m=2,expected_gamma='9/10',expected_source_id=design['source_id'],expected_schedules=[{k:design[k] for k in ('N','cap','delta','root_bits')}],expected_confidence_total='1/100',expected_tolerance='1/100')
    ck(route['status']=='UNKNOWN_REUSABLE_CONTROL_ACQUISITION');ck(route['total_source_episodes']==4096)
    # Full two-round learned refinement receiving, using fabricated UNIT arrays.
    target=[[0,1],[2,3],[4,5]];ZT,WT,_=C.partitions(target,6);perm6=S.zeros(6)
    for i,j in enumerate([0,2,1,4,3,5]):perm6[i,j]=1
    A=perm6/2+S.ones(6)/12;D=S.Matrix([[1,-1,0],[0,1,-1],[-1,0,1]])/24;Ap=A+ZT*D*WT;gam=S.Rational(1,2)
    records=[fabricated_endpoint_record([A,Ap],p,gam) for p in [[[0,1,2,3],[4,5]],target]]
    schedules=[{k:r['design'][k] for k in ('N','cap','delta','root_bits')} for r in records]
    kwargs=dict(expected_native_features=[['0'],['0'],['0'],['0'],['1'],['1']],expected_n=6,expected_m=2,expected_gamma='1/2',expected_source_id=records[0]['design']['source_id'],expected_schedules=schedules,expected_confidence_total='1/1000',expected_tolerance='1/1000000')
    learned=C.receive_refinement_attempts(records,**kwargs);ck(learned['status']=='PASS_REUSABLE_CONTROL_ACQUISITION');ck([x['rank_after'] for x in learned['trace']]==[3,3]);ck(learned['next_partition_proposal']==target)
    for goal in [['1','0','0'],['0','1','0'],['0','0','1'],['1/4','2/3','1/7']]:
        core=learned['certificate'];plan=C.margin_plan(core,goal,expected_certificate_sha256=C.digest(core),expected_goal_sha256=C.digest(goal),expected_tolerance='1/1000000');ck(plan['status']=='PASS_POLICY_REGRET');ck(plan['lp_constraints']==6);ck(S.Rational(plan['rho'])==0)
    # Same acquired core, changing action prices as well as state rewards.
    # Full-state ordinary LP is the equally informed exact truth comparator.
    action_cases=[]
    for table in [[['1','0'],['0','1']],[['1/3','2/3'],['3/4','1/4']],[['0','0'],['1','1']]]:
        ap=C.margin_plan_action_rewards(approximate,table,expected_certificate_sha256=C.digest(approximate),expected_goal_sha256=C.digest(table),expected_tolerance='1/100')
        ck(ap['status']=='PASS_POLICY_REGRET');ck(S.Rational(ap['rho'])==0)
        goals=C.matrix(table);AA=[];bb=[]
        for a,Aa in enumerate([A0,A1]):
            M=gamma*Aa-S.eye(4);AA.extend([list(M.row(i)) for i in range(4)]);bb.extend(list(-(1-gamma)*Z*goals.row(a).T))
        _,vv=linprog(S.ones(1,4)/4,S.Matrix(AA),S.Matrix(bb),bounds=(None,None));vv=S.Matrix(vv)
        pi=ap['policy'];Api=S.zeros(4);rew=S.zeros(4,1)
        for i in range(4):Api[i,:]=[A0,A1][pi[i//2]][i,:];rew[i]=goals[pi[i//2],i//2]
        vp=(1-gamma)*(S.eye(4)-gamma*Api).inv()*rew;reg=max(vv-vp)
        ck(0<=reg<=S.Rational(ap['normalized_pointwise_regret_bound']))
        action_cases.append({'goals':table,'actual_regret':str(reg),'bound':ap['normalized_pointwise_regret_bound']})
    refusals=0
    def reject(fn):
        nonlocal refusals
        try:fn()
        except (TypeError,ValueError,AssertionError):refusals+=1
        else:raise AssertionError('invalid route accepted')
    bad=copy.deepcopy(records);bad[1]['design']['parts']=[[0,2],[1,3],[4,5]];reject(lambda:C.receive_refinement_attempts(bad,**kwargs))
    kk=dict(kwargs,expected_confidence_total='1/10000000');reject(lambda:C.receive_refinement_attempts(records,**kk))
    kk=dict(kwargs,expected_native_features=[['0']]*6);reject(lambda:C.receive_refinement_attempts(records,**kk))
    kk=dict(kwargs,expected_m=1);reject(lambda:C.receive_refinement_attempts(records,**kk))
    reject(lambda:C.margin_plan(approximate,goal,expected_certificate_sha256='bad',expected_goal_sha256=C.digest(goal),expected_tolerance='1'))
    # Objective uncertainty must be paid: a wrong objective with its honest large
    # error cannot pass the positivity-margin admission merely because q is small.
    wrong=copy.deepcopy(approximate);wrong['hhat']=['99/100','1/100'];wrong['delta_h']=str(sum(abs(S.Rational(wrong['hhat'][i])-Ee['h'][i]) for i in range(2)))
    ck(C.uniform_admission(wrong,expected_certificate_sha256=C.digest(wrong),expected_tolerance='1')['status']=='UNKNOWN_ALL_GOAL_LP_ADMISSION')
    return {'status':'PASS_UNIFORM_ACQUIRED_MARGIN_CONTROL_CHECKS','checks':checks,'refusals':refusals,'approximate_nonclosed_case':{'eta':str(eta),'actual_positive_regret':str(actual),'posterior_regret_bound':out['normalized_pointwise_regret_bound'],'uniform_admission':ad},'unprotected_wrong_objective_residual':str(badrho),'divergent_reduced_iteration_sizes':[str(x) for x in sizes],'action_reward_cases':action_cases,'learned_refinement_trace':learned['trace'],'fabricated_refinement_source_episodes_NOT_EXECUTED':learned['total_source_episodes'],'saved_real_observation_route_status':route['status'],'new_source_calls_executed_by_this_harness':0,'scope':'Exact proof/LP/receiving checks; fabricated success arrays are not observations. Saved actual low-budget protocol is honestly refused. No practical or novelty claim.','seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256((ROOT/'control.py').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
if __name__=='__main__':
    out=run();(ROOT/'uniform_control_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
