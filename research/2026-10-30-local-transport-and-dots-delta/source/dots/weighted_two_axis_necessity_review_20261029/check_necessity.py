import sympy as s,json,hashlib
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);ps=[X,Y,Z];W=s.Matrix([[1,s.Rational(1,4)],[s.Rational(1,4),1]]);J=s.Matrix([[-2,s.Rational(1,3)],[s.Rational(1,3),0]]);P=s.diag(1,0);scale=s.Rational(1,128)
ds=[scale*s.kronecker_product(X,2*W),scale*s.kronecker_product(Y,W),scale*s.kronecker_product(Z,J)]
def pt(a):return s.Matrix(2,2,lambda i,j:sum(a[2*i+k,2*j+k] for k in range(2)))
def rec(a):
 Q=s.kronecker_product(I,P);Q0=s.eye(4)-Q
 return pt(Q0*a*Q0)+X*pt(Q*a*Q)*X
fe0=s.Rational(1,4)+sum(s.trace(p*pt(d)) for p,d in zip(ps,ds))/8
fe1=s.Rational(1,4)+sum(s.trace(p*rec(d)) for p,d in zip(ps,ds))/8
assert fe1-fe0==s.Rational(1,256)
choi=s.eye(8)/8+sum((s.kronecker_product(p.T,d) for p,d in zip(ps,ds)),s.zeros(8))/4
lower=min(choi[i,i]-sum(abs(choi[i,j]) for j in range(8) if j!=i) for i in range(8));assert lower>0
assert W*J!=J*W
out=dict(F_extract=str(fe0),F_conditional_X=str(fe1),gain=str(fe1-fe0),choi_gershgorin_lower=str(lower),junk_commutes=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
