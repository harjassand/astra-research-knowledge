#!/usr/bin/env python3
"""Independent equation-first reconstruction; imports no producer code.

Checks exact coefficient matrices in the six compatible second-jet variables,
not the producer's scalar expansion routine. All writes stay beside this file.
Analytic and universal-positivity arguments are recorded separately.
"""
from __future__ import annotations

import hashlib
import json
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import time
import sympy as sp

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "sources" / "global_compatible_positivity"
R = sp.Rational
r = sp.symbols("r", real=True)
x = sp.Matrix(sp.symbols("a b c d", real=True))
a, b, c, d = x
z = sp.Matrix(sp.symbols("z0:6", real=True))
checks: list[dict] = []
started = time.monotonic()


def record(label, condition, **data):
    if not bool(condition):
        raise AssertionError(label)
    checks.append(dict(label=label, status="EXACT_PASS", **data))
    print("PASS:", label, flush=True)


def zero(M):
    return all(sp.cancel(v) == 0 for v in M)


def strings(M):
    return [[str(sp.factor(v)) for v in row] for row in M.tolist()]


raw = json.loads((SOURCE / "GLOBAL_COMPLETION_CERTIFICATE.json").read_text())


def constant(name):
    return sp.Matrix([[R(v) for v in row] for row in raw[name]])


def parameter_matrix(name):
    coeffs = [sp.Matrix([[R(v) for v in row] for row in arr]) for arr in raw[name]]
    return (sum((r**k * M for k, M in enumerate(coeffs)), sp.zeros(*coeffs[0].shape)) / (r+1)).applyfunc(sp.cancel)


C = parameter_matrix("C_numerator")
S0 = parameter_matrix("S0_numerator")
SN = parameter_matrix("Snull_numerator")
W0 = parameter_matrix("W0_numerator")
WN = parameter_matrix("Wnull_numerator")
SH, N0, RR = [constant(k) for k in ("SH", "N", "R")]
N = N0[:, raw["P6"] + raw["P4"]]
pair_order = list(combinations(range(4), 2))
mon_order = list(combinations_with_replacement(range(4), 2))
record("input dimensions and order", C.shape == (24,18) and all(M.shape == (18,18) for M in (S0,SN,SH)) and raw["omega_pairs"] == [list(p) for p in pair_order] and raw["omega_monomials"] == [list(p) for p in mon_order])
record("reduced Gram symmetries", all(zero(M-M.T) for M in (S0,SN,SH)))
record("null correction is constant in parameter", all(sp.diff(v,r) == 0 for M in (SN,WN) for v in M))

J1 = sp.zeros(4,6)
J2 = sp.zeros(4,6)
for row,col in enumerate((0,1,3,4)): J1[row,col]=1
for row,col in enumerate((1,2,4,5)): J2[row,col]=1
mons = sp.Matrix([x[i]*x[j] for i,j in mon_order])


def form(W):
    om = sp.zeros(4)
    for (i,j), v in zip(pair_order, W*mons):
        om[i,j], om[j,i] = v, -v
    return om


def corrected_jet_matrix(F, W):
    Hess = sp.hessian(F,x)
    raw_null = J1.T * form(W) * J2
    return J1.T*Hess*J1 + J2.T*Hess*J2 + (raw_null+raw_null.T)/2


def check_tensor_identity(S, F, W, label):
    # At each A monomial compare the entire symmetric six-by-six jet matrix.
    Q = (C*S*C.T).applyfunc(sp.cancel)
    target = corrected_jet_matrix(F,W)
    polys = [[sp.Poly(sp.expand(target[i,j]),*x) for j in range(6)] for i in range(6)]
    for i,j in mon_order:
        qblock = Q[6*i:6*i+6,6*j:6*j+6]
        lhs = qblock if i == j else qblock+qblock.T
        rhs = sp.Matrix(6,6,lambda k,l:polys[k][l].coeff_monomial(x[i]*x[j]))
        record(label+f" A-monomial {i},{j}", zero(lhs-rhs))


u = a*a+c*c
jdet = a*d-b*c
H = ((a-d)**2+(b+c)**2)**2
P3 = 3*H+r*(r-1)*u*u/6+jdet*jdet+r*u*jdet
check_tensor_identity(S0,P3,W0,"universal base identity")
check_tensor_identity(SN,sp.S.Zero,WN,"universal null identity")
check_tensor_identity(SH,H,sp.zeros(6,10),"universal distortion identity")
for name,W in (("base",W0),("null",WN)):
    om = form(W)
    eta = om.T*x/4
    record(name+" closed two-form", all(sp.cancel(sp.diff(om[j,k],x[i])-sp.diff(om[i,k],x[j])+sp.diff(om[i,j],x[k])) == 0 for i,j,k in combinations(range(4),3)))
    record(name+" global Euler primitive", all(sp.cancel(sp.diff(eta[j],x[i])-sp.diff(eta[i],x[j])-om[i,j]) == 0 for i,j in pair_order))
expected_null = sp.Matrix([
    -(a*a-2*a*d+3*b*b+4*b*c+c*c+d*d)/2,
    a*d-b*b-b*c-d*d,
    b*(a-d), d*(b+c), 0,
    -(a*a-4*a*d+b*b+2*b*c+c*c+3*d*d)/2])
record("ordinary-coordinate null form equals report equation 15", zero(WN*mons-expected_null))

# Reconstruct old-contact forced kernel independently of the certificate basis.
t,p,h = sp.symbols("t p h", real=True)
O = sp.Matrix([[p,-h],[h,p]])
At = sp.Matrix([[1,-(r+1)*t],[(r+1)*t,1]])
rotA = O*At
rankonejet = sp.Matrix([p*t*t,p*t,p,h*t*t,h*t,h])
Zt = sp.kronecker_product(sp.Matrix(list(rotA)),rankonejet)
kernel_columns=[]
for order in (0,1):
    derivative=Zt.diff(t,order).subs(t,0)
    for mon in (p*p,p*h,h*h):
        kernel_columns.append(derivative.applyfunc(lambda v:sp.Poly(sp.expand(v),p,h).coeff_monomial(mon)))
K=sp.Matrix.hstack(*kernel_columns)
rows=list(K.T.rref()[1])
kernel_minor=sp.factor(K[rows,:].det())
record("old-contact six forced directions and moving support", len(rows)==6 and zero(C.T*K), row_minor_rows=rows,row_minor=str(kernel_minor))
pivot_rows=[0,3,6,7,9,10,12,13,14,15,16,17,18,19,20,21,22,23]
record("moving basis has rank 18 by identity minor", C[pivot_rows,:] == sp.eye(18))
basis=N.row_join(RR)
basisdet=sp.factor(basis.det())
record("kernel/complement change of basis invertible", basisdet != 0,determinant=str(basisdet))
record("ten-dimensional distortion kernel", SH*N == sp.zeros(18,10))
H8=RR.T*SH*RR
LH,DH=H8.LDLdecomposition(hermitian=False)
record("distortion complement exact positive LDL", LH*DH*LH.T == H8 and all(v>0 for v in DH.diagonal()),pivots=[str(v) for v in DH.diagonal()])
q=r*(r+2); ss=r+1
T=N.T*S0*N
A6=sp.Matrix([[2*q/3,0,0,0,0,0],[0,2*q/3+2,-2*ss,0,-2*ss,0],[0,-2*ss,2*ss**2,0,4*q/3+2,0],[0,0,0,2*ss**2,0,0],[0,-2*ss,4*q/3+2,0,2*ss**2,0],[0,0,0,0,0,2*q/3]])
record("six-dimensional quotient block", zero(T[:6,:6]-A6))
record("null correction is precisely identity on four residual kernel directions", zero(N.T*SN*N-sp.diag(sp.zeros(6),sp.eye(4))))
LA,DA=A6.LDLdecomposition(hermitian=False)
expected=[2*q/3,2*(q+3)/3,2*q*ss**2/(q+3),2*ss**2,2*q*(5*q+3)/(9*ss**2),2*q/3]
record("quotient universal LDL pivot formulas", zero(LA*DA*LA.T-A6) and all(sp.cancel(v-w)==0 for v,w in zip(DA.diagonal(),expected)),pivots=[str(sp.factor(v)) for v in expected])
record("quotient determinant factorization", sp.factor(A6.det()-64*q**4*ss**2*(5*q+3)/243)==0)

alpha,beta,gamma,delta,curve_s=sp.symbols("alpha beta gamma delta curve_s",real=True)
F=alpha*H+beta*u*u+gamma*jdet*jdet+delta*u*jdet
direction=sp.Matrix([t,1,0,0])
acoustic=(direction.T*sp.hessian(F,x).subs({a:1,b:-curve_s*t,c:curve_s*t,d:1})*direction)[0]
claimed=(12*beta+2*gamma*(1-curve_s)**2+(6-4*curve_s)*delta)*t*t+2*curve_s**2*(2*beta+delta)*t**4
record("full-parameter acoustic curve", sp.expand(acoustic-claimed)==0)
record("minimized acoustic coefficient", sp.factor(claimed.coeff(t,2).subs(curve_s,1+delta/gamma)/2-(6*beta+delta-delta**2/gamma))==0)
ac11=sp.diff(F,a,2)
bc_block=sp.hessian(ac11,(b,c))/2
record("finite-alpha strict obstruction block", bc_block == sp.Matrix([[4*alpha,4*alpha-delta],[4*alpha-delta,4*(alpha+beta)]]) and sp.expand(bc_block.det()-8*alpha*(2*beta+delta)+delta**2)==0)
record("gamma and alpha tests", sp.diff(F,b,2).subs({a:0,b:1,c:-1,d:0})==2*gamma and F.subs({a:0,b:1,c:0,d:0})==alpha)
record("r=-2 determinant is always -4", sp.expand(bc_block.det().subs({beta:1,delta:-2})) == -4)
gamma0=delta**2/(6*beta+delta); r0=(6*beta+delta)/delta
decomp=gamma0*((alpha/gamma0)*H+r0*(r0-1)*u*u/6+jdet*jdet+r0*u*jdet)+(gamma-gamma0)*jdet*jdet
record("whole projected-cone core-plus-minor decomposition", sp.cancel(F-decomp)==0)

# Regenerate the full invariant/contact linear spaces rather than taking their
# advertised dimensions as premises.
quartic_mons=[sp.prod(x[i] for i in inds) for inds in combinations_with_replacement(range(4),4)]
def quartic_vector(pol):
    poly=sp.Poly(sp.expand(pol),*x)
    return sp.Matrix([poly.coeff_monomial(mon) for mon in quartic_mons])
rotation_derivative=lambda pol:-c*sp.diff(pol,a)-d*sp.diff(pol,b)+a*sp.diff(pol,c)+b*sp.diff(pol,d)
Lie=sp.Matrix.hstack(*(quartic_vector(rotation_derivative(mon)) for mon in quartic_mons))
v=b*b+d*d; w=a*b+c*d
invariant_basis=[u*u,v*v,u*v,w*w,u*w,v*w,u*jdet,v*jdet,w*jdet]
invariant_coefficients=sp.Matrix.hstack(*(quartic_vector(pol) for pol in invariant_basis))
record("nine-dimensional left-SO2 invariant quartic space regenerated", Lie.rank()==26 and invariant_coefficients.rank()==9 and Lie*invariant_coefficients == sp.zeros(35,9))
fcoeff=sp.symbols("fcoeff0:9")
general_invariant=sum(fc*pol for fc,pol in zip(fcoeff,invariant_basis))
n,m=sp.symbols("n m",real=True)
testdir=sp.Matrix([n,m,0,0])
general_ac=(testdir.T*sp.hessian(general_invariant,x)*testdir)[0]
contact={a:1,b:0,c:0,d:1,n:0,m:1}
contact_rows=[sp.diff(general_ac,var).subs(contact) for var in list(x)+[n,m]]
contact_matrix,_=sp.linear_eq_to_matrix(contact_rows,fcoeff)
face_polynomials=[H,u*u,jdet*jdet,u*jdet]
record("entire contact-face linear space regenerated", contact_matrix.rank()==5 and sp.Matrix.hstack(*(quartic_vector(pol) for pol in face_polynomials)).rank()==4 and all(sp.diff((testdir.T*sp.hessian(pol,x)*testdir)[0],var).subs(contact)==0 for pol in face_polynomials for var in list(x)+[n,m]))

# Reconstruct the receiving sharp ROC theorem from its advertised four-square
# identity; this assertion is stronger than the new source's existence test.
alpha_floor=3*r/(8*(r+2))
Pr=alpha*H+r*(r-1)*u*u/6+jdet*jdet+r*u*jdet
xx=a-d; yy=b+c
L1=2*(r+1)**2*n*a-2*(r+1)*m*c-(3*r+2)*n*xx
L2=2*(r+1)*(r+2)*n*c-3*m*xx-3*(r+1)*n*yy
L3=(2*r+1)*n*xx+3*(r+1)*m*yy
L4=m*xx
roc_squares=L1**2/(2*(r+1)**2)+r*L2**2/(6*(r+1)**2*(r+2))+r*L3**2/(2*(r+1)**2*(r+2))+3*r*r*L4**2/(2*(r+1)**2)+4*(alpha-alpha_floor)*((xx*xx+yy*yy)*(n*n+m*m)+2*(n*xx+m*yy)**2)
roc_acoustic=(testdir.T*sp.hessian(Pr,x)*testdir)[0]
record("receiving sharp ROC four-square identity independently regenerated", sp.cancel(roc_acoustic-roc_squares)==0)
floor_point={a:0,b:(2*r+1)/3,c:1,d:0}
record("receiving exact below-floor rank-one witness", sp.factor(sp.diff(Pr,a,2).subs(floor_point)-16*(r+2)**2*(alpha-alpha_floor)/9)==0)
alpha0=delta**2/(8*(2*beta+delta))
sharp_decomp=gamma0*Pr.subs({alpha:alpha_floor,r:r0},simultaneous=False)+(gamma-gamma0)*jdet*jdet+(alpha-alpha0)*H
record("receiving full two-LMI sharp decomposition", sp.cancel(F-sharp_decomp)==0)

# Reconstruct the stronger polyconvex-support obstruction for every alpha.
minor_slope=sp.symbols("minor_slope",real=True)
Ipoint={a:1,b:0,c:0,d:1}
lift=Pr-minor_slope*jdet
record("polyconvex support forces determinant slope r+2", sp.diff(lift,b,c).subs(Ipoint)==minor_slope-r-2 and sp.diff(lift,b,2).subs(Ipoint)==0)
lift=lift.subs(minor_slope,r+2)
V=sp.Matrix([1,0,0,-r-1])
record("all-alpha lifted Hessian kernel", zero(sp.hessian(lift,x).subs(Ipoint)*V))
curve={a:1+t,b:0,c:0,d:1-(r+1)*t}
linear=sum(sp.diff(lift,xi).subs(Ipoint)*vi*t for xi,vi in zip(x,V))
gap=sp.Poly(sp.expand(lift.subs(curve)-lift.subs(Ipoint)-linear),t)
cubic=sp.factor(gap.coeff_monomial(t**3))
quartic=sp.factor(gap.coeff_monomial(t**4))
record("non-polyconvex cubic support gap for every alpha", cubic == -r*(r+2)/3,cubic=str(cubic),quartic=str(quartic))

# Direct exact Fourier coefficient audit, using finite coefficient dictionaries.
X,Y,k=sp.symbols("X Y k",nonzero=True)
sx=(X-X**-1)/(2*sp.I); sy=(Y-Y**-1)/(2*sp.I)
cx=(X+X**-1)/2; cy=(Y+Y**-1)/2
f=k*(sx+sy)
g=-k**4*(X**2+X**-2+Y**2+Y**-2)/4+2*k*k*sx*sy
dx=lambda v:sp.expand(sp.I*X*sp.diff(v,X))
dy=lambda v:sp.expand(sp.I*Y*sp.diff(v,Y))
dt=lambda v:sp.expand(-k*sp.diff(v,k))
def average(v):
    terms=sp.expand(v).as_ordered_terms()
    return sp.simplify(sum(term for term in terms if term.as_powers_dict().get(X,0)==0 and term.as_powers_dict().get(Y,0)==0))
record("both exact heat equations", dt(f)-dx(dx(f))-dy(dy(f))==0 and dt(g)-dx(dx(g))-dy(dy(g))==0)
AA=sp.Matrix([dx(f),dy(f),dx(g),dy(g)])
detAA=sp.expand(AA[0]*AA[3]-AA[1]*AA[2])
record("compatible determinant along heat", sp.expand(detAA-2*(k**3-k**5)*cx*cy*(sx-sy))==0)
energy=sp.factor(average(detAA**2))
ep=sp.factor(dt(energy))
record("exact periodic determinant-square energy", energy == (k**3-k**5)**2/2 or sp.expand(energy-(k**3-k**5)**2/2)==0,energy=str(energy),derivative=str(ep))
k0=R(9,10)
expected_d=R(212044959,2000000000)
record("exact positive heat derivative", ep.subs(k,k0)==expected_d)
hf=sp.hessian(jdet*jdet,x).subs(dict(zip(x,AA)))
diss=(AA.applyfunc(dx).T*hf*AA.applyfunc(dx))[0]+(AA.applyfunc(dy).T*hf*AA.applyfunc(dy))[0]
integrated=sp.factor(average(diss))
record("direct negative compatible integrated heat dissipation", sp.expand(integrated+ep)==0 and integrated.subs(k,k0)==-expected_d,full_parameter_formula=str(integrated),at_9_10=str(integrated.subs(k,k0)))

instances=[]
for rr in (R(-11,4),R(1),R(1,2)):
    S0r=S0.subs(r,rr); SNr=SN; Ar=A6.subs(r,rr)
    tr=N.T*S0r*N
    Br=tr[:6,6:]; Er=tr[6:,6:]
    K4=Er-Br.T*Ar.inv()*Br
    lam=1+max(sum(abs(K4[i,j]) for j in range(4)) for i in range(4))
    S1=S0r+lam*SNr
    P=N.T*S1*N; U=N.T*S1*RR; V8=RR.T*S1*RR
    K8=V8-U.T*P.inv()*U
    KT=LH.inv()*K8*LH.inv().T
    mu=1+max(sum(abs(KT[i,j]) for j in range(8))/DH[i,i] for i in range(8))
    M=S1+mu*SH
    LM,DM=M.LDLdecomposition(hermitian=False)
    record(f"independent exact rational completion at r={rr}", LM*DM*LM.T==M and all(v>0 for v in DM.diagonal()),lambda_value=str(lam),mu_value=str(mu),alpha_star=str(4+mu))
    instances.append(dict(r=str(rr),lambda_value=str(lam),mu_value=str(mu),alpha_star=str(4+mu),sufficient_integer=str(sp.ceiling(4+mu)),pivots=[str(v) for v in DM.diagonal()]))
    if rr == 1:
        integer_alpha=sp.ceiling(4+mu)
        integer_gram=S1+(integer_alpha-4)*SH
        LI,DI=integer_gram.LDLdecomposition(hermitian=False)
        record("exported positive-r1 integer completion exact LDL", LI*DI*LI.T==integer_gram and all(v>0 for v in DI.diagonal()))
        output=dict(schema="astra-independent-positive-r1-completion-v1",r="1",alpha=str(integer_alpha),beta="0",gamma="1",delta="1",subtracted_H="1",integrated_margin_at_least="4/1875",lambda_value=str(lam),diffusion=[[1,0],[0,1]],C=strings(C.subs(r,rr)),S=strings(integer_gram),omega=strings(W0.subs(r,rr)+lam*WN),positive_ldl_pivots=[str(v) for v in DI.diagonal()],omega_pairs=raw["omega_pairs"],omega_monomials=raw["omega_monomials"],matrix_entry_order=raw["matrix_entry_order"],jet_order=raw["jet_order"],scope="Independent internal exact export. The all-background QC implication uses the written analytic proof. Non-polyconvexity follows from the all-alpha cubic support obstruction; sharp positive QC remains unknown.")
        (HERE/"POSITIVE_R1_COMPLETION.json").write_text(json.dumps(output,indent=2)+"\n")

receipt=dict(schema="astra-independent-global-completion-reconstruction-v1",status="EXACT_RECONSTRUCTION_PASS",source_certificate_sha256=hashlib.sha256((SOURCE/"GLOBAL_COMPLETION_CERTIFICATE.json").read_bytes()).hexdigest(),sympy_version=sp.__version__,checks=checks,instances=instances,elapsed_seconds=time.monotonic()-started,scope="Independent internal exact algebra. Universal Schur positivity, analytic implication and the lifted-support theorem are separately argued in AUDIT.md. No external verification or novelty clearance.")
(HERE/"RECONSTRUCTION_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print("EXACT_RECONSTRUCTION_PASS",flush=True)
