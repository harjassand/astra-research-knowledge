"""Numerically locate the actual isotropic threshold, including its limits."""
import boundary_variation as b
import numpy as np,json,time
from fractions import Fraction as R
from scipy.optimize import minimize
start=time.perf_counter();cv=np.array([float(R(x)) for x in b.gd['example_cubic_coefficients']]);z=b.N.T@cv
def quotient(v):
    D,_=b.acoustic(*v);w=D@z;return float(w@w/2)
grid=[(i*np.pi/24,j*np.pi/24) for i in range(24) for j in range(24)]
values=sorted(((quotient(p),p) for p in grid),reverse=True);maxima=[]
for value,p in values[:12]:
    result=minimize(lambda x:-quotient(x),p,method='BFGS',options={'maxiter':100,'gtol':1e-10})
    maxima.append((quotient(result.x),list(result.x%np.pi)))
maxima.sort(reverse=True);out={'maxima':maxima,'seconds':time.perf_counter()-start,'scope':'Numerical proposal only, not an exact threshold certificate.'}
(b.root/'work/isotropic_boundary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
