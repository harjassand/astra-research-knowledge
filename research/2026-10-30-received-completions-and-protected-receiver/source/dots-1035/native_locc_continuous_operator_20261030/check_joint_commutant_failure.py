"""Exact rejected-shortcut fixture: terminal program erasure does NOT preserve
arbitrary operators diagonal in the semantic-Q block decomposition.
"""
import numpy as np,json
from pathlib import Path
# Basis (phase:0=active,1=retired; Alice raw bit; Bob program bit).
d=8;Q=np.zeros((d,d));O=np.zeros((d,d));Js=[]
idx=lambda phase,a,p:4*phase+2*a+p
for a in range(2):
    for p in range(2):Q[idx(0,a,p),idx(0,a,p)]=int(a!=p)
# Positive target operator |+><+| on Alice, retired P=0. It is entirely Q=0.
for a in range(2):
    for aa in range(2):O[idx(1,a,0),idx(1,aa,0)]=.5
for p in range(2):
    J=np.zeros((d,d))
    for a in range(2):J[idx(1,a,0),idx(0,a,p)]=1
    Js.append(J)
pull=sum(J.T@O@J for J in Js)
comm0=float(np.linalg.norm(Q@O-O@Q));comm1=float(np.linalg.norm(Q@pull-pull@Q));cross=float(np.linalg.norm(Q@pull@(np.eye(d)-Q)))
assert comm0==0 and comm1>.9 and cross>.4
# Yet Q=0 source is invariant under the full erase channel: destination is retired.
no_create=max(float(np.linalg.norm(Q@J@(np.eye(d)-Q))) for J in Js);assert no_create==0
out={'target_positive':bool(np.linalg.eigvalsh(O).min()>-1e-12),'target_commutes_Q_norm':comm0,'pulled_target_commutator_Q_norm':comm1,'pulled_good_bad_cross_norm':cross,'individual_no_creation_norm':no_create,'rejected_claim':'nominal adjoint preserves all arbitrary joint-Q-block-diagonal operators','surviving_claim':'own zero-range invariance and positive E_t*Q own-corner support','scope':'actual source-resolved program-erasure component, embeds in full Bob terminal because it acts trivially on Alice'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
