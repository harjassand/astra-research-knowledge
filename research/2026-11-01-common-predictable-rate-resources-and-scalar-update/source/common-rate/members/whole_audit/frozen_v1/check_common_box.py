"""Author exact controls. Not an independent audit or physical calibration."""
from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
from itertools import product
import json,hashlib
import common_box as C
root=Path(__file__).resolve().parent
raw=C.fixture();p=C.construct(raw);counts={}
assert p['independent_sets_enumerated']==0
C.receive(raw,p)
C.receive_wire(raw,C.canonical_bytes(p))
try:C.receive_wire(raw,C.canonical_bytes(p),max_bytes=1)
except C.BudgetRefusal:pass
else:raise AssertionError('wire byte budget ignored')
mutations=0
for key in ['zeta','mu_hi','Nstar','CF_prefactor']:
    bad=deepcopy(p)
    if key=='mu_hi':bad['raw'][key]+=1
    else:bad[key]+=1
    try:C.receive(raw,bad)
    except C.Unsupported:mutations+=1
    else:raise AssertionError('mutated receipt admitted')
counts['certificate_mutations_rejected']=mutations
# Model actions: invalid requests retain all previously earned positive rates.
guard=C.RateGuard(raw);reject=0;admit=0
for action in [tuple(lo for _,_,lo,hi in p['raw']['channels']),tuple(hi for _,_,lo,hi in p['raw']['channels'])]:
    assert guard.select(action)['status']=='ADMIT_MODEL_RATES';admit+=1
before=guard.active
for action in [[0]*len(before),list(before[:-1]),[float(k) for k in before],[True]*len(before),[-1]*len(before)]:
    assert guard.select(action)['status']=='REJECT_KEEP_PREVIOUS' and guard.active==before;reject+=1
# History-dependent action requests: entirely determined by a finite retained record.
record=[]
for i,x in enumerate([(0,17,0,0,0,0),(1,17,0,0,2,0),(0,0,8,9,0,0),(2,1,0,0,1,0)]):
    action=tuple((hi if (j+len(record)+sum(x))%2 else lo) for j,(_,_,lo,hi) in enumerate(p['raw']['channels']))
    assert guard.select(action)['status']=='ADMIT_MODEL_RATES';admit+=1
    intens=guard.intensities(x)
    for actual,(u,v,lo,hi) in zip(intens,p['raw']['channels']):
        prop=C.propensity(u,x);assert lo*prop<=actual<=hi*prop
    record.append((x,C.digest(action)))
counts.update(admitted_actions=admit,rejected_actions_keep_previous=reject,history_selected_intensity_checks=4*len(before))
# Tiny raw graph, enumerate all box corners to check the linear endpoint receiver.
z=lambda *ix:tuple(ix.count(i) for i in range(3))
small=[(z(),z(0),F(1),F(2)),(z(0),z(),F(1),F(3))]
for active in [z(0,0),z(0,1),z(0,2)]:
    small.extend([(active,z(1,2),F(1),F(2)),(z(1,2),active,F(1),F(2))])
ps=C.construct(small);corner_checks=0
# Use a simple exact test function for this algebraic maximizer control; full
# actual common multiplier is tested separately beyond the acquired finite head.
for x in [(0,4,0),(1,4,0),(0,2,2),(3,1,0)]:
    fn=lambda y:F(1)+F(y[0],sum(y)+1)
    mx,wit=C.worst_scaled_drift(ps,x,fn);brute=[]
    for bits in product([0,1],repeat=len(ps['raw']['channels'])):
        val=F(0)
        for bit,(u,v,lo,hi) in zip(bits,ps['raw']['channels']):
            prop=C.propensity(u,x)
            if prop:
                y=tuple(a-b+c for a,b,c in zip(x,u,v));val+=(hi if bit else lo)*prop*(ps['t']**(sum(v)-sum(u))*fn(y)-fn(x))
        brute.append(val);corner_checks+=1
    assert mx==max(brute)
counts['explicit_corner_comparisons']=corner_checks
# Actual integer budget receiving: no profile or final power is evaluated.
budgets=[]
for N0,T,alpha in [(10,F(1),F(1,100)),(10,F(2**(2*p['Nstar'].bit_length()+20)),F(1,100)),(0,F(0),F(1,3)),(2**1500,F(7,3),F(1,2**200))]:
    b=C.resource_budget(p,N0,T,alpha);fr=b['foster_receipt']
    assert fr['bernoulli_block']*p['eps']>=1
    assert F(1<<fr['dyadic_bits'])>=fr['ratio']
    assert b['foster_count_level']==fr['common_exponent_base']+fr['bernoulli_block']*fr['dyadic_bits']
    assert b['count_level']==min(b['foster_count_level'],b['immigration_count_level'])
    for rr in [b['arrival_receipt'],b['firing_receipt']]:
        assert rr['mean_ceiling']>=rr['mean'] and F(1<<rr['dyadic_confidence_bits'])*rr['failure']>=1
        assert rr['threshold']==2*rr['mean_ceiling']+rr['dyadic_confidence_bits']
    budgets.append(b)
counts['received_integer_resource_budgets']=len(budgets)
# Deterministic legal-path mass accounting: only actual immigration marks are
# exposed to the hypothetical resource client. This is NOT a stability simulation.
x=(1,3,0,2,0,0);initial_upper=9;arrivals=0
for step in range(500):
    enabled=[(u,v) for u,v,lo,hi in p['raw']['channels'] if C.propensity(u,x)]
    u,v=enabled[(step*7)%len(enabled)]
    if sum(u)==0:arrivals+=1
    x=tuple(a-b+c for a,b,c in zip(x,u,v))
    assert sum(x)<=initial_upper+arrivals
zero=(0,)*p['raw']['m'];port=next((u,v) for u,v,lo,hi in p['raw']['channels'] if sum(u)==0)
after_unreceived_arrival=tuple(a-b+c for a,b,c in zip(zero,*port));stale_bound=0
assert sum(after_unreceived_arrival)>stale_bound
counts['legal_path_injection_only_upper_bound_checks']=500
counts['missed_arrival_ground_truth_counterexample']=1
for b in budgets:C.receive_resource_budget(raw,b)
ledger=C.RiskLedger(F(1,10))
for j in range(16):assert ledger.reserve(F(1,160))['status']=='ADMIT_EPISODE_RISK'
spent=ledger.spent
for bad in [F(1,160),0,-1,0.001,True]:
    assert ledger.reserve(bad)['status']=='REJECT_NO_ALLOCATION' and ledger.spent==spent
assert sum(ledger.allocations)==ledger.total
counts['episode_risk_allocations']=16;counts['risk_overspend_or_invalid_rejections']=5
# Find the FIRST dyadic horizon at which common Foster beats the ordinary cap.
lo=0;hi=2*p['Nstar'].bit_length()+20
while lo<hi:
    mid=(lo+hi)//2;b=C.resource_budget(p,10,F(1<<mid),F(1,100))
    if b['selected_count_cap']=='COMMON_FOSTER_LOG_HORIZON':hi=mid
    else:lo=mid+1
cross_exp=lo
prev=C.resource_budget(p,10,F(1<<(cross_exp-1)),F(1,100));curr=C.resource_budget(p,10,F(1<<cross_exp),F(1,100))
assert prev['selected_count_cap']=='ORDINARY_IMMIGRATION_POISSON' and curr['selected_count_cap']=='COMMON_FOSTER_LOG_HORIZON'
# Unsupported model changes, zero lower bounds and floats are not admitted.
invalid=0
for mode in range(5):
    bad=list(raw)
    u,v,l,h=bad[mode]
    if mode==0:bad[mode]=(u,v,F(0),h)
    elif mode==1:bad[mode]=(u,v,h+1,h)
    elif mode==2:bad[mode]=(u,v,float(l),h)
    elif mode==3:bad.pop(mode)
    else:bad.append((z(),z(1),F(1),F(1))) # wrong dimension/additional port
    try:C.construct(bad)
    except C.Unsupported:invalid+=1
    else:raise AssertionError('invalid box admitted')
counts['unsupported_boxes_rejected']=invalid
refusals=0
for f in [lambda:C.faces(p,max_masks=1),lambda:C.power(p['q'],-p['M'],max_exponent=1),lambda:C.power(p['q'],-p['M'],max_bits=1)]:
    try:f()
    except C.BudgetRefusal:refusals+=1
    else:raise AssertionError('budget not enforced')
counts['quantitative_refusals']=refusals
(root/'fixture_certificate.json').write_bytes(C.canonical_bytes(p))
(root/'resource_budget_examples.json').write_bytes(C.canonical_bytes(budgets))
result=dict(status='PASS_AUTHOR_COMMON_BOX_AND_RESOURCE_CONTROLS_NOT_INDEPENDENT',counts=counts,channels=len(p['raw']['channels']),Nstar_bits=p['Nstar'].bit_length(),certificate_bytes=len(C.canonical_bytes(p)),
            crossover={'initial_total':10,'failure':'1/100','last_tested_ordinary_horizon_power_of_two':cross_exp-1,'first_foster_horizon_power_of_two':cross_exp,'units':'mathematical time units of input rates; not operationally useful merely because finite'},
            short_horizon={'horizon':'1','count_level':budgets[0]['count_level'],'firing_level':budgets[0]['firing_level'],'selected':budgets[0]['selected_count_cap']},
            bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['common_box.py','COMMON_PREDICTABLE_BOX_THEOREM.md','check_common_box.py']})
(root/'common_box_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
