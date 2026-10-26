#!/usr/bin/env python3
"""Independent exact-rational finite-time boundary-capture certificate.
Model: h=I+A_g on the half-line, A_{0,1}=7/10, A_{j,j+1}=1/2 (j>=1).
The proof uses only rational finite-walk moments and a global Taylor remainder;
finite matrix numerics are secondary diagnostics, never the root certificate.
"""
import math,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq
OUT=Path(__file__).resolve().parent
G=F(7,10); J=F(1,2)
N=26
v=[F(1)]
mom=[]
for k in range(N+1):
    mom.append(sum(z*z for z in v))
    if k==N:break
    nextv=[F(0)]*(len(v)+1)
    for i,z in enumerate(v):
        if i==0:nextv[1]+=G*z
        else:
            nextv[i-1]+=(G if i==1 else J)*z
            nextv[i+1]+=J*z
    v=nextv

def cert_eval(t):
    t=F(t)
    approx=sum((F(-1)**n)*mom[n]*(t**(2*n))/math.factorial(2*n) for n in range(N+1))
    a=t**(2*N+2)/math.factorial(2*N+2)
    rest=a/(1-t*t/F((2*N+3)*(2*N+4)))
    return approx,rest

left=F(2433886050,10**9)
right=F(2433886053,10**9)
fl,rl=cert_eval(left);fr,rr=cert_eval(right)
assert fl-rl>0, ('not lower+',float(fl),float(rl))
assert fr+rr<0, ('not upper-',float(fr),float(rr))
# h>=0 from positive Schur 1-2g^2=1/50 and h-I is bipartite,
# hence ||h-I||<=1. This justifies the Taylor remainder.
M0=1-2*G*G
assert M0==F(1,50)
tup=float(right)
def exponential_tail(T,L):
    first=T**(L+1)/math.factorial(L+1)
    return first/(1-T/(L+2)) # bound geometric ratio, for L+2>T
n=120
d=np.zeros(n)
o=np.full(n-1,.5);o[0]=.7
e,V=eigh_tridiagonal(d,o)
w=V[0]**2
a=lambda t:float(np.dot(w,np.cos(e*t)))
T=brentq(a,float(left),float(right),xtol=1e-14)
# Finite matrix here is a diagnostic of the certified root.
phi=V@(np.exp(1j*(e+1)*T)*V[0,:])
assert abs(phi[0])<1e-9
chk=[]
for L in (8,10,12,14,16,18):
    eta=float(np.linalg.norm(phi[L+1:])**2)
    bound=exponential_tail(tup,L)
    assert math.sqrt(eta)<=bound+1e-13
    chk.append({'source_sites':L,'leak_norm':math.sqrt(eta),
                'rigorous_leak_norm_upper':bound,'rigorous_phase_error_upper':2*bound,
                'simulated_phase_error':2*math.sqrt(eta)})
qsl=math.pi/2
assert T>qsl
out={'model':'positive gapless Jacobi h=I+A, g=7/10, bulk hopping=1/2',
     'strict_zero_energy_schur_margin':str(M0),'spectral_support':[0,2],
     'moment_order':2*N,'time_lower_exact':str(left),'time_upper_exact':str(right),
     'autocorrelation_lower_at_time_lower':str(fl-rl),
     'autocorrelation_upper_at_time_upper':str(fr+rr),
     'certified_sign_change':True,
     'finite_matrix_root_diagnostic':T,'finite_matrix_survival_amplitude':a(T),
     'universal_capture_speed_limit_time':qsl,
     'conditional_hold_phase_time_pi_B_inv':math.pi,
     'ideal_photon_capture_hold_release_duration':2*T+math.pi,
     'ideal_root_emitter_conditional_shift':1.0,
     'finite_packet_checks':chk,
     'proofs':['|A|<=1 by positivity of I+A and chiral symmetry',
               'Truncated cos Taylor series evaluated with exact rational walk moments',
               'Root follows from opposite certified endpoint signs and continuity',
               'P_capture,max(t)=1-|<e,e^{-iht}e>|^2',
               'For lead packet projected to sites 1..L, exact wrong-port amplitude=sqrt(sum tail norm squared)',
               'Dyson finite-propagation bound sum_{n>L} t^n/n! uses ||A||<=1',
               'Two-port sign error=2 times residual lead norm after capture, independent of common release']}
(OUT/'capture_orthogonality_results.json').write_text(json.dumps(out,indent=2))
print('root',T,'strict positive schur',M0,'certified signs',float(fl-rl),float(fr+rr))
for x in chk:print('L',x['source_sites'],'tail',x['leak_norm'],'certified sign error',x['rigorous_phase_error_upper'])
