#!/usr/bin/env python3
"""Exact arbitrary-input current identities and source-switch bounds."""
from fractions import Fraction as F
from pathlib import Path
import json
from check_source_conditioned_switch import build,tri

P=Path(__file__).resolve().parent

def probe(q,s1,s2):
    bs,lo,di,up,h1,h2,_,birth,death=build(q,s1,s2)
    size=len(bs);H=[h1[j]+h2[j]+3 for j in range(size)]
    mu=[F(1)]
    for j in range(size-1):mu.append(mu[-1]*birth[j]/death[j+1])
    lot=[F(0)]*size;upt=[F(0)]*size
    for j in range(1,size):lot[j]=up[j-1]
    for j in range(size-1):upt[j]=lo[j+1]
    wins=[]
    for port in (0,1):
        vals=build(q,s1,s2,post=port)
        _,lp,dp,upp,_,_,enemy,bp,_=vals
        u=tri(lp,dp,upp,enemy)
        if port==0:assert all(u[j]>=u[j+1] for j in range(size-1))
        else:assert all(u[j]<=u[j+1] for j in range(size-1))
        D=[(b+s1+1) if port==0 else(q-b+s2+1) for b in bs]
        cp=[mu[j]*bp[j]/D[j] for j in range(size-1)]
        wins.append((u,enemy,D,cp))
    n=min(s1,s2);points=range(size);worst=0.;cases=0
    for source in points:
        rho=[F(int(j==source)) for j in range(size)]
        nu=tri(lot,di,upt,rho);f=[nu[j]/mu[j] for j in range(size)]
        assert sum(nu[j]*H[j] for j in range(size))==1
        current=[];cumulative=F(0)
        for j in range(size-1):
            cumulative+=rho[j]-nu[j]*H[j]
            edge=mu[j]*birth[j]*(f[j]-f[j+1])
            assert edge==cumulative and abs(edge)<=1
            current.append(edge)
        for port,(u,enemy,D,cp) in enumerate(wins):
            E=sum(cp[j]*(f[j]-f[j+1])*(u[j]-u[j+1]) for j in range(size-1))
            TV=sum(abs(current[j])*abs(u[j]-u[j+1]) for j in range(size-1))
            assert TV<=1 and abs(E)<=F(2,n)*TV
            h=h1 if port==0 else h2;a1,a2=(5,3) if port==0 else(2,4)
            prob=sum(nu[j]*h[j]*u[j] for j in range(size))
            rhs=F(a1,2*a2)*(sum(nu[j]*enemy[j]*(1-u[j])/D[j] for j in range(size))-E)
            assert prob==rhs and prob<=F(3*a1,2*a2*n)
            worst=max(worst,float(prob)*n);cases+=1
    return {'q':q,'gaps':[s1,s2],'all_incoming_points':size,
            'exact_source_orders':cases,'worst_probability_times_min_gap':worst}

def main():
    rows=[]
    for q in (1,2,5,20,100):
        for s1,s2 in ((10,10),(100,10**12),(10**12,100)):
            rows.append(probe(q,s1,s2))
    result={'scope':'Exact all-point incoming tests; current proof covers arbitrary mixtures as well.',
            'cases':rows,'exact_orders':sum(r['exact_source_orders'] for r in rows)}
    (P/'results/source_switch_current_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'core_cases':len(rows),'incoming_points':sum(r['all_incoming_points'] for r in rows),
                      'exact_two_stage_orders':result['exact_orders'],
                      'worst_n_times_probability':max(r['worst_probability_times_min_gap'] for r in rows)},indent=2))

if __name__=='__main__':main()
