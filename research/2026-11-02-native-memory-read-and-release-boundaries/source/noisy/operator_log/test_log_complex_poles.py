import numpy as np
from scipy.linalg import eigh
I=np.eye(2); X=np.array([[0.,1.],[1.,0.]]); Z=np.diag([1.,-1.]); Y=np.array([[0.,-1j],[1j,0.]])
def op(n,items):
 A=np.array([[1.]])
 for j in range(n): A=np.kron(A,items.get(j,I))
 return A
for n in range(2,10):
 H=sum((.91+.013*(j%3))*op(n,{j:Z})+(.67+.007*(j%2))*op(n,{j:X}) for j in range(n))
 H+=sum(.43*op(n,{j:Z,j+1:Z})+.19*op(n,{j:X,j+1:Z}) for j in range(n-1))
 E,U=eigh(H); P=U.T@op(n,{n//2:Z})@U
 a=0;b=len(E)-1; D=E[a]-E[b]; z=2j*np.pi/D
 numerator=np.sum(P[a,:]*np.exp(-z*E)*P[:,b]); residue=-z*np.exp(z*E[a])*numerator
 print(n,'width',E[-1]-E[0],'pole_modulus',abs(z),'numerator',abs(numerator),'residue',abs(residue),flush=True)
