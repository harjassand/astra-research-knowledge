"""Exact unframed crossing pulses with actual pre/post detector records."""
import sympy as S
from itertools import product
I=S.eye(2);X=S.Matrix([[0,1],[1,0]]);Z=S.diag(1,-1);k=S.kronecker_product
N=S.eye(8);H=k(X,I,X);K=k(I,X,Z);ZA=k(Z,I,I);ZC=k(I,Z,I)
c=S.Rational(99,101);s=S.Rational(20,101)
R=c*N-S.I*s*H;T=c*N-S.I*s*K
PA=[(N+(-1)**i*ZA)/2 for i in range(2)];PC=[(N+(-1)**i*ZC)/2 for i in range(2)]
effects={(a,b):S.zeros(8) for a,b in product(range(2),repeat=2)};total=S.zeros(8)
for sa,sc,ta,tc in product(range(2),repeat=4):
 B=PC[tc]*T.H*PA[ta]*R.H*T*PC[sc]*R*PA[sa]
 E=B.H*B;total+=E;effects[ta^sa,tc^sc]+=E
 if ta!=sa:
  # Delete all A interactions, keeping B's full pulse and all record operations.
  deleted=PC[tc]*T.H*PA[ta]*T*PC[sc]*PA[sa]
  assert deleted==S.zeros(8)
 if tc!=sc:
  deleted=PC[tc]*PA[ta]*R.H*PC[sc]*R*PA[sa]
  assert deleted==S.zeros(8)
assert total==N
assert effects[1,1]==4*c**4*s**4*N
assert effects[1,0]+effects[1,1]==4*c*c*s**4*N
assert effects[0,1]+effects[1,1]==4*c*c*s**4*N
# For each pulse a_i=2 theta<2/5, so a_i²<4/25; use rational upper budgets.
p=S.Rational(4,25)
assert 4*c*c*s**4<=p and 4*c**4*s**4<=p*p
assert S.cancel((4*c**4*s**4)/(4*c*c*s**4))==c*c>p
print('PASS: no frames; complete actual pre/post instrument; all-input deletion-null identities; both marginal and joint action-budget effects; large completion conditional remains.')
