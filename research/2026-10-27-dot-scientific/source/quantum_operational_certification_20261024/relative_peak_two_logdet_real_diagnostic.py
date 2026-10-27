import numpy as np
from scipy.optimize import minimize
r=np.random.default_rng(270449)
best=(1,None)
for d in [2,3,4,6]:
 n=3*d
 def E(A):return np.kron(np.eye(3),np.einsum('aiaj->ij',A.reshape(3,d,3,d))/3)
 def PT(A):return A.reshape(3,d,3,d).transpose(2,1,0,3).reshape(n,n)
 def N(A):return (3*E(A)-PT(A))/2
 def fun(x):
  B=x.reshape(n,n);B=(B+B.T)/2;B-=E(B);e,v=np.linalg.eigh(B);i=np.argmax(abs(e));m=abs(e[i]);A=.999*B/m
  Y=np.eye(n)+N(A);X=np.eye(n)+A
  ly=np.linalg.slogdet(Y);lx=np.linalg.slogdet(X)
  if ly[0]<=0 or lx[0]<=0:raise RuntimeError('nonpositive source')
  value=2*ly[1]-lx[1];G=2*N(np.linalg.inv(Y))-np.linalg.inv(X)
  gm=np.sign(e[i])*np.outer(v[:,i],v[:,i]);grad=.999/m*G-.999/m**2*np.sum(G*B)*gm;grad-=E(grad)
  return value,grad.ravel()
 for j in range(10):
  x=r.normal(size=n*n);res=minimize(fun,x,jac=True,method='L-BFGS-B',options={'maxiter':400,'ftol':1e-12,'gtol':1e-8})
  if res.fun<best[0]:best=(res.fun,(d,res.x));np.savez('/tmp/reverse_logdet_best.npz',d=d,x=res.x)
  print(d,j,res.fun,flush=True)
print('best',best[0],best[1][0] if best[1] else None)
