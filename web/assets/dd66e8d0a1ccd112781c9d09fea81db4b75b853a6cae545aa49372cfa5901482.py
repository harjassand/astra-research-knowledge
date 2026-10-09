import numpy as np
from scipy.special import xlogy
from scipy.optimize import minimize_scalar
from scipy.linalg import block_diag

def h(x):
 x=np.maximum(x,0);return -np.sum(xlogy(x,x))/np.log(2)
def ent(x):return h(np.linalg.eigvalsh(x))
def root(x):
 w,v=np.linalg.eigh(x);return (v*np.sqrt(np.maximum(w,0)))@v.T.conj()
def cmi(w):
 d=len(w)//2;a=w[:d,:d];b=w[d:,d:];return 2*(1+(ent(2*a)+ent(2*b))/2)-ent(w)-ent(a+b)
def sym(w,c):
 d=len(w)//2
 v,z=np.linalg.eigh(w);idx=v>1e-13
 f=z[:,idx]*np.sqrt(v[idx]);m0=f[:d];m1=f[d:]
 p0=block_diag(root(m0@m0.T.conj()),root(m0.T.conj()@m0))/np.sqrt(2)
 p1=block_diag(root(m1@m1.T.conj()),root(m1.T.conj()@m1))/np.sqrt(2)
 cp=2*np.trace(p0@p1).real; weight=c/cp
 a=block_diag(weight*p0@p0, np.diag([(1-weight)/2,0]))
 b=block_diag(weight*p1@p1, np.diag([0,(1-weight)/2]))
 o=block_diag(weight*p0@p1,np.zeros((2,2)))
 return np.block([[a,o],[o.T.conj(),b]])
def mix(w,c):
 d=len(w)//2;tr=np.kron(np.array([[1,c],[c,1]])/2,np.eye(d)/d)
 grid=np.r_[0,np.geomspace(1e-12,0.1,30),np.linspace(.1,1,30)]
 vals=[cmi((1-t)*w+t*tr) for t in grid]; j=int(np.argmin(vals));t=grid[j]
 if 0<j<len(grid)-1:
  res=minimize_scalar(lambda t:cmi((1-t)*w+t*tr),bounds=(grid[j-1],grid[j+1]),method='bounded',options={'xatol':1e-13})
  if res.fun<vals[j]:t=res.x
 return (1-t)*w+t*tr,t
if __name__=='__main__':
 for c in [.01,.05,.1,.2,.4,.6,.8,.95]:
  a=(1+np.sqrt(1-c*c))/2;b=1-a;ef=h(np.array([a,b]));ed=1-h(np.array([(1+c)/2,(1-c)/2]))
  p0=np.diag(np.sqrt([a,b])/np.sqrt(2));p1=np.diag(np.sqrt([b,a])/np.sqrt(2));w=np.block([[p0@p0,p0@p1],[p1@p0,p1@p1]])
  print('START',c,ef+ed,cmi(w),flush=True)
  for it in range(4):
   w,t=mix(w,c);val=cmi(w);print(c,it,len(w)//2,t,val,'gap',val-ef-ed,flush=True)
   if val<ef+ed-1e-8:np.savez('/workspace/shared/broadcast_inequality/binary_witness.npz',w=w,c=c)
   if it<3:w=sym(w,c)
