import sympy as s
import json
from pathlib import Path
D=3;eps=s.Rational(1,8);r=s.Rational(1,2)
N=s.Matrix([[0,1],[0,0]])
def channel(t):
 C=N+t*s.eye(2);R=r*s.eye(2)-eps*C.T*C
 def f(A):
  x=A[0,0];u=A[0:1,1:3];v=A[1:3,0:1];X=A[1:3,1:3]
  B=s.zeros(3);B[0,0]=x+(1-r)*s.trace(X)
  B[0:1,1:3]=eps*u*C.T;B[1:3,0:1]=eps*C*v
  B[1:3,1:3]=eps*C*X*C.T+s.trace(R*X)*s.eye(2)/2
  return B
 return f,C,R

def basis(i,j):
 A=s.zeros(D);A[i,j]=1;return A

def sup(f):
 return s.Matrix.hstack(*(s.Matrix(f(basis(i,j))).reshape(9,1) for i in range(D) for j in range(D)))

def choi(S):
 J=s.zeros(9)
 for i in range(D):
  for j in range(D):
   B=s.Matrix(S[:,D*i+j]).reshape(D,D)
   for a in range(D):
    for b in range(D):J[D*a+i,D*b+j]=B[a,b]
 return J

def pt(J):
 return s.Matrix(9,9,lambda ai,bj:J[D*(ai//D)+bj%D,D*(bj//D)+ai%D])

rows=[]
for t in [s.Rational(0),s.Rational(1,16),s.Rational(-1,16),s.Rational(1,4),s.Rational(-1,4)]:
 f,C,R=channel(t);S=sup(f);J=choi(S)
 assert J.is_positive_semidefinite
 assert R.is_positive_definite
 for i in range(D):
  for j in range(D):assert s.trace(f(basis(i,j)))==int(i==j)
 T=eps*C # row-coordinate convention
 assert (T*T==s.zeros(2))==(t==0)
 if t==0:
  assert pt(J).is_positive_semidefinite is False
  assert pt(choi(S*S)).is_positive_semidefinite
  for i in range(1,3):assert f(f(basis(0,i)))==s.zeros(3)
 else:
  assert T.det()!=0
  for n in range(1,9):assert T**n!=s.zeros(2)
 rows.append({'t':str(t),'choi_rank':J.rank(),'cross_eigenvalue':str(eps*t),'cross_nilpotent':t==0,'exact_eb_index':2 if t==0 else 'infinite_by_cross_certificate'})
out={'status':'PASS','arithmetic':'exact SymPy rational matrices','cases':rows,'scope':'Analytical positive decomposition proves EB at t=0; PPT alone is not used as a qutrit separability oracle.'}
Path(__file__).with_name('nonfaithful_boundary_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
