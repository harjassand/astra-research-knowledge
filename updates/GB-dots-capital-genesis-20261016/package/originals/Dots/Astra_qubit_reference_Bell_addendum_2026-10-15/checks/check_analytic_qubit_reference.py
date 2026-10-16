import sympy as S
q=S.Rational; X=S.Matrix([[0,1],[1,0]]);Y=S.Matrix([[0,-S.I],[S.I,0]]);I=S.eye(2)
a=q(3,5);delta=q(1,16);t=q(6,25);reveal=q(1,5)
sig=[(I+a*X)/2,(I+a*Y)/2];B=S.diag(1,delta)/2;H=[X/2,-X/2]
def metric(A,H):
 n=A.rows;vec=S.Matrix([H[i,j] for j in range(n) for i in range(n)])
 sol=(S.kronecker_product(S.eye(n),A)+S.kronecker_product(A.T,S.eye(n))).inv()*2*vec
 return S.factor((vec.conjugate().T*sol)[0])
base=sum((S.kronecker_product(s,B) for s in sig),S.zeros(4))
tan=sum((S.kronecker_product(s,h) for s,h in zip(sig,H)),S.zeros(4))
E=sum(metric(B,h) for h in H);N=metric(base,tan);gap=S.factor(t*t*(N-reveal*E)/(1+delta))
assert gap==q(4276224,2244265625)
assert N/E==q(2601,12425)
for h in H:
 for sign in [-1,1]:
  rho=(B+sign*t*h)/(1+delta)
  assert rho.det()>0 and rho[0,0]>0
print('Independent full 4x4 Sylvester PASS',gap,float(gap))
c,r,x=S.symbols('c r x',positive=True)
f=(1-x)*(c/(1-c*x)-r)
assert S.simplify(S.diff(f,x)-(r-c*(1-c)/(1-c*x)**2))==0
print('Derivative identity PASS; second derivative =',S.factor(S.diff(f,x,2)))
