"""Exact mathematical and receiving tests; seeded paths are protocol fixtures only.

run() returns results without writing. --generate writes a new observation fixture
and test JSON and refuses overwrite. replay_saved() makes zero source calls.
"""
from pathlib import Path
from copy import deepcopy
from math import lcm,comb
import random,json,gzip,hashlib,sys,time
import sympy as S
import clock_response as R
import ordinary_coupled_geometric as O
C=R.C;D=R.D
ROOT=Path(__file__).resolve().parent


class RationalSource:
    def __init__(self,actions,seed):
        self.actions=actions;self.rng=random.Random(seed);self.calls=0;self.rows={}
        for a,A in enumerate(actions):
            for i in range(A.rows):
                den=lcm(*[int(v.q) for v in A.row(i)]);weights=[int(v*den) for v in A.row(i)]
                assert sum(weights)==den and min(weights)>=0;self.rows[i,a]=(den,weights)
    def step(self,i,a):
        den,weights=self.rows[i,a];u=self.rng.randrange(den);self.calls+=1
        for j,w in enumerate(weights):
            if u<w:return j
            u-=w
        raise AssertionError('sampler')


def paired_exact(A0,Aa,i,Z,gamma,K):
    n=A0.rows;r=Z.cols;p={(x,y):Aa[i,x]*A0[i,y] for x in range(n) for y in range(n)};mean=S.zeros(1,r)
    for s in range(K):
        for (x,y),w in p.items():mean+=gamma**(s+1)*w*(Z.row(x)-Z.row(y))
        new={(x,y):S.Integer(0) for x in range(n) for y in range(n)}
        for (x,y),w in p.items():
            if x==y:
                for z in range(n):new[z,z]+=w*A0[x,z]
            else:
                for u in range(n):
                    for v in range(n):new[u,v]+=w*A0[x,u]*A0[y,v]
        p=new
    return mean,sum(w for (x,y),w in p.items() if x!=y)


def fixture():
    A0=S.Matrix([[S.Rational(1,2),S.Rational(1,2),0,0],[S.Rational(1,2),S.Rational(1,2),0,0],[0,0,S.Rational(1,2),S.Rational(1,2)],[0,0,S.Rational(1,2),S.Rational(1,2)]])
    A1=S.Matrix([[1,0,0,0],[1,0,0,0],[0,0,1,0],[0,0,1,0]])
    return [A0,A1],[[0,2],[1,3]]


def run():
    checks=0;refusals=0;source_calls=0;start=time.perf_counter()
    def check(x):
        nonlocal checks
        assert x;checks+=1
    rng=random.Random(20261031)
    # General nonsymmetric kernels, exact finite-state distributions, not source observations.
    for n in (2,3,4):
        for trial in range(3):
            mats=[]
            for a in range(3):
                rows=[]
                for i in range(n):
                    weights=[rng.randint(0,5) for _ in range(n)]
                    if not sum(weights):weights[0]=1
                    rows.append([S.Rational(w,sum(weights)) for w in weights])
                mats.append(S.Matrix(rows))
            parts=[[i] for i in range(n)] if trial%2 else [list(range(n-1)),[n-1]]
            Z,W,_=C.partitions(parts,n);gamma=S.Rational(9,10)
            U=[gamma*(A-mats[0])*(S.eye(n)-gamma*mats[0]).inv()*Z for A in mats]
            for a in (1,2):
                for i in range(n):
                    for K in (0,1,2,4):
                        mean,p=paired_exact(mats[0],mats[a],i,Z,gamma,K)
                        check(C.row_l1(U[a][i,:]-mean)<=2*gamma**(K+1)*p/(1-gamma))
                        check(sum(mean)==0 and 0<=p<=1)
    # Exact Bernoulli finite-law coverage of the implemented upper bound.
    for N in range(2,18):
        for num in range(11):
            p=S.Rational(num,10);bad=S.Integer(0)
            for k in range(N+1):
                upper,_=R.tail_upper(k,N,1,S.Rational(1,10),32)
                if upper<p:bad+=comb(N,k)*p**k*(1-p)**(N-k)
            check(bad<=S.Rational(1,10))
    # Exact perturbed witness neighborhood: source matrices, not observed arrays.
    for trial in range(5):
        r=3;gamma=S.Rational(9,10);delta0=1-gamma;mats=[]
        for a in range(3):
            rows=[]
            for i in range(r):
                ww=[rng.randint(1,5) for _ in range(r)];rows.append([S.Rational(v,sum(ww)) for v in ww])
            mats.append(S.Matrix(rows))
        G=(S.eye(r)-gamma*mats[0]).inv();UU=[gamma*(A-mats[0])*G for A in mats]
        X0=(S.eye(r)-gamma*mats[0]).T;lam=delta0/(2*(1+delta0));X1=(1-lam)*X0-lam*S.ones(r)/r;J=max(abs(v) for v in X1)
        e=min(lam/(2*r*J),delta0/(4*r*J),1/J)/2
        pert=[UU[0]]+[U+e*S.Matrix([[1,-1,0],[0,1,-1],[-1,0,1]])/2 for U in UU[1:]]
        Ahat=S.Matrix.hstack(*[(S.eye(r)-U).T for U in pert]);YY=X1*Ahat
        check(all(YY[i,a*r+j]<=0 for a in range(3) for j in range(r) for i in range(r) if i!=j))
        check(min(sum(YY[:,k]) for k in range(3*r))>=delta0/4)
        scaled=X1/(1+J*e);ys=scaled*Ahat;gap=delta0/(4*(1+J*e))
        check(gap>=delta0/8 and max(ys[j,a*r+j] for a in range(3) for j in range(r))<=1)
        check(max(scaled[i,i] for i in range(r))/gap<=4/delta0)
    # Block equality is NOT a valid coalescence rule.
    A0=S.Matrix([[1,0,0],[0,0,1],[0,0,1]]);A1=A0.copy();A1[0,:]=S.Matrix([[0,1,0]])
    Z,W,_=C.partitions([[0,1],[2]],3);g=S.Rational(9,10)
    U=g*(A1-A0)*(S.eye(3)-g*A0).inv()*Z
    check(Z.row(0)==Z.row(1) and U.row(0)!=S.zeros(1,2))
    check(C.row_l1(U.row(0))==S.Rational(81,5))
    # Reducible baseline: pair-specific clocks can still decay, no global unique law.
    mats,parts=fixture();Z,W,_=C.partitions(parts,4)
    check((S.eye(4)-mats[0]).rank()==2)
    for K in range(6):
        for i in range(4):
            mu,p=paired_exact(mats[0],mats[1],i,Z,g,K)
            check(p==S.Rational(1,2)**(K+1))
    # Ordinary geometric estimator's actual variance grows although pair clock is fast.
    for gamma in (S.Rational(1,2),S.Rational(9,10),S.Rational(99,100)):
        q=(1-gamma)/(2-gamma);t=gamma/(1-gamma);var=t*t*q-gamma*gamma/4
        check(0<=var<=gamma*gamma/(1-gamma))
        expected_calls=2+2*gamma/(2-gamma);check(2<=expected_calls<=4)
    # Exact geometric endpoint moments from the nonmeeting pair chain.
    pairs=[(x,y) for x in range(4) for y in range(4) if x!=y]
    Q=S.Matrix(len(pairs),len(pairs),lambda k,l:mats[0][pairs[k][0],pairs[l][0]]*mats[0][pairs[k][1],pairs[l][1]])
    pinit=S.Matrix([[mats[1][0,x]*mats[0][0,y] for x,y in pairs]])
    dd=S.Matrix([Z[x,0]-Z[y,0] for x,y in pairs]);dd2=dd.applyfunc(lambda x:x*x)
    for gamma in (S.Rational(1,2),S.Rational(9,10),S.Rational(99,100)):
        inv=(S.eye(len(pairs))-gamma*Q).inv();t=gamma/(1-gamma)
        mean=(t*(1-gamma)*pinit*inv*dd)[0];moment=(t*t*(1-gamma)*pinit*inv*dd2)[0]
        check(mean==gamma/2);check(moment-mean*mean==t*t*(1-gamma)/(2-gamma)-gamma*gamma/4)
    # Lower bound and static canonical/physical-clock separation, exact arithmetic.
    for eps in (S.Rational(1,16),S.Rational(1,32),S.Rational(1,100)):
        for gamma in (S.Rational(1,2),S.Rational(9,10),S.Rational(99,100)):
            p=8*eps*(1-gamma)/gamma;c=gamma*p/(1-gamma);check(0<p<=1 and c<=S.Rational(1,2))
            Vopt=8*eps/(1+8*eps);Vhalf=5*eps/(1+4*eps)
            check(Vopt-Vhalf==eps*(3-8*eps)/((1+8*eps)*(1+4*eps)) and Vopt-Vhalf>eps)
            M=S.Matrix([[1+c,-c],[0,1]]);X=S.eye(2)/(1+c);Y=X*M.T;gap=1/(1+c)
            check(gap>=S.Rational(2,3) and all(sum(Y[:,j])>=gap and Y[j,j]<=1 for j in range(2)))
    # One actual retained trajectory bank, extension reuses paid path prefixes.
    source=RationalSource(mats,31337);bank=R.Bank(source,source_id='two_closed_components_exact_rational_fixture',n=4,m=2)
    bank.ensure(4,0);old_calls=bank.calls;bank.ensure(4,0);check(bank.calls==old_calls)
    bank.ensure(4,3);bank.ensure(8,1)
    des=R.design(source_id=bank.source_id,n=4,m=2,gamma='9/10',parts=parts,i=2,j=2,delta_total='1/100',root_bits=40)
    record=bank.record(des);out=R.receive(record,expected_design=des);check(out['retained_source_calls']==source.calls==bank.calls)
    check(R.initial_partition([[0],[1],[0],[1]])==parts)
    refinement=R.refine_received(record,expected_design=des);check(refinement['parts']==parts and refinement['requires_fresh_prefix_validation_for_changed_partition'])
    olddes=R.design(source_id=bank.source_id,n=4,m=2,gamma='9/10',parts=parts,i=2,j=0,delta_total='1/100',root_bits=40)
    oldrecord=bank.record(olddes);oldout=R.receive(oldrecord,expected_design=olddes);check(oldout['prefix_terms_replayed']==0)
    source_calls+=source.calls
    # All counts/paths/task bindings are replayed, including bool aliases.
    mutations=[]
    for key,value in [('source_id','wrong'),('n',5),('m',3),('gamma','99/100'),('delta_total','1/10'),('root_bits',39),('N',True),('K',False)]:
        rr=deepcopy(record);rr['design'][key]=value;mutations.append(rr)
    rr=deepcopy(record);rr['source_calls']+=1;mutations.append(rr)
    rr=deepcopy(record);rr['rows']=rr['rows'][:-1];mutations.append(rr)
    rr=deepcopy(record);rr['rows'][0]['trials'][0]['x'][0]=True;mutations.append(rr)
    rr=deepcopy(record);rr['rows'][0]['trials'][0]={'x':[0,0],'y':[0,0]};mutations.append(rr)
    rr=deepcopy(record);rr['rows'][0]['action']=0;mutations.append(rr)
    rr=deepcopy(record);rr['attempts'][0]['cumulative_source_calls']+=1;mutations.append(rr)
    for rr in mutations:
        try:R.receive(rr,expected_design=des)
        except (ValueError,TypeError,KeyError,IndexError):refusals+=1
        else:raise AssertionError('tampering accepted')
    # A nominal coefficient/error unit fixture checks the downstream join only.
    gamma=S.Rational(9,10);Utrue=gamma*(mats[1]-mats[0])*(S.eye(4)-gamma*mats[0]).inv()*Z
    check(Utrue==Z*(W*Utrue));etaU=S.Rational(1,10000);t=gamma/(1-gamma)
    core=dict(r=2,m=2,gamma=str(gamma),eta=str(etaU/t),Bhat=[C.serial(S.zeros(2)),C.serial(W*Utrue/t)])
    model=D.compile_model(core,expected_certificate_sha256=C.digest(core),expected_tolerance='1/100')
    check(model['status']=='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP')
    check(C.rational(model['admission']['normalized_pointwise_regret_bound'])==2*etaU*C.rational(model['admission']['weight_bound']))
    goals=[['1/3','1/4'],['1/5','4/5']]
    plan=D.plan_small_lp(core,model,goals,expected_certificate_sha256=C.digest(core),expected_model_sha256=C.digest(model),expected_goal_sha256=C.digest(goals),expected_tolerance='1/100')
    check(plan['status']=='PASS_POLICY_REGRET')
    # A complete small failed search, paid and retained, not fabricated success.
    search_source=RationalSource(mats,991)
    search=R.retained_search(search_source,source_id='small_failed_clock_search',n=4,m=2,gamma='9/10',parts=parts,delta_total='1/100',D_max=3,tolerance='1/100',root_bits=40)
    check(search['status']=='UNKNOWN_SEARCH_BUDGET');check(len(search['attempts'])==6);check(search['source_calls']==search_source.calls)
    check(sum(a['new_source_calls'] for a in search['record']['attempts'])==search_source.calls)
    source_calls+=search_source.calls
    return dict(status='PASS',checks=checks,refusals=refusals,actual_source_calls_in_this_test_run=source_calls,failed_search=dict(status=search['status'],attempts=len(search['attempts']),source_calls=search_source.calls,last_eta_U=search['received']['eta_U']),unit_canonical_join=dict(status=plan['status'],regret=plan['regret_bound'],not_an_observation_based_success=True),seconds=time.perf_counter()-start)


def generate_observations():
    paths=ROOT/'observed_paired_paths.json.gz';result=ROOT/'observed_response.json'
    if paths.exists() or result.exists():raise FileExistsError('preserve previous observation artifacts')
    mats,parts=fixture();source=RationalSource(mats,2026103123);bank=R.Bank(source,source_id='two_closed_components_observation_fixture_v1',n=4,m=2)
    # This complete cap/sample design was fixed before these seeded observations.
    d=R.design(source_id=bank.source_id,n=4,m=2,gamma='9/10',parts=parts,i=7,j=4,delta_total='1/100',root_bits=48)
    bank.ensure(d['N'],d['K']);record=bank.record(d);received=R.receive(record,expected_design=d)
    core=received['core'];model=D.compile_model(core,expected_certificate_sha256=C.digest(core),expected_tolerance='1/100')
    raw=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
    with paths.open('xb') as f:f.write(gzip.compress(raw,mtime=0))
    saved=dict(design=d,record_sha256=C.digest(record),received=received,canonical_model=model,scope='Actual seeded protocol observations, no authenticated physical iid claim. Small-regret admission is UNKNOWN. Replays of this seed are not additional independent evidence.')
    result.write_text(json.dumps(saved,indent=2)+'\n')
    return dict(source_calls=source.calls,paths_bytes=paths.stat().st_size,status=model.get('admission',{}).get('status'),eta_U=received['eta_U'])


def replay_saved():
    saved=json.loads((ROOT/('observed_response_v2.json' if (ROOT/'observed_response_v2.json').exists() else 'observed_response.json')).read_text());record=json.loads(gzip.decompress((ROOT/'observed_paired_paths.json.gz').read_bytes()))
    assert C.digest(record)==saved['record_sha256'];out=R.receive(record,expected_design=saved['design']);assert out==saved['received']
    model=saved['canonical_model'];core=out['core']
    result=D.verify_uniform(core,model,expected_certificate_sha256=C.digest(core),expected_model_sha256=C.digest(model),expected_tolerance='1/100')
    return dict(status='PASS_SAVED_REPLAY',new_source_calls=0,retained_source_calls=out['retained_source_calls'],eta_U=out['eta_U'],received_admission=result)


if __name__=='__main__':
    if '--generate' in sys.argv:
        generated=generate_observations();result=run();target=ROOT/'clock_checks.json'
        if target.exists():raise FileExistsError('preserve test result')
        target.write_text(json.dumps(dict(test=result,observations=generated,saved_replay=replay_saved()),indent=2)+'\n');print(target.read_text())
    elif '--replay-saved' in sys.argv:print(json.dumps(replay_saved(),indent=2))
    else:print(json.dumps(run(),indent=2))
