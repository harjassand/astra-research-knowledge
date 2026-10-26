"""Four-magnitude reduced qualification under an explicit cubic core/tail class.

The calibration table is GENERATED from the published nominal Pope model.
It is not new experimental data. Relative amplitude and frequency errors and
visible-tail limits are requirements of an illustrative qualification contract.
All interpolation enclosures are exact rational interval arithmetic.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import cmath
import numpy as np

HERE=Path(__file__).resolve().parent
M,K,C,G,R,L=map(F,['1.21','42992','4.56','12.5','1.7','.009'])
PI_LO,PI_HI=F(333,106),F(355,113)
XL=(2*31*PI_LO)**2;XH=(2*32*PI_HI)**2


class Interval:
    def __init__(self,lo,hi=None):
        self.lo=F(lo);self.hi=F(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,o):
        o=o if isinstance(o,Interval) else Interval(o)
        return Interval(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return Interval(-self.hi,-self.lo)
    def __sub__(self,o):return self+-as_interval(o)
    def __mul__(self,o):
        o=as_interval(o);p=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi]
        return Interval(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=as_interval(o);assert not o.lo<=0<=o.hi
        return self*Interval(1/o.hi,1/o.lo)


def as_interval(x):return x if isinstance(x,Interval) else Interval(x)


def source_q(x):
    # H(s)=-M*G*s^2/[M*L*s^3+(M*R+C*L)*s^2+(C*R+K*L+G^2)*s+K*R]
    p0=K*R/(M*G);p1=(C*R+K*L+G*G)/(M*G)
    p2=(M*R+C*L)/(M*G);p3=L/G
    return (p0-p2*x)**2+x*(p1-p3*x)**2


def generated_measurements():
    rows=[]
    for omega in [195,197,199,201]:
        x=F(omega*omega)
        mag=float(x*x/source_q(x))**.5
        center=F(str(round(mag,6)))
        measured_mag=Interval(center*F('.99'),center*F('1.01'))
        # 1 ppm frequency/timebase requirement, not a source measured accuracy.
        actual_x=Interval(x*F('.999999')**2,x*F('1.000001')**2)
        assert measured_mag.lo**2<=x*x/source_q(x)<=measured_mag.hi**2
        rows.append(dict(omega_nominal=omega,x=actual_x,mag=measured_mag,center=center))
    return rows


def qualify(rows,visible_tail,core_magnitude_floor,max_depth=16):
    # For the promised H=H_core+tail, |tail|<=visible_tail everywhere,
    # bound the cubic q_core(x)=x^2/|H_core(i sqrt(x))|^2 at uncertain nodes.
    ys=[]
    for row in rows:
        gl=row['mag'].lo-visible_tail;gu=row['mag'].hi+visible_tail
        assert gl>0
        ys.append(Interval(row['x'].lo**2/gu**2,row['x'].hi**2/gl**2))
    def q_enclosure(x_interval):
        result=Interval(0)
        for j,row in enumerate(rows):
            weight=Interval(1)
            for k,other in enumerate(rows):
                if k!=j:weight=weight*((x_interval-other['x'])/(row['x']-other['x']))
            result=result+weight*ys[j]
        return result
    core_magnitude_upper=F(30)
    stack=[(XL,XH,0)];leaves=0;maximum_depth=0;min_margin=None
    while stack:
        lo,hi,depth=stack.pop();qe=q_enclosure(Interval(lo,hi))
        margin=lo*lo-core_magnitude_floor**2*qe.hi
        upper_margin=core_magnitude_upper**2*qe.lo-hi*hi
        if margin>0 and upper_margin>0:
            leaves+=1;maximum_depth=max(maximum_depth,depth)
            min_margin=margin if min_margin is None else min(min_margin,margin)
            continue
        if depth>=max_depth:
            return dict(passport=False,reason='This sufficient interval proof did not close',
                        failed_x_interval=[str(lo),str(hi)],depth=depth)
        mid=(lo+hi)/2;stack.extend([(lo,mid,depth+1),(mid,hi,depth+1)])
    actual_floor=core_magnitude_floor-visible_tail
    assert actual_floor>0
    # R is a nominal-model resistance for the fixture. In a physical certificate,
    # this must be a certified lower bound on actual operating dissipation.
    b=(2*31*PI_LO)*R*actual_floor**2
    # Safe loss-only H-matrix bound. It does not reuse the full-complex 248k margin.
    edge_upper=F(25501);degree_upper=2*edge_upper
    beta=b-degree_upper
    assert beta>0
    def chain_ratio(n):
        unext=F(0);u=F(1)
        # u_N=1, u_(N-1)=1+beta/w, then owner's comparison recurrence.
        if n==0:return F(1)
        prev=1+beta/edge_upper
        for _ in range(n-1):unext,u=u,prev;prev=(2+beta/edge_upper)*u-unext
        return 1/prev
    n=next(n for n in range(1,30) if chain_ratio(n)<=F(1,100))
    return dict(passport=True,core_magnitude_floor_N_per_V=float(core_magnitude_floor),
                visible_tail_bound_N_per_V=float(visible_tail),
                full_transfer_magnitude_floor_N_per_V=float(actual_floor),
                full_transfer_magnitude_upper_N_per_V=float(core_magnitude_upper+visible_tail),
                resistance_lower_ohm=float(R),loss_floor_N_per_m=float(b),
                loss_floor_exact=str(b),
                comparison_margin_N_per_m=float(beta),
                one_base_total_connection_budget_N_per_m=float(edge_upper),
                whole_band_interval_leaves=leaves,max_interval_depth=maximum_depth,
                minimum_exact_interval_margin=str(min_margin),
                certified_chain_cells_for_one_percent=n,
                ratio_at_that_count=float(chain_ratio(n)),
                previous_count_ratio=float(chain_ratio(n-1)),
                nominal_source_mass_at_that_count_kg=6.181*n,
                static_series_stiffness_at_that_count_N_per_m=25000/n)


def source_h(omega,notch_impedance=0j):
    s=1j*omega
    den=(float(M)*s*s+float(C)*s+float(K))*(float(R)+float(L)*s+notch_impedance)+float(G*G)*s
    return -float(M*G)*s*s/den


def passive_notch_witness():
    # Parallel RLC inserted in SERIES with the otherwise unchanged electrical
    # loop. It is reciprocal/passive and its DC resistance tends to zero.
    # This defeats finite samples if the cubic/tail promise is dropped.
    omega0=198.0;ln=1e-7;rn=1e6;cn=1/(omega0*omega0*ln)
    def zn(omega):
        s=1j*omega
        return 1/(1/rn+1/(s*ln)+s*cn)
    rows=[]
    for omega in [195.,197.,199.,201.]:
        base=abs(source_h(omega));new=abs(source_h(omega,zn(omega)))
        rows.append(dict(omega_rad_per_s=omega,relative_magnitude_change=new/base-1))
    change=max(abs(r['relative_magnitude_change']) for r in rows)
    at_notch=abs(source_h(omega0,zn(omega0)))
    assert change<.01 and at_notch<.01
    # Loading by the actuator changes the isolated parallel-RLC ringdown.
    # Retain a numerical diagnostic of the ACTUAL connected denominator rather
    # than confusing component time with the loaded network's settling time.
    qn=np.array([rn,ln,rn*ln*cn])
    znum=np.convolve([float(R),float(L)],qn)
    znum[:2]+=np.array([0.,rn*ln])
    den=np.convolve([float(K),float(C),float(M)],znum)
    den[1:len(qn)+1]+=float(G*G)*qn
    poles=np.roots(den[::-1]);assert max(poles.real)<0
    return dict(omega0_rad_per_s=omega0,inductance_H=ln,parallel_resistance_ohm=rn,
                capacitance_F=cn,sample_changes=rows,
                maximum_sample_relative_magnitude_change=change,
                transfer_magnitude_at_notch_N_per_V=at_notch,
                isolated_parallel_RLC_ringdown_time_scale_seconds=2*rn*cn,
                connected_network_slowest_pole_real_part_diagnostic=float(max(poles.real)),
                connected_network_slow_time_scale_seconds_diagnostic=float(-1/max(poles.real)),
                scope='Finite passive reciprocal steady-state counterexample; large capacitance and settling time are charged, not hidden in a bounded-resource claim')


def main():
    rows=generated_measurements()
    exact_core=qualify(rows,F(0),F(20))
    tailed_core=qualify(rows,F('.5'),F(19))
    assert exact_core['passport'] and tailed_core['passport']
    result=dict(scope='Reduced qualification law, source-model-generated four-magnitude fixture, and passive notch counterexample. No new experiment or acquired metrological error bound.',
                input_data=[dict(omega_nominal=r['omega_nominal'],
                    magnitude_center_N_per_V=str(r['center']),
                    magnitude_interval_N_per_V=[str(r['mag'].lo),str(r['mag'].hi)],
                    x_interval=[str(r['x'].lo),str(r['x'].hi)]) for r in rows],
                required_relative_magnitude_error=.01,
                required_relative_frequency_error=1e-6,
                exact_cubic_core=exact_core,uniform_visible_tail_case=tailed_core,
                passive_notch_without_structural_promise=passive_notch_witness())
    (HERE/'reciprocal_loss_calibration_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
