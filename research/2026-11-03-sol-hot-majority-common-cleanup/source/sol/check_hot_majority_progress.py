#!/usr/bin/env python3
"""Exact checks of the new parity progress and success subsolution.

These finite checks do not prove recurrence or replace the all-integer
algebra in HOT_MAJORITY_COMMON_CLEANUP.md.
"""
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import json

P=Path(__file__).resolve().parent
Y=((0,0,0),(1,1,0),(2,1,1),(3,2,2))

@lru_cache(maxsize=None)
def progress(a,c):
    if a==0:return 0
    if a==1:return 3+4*(c%2)
    if a==2:return 6 if c%2==0 else 2
    if c==0:return 3*a
    if c==1:return 3*a-4
    return 1+progress(a-3,c-2)

def ff(v,k):
    if v<k:return 0
    out=1
    for j in range(k):out*=v-j
    return out

def gen_subsolution(x,h=30):
    # All block constants1, kf2,kb1. K_core=h, p=1/(h+2).
    a,b,c,d,e,f=x;p=Q(1,h+2);F0=progress(a,c)+progress(d,f);g=p**F0
    total=Q(0);positive_core=0
    for port in range(2):
        o=3*port;anchor=x[o];cold=x[o+2]
        for s in range(4):
            rate=1
            for j in range(3):rate*=ff(x[o+j],Y[s][j])
            if not rate:continue
            fail=s==0 or (s in (1,2) and anchor>=3 and cold>=2)
            out=list(x)
            for j in range(3):out[o+j]+=Y[(s+1)%4][j]-Y[s][j]
            gg=Q(0) if fail else p**(progress(out[0],out[2])+progress(out[3],out[5]))
            total+=rate*(gg-g)
    for donor,k in ((0,2),(1,1)):
        o=3*donor;v=3*(1-donor)
        rate=k*a*d*ff(x[o+1],2)*ff(x[o+2],2)
        if not rate:continue
        out=list(x);out[o+1]-=2;out[o+2]-=2;out[v+1]+=2;out[v+2]+=2
        fail=x[o]>=3
        gg=Q(0) if fail else p**(progress(out[0],out[2])+progress(out[3],out[5]))
        total+=rate*(gg-g)
        if not fail:
            assert gg>=g
            positive_core+=1
    assert total>=-2,(x,total)
    return total,positive_core

def main():
    algebra=0;maxremoval=0
    for a in range(101):
        for c in range(201):
            v=progress(a,c)
            assert 0<=v<=3*a+4 and ((v>0)==(a>0))
            assert progress(a,c+2)<=v
            maxremoval=max(maxremoval,v-progress(a,c+2))
            if a<=2:assert progress(a,c+2)==v
            if a and (a<=2 or c<=1):assert progress(a+1,c+1)<=v-1
            if a>=3 and c>=2:assert progress(a-3,c-2)==v-1
            algebra+=1
    raw_cases=0;core_cases=0;minimum=None
    for a in range(6):
        for d in range(6):
            if not(a or d):continue
            for c in range(6):
                for f in range(6):
                    for r1,r2 in ((200,200),(200,10**12),(10**12,200)):
                        value,ncore=gen_subsolution((a,r1+c,c,d,r2+f,f))
                        raw_cases+=1;core_cases+=ncore
                        if minimum is None or value<minimum:minimum=value
    # Exact first-genuine-event witness against the old total-growth service bound.
    witnesses=[]
    n=100
    for N in (10**4,10**8,10**16,10**32):
        x=(3,n+2,2,1,N,0)
        own0=1;own1=3*(n+2);own2=6*(n+2)*2
        term=6*ff(n+2,2)*2;core=2*3*ff(n+2,2)*2
        peer0=1;peer1=N
        prob=Q(peer1,own0+own1+own2+term+core+peer0+peer1)
        witnesses.append({'r1':n,'r2':N,'probability_first_event_peer_low_source1':str(prob),
                          'float':float(prob),'new_progress_change':progress(2,1)-progress(1,0)})
        assert witnesses[-1]['new_progress_change']==-1
    out={'scope':'Exact finite identities and generator subsolution checks; all-integer proof is separate.',
         'algebra_cases':algebra,'largest_packet_removal_cost':maxremoval,
         'raw_generator_cases':raw_cases,'continuing_core_cases':core_cases,
         'minimum_exact_Lg':str(minimum),'required_lower_bound':-2,
         'old_service_scale_witnesses':witnesses}
    (P/'results/hot_majority_progress_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='old_service_scale_witnesses'},indent=2))
    print(json.dumps(witnesses,indent=2))

if __name__=='__main__':main()
