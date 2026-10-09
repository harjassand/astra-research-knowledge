import numpy as np
from scipy.optimize import minimize
import json,sys
rng=np.random.default_rng(20261009)
ln2=np.log(2)
def h(x):
 x=np.clip(x,1e-15,1-1e-15);return -(x*np.log(x)+(1-x)*np.log1p(-x))/ln2

def entlog(A):
 z,U=np.linalg.eigh(A); z=np.maximum(z,1e-15)
 return -np.dot(z,np.log(z))/ln2,(U*np.log(z))@U.T

def obj(x,d,grad=True):
 L,K=x.reshape(2,d,d); A=L@L.T;B=K@K.T
 na=np.linalg.norm(A);nb=np.linalg.norm(B); R=A/na;S=B/nb
 rr=R@R;ss=S@S;T=(rr+ss)/2
 et,lt=entlog(T);er,lr=entlog(rr);es,ls=entlog(ss)
 c=np.clip(np.sum(R*S),1e-12,1-1e-12); v=np.sqrt(1-c*c)
 f=2*et-er-es-h((1+c)/2)-1+h((1+v)/2)
 qprime=(np.log((1+c)/(1-c))+c/v*np.log((1+v)/(1-v)))/(2*ln2)
 G=(R@(lr-lt)+(lr-lt)@R)/ln2+qprime*S
 H=(S@(ls-lt)+(ls-lt)@S)/ln2+qprime*R
 G=(G-R*np.sum(G*R))/na;H=(H-S*np.sum(H*S))/nb
 gx=np.stack([(G+G.T)@L,(H+H.T)@K]).ravel()
 return -f,-gx
best=-1
for d in [3,4,6,8,12]:
 for k in range(30):
  x=rng.normal(size=2*d*d)
  if k%3==0:
   x=x.reshape(2,d,d);x[1]=x[0]+10**rng.uniform(-3,-.2)*x[1];x=x.ravel()
  out=minimize(obj,x,args=(d,),jac=True,method='L-BFGS-B',options={'maxiter':1000,'ftol':1e-13,'gtol':1e-9,'maxls':50})
  val=-out.fun
  if val>best:
   best=val
   with open('/workspace/shared/broadcast_inequality/affinity_best.json','w') as f:json.dump({'d':d,'x':out.x.tolist(),'value':val,'seed':20261009},f)
  print(d,k,val,'best',best,'nit',out.nit,flush=True)
