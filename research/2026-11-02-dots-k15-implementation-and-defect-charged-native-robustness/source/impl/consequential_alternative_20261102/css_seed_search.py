import numpy as np, json, time
from scipy.optimize import differential_evolution, minimize
from scipy.special import logsumexp
from itertools import product

def grid(n,k=2):return (np.array(list(product(*[np.arange(n)/n-.5]*k)))+.5/n)
class Eval:
 def __init__(self,n=28,M=5,v=.37):
  self.u=grid(n);self.m=np.array(list(product(range(-M,M+1),repeat=2)));self.v=v
  self.um=self.u[:,None,:]+self.m
 def sums(self,A,shift=None,parity=None):
  x=self.um if shift is None else self.um+shift
  y=x@A.T*np.sqrt(2*np.pi)
  w=np.exp(-np.sum(y*y,axis=2)/(2*self.v)) * abs(np.linalg.det(A))/self.v
  g=w.sum(1)
  if parity is None:return g
  f=w@((-1.)**(self.m@parity))
  return g,f
 def calc(self,z,c=np.array([1,0])):
  A=np.array([[np.exp(z[0]),z[2]],[0,np.exp(z[1])]])
  s=np.linalg.svd(A,compute_uv=False)
  if min(s)<.32 or max(s)>3.1:return 1.,[0,1,0]
  g,f=self.sums(A,parity=c);rho=np.mean(f*f/g)
  B=np.linalg.inv(A).T;h=self.sums(B);ht=self.sums(B,shift=c/2)
  beta=np.mean(np.sqrt(h*ht))
  return beta-rho,[float(rho),float(beta),float(np.mean(g))]
if __name__=='__main__':
 e=Eval()
 print('baseline',e.calc([np.log(1.68),0,0]),flush=True)
 r=differential_evolution(lambda z:e.calc(z)[0],[(-1,1),(-1,1),(-1.5,1.5)],maxiter=35,popsize=8,tol=1e-5,workers=1,polish=True,seed=713)
 out={'params':r.x.tolist(),'fun':float(r.fun),'eval':e.calc(r.x),'nit':r.nit,'nfev':r.nfev}
 print(json.dumps(out),flush=True)
 fine=Eval(n=100,M=10,v=.37)
 out['fine']=fine.calc(r.x);print(json.dumps(out),flush=True)
 open('producer-workspace/css_seed_results.json','w').write(json.dumps(out,indent=2))
