import numpy as np
from scipy.optimize import differential_evolution
Qs=[np.array([[-1.,1,0],[100,-101,1],[0,100,-101]]),np.array([[-100.,100],[1,-2]]),np.array([[-1.,1,0],[0,-1,1],[100,0,-101]])]
for qi,Q in enumerate(Qs):
 for p in [2,10,100,1000,10000]:
  # logs of f^p; normalize largest log=0; allow wide small weights
  def fun(u):
   u=np.r_[u,0.];u-=u.max();f=np.exp(u/p);z=np.exp(u)
   return -np.sum(z*(Q@f)/f)/sum(z)
  res=differential_evolution(fun,[(-max(50,p),max(50,p))]*(len(Q)-1),popsize=20,maxiter=800,tol=1e-10,seed=3)
  print(qi,p,-res.fun,res.x,flush=True)
