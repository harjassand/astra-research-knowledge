"""A malformed erase clock can break a clean native prefix.
No claim of adapter-defect healing follows from owner-only SUCCESS counts.
"""
import numpy as np,json
from pathlib import Path
I=np.eye(2);p0=np.diag([1.,0.]);p1=np.diag([0.,1.]);X=np.array([[0.,1.],[1.,0.]])
U=np.kron(p0,I)+np.kron(p1,X)
G=U@np.kron(I,p0)@U.T
v=np.array([0.,0.,0.,1.]);rho=np.outer(v,v)
js=[np.kron(np.outer(np.array([1.,0.]),np.eye(2)[j]),I) for j in range(2)]
out=sum(J@rho@J.T for J in js)
a=float(np.trace(G@rho));b=float(np.trace(G@out));assert a==1 and b==0
r={'good_prefix_mass_before':a,'good_prefix_mass_after_unpaused_DATA_reset':b,'DATA_reset_complete_effect_error':float(np.linalg.norm(sum(J.T@J for J in js)-np.eye(4))),'scope':'actual unitary-prefix/W-good projector and onsite DATA reset; malformed adapter clock supplies invalid reset authority; counterexample does not apply inside the structurally consistent live-PARK adapter range'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
