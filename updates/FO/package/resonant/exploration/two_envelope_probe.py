import numpy as np
from scipy.optimize import minimize
A,B,C,E,L,M=107/24,3,19,-13,-29/2,-12

def mat(v):
 t,la,mu=v
 Q1=np.array([[A,la/2,L/2],[la/2,B,t/2],[L/2,t/2,C-la]])
 Q2=np.array([[2*A,2*mu,L/2],[2*mu,2*B,(t-2*M)/2],[L/2,(t-2*M)/2,C/2+mu]])
 z=(C+E)/2-la-mu
 return Q1,Q2,z

def con(v):
 Q1,Q2,z=mat(v[:3]); e=v[3]
 return np.r_[np.linalg.eigvalsh(Q1)-e,np.linalg.eigvalsh(Q2)-e,z-e]
for seed in range(5):
 x=np.r_[[-12,0,0],-5]+np.random.default_rng(seed).normal(size=4)
 r=minimize(lambda v:-v[3],x, constraints={'type':'ineq','fun':con},method='SLSQP',options={'maxiter':2000,'ftol':1e-12})
 print(r.success,r.fun,r.x,con(r.x),flush=True)
