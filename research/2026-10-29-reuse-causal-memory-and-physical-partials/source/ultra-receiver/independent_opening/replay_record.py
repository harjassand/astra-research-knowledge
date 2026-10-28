#!/usr/bin/env python3
"""Second finite-record arithmetic route, using pair differences.

Does not import the image consumer or independently decode/verify its weighted
pixel sums. It checks the saved sufficient statistics and the exact covariance
algebra with an O(n^2) pair-difference formula rather than the O(n) compiler.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent


def paired_cov(a, b):
    n = len(a)
    return F(sum((a[i]-a[j])*(b[i]-b[j])
                 for i in range(n) for j in range(i)), n*(n-1))


def q(rows_a, rows_b, scale):
    return sum(coefficient * paired_cov([r[i] for r in rows_a],
                                        [r[j] for r in rows_b])
               for i,j,coefficient in [(2,7,-1),(3,6,-1),(0,5,2),(1,4,2)]) / scale**2


def log2_interval(n=40):
    y=F(1,3)
    lo=2*sum(y**(2*k+1)/F(2*k+1) for k in range(n))
    tail=2*y**(2*n+1)/((2*n+1)*(1-y*y))
    return lo,lo+tail


def main():
    started=time.perf_counter()
    moment_path=ROOT/'DATA_MOMENTS.json'
    data=json.loads(moment_path.read_text())
    receipt=json.loads((ROOT/'DATA_RECEIPT.json').read_text())
    records=data['records']; scale=data['moment_scale']
    a=[r['left'] for r in records]; b=[r['right'] for r in records]
    d=[[y-x for x,y in zip(v,w)] for v,w in zip(a,b)]
    vals={'forward':q(a,b,scale),'reverse':q(b,a,scale),
          'self_start_expected_zero_only_under_model':q(a,a,scale),
          'self_end_expected_zero_only_under_model':q(b,b,scale),
          'symmetric_difference_control':-q(d,d,scale)/2,
          'normalizer_empirical':paired_cov([r[8] for r in a],[r[8] for r in b])}
    for name,value in vals.items():
        lo=F(receipt[name]['lower_fraction']); hi=F(receipt[name]['upper_fraction'])
        assert lo<=value<=hi
        assert abs(float(value)-receipt[name]['center']) <= max(1e-6,abs(float(value))*1e-15)
    assert vals['normalizer_empirical']==F(-28011124984208,6225)
    assert vals['symmetric_difference_control']==(
        vals['forward']+vals['reverse']-
        vals['self_start_expected_zero_only_under_model']-
        vals['self_end_expected_zero_only_under_model'])/2
    lower,upper=log2_interval()
    vlo=F(160,27)*lower-F(26,9); vhi=F(160,27)*upper-F(26,9)
    assert vlo>F(6,5)
    result={'saved_moment_sha256':hashlib.sha256(moment_path.read_bytes()).hexdigest(),
            'pair_difference_covariance_route':'PASS',
            'quadratic_difference_identity':'PASS',
            'exact_covariance_values':{k:str(v) for k,v in vals.items()},
            'annulus_static_pattern_variance_coefficient':{
                'lower':str(vlo),'upper':str(vhi),
                'float_lower':float(vlo),'float_upper':float(vhi),
                'strict_lower_6_over_5':True,'log_terms':40},
            'physical_model_or_iid_validation':'NOT_PERFORMED',
            'independent_pixel_decode_or_weight_sum_replay':'NOT_PERFORMED',
            'seconds_after_imports':time.perf_counter()-started}
    (ROOT/'RECORD_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
