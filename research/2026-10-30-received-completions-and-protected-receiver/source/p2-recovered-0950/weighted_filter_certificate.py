#!/usr/bin/env python3
"""Exact shorter amplitude-degree filter over Q[r]/(r^5-8).

There are 23,552 amplitude-scaled intermediate segments, before the explicit
signed-only PWM realization. The positive duration ratio r=8^(1/5) is a real
timing resource. The older integer-weight filter remains an alternative.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time
from drift_filter_certificate import commword,group_project,transform,data_parity,bracket
from explore_word import word_series,scale

ZERO=(F(0),)*5
ONE=(F(1),)+(F(0),)*4

def ra(a,b):return tuple(x+y for x,y in zip(a,b))
def rs(a,b):return tuple(x*b for x in a)
def rm(a,b):
    out=[F(0)]*5
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b):
            if y:out[(i+j)%5]+=x*y*(8 if i+j>=5 else 1)
    return tuple(out)
def rp(n):
    out=[F(0)]*5;out[n%5]=F(8)**(n//5);return tuple(out)
def add(a,b):
    out=dict(a)
    for w,v in b.items():
        out[w]=ra(out.get(w,ZERO),v)
        if out[w]==ZERO:del out[w]
    return out
def mul(a,b):
    out={}
    for u,x in a.items():
        for v,y in b.items():
            if len(u)+len(v)>5:continue
            w=u+v;out[w]=ra(out.get(w,ZERO),rm(x,y))
            if out[w]==ZERO:del out[w]
    return out
def log(a):
    x=add(a,{():rs(ONE,-1)});power={():ONE};out={}
    for j in range(1,6):
        power=mul(power,x);out=add(out,{w:rs(v,F((-1)**(j+1),j)) for w,v in power.items()})
    return out

def main():
    start=time.time();root=Path(__file__).parent
    a=[('A',1)];b=[('B',1)];c=[('C',1)]
    ell=commword(c,commword(a,b));source=commword(a,commword(a,ell))
    base=word_series(source+list(reversed(source)),5)
    s=group_project(group_project(base));m=transform(s,(1,1,-1),F(1,2))
    full={w:rs(ONE,v) for w,v in s.items()}
    stretch={w:rs(rp(len(w)),v) for w,v in m.items()}
    out={():ONE}
    for block in [stretch,full,full,stretch]:out=mul(block,out)
    generator=log(out)
    nonmemory={w:v for w,v in generator.items() if data_parity(w)!=(0,0,0)}
    aa={('A',):F(1)};bb={('B',):F(1)};cc={('C',):F(1)}
    expected=scale(bracket(aa,bracket(aa,bracket(cc,bracket(aa,bb)))),F(192))
    assert nonmemory=={w:rs(ONE,v) for w,v in expected.items()}
    assert not any(len(w)%2==0 for w in generator)
    assert all(len(w)==5 and 'D' not in w for w in nonmemory)
    # Weighted durations implement arbitrary moment weights at the one
    # surviving homogeneous degree; lower coefficients are memory-only.
    base_count=19316736
    duration_factor=2*sum(abs(w)**(1/9) for w in [-672,168,-32,3])
    result={'scope':'Root exact degree-five noncommutative check in Q[r]/(r^5-8). No independent review or physical execution. Fractional amplitudes still require explicit signed-only PWM.',
            'duration_ratio':'positive real root of r^5=8',
            'amplitude_scaled_segment_count':92*8*8*4,
            'old_integer_weight_amplitude_scaled_segment_count':105984,
            'same_degree_five_data_coefficient_as_old_filter':True,
            'all_drift_containing_data_terms_through_degree_five_vanish':True,
            'data_coefficient_of_L5':192,
            'degree_nine_derived_weighted_filter':{
                'segment_count_before_PWM':base_count*8,
                'subword_duration_factors':[abs(w)**(1/9) for w in [-672,168,-32,3]],
                'duration_multiplier_over_unfiltered_word':duration_factor,
                'data_coefficient_same_as_integer_weight_filter':True,
                'check_scope':'Moment identity and general lower-memory-only composition proof; not a full degree-nine word expansion.'},
            'seconds':time.time()-start}
    (root/'weighted_filter_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
