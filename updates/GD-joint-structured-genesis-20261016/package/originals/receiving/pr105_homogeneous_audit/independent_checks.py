"""Receiving audit: original algebra, rational data only; no producer code."""
from pathlib import Path
from fractions import Fraction
import json, hashlib
import sympy as S
BASE=Path(__file__).resolve().parent
CERT=BASE/'certificate.json'
r,a,b,c,d,s,U=S.symbols('r a b c d s U', real=True)
kap=r*(r+2)/3
j=a*d-b*c
u=a*a+c*c;v=b*b+d*d
J=3*r*(u+v-2*j)**2/(8*(r+2))+r*(r-1)*u*u/6+j*j+r*u*j
base=(r+2)*(r+3)*s**4/6
E=S.expand(J.subs({a:a+s,d:d+s}, simultaneous=True)-base)
P=r*(d+(2*r+1)*a/3)*(a*a+c*c)+2*j*((r+1)*a+d)
Ac=((r+1)*a+d)**2+kap*c*c
assert S.factor(E.coeff(s,1)-P)==0
quad_null=S.factor(E.coeff(s,2)-Ac)
assert S.factor(quad_null-(r+2)*j)==0
assert S.Poly(E.coeff(s,3),a,b,c,d).total_degree()==1
assert S.factor(E.coeff(s,4))==0
assert S.factor(E.coeff(s,0)-J)==0
Pnew=2*a*U*U-(r+2)*a*a*U+r*c*c*U-2*b*c*U-kap*a**3-kap*a*c*c
assert S.factor(P-Pnew.subs(U,(r+1)*a+d))==0
# Reconstruct the prior separated reserve independently, parsing only rational matrix data.
data=json.loads(CERT.read_text())
M=S.Matrix([[S.Rational(Fraction(x).numerator,Fraction(x).denominator) for x in row] for row in data['gram']])
assert M==M.T and M.shape==(26,26)
assert M[:10,10:]==S.zeros(10,16)
Q0=M[:10,:10]; Q1=M[10:,10:]
z0=S.Matrix([j+s*(a+d),c*r*s,c*d*r,c*c*r,b*c*r,a*r*s,a*d*r,a*c*r,a*b*r,a*a*r])
z1=S.Matrix([d*s,d*d,c*s,c*d,c*c,b*d,b*c,b*b,a*s,a*d,a*c,a*b,a*a,r*(a*a+2*a*s+c*c),a*r*s,c*r*s])
sig1=-(r+2)*s*s*b+7*r*b**3/(6*(r+2))
sig2=(r+2)*s**3+(5*r/2+2)*s*s*a+7*r*s*a*a/4+r*(4*r+3)*a**3/(12*(r+2))
G=J.subs({a:a+s,d:d+s}, simultaneous=True)-base-(r+2)*(2*r+3)*s**3*a/3-sig1*c-sig2*d
assert S.factor((r+2)*G-(z0.T*Q0*z0)[0]-r*(z1.T*Q1*z1)[0])==0
pivots={}
for name,mat in [('Q0',Q0),('Q1',Q1),('Q1_minus_I_512',Q1-S.eye(16)/512)]:
    LL,DD=mat.LDLdecomposition(hermitian=False)
    assert LL*DD*LL.T==mat
    vals=[DD[i,i] for i in range(mat.rows)]
    assert all(x>0 for x in vals)
    pivots[name]=[str(x) for x in vals]
# Quartic monomial norm is >= 5/8 Frobenius norm^4; exact SOS remainder.
xs=[a,b,c,d]
quartic_monomial_sum=sum(x**4 for x in xs)+sum(xs[i]**2*xs[jj]**2 for i in range(4) for jj in range(i+1,4))
sos=sum((xs[i]**2-xs[jj]**2)**2 for i in range(4) for jj in range(i+1,4))/8
assert S.expand(quartic_monomial_sum-S.Rational(5,8)*(a*a+b*b+c*c+d*d)**2-sos)==0
# Fourier projection identities: work with real derivative symbols, dropping the common i.
m,n,k=S.symbols('m n k',real=True,positive=True)
p=(r+1)*m*n/(n*n+k*m*m)
e=(r+1)*m-n*p;kk=m*p
assert S.factor(n*e-k*m*kk)==0
assert S.factor(e*e+k*kk*kk-(r+1)**2*k*m**4/(n*n+k*m*m))==0
# All table row sums.
R,t,ep,Le,Lc=S.symbols('R t ep Le Lc',real=True,positive=True)
Ca=S.symbols('Ca',positive=True)
rows=[
 [2*(r+1)+4*Le,2,2*Le],
 [2*(r+2),0,r+2],
 [0,2*r*Lc+r*Le/S.sqrt(k),r*Lc**2],
 [2*Lc+2*Le/S.sqrt(k),2,2*Lc],
 [0,0,k*(3/(r+1)+11*Ca)],
 [2*S.sqrt(k)*Lc,S.sqrt(k),S.sqrt(k)*Lc]
]
col_sums=[S.simplify(sum(row[i] for row in rows)) for i in range(3)]
assert S.expand(col_sums[0]-(2*(r+1)+4*Le+2*(r+2)+2*Lc+2*Le/S.sqrt(k)+2*S.sqrt(k)*Lc))==0
assert S.expand(col_sums[1]-(4+S.sqrt(k)+2*r*Lc+r*Le/S.sqrt(k)))==0
assert S.factor(col_sums[2]-(2*Le+(r+2)+r*Lc**2+2*Lc+k*(3/(r+1)+11*Ca)+S.sqrt(k)*Lc))==0
# Constant at r=1, entirely rational comparisons after squaring.
alpha=S.Rational(5,12288);mu=S.Rational(1,12288);D=10;LJ=S.Rational(19,3);CP=140;delta=S.Rational(1,40000000)
assert delta<=1 and delta*D<=1
quartic_loss=64*LJ*D*delta
cubic_loss=16*CP**2*delta**2/mu
assert quartic_loss<=alpha/4 and cubic_loss<=alpha/4
assert delta<=alpha/(256*LJ*D)
assert delta**2<=alpha*mu/(64*CP**2)
# Exact vertical kernel value and tiny mixed-mode illustration.
vertical=S.factor(E.subs({a:0,c:0,d:0}))
assert S.factor(vertical-3*r*b**4/(8*(r+2)))==0
assert 4*S.Rational(1,10**8)**4<delta**4
K=S.Rational(3,2)
telescope=1+K+K*K+S.Rational(21,8)*K*K
assert telescope==S.Rational(341,32) and telescope<11
# Independently establish the rank-one convexity premise for the prior-art comparison.
# Left SO(2) invariance reduces a rank-one direction to [[h1,h2],[0,0]].
h1,h2=S.symbols('h1 h2',real=True)
LH=S.expand(S.diff(J,a,2)*h1*h1+2*S.diff(J,a,b)*h1*h2+S.diff(J,b,2)*h2*h2)
LHmat=S.simplify(S.hessian(LH,(a,b,c,d))/2)
minors=[S.factor(LHmat[:i,:i].det()) for i in range(1,5)]
expected=[
 r*((2*r+1)**2*h1**2+3*h2**2)/(2*(r+2)),
 3*r**2*(((2*r+1)*h1**2-3*h2**2)**2+12*r*(r+2)*h1**2*h2**2)/(4*(r+2)**2),
 3*h2**2*r**2*(((r+1)*(2*r+1)*h1**2-3*h2**2)**2+3*r*(5*r+4)*h1**2*h2**2)/(2*(r+2)**2),
 9*h1**4*h2**4*r**4
]
assert all(S.factor(x-y)==0 for x,y in zip(minors,expected))
# For h1*h2 != 0 all four are positive; continuity covers the axes.
out={
 'status':'all independent exact checks passed',
 'proof_sha256':hashlib.sha256((BASE/'received_proof.md').read_bytes()).hexdigest(),
 'certificate_sha256':hashlib.sha256(CERT.read_bytes()).hexdigest(),
 'pointwise_quadratic_null_lagrangian':str(quad_null),
 'pointwise_cubic_background_linear_term':str(S.factor(E.coeff(s,3))),
 'gram_pivots':pivots,
 'r1':{'alpha':str(alpha),'mu':str(mu),'D':D,'LJ':str(LJ),'CP':CP,'delta':str(delta),'quartic_loss':str(quartic_loss),'cubic_loss':str(cubic_loss),'quartic_delta_limit':str(alpha/(256*LJ*D))},
 'dyadic_cubic_constant':str(telescope),
 'rank_one_convexity_leading_minors':[str(x) for x in expected],
 'vertical_acoustic_kernel_energy':str(vertical),
 'limits':'Rational certificate data only; no producer executable or audit receipt used. Analytic steps are justified separately in AUDIT.md.'
}
(BASE/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='gram_pivots'},indent=2))
