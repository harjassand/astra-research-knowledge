import sympy as s
from sympy.matrices import Matrix, eye, zeros, kronecker_product
from sympy.polys.matrices import DomainMatrix
from sympy.polys.domains import QQ
D=5
rt5=s.sqrt(5)
zeta=(rt5-1)/4 + s.I*s.sqrt(10+2*rt5)/4
X=Matrix([[int(j==(i+1)%D) for j in range(D)] for i in range(D)])
Z=Matrix.diag(*[zeta**j for j in range(D)])
I=eye(D)
lines=[(0,1)]+[(1,k) for k in range(D)]
modes=[((a*t)%D,(b*t)%D) for a,b in lines for t in (1,2)]
sel=[1,2,4,7,9,11]
ix=[D*D*r+D*a+b for r in range(D) for a in range(D) for b in range(D) if (a+b-r)%D==0]
H=zeros(D**3)
for i in sel:
 a,b=modes[i]
 W=X**a * Z**b
 Wd=W.conjugate().T
 H += kronecker_product(W.T,Wd,I)+kronecker_product(Wd.T,W,I)
 H += kronecker_product(W.T,I,Wd)+kronecker_product(Wd.T,I,W)
block=H.extract(ix,ix)
assert H == H.conjugate().T
assert block == block.conjugate().T
# The joint displacement symmetry preserves charge c=a+b-r. Check the exact
# block decomposition here; equivalence of the five blocks follows from the
# simultaneous X translation, which shifts c by one and commutes with H.
charges=[(a+b-r)%D for r in range(D) for a in range(D) for b in range(D)]
for rix in range(D**3):
 for cix in range(D**3):
  if charges[rix] != charges[cix]:
   assert H[rix,cix] == 0
print('block size',block.shape,'basis order',ix)
K=QQ.algebraic_field(zeta)
dm=DomainMatrix.from_Matrix(block).convert_to(K)
coeffs=dm.charpoly()
x=s.symbols('x')
poly=s.Poly.from_list([K.to_sympy(c) for c in coeffs],gens=x,extension=zeta)
expr=s.factor(poly.as_expr(),extension=zeta)
print('charpoly',expr)
val=s.simplify(expr.subs(x,14))
expected= -s.Integer(1142640210879492187500000000) - s.Integer(386433515975976562500000000)*rt5
assert s.simplify(val-expected) == 0
assert 1142640210879492187500000000 > 0 and 386433515975976562500000000 > 0 and rt5 > 0
p3=x**3-12*x**2+x*(-s.Rational(169,2)+s.Rational(5,2)*rt5)-60*rt5+716
assert s.simplify(s.factor(expr / ((x+1)**8*(x+1+rt5)**4*(x-rt5+1)**4
    *(x**2-8*x-s.Rational(33,2)+s.Rational(5,2)*rt5)
    *(x**2+2*x-s.Rational(63,2)-s.Rational(5,2)*rt5)**2))-p3) == 0
assert s.simplify(p3.subs(x,14)) == -75-25*rt5
assert s.simplify(p3.subs(x,15)) == s.Rational(247,2)-s.Rational(45,2)*rt5
assert s.simplify(s.diff(p3,x).subs(x,14)) == s.Rational(335,2)+s.Rational(5,2)*rt5
print('p14 simplified',s.simplify(val))
print('cubic factor at 14,15 and derivative at 14',p3.subs(x,14),p3.subs(x,15),s.diff(p3,x).subs(x,14))
print('p14 numeric',s.N(val,30))
