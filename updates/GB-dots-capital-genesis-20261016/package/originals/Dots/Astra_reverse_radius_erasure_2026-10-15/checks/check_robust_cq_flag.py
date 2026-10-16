import sympy as S
q=S.Rational; I=S.eye(2)
x,y=S.symbols('x y',positive=True); z=1-x-y; p=S.Matrix([x,y,z]); Q=S.Matrix([[1,0],[0,1],[-1,-1]])
M=S.diag(1/x,1/y,1/z)-2*S.eye(3)-2*p*p.T/(1-(p.T*p)[0]); C=S.simplify(Q.T*M*Q); s2=x*y+x*z+y*z
assert S.factor(C.det()-1/s2)==0
assert S.factor(C[0,0]-y*(x+z)*(x+z-3*x*z)/(x*z*s2))==0
# Independently assembled exact finite coherent-flag fixture.
pauli=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-S.I],[S.I,0]]),S.diag(1,-1)]
sigma=[(I+q(3,5)*v)/2 for v in pauli]
vs=[S.Matrix([88,88])/153,S.Matrix([32,-121])/153,S.Matrix([-121,32])/153]
zv=[a*v for a,v in zip([q(89,153),q(88,153),q(88,153)],vs)]
R=[(v*v.T+I/100)/q(103,100) for v in vs]
B=[S.diag(r,q(1,15)) for r in R]
H=[S.zeros(2).row_join(v).col_join(v.T.row_join(S.zeros(1))) for v in zv]
assert sum(B,S.zeros(3))==S.diag(1,1,q(1,5))
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
N=metric(A,Ht); gap=S.factor(N-q(1,5)*E)
assert gap>0
for b,h in zip(B,H):
 for sign in [-1,1]:
  C=b+sign*q(2,5)*h
  assert all(C[:k,:k].det()>0 for k in range(1,4))
print('ordinary compressed identities PASS')
print('Full Sylvester exact ratio',S.factor(N/E),float(N/E))
print('raw SLD gap',gap)
print('normalized balanced binary MMSE advantage',S.factor(gap*q(4,25)/q(11,5)))

for b,h in zip(B,H):
 for sign in [-1,1]:
  rho=(b+sign*q(2,5)*h)/q(11,5)
  for mat in [rho-S.eye(3)/250,S.eye(3)/3-rho]:
   assert all(S.factor(mat[:k,:k].det())>0 for k in range(1,4))
print('Exact eigenvalue bounds (1/250,1/3) PASS')
def receiver(a,h):
 n=a.rows; hv=S.Matrix([h[i,j] for j in range(n) for i in range(n)])
 sol=(S.kronecker_product(S.eye(n),a)+S.kronecker_product(a.T,S.eye(n))).inv()*2*q(2,5)*hv
 return S.Matrix(n,n,lambda i,j:sol[j*n+i])
def direct_moments(blocks):
 first=0;second=0
 for a,h in blocks:
  o=receiver(a,h); n=a.rows
  for label in [-1,1]:
   rho=(a+label*q(2,5)*h)/q(11,5)
   loss=(label*S.eye(n)-o)**2
   first+=S.trace(rho*loss)/2;second+=S.trace(rho*loss*loss)/2
 return S.factor(first),S.factor(second-first**2)
mt,vt=direct_moments([(A,Ht)])
source=[(b/5,h/5) for b,h in zip(B,H)]+[(q(4,5)*sum(B,S.zeros(3)),S.zeros(3))]
ms,vs=direct_moments(source)
assert S.factor(ms-mt-gap*q(4,25)/q(11,5))==0
assert vt+vs<q(77,200)
print('Direct conditional loss means/variances',float(mt),float(vt),float(ms),float(vs))
# High precision evaluation of integer sample thresholds.
v=q(77,200);g=q(157,20000);bound=q(53,25)
ns=S.N(2*(v+bound*g/3)*S.log(20)/g**2,60)
nc=S.N(8*(v+bound*g/6)*S.log(40)/g**2,60)
print('Bernstein real thresholds',ns,nc)
assert S.ceiling(ns)==37973 and S.ceiling(nc)==185705
