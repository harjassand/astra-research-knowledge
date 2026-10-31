#!/usr/bin/env python3
"""Finite probability/amplitude diagnostics, not an executable gate compiler."""
import numpy as np,json
from scipy.integrate import quad

def expq(q,t,u):return -np.log1p(-u*(-np.expm1(-q*t)))/q
rows=[]
for a,b,t in [(1,2,1e-6),(1,2,.1),(1,2,1/3),(1,2,.4),(1,2,2),(.01,100,.1),(100,.01,.1),(.01,100,1),(100,.01,1)]:
 v=a+b;x0=min(t,1/v);Delta=t-x0
 if Delta==0:
  pl=1.;P=quad(lambda z:2*z*np.exp(a*t*(z-1))*(-np.expm1(-v*t*z)/(v*t*z) if z else 1.),0,1,epsabs=1e-13)[0]
 else:
  L=.5*np.exp(-a*Delta);H=-np.expm1(-a*Delta)/(a/v);pl=L/(L+H)
  Zbar=v*((-np.expm1(-a*t))/a-np.exp(-a*t)*(-np.expm1(-b*t))/b)
  P=Zbar/(L+H)
 assert P>=.2-1e-12 and P<=1+1e-12
 N=1024;u=(np.arange(N)+.5)/N
 xl=x0*np.sqrt(u);al=np.exp(a*(xl-x0))*(-np.expm1(-v*xl))/np.minimum(1,v*xl)
 xu=t-expq(a,Delta,u) if Delta else np.zeros(N)
 au=(-np.expm1(-v*xu))/np.minimum(1,v*xu) if Delta else np.ones(N)
 q=np.concatenate((np.full(N,pl/N),np.full(N,(1-pl)/N)))
 acc=np.concatenate((al,au));pd=float(q@acc)
 c=np.sin(np.pi/10)/np.sqrt(P)
 good=c*np.sqrt(q*acc);afail=np.sqrt(1-c*c)*np.sqrt(q*acc);fail=np.sqrt(q*(1-acc))
 state=np.concatenate((good,afail,fail));assert abs(np.linalg.norm(state)-1)<1e-12
 out=state.copy();M=len(good)
 for _ in range(2):
  reflected=-out.copy();reflected[:M]=out[:M] # Rgood
  out=reflected-2*state*np.dot(state,reflected) # -Rstate Rgood
 target=np.concatenate((np.sqrt(q*acc/pd),np.zeros(2*M)))
 err=float(np.linalg.norm(out-target));failnorm=float(np.linalg.norm(out[M:]))
 predicted=abs(np.cos(5*np.arcsin(c*np.sqrt(pd))))
 assert abs(failnorm-predicted)<1e-10
 assert err<=20*abs(pd-P)+1e-10
 rows.append(dict(a=a,b=b,t=t,analytic_acceptance=P,finite_acceptance=pd,acceptance_difference=abs(pd-P),full_prepared_state_error=err,failure_norm=failnorm))
json.dump({'scope':'Finite grid probabilities and actual two-reflection vector dynamics only. No gate synthesis or full simulator.', 'cases':rows},open('native_first_event_optimization_20261031/amplified_source_checks.json','w'),indent=2)
print(len(rows),'cases; min acceptance',min(x['analytic_acceptance'] for x in rows),'max finite-grid error',max(x['full_prepared_state_error'] for x in rows))
