"""One-sided finite-fixture gain data -> intrinsic cubic loss certificate.

Reuses the producer's reviewed exact interval arithmetic, not its two-sided
qualification. All measurement centers are MODEL GENERATED, not laboratory data.
The fixture is a supplied pure damper; no whole fixture transfer model is fitted.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util
import json
import math

HERE=Path(__file__).resolve().parent
producer=HERE.parents[1]/'connection/passive_isolation_physical_bridge/reciprocal_loss_calibration.py'
spec=importlib.util.spec_from_file_location('interval_primitive',producer)
primitive=importlib.util.module_from_spec(spec);spec.loader.exec_module(primitive)
Interval=primitive.Interval
PI_LO,PI_HI=F(333,106),F(355,113)
XL=(62*PI_LO)**2;XH=(64*PI_HI)**2

def model(w):
    # Actual physical core and carrier only generate the displayed fixture data.
    # None of these reactive parameters enter the interval qualification below.
    m0,m,k,c,g,R,L=4.971,1.21,42992.,4.56,12.5,1.7,.009
    h=k+1j*w*c+1j*w*g*g/(R+1j*w*L)
    a=-w*w*(m0+m*h/(h-m*w*w))
    H=-g*m*w*w/((R+1j*w*L)*(k-m*w*w+1j*w*c)+1j*w*g*g)
    Zs=a/(1j*w);Zf=100000.0
    return H,-Zf/(Zs+Zf)*H

def rows():
    out=[]
    for w in [195,197,199,201]:
        H,transfer=model(w)
        center=F(str(round(abs(transfer),6)))
        gain_low=center*F('.99')
        assert float(gain_low)<abs(H)
        xx=F(w*w)
        out.append(dict(omega=w,x=Interval(xx*F('.999999')**2,xx*F('1.000001')**2),
            fixture_magnitude_center=center,known_fixture_cosine=F(1),gain_lower=gain_low))
    return out

def certify(data,tail,floor,maximum_depth=16):
    # Pointwise fixture factors are enough. The fixture transfer need not be
    # cubic. The intrinsic q_core is nonnegative cubic by its structural promise.
    qs=[]
    for row in data:
        core_gain_lower=row['known_fixture_cosine']*row['gain_lower']-tail
        assert core_gain_lower>0
        qs.append(Interval(0,row['x'].hi**2/core_gain_lower**2))
    def upper(a,b):
        z=Interval(a,b);total=Interval(0)
        for j,row in enumerate(data):
            lag=Interval(1)
            for i,other in enumerate(data):
                if i!=j:lag=lag*(z-other['x'])/(row['x']-other['x'])
            total=total+lag*qs[j]
        return total.hi
    stack=[(XL,XH,0)];leaves=0;depthmax=0;minimum=None
    while stack:
        a,b,d=stack.pop();gap=a*a-floor*floor*upper(a,b)
        if gap>0:
            leaves+=1;depthmax=max(depthmax,d)
            minimum=gap if minimum is None else min(minimum,gap)
        elif d>=maximum_depth:
            return dict(certified=False,reason='Sufficient interval bound did not close')
        else:
            mid=(a+b)/2;stack.extend([(a,mid,d+1),(mid,b,d+1)])
    actual_floor=floor-tail
    assert actual_floor>0
    loss=62*PI_LO*F('1.7')*actual_floor**2
    edge=F(25501);beta=loss-2*edge
    if beta>0:
        # Known equal-connector chain comparison, free end and one base.
        def ratio(n):
            prev,current=F(1),1+beta/edge
            for _ in range(n-1):prev,current=current,(2+beta/edge)*current-prev
            return 1/current
        cells=next(n for n in range(1,50) if ratio(n)<F(1,100))
    else:
        cells=None
    return dict(certified=True,assumed_uniform_visible_tail_N_per_V=float(tail),
        intrinsic_core_gain_lower=float(floor),actual_gain_lower=float(actual_floor),
        loss_floor_N_per_m=float(loss),loss_floor_exact=str(loss),
        conservative_comparison_margin_N_per_m=float(beta),
        chain_cells_for_one_percent=cells,
        ratio_at_that_count=float(ratio(cells)) if cells else None,
        interval_leaves=leaves,maximum_depth=depthmax,
        minimum_exact_margin=str(minimum),upper_gain_certified=False)

data=rows()
# Fixed, declared thresholds, not an optimization over new physical records.
exact=certify(data,F(0),F(17))
tailed=certify(data,F('.5'),F(16))
assert exact['certified'] and tailed['certified']
result=dict(scope='New one-sided finite-fixture compiler under intrinsic cubic/tail promise. Synthetic source-model fixture, no acquired physical envelope.',
    given_fixture_impedance_Ns_per_m=100000.,fixture_type='supplied pure viscous damper',
    measured_frequency_relative_error_requirement=1e-6,
    measured_magnitude_relative_error_requirement=.01,
    rows=[dict(omega_nominal=r['omega'],fixture_gain_center_N_per_V=str(r['fixture_magnitude_center']),
               fixture_gain_lower_N_per_V=str(r['gain_lower']),
               x_interval=[str(r['x'].lo),str(r['x'].hi)]) for r in data],
    exact_core=exact,visible_tail=tailed)
(HERE/'finite_fixture_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
