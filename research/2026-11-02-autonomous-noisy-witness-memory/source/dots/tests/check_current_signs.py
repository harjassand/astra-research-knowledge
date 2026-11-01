import sympy as s
from itertools import combinations
I=s.eye(2); low=s.Matrix([[0,1],[0,0]]); up=low.T;n=up*low
W=s.kronecker_product(n,I);N=s.kronecker_product(I,n);Q=W+N
A=s.kronecker_product(low,up);C=s.I*(A-A.conjugate().T);H=A+A.conjugate().T
l=s.kronecker_product(I,low);eps=s.Rational(1,10);V=Q+eps*C
star=lambda X:s.I*(H*X-X*H)+l.conjugate().T*X*l-(l.conjugate().T*l*X+X*l.conjugate().T*l)/2

def psd(M):
 assert M==M.conjugate().T
 for r in range(1,M.rows+1):
  for ix in combinations(range(M.rows),r):assert s.simplify(M.extract(ix,ix).det())>=0
assert Q*A-A*Q==s.zeros(4)
assert Q*V-V*Q==s.zeros(4)
assert star(Q)==-N
assert star(C)==2*(A*A.conjugate().T-A.conjugate().T*A)-C/2
psd(V-s.Rational(9,10)*Q);psd(s.Rational(11,10)*Q-V)
psd(-star(V)-s.Rational(1,10)*Q)
print('PASS: exact rational/imaginary current sign, Q conservation, comparability, and mean-drift inequalities')
