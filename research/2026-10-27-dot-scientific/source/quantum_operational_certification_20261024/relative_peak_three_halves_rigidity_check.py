import sympy as s
from pathlib import Path
import json
a,b,c=s.symbols('a b c',nonnegative=True)
I=s.eye(9); swap=s.zeros(9)
for i in range(3):
 for j in range(3): swap[3*j+i,3*i+j]=1
Ps=(I+swap)/2; Pa=(I-swap)/2

def trA(X):
 return s.Matrix(3,3,lambda i,j:sum(X[3*k+i,3*k+j] for k in range(3)))
def pt(X):
 return s.Matrix(9,9,lambda i,j:X[3*(j//3)+i%3,3*(i//3)+j%3])
def N(X): return (s.kronecker_product(s.eye(3),trA(X))-pt(X))/2
B=s.zeros(9)
for weight,(i,j) in zip([a,b,c],[(0,1),(0,2),(1,2)]):
 v=s.zeros(9,1);v[3*i+j]=1;v[3*j+i]=-1
 B+=weight*v*v.T/2
T=s.kronecker_product(s.eye(3),trA(B))-B
block=T.extract([1,3],[1,3])
assert s.simplify(block.det()-(b*c-a*a)/4)==0
phi=s.zeros(9,1)
for i in range(3):phi[3*i+i]=1
assert N(Ps)==s.Rational(3,4)*(I-phi*phi.T/3)
assert trA(Pa)==s.eye(3) and trA(Ps)==2*s.eye(3)
report={'status':'PASS','principal_block':str(block),'determinant':str(s.factor(block.det())),'actual_output_identity':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
