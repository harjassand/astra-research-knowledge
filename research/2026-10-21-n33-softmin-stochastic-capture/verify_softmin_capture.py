#!/usr/bin/env python3
"""N33 softmin capture: exact rational checks plus deterministic rate-corner scans.

Arithmetic and finite grids are NOT a proof of the general probability
inequality, the full all-network theorem, or external historical priority.
"""
from fractions import Fraction as Q
from math import ceil, floor, exp, factorial, log
import json

beta=20
L0,U0=Q(1,4),Q(3)
Ltarget,Utarget=Q(1,5),Q(61,20)
Lguard,Uguard=Q(1,16),Q(5)
Vmin,T=1200,8
assert Lguard<Ltarget<L0<U0<Utarget<Uguard
e_lower=sum(Q(1,factorial(k)) for k in range(4))
e5_partial=sum(Q(5)**k/factorial(k) for k in range(7))
assert e_lower==Q(8,3) and e5_partial>100
slope=(e_lower-Q(1,100))/(1+e_lower+Q(1,100))
assert slope==Q(797,1103) and slope>Q(7,10)
assert Q(7,10)*Q(3,5)>Q(2,5)
assert Q(7,10)*Q(21,20)>Q(2,5)
assert beta*Q(12,2)/Vmin==Q(1,10)
assert Q(2,5)-Q(120,Vmin)==Q(3,10)

theta=Q(1,4)
E=1/(1-theta)
assert E==Q(4,3)
left_margin=1-E*2*(Lguard+Q(1,64))
right_margin=(Uguard-Q(1,4))-E*2
assert left_margin==Q(19,24) and right_margin==Q(25,12)
assert theta*Q(1,64)==Q(1,256)
assert theta*(Q(1,10)-Lguard)==Q(3,320)
assert 2*12*(E-1)==8
assert exp(2)>3
assert (Q(3,10)*T)-(Q(1)+Q(2,20))>=1
assert 1/Q(2*(12*T+Q(1,3)))==Q(3,578)

# Rationally certified operational-clock thresholds for attributed 3D fixture.
e13over5=sum(Q(13,5)**k/factorial(k) for k in range(6))
assert e13over5>Q(38,3), "time 13 a-coordinate buffer"
assert e5_partial>Q(1944,19), "five operational clock units"
assert Q(9,20)*12>5, "time 25 then 37 buffering"

def soft(x):
    a=exp(-20*(x-.25))
    b=exp(-20*(3-x))
    return -log(1+a+b)/20

grid={}
for V in (1200,10000):
    minimum=float("inf")
    arg=None
    tested=0
    for count in range(ceil(float(Lguard)*V),floor(float(Uguard)*V)+1):
        x=count/V
        if float(Ltarget)<=x<=float(Utarget):
            continue
        v=soft(x)
        up=V*(soft(x+1/V)-v)
        down=V*x*(soft(x-1/V)-v)
        for kin in (1,2):
            for kout in (1,2):
                g=kin*up+kout*down
                if g<minimum: minimum,arg=g,(count,kin,kout)
                tested+=1
    assert minimum>0.3-1e-7
    grid[str(V)]={"tested_rate_corners":tested,"min_generator":minimum,"argmin_count_kin_kout":arg}

out={
"status":"PASS rational sufficient inequalities and two finite rate-corner scans",
"network":"0 -> A and A -> 0, each predictable rate in [1,2]",
"initial_range":"[1/10,4]","guard":"[1/16,5]",
"capture_range":"[1/5,61/20]","deadline":8,
"min_volume":1200,"softmin_beta":20,
"generator_drift_lower":"3/10 outside capture inside guard",
"guard_margins":[str(left_margin),str(right_margin)],
"exit_bound":"exp(-3V/578)+2exp(-3V/320)+64Vexp(-V/256)",
"bound_at_5000":exp(-3*5000/578)+2*exp(-3*5000/320)+64*5000*exp(-5000/256),
"bound_at_10000":exp(-3*10000/578)+2*exp(-3*10000/320)+64*10000*exp(-10000/256),
"3D_deterministic_fixture":"[1/10,10]^3 enters [9/20,9/4]^3 by t=37",
"grid":grid,
"scope":"Checks algebra and challenges specific generator; not stochastic martingale proof or historical novelty."
}
print(json.dumps(out,indent=2))
