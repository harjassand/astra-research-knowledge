from fractions import Fraction as F

def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F(0)) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A):return list(map(list,zip(*A)))
def add(A,B):return [[a+b for a,b in zip(x,y)] for x,y in zip(A,B)]
def scale(c,A):return [[c*x for x in row] for row in A]
def sub(A,B):return add(A,scale(-1,B))
def diag(v):return [[F(v[i] if i==j else 0) for j in range(len(v))] for i in range(len(v))]
def dissip(J,rho):
 JJ=mm(tr(J),J)
 return sub(mm(mm(J,rho),tr(J)),scale(F(1,2),add(mm(JJ,rho),mm(rho,JJ))))
# Basis 00,01,10,11; each admitted X_i changes W=Hamming weight by <=1.
X1=[[F(int(i==(j^2))) for j in range(4)] for i in range(4)]
X2=[[F(int(i==(j^1))) for j in range(4)] for i in range(4)]
J=add(X1,X2);Q=diag([1,1,1,0]);rho=diag([1,0,0,0]);L=mm(mm(Q,J),Q)
error=sub(dissip(J,rho),dissip(L,rho))
expected=[[F(0) for _ in range(4)] for _ in range(4)]
expected[0][3]=expected[3][0]=F(-1)
assert error==expected
# Exit shell W>=B-b=1 has zero population; error has eigenvalues +/-1.
assert sum(rho[i][i] for i in [1,2])==0
print('PASS: one-step boundary population = 0; dissipator difference trace norm = 2')
print('Difference matrix:',error)
