#!/usr/bin/env python3
"""Exact checks of the new GLOBAL unit-rate service receiver and source bounds.

The all-state proof is in GLOBAL_SERVICE_RECEIVER.md; finite checks only
test the formulas and the competing-service accounting.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
from check_dynamic_packet_identity import profile,packets,energy
from check_monotone_anchor_receiver import ff,block

P=Path(__file__).resolve().parent
R=Q(100);C=Q(100);RATES=(Q(1),)*4

def W(x):
    a,b,c,d,e,f=x;j1,j2=packets(x);v1,v2=profile(a,d);s=b+c+e+f
    return a*a+d*d-j1*v1-j2*v2+R*s*s

def main():
    anchors=(0,1,2,3,4,5,6,10,100,1000000);profilechecks=0
    for a,d in product(anchors,repeat=2):
        old=profile(a,d);new=profile(a+1,d)
        assert new[0]-old[0]<=C
        assert old[0]-new[0]<=C*(1+a)
        assert abs(new[1]-old[1])<=C
        old=profile(a,d);new=profile(a,d+1)
        assert new[1]-old[1]<=C
        assert old[1]-new[1]<=C*(1+d)
        assert abs(new[0]-old[0])<=C
        profilechecks+=2
    # Crossover pairs are essential, not only fixed-ratio rays.
    for a in (3,10,100,1000,1000000):
        for d in (a*a,2*a*a,10*a*a):
            v=profile(a,d);vv=profile(a+1,d)
            assert vv[0]-v[0]<=C and v[0]-vv[0]<=C*(1+a)
            assert abs(vv[1]-v[1])<=C;profilechecks+=1
    checks=readychecks=0;worst=None
    for a,d in product(anchors,repeat=2):
        for b,c,e,f in product((0,1,2,3,100),repeat=4):
            x=(a,b,c,d,e,f);s=b+c+e+f;v0=W(x);qterm=Q(0);gen=Q(0)
            assert v0>=Q((a+d)**2,4)+s*s
            for off in (0,3):
                loc=x[off:off+3]
                rate=ff(loc,(3,2,2))
                if rate:
                    z=list(x);z[off]-=3;z[off+1]-=2;z[off+2]-=2
                    qterm+=rate;gen+=rate*(W(tuple(z))-v0)
            fw=2*a*d*ff((b,c),(2,2));bw=a*d*ff((e,f),(2,2))
            for rate,sgn in ((fw,1),(bw,-1)):
                if rate:
                    z=(a,b-2*sgn,c-2*sgn,d,e+2*sgn,f+2*sgn)
                    gen+=rate*(W(z)-v0)
            assert gen<=-(1+s)*qterm,(x,gen,qterm)
            if qterm:
                ratio=gen/((1+s)*qterm);worst=ratio if worst is None else max(worst,ratio)
            for port,off in enumerate((0,3)):
                jold=packets(x)[port]
                if x[off]<3 or not jold:continue
                v=profile(a,d)[port];debt=Q(0)
                for rate,zloc in block(x[off:off+3],RATES):
                    if zloc[0]<x[off]:continue
                    z=list(x);z[off:off+3]=zloc;z=tuple(z)
                    jnew=packets(z)[port];vv=profile(z[0],z[3])[port]
                    own=-(jnew-jold)*v-jnew*(vv-v)
                    assert own==jold*(v-vv)-(jnew-jold)*vv
                    debt+=rate*max(Q(0),own)
                terminal=ff(x[off:off+3],(3,2,2))
                assert debt<=600*terminal,(x,port,debt,terminal)
                readychecks+=1
            checks+=1
    result={'scope':'Exact finite checks of a globally proved service inequality; full growth/activation drift remains unproved.',
        'profile_increment_checks':profilechecks,'physical_service_states':checks,
        'ready_source_payment_checks':readychecks,'R':str(R),'profile_C':str(C),
        'worst_service_generator_over_claimed_reward':str(worst)}
    (P/'results/global_service_receiver_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
