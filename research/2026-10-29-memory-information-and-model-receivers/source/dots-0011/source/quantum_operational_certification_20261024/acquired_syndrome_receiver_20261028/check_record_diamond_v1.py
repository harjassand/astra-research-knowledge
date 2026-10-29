#!/usr/bin/env python3
"""Independent numerical stress of exact analytic block-functional identity."""
from pathlib import Path
import json,numpy as np
from branch_recovery_v1 import P,herm
HERE=Path(__file__).parent;rng=np.random.default_rng(202610282304)
max_bell_error=0.;max_random_excess=-1.;tests=0
for S in [2,3,5,16]:
 for trial in range(40):
  raw=[]
  for s in range(S):
   Z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));raw.append(Z@Z.conj().T)
  w,V=np.linalg.eigh(sum(raw));G=(V*(1/np.sqrt(w)))@V.conj().T;effects=[herm(G@E@G) for E in raw]
  bs=[np.array([np.trace(P[j]@E).real/2 for j in range(1,4)]) for E in effects];B=[sum(b[j]*P[j+1] for j in range(3)) for b in bs]
  L=sum(np.linalg.norm(b) for b in bs);bell=sum(np.linalg.eigvalsh(x.T/2).__abs__().sum() for x in B)
  max_bell_error=max(max_bell_error,abs(L-bell))
  assert abs(L-bell)<1e-12 and L<=1+1e-12
  # Arbitrary reference dimension 1,2,3 with full rank mixed inputs.
  for r in [1,2,3]:
   Z=rng.normal(size=(2*r,2*r))+1j*rng.normal(size=(2*r,2*r));rho=Z@Z.conj().T;rho/=np.trace(rho);R=rho.reshape(2,r,2,r)
   val=0.
   for x in B:
    # Trace input after B multiplication; reference output indices retained.
    out=np.einsum('ij,jria->ra',x,R)
    val+=np.linalg.eigvalsh(herm(out)).__abs__().sum()
   max_random_excess=max(max_random_excess,val-L);assert val<=L+1e-12;tests+=1
out={'status':'PASS_ANALYTIC_IDENTITY_NUMERICAL_STRESS','POVMs':160,'arbitrary_reference_tests':tests,'Bell_max_error':max_bell_error,'random_input_max_excess_over_analytic_bound':max_random_excess,'scope':'Numerical stress supplements the independent analytic proof; not diamond optimization by samples.'}
(HERE/'record_diamond_check_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
