"""Exact helical-locking algebra and a rigorously bounded finite response point.

Default: rational canonical completion, exact positive ground-state identity,
positive Bessel-series enclosures and two opposite fixed-resource conclusions.
--diagnostic: optional Fourier rotor challenge; not material or heat data.
"""

from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
import json
import sys


def decimal_bound(value,rounding):
    with localcontext() as context:
        context.prec=22; context.rounding=rounding
        return str(Decimal(value.numerator)/Decimal(value.denominator))


def enclosure(lo,hi):
    return [decimal_bound(lo,ROUND_FLOOR),decimal_bound(hi,ROUND_CEILING)]


def i0_bounds(b,terms=100):
    # I0(2b)=sum b^(2n)/(n!)^2, all positive.
    value=F(1); total=value
    for n in range(1,terms+1):
        value*=b*b/(n*n); total+=value
    following=value*b*b/(terms+1)**2
    ratio=b*b/(terms+2)**2
    assert ratio<1
    return total,total+following/(1-ratio)


def exact():
    B0=F(3,2); I=F(5,4); g=F(7,3); P=F(2,7); L=F(-4,5)
    B=B0+I*g*g; perpendicular=B0*I/B
    original=(P-g*L)**2/(2*B0)+L*L/(2*I)
    completed=P*P/(2*B)+(L-g*I*P/B)**2/(2*perpendicular)
    assert original==completed
    # -psi''/psi + V_b/E_R equals b as a polynomial in cos(phi).
    b=F(6)
    coefficients=[-b*b+b*b+b,b-b,b*b-b*b]
    assert coefficients==[b,0,0]
    # One finite attainer, hbar=B0=I=1, g=1000: ideal B=1,000,001.
    g=F(1000); B0=I=F(1); B=1+g*g; recoil=B/2
    lo_i,hi_i=i0_bounds(b)
    f_lo=1/(hi_i*hi_i); f_hi=1/(lo_i*lo_i)
    ratio_lo=1/(1+(B-1)*f_hi)
    ratio_hi=1/(1+(B-1)*f_lo)
    assert ratio_lo>F(99,100)
    # The SAME geometric masses/gain with ANY lock of barrier<=1 has Beff<1.01.
    # sqrt(1/E_R)<3/2000, pi<22/7, exp x<=1/(1-x) for0<=x<1.
    assert 1/recoil<F(3,2000)**2
    exponent_upper=2*F(22,7)*F(3,2000)
    bare_ratio_upper=1/(1-exponent_upper)
    assert bare_ratio_upper<F(101,100)
    return dict(status='PASS exact canonical/locking/resource checks',
                ideal_relative_inertia=str(B),
                attainer=dict(b=str(b),f=enclosure(f_lo,f_hi),
                              B_eff_over_ideal=enclosure(ratio_lo,ratio_hi),
                              certified_B_eff_over_ideal_gt='99/100',
                              barrier_upper=str(recoil*(b*b+2*b)),
                              reference_ground_energy=str(recoil*b),
                              force_capacity_upper=str(g*recoil*(b*b+b)),
                              curvature_capacity_upper=str(g*g*recoil*(2*b*b+b))),
                fixed_barrier_le1=dict(certified_B_eff_over_bare_lt='101/100',
                                      rational_upper=str(bare_ratio_upper)),
                scope='exact rigid-rotor ground-band response, not full contact heat')


def diagnostic():
    import math
    import numpy as np
    n=np.arange(-35,36,dtype=float); size=len(n)
    angles=np.arange(4096)*2*math.pi/4096
    rows=[]
    for b in (.5,1.,3.):
        h=np.diag(n*n+b*b/2+b)
        h+=np.diag(np.full(size-1,-b/2),1)+np.diag(np.full(size-1,-b/2),-1)
        h+=np.diag(np.full(size-2,-b*b/4),2)+np.diag(np.full(size-2,-b*b/4),-2)
        energies,vectors=np.linalg.eigh(h)
        ground=vectors[:,0]
        wave=ground@np.exp(1j*n[:,None]*angles[None,:])
        phase_f=1/(np.mean(abs(wave)**2)*np.mean(abs(wave)**-2))
        exact_f=1/np.i0(2*b)**2
        matrix_elements=vectors[:,1:].conj().T@(n*ground)
        spectral_f=1-4*np.sum(abs(matrix_elements)**2/(energies[1:]-energies[0]))
        assert abs(energies[0]-b)<1e-11
        assert abs(phase_f/exact_f-1)<1e-7
        assert abs(spectral_f-exact_f)<1e-10
        rows.append(dict(b=b,ground_energy_error=float(abs(energies[0]-b)),
                         exact_f=float(exact_f),density_f=float(phase_f),
                         spectral_curvature_f=float(spectral_f)))
    return dict(scope='floating finite Fourier challenge only',harmonics=35,rows=rows)


if __name__=='__main__':
    result=exact()
    if '--diagnostic' in sys.argv: result['diagnostic']=diagnostic()
    print(json.dumps(result,indent=2))
