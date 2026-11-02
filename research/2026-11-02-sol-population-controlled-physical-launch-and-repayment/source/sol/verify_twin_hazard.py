#!/usr/bin/env python3
"""Exact actual terminal-port kernel; all noncore paths and residence retained."""
from fractions import Fraction as F
from pathlib import Path
import json
from conservative_fiber_kernel import raw_network,falling,bounds,shift,tridiagonal

P=Path(__file__).resolve().parent

def run(n,base):
    b,c,e,f=base
    x=(3,b+2,c+2,1,e+1,f);raw=raw_network();lo,hi=bounds(x)
    states=[shift(x,k) for k in range(lo,hi+1)];size=len(states);start=-lo
    down=[2*falling(v,raw[8][0]) for v in states]
    up=[falling(v,raw[9][0]) for v in states]
    h=[[k*falling(v,s) for s,u,k in raw[:8]] for v in states]
    assert all(row[3]==d for row,d in zip(h,down))
    diagonal=[F(d+u+sum(row)) for d,u,row in zip(down,up,h)]
    lower=[F(0)]+[-F(down[j-1]) for j in range(1,size)]
    upper=[-F(up[j+1]) for j in range(size-1)]+[F(0)]
    rhs=[F(int(j==start)) for j in range(size)]
    occ=tridiagonal(lower,diagonal,upper,rhs)
    assert min(occ)>=0
    for j in range(size):
        lhs=diagonal[j]*occ[j]
        if j:lhs+=lower[j]*occ[j-1]
        if j+1<size:lhs+=upper[j]*occ[j+1]
        assert lhs==rhs[j]
    probabilities=[sum(occ[j]*h[j][r] for j in range(size)) for r in range(8)]
    assert sum(probabilities)==1
    mean_down=sum(o*d for o,d in zip(occ,down))
    assert mean_down==probabilities[3]<=1
    time=sum(occ);assert time<=F(1,2)
    packet_bad=sum(occ[j]*h[j][3] for j,v in enumerate(states) if v[4]==0)
    distribution=sorted((v[1],occ[j]*h[j][3]) for j,v in enumerate(states))
    quantiles=[]
    for quantile in (F(1,4),F(1,2),F(3,4)):
        cumulative=F(0)
        for count,weight in distribution:
            cumulative+=weight
            if cumulative>=quantile*probabilities[3]:quantiles.append(count);break
    return {'population_parameter':n,'base':base,'input':x,'fiber_states':size,
            'all_eight_first_source_probabilities_exact':list(map(str,probabilities)),
            'physical_mean_exact':str(time),'expected_adverse_core_moves_exact':str(mean_down),
            'terminal_and_invalid_peer_packet_probability_exact':str(packet_bad),
            'terminal_pre_B_quartiles':quantiles,
            'terminal_probability_float':float(probabilities[3]),'physical_mean_float':float(time)}

def main():
    rows=[run(n,base) for n in (30,100,300) for base in ((0,0,n,n),(n,n,1,3))]
    (P/'results/twin_hazard_checks.json').write_text(json.dumps({'exact_cases':rows,
        'scope':'Exact finite actual kernel and twin hazard identities; all-population estimates are separately proved. No global recurrence or independent audit.'},indent=2)+'\n')
    print(json.dumps([{'n':v['population_parameter'],'base':v['base'],'states':v['fiber_states'],
         'P_terminal':v['terminal_probability_float'],'physical_time':v['physical_mean_float'],
         'pre_B_quartiles':v['terminal_pre_B_quartiles']} for v in rows],indent=2))

if __name__=='__main__':main()
