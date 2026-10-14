"""Conservative global uncertainty from finite pairwise/degree-two query errors.
This propagates declared deterministic oracle errors, not a laboratory validation.
"""
from fractions import Fraction as F
from math import comb,log,ceil
from pathlib import Path
import json
ROOT=Path(__file__).parent

def exp_interval(x,N=32):
    assert x>=0 and x<N+2
    term=F(1);s=term
    for k in range(1,N+1):term*=x/k;s+=term
    nex=term*x/(N+1)
    return s,s+nex/(1-x/F(N+2))

def propagate(row,energy_error=F(1,10**6),balanced_error=F(1,10**8),amin=F(1,200),kappa_rel=F(1,500),n=18):
    # All pair terms may be uncertain, including nominal zero interactions.
    Omega=(2*n+6*comb(n,2))*energy_error
    amp=2*(1+2*(n-1)+4*comb(n-1,2))
    eta=max(amp*balanced_error/amin,kappa_rel)
    assert eta<1
    elo,ehi=exp_interval(2*Omega)
    lower=F(row['lower'])/ehi/(1+eta);upper=F(row['upper'])*ehi/(1-eta)
    return dict(lower=str(lower),upper=str(upper),lower_float=float(lower),upper_float=float(upper),mass_log_oscillation=str(Omega),clock_relative_envelope=str(eta),attempt_absolute_error_amplifier=amp)

def main():
    a=json.load(open(ROOT/'pcg_primary_r3.json'));b=json.load(open(ROOT/'unknown_support_rare.json'))
    aa=propagate(a);bb=propagate(b)
    ratio=F(b['lower'])/F(a['upper']);robust=F(bb['lower'])/F(aa['upper'])
    tr=json.load(open(ROOT/'unknown_support_rare_transcript.json'));rates=[F(x) for x in tr['balanced_rates'].values()]
    M=len(rates);confidence=0.05;absolute_error=1e-8
    # Sample each clamped-context first-flip dwell repeatedly. If |samplemean/true-1|<=e,
    # inverse-mean rate estimate has relative error<=e/(1-e). Set e to meet absolute bound.
    expected_time=0;sample_count=0
    for q in rates:
        eps=absolute_error/(float(q)+absolute_error)
        m=ceil(4*log(2*M/confidence)/(eps*eps));sample_count+=m;expected_time+=m/float(q)
    out={'exact_decision_ratio_lower':str(ratio),'exact_decision_ratio_lower_float':float(ratio),'robust_A':aa,'robust_B':bb,'robust_decision_ratio_lower':str(robust),'robust_decision_ratio_lower_float':float(robust),'assumed_dimensionless_energy_error':'1e-6','assumed_balanced_rate_absolute_error':'1e-8','minimum_reference_attempt':'1/200','measurement_accounting':{'number_of_distinct_contexts':M,'confidence_failure_bound':confidence,'conservative_dwell_samples':str(sample_count),'expected_total_dwell_model_time':expected_time,'includes_reset_or_clamp_cost':False,'scope':'upper-bound design based on independent exponential dwells; not actual experiments or a lower bound'}}
    json.dump(out,open(ROOT/'uncertainty_results.json','w'),indent=2)
    print({k:v for k,v in out.items() if k not in ['robust_A','robust_B','exact_decision_ratio_lower','robust_decision_ratio_lower']});print('A',aa['lower_float'],aa['upper_float'],'B',bb['lower_float'],bb['upper_float'])
if __name__=='__main__':main()
