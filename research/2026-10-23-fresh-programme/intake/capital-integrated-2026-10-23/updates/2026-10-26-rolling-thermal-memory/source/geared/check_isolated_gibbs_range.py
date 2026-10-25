"""Exact conservative finite point for the FULL isolated Gibbs range theorem.

This verifies rational decisions using the analytic all-mode inequalities,
not a thermal-state truncation, bath draw or material implementation.
"""

import sys
sys.dont_write_bytecode=True
from fractions import Fraction as F
from math import factorial
import json
from check_compact_amplifier import i0_bounds, decimal_bound, ROUND_CEILING


def main():
    g=F(1000); B=1+g*g; recoil=B/2; b=F(6)
    beta=B; q2=g*g/(B*B)
    i0_lower,_=i0_bounds(b)
    zeta_upper=(B-1)/(i0_lower*i0_lower)
    assert zeta_upper<F(1,100)
    # pi^2<10, pi^4<100: this is a conservative sufficient flux window.
    assert F(22,7)**2<10
    assert q2<1/(64*100*(b+1))
    metric_upper=4*100*g*g/(B*B)*(b+q2)
    # Drop the negative -2/pi^2 in <P^2>, use pi^2/4<10/4.
    trial_upper=((1+zeta_upper)/3+F(10,4)+metric_upper)/2
    assert trial_upper<F(3,2)
    # ln3<2 and ln4<3/2, certified by finite positive exp partial sums.
    assert sum(F(2)**n/factorial(n) for n in range(3))>3
    assert sum(F(3,2)**n/factorial(n) for n in range(4))>4
    normal_threshold=2+10*(b+2)
    assert normal_threshold==82 and beta*recoil>normal_threshold
    variance_upper=4*trial_upper+6
    assert variance_upper<12
    # Independent exact aperture constants for the explicit response stock.
    assert F(19,12)*F(22,7)**2-8<8
    assert F(7,132)-F(1,192)>F(1,25)
    assert F(1,25)-F(1,400)==F(3,80)
    assert F(3,80)-F(1,200)>F(1,40)
    return dict(status='PASS exact full-isolated-Gibbs finite-point constants',
                B=str(B),beta=str(beta),spring=str(1/B),
                normal_threshold=str(normal_threshold),
                trial_energy_times_B_upper=decimal_bound(trial_upper,ROUND_CEILING),
                full_Gibbs_variance_upper=decimal_bound(variance_upper,ROUND_CEILING),
                certified_full_Gibbs_variance_lt='12',
                scope='isolated full canonical Gibbs model; no live-lead heat or state acquisition')


if __name__=='__main__': print(json.dumps(main(),indent=2))
