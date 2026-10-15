#!/usr/bin/env python3
"""Independent exact algebra for the pinned shear-elimination report.

This script deliberately does not read/import the source worker's verifier.
It checks finite identities only; no infinite-dimensional source inequality
or quasiconvexity conclusion is certified by this receipt.
"""
from pathlib import Path
import datetime
import hashlib
import json
import sympy as S

HERE = Path(__file__).resolve().parent
checks = []


def zero(name, expr):
    residual = S.expand(expr)
    assert residual == 0, (name, residual)
    checks.append(name)


def average(expr, *variables):
    result = S.expand(expr)
    for variable in variables:
        result = S.Add(*[
            term for term in S.Add.make_args(result)
            if term.as_powers_dict().get(variable, 0) == 0
        ])
    return S.expand(result)


a, b, c, d, h, s = S.symbols('a b c d h s', real=True)
j = a*d-b*c
J = ((a-d)**2+(b+c)**2)**2/S.Integer(8)+j**2+(a*a+c*c)*j
C = S.diff(J, a)+S.diff(J, d)
CD = S.diff(J, a)-S.diff(J, d)
e = 2*a+d
f = a-2*d
p = 3*(b+c)**2/S.Integer(2)+(a-d)**2/S.Integer(2)+2*c*c
pd = (a+d)**2/S.Integer(2)+3*(c-b)**2/S.Integer(2)+2*b*b

# Group 1: exact polynomial expansions, both determinant signs, and SOS.
zero('coercivity invariant polynomial', J-((a*a+c*c+b*b+d*d)**2/8
    +3*j*j/2+(a*a+c*c-b*b-d*d)*j/2))
zero('I conformal expansion', J.subs({a:a+s,d:d+s}, simultaneous=True)
    -2*s**4-J-s*C-s*s*(e*e+c*c+3*j)-s**3*(5*a+3*d))
zero('D conformal expansion', J.subs({a:a+s,d:d-s}, simultaneous=True)
    -2*s**4-J-s*CD-s*s*(f*f+b*b-3*j)-s**3*(3*a-5*d))
zero('I acoustic quartic expansion', J.subs(b,b+h)-J-S.diff(J,b)*h
    -p*h*h/2-(b+c)*h**3/2-h**4/8)
zero('D acoustic quartic expansion', J.subs(c,c+h)-J-S.diff(J,c)*h
    -pd*h*h/2-(c-b)*h**3/2-h**4/8)
zero('I cubic source shear increment', C.subs(b,b+h)-C+2*h*c*e)
zero('D cubic source shear increment', CD.subs(c,c+h)-CD-2*h*b*f)
zero('I positive joint quadratic identity', s*s*(e*e+c*c)-2*s*h*c*e
    +h*h*p/2-((s*e-h*c)**2+s*s*c*c
    +3*h*h*(b+c)**2/4+h*h*(a-d)**2/4))
zero('D positive joint quadratic identity', s*s*(f*f+b*b)+2*s*h*b*f
    +h*h*pd/2-((s*f+h*b)**2+s*s*b*b
    +3*h*h*(c-b)**2/4+h*h*(a+d)**2/4))
zero('separable class pointwise SOS',
    8*(J.subs(d,-2*a)-S.Rational(9,4)*a*a*b*b)
    -(97*(a*a+S.Rational(30,97)*b*c)**2+2*a*a*c*c
      +(b*b+2*b*c-c*c)**2+S.Rational(264,97)*b*b*c*c))

# Group 2: rank-one Hessian and Schur complement, independently derived.
tau,z,P,Q,X,Y = S.symbols('tau z P Q X Y', real=True)
chart = {a:(P+X)/2,b:(Y-Q)/2,c:(Y+Q)/2,d:(P-X)/2}
second = S.diff(J.subs({a:a+tau,b:b+z*tau}, simultaneous=True),tau,2)
second = second.subs(tau,0).subs(chart, simultaneous=True)
G = S.Matrix([[2,-z,-S.Rational(1,2),-z],
    [-z,(z*z+1)/2,0,z*z/2],
    [-S.Rational(1,2),0,(z*z+1)/2,z],
    [-z,z*z/2,z,2*z*z]])
v = S.Matrix([P,Q,X,Y])
zero('rank-one Hessian chart', second-(v.T*G*v)[0])
zero('leading Schur block determinant', G[:2,:2].det()-1)
schur = S.simplify(G[2:,2:]-G[2:,:2]*G[:2,:2].inv()*G[:2,2:])
target = S.Matrix([[3*(z*z+1)/8,3*z/4],[3*z/4,3*z*z/2]])
for row in range(2):
    for col in range(2):
        zero(f'Schur entry {row},{col}', schur[row,col]-target[row,col])
zero('Schur determinant', schur.det()-9*z**4/16)

# Group 3: conjugate and affine elimination signs.
pp,zz,aa,cc,qq,mm,nn,gg = S.symbols('pp zz aa cc qq mm nn gg', real=True)
root_source = h**3/2+pp*h
zero('conjugate value at its root', root_source*h-(h**4/8+pp*h*h/2)
    -(3*h**4/8+pp*h*h/2))
energy = aa+gg+nn+s*(cc-2*mm)+qq*s*s
sopt = (2*mm-cc)/(2*qq)
zero('affine scalar elimination sign', energy.subs(s,sopt)
    -(aa-cc*cc/(4*qq)+gg-mm*mm/qq+nn+cc*mm/qq))
t = S.symbols('t', real=True)
zero('fourth-degree affine homogeneity',
    J.subs({a:t*a,b:t*b,c:t*c,d:t*d}, simultaneous=True)-t**4*J)
zero('root scaling identity', (t*h)**3/2+(t*t*pp)*(t*h)-t**3*root_source)

# Group 4: exact compatible three-wave fixture and its positive bound.
LX,LY = S.symbols('LX LY', nonzero=True)
U,V,T = S.symbols('U V T', real=True)


def cosine(k,l):
    return (LX**k*LY**l+LX**(-k)*LY**(-l))/2


theta = U*cosine(1,0)+V*cosine(1,1)+T*cosine(2,1)


def dx(expr):
    return S.I*LX*S.diff(expr,LX)


def dy(expr):
    return S.I*LY*S.diff(expr,LY)


av = -dx(dy(theta))/2
bv = -dy(dy(theta))/2
cv = dx(dx(theta))
dv = dx(dy(theta))
sub = {a:av,b:bv,c:cv,d:dv}
AF = average(J.subs(sub,simultaneous=True),LX,LY)
CF = average(C.subs(sub,simultaneous=True),LX,LY)
QF = average(cv*cv,LX,LY)
PF = average(p.subs(sub,simultaneous=True),LX)
NF = average(S.diff(J,b).subs(sub,simultaneous=True),LX)
zero('fixture conformal cubic', CF+3*T*U*V/2)
zero('fixture failed separable cancellation',
    2*average(av*bv*cv,LX,LY)+3*T*U*V/8)
zero('fixture Q', QF-(16*T*T+U*U+V*V)/2)
zero('fixture P', PF-((439*T*T+28*(U*U+V*V))/16
    +11*U*V*cosine(0,1)/4))
zero('fixture N', NF-(85*T*U*V/16
    +T*(31*U*U+30*V*V)*cosine(0,1)/16))
zero('fixture quartic energy', 1024*AF-(21675*T**4+4016*T*T*U*U
    +9616*T*T*V*V+48*U**4+512*U*U*V*V+300*V**4))
BF = U*U/2+9*V*V/8+21*T*T/2
zero('fixture shear independent B', average(av*av+cv*cv+dv*dv,LX,LY)-BF)
xx,yy,zz = S.symbols('xx yy zz', nonnegative=True)
boundpoly = S.Poly(S.expand((16*zz+xx+yy)*(xx/2+9*yy/8+21*zz/2)**2),xx,yy,zz)
assert all(coefficient >= 0 for coefficient in boundpoly.coeffs())
assert boundpoly.coeff_monomial(xx*yy*zz) == S.Rational(417,8)
checks.append('fixture rational bound has nonnegative coefficients and xyz=417/8')
HH,KK = S.symbols('HH KK', real=True)
two = 3*(HH**4+KK**4)/64+7*HH*HH*KK*KK/16
Hessian = S.hessian(two,(HH,KK)).subs({HH:1,KK:1})
assert Hessian == S.Matrix([[S.Rational(23,16),S.Rational(7,4)],
    [S.Rational(7,4),S.Rational(23,16)]])
assert (Hessian*S.Matrix([1,-1])) == -S.Rational(5,16)*S.Matrix([1,-1])
checks.append('two-shear Hessian has negative eigenvalue -5/16')

snapshot = HERE/'SOURCE_REPORT_PINNED.md'
receipt = {
    'status':'PASS',
    'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'sympy_version':S.__version__,
    'source_snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
    'source_addendum_sha256':hashlib.sha256((HERE/'SOURCE_ADDENDUM_PINNED.md').read_bytes()).hexdigest(),
    'independent_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'identity_group_count':4,
    'exact_check_count':len(checks),
    'checks':checks,
    'scope':'Finite polynomial and moment identities only. Analytic assertions are proved in REPORT.md. The universal source inequality remains unproved.',
    'source_verifier_read_or_imported':False,
}
(HERE/'EXACT_CHECKS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'identity_groups':4,'checks':len(checks),
    'source_snapshot_sha256':receipt['source_snapshot_sha256']},indent=2))
