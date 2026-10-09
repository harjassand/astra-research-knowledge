import sys;sys.path.insert(0,'/workspace/shared/broadcast_inequality');from iterate_binary_squash import *
from scipy.optimize import differential_evolution

def f(x):
 c,z0,t=x;z=z0*np.sqrt(1-c*c)
 r=[np.array([[1+z,c],[c,1-z]])/2,np.array([[1-z,c],[c,1+z]])/2];v=[np.array([1,0]),np.array([t,np.sqrt(1-t*t)])]
 w=sum(np.kron(r[i],np.outer(v[i],v[i]))/2 for i in range(2));target=h(np.array([(1+np.sqrt(1-c*c))/2,(1-np.sqrt(1-c*c))/2]))+1-h(np.array([(1+c)/2,(1-c)/2]));return cmi(w)-target
r=differential_evolution(f,[(.00001,.99999),(0,1),(0,1)],seed=173,maxiter=500,tol=1e-9);print(r.x,r.fun)
