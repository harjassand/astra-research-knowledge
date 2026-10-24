"""Exact rational certificates for DISTRIBUTED_FEJER_RODS.md.

No frequency sampling or floating-point quadrature establishes the claims.
Printed decimal values are convenient renderings of certified rationals.
"""
from fractions import Fraction as F
from math import factorial
import json


def exp_lower(x, order=100):
    return sum((x**j / factorial(j) for j in range(order + 1)), F(0))


def exp_upper(x, order=100):
    # Tail ratios are <=x/(order+2) after the first omitted term.
    assert x < order + 2
    return exp_lower(x, order) + x**(order+1)/factorial(order+1)/(1-x/F(order+2))


def bose_tail_upper(R):
    t = 1/exp_lower(R)
    return t*(R*R+2*R+2)/(1-t)**2


def main():
    m=F(100,101)
    hi,lo=F(23,25),F(21,25)
    acoustic_upper=F(4,5)/(1-9*hi*hi/F(606))-m*hi*hi
    negative_cos_lower=F(20,27)-lo*lo*(m+F(1,101)/(1-9*lo*lo/F(808)))
    assert acoustic_upper < 0 < negative_cos_lower
    # pi>3.14 and sqrt(101)>10.04 imply the first Dirichlet pole exceeds10.5.
    assert F(251,25)**2 < 101
    assert F(157,50)*F(251,25)/3 > F(21,2)
    assert exp_upper(F(1),8) < F(11,4)
    assert (F(11,4)-F(4,11))/2 < F(6,5)
    fejer_upper=F(27,25)+3*bose_tail_upper(F(21,2))
    local_lower=F(25,18)
    assert fejer_upper < F(273,250) < local_lower
    fejer_lower=lo-lo**3/36
    assert fejer_lower == F(102942,125000)  # .823536

    mb=F(1,1000)
    length_ratio=F(2,5)
    k=F(2,5)
    rod_mass=k*length_ratio**2/F(101)
    ms=1-mb-F(1,101)-rod_mass
    left,right=F(13,20),F(29,5)
    denominator_margin=ms*left**2-k
    alpha2=right**2/F(101)
    z_lower=k*(1-length_ratio**2*alpha2/2)-mb*right**2
    needed_upper=alpha2/(1-alpha2/8)
    assert denominator_margin > 0
    assert length_ratio**2*alpha2 < 1  # all trig bounds in their positive range
    assert z_lower > needed_upper
    pendant_upper=left+bose_tail_upper(right)
    assert pendant_upper < F(4,5) < fejer_lower
    assert k*length_ratio == F(4,25) > F(3,20)
    assert mb+ms+F(1,101)+rod_mass == 1

    # Constants in the uniform remainder estimates, with rational pi/sqrt3 bounds.
    pi_upper=F(22,7)
    inv_sqrt3_upper=F(153,265)
    assert F(265,153)**2 < 3
    centre_coefficient=12*pi_upper*(F(1,2)+2*inv_sqrt3_upper)*F(144,143)
    derivative_coefficient=(108+F(81,4)*pi_upper**3)*F(144,143)
    assert centre_coefficient < 64
    assert derivative_coefficient < 768
    # mu<=.01, pi>3 suffice for the stated .06*x_n^2 remainder.
    assert (64*F(1,100)+2304*F(1,100)**2) < F(6,100)*16

    result={
        'exact_rational_assertions':'PASS',
        'fejer_D_at_092_upper':float(acoustic_upper),
        'fejer_D_at_084_negative_cos_lower':float(negative_cos_lower),
        'fejer_J_upper':float(fejer_upper),
        'fejer_J_lower':float(fejer_lower),
        'nearest_rod_J_lower':float(local_lower),
        'pendant_side_point_mass':float(ms),
        'pendant_internal_rod_mass':float(rod_mass),
        'pendant_denominator_margin':float(denominator_margin),
        'pendant_stopband_z_lower':float(z_lower),
        'pendant_stopband_needed_upper':float(needed_upper),
        'pendant_J_upper':float(pendant_upper),
        'uniform_centre_coefficient_upper':float(centre_coefficient),
        'uniform_derivative_coefficient_upper':float(derivative_coefficient),
    }
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
