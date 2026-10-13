"""Exact finite existential lower bounds approaching log2(1+sqrt(2)).
These do not identify a matrix; matroid_witness.py supplies a separate explicit one.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import comb,isqrt
import importlib.util,json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('scaling',HERE.parent/'tensor_scaling.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)

def bound(r):
    D=3*r+isqrt(8*r*r)
    kappa=Q(1)
    for i in range(1,r+1):kappa*=Q(2**i-1,2**i)
    assert kappa>Q(1,4)
    expected=kappa*comb(D,r)
    Bmin=-((-expected.numerator)//expected.denominator)
    Wmin=Bmin*2**(2*D)
    Mmax=2**(D+r)
    ratio=s.ratio_bounds(s.log_bounds(Wmin),s.log_bounds(Mmax))
    alpha=(ratio[0]-1,ratio[1]-1)
    return dict(rank=r,D=D,n=2*D,minimum_bases_guaranteed=Bmin,
        term_and_truth_support_upper_bound=Mmax,
        minimum_W_guaranteed=Wmin,
        alpha_lower_certified=s.decimal_endpoint(alpha[0]),
        note='Existence by average basis count; no matrix identified in this row')

if __name__=='__main__':
    scale=10**80
    root_floor=isqrt(2*scale*scale)
    sqrt_lo=Q(root_floor,scale);sqrt_hi=Q(root_floor+1,scale)
    limit=s.ratio_bounds((s.log_bounds(1+sqrt_lo)[0],s.log_bounds(1+sqrt_hi)[1]),s.LN2)
    result=dict(status='RIGOROUS_EXISTENTIAL_FAMILY_NOT_EXPLICIT_MATRIX',
        limiting_exponent='log_2(1+sqrt(2))',
        limiting_exponent_interval=[s.decimal_endpoint(limit[0]),s.decimal_endpoint(limit[1],True)],
        rank_ratio='D/r -> 3+2*sqrt(2)',
        cases=[bound(r) for r in (8,16,32,64,128)],
        proof='Expected bases = binom(D,r) product_i(1-2^-i); some matrix meets expectation; m=k<=2^(D+r), W=B*2^(2D)')
    (HERE/'existence_bound_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**result,'cases':[{k:v for k,v in x.items() if k not in ('minimum_bases_guaranteed','term_and_truth_support_upper_bound','minimum_W_guaranteed')} for x in result['cases']]},indent=2))
