#!/usr/bin/env python3
"""Independent verification of the new Fstar-only closed heat certificate.

Reads the certificate as data. Does not import producer/search code.
All computations below are over Q; analytic implication in REPORT.txt.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sympy as S

HERE=Path(__file__).resolve().parent
path=HERE.parent / "FE-quartic/checks/FSTAR_CLOSED_HEAT_CERTIFICATE.json"
raw=path.read_bytes(); data=json.loads(raw)
x=S.symbols("a b c d"); a,b,c,d=x
jet=S.symbols("r0:6")
u,v,w,q=a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
gamma=S.Rational(data["gamma"])
F=u*u+v*v+4*w*w+S.Rational(7,2)*q*q-S.Rational(29,10)*q*(u+v)
G=F-gamma*q*q
assert gamma>=0
Q=S.Matrix([[S.Rational(z) for z in row] for row in data["gram"]])
assert Q==Q.T and Q.shape==(24,24)
L,D=Q.LDLdecomposition(hermitian=False)
pivots=list(D.diagonal())
assert all(z>0 for z in pivots)
assert L*D*L.T==Q
assert pivots==list(map(S.Rational,data["ldl_diagonal"]))
bilinear=S.Matrix([a*z for a in x for z in jet])
B1=S.Matrix([jet[0],jet[1],jet[3],jet[4]])
B2=S.Matrix([jet[1],jet[2],jet[4],jet[5]])
H=S.hessian(G,x)
energy=(B1.T*H*B1+B2.T*H*B2)[0]
omega=S.zeros(4)
for pair,row in zip(data["omega_pair_order"],data["omega_coefficients"]):
    i,j=pair
    poly=sum(S.Rational(z)*x[k]*x[l] for (k,l),z in zip(data["quadratic_coefficient_order"],row))
    omega[i,j],omega[j,i]=poly,-poly
evaluation=(B1.T*omega*B2)[0]
identity=S.Poly(S.expand((bilinear.T*Q*bilinear)[0]-energy-evaluation),x+jet)
assert identity.is_zero
closure=[]
for i,j,k in itertools.combinations(range(4),3):
    z=S.expand(S.diff(omega[j,k],x[i])-S.diff(omega[i,k],x[j])+S.diff(omega[i,j],x[k]))
    assert z==0; closure.append(str(z))
alpha=S.Matrix([sum(x[i]*omega[i,j] for i in range(4))/4 for j in range(4)])
for i,j in itertools.combinations(range(4),2):
    assert S.expand(S.diff(alpha[j],x[i])-S.diff(alpha[i],x[j])-omega[i,j])==0
# Compactly replay the pure-compatible-jet reduction: omega vanishes and
# the heat density becomes |xi|^2 D2G[A][eta outer xi,eta outer xi].
eta0,eta1,k0,k1=S.symbols("eta0 eta1 k0 k1")
sub=dict(zip(jet,[eta0*k0*k0,eta0*k0*k1,eta0*k1*k1,eta1*k0*k0,eta1*k0*k1,eta1*k1*k1]))
rankone=S.Matrix([eta0*k0,eta0*k1,eta1*k0,eta1*k1])
assert S.expand(evaluation.subs(sub))==0
assert S.expand(energy.subs(sub)-(k0*k0+k1*k1)*(rankone.T*H*rankone)[0])==0
rho=S.Rational(1,500)
shiftL,shiftD=(Q-rho*S.eye(24)).LDLdecomposition(hermitian=False)
assert all(z>0 for z in shiftD.diagonal())
assert shiftL*shiftD*shiftL.T==Q-rho*S.eye(24)
def diss(f):
    h=S.hessian(f,x)
    return S.expand((B1.T*h*B1+B2.T*h*B2)[0])
basis=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
perturb=[]
for f in basis:
    R=S.zeros(24)
    for exponents,coefficient in S.Poly(diss(f),x+jet).terms():
        aa=[i for i,n in enumerate(exponents[:4]) for _ in range(n)]
        jj=[i for i,n in enumerate(exponents[4:]) for _ in range(n)]
        assert len(aa)==len(jj)==2
        row,col=6*aa[0]+jj[0],6*aa[1]+jj[1]
        if row==col:R[row,col]+=coefficient
        else:R[row,col]+=coefficient/2;R[col,row]+=coefficient/2
    assert R==R.T and S.expand((bilinear.T*R*bilinear)[0]-diss(f))==0
    perturb.append(R)
envelope=S.zeros(24)
for R in perturb:envelope+=R.applyfunc(abs)
K=max(sum(envelope[i,j] for j in range(24)) for i in range(24))
assert K==82
eta=rho/(2*K)
assert eta==S.Rational(1,82000)
moments=[S.expand(f.subs({a:7,b:0,c:0,d:7})/50+S.Rational(49,50)*f.subs({a:1,b:0,c:0,d:-1})) for f in basis]
assert moments==[49,49,49,0,0,0,S.Rational(1176,25),S.Rational(1176,25),0]
witness=sum(z*m for z,m in zip([1,1,S.Rational(7,2),S.Rational(1,2),0,0,-S.Rational(29,10),-S.Rational(29,10),0],moments))
witness_upper=witness+eta*sum(abs(z) for z in moments)
assert witness_upper==-S.Rational(166453,50000)
# Exact SOS identities for the two analytic inequalities used in the
# Jensen-gap corollary. No angular/directional sample is used.
norm=sum(z*z for z in x)
cauchy=sum((x[i]*B[j]-x[j]*B[i])**2 for B in (B1,B2) for i,j in itertools.combinations(range(4),2))
residual=12*norm*(jet[0]**2+jet[2]**2+jet[3]**2+jet[5]**2)+8*cauchy
assert S.expand(24*norm*sum(z*z for z in jet)-diss(norm**2)-residual)==0
increment=S.symbols("h0:4")
hnorm=sum(z*z for z in increment)
dot=sum(z*y for z,y in zip(x,increment))
rel=(norm**2).subs(dict(zip(x,[z+y for z,y in zip(x,increment)])),simultaneous=True)-norm**2-4*norm*dot
resid=6*(dot+hnorm/3)**2+2*sum((x[i]*increment[j]-x[j]*increment[i])**2 for i,j in itertools.combinations(range(4),2))
assert S.expand(rel-hnorm**2/3-resid)==0
result={
    "status":"PASS",
    "certificate_sha256":hashlib.sha256(raw).hexdigest(),
    "gamma":str(gamma),
    "checks":["Q symmetric 24 by 24", "exact LDL factor identity", "all 24 exact positive pivots", "producer pivot values agree", "210-coefficient degree-(2,2) heat Gram identity", "all 4 exterior-closure identities", "explicit polynomial primitive alpha=(1/4)i_R omega", "pure compatible jets remove omega and force G rank-one convex", "Q-(1/500)I exact positive LDL", "nine exact perturbation Gram identities and row-sum 82", "robust non-polyconvex measure exact moments and budget", "E_|A|4 <=24|A|2|jet|2 by exact SOS identity", "norm-four Bregman lower bound |increment|4/3 by exact SOS identity"],
    "ldl_pivots":[str(z) for z in pivots],
    "primitive_coefficients":[str(S.expand(z)) for z in alpha],
    "exact_gram_margin":str(rho),
    "perturbation_operator_bound":str(K),
    "coefficient_supnorm_radius":str(eta),
    "robust_gram_margin":str(rho/2),
    "robust_nonpolyconvex_witness_upper_bound":str(witness_upper),
    "Fstar_jensen_gap_constant":str(rho/72),
    "coefficient_cube_jensen_gap_constant":str(rho/144),
    "proof_scope":"Exact Fstar-only algebra independently reconstructed. Analytic heat implication separately checked in REPORT.txt. Universal SO(2) Morrey and N740 Q4 remain unresolved. Historical novelty and external review UNKNOWN."
}
(HERE/"HEAT_INDEPENDENT_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"status":result["status"],"certificate_sha256":result["certificate_sha256"],"gamma":result["gamma"],"exact_checks":len(result["checks"])}))
