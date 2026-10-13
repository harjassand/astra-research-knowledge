"""Optional pre-fault four-interaction interval acquisition.
Only synthetic nominal means are tested; no physical observations are fabricated.
The data interface is an actual pair of rational quadrature sample means per stage.
"""
from fractions import Fraction as F
from pathlib import Path
import json,math,time
from decision_certificate import atan_bounds,sqrt_bounds,down,up,fstr

def angle_interval(x:F,y:F):
    if x<=0:raise ValueError('calibration geometry not admitted: nonpositive X mean')
    lo,hi=sqrt_bounds(x*x+y*y)
    ts=[y/(lo+x),y/(hi+x)];tl,tu=min(ts),max(ts)
    if max(abs(tl),abs(tu))>=F(4,5):raise ValueError('outside certified half-angle series domain')
    def atan(q):
        if q>=0:return atan_bounds(q,128)
        a,b=atan_bounds(-q,128);return -b,-a
    a,_=atan(tl);_,b=atan(tu)
    return down(2*a,48),up(2*b,48)

def first_center(x,y):
    a,b=angle_interval(F(x),F(y));assert b-a<F(1,10**10)
    return (a+b)*4 # angle mean * 8

def certified_interval(center,x,y):
    a,b=angle_interval(F(x),F(y));assert b-a<F(1,10**10)
    fine=F(center)+(a+b)/4
    return fine-F(2,125),fine+F(2,125)

def certificate(folder='results'):
    started=time.perf_counter()
    # Two stages, four parameters, two quadratures: union of 16 mean errors.
    exponent=F(8192,625)
    positive=sum((exponent**k/F(math.factorial(k)) for k in range(41)),F(0))
    assert positive>320000
    failure=up(F(32)/positive)
    A=8*F(3,2)*F(101,10000)/(F(49,50)-F(3,2)*F(101,10000))
    B=F(1,2)*F(3,2)*F(201,10000)/(F(49,50)-F(3,2)*F(201,10000))
    assert A<F(63,500) and B<F(2,125)
    # Labeled synthetic exact-mean-like data only. Convert to dyadic scalars before
    # interval computation; no assertion that these are observed Bernoulli counts.
    checks=[]
    for true in [4,3,1,2]:
        x=F.from_float(math.exp(-.01/16)*math.cos(true/8));y=F.from_float(math.exp(-.01/16)*math.sin(true/8))
        c=first_center(x,y)
        xf=F.from_float(math.exp(-.01)*math.cos(2*(true-float(c))))
        yf=F.from_float(math.exp(-.01)*math.sin(2*(true-float(c))))
        a,b=certified_interval(c,xf,yf)
        assert a<=true<=b and a>=true-F(1,25) and b<=true+F(1,25)
        checks.append({'nominal_coefficient':true,'synthetic_interval':[fstr(a),fstr(b)],'accepted':True})
    out={'broad_prior':'each interaction in [0,8]; known d=1/100; all hopping and reservoirs frozen',
         'per_quadrature_mean_bias':'1/10000',
         'stage_1':{'duration':'1/8','shots_per_quadrature':2**18,'statistical_radius':'1/100','coefficient_error_upper':fstr(A)},
         'stage_2':{'duration':2,'shots_per_quadrature':2**16,'statistical_radius':'1/50','coefficient_error_upper':fstr(B)},
         'number_of_interactions':4,'quadratures_per_stage_per_interaction':2,
         'total_shots':2621440,'total_native_interrogation_time':1310720,
         'union_failure_upper':fstr(failure),
         'acceptance':'accept only when every entire interval lies in its target center +/-1/25; otherwise inconclusive',
         'statement':'probability of accepted false parameter coverage is at most the displayed union failure; not a conditional-on-rare-acceptance guarantee',
         'measurement_proposals':{'UL':'site0 Ramsey, site1 occupied, others empty','UR':'site3 Ramsey, site1 occupied, others empty','W':'site1 Ramsey, site2 occupied, others empty','Z':'site0 Ramsey, site3 occupied, others empty'},
         'acquisition_inputs':'known structural templates, phase-independent single-site coherent controls or charge-reference ancilla, preparation and readout bias bound; these calibration resources are not experimentally validated here',
         'synthetic_checks':checks,'lab_experiment_performed':False}
    decision_path=Path(folder,'decision_certificate.json')
    if decision_path.exists():
        decision=json.loads(decision_path.read_text())
        out['joint_probability_accepting_calibration_and_bad_control_upper']=fstr(failure+F(decision['bad_probability_upper']))
    out['construction_and_synthetic_check_seconds']=time.perf_counter()-started
    Path(folder,'calibration_certificate.json').write_text(json.dumps(out,indent=2));return out
if __name__=='__main__':
    c=certificate();print('shots',c['total_shots'],'time',c['total_native_interrogation_time'],'failure',float(F(c['union_failure_upper'])))
