#!/usr/bin/env python3
"""Independent high-precision evaluation, NOT a replacement for the proof.

Counts stay integer. All twelve species-level jumps are separately encoded;
neutral coordinates and roots are reconstructed after each actual jump.
"""
from fractions import Fraction
from itertools import product
import json
import random
from pathlib import Path
import mpmath as mp

mp.mp.dps = 100
a=mp.mpf(1)/100
q=mp.mpf(2)
epsilon=mp.mpf(20)

def coords(x):
    A,B,C,D,E=x
    return A+C,A+D,mp.mpf(B-A-99*E)/100

def root(x, guess=None):
    c,d,H=coords(x)
    if H<=0: return mp.mpf(0)
    if guess is None:
        guess=min(mp.root(3*H/q,3),H/(q*c*d)) if c*d else mp.root(3*H/q,3)
    t=mp.mpf(guess)
    for _ in range(150):
        residual=q*t*(c*d+(c+d)*t/2+t*t/3)-H
        dt=residual/(q*(c+t)*(d+t))
        new=t-dt
        if new<=0: new=t/2
        if abs(new-t)<=mp.mpf('1e-85')*max(1,abs(new)):
            t=new
            break
        t=new
    residual=q*t*(c*d+(c+d)*t/2+t*t/3)-H
    assert abs(residual)<=mp.mpf('1e-75')*max(1,H), (x,t,residual)
    return t

REACTIONS=[
 ('birth',(1,0,0,0,0),lambda A,B,C,D,E:1),
 ('death',(-1,0,0,0,0),lambda A,B,C,D,E:A),
 ('2A_to_AC',(-1,0,1,0,0),lambda A,B,C,D,E:A*(A-1)),
 ('AC_to_2A',(1,0,-1,0,0),lambda A,B,C,D,E:A*C),
 ('2A_to_AD',(-1,0,0,1,0),lambda A,B,C,D,E:A*(A-1)),
 ('AD_to_2A',(1,0,0,-1,0),lambda A,B,C,D,E:A*D),
 ('2A_to_AE',(-1,0,0,0,1),lambda A,B,C,D,E:A*(A-1)),
 ('AE_to_2A',(1,0,0,0,-1),lambda A,B,C,D,E:A*E),
 ('AE_to_CD',(-1,0,1,1,-1),lambda A,B,C,D,E:A*E),
 ('CD_to_AE',(1,0,-1,-1,1),lambda A,B,C,D,E:2*C*D),
 ('CD_to_AB',(1,1,-1,-1,0),lambda A,B,C,D,E:C*D),
 ('AB_to_CD',(-1,-1,1,1,0),lambda A,B,C,D,E:A*B),
]

def evaluate(x,r,guess=None):
    t=root(x,guess)
    A,B,C,D,E=x
    c,d,_=coords(x)
    p=mp.mpf(A*A)/(B+1)
    h=1+epsilon*p
    log_r=mp.log(r)
    terms={}
    for name,jump,rate_fn in REACTIONS:
        rate=rate_fn(*x)
        if not rate: continue
        y=tuple(v+w for v,w in zip(x,jump))
        assert min(y)>=0
        ty=root(y,t)
        py=mp.mpf(y[0]*y[0])/(y[1]+1)
        z=ty-t+sum(jump)*log_r
        terms[name]=mp.mpf(rate)*(mp.expm1(z)+mp.exp(z)*epsilon*(py-p)/h)
    drift=mp.fsum(terms.values())
    asserted=-(mp.mpf(3)/20+10*A*A+t/4*(mp.mpf(A*C)/(d+t+1)+mp.mpf(A*D)/(c+t+1)))
    margin=asserted-drift
    return t,drift,asserted,margin,terms

def construct(A,C,D,E,target):
    target=Fraction(target)
    c,d=A+C,A+D
    H=2*(c*d*target+(c+d)*target*target/2+target**3/3)
    desired=Fraction(A+99*E)+100*H
    B=-(-desired.numerator//desired.denominator)
    return (A,B,C,D,E)

def main():
    rng=random.Random(20261101)
    states=[]
    scales=[0,1,2,10,10**3,10**9,10**18]
    for A in [0,1,2,10,10**6]:
        for C,D in product(scales,repeat=2):
            for target in [2,3,102]:
                E=[0,1,10**6,10**24][(A+C+D+int(target))%4]
                states.append((construct(A,C,D,E,target),target))
    for _ in range(180):
        A=rng.choice(scales)
        C=rng.choice(scales)
        D=rng.choice(scales)
        E=rng.choice(scales+[10**30])
        target=Fraction(rng.choice([2000,2001,2500,5000,1000000]),1000)
        states.append((construct(A,C,D,E,target),target))
    worst=None
    largest_drift=None
    count=0
    for x,target in states:
        for r in [mp.mpf('1.01'),mp.mpf('1.000000000001')]:
            t,drift,asserted,margin,terms=evaluate(x,r,mp.mpf(target.numerator)/target.denominator if isinstance(target,Fraction) else target)
            assert t>=2
            assert margin>=-mp.mpf('1e-50'), (x,t,r,drift,asserted,terms)
            row={'state':x,'tau':mp.nstr(t,30),'r':str(r),'LV_over_V':mp.nstr(drift,30),'theorem_upper_bound':mp.nstr(asserted,30),'margin':mp.nstr(margin,30),'terms':{k:mp.nstr(v,30) for k,v in terms.items()}}
            if worst is None or margin<worst[0]: worst=(margin,row)
            if largest_drift is None or drift>largest_drift[0]: largest_drift=(drift,row)
            count+=1
    out={'arithmetic':'mpmath 100 decimal digits','state_tilt_cases':count,'all_pass':True,'minimum_certificate_margin_case':worst[1],'largest_LV_over_V_case':largest_drift[1],'scope':'Numerical stress validation only; analytic proof in the two certificate markdown files.'}
    dest=Path(__file__).with_name('EXACT_GENERATOR_VALIDATION.json')
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
