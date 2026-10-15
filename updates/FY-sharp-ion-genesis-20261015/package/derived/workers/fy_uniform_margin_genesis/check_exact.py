"""Exact algebra for one independent partial uniform-margin investigation.

Reads the pinned certificate; writes only beside this file. Does not verify
analytic inequalities, external correctness, priority, or the full margin.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sympy as s

ROOT = Path(__file__).resolve().parent
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-sharp-ion-20261015')
PIN = 'b32943eeb62d0d79929a9e572a344219a785ebf9'
CERT = W / 'updates/FW-moving-heat-observable-20261015/package/derived/workers/sharp_boundary_qc/UNIVERSAL_SHARP_NEGATIVE_CERTIFICATE.json'
CERT_SHA = 'f45149312e694f6080a179b77d322aceabf0d7c2a55ed60c5e102037e55f6ee7'

assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=W, text=True).strip() == PIN
assert hashlib.sha256(CERT.read_bytes()).hexdigest() == CERT_SHA
data = json.loads(CERT.read_text())
r = s.symbols('r', real=True)

def rat(item):
    def pol(cs):
        return sum((s.Rational(v)*r**i for i,v in enumerate(cs)), s.S.Zero)
    return s.cancel(pol(item['numerator'])/pol(item['denominator']))

C = s.Matrix([[rat(v) for v in row] for row in data['C']])
assert C[12:24, :] == s.eye(12)
A = s.Matrix(s.symbols('a b c d', real=True))
a,b,c,d = A
zz = s.Matrix(s.symbols('z0:6', real=True))
Z = s.kronecker_product(A,zz)
ell = C.T*Z
jets = [s.Matrix([zz[0],zz[1],zz[3],zz[4]]),
        s.Matrix([zz[1],zz[2],zz[4],zz[5]])]

def coefficients(expr):
    pol = s.Poly(s.expand(expr),*list(A),*list(zz))
    return s.Matrix([pol.coeff_monomial(m) for m in Z])

def derivative_vector(P,direction):
    return coefficients(sum(s.diff(P,x)*v for x,v in zip(A,jets[direction])))

def restriction(v):
    return (C*v[12:24,0]-v).applyfunc(s.cancel)

def support(P,direction):
    v = derivative_vector(P,direction)
    assert restriction(v) == s.zeros(24,1)
    w = v[12:24,0]
    assert s.cancel(sum(w[i]*ell[i] for i in range(12))
                    -sum(s.diff(P,x)*v0 for x,v0 in zip(A,jets[direction]))) == 0
    return {str(i):str(s.factor(v0)) for i,v0 in enumerate(w) if v0 != 0}

u=a*a+c*c
v=b*b+d*d
j=a*d-b*c
cross=a*b+c*d
k=-(2*r+1)/3
kappa=(10*r+8)/(3*r)
Q=v+k*u-kappa*j
entropy_weights = {'x':support(Q,0),'y':support(Q,1)}
positive_gap=s.factor(4*k-kappa*kappa)
assert positive_gap == -8*(r+2)**2*(3*r+2)/(9*r*r)

quadratics=[x*y for i,x in enumerate(A) for y in A[i:]]
cols=[]
for P in quadratics:
    cols.append(s.Matrix.vstack(restriction(derivative_vector(P,0)),
                               restriction(derivative_vector(P,1))))
M=s.Matrix.hstack(*cols)
minor_rows=(0,1,3,4,5,6,7,9,29)
minor_cols=(0,1,2,3,4,5,6,7,8)
minor=s.factor(M.extract(minor_rows,minor_cols).det())
assert minor == -16*r*(r+2)/((r+1)**3*(2*r+1))
qcoeff=s.Matrix([s.Poly(Q,*list(A)).coeff_monomial(x) for x in quadratics])
assert (M*qcoeff).applyfunc(s.cancel) == s.zeros(48,1)
assert M.rank() == 9

fluxes = {
    'Ux':(v+(2*r+1)**2*u/(9*(r+1)),0),
    'Vx':(j+r*(2*r+1)*u/(6*(r+1)),0),
    'Uy':(v+(r+1)*u,1),
    'Vy':(j+r*u/2,1),
}
flux_weights = {name:support(P,direction) for name,(P,direction) in fluxes.items()}
metric_columns=[restriction(derivative_vector(P,di))
                for P in [u,v,cross,j] for di in [0,1]]
metric_M=s.Matrix.hstack(*metric_columns)
assert metric_M.rank() == 4
mx_rows=metric_M.T.rref()[1]
mx_cols=metric_M.rref()[1]
metric_minor=s.factor(metric_M.extract(mx_rows,mx_cols).det())

ex=s.Matrix([1,-(2*r+1)**2/(9*(r+1)),-r*(2*r+1)/(6*(r+1))])
ey=s.Matrix([1,-r-1,-r/2])
cone_x=s.factor(ex[0]*ex[1]-ex[2]**2)
cone_y=s.factor(ey[0]*ey[1]-ey[2]**2)
assert cone_x == -(2*r+1)**2*(r+2)**2/(36*(r+1)**2)
assert cone_y == -(r+2)**2/4

alpha=3*r/(8*(r+2))
beta=r*(r-1)/6
F=alpha*((a-d)**2+(b+c)**2)**2+beta*u*u+j*j+r*u*j
t,p,q,cc,z,SS=s.symbols('t p q cc z SS',real=True)
shift=s.Poly(s.expand(F.subs({a:1+t*p,b:t*q,c:t*cc,d:1+t*z})),t)
quadratic=shift.coeff_monomial(t*t)
m_expected=((r+1)*p+z)**2+r*(r+2)*cc*cc/3
assert s.cancel(quadratic-m_expected-(r+2)*(p*z-q*cc)) == 0
cubic=shift.coeff_monomial(t**3)
cubic_S=s.expand(cubic.subs(z,SS-(r+1)*p))
cubic_expected=2*p*SS**2+(-2*q*cc+r*cc**2-(r+2)*p**2)*SS-r*(r+2)*p*(p*p+cc*cc)/3
assert s.cancel(cubic_S-cubic_expected) == 0

T=s.symbols('T',positive=True)
B=s.Matrix([T,0,0,T])
qsoft=s.Matrix([p/T,q,cc/T**2,z/T])
linear=sum(s.diff(F,x).subs(dict(zip(A,B)))*qx for x,qx in zip(A,qsoft))
soft=s.expand(F.subs(dict(zip(A,B+qsoft)))-F.subs(dict(zip(A,B)))-linear)
soft_lead=s.factor(s.limit(soft,T,s.oo))
soft_expected=alpha*q**4+((r+1)*p+z)**2+(r+2)*(p*z-q*cc)
assert s.cancel(soft_lead-soft_expected) == 0

x,y=s.symbols('x y',real=True)
rankone={a:0,b:x,c:0,d:y}
assert s.expand(Q.subs(rankone)-(x*x+y*y)) == 0
assert s.cancel(F.subs(rankone)-alpha*(x*x+y*y)**2) == 0
assert s.cancel(alpha/24-r/(64*(r+2))) == 0
amplitude=s.symbols('amplitude',positive=True)
assert s.simplify(amplitude**4*(amplitude**(-2))**2) == 1

sources=[
    'AGENTS.md','00_START_HERE.txt','frontier/dossiers/N867.txt','frontier/dossiers/N876.txt',
    'updates/FW-moving-heat-observable-20261015/package/derived/workers/sharp_boundary_qc/UNIVERSAL_SHARP_NEGATIVE_CERTIFICATE.json',
    'updates/FW-moving-heat-observable-20261015/package/derived/workers/sharp_boundary_qc/UNIVERSAL_REPORT.txt',
    'updates/FW-moving-heat-observable-20261015/package/derived/workers/nonlinear_flow_audit/UNIVERSAL_QC_ANALYTIC_AUDIT.md',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/sharp_boundary_coercivity/PROOFS.md',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/sharp_boundary_coercivity/CLARIFICATION_20261015_V1.md',
]
provenance={'worktree':str(W),'pinned_revision':PIN,'source_certificate_sha256':CERT_SHA,
            'sources':[{'path':str(W/p),'sha256':hashlib.sha256((W/p).read_bytes()).hexdigest()} for p in sources],
            'write_scope':str(ROOT),'source_writes':False,
            'new_worker_outputs_used_in_initial_construction':False,
            'later_analytic_audit_repair':{
                'auditor':'fy_margin_analytic_audit',
                'repair':'R2 Lemma H explicitly requires D2f in L4 to exclude polynomial f=xy; use smooth rectangular Fourier cutoffs',
                'scope_unchanged':'C1 and U already supply the stronger Hessian assumption'},
            'external_correctness':'UNKNOWN','historical_priority':'UNKNOWN'}
record={
    'algebra_status':'PASS',
    'scope':'Exact polynomial identities and linear-algebra support checks only',
    'Q':str(s.factor(Q)),
    'Q_positive_definiteness_gap':str(positive_gap),
    'Q_derivative_weights':entropy_weights,
    'unique_quadratic_observable_restriction_rank':9,
    'unique_quadratic_minor':str(minor),
    'metric_flux_weights':flux_weights,
    'metric_derivative_restriction_rank':4,
    'metric_minor':str(metric_minor),
    'metric_minor_rows':mx_rows,'metric_minor_columns':mx_cols,
    'metric_null_cone_gaps':{'x':str(cone_x),'y':str(cone_y)},
    'I_quadratic':str(m_expected),'I_cubic_in_S':str(cubic_expected),
    'soft_shear_Laurent_limit':str(soft_lead),
    'scalar_entropy_countermodel':'A=(cos y,sin y) tensor e2; Q=1 while J=alpha',
    'triangular_margin':str(s.factor(alpha/24)),
    'exact_concentration_scale_identity':'a^4*(a^(-2))^2=1; phi_a(x)=a^(-1)phi(a^2(x-x0)), B_a=a B0 preserves Gap and gradient fourth norm',
    'analytic_proof_status':'Construction proof in PROOFS.md; not certified by this script',
    'full_all_affine_margin':'UNRESOLVED','zero_margin_sequence':'NOT_FOUND',
    'external_correctness':'UNKNOWN','historical_priority':'UNKNOWN',
}
(ROOT/'EXACT_CHECKS.json').write_text(json.dumps(record,indent=2)+'\n')
(ROOT/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps({'algebra_status':'PASS','checks_file':str(ROOT/'EXACT_CHECKS.json'),
                  'provenance_file':str(ROOT/'PROVENANCE.json'),
                  'full_all_affine_margin':'UNRESOLVED'},indent=2))
