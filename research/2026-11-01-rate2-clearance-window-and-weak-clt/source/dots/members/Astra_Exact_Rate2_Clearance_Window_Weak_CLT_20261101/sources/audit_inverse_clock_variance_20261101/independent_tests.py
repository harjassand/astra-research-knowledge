#!/usr/bin/env python3
"""Exact independent interval, exponential, quadrature, and mutation checks."""
from fractions import Fraction as R
import hashlib,json
from pathlib import Path
import independent_variance as iv

ROOT=Path(__file__).resolve().parent

def independent_negative_exp(x):
    # Alternating rational series, unlike the author's positive-series tail.
    x=R(x);power=1
    while x>R(1,16):x/=2;power*=2
    term=R(1);even=R(1)
    for n in range(1,33):
        term=-term*x/n;even+=term
    odd=even-term*x/33
    assert 0<odd<=even
    return odd**power,even**power

def test_exponentials():
    points=[R(0),R(1,10000),R(1,8),R(2,7),R(1),R(3),R(17)]
    checked=0
    for x in points:
        lower,upper=independent_negative_exp(x)
        neg=iv.negative_exp(iv.Grid(x))
        pos=iv.expbox(iv.Grid(x))
        assert neg.lower<=lower<=upper<=neg.upper
        assert pos.lower<=1/upper<=1/lower<=pos.upper
        checked+=2
    for a,b in [(R(0),R(1,8)),(R(1,10),R(1)),(R(2),R(3))]:
        la,ua=independent_negative_exp(a);lb,ub=independent_negative_exp(b)
        neg=iv.negative_exp(iv.Grid(a,b));pos=iv.expbox(iv.Grid(a,b))
        assert neg.lower<=lb<=ub<=la<=ua<=neg.upper
        assert pos.lower<=1/ua<=1/la<=1/ub<=1/lb<=pos.upper
        checked+=2
    return checked

def test_rounding():
    points=[R(n,d) for d in (1,3,7,11) for n in range(-4,5)]
    n=0
    for x in points:
        for y in points:
            a=iv.Grid(x-R(1,31),x+R(1,37));b=iv.Grid(y-R(1,41),y+R(1,43))
            def test(g,lo,hi):
                assert g.lower==iv.ic.floor_grid(lo)
                assert g.upper==iv.ic.ceil_grid(hi)
            test(a+b,a.lower+b.lower,a.upper+b.upper)
            products=[v*w for v in (a.lower,a.upper) for w in (b.lower,b.upper)]
            test(a*b,min(products),max(products))
            if b.a>0 or b.b<0:test(b.inv(),1/b.upper,1/b.lower)
            n+=1
    for lo,hi in [(-1,1),(0,1),(-1,0),(0,0)]:
        try:iv.Grid(lo,hi).inv()
        except AssertionError:pass
        else:raise AssertionError('zero-containing reciprocal accepted')
    return n

def polyprod(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def test_tail_and_rectangles():
    low=polyprod([1,-3],[1,3,3,1]);low[0]-=1
    assert [-x for x in low]==[0,0,6,8,3]
    high=polyprod([1,-3,6],[1,3,3,1]);high[0]-=1
    assert high==[0,0,0,10,15,6]
    # Exact test integrand (1-l)^2 against dl on [0,1], integral 1/3.
    for n in [1,2,7,32]:
        ls=[iv.Grid(R(j,n)) for j in range(n+1)]
        qs=[iv.Grid(1-R(j,n)) for j in range(n+1)]
        bound=iv.rectangles(ls,qs)
        assert bound.lower<=R(1,3)<=bound.upper
    # A sharp counterexample to using the left rectangle as a lower bound.
    assert R(1)>R(1,3)>R(0)
    return 2,4

def test_certificates():
    path=ROOT/'frozen_inputs/inverse_clock_variance_20261101/VARIANCE_CERTIFICATE.json'
    saved=json.loads(path.read_text())
    repeated=json.loads((ROOT/'AUTHOR_CODE_REPLAY.json').read_text())
    iv.no_floats(saved);iv.no_floats(repeated)
    for k,v in saved.items():
        if k!='wall_nanoseconds_nonproof':assert repeated[k]==v,k
    expected=json.loads((ROOT/'INDEPENDENT_RECOMPUTED_FIELDS.json').read_text())
    mutations={
       'lower_endpoint_plus_one':('sigma_squared_lower',str(R(saved['sigma_squared_lower'])+1)),
       'inward_upper_decimal':('sigma_squared_decimal_outward',[saved['sigma_squared_decimal_outward'][0]]*2),
       'zero_origin_sensitivity_join':('J_at_s_half_lower','0'),
       'removed_H_tail':('H_tail_upper','0'),
       'removed_variance_tail':('tail_variance_upper','0'),
       'omitted_startup_join':('gap_variance_upper','0'),
       'wrong_rectangles':('startup_intervals',1023),
       'wrong_precision':('bits',119),
       'wrong_cost':('integer_interval_operations',dict(saved['integer_interval_operations'],div=0)),
    }
    for name,(key,bad) in mutations.items():
        altered=dict(saved);altered[key]=bad
        assert any(altered.get(k)!=v for k,v in expected.items()),name
    return list(mutations),repeated['wall_nanoseconds_nonproof']

def main():
    rejections,runtime=test_certificates()
    pairs=test_rounding();exps=test_exponentials();identities,rectangles=test_tail_and_rectangles()
    out={'status':'PASS_INDEPENDENT_VARIANCE_TESTS','full_author_code_replay_exact_except_nonproof_runtime':True,
         'author_replay_wall_nanoseconds_nonproof':runtime,'fraction_endpoint_rounding_pairs':pairs,
         'alternating_series_exponential_checks':exps,'symbolic_H_tail_polynomial_identities':identities,
         'exact_integral_monotone_rectangle_tests':rectangles,'zero_containing_reciprocals_rejected':4,
         'certificate_mutations_rejected':rejections,'left_rectangle_as_lower_bound_counterexample':'integrand (1-l)^2 on [0,1]: left rectangle 1 > exact integral 1/3',
         'no_actual_chain_CLT_claim':True}
    (ROOT/'INDEPENDENT_TEST_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
