"""Exact scalar-only constants for the proved Fourier alias bound.

No physical trace input is read. This verifies quadrature truncation
constants relative to f_p(0), assuming beta3 and the proved strip bound.
It does not enclose the floating physical traces in the angular preview.
"""
from fractions import Fraction as F
import json,pathlib,time,math
ROOT=pathlib.Path(__file__).resolve().parents[1]

def exp_bounds(x,degree=256):
    assert x>=0
    t=F(1);v=F(1)
    for k in range(1,degree+1):t*=x/k;v+=t
    nxt=t*x/(degree+1);ratio=x/(degree+2);assert ratio<1
    return v,v+nxt/(1-ratio)

def main():
    start=time.monotonic();rows=[]
    for N,y,cosh_upper,lower_error,upper_error in [
        (32,F(5,4),F(1889,1000),F(2,10**11),F(5,10**10)),
        (64,F(2),F(3763,1000),F(2,10**35),F(6,10**33))]:
        eylo,eyhi=exp_bounds(y)
        assert (eyhi+1/eylo)/2<cosh_upper
        den_exp_lower=exp_bounds(N*y)[0]
        assert den_exp_lower>1001
        denominator_factor_upper=F(1001,1000)
        c=18*(cosh_upper-1)
        plus_exponent=(N+1)*y-c
        minus_exponent=(N-2)*y-c
        assert plus_exponent>0 and minus_exponent>0
        plus_exp_lower=exp_bounds(plus_exponent)[0]
        minus_exp_lower=exp_bounds(minus_exponent)[0]
        assert denominator_factor_upper/plus_exp_lower<lower_error
        assert denominator_factor_upper/minus_exp_lower<upper_error
        rows.append({'angle_count':N,'spin':1,'imaginary_shift':str(y),
                     'cosh_strict_upper':str(cosh_upper),
                     'moment_lower_alias_error_coefficient':str(lower_error),
                     'moment_upper_alias_error_coefficient':str(upper_error),
                     'exact_cosine_hyperbolic_slack':str(cosh_upper-(eyhi+1/eylo)/2),
                     'exact_lower_alias_slack':str(lower_error-denominator_factor_upper/plus_exp_lower),
                     'exact_upper_alias_slack':str(upper_error-denominator_factor_upper/minus_exp_lower)})
    result={'status':'PASS_EXACT_SCALAR_FOURIER_ALIAS_CONSTANTS','beta':3,
            'assumed_proved_strip_bound':'|f(phi+i y)| <= f(0) exp[18(cosh(y)-1)]',
            'rows':rows,'seconds':time.monotonic()-start,
            'physical_traces_certified':False,
            'scope':'Exact quadrature alias constants only; no trace-sample or floating DFT enclosure.'}
    (ROOT/'results/alias_constants_fraction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='rows'},indent=2))
    for row in rows:print({k:row[k]for k in ['angle_count','moment_lower_alias_error_coefficient','moment_upper_alias_error_coefficient']})

if __name__=='__main__':main()
