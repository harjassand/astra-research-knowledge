#!/usr/bin/env python3
"""Author exact replay/contract tests; not independent mathematical review."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
import validated_variance as vv
ROOT=Path(__file__).resolve().parent

def no_floats(x):
    assert not isinstance(x,float)
    if isinstance(x,dict):
        for v in x.values():no_floats(v)
    if isinstance(x,list):
        for v in x:no_floats(v)

def independent_exp_bounds(x):
    """Separate exact-Fraction Taylor construction, degree 40, scale to 1/16."""
    x=F(x);power=1
    while x>F(1,16):x/=2;power*=2
    term=F(1);lower=term
    for k in range(1,41):term=term*x/k;lower+=term
    first=term*x/41
    upper=lower+first/(1-x/42)
    return lower**power,upper**power

def main():
    saved=json.loads((ROOT/'VARIANCE_CERTIFICATE.json').read_text());no_floats(saved)
    assert saved['code_sha256']==hashlib.sha256((ROOT/'validated_variance.py').read_bytes()).hexdigest()
    assert saved['scalar_code_sha256']==hashlib.sha256((vv.SCALAR/'validated_clock.py').read_bytes()).hexdigest()
    manifest=json.loads((vv.SCALAR/'SCALAR_FREEZE.json').read_text())
    for row in manifest['files']:
        assert hashlib.sha256((vv.SCALAR/row['path']).read_bytes()).hexdigest()==row['sha256']
    samples=[F(0),F(1,10000),F(1,8),F(2,7),F(1),F(3),F(17)]
    for z in samples:
        lo,hi=independent_exp_bounds(z)
        got=vv.exp_positive(vv.IV.exact(z))
        assert vv.asF(got.lo)<=lo<=hi<=vv.asF(got.hi)
        got=vv.exp_negative(vv.IV.exact(z))
        assert vv.asF(got.lo)<=1/hi<=1/lo<=vv.asF(got.hi)
    for x in [F(k,31) for k in range(1001)]:
        assert 1/(1+x)**3-(1-3*x)==(6*x*x+8*x**3+3*x**4)/(1+x)**3
        assert 1-3*x+6*x*x-1/(1+x)**3==(10*x**3+15*x**4+6*x**5)/(1+x)**3
    rerun=vv.solve(saved['inverse_grid_power'],saved['startup_intervals'],int(saved['terminal_e']),saved['inverse_taylor_order'])
    no_floats(rerun)
    for k,v in saved.items():
        if k!='wall_nanoseconds_nonproof':assert v==rerun[k],k
    lo,hi=F(saved['sigma_squared_lower']),F(saved['sigma_squared_upper'])
    assert hi-lo==F(saved['total_width'])<F(1,1000)
    assert F(saved['sigma_squared_decimal_outward'][0])<=lo<=hi<=F(saved['sigma_squared_decimal_outward'][1])
    assert F(saved['startup_width'])+F(saved['inverse_width'])+F(saved['tail_and_gap_charged_width'])==hi-lo
    assert 0<=F(saved['tail_and_gap_rounding_excess'])<F(1,vv.Q)
    assert F(saved['gap_variance_upper'])<F(1,10**26)
    assert F(saved['tail_variance_upper'])<F(2512,10**12)
    assert F(saved['startup_width'])<F('0.000235684126')
    assert F(saved['inverse_width'])<F('0.000754522242')
    out={'status':'PASS_AUTHOR_SELF_CHECK_NOT_INDEPENDENT_REVIEW','exact_full_replay':True,
         'no_float_certificate_fields':True,'existing_scalar_freeze_unchanged':True,
         'independent_fraction_exponential_samples':len(samples),
         'exact_tail_identity_samples':1001,'exact_width_ledger':True,
         'width_less_than_one_milliunit':True,'outward_decimal_bounds':True}
    (ROOT/'VERIFY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
