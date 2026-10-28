"""Independent exact-rational bounds for the declared 32-state model.

This validates the model's return revival without scipy, matrix logarithms,
floating exponential evaluation, or random trials. It is not physical evidence.
"""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
N=180

def bound_return(t):
    x=F(31,5)*t
    v=[F(1)]+[F(0)]*31
    coefficient=F(1);E=F(0);S=F(0)
    for k in range(N+1):
        E+=coefficient;S+=coefficient*v[0]
        v=[F(26,31)*v[0]+v[31],F(5,31)*v[0]]+v[1:31]
        coefficient*=x/F(k+1)
    # coefficient is x^(N+1)/(N+1)!; later Taylor-term ratios <=x/(N+2).
    tail=coefficient/(1-x/F(N+2))
    return S/(E+tail),(S+tail)/E

def encode_interval(interval):
    lo,hi=interval
    return {'lower_exact':str(lo),'upper_exact':str(hi),
            'lower_display':float(lo),'upper_display':float(hi),
            'exact_width':str(hi-lo),'width_display':float(hi-lo)}

def h(s):return F(1,100)+F(49,50)*s*s

if __name__=='__main__':
    record=json.loads((ROOT/'outputs/ordinal_one_state_record.json').read_text())
    returns=[bound_return(F(3)),bound_return(F(6))]
    revival_lower=returns[1][0]-returns[0][1]
    assert revival_lower>0
    ae=F(17,20);al=F(9,10);p0=F(8,31);theta=F(17,155);pi0=F(1,6)
    means=[]
    for lo,hi in returns:
        # p0(t)=(1-theta)*pi0+theta*P00(t), exactly.
        late_lo=1-al*((1-theta)*pi0+theta*hi)
        late_hi=1-al*((1-theta)*pi0+theta*lo)
        both_lo=1-ae*p0-al*(1-theta)*pi0+al*theta*lo
        both_hi=1-ae*p0-al*(1-theta)*pi0+al*theta*hi
        means += [(h(late_lo),h(late_hi)),(h(both_lo),h(both_hi))]
    float_mean_error=[]
    for approximate,(lo,hi) in zip(record['exact_means'],means):
        exact_float=F.from_float(approximate)
        error=max(abs(exact_float-lo),abs(exact_float-hi))
        assert error<F(1,10**12)
        float_mean_error.append(error)
    late_margin=means[0][0]-means[2][1]
    both_margin=means[3][0]-means[1][1]
    assert late_margin>0 and both_margin>0
    result={'scope':'independent exact-rational declared-model certificate; no physical experiment or historical novelty claim',
            'uniformization_rate_exact':'31/5','Taylor_last_degree':N,
            'method':'positive stochastic uniformization; exact rational exponential Taylor bounds and geometric upper tail',
            'return_intervals':[encode_interval(x) for x in returns],
            'return_revival_lower_exact':str(revival_lower),'return_revival_lower_display':float(revival_lower),
            'detector_mean_intervals':[encode_interval(x) for x in means],
            'ordinal_mean_margins_lower_exact':[str(late_margin),str(both_margin)],
            'ordinal_mean_margins_lower_display':[float(late_margin),float(both_margin)],
            'synthetic_forward_mean_float_error_upper_exact':[str(x) for x in float_mean_error],
            'max_synthetic_forward_mean_float_error_upper_display':float(max(float_mean_error)),
            'inference_scope':'detector law used here only to validate declared synthetic forward model; ordinal inference never uses it'}
    (ROOT/'outputs/uniformization_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['return_intervals','detector_mean_intervals','return_revival_lower_exact','ordinal_mean_margins_lower_exact','synthetic_forward_mean_float_error_upper_exact']},indent=2))
