import sympy as S
q=S.Rational; I=S.eye(2)
x,y=S.symbols('x y',positive=True); z=1-x-y; p=S.Matrix([x,y,z]); Q=S.Matrix([[1,0],[0,1],[-1,-1]])
M=S.diag(1/x,1/y,1/z)-2*S.eye(3)-2*p*p.T/(1-(p.T*p)[0]); C=S.simplify(Q.T*M*Q); s2=x*y+x*z+y*z
assert S.factor(C.det()-1/s2)==0
assert S.factor(C[0,0]-y*(x+z)*(x+z-3*x*z)/(x*z*s2))==0
# Independently assembled exact finite coherent-flag fixture.
pauli=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-S.I],[S.I,0]]),S.diag(1,-1)]
sigma=[(I+q(3,5)*v)/2 for v in pauli]
vs=[S.Matrix([q(2,3),q(2,3)]),S.Matrix([q(1,3),-q(2,3)]),S.Matrix([-q(2,3),q(1,3)])]
zv=[a*v for a,v in zip([q(1,3),q(2,3),q(2,3)],vs)]
R=[(v*v.T+I/1000)/q(1003,1000) for v in vs]
B=[S.diag(r,q(1,3000)) for r in R]
H=[S.zeros(2).row_join(v).col_join(v.T.row_join(S.zeros(1))) for v in zv]
assert sum(B,S.zeros(3))==S.diag(1,1,q(1,1000))
assert sum(H,S.zeros(3))==S.zeros(3)
def metric(A,H):
 n=A.rows
 # Solve the FULL Sylvester equation, with no off-diagonal reduction.
 L=S.kronecker_product(S.eye(n),A)+S.kronecker_product(A.T,S.eye(n))
 hv=S.Matrix([H[i,j] for j in range(n) for i in range(n)])
 sol=L.inv()*2*hv
 return S.factor((hv.conjugate().T*sol)[0])
E=sum(metric(b,h) for b,h in zip(B,H))
A=sum((S.kronecker_product(s,b) for s,b in zip(sigma,B)),S.zeros(6))
Ht=sum((S.kronecker_product(s,h) for s,h in zip(sigma,H)),S.zeros(6))
N=metric(A,Ht); gap=S.factor(N-q(6,25)*E)
assert gap>0
for b,h in zip(B,H):
 for sign in [-1,1]:
  C=b+sign*h/10000
  assert all(C[:k,:k].det()>0 for k in range(1,4))
print('ordinary compressed identities PASS')
print('Full Sylvester exact ratio',S.factor(N/E),float(N/E))
print('raw SLD gap',gap)
print('normalized balanced binary MMSE advantage',S.factor(gap/q(2001,1000)/10**8))
