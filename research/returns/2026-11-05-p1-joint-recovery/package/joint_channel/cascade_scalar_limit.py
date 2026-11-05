from pathlib import Path
HERE=Path(__file__).resolve().parent
import numpy as np
from math import factorial
from fractions import Fraction
from itertools import permutations
from scipy.linalg import expm

I=np.eye(2,dtype=complex); pauli=[I,np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
def tensor(q):
 r=np.array([[1.]],complex)
 for A in q:r=np.kron(r,A)
 return r

def swap(n,i,j):
 d=2**n; P=np.zeros((d,d),complex)
 for x in range(d):
  y=x
  if ((x>>(n-1-i))&1)!=((x>>(n-1-j))&1):y=x^(1<<(n-1-i))^(1<<(n-1-j))
  P[y,x]=1
 return P

def dot(n,i,j):
 R=np.zeros((2**n,2**n),complex)
 for a in range(1,4):
  z=[I]*n;z[i]=pauli[a];z[j]=pauli[a];R+=tensor(z)
 return R

def chir(n,i,j,k):
 R=np.zeros((2**n,2**n),complex)
 for a,b,c in permutations([1,2,3]):
  sign=1 if (a,b,c) in [(1,2,3),(2,3,1),(3,1,2)] else -1
  z=[I]*n;z[i]=pauli[a];z[j]=pauli[b];z[k]=pauli[c];R+=sign*tensor(z)
 return R

B=[np.eye(8,dtype=complex),dot(3,0,1),dot(3,0,2),dot(3,1,2),chir(3,0,1,2)]
norm=np.array([np.vdot(x,x).real for x in B]);M=[]
for b in B:
 A=[np.kron(I,b)]+[np.zeros((16,16),complex) for _ in range(4)]
 for j in range(1,4):
  P=swap(4,0,j)
  C=[np.zeros((16,16),complex) for _ in range(5)]
  for p in range(5):
   D=A[p].copy()
   for q in range(5-p):
    if q:D=1j*(P@D-D@P)
    C[p+q]+=D/factorial(q)
  A=C
 vals=[]
 for X in A:
  O=(X[:8,:8]+X[8:,8:])/2
  vals.append(np.array([np.vdot(bi,O)/ni for bi,ni in zip(B,norm)]))
 M.append(vals)
M=np.array(M).transpose(1,2,0)
for p in range(5):
 print('order',p)
 for row in M[p]:print([str(Fraction(float(v.real)).limit_denominator()) if abs(v.imag)<1e-10 else str(v) for v in row])
G=M[4].real
for t in [.1,.3,1.,3.]:
 U=expm(t*G);x=U[3,2];z=U[3,1];y=U[3,4]
 a=(x*x+z*z)/9+y*y/36
 print('t',t,'components',x,y,z,'a',a)
np.save(HERE / 'cascade_three_spin_generator.npy',G)
