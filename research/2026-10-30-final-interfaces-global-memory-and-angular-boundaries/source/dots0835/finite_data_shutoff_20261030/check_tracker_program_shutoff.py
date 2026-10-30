"""Actual 36-level finite-group program: all-target monotonicity during ramp.
The permanent tracker is not treated as a DATA-free clock while its H remains on.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
src=Path('producer-workspace/check_reusable_frame_register.py').read_text()
ns={};exec(compile(src.split('# Full physical gauge')[0],'<frozen program definitions>','exec'),ns)
d=ns['d'];labels=ns['labels'];idx=ns['idx'];group=ns['group'];w=ns['w'];Js=ns['Js'];H=ns['H'];m=ns['m']
G=np.zeros((4*d,4*d),complex)
for q in range(d):G[4*q:4*q+4,4*q:4*q+4]=group[w[q]][1]
I=np.eye(4*d);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);DX=np.kron(np.eye(d),np.kron(X,np.eye(2)));DZ=np.kron(np.eye(d),np.kron(Z,np.eye(2)))
results=[]
for v in range(m):
 pv=np.zeros((d,d),complex);pv[idx[('r',v)],idx[('r',v)]]=1
 P=np.kron(pv,np.eye(4));B=I-P
 hp=G@np.kron(H(v),np.eye(4))@G.conj().T
 herrors=[]
 for f in [1.,.63,.17,0.]:
  h=f*hp;herrors.extend([np.linalg.norm(h@P),np.linalg.norm(h@P-P@h)])
  assert herrors[-1]<1e-12 and herrors[-2]<1e-12
 drift=np.zeros_like(I,dtype=complex);reseterrors=[]
 for j in Js:
  jp=G@np.kron(j,np.eye(4))@G.conj().T;jj=jp.conj().T@jp
  reseterrors.append(np.linalg.norm((I-P)@jp@P))
  drift+=jp.conj().T@B@jp-(jj@B+B@jj)/2
  assert np.linalg.norm(jp@DX-DX@jp)<1e-12 and np.linalg.norm(jp@DZ-DZ@jp)<1e-12
 source=np.zeros((d,d),complex)
 for g in range(m):
  if g!=v:source[idx[('e',g,v)],idx[('e',g,v)]]=1
 residual=np.linalg.norm(drift+np.kron(source,np.eye(4)))
 assert residual<1e-12 and max(reseterrors)<1e-12
 # A DATA-active arbitrary native payload conjugated by G preserves target program label.
 payload=np.kron(X,Z)+.37*np.kron(Z,X)
 dressed=G@np.kron(np.eye(d),payload)@G.conj().T
 native_comm=np.linalg.norm(dressed@P-P@dressed);assert native_comm<1e-12
 dataactive=max(np.linalg.norm(hp@DX-DX@hp),np.linalg.norm(hp@DZ-DZ@hp))
 results.append({'target':v,'max_ramped_H_ready_error':float(max(herrors)),'reset_noncreation_error':float(max(reseterrors)),'exact_ready_drift_error':float(residual),'dressed_native_payload_preserves_program_ready_error':float(native_comm),'held_program_H_is_DATA_active_norm':float(dataactive)})
out={'actual_program_dimension':d,'all_targets':results,'must_ramp_program_H_not_merely_hold_target':True,'scope':'Actual finite program matrix checks; native term classification and whole common-bath support theorem remain analytic.'}
Path(__file__).with_name('tracker_program_shutoff_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
