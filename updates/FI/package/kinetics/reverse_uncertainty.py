"""Reverse-query errors propagated to a complete kinetic model envelope.
The global pairwise energy and degree-two attempt classes remain premises.
"""
from fractions import Fraction as F
from math import comb,ceil,log
from pathlib import Path
import json
from uncertainty import exp_interval
from reverse_tomography import recover_reverse
ROOT=Path(__file__).parent

def main():
    n=18;de=F(1,10**10);dq=F(1,10**8);M=n*(1+(n-1)+comb(n-1,2));H=1+2*(n-1)+4*comb(n-1,2)
    Omega=(2*n+6*comb(n,2))*de
    # Context probes have at most two ones: log local weight-ratio error <=10 de.
    _,e=exp_interval(10*de)
    tr=json.load(open(ROOT/'reverse_B_transcript.json'));m,coefs,derived=recover_reverse(n,tr)
    measured_a=[2*F(v) for v in derived.values()];amax=max(measured_a)
    amin=min(v for t in m['clock_tables'].values() for v in t)
    point_error=2*e*dq+amax*(e-1)
    eta=max(H*point_error/amin,F(1,500));assert eta<1
    _,massfactor=exp_interval(2*Omega)
    rows={}
    for key in ['A','B']:
        row=json.load(open(ROOT/f'reverse_{key}.json'))
        lo=F(row['lower'])/massfactor/(1+eta);hi=F(row['upper'])*massfactor/(1-eta)
        rows[key]=dict(lower=str(lo),upper=str(hi),lower_float=float(lo),upper_float=float(hi))
    ratio=F(rows['B']['lower'])/F(rows['A']['upper'])
    samples=0;dwell=0.
    for val in tr['reverse_rates'].values():
        q=float(F(val));eps=float(dq)/(q+float(dq));count=ceil(4*log(2*M/.05)/eps**2)
        samples+=count;dwell+=count/q
    out=dict(energy_absolute_error=str(de),reverse_rate_absolute_error=str(dq),source_mass_log_oscillation=str(Omega),query_attempt_absolute_error_bound=str(point_error),degree_two_error_amplifier=H,minimum_nominal_attempt=str(amin),clock_relative_bound=str(eta),clock_relative_bound_float=float(eta),rows=rows,robust_ratio_lower=str(ratio),robust_ratio_lower_float=float(ratio),maximum_local_preparation_energy_kBT=log(float(F(tr['maximum_local_excitation_weight_ratio']))),measurement_accounting=dict(contexts=M,sufficient_independent_dwell_samples=str(samples),expected_dwell_model_time=dwell,reset_and_clamping_cost_included=False,scope='sufficient conservative sample design, not a necessary lower bound and not executed physically'))
    json.dump(out,open(ROOT/'reverse_uncertainty_results.json','w'),indent=2)
    print({'ratio':float(ratio),'A':[rows['A']['lower_float'],rows['A']['upper_float']],'B':[rows['B']['lower_float'],rows['B']['upper_float']],'eta':float(eta),'samples':str(samples),'dwell':dwell,'max_local_work':out['maximum_local_preparation_energy_kBT']})
if __name__=='__main__':main()
