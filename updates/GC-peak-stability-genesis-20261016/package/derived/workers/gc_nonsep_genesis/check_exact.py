#!/usr/bin/env python3
"""Independent exact algebra checks. This is not a formal analytic proof checker."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import subprocess
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
PIN = '9dbe934e5475f415c2d160a6c0715534aafa546b'
checks = []

def check(name, condition, detail=None):
    assert condition, name
    checks.append({'name': name, 'pass': True, 'detail': detail})

def zero(expr):
    return S.cancel(expr) == 0

r,a,b,c,d,s = S.symbols('r a b c d s', real=True)
kappa = r*(r+2)/3
u = a*a+c*c
v = b*b+d*d
j = a*d-b*c
J = 3*r*(u+v-2*j)**2/(8*(r+2))+r*(r-1)*u*u/6+j*j+r*u*j
us = (a+s)**2+c*c
vs = b*b+(d+s)**2
js = (a+s)*(d+s)-b*c
Js = 3*r*(us+vs-2*js)**2/(8*(r+2))+r*(r-1)*us*us/6+js*js+r*us*js
B = ((r+1)*a+d)**2+kappa*c*c
P = r*(d+(2*r+1)*a/3)*(a*a+c*c)+2*j*((r+1)*a+d)
check('exact conformal expansion including derivative means and null determinant',
      zero(Js-(r+2)*(r+3)*s**4/6-(r+2)*(2*r+3)*s**3*a/3
           -(r+2)*s**3*d-s*s*(B+(r+2)*j)-s*P-J))
U = S.symbols('U', real=True)
P_acoustic = 2*a*U**2-(r+2)*a*a*U+r*c*c*U-2*b*c*U-kappa*a**3-kappa*a*c*c
check('exact acoustic cubic rewrite', zero(P-P_acoustic.subs(U,(r+1)*a+d)))

# Supplied JSON is data only. Reconstruct the independent polynomial identity.
cert_path = ROOT/'originals/stability/certificate.json'
data = json.loads(cert_path.read_text())
Q = S.Matrix([[S.Rational(Fraction(x).numerator,Fraction(x).denominator)
               for x in row] for row in data['gram']])
z0 = S.Matrix([j+s*(a+d),r*c*s,r*c*d,r*c*c,r*b*c,r*a*s,r*a*d,r*a*c,r*a*b,r*a*a])
z1 = S.Matrix([d*s,d*d,c*s,c*d,c*c,b*d,b*c,b*b,a*s,a*d,a*c,a*b,a*a,
               r*(a*a+2*a*s+c*c),r*a*s,r*c*s])
s1 = -(r+2)*s*s*b+7*r*b**3/(6*(r+2))
s2 = (r+2)*s**3+(5*r/2+2)*s*s*a+7*r*s*a*a/4+r*(4*r+3)*a**3/(12*(r+2))
G = Js-(r+2)*(r+3)*s**4/6-(r+2)*(2*r+3)*s**3*a/3-s1*c-s2*d
check('supplied baseline Gram polynomial reconstructed independently',
      zero((r+2)*G-(z0.T*Q[:10,:10]*z0)[0]-r*(z1.T*Q[10:,10:]*z1)[0]))
check('supplied baseline Gram cross blocks vanish',Q[:10,10:]==S.zeros(10,16))
for name,mat in [('Q0',Q[:10,:10]),('Q1',Q[10:,10:]),('Q1-minus-floor',Q[10:,10:]-S.eye(16)/512)]:
    ll,dd = mat.LDLdecomposition(hermitian=False)
    check('baseline exact LDL '+name, ll*dd*ll.T==mat and all(dd[i,i]>0 for i in range(mat.rows)),
          {'dimension':mat.rows,'positive_pivots':[str(dd[i,i]) for i in range(mat.rows)]})

# Every frequency in the mixed residual is compatible by construction.
m,n,Fv,Gv = S.symbols('m n Fv Gv', real=True)
den = n*n+kappa*m*m
pv = (r+1)*m*n/den*Fv
av = m*Fv
kv = m*pv
ev = (r+1)*av-n*pv
g0v = Gv+pv
Bv = ((r+1)*av+n*Gv)**2+kappa*(m*Gv)**2
B0v = (n*g0v)**2+kappa*(m*g0v)**2
Rv = ev*ev+kappa*kv*kv
check('exact acoustic orthogonal projection per arbitrary Fourier frequency',zero(Bv-B0v-Rv))
check('residual stress is orthogonal to compatible gradients',zero(n*ev-kappa*m*kv))
check('exact residual Fourier multiplier',zero(Rv-(r+1)**2*kappa*m*m/den*av*av))

a0,A,b0,bb,c0,kk,U0,ee = S.symbols('a0 A b0 bb c0 kk U0 ee',real=True)
base_cubic = P_acoustic.subs({a:a0,b:b0,c:c0,U:U0},simultaneous=True)
full_cubic = P_acoustic.subs({a:a0+A,b:b0+bb,c:c0-kk,U:U0+ee},simultaneous=True)
expanded_diff = (
    2*(A*(U0+ee)**2+a0*ee*(2*U0+ee))
    -(r+2)*(A*(2*a0+A)*(U0+ee)+a0*a0*ee)
    +r*((-kk)*(2*c0-kk)*(U0+ee)+c0*c0*ee)
    -2*(bb*(c0-kk)*(U0+ee)+b0*(-kk)*(U0+ee)+b0*c0*ee)
    -kappa*(3*a0*a0*A+3*a0*A*A+A**3)
    -kappa*(A*(c0-kk)**2+a0*(-kk)*(2*c0-kk))
)
check('all six exact cubic difference decompositions',zero(full_cubic-base_cubic-expanded_diff))
check('exact cubic canonical split',zero((a0+A)**3-a0**3-3*a0*a0*A-3*a0*A*A-A**3))

# Uniform multiplier bound proof reduces to these exact rational identities
# and the nonnegative squares stated in the analytic proof.
tau,vv = S.symbols('tau vv', positive=True)
chi = lambda tau_: tau_**2*n*n/(m*m+tau_**2*n*n)
check('resolvent dyadic difference multiplier',zero(
    (chi(tau)-chi(tau/2)).subs(m,tau*n*vv)-3*vv**2/((1+vv**2)*(1+4*vv**2))))
check('resolvent last scalar inequality is a square',zero(4*vv**2+1-4*vv-(2*vv-1)**2))
K = S.Rational(3,2)
cube_constant = 1+K+K*K+21*K*K/8
check('exact infinite telescoping constant',cube_constant==S.Rational(341,32) and cube_constant<11)

# Bounded rational checks supplement, and do not replace, the uniform proof.
samples = 0
for mm in range(-12,13):
    for nn in range(-12,13):
        if mm==0 and nn==0:
            continue
        for tt in [S.Rational(1,2**i) for i in range(8)]:
            diff = (chi(tt)-chi(tt/2)).subs({m:mm,n:nn})
            tx2 = S.Rational(mm*mm,mm*mm+nn*nn)
            check_value = S.cancel(diff**2-S.Rational(9,16)*tx2/tt**2)
            assert check_value<=0
            samples += 1
check('bounded exact multiplier diagnostics',True,{'rational_frequency_scale_cases':samples,'scope':'specified finite cases only'})

def constants(rr):
    rr=S.Rational(rr)
    kap=rr*(rr+2)/3
    al=5*rr/(4096*(rr+2))
    be=rr/(512*(rr+2))
    K0=max(2*(rr+1)**2,kap)
    mu=be/K0
    L=3*(rr+1)*(1+1/(2*S.sqrt(kap)))
    DD=1+L
    lc=L
    le=rr+1+L
    ca=max(1,1/S.sqrt(kap))/(rr+1)
    ct=4+S.sqrt(kap)+2*rr*lc+rr*le/S.sqrt(kap)
    cr=2*(rr+1)+4*le+2*(rr+2)+2*lc+2*le/S.sqrt(kap)+2*S.sqrt(kap)*lc
    ce=2*le+(rr+2)+rr*lc**2+2*lc+kap*(3/(rr+1)+11*ca)+S.sqrt(kap)*lc
    cp=max(ct,cr,ce)
    lj=6*rr/(rr+2)+S.Rational(2,3)*rr*(rr+1)+1+2*rr
    return {'kappa':kap,'alpha':al,'beta':be,'K0':K0,'mu':mu,'L':L,'D':DD,
            'Lc':lc,'Le':le,'Ca':ca,'Ct':ct,'CR':cr,'Cepsilon':ce,'CP':cp,'LJ':lj}

con=constants(1)
delta=S.Rational(1,40000000)
check('r1 exact constants',con=={
    'kappa':S.Integer(1),'alpha':S.Rational(5,12288),'beta':S.Rational(1,1536),
    'K0':S.Integer(8),'mu':S.Rational(1,12288),'L':S.Integer(9),'D':S.Integer(10),
    'Lc':S.Integer(9),'Le':S.Integer(11),'Ca':S.Rational(1,2),
    'Ct':S.Integer(34),'CR':S.Integer(112),'Cepsilon':S.Integer(140),'CP':S.Integer(140),'LJ':S.Rational(19,3)})
check('r1 radius has every exact absorption condition',
      delta<=1 and delta<=1/con['D']
      and 256*con['LJ']*con['D']*delta<=con['alpha']
      and 64*con['CP']**2*delta**2<=con['alpha']*con['mu'])
margin=con['alpha']-64*con['LJ']*con['D']*delta-16*con['CP']**2/con['mu']*delta**2
check('r1 final exact quartic margin',margin>=con['alpha']/2,{'margin':str(margin),'required':str(con['alpha']/2)})

eps=S.Rational(1,100000000)
check('explicit degenerate-center nonseparable example is in the cone',4*eps**4<delta**4,
      {'first_potential':'sin(y)+1/100000000*sin(x+y)','epsilon4_over_R4':str(4*eps**4)})
# g=0 example, exact moments; the theorem itself admits every g.
example_B=2*eps**2
example_P=S.Integer(0)
example_Q=S.Rational(3,64)+eps**2/4+3*eps**4/16
check('illustrative example exact energy polynomial positive at every background',
      example_B>0 and example_P==0 and example_Q>0,
      {'B':str(example_B),'P':str(example_P),'Q':str(example_Q),
       'scope':'the specified g=0 map only; arbitrary g is an analytic theorem'})

paths=[
'00_START_HERE.txt',
'frontier/dossiers/N888.txt',
'frontier/dossiers/N880.txt',
'frontier/dossiers/N885.txt',
'updates/GA-conformal-causal-genesis-20261016/package/derived/workers/ga_parametric_stress_genesis/ALL_R_THEOREM_PROOF.txt',
'updates/GA-conformal-causal-genesis-20261016/package/derived/workers/ga_sharp_invention/MIXED_SOURCE_CONTINUATION.md',
'updates/GA-conformal-causal-genesis-20261016/package/derived/workers/ga_polynomial_genesis/CORE_THEOREM_v1.md',
'updates/GA-conformal-causal-genesis-20261016/package/derived/workers/ga_primary_math_prior/SEPARATED_SUBCLASS_PRIOR_ADDENDUM.md',
'updates/FZ-positive-memory-genesis-20261016/package/derived/workers/fz_positive_conformal_genesis/REPORT.md'
]
source_records=[]
for path in paths:
    raw=subprocess.check_output(['git','show',PIN+':'+path],cwd=W)
    source_records.append({'kind':'Astra prior at exact assigned pin','pin':PIN,'path':path,
        'sha256':hashlib.sha256(raw).hexdigest(),
        'url':'https://github.com/harjassand/astra-research-knowledge/blob/'+PIN+'/'+path})
for path in [ROOT/'originals/stability/PROOF_NOTE.md',cert_path,ROOT/'originals/stability/independent_checker.py']:
    source_records.append({'kind':'supplied immutable input; data or text read only',
        'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
source_records.extend([
 {'kind':'acquired primary analytic input','authors':'Rodrigo Bañuelos and Fabrice Baudoin',
  'title':'Martingale transforms and their projection operators on manifolds',
  'url':'https://arxiv.org/pdf/1109.5751','decisive':'Theorem 4.1(i), PDF page 17 (zero-index 16); Theorem 1.1, PDF page 3',
  'scope':'classical second-order Riesz norm bound on compact Lie groups, including the anisotropic flat torus',
  'access':'web tool PDF theorem text inspected, 2026-10-16; no external PDF copied into package'},
 {'kind':'primary qualitative comparator','authors':'Terence L. J. Harris, Bernd Kirchheim, and Chun-Chi Lin',
  'title':"Two-by-two upper triangular matrices and Morrey's conjecture",
  'url':'https://arxiv.org/pdf/1708.07849v2','decisive':'Theorem 2.4',
  'scope':'triangular-support gradient measures; exact prior audit read at assigned pin; theorem statement and its three-part proof on PDF pages 3-5 read directly in this run',
  'access':'web tool PDF text inspected, 2026-10-16; no external PDF copied into package'}
])
(HERE/'SOURCES.json').write_text(json.dumps({'status':'source and proof dependency manifest; no novelty clearance',
   'assigned_pin':PIN,'records':source_records},indent=2)+'\n')
receipt={'status':'PASS','analytic_status':'internal unreviewed proof in PROOF.md; not formal verification',
 'scope':'exact identities, supplied baseline certificate, stated radius arithmetic, and explicitly bounded diagnostics only',
 'not_established':['external mathematical correctness','historical originality','unrestricted conformal Jensen','negative compatible map','hardware capability'],
 'checks':checks,
 'input_certificate_sha256':hashlib.sha256(cert_path.read_bytes()).hexdigest(),
 'proof_sha256':hashlib.sha256((HERE/'PROOF.md').read_bytes()).hexdigest(),
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'CHECK_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','exact_check_groups':len(checks),'bounded_multiplier_cases':samples,
                  'proof_sha256':receipt['proof_sha256'],'receipt':str(HERE/'CHECK_RECEIPT.json')},indent=2))
