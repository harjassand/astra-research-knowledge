"""A full three-charge-state transfer certificate with one selected resonance.

The off-target diagonal source generator is unrestricted by the theorem.
Finite samples below check the proof against large noncommuting generators;
they do not certify arbitrary generators. The displayed coarse source box
and finite schedule are certified separately with rational arithmetic.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util
import json, math
import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('prior_exact_bounds', HERE.parent/'p2_spin_interface'/'exact_bounds.py')
eb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eb)
I = np.eye(2,dtype=complex)
X = np.array([[0,1],[1,0]],complex)
Y = np.array([[0,-1j],[1j,0]],complex)
Z = np.diag([1.,-1.]).astype(complex)

def sinh_upper(x, n=16):
    total = sum((x**(2*k+1)/F(math.factorial(2*k+1)) for k in range(n)), F(0))
    first_omitted = x**(2*n+1)/F(math.factorial(2*n+1))
    ratio = x*x/F((2*n+2)*(2*n+3))
    return total+first_omitted/(1-ratio)

def certify_box():
    # a_- = sqrt(2), a_+=b_+=2 sqrt(2), nu=4 exactly.
    # sqrt(2)>7/5 and 2 sqrt(2)<20/7.
    assert F(7,5)**2<2 and F(20,7)**2>8
    am,ap,nu,delta,kappa = F(7,5),F(20,7),F(4),F(1,5),F(1,5)
    bounds = []
    for t in [F(19,100), F(21,100)]:
        dyson_lower = am*t-ap*delta*t*t/2-sinh_upper(nu*t)+nu*t-kappa*t
        # The exact block-equation bound replaces the odd Dyson tail by a
        # cubic term. A double-sector perturbation is reached only after
        # one contact, so its contribution is quadratic, not linear.
        lower = am*t-(ap*delta+kappa*nu)*t*t/2-ap*nu*nu*t*t*t/6
        assert lower>0 and lower*lower>F(1,30)
        bounds.append(dict(tau=str(t),amplitude_lower=float(lower),
                           probability_lower=float(lower*lower),
                           initial_conservative_dyson_amplitude=float(dyson_lower)))
    # The lower function has negative second derivative for positive t;
    # its minimum on this interval is attained at an endpoint.
    return dict(arithmetic='exact fractions and cubic concavity; initial Dyson comparison uses a positive-series remainder',
                timing_interval=['19/100','21/100'],selected_detuning_norm='1/5',
                double_mixing_norm='1/5',hopping_norm_bound=4,
                certified_transfer_probability='1/30',endpoints=bounds,
                off_target_diagonal_generator='no bound assumed')

def schedule(epsilon):
    e=F(str(epsilon)); q=F(29,30)
    rcount=0
    while q**rcount>e/6:
        rcount+=1
    # sqrt(q)**N <= e/6, q**R <= e/6, using even N.
    n=2*rcount; r=rcount; count=n+r
    dch=e/(2*count)
    _, loghi=eb.log_interval(2/dch)
    ml=eb.ceil_fraction(8*loghi)
    ms=eb.ceil_fraction(F(20,7)*loghi)
    assert q**(n//2)+q**n+F(3,2)*q**r<=e/2
    assert F(ml,4)>=2*loghi and F(7*ms,10)>=2*loghi
    return dict(target=str(e),search_windows=n,return_windows=r,
                charge_interrogations=count,long_probes=ml,short_probes=ms,
                fresh_probe_slots=count*(ml+ms),
                hopping_time_upper_in_hbar_over_gmin=float(F(21,100)*count),
                note='Meter time, preparation, readout, ramps, loading, transport, and holding must also be added.')

def example_checks():
    out=[]
    for scale in [0.,10.,1000.]:
        for tau in [.19,.2,.21]:
            u=np.eye(6,dtype=complex)
            for k in range(7):
                hs=(17.3+4*k)*Y+(.7*k-1.2)*X
                da=.11*np.cos(k)*Z+.09*np.sin(k)*X
                hb=scale*(np.cos(.7*k)*X+np.sin(.7*k)*Z)+(.3*k-4)*I
                ta=np.sqrt(2)*(1.35*I+.20*np.cos(k)*X+.12j*np.sin(k)*Y)
                tb=np.sqrt(2)*(1.45*I+.17*np.sin(k)*Z+.16j*np.cos(k)*X)
                mix=.15*np.cos(k)*Y+.08j*np.sin(k)*Z
                assert np.linalg.eigvalsh((ta+ta.conj().T)/2).min()>=np.sqrt(2)
                assert np.linalg.norm(ta,2)<=2*np.sqrt(2)
                assert np.linalg.norm(tb,2)<=2*np.sqrt(2)
                assert np.linalg.norm(da,2)<=.2
                assert np.linalg.norm(mix,2)<=.2
                h=np.block([[hs,ta.conj().T,tb.conj().T],
                            [ta,hs+da,mix],
                            [tb,mix.conj().T,hb]])
                u=expm(-1j*h*tau/7)@u
            forward=float(np.linalg.svd(u[2:4,0:2],compute_uv=False).min())
            reverse=float(np.linalg.svd(u[0:2,2:4],compute_uv=False).min())
            bound=np.sqrt(2)*tau-(2*np.sqrt(2)*.2+.2*4)*tau*tau/2-(2*np.sqrt(2))*16*tau**3/6
            assert min(forward,reverse)>=bound-1e-12
            out.append(dict(off_target_scale=scale,tau=tau,amplitude_bound=float(bound),
                            forward_minimum_amplitude=forward,reverse_minimum_amplitude=reverse))
    return out

if __name__=='__main__':
    data=dict(scope=__doc__,certificate=certify_box(),
              schedules=[schedule(x) for x in ['0.01','0.0001','0.000001']],
              finite_noncommuting_source_checks=example_checks())
    (HERE/'one_resonance_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
