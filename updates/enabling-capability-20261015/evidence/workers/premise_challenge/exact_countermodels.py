"""Exact arithmetic countermodels; no physical observations are synthesized as real data."""
from fractions import Fraction as F
from itertools import combinations
from math import factorial, log, ceil, prod
from pathlib import Path
import json


def click(ps, t=F(1)):
    return 1 - prod(1-t*p for p in ps)


def fm(ps, k):
    return factorial(k)*sum((prod(v) for v in combinations(ps,k)), F(0))


def law(ps):
    c=[F(1)]
    for p in ps:
        d=[F(0)]*(len(c)+1)
        for i,v in enumerate(c):
            d[i]+=v*(1-p); d[i+1]+=v*p
        c=d
    return [str(x) for x in c]


def main():
    h1=[F(3,4)]; h2=[F(1,2)]*2
    assert click(h1)==click(h2)==F(3,4)
    assert click(h1,F(1,2))==F(3,8)
    assert click(h2,F(1,2))==F(7,16)
    m2=[F(1,2)]*2; m3=[F(2,3),F(1,6),F(1,6)]
    assert fm(m2,1)==fm(m3,1)==1
    assert fm(m2,2)==fm(m3,2)==F(1,2)
    assert fm(m2,3)==0 and fm(m3,3)==F(1,9)
    assert law(m2)!=law(m3)
    # Physically lower efficiency: match threshold law by adjusting unknown
    # source brightness, then compare attainable measurement additions.
    efficiency=F(3,25)
    physical_one=[1-efficiency/4]
    physical_two=[F(1,2)]*2
    detected_one=[efficiency*p for p in physical_one]
    detected_two=[efficiency*p for p in physical_two]
    assert click(detected_one)==click(detected_two)
    p1=click(detected_one,F(1,2)); p2=click(detected_two,F(1,2))
    gap=float(p2-p1)
    alpha=.05
    # Known simple alternatives, fixed halfway threshold, independent pulses.
    hoeffding_n=ceil(2*log(1/alpha)/gap**2)
    pair_prob=float(efficiency**2/F(8))
    pair_n=ceil(log(alpha)/log(1-pair_prob))
    a=efficiency*(1-efficiency/4)
    b=efficiency**2/4
    kl_upper=4*b*b/(27*a*(1-a))
    required_decision_kl=(1-2*alpha)*log((1-alpha)/alpha)
    adaptive_lower_n=ceil(required_decision_kl/float(kl_upper))
    out={
        'status':'EXACT_INTERNAL_CHECK_PASSED',
        'scope':'Ideal independent Bernoulli emission per pulse, declared threshold observation; not experimental validation or novel theorem.',
        'threshold_countermodel':{
            'source_probabilities':[list(map(str,h1)),list(map(str,h2))],
            'equal_click_probability':str(click(h1)),
            'half_transmission_click_probabilities':[str(click(h1,F(1,2))),str(click(h2,F(1,2)))],
            'full_observed_laws':'Equal iid Bernoulli law at original transmission for every sample size.',
            'ideal_hoeffding_pulses_for_each_error_at_most_0_05':ceil(512*log(20))},
        'moment_countermodel':{
            'source_probabilities':[list(map(str,m2)),list(map(str,m3))],
            'factorial_moments':[[str(fm(ps,k)) for k in [1,2,3]] for ps in [m2,m3]],
            'photon_number_laws':[law(m2),law(m3)],
            'scope':'Only first and second moments agree; full raw count laws do not.'},
        'matched_efficiency_benchmark':{
            'efficiency':str(efficiency),
            'underlying_source_probabilities':[list(map(str,physical_one)),list(map(str,physical_two))],
            'equal_original_click_probability':str(click(detected_one)),
            'half_transmission_click_probabilities':[str(p1),str(p2)],
            'attenuation_hoeffding_upper_bound_pulses':hoeffding_n,
            'two_detector_pair_probability_under_two_emitters':pair_prob,
            'pair_detection_pulses_for_95pct_power':pair_n,
            'adaptive_attenuation_per_pulse_KL_upper_bound':str(kl_upper),
            'adaptive_attenuation_pulse_lower_bound_for_both_errors_0_05':adaptive_lower_n,
            'lower_bound_proof':'For every transmission t in [0,1], p0=a*t, p1=eta*t-eta^2*t^2/4, difference=b*t*(1-t). Bernoulli KL <= chi-square <= b^2*t*(1-t)^2/[a*(1-a)] <= 4*b^2/[27*a*(1-a)]. Conditional KL chain rule applies to adaptive transmission policies. A decision with both errors <=alpha needs KL >= (1-2alpha)*log((1-alpha)/alpha).',
            'assumptions':'Background-free; no deadtime, crosstalk, afterpulsing or fluorescence carryover; known simple hypotheses. Pair test has ideal zero false-positive probability. Hoeffding is a conservative sufficient budget, not a fair exact optimality comparison.',
            'conclusion':'Any fixed-budget adaptive attenuation-only binary policy needs at least the stated lower bound; an ideal two-detector coincidence policy attains the stated upper bound. This is a rigorous shot-budget separation for these fixed alternatives, not an end-to-end cost or practical advantage claim.'},
        'dim_emitter_bound':{
            'statement':'Adding emitters with total per-pulse detection probability at most epsilon changes the n-pulse full observed law in total variation by at most n*epsilon (coupling/union bound).',
            'consequence':'No uniformly finite reliable count certification over arbitrarily small positive brightness. Dark emitters give exactly equal full optical laws.'},
        'inference_cost':'UNKNOWN'
    }
    path=Path(__file__).with_name('EXACT_COUNTERMODELS.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
