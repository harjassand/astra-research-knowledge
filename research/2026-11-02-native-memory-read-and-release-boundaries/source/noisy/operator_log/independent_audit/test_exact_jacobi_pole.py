"""Independent full physical-chain/block and meromorphic-germ checks; not preparation."""
import numpy as np
from scipy.linalg import eigh
I=np.eye(2); X=np.array([[0.,1.],[1.,0.]]); Z=np.diag([1.,-1.]); N=(I-Z)/2

def op(n,items):
 out=np.ones((1,1))
 for i in range(n):out=np.kron(out,items.get(i,I))
 return out
for n in range(2,8):
 g=.2
 A=sum(op(n,{i:N}) for i in range(n))
 for i in range(n):
  factors={i:X}
  if i>0:factors[i-1]=N
  if i<n-1:factors[i+1]=I-N
  A+=g*op(n,factors)
 P=op(n,{0:Z})
 ids=[((1<<j)-1)<<(n-j) for j in range(n+1)]
 V=np.eye(1<<n)[:,ids]
 J=np.diag(np.arange(n+1,dtype=float))+g*(np.eye(n+1,k=1)+np.eye(n+1,k=-1))
 PD=np.diag([1.]+[-1.]*n)
 assert np.linalg.norm(A@V-V@J)<1e-13
 assert np.linalg.norm(P@V-V@PD)<1e-13
 E,U=eigh(J);u=U[0,:];D=E[-1]-E[0]
 assert n-1e-12<=D<=n+4*g+1e-12
 z=2j*np.pi/D;lam=np.exp(-z*E[0]);M=np.dot(u*u,np.exp(-z*E))
 pe=U.T@PD@U
 B=(pe*np.exp(-z*E)[None,:])@pe
 predicted=4*u[0]*u[-1]*(M-lam)
 assert abs(B[0,-1]-predicted)<1e-13
 assert np.real(M/lam)<1 and abs(predicted)>0
 # Residue K'_ab=-z(Ea-Eb) B_ab/(lambda_a-lambda_b).
 residue=z*predicted/lam
 def derivative(w):
  b=((pe*np.exp(-w*E)[None,:])@pe)[0,-1]
  return w*D*b/(np.exp(-w*E[0])-np.exp(-w*E[-1]))
 errors=[abs(h*derivative(z+h)-residue)/abs(residue) for h in (1e-5,1e-6,1e-7)]
 assert errors[1]<.2*errors[0] and errors[2]<.2*errors[1]
 assert errors[-1]<2e-5
 print('relative pole-limit errors',errors)
 print(n,'width',D,'pole_modulus',abs(z),'phase_deficit',1-np.real(M/lam),'residue_abs',abs(residue))
print('PASS: exact-family full-chain invariance, Pauli restriction, residue identity, pole limit')
