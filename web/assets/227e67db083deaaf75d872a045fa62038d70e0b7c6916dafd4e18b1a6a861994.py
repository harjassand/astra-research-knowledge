#!/usr/bin/env python3
"""Small dense / high-precision checks, not the counting FPRAS or compiler."""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(20261008)

def hamiltonian(n, edges, h, g):
    N=1<<n; H=np.zeros((N,N))
    for x in range(N):
        z=[1-2*((x>>i)&1) for i in range(n)]
        H[x,x]+=sum(h[i]*z[i] for i in range(n))
        for i in range(n): H[x,x^(1<<i)]-=g[i]
        for i,j,f,d in edges:
            H[x,x]+=.5*d*z[i]*z[j]
            if z[i]!=z[j]: H[x,x^(1<<i)^(1<<j)]-=f
    return H

fixtures=[]
for n in range(2,6):
    for trial in range(12):
        edges=[]
        for i in range(n):
            for j in range(i+1,n):
                if rng.random()<.6:
                    f=float(rng.integers(1,6))/3
                    d=f*float(rng.integers(-4,5))/4
                    edges.append((i,j,f,d))
        h=rng.integers(-5,6,size=n)/4
        g=rng.integers(1,6,size=n)/10
        H=hamiltonian(n,edges,h,g)
        vals,vecs=eigh(H)
        u=vecs[:,0]
        if sum(u)<0:u=-u
        assert min(u)>0
        V=sum(f+max(d,0) for i,j,f,d in edges)+2*sum(abs(h))+sum(g)
        r=min([f for i,j,f,d in edges]+list(g))
        loggamma=-n*math.log(2)+2*n*n*math.log(min(1,r/V))
        assert math.log(min(u))+1e-10>=loggamma
        gap=float(vals[1]-vals[0]);known=2*min(g)
        assert gap+1e-9>=known
        fixtures.append({'n':n,'trial':trial,'log_min_amplitude':float(math.log(min(u))),
                         'log_acquired_floor':loggamma,'gap':gap,
                         'prior_art_gap_bound':float(known)})

mp.mp.dps=100
# An exact two-spin instance with a unique ground vector (01+10)/sqrt(2).
n=2; gamma=mp.mpf(1)/1024; eps=mp.mpf('0.01'); Delta=mp.mpf(2)
tau=(n+1+mp.ceil(mp.log(128/(eps*gamma),2)))/Delta
z=mp.exp(-2*tau)
normal=mp.sqrt(2*(1+z*z))
psi=mp.matrix([z/normal,1/normal,1/normal,z/normal])
ground=mp.matrix([0,1/mp.sqrt(2),1/mp.sqrt(2),0])
err=mp.norm(psi-ground)
assert err<=eps*gamma/128
pzero=psi[0]**2;pone=psi[1]**2
assert pzero<gamma**2/4 and pone>gamma**2/4
conditional=mp.matrix([z,1])/mp.sqrt(1+z*z)
assert mp.norm(conditional-mp.matrix([0,1]))<eps
assert abs(2*pone-1)<eps
# Overlap with |00> is zero, with |01> is 1/sqrt(2).
assert pzero<gamma**2/4
assert abs(pone/mp.mpf('.5')-1)<eps

# Exponentially small positive fidelity, evaluated without cancellation at high precision.
h=mp.mpf(1);g=mp.mpf('0.001');R=mp.sqrt(h*h+g*g);nprod=4
ua=mp.matrix([mp.sqrt((R-h)/(2*R)),mp.sqrt((R+h)/(2*R))])
ub=mp.matrix([ua[1],ua[0]])
overlap=sum(ua[i]*ub[i] for i in range(2))
F=overlap**(2*nprod);exact=(g*g/(h*h+g*g))**nprod
assert abs(F/exact-1)<mp.mpf('1e-85')
Vprod=nprod*(2*h+g)
log_floor=-nprod*mp.log(2)+2*nprod*nprod*mp.log(g/Vprod)
assert mp.log(F)>=4*log_floor  # each state has this floor; F >= gamma^4.

result={'scope':'48 dense finite cases plus 100-digit two-spin and product examples; no counting FPRAS, independent proof or quantum compiler',
 'random_positive_field_fixtures':fixtures,
 'summary':{'dense_cases':len(fixtures),'smallest_gap_ratio_to_prior_bound':min(x['gap']/x['prior_art_gap_bound'] for x in fixtures)},
 'two_spin_rare_support':{'gamma':mp.nstr(gamma,40),'epsilon':str(eps),'tau':str(tau),
   'cooling_euclidean_error':mp.nstr(err,40),'zero_ground_event_finite_time_probability':mp.nstr(pzero,40),
   'positive_ground_event_probability':'.5','finite_time_positive_event_probability':mp.nstr(pone,40),
   'conditional_cooling_error':mp.nstr(mp.norm(conditional-mp.matrix([0,1])),40)},
 'small_positive_fidelity':{'n':nprod,'h':'1','g':'0.001','fidelity':mp.nstr(F,80),'formula':'(g^2/(h^2+g^2))^n',
                          'log_amplitude_floor_each':mp.nstr(log_floor,50)},
 'all_assertions_passed':True}
(ROOT/'checks'/'rare_ground_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='random_positive_field_fixtures'},indent=2))
