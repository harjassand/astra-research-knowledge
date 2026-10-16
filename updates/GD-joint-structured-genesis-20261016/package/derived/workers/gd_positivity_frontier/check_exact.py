"""Independent exact algebra checks. Does not execute any producer program."""
from pathlib import Path
from hashlib import sha256
import json
import sympy as S

HERE = Path(__file__).resolve().parent
r,h,x = S.symbols('r h x', positive=True)
sig = r+1
kap = r*(r+2)/3
al = 3*r/(8*(r+2))
be = r*(r-1)/6
t = (2*r+1)/3
a,b,c,d,s = S.symbols('a b c d s', real=True)
checks = []

def equal(name, lhs, rhs):
    residual = S.factor(lhs-rhs)
    assert residual == 0, (name, residual)
    checks.append(name)

def J(V, rr=r):
    aa,bb,cc,dd = V
    u = aa**2+cc**2
    v = bb**2+dd**2
    j = aa*dd-bb*cc
    return 3*rr/(8*(rr+2))*(u+v-2*j)**2 + rr*(rr-1)/6*u*u+j*j+rr*u*j

U = sig*a+d
j = a*d-b*c
P = 2*a*U**2-(r+2)*a*a*U+r*c*c*U-2*b*c*U-kap*a**3-kap*a*c*c
expansion = J([s+a,b,c,s+d])-J([s,0,0,s])
equal('full conformal expansion including null terms', expansion,
      J([a,b,c,d])+s*P+s*s*(U*U+kap*c*c+(r+2)*j)
      +s**3*(r+2)/3*((2*r+3)*a+3*d))

X,Y = S.symbols('X Y', real=True)
mx2,mx3,mx4,my2,my3,my4 = S.symbols('mx2 mx3 mx4 my2 my3 my4', real=True)
momx = {0:1,1:0,2:mx2,3:mx3,4:mx4}
momy = {0:1,1:0,2:my2,3:my3,4:my4}
def independent_average(poly):
    return sum(co*momx[i]*momy[jj] for (i,jj),co in S.Poly(S.expand(poly),X,Y).terms())

u0 = 1+sig*h
u1 = 2*(1-sig*h)
v0 = sig**2+sig/h
v1 = 2*(sig**2-sig/h)
uc = (X+Y)**2+sig*h*(X-Y)**2
vc = sig**2*(X+Y)**2+sig/h*(X-Y)**2
jc = -4*sig*X*Y
Jc = al*(uc+vc-2*jc)**2+be*uc**2+jc**2+r*uc*jc
L = al*u0**2*((sig/h)**2+2*sig/h+t*t)
K = al*(2*(u0+v0)**2+(u1+v1+8*sig)**2)+be*(2*u0*u0+u1*u1)+16*sig*sig-4*r*sig*u1
equal('characteristic quartic moment identity', independent_average(Jc),
      L*(mx4+my4)+K*mx2*my2)
Pc = -kap*(X+Y)*uc
equal('characteristic cubic moment identity', independent_average(Pc),
      -kap*(1+sig*h)*(mx3+my3))
equal('characteristic acoustic moment identity',
      independent_average(kap*sig*h*(X-Y)**2), kap*sig*h*(mx2+my2))

Kpos = r*sig**2*(2*r+1)**2/(4*(r+2))*h*h \
    +r*sig*(35*r*r+50*r+14)/(6*(r+2))*h \
    +9*r*sig**2/(4*(r+2))*(1/h-(r*r+10*r+10)/(3*sig))**2 \
    +sig*(4*r**4+28*r**3+95*r*r+133*r+64)/(2*(r+2))
equal('all-r interaction coefficient positive square identity', K,Kpos)
rho = 2*(r+2)**2*h/(9*sig*(sig*sig+2*sig*h+t*t*h*h))
equal('sharp restricted discriminant coefficient',
      kap**2*(1+sig*h)**2/(4*kap*sig*h*L),rho)
equal('all-h maximum denominator square identity',
      sig*sig+2*sig*h+t*t*h*h,(sig-t*h)**2+2*sig*h*(t+1))
equal('maximum restricted ratio', rho.subs(h,sig/t),(r+2)/(6*sig**2))
equal('strict one-third reserve numerator', 2*sig*sig-(r+2),r*(2*r+3))

pp = S.symbols('p', positive=True)
bern = {j:pp+(1-pp)*(-pp/(1-pp))**j for j in (2,3,4)}
equal('sharpness skew-profile moment ratio',bern[3]**2/(bern[2]*bern[4]),
      (1-2*pp)**2/(1-3*pp+3*pp*pp))
equal('sharpness ratio limit', S.limit(bern[3]**2/(bern[2]*bern[4]),pp,0,dir='+'),1)

k = S.symbols('k',positive=True)
out = S.Matrix([[1,1],[-sig/k,sig/k]])
inp = S.Matrix([[1,k],[1,-k]])
VV = S.Matrix([[X+Y,k*(X-Y)],[-sig/k*(X-Y),-sig*(X+Y)]])
assert S.simplify(out*S.diag(X,Y)*inp-VV) == S.zeros(2)
checks.append('invertible diagonal rank-one factorization')
equal('rank-one plane determinant',VV.det(),-4*sig*X*Y)
equal('plane acoustic cancellation',sig*VV[0,0]+VV[1,1],0)
equal('plane second constraint',VV[1,0]+sig/k**2*VV[0,1],0)

equal('r1 h2 L',L.subs({r:1,h:2}),S.Rational(25,2))
equal('r1 h2 K',K.subs({r:1,h:2}),169)
equal('r1 h2 rho',rho.subs({r:1,h:2}),S.Rational(1,8))
z = S.symbols('z')
profile = (z+1/z)/2+(z*z+1/(z*z))/4
profile_mom = {j:S.expand(profile**j).coeff(z,0) for j in (2,3,4)}
for j,val in zip((2,3,4),(S.Rational(5,8),S.Rational(3,8),S.Rational(99,128))):
    equal(f'exact trigonometric profile moment {j}',profile_mom[j],val)
aa = 4*2*profile_mom[2]
pc = -5*2*profile_mom[3]
qq = S.Rational(25,2)*2*profile_mom[4]+169*profile_mom[2]**2
equal('compatible example acoustic',aa,5)
equal('compatible example cubic',pc,-S.Rational(15,4))
equal('compatible example quartic',qq,S.Rational(10925,128))
equal('compatible example ratio',pc*pc/(4*aa*qq),S.Rational(18,2185))
equal('compatible example optimized energy',qq-pc*pc/(4*aa),S.Rational(10835,128))

# The minor-moment law: this is never labelled a gradient witness.
D = sig*x*x+h**3
wp = h**3/(2*D)
wq = sig*x*x/(2*D)
yy = -h**3/(sig*x)
H = S.diag(1,-sig)
B = S.Matrix([[0,h],[-h*h,0]])
atoms = [x*H,yy*H,B,-B]
weights = [wp,wq,S.Rational(1,4),S.Rational(1,4)]
equal('minor law total probability',sum(weights),1)
mean = sum((w*V for w,V in zip(weights,atoms)),S.zeros(2))
assert S.simplify(mean) == S.zeros(2)
checks.append('minor law mean exactly zero')
equal('minor law mean determinant exactly zero',sum(w*V.det() for w,V in zip(weights,atoms)),0)
M3 = h**3*x/(2*sig)-h**6/(2*sig**2*x)
M4 = h**3*x*x/(2*sig)-h**6/(2*sig**2)+h**9/(2*sig**3*x*x)
equal('minor law diagonal third moment',wp*x**3+wq*yy**3,M3)
equal('minor law diagonal fourth moment',wp*x**4+wq*yy**4,M4)
LH = al*(r+2)**4+(r+2)*(r+3)/6
equal('negative acoustic direction quartic',J(list(H)),LH)
Alaw = kap*h**4/2
Plaw = -kap*M3
Qlaw = LH*M4+(al*h**4*(1-h)**4+h**6+r*h**7+be*h**8)/2
equal('minor law acoustic formula',sum(w*((sig*V[0,0]+V[1,1])**2+kap*V[1,0]**2) for w,V in zip(weights,atoms)),Alaw)
equal('minor law cubic formula',sum(w*P.subs(dict(zip((a,b,c,d),list(V)))) for w,V in zip(weights,atoms)),Plaw)
equal('minor law quartic formula',sum(w*J(list(V)) for w,V in zip(weights,atoms)),Qlaw)
equal('minor law unbounded ratio asymptotic',S.limit(h*Plaw**2/(4*Alaw*Qlaw),h,0,dir='+'),kap/(4*sig*LH))
equal('minor law negative fixed-background leading coefficient',
      S.limit((Alaw+Plaw+Qlaw)/h**3,h,0,dir='+'),x*(LH*x-kap)/(2*sig))

sub = {r:1,x:S.Rational(1,32),h:S.Rational(1,256)}
Ar,Pr,Qr = [S.factor(v.subs(sub)) for v in (Alaw,Plaw,Qlaw)]
assert Ar>0 and Qr>0 and Pr*Pr>4*Ar*Qr and Ar+Pr+Qr<0
checks.append('rational law strictly violates moment discriminant')
full = sum(w*(J(list(S.eye(2)+V))-J(list(S.eye(2)))) for w,V in zip(weights,atoms))
equal('minor law direct full-energy check at s1',full,Alaw+Plaw+Qlaw)
equal('rational law exact negative energy',Ar+Pr+Qr,
      -S.Rational(93542709149,590295810358705651712))
equal('rational law exact ratio',Pr*Pr/(4*Ar*Qr),
      S.Rational(274861129984,112607332451))

# Exact angular-envelope obstruction at r=1.
v = S.symbols('v',real=True)
zz = 1+v/2
def angular_min(q):
    return 2*(zz**4+q**4-zz**2*q*q-zz*q*(zz*zz-q*q))
equal('angular envelope right rank-one derivative',S.diff(angular_min(v/2),v).subs(v,0),3)
equal('angular envelope left rank-one derivative',S.diff(angular_min(-v/2),v).subs(v,0),5)

report = {
    'status':'PASS',
    'verification_scope':'Exact polynomial and rational identities only; no unrestricted theorem or formal proof replay.',
    'checks':checks,
    'number_of_checks':len(checks),
    'compatible_example':{'r':'1','h':'2','A':str(aa),'P':str(pc),'Q':str(qq),'ratio':str(S.factor(pc*pc/(4*aa*qq)))},
    'noncompatible_minor_law':{'r':'1','x':'1/32','epsilon':'1/256','weights':[str(S.factor(w.subs(sub))) for w in weights],
                             'A':str(Ar),'P':str(Pr),'Q':str(Qr),'E_at_1':str(Ar+Pr+Qr),
                             'ratio':str(S.factor(Pr*Pr/(4*Ar*Qr))),
                             'is_compatible_gradient_witness':False},
    'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
    'sympy_version':S.__version__,
}
HERE.joinpath('CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'number_of_checks':len(checks),
                  'minor_law_ratio':report['noncompatible_minor_law']['ratio']},indent=2))
