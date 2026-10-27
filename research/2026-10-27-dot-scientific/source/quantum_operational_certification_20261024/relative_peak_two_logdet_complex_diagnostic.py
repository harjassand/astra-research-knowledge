import numpy as np
from scipy.optimize import minimize
r=np.random.default_rng(270452)
best=(1,None)
for d in [3,4,6]:
 n=3*d
 def E(A):return np.kron(np.eye(3),np.einsum('aiaj->ij',A.reshape(3,d,3,d))/3)
 def PT(A):return A.reshape(3,d,3,d).transpose(2,1,0,3).reshape(n,n)
 def N(A):return (3*E(A)-PT(A))/2
 for radius in [.25,.75,.999999]:
  def fun(x):
   Z=x[:n*n].reshape(n,n)+1j*x[n*n:].reshape(n,n);B=(Z+Z.conj().T)/2;B-=E(B);e,v=np.linalg.eigh(B);i=np.argmax(abs(e));m=abs(e[i]);A=radius*B/m
   Y=np.eye(n)+N(A);X=np.eye(n)+A
   value=2*np.linalg.slogdet(Y)[1]-np.linalg.slogdet(X)[1];G=2*N(np.linalg.inv(Y))-np.linalg.inv(X)
   gm=np.sign(e[i])*np.outer(v[:,i],v[:,i].conj());grad=radius/m*G-radius/m**2*np.vdot(G,B).real*gm;grad-=E(grad)
   return value,np.r_[grad.real.ravel(),grad.imag.ravel()]
  for j in range(5):
   x=r.normal(size=2*n*n);res=minimize(fun,x,jac=True,method='L-BFGS-B',options={'maxiter':500,'ftol':1e-12,'gtol':1e-8})
   if res.fun<best[0]:best=(res.fun,(d,radius));np.savez('/tmp/reverse_logdet_complex_best.npz',d=d,radius=radius,x=res.x)
   print(d,radius,j,res.fun,flush=True)
print('best',best)
