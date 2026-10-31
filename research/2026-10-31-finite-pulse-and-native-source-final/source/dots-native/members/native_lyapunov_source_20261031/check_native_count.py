"""Small dense diagnostics, not a simulator or a general norm certificate."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad_vec
v=np.array([1.,-1.])/np.sqrt(2);s=np.array([1.,1.])/np.sqrt(2)
Ls=[np.outer([0.,1.],v),-np.outer([1.,0.],v)]
H=np.outer(v,v);Id=np.eye(4);Is=np.eye(2);Z=np.diag([1.,-1.]);X=np.array([[0.,1.],[1.,0.]])
K=np.kron(Z,X);HH=np.kron(H,Is);JL=[np.kron(L,Is) for L in Ls]
assert np.allclose(sum(L.T@L for L in JL),2*HH)
u=.01;theta=np.log1p(u);rows=[]
init=[np.kron(v,s),np.kron(s,s),np.array([1.,0.,0.,1.])/np.sqrt(2)]
for lam in [256.,1024.,4096.]:
 for T in [.1,1.,4.]:
  A=-lam*HH-1j*np.sqrt(lam)*K
  LT=np.kron(Id,A)+np.kron(A.conj(),Id)
  for L in JL:LT+=lam*(1+u)*np.kron(L.conj(),L)
  E=expm(T*LT);vals=[]
  for z in init:
   r=np.outer(z,z.conj());out=(E@r.reshape(-1,order='F')).reshape((4,4),order='F');vals.append(float(np.trace(out).real))
  bound=2*np.exp(32*u*T);assert max(vals)<=bound+1e-9
  rows.append({'lambda':lam,'T':T,'MGFs':vals,'proved_bound':float(bound)})
checks=[]
for lam in [256.,4096.]:
 T=.5;A=-lam*HH-1j*np.sqrt(lam)*K;N=expm(T*A)
 J,err=quad_vec(lambda t:expm(t*A).conj().T@(2*lam*HH)@expm(t*A),0,T,epsabs=1e-10,epsrel=1e-10)
 residual=np.linalg.norm(N.conj().T@N+J-Id);assert residual<1e-8
 checks.append({'lambda':lam,'T':T,'complete_first_event_isometry_residual':float(residual),'quadrature_estimate':float(err)})
r={'scope':'Dense one-source-qubit diagnostics only, h=g=kappa=b=1; not full algorithm','count_checks':rows,'first_event_checks':checks}
Path(__file__).with_name('native_count_diagnostics.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
