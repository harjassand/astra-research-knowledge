"""Exact-law floating-point diagnostic of a whole two-state bridge sampler.
No endpoint rejection. This is not a coherent gate implementation.
"""
import math,json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(9131031)
max_race=max_clock=0

def atom_coin(pi,nu,t):
 global max_race
 ts=-math.log(pi)/nu
 for attempt in range(1,200):
  if t>=ts:
   delta=t-ts
   if rng.integers(2)==0:
    if rng.exponential(1/nu)>=delta:
     max_race=max(max_race,attempt);return True
   elif not (rng.random()<pi and rng.exponential(1/nu)>=delta):
    max_race=max(max_race,attempt);return False
  elif rng.integers(2)==0:
   max_race=max(max_race,attempt);return True
  else:
   e=rng.exponential(1/nu)
   if ts-t<=e<ts:
    max_race=max(max_race,attempt);return False
 raise RuntimeError('diagnostic race cap')

def last_gap(nu,t):
 global max_clock
 M=math.ldexp(1.,math.ceil(math.log2(t)))
 mass=-math.expm1(-nu*M)
 for attempt in range(1,200):
  y=-math.log1p(-rng.random()*mass)/nu
  if y<=t:
   max_clock=max(max_clock,attempt);return y
 raise RuntimeError('diagnostic dyadic cap')

def sample(q0,q1,t,i,j,selfrate):
 nu=q0+q1; rates=[q0,q1];pi=[q1/nu,q0/nu]
 if t==0:return (0 if i==j else 1),0
 if i==j and atom_coin(pi[i],nu,t):
  return (int(rng.poisson(selfrate*t)) if i==1 else 0),1
 gap=last_gap(nu,t);stop=t-gap;now=0.;state=i;count=0
 for _ in range(256):
  wait=rng.exponential(1/rates[state]);end=min(stop,now+wait)
  if state==1:count+=int(rng.poisson(selfrate*(end-now)))
  if now+wait>=stop:break
  now=end;state=1-state;count+=1
 else:raise RuntimeError('diagnostic path cap')
 if state!=j:count+=1
 if j==1:count+=int(rng.poisson(selfrate*gap))
 return count,0
rows=[];N=4000;z=1.1
for q0,q1 in [(.2,100.),(1.,1.),(.001,1000.),(1000.,.001)]:
 nu=q0+q1;selfrate=.2*min(q0,q1)
 for t in [1e-6,.1,1.]:
  Q=np.array([[-q0,q0],[q1,-q1]])
  P=expm(t*Q)
  def pgf(w):
   A=np.array([[-q0,w*q0],[w*q1,-q1+selfrate*(w-1)]])
   return expm(t*A)
  G=pgf(z);G2=pgf(z*z)
  for i in range(2):
   for j in range(2):
    observations=[sample(q0,q1,t,i,j,selfrate) for _ in range(N)]
    vals=np.array([z**v for v,_ in observations]);target=G[i,j]/P[i,j]
    se=math.sqrt(max(0,G2[i,j]/P[i,j]-target*target)/N)
    error=float(abs(vals.mean()-target));assert error<=8*se+2e-7,(q0,q1,t,i,j,error,se)
    rows.append({'q0':q0,'q1':q1,'t':t,'i':i,'j':j,'samples':N,'pgf_error':error,'theoretical_standard_error':se})
r={'scope':'48 floating-point whole-bridge PGF checks; not a quantum backend or production precision proof','rows':rows,'max_atom_race_attempts':max_race,'max_dyadic_clock_attempts':max_clock}
Path(__file__).with_name('last_refresh_bridge_checks.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'cases':len(rows),'max_standardized_error':max(x['pgf_error']/x['theoretical_standard_error'] if x['theoretical_standard_error'] else 0 for x in rows),'max_race':max_race,'max_clock':max_clock}))
