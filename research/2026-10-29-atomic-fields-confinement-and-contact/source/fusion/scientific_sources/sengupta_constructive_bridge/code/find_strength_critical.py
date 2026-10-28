"""Limited repair test: true magnetic-well critical points, not favourable trajectories."""
from pathlib import Path
import sys,importlib.util,json
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parents[2]/'positive_current_operation/vendor'))
import numpy as np
from scipy.optimize import least_squares
spec=importlib.util.spec_from_file_location('frozen_reference',Path(__file__).parents[1]/'sources/worker_sengupta_paraboloid.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
def grad(q):
 d=f.data(q,True);return d['J'].T@d['grad_strength']
rows=[]
for z in [.451186823767,1.119609503028]:
 for u,v in [(f.U0,0),(f.U0+.1,.03),(f.U0+.2,-.05)]:
  sol=least_squares(grad,[u,v,z],bounds=([.3,-.2,z-.3],[.95,.2,z+.3]),xtol=1e-12,gtol=1e-12,ftol=1e-12,max_nfev=200)
  q=sol.x;eps=1e-5;H=np.column_stack([(grad(q+eps*np.eye(3)[j])-grad(q-eps*np.eye(3)[j]))/(2*eps) for j in range(3)])
  rows.append(dict(start=[float(u),float(v),z],q=q.tolist(),gradient_norm=float(np.linalg.norm(grad(q))),strength=float(f.data(q)['strength']),DeltaPsi=float(f.surface_label(q)-f.PSI0),coordinate_Hessian_eigenvalues=np.linalg.eigvalsh((H+H.T)/2).tolist(),nfev=sol.nfev))
Path('results/strength_critical_repair.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
