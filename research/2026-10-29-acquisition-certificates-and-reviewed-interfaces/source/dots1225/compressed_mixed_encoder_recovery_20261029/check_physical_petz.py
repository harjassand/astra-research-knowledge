"""Finite-record tomography and actual CPTP Petz decoder in the SMALL compressed model.
Counts sampled by multinomial; this does not execute the large-D joint Schur circuit.
"""
import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(202610291202);k=2;r=2;d=k*r;h=k*d;beta=.01
rows=[]
for spectrum in [[.5,.5],[.01,.99],[1e-8,1-1e-8]]:
 A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));U=np.linalg.qr(A)[0]
 Ks=[np.sqrt(spectrum[a])*U[:,[i*r+a for i in range(k)]] for a in range(r)]
 J=sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj()) for K in Ks)/k
 for m in [10000,1000000,100000000]:
  H=np.zeros((h,h),complex)
  for i in range(h):H[i,i]=rng.binomial(m,J[i,i].real)/m
  for i in range(h):
   for j in range(i+1,h):
    ss=(J[i,i]+J[j,j]).real/2
    vals=[]
    for mu in [J[i,j].real,J[i,j].imag]:
     p=np.array([ss+mu,ss-mu,1-2*ss]);p=np.maximum(p,0);p/=p.sum();n=rng.multinomial(m,p);vals.append((int(n[0])-int(n[1]))/(2*m))
    H[i,j]=vals[0]+1j*vals[1];H[j,i]=H[i,j].conj()
  marginal=np.einsum('aibi->ab',H.reshape(k,d,k,d))
  B=H-np.kron(marginal-np.eye(k)/k,np.eye(d)/d)
  e=np.sqrt(np.log(2*h*h/beta)/(2*m));a=4*h*e
  C=(B+2*a*np.eye(h))/(1+2*h*a)
  ev,V=np.linalg.eigh(C);assert ev.min()>0
  Khat=[np.sqrt(k*ev[j])*V[:,j].reshape(k,d).T for j in range(h)]
  S=sum(K@K.conj().T for K in Khat)/k;se,sv=np.linalg.eigh(S);inv=(sv*(1/np.sqrt(se)))@sv.conj().T
  Rs=[K.conj().T@inv/np.sqrt(k) for K in Khat]
  tp=np.linalg.norm(sum(R.conj().T@R for R in Rs)-np.eye(d));assert tp<1e-11
  fe=lambda recovery,channel:sum(abs(np.trace(R@K))**2 for R in recovery for K in channel)/k**2
  exactR=[U[:,[i*r+j for i in range(k)]].conj().T for j in range(r)]
  ftrue=fe(Rs,Ks);fmodel=fe(Rs,Khat);fcompetitor=fe(exactR,Khat)
  assert fmodel+1e-11>=fcompetitor**2
  delta=min(1,k*np.linalg.norm(C-J,ord='nuc')/2)
  assert ftrue>=1-3*delta-1e-10
  rows.append(dict(junk_spectrum=spectrum,shots_per_setting=m,total_training_queries=h*h*m,entry_confidence_radius=float(e),actual_max_entry_error=float(np.max(np.abs(H-J))),decoder_TP_residual=float(tp),model_fe=float(fmodel),actual_fe=float(ftrue),known_correct_recovery_model_fe=float(fcompetitor),model_channel_distance_upper=float(delta),conservative_halfdiamond_upper=min(1,k*np.sqrt(max(0,1-ftrue)))))
res=dict(scope='Small compressed-model finite-outcome simulation and physical CPTP decoder; no SDP/globaloptimizer, no actual largeD compression or hardware; fresh IID source only',rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
