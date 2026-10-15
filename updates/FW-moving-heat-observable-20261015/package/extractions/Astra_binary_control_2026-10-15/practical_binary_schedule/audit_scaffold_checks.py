"""Independent exact checks; reads receipts without importing their generators."""
import json,itertools
import sympy as sp
from pathlib import Path
P=Path(__file__).resolve().parent
w=json.loads((P/'rank_witness.json').read_text()); prime=w['prime']
assert sp.isprime(prime)
a=sp.Matrix(w['a']); B=sp.Matrix(w['B']); rows=[]
for T in w['row_subsets_zero_indexed']:
 M=sp.eye(len(T))+B.extract(T,T)
 assert int(M.det())%prime
 v=M.inv()*sp.ones(len(T),1); u=M.T.inv()*a.extract(T,[0]); pos={i:k for k,i in enumerate(T)}
 rows.append([(-u[pos[i]]*v[pos[j]]) if i in pos and j in pos else 0 for i,j in w['column_order']])
A=[[int(sp.numer(x))*pow(int(sp.denom(x)),-1,prime)%prime for x in row] for row in rows]
det=1
for j in range(len(A)):
 pivot=next(i for i in range(j,len(A)) if A[i][j])
 if pivot!=j: A[j],A[pivot]=A[pivot],A[j];det=-det
 q=A[j][j];det=det*q%prime
 for i in range(j+1,len(A)):
  c=A[i][j]*pow(q,-1,prime)%prime
  for k in range(j,len(A)):A[i][k]=(A[i][k]-c*A[j][k])%prime
assert det==w['minor_determinant_mod_prime']==473745
# Verify pair equation by symbolic cross multiplication with independent letters.
x,y,z,h,alpha,delta,r,s,p,q,d,e=sp.symbols('x y z h alpha delta r s p q d e')
N=d*delta*p+e*alpha*q-d*(x-r)*q-e*(y-s)*p
D=alpha*delta-(x-r)*(y-s)
L=(h*s+d*q)*x+(h*r+e*p)*y-h*x*y
R=d*delta*p+e*alpha*q+d*r*q+e*s*p-h*(alpha*delta-r*s)
assert sp.expand((L-R)-(h*D-N))==0
# Weighted transpose and all-subset nonsingularity are exact identities.
B=sp.Matrix([[0,sp.Rational(1,5),sp.Rational(1,7)],[sp.Rational(2,7),0,sp.Rational(1,9)],[sp.Rational(1,6),sp.Rational(1,8),0]])
a=sp.Matrix([1,2,3]); W=sp.diag(*a); Bt=W.inv()*B.T*W
for size in range(1,4):
 for T in itertools.combinations(range(3),size):
  M=sp.eye(size)+B.extract(T,T);Mt=sp.eye(size)+Bt.extract(T,T);at=a.extract(T,[0]);one=sp.ones(size,1)
  assert M.det()==Mt.det()!=0
  assert (at.T*M.inv()*one)[0]==(at.T*Mt.inv()*one)[0]
# Entrywise nonnegativity survives positive a; internal-state positivity need not.
B=sp.Matrix([[0,sp.Rational(1,5)],[sp.Rational(1,5),0]]);W=sp.diag(1,10);Bt=W.inv()*B.T*W
v=(sp.eye(2)+B).inv()*sp.ones(2,1); vt=(sp.eye(2)+Bt).inv()*sp.ones(2,1)
assert list(v)==[sp.Rational(5,6)]*2
assert list(vt)==[-sp.Rational(25,24),sp.Rational(49,48)]
print('PASS: independent modular minor 473745; symbolic pair equation; weighted transpose; positivity counterexample.')
