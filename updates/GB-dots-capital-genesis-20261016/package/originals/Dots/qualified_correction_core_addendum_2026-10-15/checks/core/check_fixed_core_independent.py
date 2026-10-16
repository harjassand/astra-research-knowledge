"""Exact independent fixed-core compiler check with two noncommuting bath-error segments."""
import sympy as S
I=S.eye(2);X=S.Matrix([[0,1],[1,0]]);Y=S.Matrix([[0,-S.I],[S.I,0]]);Z=S.diag(1,-1)
P=[I,X,Y,Z];k=S.kronecker_product
C=(X+Z)/S.sqrt(2) # endpoint Clifford H
c=S.Rational(99,101);s=S.Rational(20,101)
C1=c*I-S.I*s*X; C2=C*C1.H
N1=c*S.eye(4)-S.I*s*k(Z,X)
N2=c*S.eye(4)-S.I*s*k(Y,Z)
core=k(C2,I)*N2*k(C1,I)*N1
W=k(C.H,I)*core
assert S.simplify(core.H*core-S.eye(4))==S.zeros(4)
actual=[]
for T in P:
 wrapped=k(C*T.H*C.H,I)*core*k(T,I)
 assert S.simplify(wrapped-k(C,I)*k(T.H,I)*W*k(T,I))==S.zeros(4)
 actual.append(wrapped)
B=[]
for E in P:
 coeff=S.zeros(4)
 for T,wrapped in zip(P,actual):
  chi=S.trace(T.H*E*T*E)/2
  assert chi in (-1,1)
  coeff+=chi*wrapped/4
 ip=k(E.H*C.H,I)*coeff
 bath=S.Matrix(2,2,lambda a,b:S.simplify((ip[a,b]+ip[2+a,2+b])/2))
 assert S.simplify(coeff-k(C*E,bath))==S.zeros(4)
 B.append(bath)
assert S.simplify(sum((b.H*b for b in B),S.zeros(2))-I)==S.zeros(2)
effect=S.simplify(sum((b.H*b for b in B[1:]),S.zeros(2)))
q=S.Rational(16,101);gap=S.simplify(q*I-effect)
assert gap==gap.H and gap[0,0]>=0 and gap[1,1]>=0 and gap.det()>=0
print('PASS: same physical two-segment core for all frames; exact compiler equality; full Pauli Fourier factors C P tensor B; completeness and bad-effect bound.')
