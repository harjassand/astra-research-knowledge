#!/usr/bin/env python3
"""Independently rescore SAVED numerical models without rerunning optimizers."""
from pathlib import Path
import numpy as np,json,itertools,hashlib
from scipy.linalg import expm
D=Path(__file__).parent;I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.]);P=[X,Y,Z]
V=expm(-1j*(.47*np.kron(X,X)+.31*np.kron(Y,Z)+.19*np.kron(Z,I)+.37*np.kron(I,X)))
U=np.array([[3.,-1.],[1.,3.]])/np.sqrt(10);base=[np.diag([1.,.8]),np.array([[0.,.6],[0.,0.]])];g=[np.array([[1.],[0.]]),np.array([[1.],[1.]])/np.sqrt(2)]
sourceK=[V@np.kron(k,gg)/np.sqrt(2) for kk,gg in zip([base,[U@k@U.T for k in base]],g) for k in kk]
assert np.linalg.norm(sum(k.conj().T@k for k in sourceK)-I)<1e-12
models=np.load(D/'replayed_models.npz');saved=json.loads((D/'replayed_results.json').read_text())
for f,h in saved['sha256'].items():assert hashlib.sha256((D/f).read_bytes()).hexdigest()==h

def receiver(A):
 a,b=A[0],A[2];q=np.kron((np.eye(4)+b)/2,I)+np.kron((np.eye(4)-b)/2,X);c=np.kron(np.eye(4),(I+Z)/2)+np.kron(a,(I-Z)/2);W=q@c@q
 K=[W.reshape(4,2,4,2)[pout,:,:,ain]/np.sqrt(2) for pout in range(4) for ain in range(2)]
 return K,float(np.linalg.norm(W.conj().T@W-np.eye(8),2))
def score(K):
 fe=sum(abs(np.trace(l@k))**2 for l in K for k in sourceK)/4
 T=np.zeros((2,2),complex)
 for l in K:
  t=np.array([np.trace(l@V@np.kron(I,np.eye(2)[:,r:r+1])) for r in range(2)])
  T+=np.outer(t.conj(),t)/4
 return 1-float(fe),1-float(np.linalg.eigvalsh(T).min())
maxdiff=0.;maxTP=0.;maxunit=0.;methods=0;rows=[]
for row in saved['runs']:
 key=row['bank'];entry={'bank':key}
 for method in ['variational','raw_sign','scalar_whitening','operator_whitening','SDP_rounded']:
  f=key+'_'+method+'_A'
  if f not in models.files:continue
  A=models[f];K,ur=receiver(A);native,worst=score(K);maxunit=max(maxunit,ur);maxTP=max(maxTP,np.linalg.norm(sum(l.conj().T@l for l in K)-np.eye(4),2))
  for val,field in [(native,'native_Bell_loss'),(worst,'worst_gauge_inverse_Bell_loss')]:maxdiff=max(maxdiff,abs(val-row[method][field]))
  entry[method]={'native_Bell_loss':native,'worst_gauge_inverse_Bell_loss':worst};methods+=1
 J=models[key+'_SDP_Choi'];v,Q=np.linalg.eigh((J+J.conj().T)/2);assert v.min()>-1e-12
 K=[np.sqrt(max(0,t))*Q[:,j].reshape(2,4) for j,t in enumerate(v)]
 native,_=score(K);maxdiff=max(maxdiff,abs(native-row['full_CPTP_SDP']['native_Bell_loss']));maxTP=max(maxTP,np.linalg.norm(sum(l.conj().T@l for l in K)-np.eye(4),2));entry['full_CPTP_SDP_native_loss']=native;methods+=1;rows.append(entry)
assert maxdiff<1e-12 and maxTP<1e-10
quad=json.loads((D/'quadratic_native_oracle_guard_diagnostics.json').read_text())
for r in quad['rows']:
 e=r['empirical_fit_residual']+r['simultaneous_data_Frobenius_allowance'];bound=e*e/(8*r['candidate_kappa_float'])
 assert abs(bound-r['native_oracle_regret_bound_unclipped'])<1e-10
 assert not r['passes_regret_0_01']
assert len(quad['rows'])==12
out={'status':'PASS_SAVED_MODEL_KRAUS_RESCORE','optimizer_reruns':0,'source_calls':0,'banks':len(rows),'quadratic_native_confidence_failures_rechecked':12,'decoder_method_instances':methods,'max_saved_score_difference':maxdiff,'max_receiver_or_SDP_TP_residual':float(maxTP),'max_three_reflection_unitarity_residual':maxunit,'method':'Direct Kraus composition/trace fidelity and Kraus gauge effect, independently of original matrix-unit decoder scorer','runs':rows,'scope':'Floating saved-model rescoring, not exact interval physicality or source acquisition','sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),D/'replayed_models.npz',D/'replayed_results.json',D/'quadratic_native_oracle_guard_diagnostics.json']}}
(D/'independent_rescore_saved_models.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
