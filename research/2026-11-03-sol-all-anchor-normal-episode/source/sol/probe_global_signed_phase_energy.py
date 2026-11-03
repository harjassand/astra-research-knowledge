#!/usr/bin/env python3
"""Globally defined signed phase energy at the actual completed episode."""
from functools import lru_cache
from pathlib import Path
import json
import mpmath as mp
import probe_completed_factorial_episode as f
from probe_completed_factorial_episode_equivariant import means
from probe_factorial_mixed_boundaries import configure
from certify_completed_episode_failures import components
from native_corner_bridge import channels

P=Path(__file__).resolve().parent
mp.mp.dps=80

def h(z):return mp.loggamma(abs(z)+1)

@lru_cache(maxsize=None)
def energy(x,alpha,beta,core):
    a,b,c,d,e,g=x;u,v=f.gift(a);uu,vv=f.gift(d)
    z=(b-u,c-v,e-uu,g-vv);theta=means(alpha,beta,core)
    th=(theta[1],theta[2],theta[4],theta[5]);logs=[mp.log(y) for y in th]
    def objective(k):
        zz=(z[0]-2*k,z[1]-2*k,z[2]+2*k,z[3]+2*k)
        return sum(h(y)-y*l for y,l in zip(zz,logs))
    def delta(k):return objective(k+1)-objective(k)
    left,right=-1,1
    while delta(left)>=0:left*=2
    while delta(right)<0:right*=2
    while left<right:
        mid=(left+right)//2
        if delta(mid)<0:left=mid+1
        else:right=mid
    ans=objective(left)+sum(y+1/y for y in th)+1
    for n,ref in ((a,theta[0]),(d,theta[3])):ans+=mp.loggamma(n+1)-n*mp.log(ref)+ref
    assert ans>=0
    return ans

def main():
    configure();f.energy=energy
    rows=[]
    cases=[('old_native_failure',(1,10,110,1,0,100),(1,1,1,1),(1,1,1,1),(2,1)),
           ('ordinary_stationary_control',(1,20,1000020,1,0,1000000),(1,1000,1,1),(1,1000,1,1),(1,1)),
           ('generic_fast_sources',(1,20,1000020,1,0,1000000),(1,1000,1,1),(1,1000,1,1),(2,1)),
           ('negative_separated_scales',(1,2,1000002,1,0,100),(1,1,1,1),(1,1,1,1),(2,1)),
           ('positive_unpaired',(1,100,0,1,100,0),(1,1,1,1),(1,1,1,1),(2,1)),
           ('mixed_unpaired',(1,0,1000,1,1000,0),(1,1,1,1),(1,1,1,1),(2,1)),
           ('balanced_cold_launch',(1,0,0,1,20,20),(1,1,1,1),(1,1,1,1),(2,1))]
    for name,x,alpha,beta,core in cases:
        e0=energy(x,alpha,beta,core)
        assert abs(e0-energy(x[3:]+x[:3],beta,alpha,core[::-1]))<mp.mpf('1e-60')
        maxjump=mp.mpf(0)
        for y,rate,label in channels(x,alpha,beta,core):
            de=energy(y,alpha,beta,core)-e0
            if label[0]=='core':assert abs(de)<mp.mpf('1e-60')
            else:maxjump=max(maxjump,abs(de))
        dm,ds,cost=components(x,20,alpha,beta,core)
        rows.append({'boundary':name,'input':x,'alpha':alpha,'beta':beta,'core':core,
                     'largest_checked_one_jump':str(maxjump),'mean_energy_increment':str(dm),
                     'second_energy_increment':str(ds),'extra_physical_time_and_count':str(cost),
                     'full_received_difference':str(ds+2*dm+cost)})
    result={'scope':'Global signed representation; 80-decimal finite actual complete episodes and own actual corner. No uniform inwardness claim.','cases':rows}
    (P/'results/global_signed_phase_energy_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
