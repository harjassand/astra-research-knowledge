#!/usr/bin/env python3
"""Classical sampler diagnostics; not coherent finite-bit or production implementation."""
import numpy as np,json,math
from scipy.integrate import quad
rng=np.random.default_rng(20261031)
def truncexp(q,t):return -np.log1p(-rng.random()*(-np.expm1(-q*t)))/q

def opposite(a,b,t):
 v=a+b;w=(-np.expm1(-a*t))/(-np.expm1(-v*t))
 return truncexp(a,t) if rng.random()<w else t-truncexp(b,t)

def same_cond(a,b,t):
 v=a+b
 for attempts in range(1,10001):
  if v*t>=1:
   x=t-truncexp(a,t);acc=-np.expm1(-v*x)
  else:
   x=t*np.sqrt(rng.random());z=v*x
   acc=np.exp(a*(x-t))*(-np.expm1(-z)/z if z else 1.)
  if rng.random()<acc:return t-x,attempts
 raise RuntimeError('diagnostic cap')

rows=[]
for a,b,t in [(1,2,.000001),(1,2,.1),(1,2,1),(1,2,10),(.01,100,.1),(100,.01,.1),(.01,100,1),(100,.01,1),(1e-4,1e4,.001),(1e4,1e-4,.001),(1,2,.3333333333),(1,2,.35)]:
 for kind in ['opposite','same_conditional_event']:
  N=12000;v=a+b
  if kind=='opposite':
   samples=np.array([opposite(a,b,t) for _ in range(N)])
   w=-np.expm1(-a*t)/(-np.expm1(-v*t))
   def den(u):return w*a*np.exp(-a*u)/(-np.expm1(-a*t))+(1-w)*b*np.exp(-b*(t-u))/(-np.expm1(-b*t))
   attempts=None
  else:
   vals=[same_cond(a,b,t) for _ in range(N)];samples=np.array([x[0] for x in vals]);attempts=np.mean([x[1] for x in vals])
   def raw(u):return np.exp(-a*u)*(-np.expm1(-v*(t-u)))
   Z=quad(raw,0,t,epsabs=1e-13,epsrel=1e-12)[0]
   def den(u):return raw(u)/Z
  mean=quad(lambda u:u*den(u),0,t,epsabs=1e-12)[0]
  var=quad(lambda u:(u-mean)**2*den(u),0,t,epsabs=1e-12)[0]
  se=np.sqrt(var/N);zscore=abs(samples.mean()-mean)/max(se,1e-100)
  assert zscore<6
  if attempts is not None:assert attempts<5
  rows.append(dict(a=a,b=b,t=t,kind=kind,mean=float(samples.mean()),exact_integral_mean=mean,zscore=float(zscore),average_proposals=attempts))
# Numerical TV duration checks, integrate smooth pieces and account no-event atom.
tvrows=[]
for a,b,t in [(1,2,.01),(.01,100,.1),(100,.01,.1),(1,2,1)]:
 for same in [False,True]:
  dt=t*1e-4;v=a+b
  def atom(T):return np.exp(-a*T)*v/(b+a*np.exp(-v*T)) if same else 0.
  def den(u,T):
   if u<0 or u>T:return 0.
   if same:
    return a*b*np.exp(-a*u)*(-np.expm1(-v*(T-u)))/(b+a*np.exp(-v*T))
   return np.exp(-a*u)*(a+b*np.exp(-v*(T-u)))/(-np.expm1(-v*T))
  tv=.5*(abs(atom(t+dt)-atom(t))+quad(lambda u:abs(den(u,t+dt)-den(u,t)),0,t,epsabs=1e-12)[0]+quad(lambda u:den(u,t+dt),t,t+dt,epsabs=1e-12)[0])
  bound=32*(v+1/t)*dt
  assert tv<=bound
  tvrows.append(dict(a=a,b=b,t=t,same_endpoint=same,tv=tv,bound=bound))
out={'scope':'Floating diagnostic only; exact source proof and finite coherent arithmetic are separate. Conditional-event testing is not physical postselection.', 'sampler_cases':rows,'duration_cases':tvrows}
open('native_first_event_optimization_20261031/elementary_bridge_checks.json','w').write(json.dumps(out,indent=2)+'\n')
print(len(rows),'sampler cases; max zscore',max(x['zscore'] for x in rows),'max average proposals',max(x['average_proposals'] or 0 for x in rows),';',len(tvrows),'TV cases')
