"""Check the derived X-noise spectral identity on the same 81 controls."""
from pathlib import Path
from fractions import Fraction
import json
import numpy as np

base=Path(__file__).parent
rows=json.loads((base/'DESIGNED_CONTROLS.json').read_text())['rows']
raising=np.kron(np.eye(2),np.array([[0.,1.],[0.,0.]]))
out=[]
for row in rows:
    rho=np.array(row['rho_real_float'])
    p=float(Fraction(row['exact_parameters']['p']))
    alpha=.5*np.log(p/(1-p))
    vals,vec=np.linalg.eigh(rho)
    r=np.sqrt(vals)
    d=np.log(r)[:,None]-np.log(r)[None,:]
    a=(vec.T @ raising @ vec).T
    def kfun(x): return x*np.sinh(x)-(np.pi/2)*(np.cosh(x)-1)
    spectral=4*np.sum(r[:,None]*r[None,:]*(kfun(d+alpha)*np.abs(a)**2+kfun(d)*np.real(a*a.T)))
    direct=row['J_matrix'][0][0]-np.pi*row['E_matrix'][0][0]
    out.append({'exact_parameters':row['exact_parameters'],'spectral_F_X':float(spectral),'direct_F_X':float(direct),'absolute_residual':float(abs(spectral-direct))})
report={'status':'finite identity diagnostics only','number_of_states':len(out),'maximum_absolute_residual':max(v['absolute_residual'] for v in out),'rows':out}
(base/'SPECTRAL_CONTROL_REPLAY.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({key:report[key] for key in ['status','number_of_states','maximum_absolute_residual']},indent=2))
