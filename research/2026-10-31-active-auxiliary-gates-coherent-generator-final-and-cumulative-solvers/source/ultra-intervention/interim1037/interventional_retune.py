#!/usr/bin/env python3
"""Keep the failed smooth-limit shortcut; retune the actual finite protocol."""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import sys
import time
import numpy as np
from scipy.optimize import brentq
from interventional_opening import ring,gauge,cycle,OUT


def main():
    start=time.perf_counter();q,pi,labels=ring();other,S,Si=gauge(q,F(1,100))
    p=np.array(list(map(float,pi)));f=np.array(labels);steps=16
    ratios=[F(1+.2*math.cos(2*math.pi*k/steps)).limit_denominator(1000000) for k in range(steps)]
    roots=[];scan=[]
    for name,z in [('source',q),('passive_equivalent',other)]:
        xs=np.geomspace(.015,1,100);ys=[cycle(z,p,f,ratios,float(x))['work_on'] for x in xs]
        crosses=[]
        for x,y,a,b in zip(xs[:-1],xs[1:],ys[:-1],ys[1:]):
            if a*b<0:crosses.append(brentq(lambda t:cycle(z,p,f,ratios,t)['work_on'],x,y,xtol=1e-14))
        roots.append({'name':name,'finite_step_duration_roots':crosses})
        scan.append({'name':name,'min_work_on':min(ys),'max_work_on':max(ys)})
    assert all(r['finite_step_duration_roots'] for r in roots)
    dt=F(sum(x['finite_step_duration_roots'][0] for x in roots)/2).limit_denominator(100000000)
    a=cycle(q,p,f,ratios,dt);b=cycle(other,p,f,ratios,dt)
    assert a['work_on']*b['work_on']<0
    data={'status':'FINITE_CYCLIC_WORK_SIGN_PROPOSAL','floating_only':True,'physical_experiments':0,
          'previous_failed_protocols':'opening_receipt.json: finite staircase did not inherit the smooth-limit sign',
          'Q':[[str(x) for x in row] for row in q],'Q_gauge':[[str(x) for x in row] for row in other],
          'S':[[str(x) for x in row] for row in S],'stationary_pi':list(map(str,pi)),'labels':labels,
          'roots':roots,'scan':scan,'step_duration':str(dt),'field_multipliers':list(map(str,ratios)),
          'source':a,'passive_equivalent':b,'same_actual_control_protocol':True,
          'new_observations':0,'elapsed_wall_seconds':time.perf_counter()-start,
          'not_claimed':['certified work signs before exact enclosure','controller/net-device advantage','new energy source']}
    (OUT/'retuned_receipt.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ['Q','Q_gauge','S','field_multipliers']} ,indent=2))


if __name__=='__main__':main()
