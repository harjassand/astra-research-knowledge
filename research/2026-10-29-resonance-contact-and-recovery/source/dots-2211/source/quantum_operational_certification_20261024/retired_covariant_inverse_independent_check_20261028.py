#!/usr/bin/env python3
"""Exact finite-root estimator distributions, symmetry and independent coherent service."""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import numpy as np,json,math,cmath
roots=[(1,0),(0,1),(-1,0),(0,-1)]
rows=[];states_checked=0
for a in [F(1),F(1,2),F(1,10)]:
 for ui,u in enumerate(roots):
  probs=[(1+a*(u[0]*z[0]+u[1]*z[1]))/4 for z in roots]
  law={(0,0):F(1)}
  for N in range(1,17):
   nxt=defaultdict(F)
   for (x,y),mass in law.items():
    for (dx,dy),prob in zip(roots,probs):nxt[x+dx,y+dy]+=mass*prob
   law=dict(nxt);assert sum(law.values())==1
   meanx=sum(m*x for (x,y),m in law.items());meany=sum(m*y for (x,y),m in law.items())
   assert meanx==N*a*u[0]/2 and meany==N*a*u[1]/2
   v=4/a**2-1
   mse=sum(m*((2*x/(a*N)-u[0])**2+(2*y/(a*N)-u[1])**2) for (x,y),m in law.items())
   assert mse==v/N
   # Conjugation about the true root maps integer lattice points to integer points.
   ucomplex=complex(*u);lam=0j;record=0.
   for (x,y),mass in law.items():
    point=complex(x,y);reflected=ucomplex*ucomplex*point.conjugate()
    assert law.get((int(reflected.real),int(reflected.imag)),F(0))==mass
    if point:
     err=point/abs(point)/ucomplex;lam+=float(mass)*err;record+=float(mass)*math.sqrt(max(0,(1-err.real)/2))
    else:
     # Uniform tie roots have mean zero and obey the same covariance/reflection.
     record+=float(mass)*sum(math.sqrt(max(0,(1-(complex(*r)/ucomplex).real)/2)) for r in roots)/4
    states_checked+=1
   assert abs(lam.imag)<1e-12
   b=(1-lam.real)/2;assert b<=min(1,float(v/N))+1e-12
   rows.append({'a':str(a),'grid_index':ui,'N':N,'mean_residual_multiplier':lam.real,'retired_error':b,'retained_service_error':record,'bound':min(1,float(v/N))})
# Actual coherent native service, no classical Pauli-instrument decomposition.
I=np.eye(2);Z=np.diag([1,-1]);plus=np.ones(2)/np.sqrt(2);minus=np.array([1,-1])/np.sqrt(2);p=.37
psi=np.sqrt(1-p)*np.kron(plus,[1,0])+np.sqrt(p)*np.kron(minus,[0,1]);R=np.outer(psi,psi.conj());Z4=np.kron(Z,I)
# Last distribution a=1/10,u=-i,N16; average the actual unitary programs explicitly.
actual=np.zeros((4,4),complex)
for (x,y),mass in law.items():
 rs=[complex(x,y)/abs(complex(x,y))] if x or y else [complex(*z) for z in roots]
 for r in rs:
  err=r/ucomplex;half=cmath.sqrt(err);W=np.diag([half,half.conjugate()]);Q=np.kron(W,I)
  actual+=float(mass)/len(rs)*(Q@R@Q.conj().T)
b=rows[-1]['retired_error'];theory=(1-b)*R+b*Z4@R@Z4
assert np.linalg.norm(actual-theory)<1e-12
loss=np.abs(np.linalg.eigvalsh(actual-R)).sum()/2;assert abs(loss-b)<1e-12
out={'status':'PASS_EXACT_COVARIANT_ROOT_ESTIMATOR_AND_INDEPENDENT_COHERENT_SERVICE','K':4,'exact_distribution_cases':len(rows),'exact_lattice_states_checked':states_checked,'source_draws':0,'rng_draws':0,'rows':rows,'coherent_service_error':float(loss),'coherent_service_formula_residual':float(np.linalg.norm(actual-theory)),'scope':'Exact rational estimator probability laws and moment/reflection identities; float evaluation only for algebraic normalization/trace norm; no sampled learner or hardware.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
