"""Exact independent schedule/history checks; zero draws and source trials."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,itertools,math

HERE=Path(__file__).resolve().parent;Q=HERE.parent
ceil=lambda z:(z.numerator+z.denominator-1)//z.denominator
def log2ceil_rat(z):
    n=0
    while F(2)**n<z:n+=1
    return n
def sched(d):
    J=0
    while 2**J<4*d*d:J+=1
    return J,[F(1,2**(j+2)) for j in range(J+1)]
dimension_cases=balance_cases=0
for d in range(2,258):
    J,kap=sched(d)
    assert F(1,32*d*d)<kap[-1]<=F(1,16*d*d)
    assert sum(1/k for k in kap)<2/kap[-1]
    # Elementary pi>3 already makes the small-band union strictly <1.
    a=F(1,4*d)
    assert d*4*a/3==F(1,3)<1
    for js in range(J+1):
        for star in ([kap[0]] if js==0 else [kap[js],F(3,2)*kap[js],F(7,4)*kap[js]]):
            if star<F(1,16*d*d):continue
            first=next(j for j,k in enumerate(kap) if k<=star)
            assert first==js and kap[first]>=star/2
            assert sum(1/k for k in kap[:first+1])<4/star
            balance_cases+=1
    dimension_cases+=1

resource_cases=0;max_pre_ratio=F(0)
for d,r,gam,eps in itertools.product([2,6,16,50,128],[1,2],[F(1),F(1,7)],[F(1),F(1,19)]):
    r=min(r,d);J,kap=sched(d)
    bt=eps/(1024*(J+1));b0=eps/(8192*(J+1));bq=eps/512
    L=max(1,log2ceil_rat(64*d/bt));lv=log2ceil_rat(1/b0)
    D=1
    while D<d*r:D*=2
    lb=log2ceil_rat(12*D/bq)
    bills=[];banks=[]
    for k in kap:
        N=ceil(F(2**44*d*L)/(k*gam*eps))
        uD=gam*eps/2**22;uS=k*gam*eps/(3*d*2**24)
        nD=ceil(64*lv/uD);nS=ceil(64*lv/uS)
        assert uS<=uD and nD<=nS
        m=k*gam*eps/2**24;n0=ceil(80*D*lb/m)
        bills.append(N+nD+nS);banks.append(n0)
    for js in range(J+1):
        ratio=F(sum(bills[:js+1]),bills[js]);max_pre_ratio=max(max_pre_ratio,ratio)
        assert ratio<=6
        assert banks[js]<=banks[-1]
        # Uniform deterministic cap covers every early-stop branch and fallback.
        all_stage_cap=sum(bills)+max(banks)
        assert sum(bills[:js+1])+banks[js]<=all_stage_cap
        resource_cases+=1

history_cases=0
for d,eps,gam,star,pattern in itertools.product([2,8,32],[F(1),F(1,31)],
    [F(1),F(1,9)],[F(0),F(1,4)],[0,1,2,3]):
    J,kap=sched(d);b0=eps/(8192*(J+1));bt=eps/(1024*(J+1));bq=eps/512
    reach=F(1);false=valid=F(0)
    for j in range(J+1):
        pf=2*b0 if (j+pattern)%2 else b0
        pv=[F(0),F(1,5),F(2,7),F(1,2)][(j+pattern)%4]
        assert pf+pv<=1
        false+=reach*pf;valid+=reach*pv;reach*=1-pf-pv
    assert reach+false+valid==1
    assert false<=2*(J+1)*b0==eps/4096
    base=(1+gam/2)*star
    risk=reach*(base+eps/512)+false+valid*((1-bq)*(base+eps/1024)+bq)
    assert risk<=base+17*eps/4096
    assert 2*F(17,4096)+F(1,2)<1
    # Worst conditional pilot/test failure at the relevant reached stage.
    fail=bt+2*b0
    assert fail<eps/512
    assert reach*fail<=fail
    nu_pre=eps/1024
    assert fail+nu_pre<3*eps/1024<eps/256
    history_cases+=1

receipt_names=['acquired_anchor_independent_receipt.json','row_residual_validation_independent_receipt.json']
verified={}
for name in receipt_names:
    data=json.loads((HERE/name).read_text())
    for path,digest in data['sha256_relative_to_programme_root'].items():
        assert hashlib.sha256((Q/path).read_bytes()).hexdigest()==digest,path
    verified[name]=len(data['sha256_relative_to_programme_root'])

source='AUTOMATIC_VALIDATED_ROW_FAST_PATH.md';clarification='FAST_PATH_RESOURCE_EVENT_IMPLEMENTATION_CLARIFICATION.md'
out={'status':'PASS independent exact geometric-schedule and adaptive-history composition checks',
 'source_sha256':hashlib.sha256((HERE/source).read_bytes()).hexdigest(),
 'implementation_clarification_sha256':hashlib.sha256((HERE/clarification).read_bytes()).hexdigest(),
 'dimension_cases':dimension_cases,'intrinsic_balance_index_cases':balance_cases,
 'finite_source_cap_cases':resource_cases,'largest_prefix_to_last_stage_bill_ratio':str(max_pre_ratio),
 'exact_adaptive_history_cases':history_cases,'verified_module_binding_counts':verified,
 'source_calls':0,'rng_draws':0,'sampled_trial_outcomes':0,
 'evidence_class':'Exact rational finite schedule, source-cap and adaptive first-accept/fallback arithmetic. No source or aggregate trial simulation, quantum estimation circuit, optimizer or hardware execution.'}
(HERE/'automatic_row_schedule_independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
