#!/usr/bin/env python3
"""Exact finite checks of the all-hidden normal-resource cap.

The all-state result is algebraic in JOINT_NORMAL_RESOURCE_CAP.md. This
also replays a genuine neutral debt loop, so strict-progress failure is
not confused with an inward/recurrence claim.
"""
from functools import lru_cache
from pathlib import Path
from fractions import Fraction as Q
import json

P=Path(__file__).resolve().parent
Y=((0,0,0),(1,1,0),(2,1,1),(3,2,2))

@lru_cache(maxsize=None)
def w(a,b):
    if a==0:return 0
    if a==1:return b%2
    if a==2:return -(b%2)
    if b==0:return 0
    if b==1:return -1
    return w(a-3,b-2)-2

@lru_cache(maxsize=None)
def v(a,b):
    if a==0:return 0
    if a==1:return 0
    if a==2:return -1
    if b==0:return 0
    if b==1:return -1
    return v(a-3,b-2)-2

def continuing(a,b,source):
    return ((source==0 and a>=1 and (a==1 or b==0))
            or (source==1 and a==1)
            or (source==2 and a>=2 and (a==2 or b==1))
            or source==3)

def resources(x):
    a,b,c,d,e,f=x
    return (b+e+w(a,b)+w(d,e),c+f+v(a,b)+v(d,e))

def replay():
    x=[1,0,100,1,2,200];initial=tuple(x)
    word=('COREb','I1','COREf','I0','I2','I3');rows=[]
    for label in word:
        before=tuple(x);r0=resources(before)
        if label.startswith('CORE'):
            donor=1 if label=='COREb' else 0;o=3*donor;t=3*(1-donor)
            assert x[o]<=2 and x[0]*x[3] and x[o+1]>=2 and x[o+2]>=2
            x[o+1]-=2;x[o+2]-=2;x[t+1]+=2;x[t+2]+=2
        else:
            s=int(label[-1]);assert continuing(x[0],x[1],s)
            assert all(x[k]>=Y[s][k] for k in range(3))
            for k in range(3):x[k]+=Y[(s+1)%4][k]-Y[s][k]
        assert resources(x)==r0
        rows.append({'label':label,'before':before,'after':tuple(x),'resources':r0})
    assert tuple(x)==initial
    return {'initial':initial,'rows':rows,'final':x,'exactly_neutral':True}

def main():
    states=transitions=0;changes=set();worst_removal_w=worst_removal_v=0
    for a in range(101):
        for b in range(201):
            ww,vv=w(a,b),v(a,b)
            assert -Q(2,3)*a-1<=ww<=1
            assert -Q(2,3)*a-1<=vv<=0
            assert w(a,b+2)<=ww and v(a,b+2)<=vv
            worst_removal_w=max(worst_removal_w,ww-w(a,b+2))
            worst_removal_v=max(worst_removal_v,vv-v(a,b+2))
            if a<=2:assert w(a,b+2)==ww and v(a,b+2)==vv
            for c in range(4):
                for s in range(4):
                    if not continuing(a,b,s) or any(t<r for t,r in zip((a,b,c),Y[s])):continue
                    out=tuple(t+u-r for t,u,r in zip((a,b,c),Y[(s+1)%4],Y[s]))
                    aa,bb,cc=out
                    dw=bb-b+w(aa,bb)-ww;dv=cc-c+v(aa,bb)-vv
                    assert dw<=0 and dv<=0,(a,b,c,s,out,dw,dv)
                    changes.add((s,dw,dv));transitions+=1
            states+=1
    result={'scope':'Exact finite raw resource/transport checks and a physical neutral loop. Not an inward-drift or recurrence proof.',
            'state_cases':states,'enabled_continuing_reaction_cases':transitions,
            'observed_source_resource_changes':sorted(changes),
            'largest_packet_removal_w':worst_removal_w,'largest_packet_removal_v':worst_removal_v,
            'neutral_word':replay()}
    (P/'results/joint_resource_cap_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='neutral_word'},indent=2))
    print(json.dumps({'exact_neutral_loop':result['neutral_word']['exactly_neutral'],
                      'initial_and_final':result['neutral_word']['initial']},indent=2))

if __name__=='__main__':main()
