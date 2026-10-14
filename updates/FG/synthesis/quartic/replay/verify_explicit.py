"""Independent exact verification of the explicit compatible-heat certificate."""
from pathlib import Path
import json
import sympy as s
R=s.Rational
a,b,c,d=s.symbols('a b c d')
h0,h1,h2,h3,h4,h5=s.symbols('h0 h1 h2 h3 h4 h5')
A=s.Matrix([a,b,c,d]);H1=s.Matrix([h0,h1,h3,h4]);H2=s.Matrix([h1,h2,h4,h5])
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
F=u*u+v*v+4*w*w+R(7,2)*q*q-R(29,10)*q*(u+v)
S=s.Matrix([[12,R(13,5),R(54,5),-R(23,5),R(87,10),R(13,10)],
[R(13,5),8,R(26,5),R(8,5),3,R(29,10)],
[R(54,5),R(26,5),R(74,5),-R(73,10),R(37,5),R(6,5)],
[-R(23,5),R(8,5),-R(73,10),R(43,5),-R(11,5),R(16,5)],
[R(87,10),3,R(37,5),-R(11,5),7,R(6,5)],
[R(13,10),R(29,10),R(6,5),R(16,5),R(6,5),4]])
alpha=s.Matrix([0,
R(26,15)*a**3-R(43,10)*a*a*d+R(26,5)*a*b*b+R(43,5)*a*b*c+R(12,5)*a*c*c+R(12,5)*a*d*d,
R(41,15)*a**3-a*a*d+R(13,5)*a*b*b+2*a*b*c+R(41,5)*a*c*c+R(13,5)*a*d*d-R(7,5)*b*b*d-R(17,5)*b*c*d,
-R(17,10)*a*a*b+R(7,5)*a*a*c+R(14,5)*a*b*d-R(17,5)*a*c*d+R(41,15)*b**3+b*b*c+R(13,5)*b*c*c+R(41,5)*b*d*d+R(26,15)*c**3+R(26,5)*c*d*d])
x=s.Matrix([a,c]);y=s.Matrix([b,d]);X=s.Matrix([h0,h3]);Y=s.Matrix([h1,h4]);Z=s.Matrix([h2,h5])
def cross(x,y):return x[0]*y[1]-x[1]*y[0]
zp=s.Matrix([x.dot(X),x.dot(Z),y.dot(Y),cross(x,Y),cross(y,X),cross(y,Z)])
zm=s.Matrix([-y.dot(Z),-y.dot(X),-x.dot(Y),cross(y,Y),cross(x,Z),cross(x,X)])
H=s.hessian(F,A)
E=(H1.T*H*H1+H2.T*H*H2)[0]
Da=alpha.jacobian(A)
theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c]);theta_a=s.Matrix([-c,d,a,-b])
compact=(R(37,40)*(u+v)+q/5)*theta+(R(13,10)*(u+v)-3*q)*zeta+R(9,8)*(u-v)*theta_a
Dc=compact.jacobian(A)
assert ((Dc.T-Dc)-(Da.T-Da)).applyfunc(s.expand)==s.zeros(4)
# d alpha(U,V)=U^T(Dalpha^T-Dalpha)V for column coefficients alpha.
exterior=(H1.T*(Da.T-Da)*H2)[0]
identity=s.expand(E+exterior-(zp.T*S*zp+zm.T*S*zm)[0])
assert identity==0,identity
normidentity=s.expand(zp.dot(zp)+zm.dot(zm)-(u+v)*(X.dot(X)+Y.dot(Y)+Z.dot(Z)))
assert normidentity==0
records={'polynomial_identity':True,'bilinear_norm_identity':True,'margins':{}}
for margin in [R(0),R(1,10),R(1,8),R(1,7)]:
 mat=S-margin*s.eye(6)
 minors=[s.factor(mat[:j,:j].det()) for j in range(1,7)]
 ispositive=all(x>0 for x in minors)
 records['margins'][str(margin)]={'positive_definite':bool(ispositive),'leading_principal_minors':list(map(str,minors))}
 print('margin',margin,'PD',ispositive,'minors',minors)
assert records['margins']['1/8']['positive_definite']
# Existing non-polyconvexity witness.
FI=F.subs({a:1,b:0,c:0,d:1});FJ=F.subs({a:1,b:0,c:0,d:-1})
expect=R(2,100)*7**4*FI+R(98,100)*FJ
assert FI==-R(3,10) and FJ==R(113,10) and expect==-R(833,250)
records['nonpolyconvex_witness']={'F(I)':str(FI),'F(J)':str(FJ),'expected_energy':str(expect)}
# Sharp fourth-power Bregman lower bound, algebraic square completion.
bv=s.Matrix(s.symbols('B0:4'));aa=A.dot(A);bb=bv.dot(bv);ab=A.dot(bv)
breg=s.expand((A+bv).dot(A+bv)**2-aa**2-4*aa*ab)
assert s.expand(breg-(R(1,3)*bb**2+6*(ab+bb/3)**2+2*(aa*bb-ab**2)))==0
records['fourth_power_bregman_identity']=True
out=Path(__file__).with_name('exact_verification.json');out.write_text(json.dumps(records,indent=2))
print('All independent exact checks passed. Output:',out)
