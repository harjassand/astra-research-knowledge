#!/usr/bin/env python3
"""Symbolic uniform rate bounds and actual multi-inventory return diagnostics.

The universal stopped-cycle proof is analytic. Finite dynamic programming leaves
all unresolved tail mass visible and does not certify a global recurrence claim.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
import json,math
import sympy as sp
from episode_diagnostics import ordered,rate,jump

P=Path(__file__).resolve().parent

def polynomial_bounds():
    x,y,z,k,u,v=sp.symbols('x y z k u v',nonnegative=True)
    K=3+k;a=3+x;b=K+y;c=K+z
    down=a*(a-1)*(a-2)*b*(b-1)*c*(c-1)
    up=1+a*b+a*(a-1)*b*c
    p=sp.Poly(sp.expand(2*down-(K-1)**2*up),x,y,z,k)
    assert all(co>=0 for co in p.coeffs()) and min(p.coeffs())>0
    b0=2+x;c0=2+y;B=b0+1+u;C=c0+v;A=3
    dd=A*(A-1)*(A-2)*B*(B-1)*C*(C-1);uu=1+A*B+A*(A-1)*B*C
    p2=sp.Poly(sp.expand(4*dd-b0*c0*uu),x,y,u,v)
    assert all(co>=0 for co in p2.coeffs()) and min(p2.coeffs())>0
    return {'high_A_rate_bound':{'shift':'a=3+x,b=K+y,c=K+z,K=3+k','polynomial':'2 q_down-(K-1)^2 q_up',
                                  'positive_coefficients':len(p.coeffs()),'minimum_coefficient':str(min(p.coeffs()))},
            'first_overrun_bound':{'shift':'a=3,B=b+1+u,C=c+v,b=2+x,c=2+y',
                                  'polynomial':'4 q_down-b c q_up','positive_coefficients':len(p2.coeffs()),'minimum_coefficient':str(min(p2.coeffs()))}}

def four_jump_split(b,c):
    raw=ordered();front={(0,b,c):F(1)}
    for step in range(3):
        nxt=defaultdict(F)
        for state,p in front.items():
            rr=[rate(state,y,k) for y,z,k in raw];q=sum(rr)
            for e,r in zip(raw,rr):
                if r:nxt[jump(state,e)]+=p*r/q
        front=nxt
    assert all(s[0]==3 for s in front) and sum(front.values())==1
    overrun=F(0)
    for state,p in front.items():
        rr=[rate(state,y,k) for y,z,k in raw];q=sum(rr);overrun+=p*sum(rr[:3])/q
    state=(0,b,c);p=F(1)
    for i in [0,1,1,3]:
        rr=[rate(state,y,k) for y,z,k in raw];p*=rr[i]/sum(rr);state=jump(state,raw[i])
    assert state==(0,b-1,c) and p>=F(1,16*c) and overrun<=F(4,b*c)
    return {'negative_word_probability_exact':str(p),'negative_word_lower_exact':str(F(1,16*c)),
            'first_overrun_probability_exact':str(overrun),'first_overrun_upper_exact':str(F(4,b*c))}

def actual_return_dp(b,c,K=3,theta=0.1,maxsteps=24):
    raw=ordered();active={(0,b,c):1.0};endmass=0.0;increment=0.0;steps_reward=0.0
    expected_time_partial=0.0;states_peak=1
    for step in range(1,maxsteps+1):
        nxt=defaultdict(float)
        for state,p in active.items():
            rr=[int(rate(state,y,k)) for y,z,k in raw];q=sum(rr)
            expected_time_partial+=p/q
            steps_reward+=p*math.exp(theta*(sum(state)-b-c))/q
            for e,r in zip(raw,rr):
                if not r:continue
                dst=jump(state,e);pp=p*r/q
                if dst[0]==0 or dst[1]<K or dst[2]<K:
                    energy=sum(dst) if dst[0] else dst[1]+dst[2]
                    increment+=pp*math.expm1(theta*(energy-b-c));endmass+=pp
                else:nxt[dst]+=pp
        active=nxt;states_peak=max(states_peak,len(active))
    remainder=sum(active.values())
    assert abs(endmass+remainder-1)<1e-12
    return {'b':b,'c':c,'stop_strip_K':K,'theta':theta,'jump_cutoff':maxsteps,
            'terminated_probability':endmass,'unresolved_tail_probability':remainder,
            'partial_output_increment_relative':increment,'physical_time_partial':expected_time_partial,
            'physical_exp_reward_partial_relative':steps_reward,'peak_actual_states':states_peak,
            'scope':'Actual raw-count deterministic finite-jump diagnostic; unresolved tail retained; theta-dependent universal K of the analytic theorem is not asserted here.'}

if __name__=='__main__':
    symbolic=polynomial_bounds();rows=[]
    for b,c in [(12,12),(12,10**6),(10**6,12),(120,120),(120,10**6),(10**6,120)]:
        row={**actual_return_dp(b,c),**four_jump_split(b,c)};rows.append(row)
        print(b,c,'partial increment',row['partial_output_increment_relative'],'tail mass',row['unresolved_tail_probability'],flush=True)
    out={'scope':'Two uniform raw-rate inequalities certified by exact shifted polynomial positivity; finite actual return diagnostics have separate truncation scope.',
         'symbolic_bounds':symbolic,'return_diagnostics':rows}
    (P/'results/activation_cycle_checks.json').write_text(json.dumps(out,indent=2)+'\n')
