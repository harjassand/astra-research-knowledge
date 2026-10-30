"""Finite diagnostic of the previously derived unrestricted PC pair criterion."""
from pathlib import Path
import numpy as np,json
from scipy.optimize import differential_evolution
K=np.array([[1.,0.,11/13],[0.,1.,0.],[11/13,0.,28/13]])
def sphere(v):return np.array([np.cos(v[0])*np.cos(v[1]),np.sin(v[0])*np.cos(v[1]),np.sin(v[1])])
def sv(n):
    f=n@K@n;g=f*np.trace(K)-n@K@K@n
    si=2*np.linalg.det(K)/(g+np.sqrt(max(0,g*g-4*np.linalg.det(K)*f)))
    return si,K@n-si*n
def ratio(x):
    n,pp=sphere(x[:2]),sphere(x[2:]);sn,vn=sv(n);sp,vp=sv(pp)
    return np.linalg.norm(pp[2]*vn-n[2]*vp)/(pp[2]*sn+n[2]*sp)
res=differential_evolution(lambda x:-ratio(x),[(0,2*np.pi),(1e-6,np.pi/2)]*2,seed=889,popsize=18,maxiter=250,tol=1e-10)
out={'angles':res.x.tolist(),'maximum_pair_ratio_found':-res.fun,'scope':'Finite numerical diagnostic; neither a global PC proof nor a non-PC proof.'}
Path(__file__).with_name('pc_geometry_diagnostic.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
