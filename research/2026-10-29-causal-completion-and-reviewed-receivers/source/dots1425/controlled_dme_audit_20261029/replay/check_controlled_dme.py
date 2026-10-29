import numpy as np,json
from scipy.linalg import expm
from pathlib import Path
rng=np.random.default_rng(219)
rows=[]
for d in [2,3]:
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));tau=z@z.conj().T;tau/=np.trace(tau);vals,vecs=np.linalg.eigh(tau)
 swap=np.zeros((d*d,d*d))
 for i in range(d):
  for j in range(d):swap[i*d+j,j*d+i]=1
 H=np.kron(np.diag([0,1]),swap);heff=np.kron(np.diag([0,1]),tau);syst=2*d
 for t in [.5,2.]:
  target=expm(-1j*t*heff);psi=target.reshape(-1,order='F')/np.sqrt(syst);ideal=np.outer(psi,psi.conj())
  for n in [16,64,256]:
   U=expm(-1j*(t/n)*H).reshape(syst,d,syst,d);kraus=[]
   for b in range(d):
    for a in range(d):
     K=np.einsum('icj,j->ic',U[:,a,:,:],vecs[:,b])*np.sqrt(vals[b]);kraus.append(K)
   sup=sum(np.kron(K.conj(),K) for K in kraus);sup=np.linalg.matrix_power(sup,n)
   J=np.zeros((syst*syst,syst*syst),complex)
   for i in range(syst):
    for j in range(syst):
     E=np.zeros((syst,syst));E[i,j]=1;out=(sup@E.reshape(-1,order='F')).reshape(syst,syst,order='F')
     J[i*syst:(i+1)*syst,j*syst:(j+1)*syst]=out/syst
   err=float(np.linalg.norm(J-ideal,ord='nuc')/2)
   bound=16*t*t/n
   assert err<=bound+1e-10
   rows.append(dict(d=d,time=t,copies=n,normalized_Choi_trace_error=err,conservative_halfdiamond_upper=bound))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(rows=rows,scope='Entangled control/target Choi diagnostic, not generic diamond-norm numerical computation'),indent=2)+'\n');print(rows)
