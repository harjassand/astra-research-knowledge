"""A genuine determinant resonance, distinct from a spurious scalar pivot.

M(u)=[[epsilon-i, -i],[-i,epsilon-i(1+sqrt(2)u)]].
For u~N(0,1), raw |det(M)^(-1/2)|^2 has a logarithmically
 divergent expectation as epsilon -> 0. Exact conditional quartic
integration has a finite nonzero limit. All numerics are diagnostics,
not interval enclosures.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
import mpmath as mp


def mean_reference(eps: float) -> complex:
    mp.mp.dps=70
    e=mp.mpf(str(eps)); h=e-1j; d=e-1j
    s=d+1/h
    # Re s>0 for eps>0; branch follows the accretive real-cycle Gaussian.
    u=s*s/8
    val=mp.sqrt(s/2)*mp.exp(u)*mp.besselk(mp.mpf(1)/4,u)
    return complex(val/mp.sqrt(2*mp.pi*h))


def second_moment(eps: float) -> tuple[float,float]:
    a=math.sqrt(2.)
    hmod=math.sqrt(1+eps*eps)
    m=eps*(1+1/(1+eps*eps))
    center=-eps*eps/(a*(1+eps*eps))
    cutoff=12.
    lo=math.asinh((-cutoff-center)*a/m)
    hi=math.asinh((cutoff-center)*a/m)
    def integrand(v:float)->float:
        u=center+(m/a)*math.sinh(v)
        return math.exp(-u*u/2)/(a*hmod*math.sqrt(2*math.pi))
    val,err=quad(integrand,lo,hi,epsabs=1e-11,epsrel=1e-11,limit=300)
    # Beyond |u|>=12, denominator >= a*(12-|center|).
    tail=math.erfc(cutoff/math.sqrt(2))/(a*hmod*(cutoff-abs(center)))
    return val,err+tail


def main()->None:
    j0=float(mp.gamma(mp.mpf(1)/4)/(2*mp.sqrt(mp.pi)))
    coefficient=1/math.sqrt(math.pi)
    rows=[]
    for eps in [1e-1,1e-2,1e-3,1e-4,1e-6,1e-8,1e-10,1e-12]:
        mean=mean_reference(eps)
        mom,err=second_moment(eps)
        rows.append(dict(epsilon=eps,conditional_mean=[mean.real,mean.imag],
            abs_conditional_mean=abs(mean),raw_second_moment=mom,
            integration_error_estimate=err,
            raw_relative_variance=mom/abs(mean)**2-1,
            second_moment_minus_leading_log=mom-coefficient*math.log(1/eps)))
    out=dict(status='Analytic logarithmic divergence and bounded conditional mean; numerical verification not interval certified',
      model='A=epsilon I_2; C=[[1,1],[1,1]]; g=1; condition sigma_1=0',
      asymptotic_second_moment_log_coefficient=coefficient,
      limiting_conditional_mean_modulus=j0,
      limiting_mean=[j0/math.sqrt(2),j0/math.sqrt(2)],cases=rows,
      limitation='A two-variable conditional operation, not a global algorithm or a demonstrated superiority over exact block quadrature.')
    Path(__file__).with_name('true_resonance_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
