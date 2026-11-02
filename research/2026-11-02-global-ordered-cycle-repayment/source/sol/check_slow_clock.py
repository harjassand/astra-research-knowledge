#!/usr/bin/env python3
"""Exact designated-cycle and Poisson-cut diagnostics; proof is in the note."""
from pathlib import Path
from fractions import Fraction as F
import json
from ordered_cycle_certificate import raw_cycle,complexes
from check_global_construction import rate

P=Path(__file__).resolve().parent

def cycle_transform(k,kap,n,s):
    raw=raw_cycle(k,kap);value=F(1);phase=[]
    for j,y in enumerate(complexes(k)):
        x=tuple(a+b for a,b in zip((0,n,n),y))
        rr=[rate(x,yy,c) for yy,zz,c in raw];q=sum(rr)
        assert q>s
        value*=rr[j]/(q-s)
        phase.append({'phase':j,'designated_probability':str(rr[j]/q),
                      'total_rate':str(q),'weighted_factor':str(rr[j]/(q-s))})
    return value,phase

def poisson_cut(n):
    weights=[F(1),F(1,n+1),F(1,2*(n+1)**2),F(1,6*(n+1)**2*(n+2)**2)]
    raw=raw_cycle(3);C=complexes(3);flux=F(0)
    for j,y in enumerate(C):
        x=tuple(a+b for a,b in zip((0,n,n),y))
        flux+=weights[j]*sum(rate(x,yy,c) for yy,zz,c in raw[:j])
    formula=F(1,n+1)+F(1+2*(n+1),2*(n+1)**2)+F(1+3*(n+2)+6*(n+2)**2,6*(n+1)**2*(n+2)**2)
    assert flux==formula
    return flux/sum(weights)

if __name__=='__main__':
    rows=[]
    for k in [3,4,5,8]:
        kap=[F(j+1,2*j+1) for j in range(k+1)]
        for s in [kap[0]/10,kap[0]/2]:
            n=max(4,k)
            while True:
                value,phases=cycle_transform(k,kap,n,s)
                if value>1:break
                n*=2;assert n<2**50
            rows.append({'k':k,'rates':[str(v) for v in kap],'positive_s':str(s),
                         'acquired_n':n,'actual_neutral_cycle_transform':str(value),
                         'limit':str(kap[0]/(kap[0]-s)),'phases':phases})
    cuts=[{'n':n,'exact_exit_flux_over_mass':str(poisson_cut(n)),
           'n_times_ratio_decimal':float(n*poisson_cut(n))} for n in [10,100,1000,10000]]
    out={'scope':'Exact finite diagnostics of the all-n asymptotic proofs; same principal, no independent audit.',
         'neutral_cycles_with_transform_gt_one':rows,'poisson_cut_checks':cuts}
    (P/'results'/'slow_clock_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'neutral_cycle_witnesses':len(rows),'all_transforms_gt_one':True,
                      'Poisson_cut_n_times_ratio':[v['n_times_ratio_decimal'] for v in cuts],
                      'all_checks':'PASS'},indent=2))
