"""Floating diagnostic of exact angular and weak-form identities. No N-body claim."""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import sici

PI=math.pi
A=PI/2

def sinc(x):
    return float(np.sinc(x/PI))

def phi_cos(x):
    if abs(abs(x)-A)<1e-7:
        h=abs(x)-A
        # what(A+h)=pi sin(h)/(h*(pi+h))
        what=PI*sinc(h)/(PI+h)
    else:
        what=PI*math.cos(x)/(A*A-x*x)
    return what*what/(2*PI)

def phi_triangle(x):
    return 3*sinc(x/2)**4/(4*PI)

def angular(phi,a):
    return 2*quad(lambda x:(1-(x/a)**2)*phi(x),0,a,
                  epsabs=3e-11,limit=500)[0]

def r_fejer(a):
    if a<0.03:
        return 2*a/(3*PI)-a**3/(90*PI)+a**5/(6300*PI)
    return 2/PI*(sici(a)[0]+(math.cos(a)-2)/a+math.sin(a)/a**2)

def coeff_cos(r,L,K,kappa=1):
    t=L/2
    fn=lambda k:k**3/(k*k+kappa*kappa)**2*angular(phi_cos,t*k*r)
    return PI/r*quad(fn,0,K,epsabs=2e-8,limit=150)[0]

def coeff_inf(r,K,kappa=1):
    z=K*K/kappa**2
    return PI/(2*r)*(math.log1p(z)+1/(1+z)-1)

rows=[]
for a in [0.1,1,3,10,30,100]:
    rc=angular(phi_cos,a)
    rt=angular(phi_triangle,a)
    rf=r_fejer(a)
    rows.append(dict(a=a,cosine=rc,triangle=rt,fejer=rf,
                     fejer_at_equal_maximum_time_lag=r_fejer(2*a),
                     cosine_scaled_deficit=a*a*(1-rc),
                     triangle_scaled_deficit=a*a*(1-rt),
                     fejer_scaled_deficit=a*(1-rf)))
    assert 0<=rc<=1+1e-12
    assert 1-rc<=A*A/a**2+1e-10

cutoff=[]
for K in [1,10,100]:
    for L in [2,8,32]:
        exact=coeff_inf(1,K)
        finite=coeff_cos(1,L,K)
        bound=PI**3/(2*L*L)
        cutoff.append(dict(K=K,L=L,infinite=exact,finite=finite,
                           difference=exact-finite,bound=bound))
        assert -2e-7<=exact-finite<=bound+2e-7

heating=[]
for T in [0.25,1,4,16]:
    val=2/T*quad(lambda k:k*k/(k*k+1)**2*(-math.expm1(-T*T*k*k)),
                 0,np.inf,epsabs=1e-10,limit=300)[0]
    heating.append(dict(T=T,raw_maxwellian_energy_rate=val,
                        projected_energy_rate=0.0))
    assert val>0

# The unscreened radial integral and a genuinely different, Tonelli-swapped
# formula. Analytic proofs in FINITE_TIME_RESONANCE.txt carry the claims.
si_pi,ci_pi=sici(PI)
c_cos=0.5+math.log(PI/2)-ci_pi-si_pi/PI
unscreened=[]
for cutoff_parameter in [0.01,0.1,1,3,10,100]:
    direct=quad(lambda a:angular(phi_cos,a)/a,0,cutoff_parameter,
                epsabs=1e-9,limit=250)[0]
    swapped=2*quad(lambda x:phi_cos(x)*(math.log(cutoff_parameter/x)
                         -0.5+x*x/(2*cutoff_parameter**2)),
                   0,cutoff_parameter,epsabs=1e-9,limit=250)[0]
    error=swapped-math.log(cutoff_parameter)+c_cos
    bound=A*A/(2*cutoff_parameter**2)
    raw_longitudinal_scaled=angular(phi_cos,cutoff_parameter)
    unscreened.append(dict(A=cutoff_parameter,J_direct=direct,J_swapped=swapped,
                          logarithmic_remainder=error,remainder_bound=bound,
                          raw_longitudinal_coefficient_over_pi_per_r=
                          raw_longitudinal_scaled))
    assert abs(direct-swapped)<2e-8
    assert -2e-8<=error<=bound+2e-8

out=dict(status='floating_diagnostic_not_microscopic_validation',
         runtime='/Library/Frameworks/Python.framework/Versions/3.13/bin/python3',
         exact_cosine_variance=A*A,exact_triangle_variance=3,
         angular=rows,cutoff=cutoff,maxwellian_heating=heating,
         unscreened_cosine_log_constant=c_cos,unscreened=unscreened)
path=Path(__file__).with_name('resonance_evidence.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
