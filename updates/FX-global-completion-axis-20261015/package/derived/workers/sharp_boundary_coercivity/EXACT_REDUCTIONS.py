"""Exact algebra supporting the new analytic reductions, not formal proof.

The source JSON is read only. All writes are local to this worker directory.
"""
import hashlib,json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).parent
SOURCE=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-global-completion-axis-20261015/updates/FW-moving-heat-observable-20261015/package/derived/workers/sharp_boundary_qc/UNIVERSAL_SHARP_NEGATIVE_CERTIFICATE.json')
data=json.loads(SOURCE.read_text())
r,t=s.symbols('r t',real=True)
def rat(item):
    def pol(co):return sum((s.Rational(v)*r**i for i,v in enumerate(co)),s.S.Zero)
    return s.cancel(pol(item['numerator'])/pol(item['denominator']))
C=s.Matrix([[rat(item) for item in row] for row in data['C']])
a,b,c,d=s.symbols('a b c d',real=True)
A=s.Matrix([a,b,c,d]);zz=s.Matrix(s.symbols('z0:6'))
ell=C.T*s.kronecker_product(A,zz)
X=(a-d,b+c)
Y=(-3*b+(2*r+1)*c,(2*r+1)*a+3*d)
expected={0:Y[0]*zz[0]/(2*r+1),3:Y[0]*zz[3]/(2*r+1),
          6:Y[1]*zz[0]/3,9:Y[1]*zz[3]/3,
          2:X[1]*zz[2],5:X[1]*zz[5],
          8:-X[0]*zz[2],11:-X[0]*zz[5]}
assert all(s.cancel(ell[i]-v)==0 for i,v in expected.items())
alpha=3*r/(8*(r+2));beta=r*(r-1)/6
F=alpha*((a-d)**2+(b+c)**2)**2+beta*(a*a+c*c)**2+(a*d-b*c)**2+r*(a*a+c*c)*(a*d-b*c)
x,y,n,m=s.symbols('x y n m',real=True)
rankone=s.factor(F.subs({a:x*n,b:x*m,c:y*n,d:y*m}))
rankone_expected=(x*x+y*y)**2*(alpha*(n*n+m*m)**2+beta*n**4)
assert s.cancel(rankone-rankone_expected)==0
assert s.cancel(alpha/s.Integer(3)-s.Rational(1,8)+s.Rational(1,4)/(r+2))==0

p,q,w,z=s.symbols('p q w z',real=True)
shift=s.Poly(s.expand(F.subs({a:1+t*p,b:t*q,c:t*w,d:1+t*z})),t)
Q=shift.coeff_monomial(t*t)
Q_expected=((r+1)*p+z)**2+r*(r+2)*w*w/3
# Only det(Dphi)=p*z-q*w is discarded after integration.
det_multiple=s.factor((Q-Q_expected)/(p*z-q*w))
assert s.cancel(Q-Q_expected-det_multiple*(p*z-q*w))==0
assert det_multiple==r+2
assert shift.coeff_monomial(t**3).subs({p:0,w:0,z:0})==0

scalar_a,scalar_b,scalar_c=s.symbols('scalar_a scalar_b scalar_c',real=True)
assert s.expand(scalar_a+scalar_b+3*scalar_b**2/(8*scalar_a)
                -scalar_a/3-3*(scalar_b+4*scalar_a/3)**2/(8*scalar_a))==0

radial=(alpha*(s.Rational(1,2)-1)**4
        +beta*(3*s.Rational(1,2)**4+2*s.Rational(1,2)**2+3)/8
        +s.Rational(1,4)+r*s.Rational(1,2)*(s.Rational(1,4)+1)/2)
radial_ratio=s.factor(radial/(s.Rational(5,4)**2))
assert s.cancel(radial_ratio-(59*r**3+299*r**2+572*r+384)/(1200*(r+2)))==0

record={'status':'PASS','source_certificate_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'exact_kernel_rows':{str(i):str(s.factor(v)) for i,v in expected.items()},
        'X':[str(v) for v in X],'Y':[str(v) for v in Y],
        'second_elliptic_equation':'k^2 phi_xx+phi_yy=0, k=-(2r+1)/3>1',
        'rank_one_quartic':str(rankone_expected),
        'rank_one_bregman_lower_constant':'alpha/3 > 1/8 for each r < -2',
        'I_background_quadratic':str(Q_expected),
        'discarded_quadratic_null_lagrangian_multiplier':str(det_multiple),
        'pure_shear_cubic_zero':True,
        'radial_degree_half_upper_ratio':str(radial_ratio),
        'analytic_theorem_status':'See PROOFS.md; algebra replay is not formal proof or external review',
        'all_affine_uniform_fourth_order_margin':'UNRESOLVED'}
(ROOT/'EXACT_REDUCTIONS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
