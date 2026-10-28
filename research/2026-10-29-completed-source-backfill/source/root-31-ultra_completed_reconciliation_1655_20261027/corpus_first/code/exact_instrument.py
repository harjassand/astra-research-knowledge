"""Exact rational controlled instrument. J(T)=sum_ij |i><j| tensor T(|i><j|)."""
import sys
sys.dont_write_bytecode=True
from itertools import product
import sympy as S
I=S.I
R=S.Rational
D=3
s=2*D-1

def rotation(i,j,c,t):
 U=S.eye(D); U[i,i]=U[j,j]=c; U[i,j]=-t; U[j,i]=t
 return U

def clean(M): return M.applyfunc(S.expand)
def projector(v): return clean(v*v.H)
def key(M): return tuple(M)
def phi(X): return clean((2*S.trace(X)*S.eye(D)-X.T)/s)
def branch(A,X): return phi(A*X*A.H)
def choi(T):
 C=S.zeros(D*D)
 for i in range(D):
  for j in range(D):
   E=S.zeros(D); E[i,j]=1
   C+=S.kronecker_product(E,T(E))
 return clean(C)
def partial_transpose(C):
 return S.Matrix(D*D,D*D,lambda r,c:C[(r//D)*D+c%D,(c//D)*D+r%D])

def model():
 d0=S.diag(R(3,5),R(5,13),R(8,17))
 d1=S.diag(R(4,5),R(12,13),R(15,17))
 assert d0*d0+d1*d1==S.eye(D)
 U=[rotation(0,1,R(3,5),R(4,5)),
    rotation(1,2,R(5,13),R(12,13))*S.diag(1,I,1),
    rotation(0,2,R(8,17),R(15,17))*S.diag(I,1,1),
    rotation(0,1,R(5,13),R(12,13))*rotation(1,2,R(3,5),R(4,5))]
 V=[S.eye(D),rotation(0,2,R(20,29),R(21,29))*S.diag(1,I,1)]
 out=[]
 for x in range(2):
  for a,diag in enumerate((d0,d1)):
   u=clean(U[2*x+a]); v=clean(V[x]); A=clean(u*diag*v)
   assert u.H*u==S.eye(D) and v.H*v==S.eye(D)
   out.append(dict(x=x,a=a,U=u,V=v,diag=diag,A=A))
 for x in range(2):
  assert clean(sum((v['A'].H*v['A'] for v in out if v['x']==x),S.zeros(D)))==S.eye(D)
 return out

def phase_vectors():
 return [S.Matrix([1,*[I**k for k in ks]]) for ks in product(range(4),repeat=D-1)]

def holevo(first,last):
 """Exact pairs (E,sigma) for T_last T_first(X)=sum sigma tr(E X)."""
 diag=last['diag']; total=S.trace(diag*diag)
 transform=clean(first['A'].T*last['V'].H)
 output=last['U'].conjugate()
 terms=[]
 phases=phase_vectors()
 for z in phases:
  p=clean(transform*diag*z)
  q=clean(output*z.conjugate())
  E=clean(R(D,len(phases)*s*s)*projector(p.conjugate()))
  sigma=clean(projector(q)/D)
  terms.append((E,sigma))
 for i in range(D):
  for j in range(D):
   ai=diag[i,i]; aj=diag[j,j]
   coeff=4*total-2*ai*ai-2*aj*aj-(ai*ai if i!=j else 0)
   assert coeff>0
   p=transform[:,i]; q=output[:,j]
   terms.append((clean(coeff*projector(p.conjugate())/(s*s)),projector(q)))
 return terms
