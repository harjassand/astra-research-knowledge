"""Exact existing-fixture comparator tests; zero source calls."""
from pathlib import Path
import sys,json,time,itertools,copy,hashlib
import sympy as S
import canonical as K
C=K.C
from check_control import cert_from_exact
ROOT=Path(__file__).resolve().parent

def fixtures():
    parts=[[0,1],[2,3]];Z,W,_=C.partitions(parts,4);P=Z*W;perm=S.zeros(4)
    for i,j in enumerate([0,2,1,3]):perm[i,j]=1
    gamma=S.Rational(9,10);A0=gamma*perm+S.ones(4)/40;A1=gamma*perm+P/10
    E=C.exact_effects([A0,A1],parts,gamma)
    yield 'existing_nonpredictive', [A0,A1],parts,gamma,E
    null=E['H'].T.nullspace()[0];null/=max(abs(v) for v in null)
    weak=gamma*perm+P/20+S.ones(4)/80+S.Matrix([1,-1,0,0])*null.T/1000
    yield 'existing_strict_weak_closure',[A0,weak],parts,gamma,C.exact_effects([A0,weak],parts,gamma)
    g=S.Rational(1,2);A0=perm/2+S.ones(4)/8;A1=A0+S.Matrix([1,-1,0,0])*S.Matrix([[1,0,0,-1]])/10000
    yield 'existing_nonclosed',[A0,A1],parts,g,C.exact_effects([A0,A1],parts,g)
    n=22;parts22=[list(range(11)),list(range(11,22))];A=S.zeros(n)
    probs=[S.Rational(25,27)]+[S.Rational(1,9)]*10+[S.Rational(1,27)]+[S.Rational(4,9)]*10
    for i,p in enumerate(probs):A[i,0]=p;A[i,11]=1-p
    Ap=A.copy()
    for i in range(n):
        d=S.Rational(1 if i<11 else -1,100);Ap[i,0]+=d;Ap[i,11]-=d
    yield 'existing_singular_R',[A,Ap],parts22,gamma,C.exact_effects([A,Ap],parts22,gamma)
    n=6;parts3=[[0,1],[2,3],[4,5]];Z,W,_=C.partitions(parts3,n);perm6=S.zeros(n)
    for i,j in enumerate([0,2,1,4,3,5]):perm6[i,j]=1
    A=perm6/2+S.ones(n)/12;D=S.Matrix([[1,-1,0],[0,1,-1],[-1,0,1]])/24;Ap=A+Z*D*W;g=S.Rational(1,2)
    yield 'existing_rank3_refinement',[A,Ap],parts3,g,C.exact_effects([A,Ap],parts3,g)

def run():
    start=time.perf_counter();checks=0;cases=[];refusals=0;totalpi=0
    def ck(x):
        nonlocal checks
        assert x;checks+=1
    for name,actions,parts,gamma,E in fixtures():
        cert=cert_from_exact(E,gamma,E['eta']);tol='1/100';ch=C.digest(cert);model=K.compile_model(cert,expected_certificate_sha256=ch,expected_tolerance=tol)
        ck(model['status']=='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP');ck(model['new_source_calls']==0);mh=C.digest(model);r=E['H'].cols;m=len(actions)
        goals=[]
        if r==2:
            goals=[[[str(x) for x in vv[:2]],[str(x) for x in vv[2:]]] for vv in itertools.product([0,S.Rational(1,2),1],repeat=4)]
        else:
            goals=[[[str((j+a+k)%3)+'/2' for j in range(r)] for a in range(m)] for k in range(3)]
        for gg in goals:
            gh=C.digest(gg);out=K.plan_model(cert,model,gg,expected_certificate_sha256=ch,expected_model_sha256=mh,expected_goal_sha256=gh,expected_tolerance=tol)
            baseline=C.margin_plan_action_rewards(cert,gg,expected_certificate_sha256=ch,expected_goal_sha256=gh,expected_tolerance=tol)
            ck(out['status']=='PASS_POLICY_REGRET');ck(baseline['status']=='PASS_POLICY_REGRET');ck(out['w']==baseline['w']);ck(out['rho']=='0');ck(S.Rational(out['regret_bound'])==S.Rational(baseline['normalized_pointwise_regret_bound']));totalpi+=out['policy_iteration_evaluations']
        raw=all(A-actions[0]==E['Z']*E['W']*(A-actions[0])*E['Z']*E['W'] for A in actions)
        if name=='existing_strict_weak_closure':ck(not raw and E['eta']==0)
        if name=='existing_singular_R':ck(E['R'].det()==0)
        if raw:
            D=[E['W']*(A-actions[0])*E['Z'] for A in actions];Dm=S.Matrix(r,r,lambda j,k:min(Da[j,k] for Da in D));background=actions[0]+E['Z']*Dm*E['W'];reset=[Da-Dm for Da in D]
            ck(min(background)>=0);ck(max(background*S.ones(background.rows,1))<=1)
            for a in range(m):ck(min(reset[a])>=0);ck(actions[a]==background+E['Z']*reset[a]*E['W'])
            ss=-Dm*S.ones(r,1)
            if min(ss)>0:
                GS=(S.eye(background.rows)-gamma*background).inv();SS=S.diag(*ss);DD=S.diag(*list(S.ones(background.rows,1)-E['Z']*ss));TT=[gamma*SS.inv()*Ra*E['W']*GS*E['Z']*SS for Ra in reset]
                for T in TT:ck(min(T)>=0);ck(max(T*S.ones(r,1))<=gamma)
                for vv in [[S.Rational((j+k)%3,2) for j in range(r)] for k in range(3)]:
                    g=S.Matrix(vv);f=(1-gamma)*E['Z']*g;bb=[(1-gamma)*g+gamma*SS.inv()*Ra*E['W']*GS*DD*f for Ra in reset];pi=[0]*r;seen=set()
                    while True:
                        ck(tuple(pi) not in seen);seen.add(tuple(pi));T=S.Matrix(r,r,lambda i,j:TT[pi[i]][i,j]);b=S.Matrix([bb[pi[i]][i] for i in range(r)]);u=(S.eye(r)-T).inv()*b;scores=[bb[a]+TT[a]*u for a in range(m)];best=S.Matrix([max(v[j] for v in scores) for j in range(r)])
                        if u==best:break
                        for j in range(r):
                            if best[j]>u[j]:pi[j]=max(range(m),key=lambda a:scores[a][j])
                    v=GS*(E['Z']*SS*u+DD*f);ck(v==f+gamma*S.Matrix([max((A*v)[i] for A in actions) for i in range(len(v))]))
        cases.append(dict(name=name,raw_reset_factorization=raw,eta=str(E['eta']),tasks=len(goals),model=model,canonical_equals_observed_block_predictor=all(C.matrix(model['transitions'][a])[:r,:r]==E['W']*actions[a]*E['Z'] for a in range(m))))
    # External certificate/goal/model binding and explicit model tamper refusals.
    def reject(fn):
        nonlocal refusals
        try:fn()
        except (ValueError,AssertionError,TypeError):refusals+=1
        else:raise AssertionError('invalid accepted')
    reject(lambda:K.compile_model(cert,expected_certificate_sha256='bad',expected_tolerance=tol))
    gg=goals[0];reject(lambda:K.plan_model(cert,model,gg,expected_certificate_sha256=ch,expected_model_sha256='bad',expected_goal_sha256=C.digest(gg),expected_tolerance=tol))
    bad=copy.deepcopy(model);bad['transitions'][0][0][0]='9';reject(lambda:K.plan_model(cert,bad,gg,expected_certificate_sha256=ch,expected_model_sha256=C.digest(bad),expected_goal_sha256=C.digest(gg),expected_tolerance=tol))
    return dict(status='PASS_ORDINARY_CANONICAL_MDP_COMPARATOR',checks=checks,refusals=refusals,cases=cases,total_policy_iteration_evaluations=totalpi,new_source_calls=0,seconds=time.perf_counter()-start,scope='Existing algebra fixtures only. Ordinary hidden-K compilation and ordinary stochastic policy iteration get the SAME acquired moments/certificate; no empirical acquisition or practical speedup claim.',source_sha256=hashlib.sha256((ROOT/'canonical.py').read_bytes()).hexdigest())
if __name__=='__main__':
    out=run();(ROOT/'canonical_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
