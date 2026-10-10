#!/usr/bin/env python3
"""Exact two-level clock check in Q[zeta_256], using zeta_256^128 = -1.
No floating-point approximation and no general-theorem certification.
"""
from pathlib import Path
import json
from collections import defaultdict
from fractions import Fraction as Q

N=256
HALF=N//2

def mono(k,c=1):
    k%=N
    if k>=HALF: return {k-HALF:-c} if c else {}
    return {k:c} if c else {}

def add(a,b):
    out=dict(a)
    for k,v in b.items():
        out[k]=out.get(k,0)+v
        if not out[k]: del out[k]
    return out

def mul(a,b):
    out=defaultdict(int)
    for i,v in a.items():
        for j,w in b.items():
            k=i+j
            if k>=HALF: out[k-HALF]-=v*w
            else: out[k]+=v*w
    return {k:v for k,v in out.items() if v}

ONE={0:1}
levels=[]
P=2; T=1
for power in [64,1]:
    Nj=2**P
    assert N % Nj == 0 and power==N//Nj
    zeta=mono(power)
    levels.append({'x':ONE,'y':ONE,'a':{},'z':0,'zeta':zeta,'N':Nj,'old_period':P})
    P,T=P*Nj,T+1+Nj*P
expected=[{'period':8,'first_pulse':10},{'period':2048,'first_pulse':2059}]
b=0
pulses=[[],[]]
max_terms=0
for t in range(3*P+1):
    assert b in (0,1)
    for j,L in enumerate(levels):
        if L['z']:
            pulses[j].append(t)
        assert L['z'] in (0,1)
    if t==3*P: break
    old_pulses=[b]+[L['z'] for L in levels[:-1]]
    new=[]
    for L,pulse in zip(levels,old_pulses):
        total={k:Q(v,2) for k,v in mul(L['a'],add(ONE,L['y'])).items()}
        zn=0
        if pulse:
            assert not total or total==ONE,total
            zn=1 if total else 0
        xn=mul(L['zeta'],L['x']) if pulse else L['x']
        yn=xn if pulse else mul(L['y'],L['y'])
        an=ONE if pulse else total
        new.append({**L,'x':xn,'y':yn,'a':an,'z':zn})
        max_terms=max(max_terms,len(an))
    b=1-b
    levels=new
for got,ex in zip(pulses,expected):
    want=list(range(ex['first_pulse'],3*P+1,ex['period']))
    assert got==want,(got,want)
record={'scope':'Exact two-level algebraic-coefficient sanity check only','field':'Q(zeta_256), with minimal polynomial x^128+1','levels':2,'dimension_complex_coordinates':9,'maximum_coordinate_degree':3,'output_degree':1,'steps_checked':3*P,'periods':[x['period'] for x in expected],'first_pulse_indices':[x['first_pulse'] for x in expected],'top_level_pulses':pulses[-1],'max_accumulator_terms':max_terms,'checks_passed':True}
Path(__file__).with_name('nested_clock_checks.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
