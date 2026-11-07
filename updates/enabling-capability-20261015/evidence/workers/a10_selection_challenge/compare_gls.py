from pathlib import Path
import json,time
import numpy as np
P=Path(__file__).resolve().parent;t0=time.perf_counter()
D=np.load(P/'data/network_psd_and_response_v2.npz');F=D['response'];S=D['psd'];freq=D['freq'];rng=np.random.default_rng(3187)
maxrel=0.;scalars=[]
for j in np.flatnonzero((freq>=1000)&(freq<=1500)):
 infos=[]
 for ind in [[0,1,2],[0,1,2,3]]:
  Z=F[ind]*(1e-22/np.sqrt(S[ind,j]))[:,None];A=Z[:,:2];b=Z[:,2];u,s,vh=np.linalg.svd(A,full_matrices=True);N=u[:,2:]
  Ip=float(np.linalg.norm(N.T@b)**2)
  # Independent strongest linear incumbent: Schur complement of normal equations.
  G=np.c_[A,b].T@np.c_[A,b];Ig=float(G[-1,-1]-G[-1,:2]@np.linalg.solve(G[:2,:2],G[:2,-1]))
  maxrel=max(maxrel,abs(Ip-Ig)/max(Ip,Ig,1e-30));infos.append(Ip)
 scalars.append(infos)
scalars=np.array(scalars)
# For unknown coefficient at every bin, ASD scale does not assume frequency coherence.
ratio=scalars[:,1]/scalars[:,0]
r={'comparison':'Same measured PSD, same sky and response, same tensor nuisance, same exclusion of vector modes. Null-projection scalar information vs ordinary weighted GLS Schur complement.','max_relative_difference':maxrel,'frequency_band_hz':[1000,1500],'information_gain_adding_G1_over_HLV':{'p05':float(np.quantile(ratio,.05)),'median':float(np.median(ratio)),'p95':float(np.quantile(ratio,.95))},'median_amplitude_precision_gain':float(np.median(np.sqrt(ratio))),'claim':'Sensor inclusion changes the available information. The proposed algebra supplies no advantage over the equally informed incumbent.','runtime_s':time.perf_counter()-t0}
(P/'EQUAL_INFORMATION_COMPARATOR.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
