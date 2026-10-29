"""Random-code moment and exact-model Petz diagnostics, NOT learned decoder execution.
Worst-HS partial-trace source, Haar code sampling; efficient Clifford2design not simulated.
"""
import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(202610291340);rows=[]
for D in [8,16,32,64,128]:
 k=r=2;out=D//r;Ks=[]
 for a in range(r):
  K=np.zeros((out,D));K[np.arange(out),np.arange(out)*r+a]=1;Ks.append(K)
 noiseI=sum(K@K.T for K in Ks);b=np.trace(noiseI@noiseI);tauE=np.eye(r)/r
 # Complement on unnormalizedI is(D/r)I_r; aTrace=Tr T(I)^2.
 aTrace=D*D/r
 exact=(k*D-1)/(k*D*(D*D-1))*(b-aTrace/D)
 vals=[];loss=[];decoupling=[]
 for trial in range(1000):
  raw=rng.normal(size=(D,k))+1j*rng.normal(size=(D,k));E=np.linalg.qr(raw)[0];restricted=[K@E for K in Ks]
  J=np.empty((k,r,k,r),complex)
  for i in range(k):
   for j in range(k):
    for a in range(r):
     for bb in range(r):J[i,a,j,bb]=np.vdot(restricted[bb][:,j],restricted[a][:,i])/k
  Delta=J.reshape(k*r,k*r)-np.kron(np.eye(k)/k,tauE)
  vals.append(float(np.linalg.norm(Delta,'fro')**2));decoupling.append(float(np.linalg.norm(Delta,ord='nuc')))
  # Oracle-model compressed support only to diagnose mathematical code performance.
  basis=np.linalg.qr(np.column_stack(restricted))[0];F=[basis.conj().T@K for K in restricted]
  S=sum(K@K.conj().T for K in F)/k;ev,V=np.linalg.eigh(S);inv=(V*(1/np.sqrt(np.maximum(ev,1e-15))))@V.conj().T
  R=[K.conj().T@inv/np.sqrt(k) for K in F];fe=sum(abs(np.trace(A@B))**2 for A in R for B in F)/k**2
  loss.append(float(1-fe))
 rows.append(dict(input_dimension=D,output_dimension=out,logical_dimension=k,Kraus_rank=r,trials=1000,mean_hs_square=float(np.mean(vals)),exact_mean_hs_square=float(exact),mean_trace_decoupling=float(np.mean(decoupling)),mean_exact_model_Petz_loss=float(np.mean(loss)),Petz_mean_loss_bound=2*r*np.sqrt(k/D)))
res=dict(scope='Seeded finite algebra diagnostic for fixed partial-trace source and Haar codes. Exact-model recovery computed using unavailable oracle matrices ONLY as benchmark; no black-box learner/hardware/Clifford sampler execution.',rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
