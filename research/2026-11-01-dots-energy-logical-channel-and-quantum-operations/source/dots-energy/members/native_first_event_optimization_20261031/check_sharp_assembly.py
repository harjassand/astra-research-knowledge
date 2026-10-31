#!/usr/bin/env python3
"""Finite matrix checks only; not a quantum compiler or certified numerical proof."""
import json, numpy as np
from scipy.linalg import eigh, expm
from scipy.integrate import quad
rng=np.random.default_rng(20261031)
def norm(x):return float(np.linalg.norm(x,2))
def root(a):
 w,v=eigh((a+a.conj().T)/2);return (v*np.sqrt(np.maximum(w,0)))@v.conj().T
rows=[]
for A in [1,2,4,8,14]:
 for frac in [1e-6,.01,.1,.25]:
  for rep in range(3):
   m,n=7,3
   v,_=np.linalg.qr(rng.normal(size=(m,n))+1j*rng.normal(size=(m,n)))
   e=rng.normal(size=(m,n))+1j*rng.normal(size=(m,n));e=e/norm(e)*(frac/A)
   B=v/A+e; atten=A*np.sin(np.pi/(4*A+2)); C=atten*B
   # Rectangular contraction dilation: first n inputs, first m good outputs.
   U=np.block([[C,root(np.eye(m)-C@C.conj().T)],
               [root(np.eye(n)-C.conj().T@C),-C.conj().T]])
   Ri=np.diag([1]*n+[-1]*m);Ro=np.diag([1]*m+[-1]*n)
   G=-(U@Ri@U.conj().T)@Ro
   out=np.linalg.matrix_power(G,A)@U[:,:n]
   target=np.vstack((v,np.zeros((n,n))))
   error=norm(out-target)
   rows.append(dict(A=A,x=frac,unitarity=norm(U.conj().T@U-np.eye(n+m)),error=error,over_32x=error/(32*frac)))
   assert error<=32*frac+1e-10
scalar=[]
for mu in [4096.,1e4,1e6]:
 c=np.sqrt(mu);r=mu/2;ta=1/256;al2=8
 for z in [1,2]:
  cz=z*c;delta=r-2*cz;nu=np.sqrt(delta**2+8*cz**2);d=(nu+delta)/2;s=2*cz**2/d
  aa=2*(cz+s)/nu;bb=2*(d-cz)/nu
  def S1(t):return aa*np.exp(s*t)+bb*np.exp(-d*t)
  # Fast and slow terms integrated separately, with scaled fast coordinates.
  integ=aa*aa*np.expm1(2*s*ta)/(2*s)+2*aa*bb*(-np.expm1(-delta*ta))/delta+bb*bb*(-np.expm1(-2*d*ta))/(2*d)
  numeric=aa*aa*quad(lambda t:np.exp(2*s*t),0,ta,epsabs=1e-13)[0]+2*aa*bb/delta*quad(lambda x:np.exp(-x),0,min(delta*ta,50),epsabs=1e-13)[0]+bb*bb/(2*d)*quad(lambda x:np.exp(-x),0,min(2*d*ta,50),epsabs=1e-13)[0]
  errs=[]
  for t in [0,ta/100,ta]:
   E=expm(np.array([[0,cz],[2*cz,-r+2*cz]])*t)@np.diag([1,2])
   errs.append(abs(E[1,:].sum()-S1(t)))
  scalar.append(dict(mu=mu,z=z,entry_error=max(errs),integral_error=abs(integ-numeric)))
  assert max(errs)<1e-10 and abs(integ-numeric)<1e-12
out={'scope':'Numerical rectangular-dilation/OAA and scalar proposal checks only; no gate implementation or certified simulation.', 'OAA_cases':rows,'scalar_cases':scalar}
open('native_first_event_optimization_20261031/sharp_assembly_checks.json','w').write(json.dumps(out,indent=2)+'\n')
print('OAA cases',len(rows),'max bound ratio',max(x['over_32x'] for x in rows),'max unitarity',max(x['unitarity'] for x in rows),'scalar cases',len(scalar))
