import numpy as np
from scipy.optimize import minimize, minimize_scalar
from search import S,h

def o(v,theta,acc):
 z=(v[:8]+1j*v[8:]).reshape(4,2);q,_=np.linalg.qr(z)
 states=np.array([[np.cos(theta/2),np.sin(theta/2)],[-np.sin(theta/2),np.cos(theta/2)],[np.cos(theta/2),-np.sin(theta/2)],[np.sin(theta/2),np.cos(theta/2)]])
 ps=(q@states.T).T.reshape(4,2,2);b=np.array([p@p.conj().T for p in ps]);e=np.array([p.T@p.conj() for p in ps]);chi=S(b.mean(0))+S(e.mean(0))-2*np.mean([S(r) for r in b]);return -(chi-1-acc)
for theta in [.001,.01,.03,.1,.2,.4,.6,.785398]:
 phi=np.linspace(0,np.pi,10001); hs=np.array([.5*(h((1+np.cos(p-theta))/2)+h((1+np.cos(p+theta))/2)) for p in phi]);acc=1-min(hs);best=-100
 for j in range(20):
  r=minimize(o,np.random.randn(16),args=(theta,acc),method='BFGS',options={'maxiter':300,'gtol':1e-8});best=max(best,-r.fun)
 print(theta,acc,best,flush=True)
