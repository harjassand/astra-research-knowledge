#!/usr/bin/env python3
"""Small tests of the routing-channel weak-norm upper bound."""
from pathlib import Path
import numpy as np,json
root=Path(__file__).resolve().parent
rng=np.random.default_rng(6050104)
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]);I=np.eye(2)
rows=[]
for k in range(1,7):
 d=2**k
 ops=[]
 for j in range(k):
  oa=[]
  for P in [X,Y,Z]:
   v=np.array([[1]],complex)
   for l in range(k):v=np.kron(v,P if l==j else I)
   oa.append(v)
  ops.append(oa)
 max_weak=0.;max_bessel=0.
 for _ in range(16):
  A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));A=(A+A.conj().T)/2;A/=max(1,np.linalg.norm(A,2))
  coeff=np.array([[np.trace(P@A).real/d for P in oa] for oa in ops])
  s=float((coeff[:,:2]**2).sum());a2=float(np.trace(A@A).real/d)
  assert s<=a2+1e-10
  err=float(np.sqrt((coeff[:,:2]**2).sum(axis=1)).mean())
  assert err<=1/np.sqrt(k)+1e-10
  max_weak=max(max_weak,err);max_bessel=max(max_bessel,s)
 rows.append({'k':k,'input_dimension':d,'output_classical_sectors':k,'output_quantum_fibre_dimension':2,'proved_weak_upper_bound':float(1/np.sqrt(k)),'sample_max_weak_error':max_weak,'sample_max_Bessel_energy':max_bessel,'exact_diamond_EB_distance_by_written_witness_and_dephasing_upper_bound':1})
(root/'routing_boundary_checks.json').write_text(json.dumps({'seed':6050104,'fixtures':rows,'scope':'Numerical Bessel checks only. Diamond distance 1 and k-extension are proved analytically, not inferred from a solver.'},indent=2)+'\n')
print(json.dumps({'fixtures':len(rows),'largest_input_dimension':rows[-1]['input_dimension'],'quantum_fibre_size':2},indent=2))
