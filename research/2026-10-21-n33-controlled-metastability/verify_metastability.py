#!/usr/bin/env python3
"""N33 follow-on: standard-library exact rational tests; not a stochastic proof."""
from fractions import Fraction as F
from math import comb, exp, log, ceil
import json

lo, hi, ell=F(2,5),F(5,2),F(1,40)
low_edge,upper_edge=lo+ell,hi-ell
kap, K, theta=F(1,2),F(2),F(1,4)
reaction_data=(
    ((0,0,1),(1,0,0)),
    ((2,0,1),(-1,0,0)),
    ((1,1,0),(0,1,0)),
    ((1,3,0),(0,-1,0)),
    ((0,1,1),(0,0,1)),
    ((0,1,3),(0,0,-1)),
)

# Mean-field inward collar lower bounds, including the clock prefactors.
b_low=kap-K*low_edge**2
b_high=kap*upper_edge**2-K
assert b_low==F(111,800) and b_high==F(3401,3200)
gamma=min(lo*b_low,lo**2*b_low,lo*b_high,lo*upper_edge*b_high)
assert gamma==F(111,5000)

# Molecular falling-factorial birth/death favorable ratios (V >= 100).
lower_ratio=1/(4*low_edge**2)
upper_ratio=(upper_edge-F(1,100))*(upper_edge-F(2,100))/4
assert lower_ratio==F(400,289)
assert upper_ratio==F(242063,160000)
assert upper_ratio>lower_ratio

# Bound exp(1/4) using n!>=2*3**(n-2) (n>=2); rational comparison.
exp_up=1+theta+theta**2/(2*(1-theta/3))
assert exp_up==F(113,88)
assert exp_up<F(4,3)<lower_ratio
assert exp_up-1<F(1,3)

# Uniform total rate budget on Q.
Lambda=K*sum(hi**sum(y) for y,nu in reaction_data)
assert Lambda==F(435,2)

# Compare with N33's (much looser) general appendix constant formula.
def factorial_correction(y):
    total=F(0)
    for j,power in enumerate(y):
        if power<2:
            continue
        term=F(comb(power,2))*hi**(power-1)
        for l,p in enumerate(y):
            if j!=l: term*=hi**p
        total+=term
    return total

D=[K*sum(abs(nu[i])*factorial_correction(y) for y,nu in reaction_data) for i in range(3)]
B=[K*sum(nu[i]**2*hi**sum(y) for y,nu in reaction_data) for i in range(3)]
assert D==[F(25,2),F(375,4),F(375,4)]
assert B==[F(145,4),F(725,8),F(725,8)]
v_generic=max(1,*[ceil(2*d/gamma) for d in D])
assert v_generic==8446
rough_theta=[min(F(1), (gamma/2)/(3*b)) for b in B]
assert min(rough_theta)*ell==F(111,108750000)

V=10000
exit_bound=6*exp(-3*V/20)+435*V*exp(-V/320)
assert 0<exit_bound<1.2e-7
result={
  "status":"PASS exact rational constant checks, NOT proof of probability estimate",
  "volume_cutoff":100,
  "lower_ratio":str(lower_ratio),
  "upper_ratio":str(upper_ratio),
  "collar":str(ell),
  "drift_margin":str(gamma),
  "exp_theta_bound":str(exp_up),
  "Lambda":str(Lambda),
  "generic_N33_volume_cutoff":v_generic,
  "exit_bound":"6*exp(-3V/20)+435*V*T*exp(-V/160)",
  "example_V":V,
  "example_T":"exp(V/320)",
  "example_exit_upper":exit_bound,
  "example_horizon_log10":(V/320)/log(10)
}
print(json.dumps(result,indent=2))
