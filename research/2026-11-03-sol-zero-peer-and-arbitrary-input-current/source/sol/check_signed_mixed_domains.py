#!/usr/bin/env python3
"""Exact common-workload checks for new mixed and zero-peer domains.

The analytic domains are SIGNED_ZERO_PEER_RETURN.md. Finite checks are
diagnostics; no global recurrence or independent audit is claimed.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from native_corner_bridge import complete_bridge,channels,psi

P=Path(__file__).resolve().parent

def h(b,c):
    t=min(b,c)
    return F(abs(b-c))+F(3,2)*t+F(t%2,2)

def main():
    mixed=[]
    for n in (100,10000,10**6):
        for cold in (0,2,10):
            r=complete_bridge(n+1,n+cold,cold,w=20)
            mixed.append({'n':n,'peer_minority':cold,'mean_psi_change':str(r['mean_delta']),
                          'float_mean':float(r['mean_delta']),'physical_time':str(r['time']),
                          'noncore_count':str(r['count'])})
    alpha=(1,1000,1,1);beta=(10,1,100,1);w=92
    for cold in (0,2,10):
        r=complete_bridge(10**6+1,10**6+cold,cold,w,alpha,beta)
        mixed.append({'n':10**6,'peer_minority':cold,'rates':[alpha,beta],'w':w,
                      'mean_psi_change':str(r['mean_delta']),'float_mean':float(r['mean_delta']),
                      'physical_time':str(r['time']),'noncore_count':str(r['count'])})
    checked=0;skipped=0;worst=None;firsts=[]
    for alpha,beta in (((1,1,1,1),(1,1,1,1)),((2,5,3,7),(1,2,3,4))):
        B0=alpha[0]+beta[0];w=4+8*B0//min(alpha[0],beta[0]);b=w+1;c0=8*b*b
        for a in (6,10,100):
            for gap in (10**4,10**6):
                for sign in (-1,1):
                    for minor in (0,1,2,20,10000):
                        bb,cc=(minor,minor+gap) if sign<0 else (minor+gap,minor)
                        for ee,ff in ((0,0),(1,1),(10**6,10**6),(10**12,1),(1,10**12)):
                            x=(a,bb,cc,0,ee,ff);pin=psi(x,w);S=bb+cc+ee+ff
                            if pin-S<10*(w+5):skipped+=1;continue
                            assert a<=h(bb,cc)
                            drift=F(0);square=F(0);rate=F(0)
                            for out,lam,label in channels(x,alpha,beta):
                                assert label[0]=='block'
                                assert out[0]<=h(out[1],out[2]) and out[3]<=h(out[4],out[5])
                                assert out[0]>=3 or out[3]>=3
                                assert psi(out,w)>=sum(out[1:3])+sum(out[4:6])
                                delta=psi(out,w)-pin
                                drift+=lam*delta;square+=lam*delta*delta;rate+=lam
                            assert drift<=-rate/8,(x,alpha,beta,drift,rate)
                            L=2*(pin+c0)*drift+square
                            assert L<=-1-rate,(x,L,rate)
                            ratio=F(-L,rate)
                            if worst is None or ratio<worst:worst=ratio
                            checked+=1
    result={'scope':'Exact full raw mixed/corner kernels and zero-peer generator tests. Uniform proofs are in source notes.',
            'mixed_corner_cases':mixed,'zero_peer_generator_cases':checked,'outside_gate_cases_skipped':skipped,
            'smallest_negative_V_drift_per_noncore_rate':str(worst)}
    (P/'results/signed_mixed_domain_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'mixed_cases':len(mixed),'mixed_means':[r['float_mean'] for r in mixed],
                      'zero_peer_generator_cases':checked,'outside_gate_skipped':skipped,
                      'worst_negative_V_per_rate':float(worst)},indent=2))

if __name__=='__main__':main()
