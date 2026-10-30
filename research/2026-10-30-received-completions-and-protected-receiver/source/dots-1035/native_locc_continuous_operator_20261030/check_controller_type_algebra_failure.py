"""Complete dirty erasure can pull tag coherence into DATA dependence."""
import numpy as np,json
from pathlib import Path
I2=np.eye(2);I4=np.eye(4);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);CX=np.block([[I2,np.zeros((2,2))],[np.zeros((2,2)),X]])
V=np.block([[I4,np.zeros((4,4))],[np.zeros((4,4)),CX]])
O=np.kron(X,I4);pull=np.zeros((8,8),complex)
for w in range(2):
 e=np.zeros((2,2));e[0,w]=1
 J=np.kron(I2,np.kron(e,I2))@V
 pull+=J.conj().T@O@J
expected=V.conj().T@O@V
err=float(np.linalg.norm(pull-expected));comm=float(np.linalg.norm(pull@np.kron(I4,Z)-np.kron(I4,Z)@pull))
assert err<1e-12 and comm>1
out={'complete_workspace_erasure_formula_error':err,'pulled_controller_tag_observable_DATA_commutator':comm,'all_checks_pass':True,'rejected_shortcut':'all controller-TYPE observables form a DATA-independent adjoint algebra on arbitrary malformed owner coherences','scope':'actual controlled-forest reset structure; no objection to buffered-clean restriction or reviewed raw/weighted debt statements'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
