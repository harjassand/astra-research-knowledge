"""Exact outward deadline certificate from the retained qualified mean intervals.

The only transcendental evaluation in the reported probability endpoints is
bounded by rational Taylor series.  The lifetime-law error is conservatively
rounded UP to 10^-10, with an entirely rational check of its sufficient bound.
This is a model probability certificate, conditional on the same statistical
event as qualified_intervals.json; it is not a physical-device measurement.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from qualify_intervals import exp_lower, decimal_out, serial

P = Path(__file__).resolve().parent

def fraction_from_json(x):
    return F(int(x['numerator']), int(x['denominator']))

def exp_negative_bounds(x, n=100):
    """For x>=0, bound exp(-x) by reciprocal positive Taylor sums."""
    assert x >= 0 and x < n+2
    term = F(1)
    total = term
    for k in range(1, n+1):
        term *= x/k
        total += term
    tail_upper = (term*x/(n+1))/(1-x/(n+2))
    return 1/(total+tail_upper), 1/total

def main():
    raw = json.loads((P/'qualified_intervals.json').read_text())
    deadline = F(10**12)
    true_gap_lower = F(1)  # known flip-rate floor 1/2
    delta_upper = F(4, 10**13)
    law_error = F(1, 10**10)

    # D(delta) increases on (0,1/4].  At delta_upper, pi>3 and
    # log(1+1/(4 delta_upper^2))<60 imply D<96 delta_upper.
    assert exp_lower(F(60), 200) > 1 + 1/(4*delta_upper**2)
    rows = []
    for row in raw['targets']:
        p = fraction_from_json(row['target_mass'])
        b = 1-p
        lo = fraction_from_json(row['exact_mean_lower'])
        hi = fraction_from_json(row['exact_mean_upper'])
        delta = 1/(true_gap_lower*b*lo)
        assert delta <= delta_upper <= F(1,4)
        assert (96*delta_upper+p)/b < law_error
        # Mean upper gives the smaller probability of hitting by a deadline.
        surv_hi_lo, surv_hi_hi = exp_negative_bounds(deadline/(b*hi))
        surv_lo_lo, surv_lo_hi = exp_negative_bounds(deadline/(b*lo))
        risk_lo = max(F(0), 1-surv_hi_hi-law_error)
        risk_hi = min(F(1), 1-surv_lo_lo+law_error)
        rows.append(dict(name=row['name'],
            separation_parameter_upper=decimal_out(delta, True),
            probability_lower_outward=decimal_out(risk_lo),
            probability_upper_outward=decimal_out(risk_hi, True),
            exact_probability_lower=serial(risk_lo),
            exact_probability_upper=serial(risk_hi)))
    out = dict(deadline=int(deadline), true_gap_lower=int(true_gap_lower),
        uniform_law_error=serial(law_error), confidence_lower=raw['confidence_lower'],
        assumptions='Same source and simulation confidence event; stationary start conditioned outside target',
        arithmetic='Exact Fraction bounds for exponentials; decimal endpoints rounded outward',
        targets=rows)
    (P/'deadline_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k!='targets'},indent=2))
    for row in rows:
        print(json.dumps({k:v for k,v in row.items() if not k.startswith('exact_')}))

if __name__=='__main__':
    main()
