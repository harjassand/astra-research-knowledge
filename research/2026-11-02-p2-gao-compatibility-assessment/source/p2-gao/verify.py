#!/usr/bin/env python3
"""Astra P2 Gao source-compatible exact countermodel and external-input test.
No inferred material rate is represented as an experimental observation.
Python stdlib only; run python verify.py.
"""
from fractions import Fraction as F
from math import log
FARADAY=96485.33212
Q=0.2*2*5
N=round(500*3600/10)
print("500h cycles",N,"reduction charge/pulse",Q)
for fe in (0.60,0.01):
    methane=Q*fe/(8*FARADAY)
    hydrogen=Q*(1-fe)/(2*FARADAY)
    assert abs((8*methane+2*hydrogen)*FARADAY-Q)<1e-12
    print("CH4 FE",fe,"methane umol",methane*1e6,"H2 umol",hydrogen*1e6)
print("reduction-only MJ per mol CH4 at FE=.60, V=3.9",8*FARADAY*3.9/.60/1e6)
print("LHV-to-reduction-only energy",55.5e6*.016043/(8*FARADAY*3.9/.60))
lim=1-0.9**(1/N)
print("90percent Cu retention: max net relative loss/cycle",lim)
print("hypothetical lambda=1e-5: required recovery fraction",1-lim/1e-5)
for r in (0,.9,.95,.99):
    print("hypothetical recovery",r,"fraction Cu remaining",(1-1e-5*(1-r))**N)
# pi(A|O_past) and q(A|O_past) are EXTERNAL randomized commands.
# Kernel K is shared but hidden modes may change as a result of each command.
def action(policy,obs):
    if policy=="base":return {0:F(1,2),1:F(1,2)}
    return ({0:F(1,4),1:F(3,4)} if obs==0
            else {0:F(3,4),1:F(1,4)})
def transition(hidden,a):
    p=F(1,5) if a else F(1,10)
    return {hidden:1-p,1-hidden:p}
def product(hidden,a):
    p={(0,0):F(1,5),(0,1):F(1,2),
       (1,0):F(2,5),(1,1):F(4,5)}[(hidden,a)]
    return {0:1-p,1:p}
def distribution(policy):
    states=[(h,0,F(3,4) if h==0 else F(1,4),F(1)) for h in (0,1)]
    for _ in range(2):
        new=[]
        for h,previous,mass,L in states:
            for a,pa in action(policy,previous).items():
                for hn,ph in transition(h,a).items():
                    for y,py in product(hn,a).items():
                        LR=action("alt",previous)[a]/action("base",previous)[a]
                        new.append((hn,y,mass*pa*ph*py,L*LR))
        states=new
    assert sum(x[2] for x in states)==1
    return states
P=distribution("base"); Qalt=distribution("alt")
e_base=sum(m*y for h,y,m,L in P)
e_alt=sum(m*y for h,y,m,L in Qalt)
assert e_alt==sum(m*L*y for h,y,m,L in P)
print("Exact external-command causal identity",str(e_base),str(e_alt),"PASS")
