#!/usr/bin/env python3
"""Exact algebra/receiver fixtures; zero empirical source observations."""
from pathlib import Path
import json,hashlib,time,copy,itertools,random
import sympy as S
import control as C
ROOT=Path(__file__).resolve().parent


def cert_from_exact(E,gamma,eta=0,dh=0,B=None,h=None):
    r=E['H'].cols;B=E['B'] if B is None else B;h=E['h'] if h is None else h
    return {'r':r,'m':len(B),'gamma':str(gamma),'eta':str(eta),'delta_h':str(dh),'Bhat':[C.serial(x) for x in B],'hhat':C.serial(h)[0],'scope':'EXACT ALGEBRA UNIT FIXTURE, not acquired statistical evidence'}

def run():
    start=time.perf_counter();checks=0
    def ck(x):
        nonlocal checks
        assert x;checks+=1
    cases=[]
    parts=[[0,1],[2,3]];Z,W,_=C.partitions(parts,4);P=Z*W;J=S.ones(4)/4;perm=S.zeros(4)
    for i,j in enumerate([0,2,1,3]):perm[i,j]=1
    A0=S.Rational(9,10)*perm+J/10;A1=S.Rational(9,10)*perm+P/10;gamma=S.Rational(9,10)
    E=C.exact_effects([A0,A1],parts,gamma);ck(E['eta']==0);ck(A0*Z!=Z*W*A0*Z);ck(A0.rank()==4)
    native=[[1],[1],[0],[0]];ref=C.exact_refinement([A0,A1],native,gamma);ck(ref['parts']==parts);ck(ref['effects']['eta']==0)
    cert=cert_from_exact(E,gamma)
    for g in [[str(S.Rational(j,5)),str(S.Rational(k,5))] for j,k in itertools.product(range(6),repeat=2)]:
        out=C.robust_plan(cert,g,expected_certificate_sha256=C.digest(cert),expected_goal_sha256=C.digest(g),expected_tolerance='0')
        ck(out['status']=='PASS_POLICY_REGRET');ck(out['exact_primal_dual_verified']);ck(S.Rational(out['rho'])==0)
        y=S.Matrix([S.Rational(x) for x in out['y']]);v=E['H']*(S.Matrix([S.Rational(x) for x in g])+y)
        values=[A*v for A in [A0,A1]];Tv=(1-gamma)*Z*S.Matrix([S.Rational(x) for x in g])+gamma*S.Matrix([max(vv[i] for vv in values) for i in range(4)])
        ck(v==Tv)
    cases.append({'case':'nonpredictive_fullrank_baseline','rank':2,'ambient_n':4,'tasks':36,'zero_exact_regret':True})
    # Strictly weaker than raw difference factorization: invisible action changes
    # annihilate H while varying inside the acquired blocks.
    base1=S.Rational(9,10)*perm+P/20+J/20
    null=E['H'].T.nullspace()[0];null=null/max(abs(x) for x in null)
    bump=S.Matrix([1,-1,0,0])*null.T/1000;weak1=base1+bump
    ck(min(weak1)>=0 and weak1*S.ones(4,1)==S.ones(4,1))
    weak=C.exact_effects([A0,weak1],parts,gamma);ck(weak['eta']==0);ck((weak1-A0)!=(P*(weak1-A0)*P))
    cases.append({'case':'effect_closure_without_raw_factorization','closure_error':'0','raw_factorization':False})
    # Parent-supplied exact singular-R construction; no inversion of R.
    n=22;parts22=[list(range(11)),list(range(11,22))];A=S.zeros(n)
    probs=[S.Rational(25,27)]+[S.Rational(1,9)]*10+[S.Rational(1,27)]+[S.Rational(4,9)]*10
    for i,p in enumerate(probs):A[i,0]=p;A[i,11]=1-p
    Aplus=A.copy()
    for i in range(n):
        d=S.Rational(1 if i<11 else -1,100);Aplus[i,0]+=d;Aplus[i,11]-=d
    E22=C.exact_effects([A,Aplus],parts22,gamma);ck(E22['eta']==0);ck(E22['H'].rank()==2);ck(E22['R'].det()==0)
    ck(E22['R']==S.Matrix([[S.Rational(1,3),S.Rational(2,3)]]*2))
    cert22=cert_from_exact(E22,gamma);g=['1','0'];o=C.robust_plan(cert22,g,expected_certificate_sha256=C.digest(cert22),expected_goal_sha256=C.digest(g),expected_tolerance='0');ck(o['status']=='PASS_POLICY_REGRET')
    cases.append({'case':'singular_R','R':C.serial(E22['R']),'H_rank':2,'rho':o['rho']})
    # Tiny rational coefficient errors: exact robust LP success and posterior bound.
    theta=S.Rational(1,10**7);Bn=[x.copy() for x in E['B']];Bn[1]+=theta*S.Matrix([[1,-1],[-1,1]])
    hn=E['h']+theta*S.Matrix([[1,-1]]);eta=2*theta;dh=2*theta;noisy=cert_from_exact(E,gamma,eta,dh,Bn,hn)
    ck(max(C.row_l1(Ea-E['Z']*Ba) for Ea,Ba in zip(E['C'],Bn))<=eta)
    for g in [['1','0'],['0','1'],['1/3','2/3'],['1','1']]:
        out=C.robust_plan(noisy,g,expected_certificate_sha256=C.digest(noisy),expected_goal_sha256=C.digest(g),expected_tolerance='1/100')
        ck(out['status']=='PASS_POLICY_REGRET');ck(S.Rational(out['normalized_pointwise_regret_bound'])<=S.Rational(out['a_priori_exact_closure_bound']))
        y=S.Matrix([S.Rational(x) for x in out['y']]);gg=S.Matrix([S.Rational(x) for x in g]);v=E['H']*(gg+y);pi=out['policy'];Ap=S.zeros(4)
        for i in range(4):Ap[i,:]=[A0,A1][pi[i//2]][i,:]
        vp=(1-gamma)*(S.eye(4)-gamma*Ap).inv()*Z*gg
        exact=C.robust_plan(cert,g,expected_certificate_sha256=C.digest(cert),expected_goal_sha256=C.digest(g),expected_tolerance='0');vo=E['H']*(gg+S.Matrix([S.Rational(x) for x in exact['y']]))
        ck(max(vo-vp)<=S.Rational(out['normalized_pointwise_regret_bound']));ck(min(v-vo)>=0)
        cases.append({'case':'noisy_coefficients','g':g,'regret_bound':out['normalized_pointwise_regret_bound'],'a_priori_bound':out['a_priori_exact_closure_bound'],'actual_regret':str(max(vo-vp))})
    # Acquisition refinement does not start with the useful partition: native
    # reward has two levels; action effects split the first level into two.
    n=6;target=[[0,1],[2,3],[4,5]];ZT,WT,_=C.partitions(target,n);perm6=S.zeros(n)
    for i,j in enumerate([0,2,1,4,3,5]):perm6[i,j]=1
    A=S.Rational(1,2)*perm6+S.ones(n)/12;D=S.Matrix([[1,-1,0],[0,1,-1],[-1,0,1]])/24;Ap=A+ZT*D*WT
    refined=C.exact_refinement([A,Ap],[[0],[0],[0],[0],[1],[1]],S.Rational(1,2))
    ck(refined['parts']==target);ck([x['rank_after'] for x in refined['rounds']]==[3,3]);ck(refined['effects']['eta']==0)
    cases.append({'case':'acquired_refinement_from_native_rewards','rounds':refined['rounds'],'final_rank':3})
    # A noisy chain merges distinct profiles: no unjustified exact clustering.
    effects=[S.zeros(3,2),S.Matrix([[0,0],[S.Rational(3,10),-S.Rational(3,10)],[S.Rational(6,10),-S.Rational(6,10)]])]
    chain=C.statistical_refinement([[0,1,2]],effects,S.Rational(1,5));ck(chain['parts']==[[0,1,2]])
    # Fabricated integer endpoint counts exercise receiving; NOT observations.
    design={'n':4,'m':2,'gamma':'1/2','parts':parts,'N':10**12,'cap':64,'delta':'1/100','root_bits':80,'source_id':'fabricated-unit-fixture-not-an-observation-source'}
    rows=[[[700000000000,300000000000],[600000000000,400000000000],[200000000000,800000000000],[300000000000,700000000000]],[[750000000000,250000000000],[650000000000,350000000000],[150000000000,850000000000],[250000000000,750000000000]]]
    rec={'design':design,'counts':rows};acq=C.receive_counts(rec,expected_design=design);ck(S.Rational(acq['eta_hat'])==0);ck(acq['source_episodes']==8*10**12)
    g=['1','0'];planned=C.robust_plan(acq,g,expected_certificate_sha256=C.digest(acq),expected_goal_sha256=C.digest(g),expected_tolerance='1/100');ck(planned['status']=='PASS_POLICY_REGRET');ck(planned['exact_primal_dual_verified'])
    cases.append({'case':'fabricated_count_frontend','status':planned['status'],'regret_bound':planned['normalized_pointwise_regret_bound'],'claimed_observations_executed':0})
    rejects=0
    def reject(fn):
        nonlocal rejects
        try:fn()
        except (TypeError,ValueError,AssertionError):rejects+=1
        else:raise AssertionError('bad input accepted')
    for x in [True,0.5,S.Float('.5')]:reject(lambda x=x:C.rational(x))
    bad=copy.deepcopy(rec);bad['design']['n']=True;reject(lambda:C.receive_counts(bad,expected_design=design))
    bad=copy.deepcopy(rec);bad['counts'][0][0][0]=True;reject(lambda:C.receive_counts(bad,expected_design=design))
    for field,value in [('gamma','2/3'),('delta','1/10'),('m',1),('cap',63),('N',10**12-1)]:
        dd=copy.deepcopy(design);dd[field]=value;reject(lambda dd=dd:C.receive_counts(rec,expected_design=dd))
    reject(lambda:C.robust_plan(acq,g,expected_certificate_sha256='bad',expected_goal_sha256=C.digest(g),expected_tolerance='1'))
    reject(lambda:C.robust_plan(acq,g,expected_certificate_sha256=C.digest(acq),expected_goal_sha256='bad',expected_tolerance='1'))
    reject(lambda:C.robust_plan(acq,['2','0'],expected_certificate_sha256=C.digest(acq),expected_goal_sha256=C.digest(['2','0']),expected_tolerance='1'))
    return {'status':'PASS_EXACT_RESOLVENT_CONTROL_CHECKS','checks':checks,'refusals':rejects,'cases':cases,'new_source_observations_executed':0,'scope':'Exact algebra and fabricated-count receiving fixtures, not an empirical acquisition/performance experiment. Rational simplex has actual charged runtime, not a polynomial worst-case guarantee.','seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256((ROOT/'control.py').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
if __name__=='__main__':
    out=run();(ROOT/'control_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
