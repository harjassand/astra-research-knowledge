from polyconvex_probe import *
J=np.diag([1.,1.,-1.,-1.])
def Hess(A):
 x,y,u,v=A;r=x*x+y*y;t=u*u+v*v;z=A[:2];w=A[2:]
 H=np.zeros((4,4));H[:2,:2]=(4*t+2*lam)*np.eye(2);H[2:,2:]=(4*(r+t)+2*lam)*np.eye(2)+8*np.outer(w,w)
 Dnu=np.array([[2*u,-2*v],[2*v,2*u]]);H[:2,2:]=8*np.outer(z,w)+Dnu;H[2:,:2]=H[:2,2:].T;H[2:,2:]+=np.array([[2*x,2*y],[2*y,-2*x]])
 return H
def interval(A):
 H=Hess(A);roots=np.linalg.eigvals(J@H/2);roots=sorted([rr.real for rr in roots if abs(rr.imag)<1e-7]);safe=[]
 for low,up in zip(roots,roots[1:]):
  if np.linalg.eigvalsh(H-(low+up)*J)[0]>-1e-8:safe.append((low,up))
 return safe
A=np.array([-.25,0,0,-.25]);print('A0 interval',interval(A));print('H eig',np.linalg.eigvalsh(Hess(A)))
