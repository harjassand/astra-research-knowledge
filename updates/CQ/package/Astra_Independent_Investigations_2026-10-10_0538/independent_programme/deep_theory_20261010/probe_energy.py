import numpy as np
from scipy.optimize import minimize

def min_energy(m):
 mask=1+np.triu(np.ones((m,m)),1)
 def fg(z):
  a=z[:m]; b=np.r_[z[m:],0.]
  x=np.maximum(a[:,None]+b[None,:],0)
  f=.5*np.sum(mask*x*x)-sum(a)-sum(b)
  g=np.r_[np.sum(mask*x,axis=1)-1,(np.sum(mask*x,axis=0)-1)[:-1]]
  return f,g
 z=np.r_[np.ones(m)/m,np.zeros(m-1)]
 res=minimize(fg,z,method='L-BFGS-B',jac=True,options={'gtol':1e-11,'ftol':1e-15,'maxiter':5000,'maxls':50})
 a=res.x[:m]; b=np.r_[res.x[m:],0.]; X=np.maximum(a[:,None]+b[None,:],0)
 return {'m':m,'energy':4*np.sum(mask*X*X),'residual':float(max(abs(fg(res.x)[1]))),'min_potential':float(np.min(a[:,None]+b[None,:])),'success':bool(res.success),'a':a.tolist(),'b':b.tolist()}
if __name__=='__main__':
 import json
 rows=[]
 for m in [2,3,4,8,10,20,50,100,200]:
  row=min_energy(m); rows.append(row); print({k:v for k,v in row.items() if k not in ('a','b')},flush=True)
 with open('independent_programme/deep_theory_20261010/energy_probe.json','w') as f:json.dump(rows,f,indent=2)
