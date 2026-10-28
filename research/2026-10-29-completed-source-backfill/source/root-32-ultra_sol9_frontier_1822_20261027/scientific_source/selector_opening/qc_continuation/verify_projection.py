#!/usr/bin/env python3
"""Exact projection/lift constructor and general symbolic identity replay.

Only this continuation's outputs are written. No producer code or solver
is imported. The proof of convexity/quantifiers is in PROOF.md.
"""
from pathlib import Path
import json
import time
import sympy as s

started=time.perf_counter()
OUT=Path(__file__).resolve().parent
a,b,c,d=s.symbols('a b c d',real=True)
vs=(a,b,c,d)
A=s.Matrix([[a,b],[c,d]])
J=s.Matrix([[-b,a],[d,-c]])
T=sum(xx*xx for xx in vs)
q=A.det()
h=s.Matrix([a*a+c*c-b*b-d*d,2*(a*b+c*d),2*q])
assert s.expand((h.T*h)[0]-T*T)==0
subJ=dict(zip(vs,list(J)))
for hh in h:
    assert s.expand(hh.subs(subJ,simultaneous=True)+hh)==0
assert s.expand(T.subs(subJ,simultaneous=True)-T)==0

rt=s.sqrt(2)/2
rotations=[s.eye(2),s.Matrix([[rt,-rt],[rt,rt]]),
           s.Matrix([[0,-1],[1,0]]),s.Matrix([[-rt,-rt],[rt,-rt]])]
def substitute(poly,B):
    return s.expand(poly.subs(dict(zip(vs,list(B))),simultaneous=True))
def row_project(poly):
    return s.expand(sum(substitute(poly,R*A) for R in rotations)/4)
def project(poly):
    row=row_project(poly)
    return s.expand((row+substitute(row,J))/2)
def energy(B,aa,bb,cc):
    tt=sum(vv*vv for vv in B)
    qq=B.det()
    return s.expand(aa*tt*tt+bb*tt*qq+cc*qq*qq)

# General output map, with all four entries independent.
p00,p01,p10,p11=s.symbols('p00 p01 p10 p11',real=True)
P=s.Matrix([[p00,p01],[p10,p11]])
iso_a,iso_b,iso_c=s.symbols('iso_a iso_b iso_c',real=True)
C0=sum(pp*pp for pp in P)/2
detP=P.det()
C1sq=s.expand(C0*C0-detP*detP)
AA=C0*C0+C1sq/2
ha,hb,hc=iso_a*AA,iso_b*C0*detP,iso_c*detP**2-2*iso_a*C1sq
literal_row=s.expand(sum(energy(P*R*A,iso_a,iso_b,iso_c) for R in rotations)/4)
assert s.expand(literal_row-energy(A,ha,hb,hc))==0

# Full input map (including arbitrary orientation/shear); the closed form
# uses no eigenvectors, inverses, lambda denominators, or square roots.
s00,s01,s10,s11=s.symbols('s00 s01 s10 s11',real=True)
S=s.Matrix([[s00,s01],[s10,s11]])
tau,mu=s.symbols('tau mu',real=True)
SD=S*S.T
D0=(SD[0,0]+SD[1,1])/2
D1=(SD[0,0]-SD[1,1])/2
D2=SD[0,1]
detS=S.det()
assert s.expand(D0*D0-D1*D1-D2*D2-detS*detS)==0
v=s.Matrix([D1,D2,tau*detS])
rho_sq=(v.T*v)[0]
assert s.expand(D0*D0-rho_sq-(1-tau*tau)*detS*detS)==0
S4=T*T-2*q*q
convex_part=s.expand((1-tau*tau)*detS*detS*S4+rho_sq*T*T+(v.T*h)[0]**2)
literal_spin=(energy(A*S,1,4*tau,6*tau*tau-2)
             +energy(J*S,1,4*tau,6*tau*tau-2))/2
assert s.expand(literal_spin-convex_part)==0

# Exact inherited nonnegative mu formula from the output-map reduction.
z0,z1,dp=s.symbols('z0 z1 dp',real=True)
zAA=z0*z0+z1*z1/2
mu_old=iso_c+2*iso_a-3*iso_b**2/(8*iso_a)
mu_new=iso_c*dp*dp-2*iso_a*z1*z1+2*iso_a*zAA-3*iso_b**2*z0*z0*dp*dp/(8*iso_a*zAA)
mu_formula=mu_old*dp*dp+iso_a*z1*z1+3*iso_b**2*z1*z1*dp*dp/(16*iso_a*zAA)
assert s.cancel((mu_new-mu_formula).subs(dp*dp,z0*z0-z1*z1))==0

# Convexity of S4 is verified by a literal general Hessian SOS identity.
X=s.Matrix(2,2,s.symbols('x0:4',real=True))
H=s.hessian(S4,vs)
vecX=s.Matrix(list(X))
left=(vecX.T*H*vecX)[0]
N=A.T*X+X.T*A
right=2*sum(nn*nn for nn in N)+4*sum(xx*xx for xx in X*A.T)
assert s.expand(left-right)==0

# The eight-evaluation map is the exact rank-six projection on the full
# ordinary 35-dimensional quartic space, not just on the chosen W family.
monomials=[]
for aa in range(5):
    for bb in range(5-aa):
        for cc in range(5-aa-bb):
            dd=4-aa-bb-cc
            monomials.append(a**aa*b**bb*c**cc*d**dd)
images=[project(mm) for mm in monomials]
projection_matrix=s.Matrix([[s.Poly(im,*vs).coeff_monomial(mm) for im in images]
                            for mm in monomials])
assert projection_matrix*projection_matrix==projection_matrix
assert projection_matrix.rank()==6
for ii in range(3):
    for jj in range(ii,3):
        assert s.expand(project(h[ii]*h[jj])-h[ii]*h[jj])==0

def construct(aa,bb,cc,PP,SS):
    """Acquire rational polynomial lift of projected generator, at fixed size."""
    aa,bb,cc=map(s.Rational,(aa,bb,cc))
    if aa==0:
        assert bb==0 and cc>=0
        return s.Integer(0),s.factor(cc*PP.det()**2*SS.det()**2),{}
    assert aa>0 and abs(bb)<=4*aa and cc>=-2*aa+3*bb*bb/(8*aa)
    pC0=sum(pp*pp for pp in PP)/2
    pD=PP.det()
    pC1sq=pC0*pC0-pD*pD
    pAA=pC0*pC0+pC1sq/2
    if pAA==0:
        return s.Integer(0),s.Integer(0),{'zero_output_map':True}
    newa=aa*pAA
    newb=bb*pC0*pD
    newc=cc*pD*pD-2*aa*pC1sq
    newt=s.factor(newb/(4*newa))
    newmu=s.factor(newc+2*newa-3*newb*newb/(8*newa))
    assert abs(newt)<=1 and newmu>=0
    DD=SS*SS.T
    vv=s.Matrix([(DD[0,0]-DD[1,1])/2,DD[0,1],newt*SS.det()])
    rr=(vv.T*vv)[0]
    convex=s.expand(newa*((1-newt*newt)*SS.det()**2*S4+rr*T*T+(vv.T*h)[0]**2))
    gamma=s.factor(newmu*SS.det()**2)
    return convex,gamma,{'row_a':str(newa),'row_t':str(newt),'row_mu':str(newmu)}

# Ordinary control is itself a known isotropic QC/non-PC boundary quartic.
# Its value at diag(1,-1) is -1/2; the projection constructor nevertheless
# supplies a PC lift after arbitrary nonorthogonal maps.
PP=s.Matrix([[2,1],[1,1]])
SS=s.Matrix([[3,1],[1,-2]])
control_W=energy(A,1,2,s.Rational(-1,2))
assert substitute(control_W,s.diag(1,-1))==s.Rational(-1,2)
control_C,control_gamma,control_parameters=construct(1,2,s.Rational(-1,2),PP,SS)
assert s.expand(project(energy(PP*A*SS,1,2,s.Rational(-1,2)))-control_C-control_gamma*q*q)==0
assert control_gamma>=0
assert all(coef.is_Rational for coef in s.Poly(control_C,*vs).coeffs())

controls=[]
for label,aa,bb,cc,PP0,SS0 in [
    ('negative_orientation',1,2,s.Rational(-1,2),PP,SS),
    ('singular_output',1,2,s.Rational(-1,2),s.Matrix([[1,2],[2,4]]),SS),
    ('zero_output',1,2,s.Rational(-1,2),s.zeros(2),SS),
    ('singular_input',1,2,s.Rational(-1,2),PP,s.Matrix([[1,2],[2,4]])),
    ('pure_det_squared',0,0,3,PP,SS)]:
    cp,gg,params=construct(aa,bb,cc,PP0,SS0)
    assert s.expand(project(energy(PP0*A*SS0,aa,bb,cc))-cp-gg*q*q)==0
    controls.append({'label':label,'status':'EXACT_CONSTRUCTOR_IDENTITY_PASS','gamma':str(gg),**params})

data={
    'status':'EXACT_PROJECTION_NORMAL_FORM_PASS',
    'projection_evaluations':8,'ordinary_quartic_dimension':35,'projection_rank':6,
    'projection_idempotent':True,
    'general_four_entry_output_map_row_identity':'PASS',
    'general_four_entry_input_map_spin_identity':'PASS',
    'output_mu_nonnegative_decomposition_identity':'PASS',
    'convex_S4_Hessian_SOS_identity':'PASS',
    'control_original_W_value_at_anticonformal':'-1/2',
    'control_convex_part':str(control_C),'control_gamma':str(control_gamma),
    'controls':controls,
    'QC_of_new_even_target':'UNKNOWN',
    'route_status':'ALL_POSITIVE_TRANSPORTED_ISOTROPIC_QC_PLUS_PC_DECOMPOSITIONS_EXCLUDED',
    'runtime_seconds':time.perf_counter()-started}
(OUT/'REPLAY.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
