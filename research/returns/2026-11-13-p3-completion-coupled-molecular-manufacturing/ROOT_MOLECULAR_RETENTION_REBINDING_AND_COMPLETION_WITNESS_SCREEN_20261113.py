"""Introduced molecular-retention checkpoint screen, ROOT 13 Nov 2026.
All rates are chosen diagnostics, not measured bond properties or source fits.
This is ordinary two-state/absorbing CTMC mathematics, not a new machine.
"""
import json, math
from pathlib import Path

EPS=0.001
GOOD_LOSS=0.001
D_GOOD=1e-5

def endpoint_bound(t,a,b):
    return b/(a+b)+a/(a+b)*math.exp(-(a+b)*t)

def endpoint_time(a,b,eps):
    floor=b/(a+b)
    if floor>=eps:return None
    return -math.log((eps-floor)/(1-floor))/(a+b)

def sampled_time(a,b,delta,eps):
    # Bad bridge starts bound. Every sample must say bound to pass.
    p=endpoint_bound(delta,a,b)
    n=max(1,math.ceil(math.log(eps)/math.log(p)))
    t=n*delta
    return {"sample_interval_s":delta,"samples":n,"time_s":t,
            "bad_pass":math.exp(n*math.log(p)),
            "good_pass":math.exp(-D_GOOD*t)}

def not_separated(t,a,b,c):
    # B --a--> U --c--> D, U --b--> B; D is absorbing.
    # Count both B and U as possible false acceptance: a conservative screen.
    if c==0:return 1.
    z=a+b+c
    disc=math.sqrt(max(0.,z*z-4*a*c))
    fast=(z+disc)/2
    slow=(2*a*c)/(z+disc)
    if abs(fast-slow)<1e-10:
        return (1+slow*t)*math.exp(-slow*t)
    return (fast*math.exp(-slow*t)-slow*math.exp(-fast*t))/(fast-slow)

def separation_time(a,b,c,eps):
    if c==0:return None
    lo,hi=0.,1.
    while not_separated(hi,a,b,c)>eps:hi*=2
    for _ in range(100):
        mid=(lo+hi)/2
        if not_separated(mid,a,b,c)>eps:lo=mid
        else:hi=mid
    return hi

endpoint=[]
for b in [0.,0.001,0.01,1.,100.]:
    t=endpoint_time(1.,b,EPS)
    endpoint.append({"unbinding_s_inv":1.,"rebinding_s_inv":b,
        "false_pass_floor":b/(1+b),"required_time_s":t,
        "good_pass_at_required_time":math.exp(-D_GOOD*t) if t else None})
sampled=[sampled_time(1.,100.,dt,EPS) for dt in [0.0001,0.001,0.01,0.1,1.,10.]]
separation=[]
for c in [0.,0.01,0.1,1.,10.,100.,1000.]:
    t=separation_time(1.,100.,c,EPS)
    good=math.exp(-D_GOOD*t) if t else None
    separation.append({"unbinding_s_inv":1.,"rebinding_s_inv":100.,
        "irreversible_separation_s_inv":c,"required_time_s":t,
        "good_pass":good,
        "both_introduced_error_limits_met":good is not None and good>=1-GOOD_LOSS})
posteriors=[]
for prior in [0.001,0.1,0.5,0.99,0.9999]:
    bad_pass=EPS;good_pass=0.999
    posteriors.append({"prior_bad":prior,
        "posterior_bad_given_pass":prior*bad_pass/(prior*bad_pass+(1-prior)*good_pass)})
assert not_separated(0.,1.,100.,10.)==1.
assert not_separated(100.,1.,100.,0.)==1.
# With no rebinding and equal unbinding/separation rates this is Erlang(2).
for t in [0.,0.1,1.,10.]:
    assert abs(not_separated(t,1.,0.,1.)-(1+t)*math.exp(-t))<1e-12

data={"status":"INTRODUCED_DIAGNOSTIC_NOT_QUALIFIED_CHEMISTRY_OR_NOVEL_ASSEMBLER",
 "assumptions":["Finite constant rates; idealized bridge classes and chosen observations",
    "No measured force dependence, load partition, geometry, manufacture or chemistry supplied",
    "No gate hardware, absorbing displacement, sensing bandwidth or reset supplied",
    "Wrong covalent isomers or unintended strong bridges can be observationally identical to good product",
    "Error conditional on accepted output also depends on the input mixture and all rejected material",
    "Binary64 calculation and illustrative units; no physical experiment"],
 "limits":{"max_bad_pass":EPS,"max_good_loss":GOOD_LOSS,"introduced_good_break_s_inv":D_GOOD,
    "max_good_proof_time_s":-math.log1p(-GOOD_LOSS)/D_GOOD,
    "minimum_no_rebinding_weak_to_good_break_rate_ratio":
         math.log(1/EPS)/(-math.log1p(-GOOD_LOSS))},
 "endpoint_retention":endpoint,"finite_sampling":sampled,
 "absorbing_separation":separation,"posterior_examples":posteriors,
 "chemical_identity_limit":"Equal observable path distributions of two strong-bridge chemistries do not authenticate chemical identity. This screen separates only its declared bridge classes."}
out=Path(__file__).with_suffix(".json");out.write_text(json.dumps(data,indent=2)+"\n")
print(json.dumps({"output":str(out),**data}))

