"""Numerical checks of the interval lemma, not simulated empirical evidence."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parent

def integral(lo,hi,a,b):
    return quad(lambda z:1/np.sqrt(a*(1+z)**3+b),lo,hi,
                epsabs=1e-11,epsrel=1e-11)[0]

def main():
    rng=np.random.default_rng(551109)
    worst=0.
    for _ in range(100):
        lo=rng.uniform(0,2.);hi=lo+rng.uniform(.01,1.)
        a=rng.uniform(1e-4,5e-4);b=rng.uniform(2e-4,1e-3)
        d=b+rng.uniform(0,2e-3)
        lower=integral(lo,hi,a,d);upper=integral(lo,hi,a,b)
        theta=rng.uniform(.001,.999)
        target=lower+theta*(upper-lower)
        switch=brentq(lambda s:integral(lo,s,a,b)+integral(s,hi,a,d)-target,lo,hi,xtol=1e-13)
        error=abs(integral(lo,switch,a,b)+integral(switch,hi,a,d)-target)
        worst=max(worst,error)
        assert error<1e-9
        # Independent smooth monotone curve must remain between envelopes.
        def smooth_density(z):
            t=(z-lo)/(hi-lo)
            return b+(d-b)*(3*t*t-2*t*t*t)
        value=quad(lambda z:1/np.sqrt(a*(1+z)**3+smooth_density(z)),lo,hi,
            epsabs=1e-11,epsrel=1e-11)[0]
        assert lower-1e-10<=value<=upper+1e-10
    # Check bounded-slope envelopes (0 <= d log B/d log(1+z) <= 6).
    for _ in range(100):
        lo=rng.uniform(0,2.);hi=lo+rng.uniform(.01,1.)
        b=rng.uniform(.1,2.)
        power=rng.uniform(0,6.)
        d=b*((1+hi)/(1+lo))**power
        zz=np.linspace(lo,hi,1001)
        lower=np.maximum(b,d*((1+zz)/(1+hi))**6)
        upper=np.minimum(d,b*((1+zz)/(1+lo))**6)
        chosen=b*((1+zz)/(1+lo))**power
        assert np.all(lower<=upper+1e-10)
        assert np.all(chosen>=lower-1e-10) and np.all(chosen<=upper+1e-10)
    out={'status':'passed','unbounded_random_cases':100,'bounded_slope_cases':100,
         'worst_step_reconstruction_error':worst,
         'scope':'Numerical implementation diagnostics only; not observational evidence or a formal proof.'}
    (ROOT/'results/envelope_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
