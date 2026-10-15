#!/usr/bin/env python3
"""Exact supporting algebra and one compatible candidate family.

The exact checks support the accompanying analytic derivations. Numerical
quadrature/linear algebra supplies candidate values only, not a lower-bound
certificate. No source/worktree files are changed.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-sharp-ion-20261015')
PIN = 'b32943eeb62d0d79929a9e572a344219a785ebf9'

r, a, b, c, d = s.symbols('r a b c d', real=True)
alpha = 3*r/(8*(r+2))
beta = r*(r-1)/6
C = r*(r+2)/3
u = a*a+c*c
j = a*d-b*c
J = alpha*((a-d)**2+(b+c)**2)**2 + beta*u*u+j*j+r*u*j
qvars = (a,b,c,d)
DJ = s.Matrix([s.diff(J,v) for v in qvars])
HJ = s.hessian(J, qvars)
p, z, w, shear, e, t = s.symbols('p z w shear e t', real=True)

expanded = s.Poly(s.expand(J.subs({a:1+t*p,b:t*shear,c:t*w,d:1+t*z})),t)
quadratic = expanded.coeff_monomial(t**2)
cubic = expanded.coeff_monomial(t**3)
soft_e = (r+1)*p+z
expected_quad = soft_e**2+C*w*w+(r+2)*(p*z-shear*w)
expected_cubic = (
    2*p*e*e+(-2*shear*w-(r+2)*p*p+r*w*w)*e
    -C*p*(p*p+w*w)
)
assert s.factor(quadratic-expected_quad)==0
assert s.factor(cubic.subs(z,e-(r+1)*p)-expected_cubic)==0

eps, P, S, Q = s.symbols('eps P S Q', real=True)
qsub = {a:eps*P,b:S,c:eps**2*Q,d:-(r+1)*eps*P}
Jq = s.factor(J.subs(qsub))
Lq = DJ.subs(qsub)
Mq = HJ.subs(qsub)/2
ivec = s.Matrix([1,0,0,1])
vvec = s.Matrix([1,0,0,-1])
assert s.factor((ivec.T*Lq)[0] + C*eps**3*P*(P*P+eps**2*Q*Q))==0
# These are pointwise identities; the determinant term integrates to zero.
mi = s.simplify(ivec.T*Mq)
assert s.factor(mi[1])==0
assert s.factor(mi[2]+C*eps**3*P*Q)==0
assert s.factor((ivec.T*Mq*vvec)[0]
                -(-r*eps**2*P*P+r*(r-1)*eps**4*Q*Q/3)
                +r*eps**2*((r+1)*P*P+S*Q))==0
assert s.factor((ivec.T*Mq*ivec)[0]
                - (C*eps**4*Q*Q+(r+2)*eps**2*(-(r+1)*P*P-S*Q)))==0
assert s.factor(Jq.subs(eps,0)-alpha*S**4)==0

# Calibration for the large-frequency logspiral. cth^2+sth^2=1 is imposed
# by direct trigonometric substitution. sigma is checked at both signs.
theta, radial, nu, gnorm = s.symbols('theta radial nu gnorm', real=True)
cth, sth = s.cos(theta), s.sin(theta)
P0 = alpha*(1+nu*nu)**2+beta*(cth-sth*nu)**4
calibrations = {}
for sig in (-1,1):
    # g=gnorm*e1; first column sig*Jg; second gnorm*(radial*e1+sig*nu*e2).
    aa=-gnorm*sth*radial
    bb=gnorm*cth*radial
    cc=sig*gnorm*(cth-sth*nu)
    dd=sig*gnorm*(sth+cth*nu)
    poly=s.factor(J.subs({a:aa,b:bb,c:cc,d:dd})/gnorm**4)
    expected=(alpha*(1+radial*radial+nu*nu+2*sig*radial)**2
              +beta*(sth*sth*radial*radial+(cth-sth*nu)**2)**2
              +radial*radial-r*sig*radial*(sth*sth*radial*radial+(cth-sth*nu)**2))
    assert s.trigsimp(poly-expected)==0
    assert s.trigsimp(poly.subs(radial,0)-P0)==0
    mu=sig*(4*alpha*(1+nu*nu)-r*(cth-sth*nu)**2)
    assert s.trigsimp(s.diff(poly,radial).subs(radial,0)-mu)==0
    calibrations[str(sig)]={'radial_support_coefficient':str(mu)}
assert s.simplify(s.diff(P0,nu)/4-
                  (alpha*nu*(1+nu*nu)-beta*sth*(cth-sth*nu)**3))==0

exact_receipt={
    'schema':'astra.fy-margin-counterconstruction.exact-support.v1',
    'status':'PASS for listed polynomial identities; analytic proofs separate',
    'pin':PIN,
    'checks':[
        'contact expansion quadratic including determinant null term',
        'correct full cubic in e=(r+1)p+z',
        'compatible slow-fast I-column of affine matrix and cubic scaling',
        'slow-fast tracefree diagonal cross term modulo determinant identity',
        'slow-fast leading quartic equals alpha*S^4',
        'logspiral rank-one calibration polynomial for both frequency signs',
        'logspiral radial support coefficient',
        'calibration minimizer equation',
    ],
    'calibration':calibrations,
}

rv=-2.5
jfun=s.lambdify(qvars,J.subs(r,rv),'numpy',cse=True)
lfuns=[s.lambdify(qvars,x.subs(r,rv),'numpy',cse=True) for x in DJ]
mfuns=[[s.lambdify(qvars,HJ[i,k].subs(r,rv)/2,'numpy',cse=True)
        for k in range(4)] for i in range(4)]
n=64
X,Y=np.meshgrid(np.arange(n)*2*np.pi/n,np.arange(n)*2*np.pi/n,indexing='ij')
# f=sin y+.2 sin(2y)+.35 sin X sin y+.12 sin(2X)cos(2y).
Sval=np.cos(Y)+.4*np.cos(2*Y)+.35*np.sin(X)*np.cos(Y)-.24*np.sin(2*X)*np.sin(2*Y)
Pval=.35*np.cos(X)*np.sin(Y)+.24*np.cos(2*X)*np.cos(2*Y)
# Q=-(r+1)partial_XX partial_y^{-1} f.
Qval=-(rv+1)*(.35*np.sin(X)*np.cos(Y)-.24*np.sin(2*X)*np.sin(2*Y))
mean=lambda x:float(np.mean(x))
m2,m3,m4=map(mean,(Sval**2,Sval**3,Sval**4))
aval=float(alpha.subs(r,rv))
limit=aval*(1-2*m3*m3/(3*m2*m4))
det_residual=mean(-(rv+1)*Pval**2-Sval*Qval)
rows=[]
for ev in (.5,.25,.125,.0625,.03125,.015625,.0078125):
    q=(ev*Pval,Sval,ev**2*Qval,-(rv+1)*ev*Pval)
    K=mean(jfun(*q))
    Lv=np.array([mean(f(*q)) for f in lfuns])
    Mv=np.array([[mean(f(*q)) for f in row] for row in mfuns])
    Bv=-np.linalg.solve(Mv,Lv)/2
    residual=K+float(Lv@Bv+Bv@Mv@Bv)
    norm=mean(sum(x*x for x in q)**2)
    ii=np.array([1.,0.,0.,1.])
    mt=float(ii@Mv@ii)
    lt=float(ii@Lv)
    rayt=-lt/(2*mt)
    rayres=K-lt*lt/(4*mt)
    direct=mean(jfun(q[0]+Bv[0],q[1]+Bv[1],q[2]+Bv[2],q[3]+Bv[3])
                -jfun(*Bv))
    rows.append({
        'epsilon':ev,'full_affine_ratio':residual/norm,
        'restricted_tI_ratio':rayres/norm,'optimal_B_row_major':Bv.tolist(),
        'optimal_t_on_I_ray':rayt,'affine_matrix_min_eigenvalue':float(np.linalg.eigvalsh(Mv)[0]),
        'affine_matrix_condition_number':float(np.linalg.cond(Mv)),
        'direct_evaluation_gap_difference':direct-residual,
    })
numeric_receipt={
    'schema':'astra.fy-margin-counterconstruction.compatible-candidate.v1',
    'status':'finite floating-point diagnostics only; not a lower-bound proof',
    'r':rv,'quadrature':{'grid':[n,n],'max_input_frequency':2,
                        'quartic_trig_quadrature':'exact in exact arithmetic at this resolution'},
    'profile':'sin y+.2 sin(2y)+.35 sin X sin y+.12 sin(2X)cos(2y)',
    'compatibility_determinant_mean_residual':det_residual,
    'limiting_ratio_formula':'alpha*(1-2*m3^2/(3*m2*m4))',
    'limiting_ratio_value':limit,'rank_one_lower_bound':aval/3,
    'rows':rows,
}

source_paths=[
    'AGENTS.md','frontier/dossiers/N867.txt','frontier/dossiers/N876.txt',
    'updates/FW-moving-heat-observable-20261015/package/derived/workers/sharp_boundary_qc/UNIVERSAL_REPORT.txt',
    'updates/FW-moving-heat-observable-20261015/package/derived/workers/contact_face_priority_audit/STRUCTURAL_PROOF.txt',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/sharp_boundary_coercivity/PROOFS.md',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/sharp_boundary_coercivity/CLARIFICATION_20261015_V1.md',
]
inputs={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in source_paths}
(HERE/'EXACT_SUPPORT_RECEIPT.json').write_text(json.dumps(exact_receipt,indent=2)+'\n')
(HERE/'COMPATIBLE_CANDIDATE_DIAGNOSTICS.json').write_text(json.dumps(numeric_receipt,indent=2)+'\n')
(HERE/'INPUTS_SHA256.json').write_text(json.dumps({'pin':PIN,'files':inputs},indent=2)+'\n')
print(json.dumps({'exact_status':exact_receipt['status'],'candidate_limit':limit,
                  'last_full_affine_ratio':rows[-1]['full_affine_ratio'],
                  'determinant_residual':det_residual},indent=2))
