"""Exact conditional record checks; no claim of physical calibration trials."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json, math

C=(F(3,20),F(3,10))
ETA=F(1,100)
D_RAW=F(19,400)
D_TARGET=F(51,400)

def clip(x,lo,hi):return max(lo,min(x,hi))
def high(p):return 2*p*(1-p)
def weight(p0h,p3h,c):return (high(p3h)-c)/(high(p3h)-p0h)
def marked_probs(p0,p3,w):
    return (w*(1-p0),w*p0,(1-w)*(1-p3)**2,
            (1-w)*(1-p3)*p3,(1-w)*p3*(1-p3),(1-w)*p3*p3)

def max_marked_tv(actual,reference,depth):
    # Bellman recursion over all policies using the FULL six-valued macro record.
    # a,b are unnormalized true/reference prefix masses. Symmetry removes Y.
    @lru_cache(None)
    def go(d,a,b):
        if d==0:return abs(a-b)/2
        return max(sum(go(d-1,a*p,b*q) for p,q in zip(pa,qa))
                   for pa,qa in zip(actual,reference))
    result=go(depth,F(1),F(1))
    return result,go.cache_info().currsize

checks=[]
worst=F(0)
worst_case=None
max_nodes=0
for h in (F(-1),F(-1,2),F(0),F(1,2),F(1)):
    p0=F(1,10)+h/20
    p3=F(7,20)+h/10
    for e0,e3 in product((-ETA,ETA),repeat=2):
        ph0=clip(p0+e0,F(1,20),F(3,20))
        ph3=clip(p3+e3,F(1,4),F(9,20))
        actual=[];reference=[]
        for c in C:
            w=weight(ph0,ph3,c)
            assert 0<=w<=1
            fitted=w*ph0+(1-w)*high(ph3)
            true=w*p0+(1-w)*high(p3)
            assert fitted==c
            assert abs(true-c)<=ETA
            a=marked_probs(p0,p3,w);b=marked_probs(ph0,ph3,w)
            assert sum(a)==sum(b)==1 and min(a+b)>=0
            actual.append(a);reference.append(b)
        val,nodes=max_marked_tv(tuple(actual),tuple(reference),3)
        max_nodes=max(max_nodes,nodes)
        if val>worst:
            worst=val;worst_case={'h':str(h),'estimated_p0':str(ph0),'estimated_p3':str(ph3)}
        checks.append({'h':str(h),'estimated_p0':str(ph0),'estimated_p3':str(ph3),
                       'exact_max_TV_all_depth_three_marked_policies':str(val)})
conditional_bound=float(ETA)*math.sqrt(3/float(D_RAW))
assert float(worst)<=conditional_bound

# Exact complete stopping-record discrepancy for the NOT controller.
slow,fast=F(1,4),F(9,20)
assert fast*(1-fast)>slow*(1-slow)
assert fast*(1-fast)**2<slow*(1-slow)**2
stop_tv=(1-(1-fast)**2)-(1-(1-slow)**2)
assert stop_tv==F(13,50)

resources=[]
for n,eps,beta in ((10,.1,.01),(100,.1,.01),(1000,.1,.01),(1000,.01,.001)):
    per_mode_marked=math.ceil(n*math.log(4/beta)/(2*float(D_RAW)*(eps-beta)**2))
    per_mode_unmarked=math.ceil(n*math.log(4/beta)/(4*float(D_TARGET)*(eps-beta)**2))
    resources.append({'macro_stages':n,'target_total_TV':eps,'confidence_failure_budget':beta,
                       'N_per_mode_exposed_marks':per_mode_marked,
                       'calibration_raw_calls_exposed_marks':2*per_mode_marked,
                       'N_per_mode_unmarked':per_mode_unmarked,
                       'deployment_raw_call_ceiling':2*n})

def entropy_to_uniform(x):
    return ((1+x)*math.log1p(x)+(1-x)*math.log1p(-x))/2

waiting=[]
for stages,tolerance in ((100,.01),(1000,.01),(1000,.001)):
    cmax=F(3,10)
    Lhybrid=max(1,math.ceil(math.log2(stages*float(cmax)/tolerance)))
    Lentropy=1
    while math.sqrt(stages*float(cmax)*entropy_to_uniform(2.0**(-Lentropy)))>tolerance:
        Lentropy+=1
    waiting.append({'macro_stages':stages,'target_TV':tolerance,
                    'hybrid_L':Lhybrid,
                    'hybrid_bound':float(stages*cmax/F(2)**Lhybrid),
                    'entropy_L':Lentropy,
                    'entropy_bound':math.sqrt(stages*float(cmax)*entropy_to_uniform(2.0**(-Lentropy))),
                    'expected_total_raw_call_ceiling_entropy':float(2*cmax*Lentropy*stages),
                    'maximum_total_raw_calls_entropy':Lentropy*stages})

# Exact endpoint-and-branch record check for two waiting lengths and all depth-3
# adaptive service policies, with no calibration. Native interiors are absent.
waiting_policy_checks=[]
for h,L in product((F(-1),F(0),F(1)),(2,3)):
    multiplier=(F(3,10)-h/5)**L
    pa=[];qa=[]
    for c in C:
        a=(1-2*c,c*(1+multiplier),c*(1-multiplier))
        b=(1-2*c,c,c)
        assert sum(a)==sum(b)==1
        assert sum(abs(x-y) for x,y in zip(a,b))/2==c*multiplier
        pa.append(a);qa.append(b)
    tv,_=max_marked_tv(tuple(pa),tuple(qa),3)
    hybrid=3*C[-1]/F(2)**L
    entropy=math.sqrt(3*float(C[-1])*entropy_to_uniform(2.0**(-L)))
    assert tv<=hybrid and float(tv)<=entropy
    waiting_policy_checks.append({'h':str(h),'L':L,'depth':3,
                                   'exact_worst_marked_TV':str(tv),
                                   'hybrid_bound':str(hybrid),'entropy_bound':entropy})

out={'scope':'Exact rational conditional model checks and analytic confidence arithmetic; not physical trials',
     'target_flip_probabilities':[str(c) for c in C],
     'calibration_error_radius_for_exact_checks':str(ETA),
     'tested_hidden_values':5,'tested_calibration_configurations':len(checks),
     'service_depth_macros':3,'macro_record_alphabet_size':6,
     'policy_optimization':'Exact Bellman recursion over every deterministic adaptive policy on the complete marked prefix; randomized policies cannot increase this convex objective',
     'worst_exact_marked_TV':str(worst),'worst_exact_marked_TV_decimal':float(worst),
     'worst_case':worst_case,'proved_conditional_marked_bound':conditional_bound,
     'maximum_Bellman_states':max_nodes,
     'stopping_NOT_expected_raw_call_ceiling':4,
     'stopping_NOT_endpoint_error':0,'stopping_exposed_time_TV_hminus_vs_hplus':str(stop_tv),
     'stopping_randomized_target_exposed_time_TV':[str(c*stop_tv) for c in C],
     'confidence_example_N_per_mode':30000,
     'confidence_example_failure_bound_at_eta_001':4*math.exp(-6),
     'resource_table':resources,'conditional_checks':checks,
     'waiting_resources':waiting,'waiting_conditional_checks':waiting_policy_checks}
p=Path(__file__).with_name('ORDINARY_COMPARATOR_CHECKS.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='conditional_checks'},indent=2))
