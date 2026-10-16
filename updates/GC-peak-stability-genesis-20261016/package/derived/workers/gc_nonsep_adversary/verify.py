"""Independent exact checks and finite adversarial diagnostics.

The analytic arguments are in PROOFS.md and A0_RECEIVING_AUDIT.md.
No producer verifier is imported or executed. Matrix input is data only.
"""

from pathlib import Path
from fractions import Fraction
import hashlib
import json
import math
import numpy as np
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / 'originals' / 'stability'
CANDIDATE = HERE.parent / 'gc_nonsep_genesis' / 'PROOF.md'
checks = {}

def check(name, result):
    result = bool(result)
    checks[name] = result
    assert result, name

r, a, b, c, d, s = S.symbols('r a b c d s')
sigma = r + 1
kappa = r * (r + 2) / 3
alpha = 5 * r / (4096 * (r + 2))
beta = r / (512 * (r + 2))

def J(A, B, C, D):
    u, v, j = A*A+C*C, B*B+D*D, A*D-B*C
    return 3*r*(u+v-2*j)**2/(8*(r+2))+r*(r-1)*u*u/6+j*j+r*u*j

Q = J(a, b, c, d)
B = (sigma*a+d)**2+kappa*c*c
P = r*(d+(2*r+1)*a/3)*(a*a+c*c)+2*(a*d-b*c)*(sigma*a+d)
check('exact acoustic expansion with all null terms', S.cancel(
    J(a+s,b,c,d+s)-(r+2)*(r+3)*s**4/6
    -(r+2)*(2*r+3)*s**3*a/3-(r+2)*s**3*d
    -s*s*(B+(r+2)*(a*d-b*c))-s*P-Q
) == 0)
q = S.symbols('q')
check('acoustic-factor cubic identity', S.cancel(
    P.subs(d,q-sigma*a)
    -(2*a*q*q-(r+2)*a*a*q+r*c*c*q-2*b*c*q-kappa*a**3-kappa*a*c*c)
) == 0)

expected = [2*(r+1)*(r+2), 2*(r+2)*(4*r+9)/3,
            4*(r**3+7*r*r+34*r+12)/(3*(r+2))]
for name, polynomial, target in zip(['LB','LP','LQ'], [B,P,Q], expected):
    terms = []
    for variable in [a,b]:
        for _, coefficient in S.Poly(S.diff(polynomial,variable),a,b,c,d).terms():
            coefficient = S.factor(coefficient)
            signed = coefficient if coefficient.subs(r,1)>0 else -coefficient
            numerator, denominator = S.fraction(signed)
            check(name+' fixed coefficient sign '+str(len(terms)),
                  all(x>=0 for x in S.Poly(numerator,r).all_coeffs())
                  and all(x>=0 for x in S.Poly(denominator,r).all_coeffs()))
            terms.append(signed)
    check(name+' exact coefficient sum', S.cancel(sum(terms)-target)==0)

data = json.loads((SOURCE/'certificate.json').read_text())
Gmat = S.Matrix([[S.Rational(Fraction(entry).numerator,
                              Fraction(entry).denominator)
                 for entry in row] for row in data['gram']])
z0 = S.Matrix([a*d-b*c+s*(a+d),r*c*s,r*c*d,r*c*c,r*b*c,
               r*a*s,r*a*d,r*a*c,r*a*b,r*a*a])
z1 = S.Matrix([d*s,d*d,c*s,c*d,c*c,b*d,b*c,b*b,a*s,a*d,a*c,
               a*b,a*a,r*(a*a+2*a*s+c*c),r*a*s,r*c*s])
stress1 = -(r+2)*s*s*b+7*r*b**3/(6*(r+2))
stress2 = (r+2)*s**3+(5*r/2+2)*s*s*a+7*r*s*a*a/4+r*(4*r+3)*a**3/(12*(r+2))
residual = J(a+s,b,c,d+s)-(r+2)*(r+3)*s**4/6-(r+2)*(2*r+3)*s**3*a/3-stress1*c-stress2*d
check('independent exact Gram identity', S.cancel((r+2)*residual
      -(z0.T*Gmat[:10,:10]*z0)[0]-r*(z1.T*Gmat[10:,10:]*z1)[0])==0)
check('zero cross block', Gmat[:10,10:]==S.zeros(10,16))
for name, matrix in [('Q0',Gmat[:10,:10]),('Q1',Gmat[10:,10:]),
                     ('Q1 minus floor',Gmat[10:,10:]-S.eye(16)/512)]:
    lower, diag = matrix.LDLdecomposition(hermitian=False)
    check(name+' exact reconstruction', lower*diag*lower.T==matrix)
    check(name+' exact positive pivots', all(diag[i,i]>0 for i in range(matrix.rows)))

# Independent rank-one-convexity reconstruction, with coefficient 1/2 J''.
z, tau, cp, cq, cx, cy = S.symbols('z tau cp cq cx cy')
LH = S.diff(J(a+tau,b+z*tau,c,d),tau,2).subs(tau,0)/2
LH = S.expand(LH.subs({a:(cp+cx)/2,b:(cy-cq)/2,
                      c:(cy+cq)/2,d:(cp-cx)/2}))
H = S.hessian(LH,[cp,cq,cx,cy])/2
Ac, cross, tail = H[:2,:2], H[:2,2:], H[2:,2:]
schur = S.simplify(tail-cross.T*Ac.inv()*cross)
check('rank-one acoustic determinant', S.factor(Ac.det())==r*(r+1)**2*(r+2)/48)
check('rank-one Schur determinant', S.factor(schur.det())==27*r**3*z**4/(16*(r+1)**2*(r+2)))
check('rank-one Schur first entry', S.cancel(schur[0,0]
      -r*(3*r*(r+2)*z*z+(2*r+1)**2)/(4*(r+1)**2*(r+2)))==0)

# Exact A=0 domination counterfamily, with independent phase moments.
N, delta, T, W = S.symbols('N delta T W',positive=True)
row = {a:delta*T/N,b:W+delta*T,c:-sigma*delta*T/N**2,d:-sigma*delta*T/N}
moments = {0:S.Integer(1),2:S.Rational(1,2),4:S.Rational(3,8)}
def avg_phase(expr):
    return S.factor(sum(co* moments.get(exp[0],0)*moments.get(exp[1],0)
                        for exp,co in S.Poly(S.expand(expr),T,W).terms()))
actualB, actualP, actualQ = [avg_phase(pol.subs(row)) for pol in [B,P,Q]]
base_row = dict(row)
base_row[a] = S.Integer(0)
base_row[b] = W
baseB, baseP, baseQ = [avg_phase(pol.subs(base_row)) for pol in [B,P,Q]]
check('counterfamily acoustic ratio', S.cancel(actualB/baseB-kappa/(N*N+kappa))==0)
check('counterfamily actual cubic zero', actualP==0)
check('counterfamily baseline cubic zero', baseP==0)
coeff2 = S.factor(S.Poly(actualQ,delta).coeff_monomial(delta**2))
m = S.symbols('m',positive=True)
positive_numerator = 9*r*(m-1)**2+3*r*((r-1)**2+3)*(m-1)+16*r**3+28*r*r+32*r+8
check('counterfamily exact positive quadratic coefficient',
      S.cancel(coeff2-positive_numerator.subs(m,N*N)/(16*N**4*(r+2)))==0)
example_values = {r:S.Integer(1),N:S.Integer(2),delta:S.Rational(1,10**8),s:S.Integer(10**16)}
Eact = S.factor((actualB*s*s+actualQ).subs(example_values))
Ebase = S.factor((baseB*s*s+baseQ).subs(example_values))
check('counterfamily exact positive actual energy', Eact>0)
check('counterfamily exact half domination failure', 2*Eact<Ebase)

# Independent Fourier proof identities for the receiving candidate.
m,n = S.symbols('m n',real=True)
den = n*n+kappa*m*m
pmult = sigma*m*n/den
emult = S.factor(sigma*m-n*pmult)
kmult = S.factor(m*pmult)
check('projection differential orthogonality', S.cancel(n*emult-kappa*m*kmult)==0)
check('projection exact residual symbol', S.cancel(emult**2+kappa*kmult**2
      -sigma**2*kappa*m**4/den)==0)
K = S.Rational(3,2)
check('cubic telescoping constant', 1+K+K*K+21*K*K/8==S.Rational(341,32))
check('cubic constant is less than eleven', S.Rational(341,32)<11)

# Exact constants at r=1, independently entered from the candidate formulas.
rr = S.Integer(1)
kk = rr*(rr+2)/3
ss = rr+1
al = 5*rr/(4096*(rr+2))
be = rr/(512*(rr+2))
K0 = max(2*ss*ss,kk)
mu = be/K0
L = 3*ss*(1+1/(2*S.sqrt(kk)))
D = 1+L
Lc, Le = L, ss+L
Ca = max(S.Integer(1),1/S.sqrt(kk))/ss
Ct = 4+S.sqrt(kk)+2*rr*Lc+rr*Le/S.sqrt(kk)
CR = 2*ss+4*Le+2*(rr+2)+2*Lc+2*Le/S.sqrt(kk)+2*S.sqrt(kk)*Lc
Ce = 2*Le+(rr+2)+rr*Lc**2+2*Lc+kk*(3/ss+11*Ca)+S.sqrt(kk)*Lc
CP = max(Ct,CR,Ce)
LJ = 6*rr/(rr+2)+S.Rational(2,3)*rr*(rr+1)+1+2*rr
rad = S.Rational(1,40_000_000)
check('candidate r1 radius below one',rad<=1)
check('candidate r1 radius below inverse D',rad*D<=1)
check('candidate r1 quartic loss at most alpha/4',64*LJ*D*rad<=al/4)
check('candidate r1 cubic loss at most alpha/4',16*CP**2*rad**2/mu<=al/4)

# Diagnostics only: these grid checks do not prove a continuum theorem.
rng = np.random.default_rng(382919)
ngrid = 256
xx = 2*np.pi*np.arange(ngrid)[:,None]/ngrid
yy = 2*np.pi*np.arange(ngrid)[None,:]/ngrid
max_ratio = 0.
max_projection_error = 0.
for trial in range(48):
    aa = np.zeros((ngrid,ngrid))
    bb = np.zeros_like(aa)
    rrxa = np.zeros_like(aa)
    pp_x = np.zeros_like(aa)
    pp_y = np.zeros_like(aa)
    cc0 = np.zeros_like(aa)
    dd0 = np.zeros_like(aa)
    scale_y = [1,2,4,8][trial%4]
    for mode in range(6):
        mm = int(rng.integers(1,5))
        nn = int(rng.integers(1,5))*scale_y
        amp = float(rng.normal())/(mm*mm+nn*nn)
        phase = float(rng.uniform(0,2*np.pi))
        cos = np.cos(mm*xx+nn*yy+phase)
        sin = np.sin(mm*xx+nn*yy+phase)
        aa += amp*mm*cos
        bb += amp*nn*cos
        rrxa += -amp*mm*mm/math.sqrt(mm*mm+nn*nn)*sin
        mult = 2*mm*nn/(nn*nn+mm*mm)
        pp_x += mult*amp*mm*cos
        pp_y += mult*amp*nn*cos
        ga = float(rng.normal())/(mm*mm+nn*nn)
        cc0 += ga*mm*cos
        dd0 += ga*nn*cos
    epsilon = float(np.mean((aa*aa+bb*bb)**2)**.25)
    qstar = float(np.mean(rrxa*rrxa)**.5)
    ratio = float(np.mean(np.abs(aa)**3)/(qstar*epsilon**2))
    max_ratio = max(max_ratio,ratio)
    U = dd0+2*aa-pp_y
    cc = cc0-pp_x
    lhs = float(np.mean(U*U+cc*cc))
    rhs = float(np.mean(dd0*dd0+cc0*cc0+(2*aa-pp_y)**2+pp_x*pp_x))
    max_projection_error=max(max_projection_error,abs(lhs-rhs)/(1+abs(rhs)))
check('finite stress diagnostic cubic bound',max_ratio<11)
check('finite stress diagnostic projection',max_projection_error<1e-12)

receipt = {
    'scope':'Exact polynomial/rational checks plus finite diagnostics; analytic proof is separately reconstructed in saved reports. No external certification.',
    'checks_passed':sum(checks.values()),
    'checks':checks,
    'sha256':{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
              for path in [SOURCE/'PROOF_NOTE.md',SOURCE/'certificate.json',CANDIDATE]},
    'A0_counterexample':{'r':1,'N':2,'delta':'1/100000000','s':'10000000000000000',
                         'actual_energy':str(Eact),'baseline_energy':str(Ebase),
                         'ratio_float':float(Eact/Ebase)},
    'candidate_r1_constants':{name:str(val) for name,val in
        [('mu',mu),('L',L),('D',D),('CP',CP),('LJ',LJ),('delta',rad)]},
    'finite_diagnostics':{'cases':48,'grid':ngrid,'max_cubic_ratio':max_ratio,
                           'max_relative_projection_error':max_projection_error},
}
(HERE/'VERIFICATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({key:receipt[key] for key in
                 ['scope','checks_passed','sha256','A0_counterexample',
                  'candidate_r1_constants','finite_diagnostics']},indent=2))
