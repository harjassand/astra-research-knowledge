"""Independent finite checks of passive acquisition constants and inequalities."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

HERE=Path(__file__).resolve().parent
s1=lambda s:140*s**3*(1-s)**3
s2=lambda s:420*s*s*(1-s)**2*(1-2*s)
s3=lambda s:840*s*(1-s)*(1-5*s+5*s*s)
constants=[35/16,84/(5*math.sqrt(5)),105/2]
maxima=[]
for fun,bound in zip([s1,s2,s3],constants):
    mesh=np.linspace(0,1,10001)
    maximum=max(abs(float(fun(t))) for t in mesh)
    assert maximum<=bound+1e-10
    maxima.append({'claimed':bound,'mesh_maximum':maximum})

variance_checks=[]
for n in [1,2,3,10,100,5000]:
    r=(np.arange(n)+.5)/n
    a=np.r_[r,1-r]/n
    theory=(4*n*n-1)/(6*n**3)
    assert abs(float(a.sum())-1)<1e-12
    assert abs(float(a@a)-theory)<1e-12
    variance_checks.append({'n':n,'weight_sum':float(a.sum()),'sum_squared_weights':float(a@a),'theory':theory})

h=.08
w=.03
T=2.
H=3.
rates=np.r_[0.,np.logspace(-12,12,181)]
rng=np.random.default_rng(73214)
weights=rng.dirichlet(np.ones(len(rates)))
z=rng.normal(size=len(rates))
G=float(weights@np.abs(z))

def ch(lam):
    lh=lam*h
    if lh==0: return 1.
    if lh<=50:
        return quad(lambda s:s1(s)*math.exp(-lh*(1-s)),0,1,epsabs=1e-13)[0]
    return quad(lambda r:s1(1-r/lh)*math.exp(-r)/lh,0,min(lh,60),epsabs=1e-15)[0]

def dw(lam):
    lw=lam*w
    return 1. if lw==0 else (-math.expm1(-lw)/lw)**2

filter_c=np.array([ch(l)*dw(l) for l in rates])
assert np.all(filter_c>=-1e-14) and np.all(filter_c<=1+1e-12)
per_mode_bias=np.array([(1-c)*(T if l==0 else -math.expm1(-l*T)/l) for l,c in zip(rates,filter_c)])
assert np.max(per_mode_bias)<=h/2+w+1e-12
mixture_bias=float(weights@per_mode_bias)
age_checks=[]
for t in [0.,.2,1.,T]:
    baseline=np.exp(-rates*(H-2*w))*np.array([dw(l) for l in rates])
    post=np.exp(-rates*(H+h+t))*np.array([dw(l) for l in rates])
    actual=abs(float((weights*z)@(post-baseline)))
    bound=G*(h+t+2*w)/(math.e*(H-2*w))
    assert actual<=bound+1e-12
    age_checks.append({'t':t,'actual_signed_force_change':actual,'bound':bound})

result={'septic_ramp_derivative_constants':maxima,'triangular_force_weight_variance':variance_checks,
        'test_spectrum':{'mode_count':len(rates),'has_frozen_mode':True,'smallest_positive_rate':float(rates[1]),'largest_rate':float(rates[-1])},
        'filter_bound':{'h':h,'w':w,'T':T,'largest_per_unit_weight_L1_bias':float(np.max(per_mode_bias)),
                        'mixture_L1_bias':mixture_bias,'claimed_mass_one_bound':h/2+w},
        'aged_baseline_bound':{'H':H,'initial_L1_force_G':G,'checks':age_checks}}
(HERE/'passive_bound_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
