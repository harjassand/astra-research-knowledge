"""Direct geometry certificates: exact unit checks, zero new observations."""
from pathlib import Path
import sys,json,copy,time,itertools,hashlib
import sympy as S
import direct as D
C=D.C
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'resolvent_canonical_comparator_20261031'))
import check_canonical as T
ROOT=Path(__file__).resolve().parent

def core(E,gamma,eta=None,B=None):
    return dict(r=E['H'].cols,m=len(E['B']),gamma=str(gamma),eta=str(E['eta'] if eta is None else eta),Bhat=[C.serial(x) for x in (E['B'] if B is None else B)])

def run():
    checks=0;refusals=0;start=time.perf_counter();cases=[]
    def ck(x):
        nonlocal checks
        assert x;checks+=1
    for name,actions,parts,gamma,E in T.fixtures():
        cert=core(E,gamma);ch=C.digest(cert);model=D.compile_model(cert,expected_certificate_sha256=ch,expected_tolerance='1/100');mh=C.digest(model)
        ad=D.verify_uniform(cert,model,expected_certificate_sha256=ch,expected_model_sha256=mh,expected_tolerance='1/100');ck(ad['status']=='PASS_ALL_GOAL_DIRECT_CANONICAL_ADMISSION');ck('hhat' not in cert and 'delta_h' not in cert)
        r=cert['r'];m=cert['m'];goals=[[[str(S.Rational((a+j+k)%3,2)) for j in range(r)] for a in range(m)] for k in range(3)]
        for gg in goals:
            kw=dict(expected_certificate_sha256=ch,expected_model_sha256=mh,expected_goal_sha256=C.digest(gg),expected_tolerance='1/100');p=D.plan_model(cert,model,gg,**kw);q=D.plan_small_lp(cert,model,gg,**kw)
            ck(p['status']==q['status']=='PASS_POLICY_REGRET');ck(p['w']==q['w']);ck(max(S.Rational(x) for x in p['w'])<=S.Rational(ad['weight_bound']));ck(S.Rational(q['regret_bound'])<=S.Rational(ad['normalized_pointwise_regret_bound']))
        cases.append(dict(name=name,model=model))
    # Valid conservative effect bound: old inverse/objective test refuses, direct
    # observed canonical geometry admits. This is exact algebra, NOT acquired data.
    name,actions,parts,gamma,E=next(T.fixtures());cert=core(E,gamma,S.Rational(1,1000));old=T.cert_from_exact(E,gamma,S.Rational(1,1000),0);oldad=C.uniform_admission(old,expected_certificate_sha256=C.digest(old),expected_tolerance='1/20');model=D.compile_model(cert,expected_certificate_sha256=C.digest(cert),expected_tolerance='1/20');ck(oldad['status']=='UNKNOWN_ALL_GOAL_LP_ADMISSION');ck(model['admission']['status']=='PASS_ALL_GOAL_DIRECT_CANONICAL_ADMISSION')
    improvement={'old':oldad,'direct':model['admission'],'scope':'Algebraic valid error bound, not an empirical count acquisition.'}
    # The old source with varying task discount. Verify the explicit p formula
    # and noisy observed-coefficient witness over a rational grid.
    Z,W,_=C.partitions(parts,4);P=Z*W;perm=S.zeros(4)
    for i,j in enumerate([0,2,1,3]):perm[i,j]=1
    A0=S.Rational(9,10)*perm+S.ones(4)/40;A1=S.Rational(9,10)*perm+P/10
    noisy_cases=[];epsilon=S.Rational(1,10)
    for gamma in [S.Rational(9,10),S.Rational(99,100),S.Rational(999,1000),S.Rational(9999,10000)]:
        t=gamma/(1-gamma);E=C.exact_effects([A0,A1],parts,gamma);p=gamma/(20*(1-S.Rational(81,100)*gamma**2));ck(t*E['B'][1]==p*S.Matrix([[1,-1],[-1,1]]));ck(S.Rational(450,3439)<=p<S.Rational(5,19))
        e=epsilon/(21*t)
        for a,b in itertools.product([-1,0,1],repeat=2):
            pp=p+a*2*t*e;qq=p+b*2*t*e;Bh=S.Matrix([[pp,-pp],[-qq,qq]])/t;eta=max(C.row_l1(Ea-Z*Ba) for Ea,Ba in zip(E['C'],[S.zeros(2),Bh]));ck(eta<=6*e)
            X=S.Matrix([[1,-qq/(1-qq)],[-pp/(1-pp),1]]);gap=S.Rational(4,7)
            for Ba in [S.zeros(2),Bh]:
                Y=X*(S.eye(2)-t*Ba).T
                for j in range(2):ck(gap<=sum(Y[:,j])<=Y[j,j]<=1);ck(all(Y[i,j]<=0 for i in range(2) if i!=j))
            ck(2*t*6*e/gap<=epsilon)
            cc=core(E,gamma,6*e,[S.zeros(2),Bh]);cm=D.compile_model(cc,expected_certificate_sha256=C.digest(cc),expected_tolerance=str(epsilon));ck(cm['admission']['status']=='PASS_ALL_GOAL_DIRECT_CANONICAL_ADMISSION');ck(S.Rational(cm['canonical_gap'])>=gap)
            gg=[['1','0'],['0','1']];out=D.plan_small_lp(cc,cm,gg,expected_certificate_sha256=C.digest(cc),expected_model_sha256=C.digest(cm),expected_goal_sha256=C.digest(gg),expected_tolerance=str(epsilon));ck(out['status']=='PASS_POLICY_REGRET')
        noisy_cases.append({'gamma':str(gamma),'endpoint_radius':str(e),'explicit_gap_lower':'4/7','regret_upper':str(21*t*e),'grid_perturbations':9})
    # Check explicit finite-bit schedule WITHOUT generating fake observations.
    schedule_checks=[]
    for rec in noisy_cases:
        gamma=S.Rational(rec['gamma']);e=S.Rational(rec['endpoint_radius']);L=C.ceil_log2(S.Integer(2)**2*4*2/S.Rational(1,100));N=int(S.ceiling(32*L/e**2));bits=max(1,int(S.ceiling(S.log(4/e,2))))
        while S.Rational(1,2**bits)>e/4:bits+=1
        # Integer doubling/bisection finds the paid cap without O(K) trials.
        high=1
        while 2*gamma**(high+1)>e/2:high*=2
        low=0
        while low<high:
            mid=(low+high)//2
            if 2*gamma**(mid+1)<=e/2:high=mid
            else:low=mid+1
        cap=low;rad=C.sqrt_up(S.Rational(2*L,N),bits)+2*gamma**(cap+1);ck(rad<=e)
        schedule_checks.append({'gamma':str(gamma),'N':N,'cap':cap,'root_bits':bits,'episodes':8*N,'source_call_cap':8*N*(cap+1),'scope':'Calculated sufficient schedule only; ZERO episodes executed.'})
    # Real historical observed batch: no regeneration, still UNKNOWN at .01.
    saved=json.loads((ROOT.parent/'resolvent_control_reuse_20261031/episode_protocol_checks.json').read_text());record=saved['record'];design=record['design'];kwargs=dict(expected_native_features=[[1],[1],[0],[0]],expected_n=4,expected_m=2,expected_gamma='9/10',expected_source_id=design['source_id'],expected_schedules=[{k:design[k] for k in ['N','cap','delta','root_bits']}],expected_confidence_total='1/100',expected_tolerance='1/100')
    received=D.receive_refinement_attempts([record],**kwargs);ck(received['status']=='UNKNOWN_REUSABLE_DIRECT_CANONICAL_ACQUISITION');ck(received['total_source_episodes']==4096);ck(received['certificate']==saved['certificate'])
    # An intentionally VACUOUS tolerance only exercises successful stopping and
    # the refusal to hide supplied later paid attempts. Not a useful task success.
    vac=dict(kwargs,expected_tolerance='20');stop=D.receive_refinement_attempts([record],**vac);ck(stop['status']=='PASS_REUSABLE_DIRECT_CANONICAL_ACQUISITION')
    def reject(fn):
        nonlocal refusals
        try:fn()
        except (ValueError,AssertionError,TypeError):refusals+=1
        else:raise AssertionError('invalid accepted')
    reject(lambda:D.receive_refinement_attempts([record,record],**dict(vac,expected_schedules=vac['expected_schedules']*2,expected_confidence_total='1/50')))
    reject(lambda:D.receive_refinement_attempts([record],**dict(kwargs,expected_m=1)))
    reject(lambda:D.receive_refinement_attempts([record],**dict(kwargs,expected_confidence_total='1/1000')))
    reject(lambda:D.compile_model(cert,expected_certificate_sha256='bad',expected_tolerance='1/20'))
    reject(lambda:D.verify_uniform(cert,model,expected_certificate_sha256=C.digest(cert),expected_model_sha256=C.digest(model),expected_tolerance='1/10'))
    for field,value in [('canonical_gap','1'),('r',True)]:
        bad=copy.deepcopy(model);bad[field]=value;reject(lambda bad=bad:D.verify_uniform(cert,bad,expected_certificate_sha256=C.digest(cert),expected_model_sha256=C.digest(bad),expected_tolerance='1/20'))
    bad=copy.deepcopy(model);bad['admission']['normalized_pointwise_regret_bound']='0';reject(lambda:D.verify_uniform(cert,bad,expected_certificate_sha256=C.digest(cert),expected_model_sha256=C.digest(bad),expected_tolerance='1/20'))
    # Non-hidden-K nominal table: refusal is preserved, not all sources admitted.
    impossible={'r':2,'m':2,'gamma':'1/2','eta':'2','Bhat':[[['0','0'],['0','0']],[['3/5','-3/5'],['-3/5','3/5']]]};no=D.compile_model(impossible,expected_certificate_sha256=C.digest(impossible),expected_tolerance='1/10');ck(no['status']!='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP')
    return dict(status='PASS_DIRECT_CANONICAL_ADMISSION_CHECKS',checks=checks,refusals=refusals,old_vs_direct=improvement,noisy_family=noisy_cases,sufficient_schedules=schedule_checks,saved_real_batch_status=received['status'],saved_real_direct_admission=received['model']['admission'],non_hidden_K_refusal=no,new_source_calls=0,existing_models=cases,seconds=time.perf_counter()-start,scope='Exact proof/receiving and calculated schedule checks only; no new observations, and actual saved batch still refuses. Schedule improvement is sufficient-bound comparison, not a lower bound or measured economic speedup.',source_sha256=hashlib.sha256((ROOT/'direct.py').read_bytes()).hexdigest())
if __name__=='__main__':
    out=run();(ROOT/'direct_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['existing_models']},indent=2))
