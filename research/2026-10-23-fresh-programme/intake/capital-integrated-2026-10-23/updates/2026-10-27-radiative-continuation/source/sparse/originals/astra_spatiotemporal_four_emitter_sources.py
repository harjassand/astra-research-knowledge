#!/usr/bin/env python3
"""Four-emitter exact radiation-null source: early emitter #2, late emitter #3.
This verifies only the source algebra, NOT a local Hamiltonian realization.
"""
import json,numpy as np,sympy as sp
from scipy.integrate import quad
z=sp.symbols('z',nonzero=True)
gA=[1,-(z+1/z),1,0]
gB=[0,1,-(z+1/z),1]
for g in (gA,gB):
    assert sp.simplify(sum(g[j]*z**j for j in range(4)))==0
    assert sp.simplify(sum(g[j]*z**(-j) for j in range(4)))==0

tau=.5;T=12

def bump(t,a,b):
    if t<=a or t>=b:return 0.
    p=(t-a)/(b-a)
    return (4*p*(1-p))**3

def A(t):return bump(t,.5,1.5)
def B(t):return bump(t,10.5,11.5)
def source(t):
    return np.array([A(t),-(A(t-tau)+A(t+tau))+B(t), A(t)-(B(t-tau)+B(t+tau)), B(t)],dtype=float)

def FT(w):
    return np.array([quad(lambda t:source(t)[j]*np.cos(w*t),0,T,points=[0,.5,1,1.5,2,10,10.5,11,11.5,12],epsabs=3e-11)[0]+1j*quad(lambda t:source(t)[j]*np.sin(w*t),0,T,points=[0,.5,1,1.5,2,10,10.5,11,11.5,12],epsabs=3e-11)[0] for j in range(4)])
check=[]
for w in [.3,.7,1.4,3.2,6.2831853,9.9]:
    F=FT(w)
    for sgn in [-1,1]:
        res=abs(sum(np.exp(1j*sgn*w*j*tau)*F[j] for j in range(4)))
        check.append(res)

# Check the support endpoints analytically from the shifts:
# A: q2 support (0,2), q1 and q3 support (.5,1.5)
# B: q3 support (10,12), q2 and q4 support (10.5,11.5).
result={'generator_A':[str(v) for v in gA],'generator_B':[str(v) for v in gB], 'emitters':4,'positions':[0,.5,1.,1.5],'source_support_intervals':{'q1':[[.5,1.5]],'q2':[[0,2],[10.5,11.5]],'q3':[[.5,1.5],[10,12]],'q4':[[10.5,11.5]]}, 'earliest_source_emitter':2,'latest_source_emitter':3,'max_Fourier_zero_residual':float(max(check)),'scope':'Exact Laurent-polynomial source null identity; no claim of a local Schrödinger Hamiltonian or successful remote state transfer.'}
with open('/mnt/data/astra_spatiotemporal_four_emitter_sources_results.json','w') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
