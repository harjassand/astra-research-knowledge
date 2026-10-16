"""Exact rational witness: bath filter obstructs a CPTP minorant."""
import sympy as s
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
B0=s.diag(1,0);B1=s.diag(0,1);kron=s.kronecker_product
c=s.Rational(99,101);t=s.Rational(20,101)
U=kron(I,B0)+kron(c*I-s.I*t*X,B1)
ZA=kron(Z,I)
U0=(U+ZA*U*ZA)/2;U1=(U-ZA*U*ZA)/2
A0=s.diag(1,c);A1=s.diag(0,-s.I*t)
assert U.H*U==s.eye(4)
assert U0==kron(I,A0) and U1==kron(X,A1)
assert A0.H*A0+A1.H*A1==I
assert A1.H*A1==s.diag(0,t*t)
# A0 is a single invertible Kraus with unequal singular values.
# Any CP map dominated by Ad_A0 has proportional rank-one Choi matrix,
# and so cannot be trace preserving.
v=s.Matrix([A0[0,0],A0[1,0],A0[0,1],A0[1,1]])
assert (v*v.H).rank()==1
assert A0.H*A0!=I and (A0.H*A0)[0,0]!=(A0.H*A0)[1,1]
print('PASS: exact joint twirl and instrument completeness.')
print('bad effect = diag(0,',t*t,'); norm-distance squared =',2-2*c)
print('rank-one Choi bath filter has unequal squared singular values:',1,c*c)
print('Therefore no positive common CPTP bath-channel minorant exists.')
