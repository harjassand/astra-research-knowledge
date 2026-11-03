#!/usr/bin/env python3
"""Materialize raw scalar constants for the polynomial episode theorem."""
from pathlib import Path
import json
import mpmath as mp

P=Path(__file__).resolve().parent
mp.mp.dps=80

def compile_bound(r,alpha=(1,1,1,1),beta=(1,1,1,1),core=(2,1)):
    a=list(map(mp.mpf,alpha));b=list(map(mp.mpf,beta));kf,kb=map(mp.mpf,core)
    B=a[0]+b[0];b0=min(a[0],b[0]);c1=max(a[1],b[1]);c2=max(a[2],b[2]);t0=24*min(a[3],b[3])
    CF=1/b0+(1/B+1/b0)*(1+c1/b0)
    CR=1/b0+(1/B+1/t0+1/b0)*(1+c2/b0)
    R=kf/kb;Kc=max(1,R,1/R);Kp=max(1,a[0]/a[3],b[0]/b[3]);K=Kc*Kp;t=6*K
    rmin=min(1,a[0]/a[3],b[0]/b[3]);Cx=Kc/rmin
    G0=sum(a[:3])+sum(b[:3]);D0=32*CR*G0*Kc**2*max(a)*max(b)/(min(a)*min(b))
    delta=mp.mpf(2)**(-r-3)
    N=int(mp.ceil(max(3,t+2,2*Cx*t*t,512*t*t)))+1
    def logH(n):return mp.log(D0)+17*mp.log(2)+mp.loggamma(9)+8*mp.log(n)+2*n*mp.log(t)-mp.loggamma(n+1)
    while logH(N)>mp.log(delta):N*=2
    assert N>=3 and N>=t+2 and N+1>=2*Cx*t*t and N+1>=512*t*t
    assert logH(N)<=mp.log(delta)
    C=8*CF*(mp.mpf(2)**r)*(2*N+3)**(r+2)
    return {'occupation_power':r,'alpha':alpha,'beta':beta,'core':core,'head_offset_N':N,
            'uniform_head_probability_bound_log10':str(logH(N)/mp.log(10)),
            'selected_delta':str(delta),'forward_clock_constant':str(CF),'reverse_clock_constant':str(CR),
            'log10_polynomial_occupation_constant':str(mp.log(C)/mp.log(10)),
            'contract':'E integral_0^sigma (1+M_t)^r dt <= C*(1+M_in)^(r+2)'}

def main():
    rows=[]
    for a,b,k in (((1,1,1,1),(1,1,1,1),(2,1)),((1,1000,1,1),(1,1000,1,1),(2,1)),
                  ((1,5,3,7),(2,2,4,11),(3,7))):
        for r in (0,7):rows.append(compile_bound(r,a,b,k))
    result={'scope':'Acquired conservative theorem constants, deliberately loose. No practical-performance or inwardness claim.','cases':rows}
    (P/'results/global_polynomial_episode_bounds.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
