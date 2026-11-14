#!/usr/bin/env python3
"""Exact rational algebra for spatial N33 stochastic first-exit certificate.

Checks arithmetic, not the stopped counting-process proof, novelty, or an experiment.
Only Python standard library is used.
"""
from fractions import Fraction as F
from math import exp, log
import json

L, U, ell=F(2,5), F(5,2), F(1,40)
up_low=L+ell
low_high=U-ell
D=F(1,4)
theta=F(1,12)
E=1/(1-theta)
assert E==F(12,11)
# Scalar Taylor bound exp(theta) <= 1/(1-theta).
assert float(E)>exp(float(theta))
Vmin=100

# Six integer-complex reactions: (source,target,moving_species,change)
edges=[
((0,0,1),(1,0,1),0,1),
((2,0,1),(1,0,1),0,-1),
((1,1,0),(1,2,0),1,1),
((1,3,0),(1,2,0),1,-1),
((0,1,1),(0,1,2),2,1),
((0,1,3),(0,1,2),2,-1)
]
for y,yp,i,di in edges:
    assert tuple(yp[j]-y[j] for j in range(3))==tuple(di if j==i else 0 for j in range(3))

# Lower collar for any of A,B,C: clock q >= L^2.
lower_base=F(1,2)-2*E*up_low**2
lower_transport=D*(E*up_low-L)
lower_margin=L**2*lower_base-lower_transport
assert lower_base==F(233,2200)
assert lower_transport==F(7,440)
assert lower_margin==F(57,55000)>0

# Upper collar A has q=c >=L and death q*u*(u-1/V).
# Upper collar B/C has q>=L*low_high and death q*(u-1/V)*(u-2/V).
upper_transport=D*(E*U-low_high)
upper_A=L*(F(1,2)*low_high*(low_high-F(1,Vmin))-2*E)-upper_transport
upper_BC=(L*low_high)*(F(1,2)*(low_high-F(1,Vmin))*(low_high-F(2,Vmin))-2*E)-upper_transport
assert upper_A==F(125127,440000)>0
assert upper_BC==F(67976607,88000000)>0

# Reaction event intensity affecting one coordinate/site (scaled by V).
lambda_A=2*(U+U**3)
lambda_BC=2*(U**2+U**4)
lambda_facet=max(lambda_A,lambda_BC)+2*D*U
assert lambda_A==F(145,4)
assert lambda_BC==F(725,8)
assert lambda_facet==F(735,8)

# Test functions exp(-theta V g), six site-faces per compartment.
b0=theta*(1-L)
cstar=theta*ell
coef=6*lambda_facet*(E-1)
assert b0==F(1,20)
assert cstar==F(1,480)
assert coef==F(2205,44)

V=30000;n=100
Tlog=V/960
risk=6*n*exp(-V/20)+float(coef)*n*V*exp(-V/960)
assert 0<risk<1e-5
print(json.dumps({
    "status":"PASS exact rational sufficient inequalities",
    "network":"six reactions, three species, unequal balanced migration",
    "range_reactions":"[1/2,2]",
    "transport_species_node_budget":str(D),
    "volume_cutoff":Vmin,
    "collar":str(ell),
    "theta":str(theta),
    "exp_theta_rational_majorant":str(E),
    "lower_margin":str(lower_margin),
    "upper_A_margin":str(upper_A),
    "upper_BC_margin":str(upper_BC),
    "max_facet_scaled_hazard":str(lambda_facet),
    "exponent_initial":str(b0),
    "exponent_outside_collar":str(cstar),
    "prefactor":str(coef),
    "bound":"P(exit<=T) <= 6*n*exp(-V/20)+(2205/44)*n*V*T*exp(-V/480)",
    "example_n":n,
    "example_V":V,
    "example_T":"exp(V/960)",
    "example_log10_T":Tlog/log(10),
    "example_risk_bound":risk,
    "scope":"arithmetic check, not martingale proof, Lean certification or priority review"
},indent=2))
