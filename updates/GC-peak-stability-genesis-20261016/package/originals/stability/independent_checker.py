import json, sympy as S, hashlib
from fractions import Fraction
C=json.load(open('certificate.json'))
# Certificate data only. Reconstruct all expressions locally, not from producer code/strings.
r,a,b,c,d,s=S.symbols('r a b c d s')
Q=S.Matrix([[S.Rational(Fraction(x).numerator,Fraction(x).denominator) for x in row] for row in C['gram']])
z0=S.Matrix([a*d-b*c+s*(a+d),r*c*s,r*c*d,r*c*c,r*b*c,r*a*s,r*a*d,r*a*c,r*a*b,r*a*a])
z1=S.Matrix([d*s,d*d,c*s,c*d,c*c,b*d,b*c,b*b,a*s,a*d,a*c,a*b,a*a,r*(a*a+2*a*s+c*c),r*a*s,r*c*s])
u=(a+s)**2+c*c;v=b*b+(d+s)**2;j=(a+s)*(d+s)-b*c
J=3*r*S.Rational(1,8)/(r+2)*(u+v-2*j)**2+r*(r-1)*u*u/6+j*j+r*u*j
s1=-(r+2)*s*s*b+7*r*b**3/(6*(r+2))
s2=(r+2)*s**3+(5*r/2+2)*s*s*a+7*r*s*a*a/4+r*(4*r+3)*a**3/(12*(r+2))
G=J-(r+2)*(r+3)*s**4/6-(r+2)*(2*r+3)*s**3*a/3-s1*c-s2*d
expr=S.cancel((r+2)*G-(z0.T*Q[:10,:10]*z0)[0]-r*(z1.T*Q[10:,10:]*z1)[0])
print('Exact identity zero:',expr==0)
for name,M in [('Q0',Q[:10,:10]),('Q1',Q[10:,10:]),('Q1-floor',Q[10:,10:]-S.eye(16)/512)]:
 L,D=M.LDLdecomposition(hermitian=False)
 print(name,'all positive pivots:',all(D[i,i]>0 for i in range(M.rows)),'reconstruction:',L*D*L.T==M)
print('Cross blocks zero:',Q[:10,10:]==S.zeros(10,16))
K=S.factor(S.diff(s1,b)+S.diff(s2,a));print('Divergence coefficient:',K)
# independent one phase test f=sin(x+y), g=-f; averaged cos^2=1/2, cos^4=3/8
q=S.symbols('q')
E=S.Poly(S.cancel((G+s1*c+s2*d).subs({a:q,b:q,c:-q,d:-q})),q)
avg=lambda poly: S.factor(sum(coef*({0:1,2:S.Rational(1,2),4:S.Rational(3,8)}.get(exp[0],0)) for exp,coef in poly.terms()))
print('One-phase actual energy:',avg(E))
print('One-phase stress pairing:',avg(S.Poly((s1*c+s2*d).subs({a:q,b:q,c:-q,d:-q}),q)))
print('sha256',hashlib.sha256(open('certificate.json','rb').read()).hexdigest())
assert expr == 0
assert Q[:10,10:] == S.zeros(10,16)
for mat in [Q[:10,:10],Q[10:,10:],Q[10:,10:]-S.eye(16)/512]:
    L,D=mat.LDLdecomposition(hermitian=False)
    assert L*D*L.T==mat
    assert all(D[i,i]>0 for i in range(mat.rows))
B=((r+1)*a+d)**2+r*(r+2)*c*c/3
P=r*(d+(2*r+1)*a/3)*(a*a+c*c)+2*(a*d-b*c)*((r+1)*a+d)
u0=a*a+c*c;v0=b*b+d*d;j0=a*d-b*c
Qpoly=3*r*(u0+v0-2*j0)**2/(8*(r+2))+r*(r-1)*u0*u0/6+j0*j0+r*u0*j0
# Integrated acoustic polynomial differs pointwise by the null determinant.
assert S.cancel(J-(r+2)*(r+3)*s**4/6-(r+2)*(2*r+3)*s**3*a/3-(r+2)*s**3*d-s*s*(B+(r+2)*j0)-s*P-Qpoly)==0
expected=[2*(r+1)*(r+2),2*(r+2)*(4*r+9)/3,4*(r**3+7*r*r+34*r+12)/(3*(r+2))]
for polynomial, bound in zip([B,P,Qpoly],expected):
    coeffs=[S.factor(co) for z in [a,b] for _,co in S.Poly(S.diff(polynomial,z),a,b,c,d).terms()]
    # Verify each signed coefficient is positive on r>0 by checking positive polynomial coefficients after clearing r+2.
    positive=[]
    for co in coeffs:
        signed=co if co.subs(r,1)>0 else -co
        num,den=S.fraction(S.factor(signed))
        assert all(x>=0 for x in S.Poly(num,r).all_coeffs())
        assert all(x>=0 for x in S.Poly(den,r).all_coeffs())
        positive.append(signed)
    assert S.cancel(sum(positive)-bound)==0
assert S.Rational(3000,20000000)<S.Rational(1,6144)
print('Stability coefficient sums, acoustic expansion, rational example: PASS')
