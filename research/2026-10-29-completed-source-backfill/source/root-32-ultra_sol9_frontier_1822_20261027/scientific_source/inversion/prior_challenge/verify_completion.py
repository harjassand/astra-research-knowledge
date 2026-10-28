"""Independent literal rational replay and symbolic completion identities.

Does not import any Hopf producer program. The accepted continuum ROC theorem
is an explicitly imported mathematical premise, not re-proved by this file.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)

def add(A,B):return [[A[i][j]+B[i][j] for j in range(2)] for i in range(2)]
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def literal_F(A):
    a,b=A[0];c,d=A[1]
    u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
    return (u+v)**2+Q(252,25)*q*q+Q(99,25)*q*(u-v)
co=Q(25399,10000)
def flat_W(A):return literal_F(A)-8*co*det(A)+4*co

A=[[Q(36),Q(0)],[Q(0),Q(35)]]
X=[[[Q(-264,28745),Q(-63481,114980)],[Q(5771,143725),Q(528,28745)]],
   [[Q(0),Q(11,20)],[Q(-1,25),Q(0)]],
   [[Q(12,5),Q(0)],[Q(0),Q(-24,5)]]]
weights=[Q(5749,11542),Q(1,2),Q(11,5771)]
B=[add(A,x) for x in X]
assert sum(weights)==1 and min(weights)>0
assert all(sum(weights[k]*B[k][i][j] for k in range(3))==A[i][j] for i in range(2) for j in range(2))
determinants=[det(A)]+[det(b) for b in B]
assert min(determinants)>Q(1,2)
assert sum(weights[k]*det(B[k]) for k in range(3))==det(A)
gapF=sum(weights[k]*literal_F(B[k]) for k in range(3))-literal_F(A)
gapW=sum(weights[k]*flat_W(B[k]) for k in range(3))-flat_W(A)
expected=-Q(13534664264487807,296890944920312500)
assert gapF==gapW==expected and gapW<0

a,b,c,d,beta,r=s.symbols('a b c d beta r',real=True)
q=a*d-b*c;x=a*a+c*c-b*b-d*d;y=2*(a*b+c*d)
F=x*x+y*y+4*beta*q*x+4*r*q*q
flat=F-8*(r-beta*beta)*q+4*(r-beta*beta)
squares=(x+2*beta*q)**2+y*y+4*(r-beta*beta)*(q-1)**2
assert s.expand(flat-squares)==0
bb=s.Rational(99,100);rr=s.Rational(88,25)
ss=s.sqrt(s.sqrt(1+bb**2)-bb)
A0=s.diag(ss,1/ss)
xx=s.simplify(x.subs({a:ss,b:0,c:0,d:1/ss}))
assert s.simplify(xx+2*bb)==0
assert s.simplify(A0.det()-1)==0
gradient=[]
for v in [a,b,c,d]:
    z=s.simplify(s.diff(flat,v).subs({beta:bb,r:rr,a:ss,b:0,c:0,d:1/ss}))
    assert z==0;gradient.append(str(z))
def SF(M):return s.expand(F.subs({beta:bb,r:rr,a:M[0,0],b:M[0,1],c:M[1,0],d:M[1,1]},simultaneous=True))
rotation=s.Matrix([[0,-1],[1,0]])
D=s.diag(2,1)
anisotropy=s.simplify(SF(D*A0)-SF(D*rotation*A0))
assert s.simplify(anisotropy+12*bb*s.sqrt(1+bb**2))==0

# Physical scale for every member of the accepted m>=197 family.
t=s.symbols('t',nonnegative=True)
m=197+t;bm=(m*m-1)/(m*m+1)
tstar=s.factor((18*bm-14)/(24*bm+73))
positive_numerator=s.Poly(s.fraction(tstar)[0],t)
assert min(positive_numerator.all_coeffs())>0
uppergap=s.factor(s.Rational(4,97)-tstar)
assert min(s.Poly(s.fraction(uppergap)[0],t).all_coeffs())>0
q_at_tstar=s.factor((1+tstar)*(1-2*tstar))
q_lower=s.Rational(8989,9409)
qgap=s.factor(q_at_tstar-q_lower)
assert min(s.Poly(s.fraction(qgap)[0],t).all_coeffs())>0

# The actual affine support plane is GL2-equivalent to the diagonal plane.
# Mueller's established theorem, not this finite algebra alone, excludes a
# bounded homogeneous gradient Young measure with these atoms and weights.
X1=s.Matrix([[0,s.Rational(11,20)],[-s.Rational(1,25),0]])
X2=s.diag(s.Rational(12,5),-s.Rational(24,5))
ps,pt=s.symbols('plane_s plane_t',real=True)
plane_det=s.factor((ps*X1+pt*X2).det())
assert s.expand(plane_det-(s.Rational(11,500)*ps**2-s.Rational(288,25)*pt**2))==0
alpha=s.sqrt(s.Rational(11,5760))
Rp=X1+alpha*X2;Rm=X1-alpha*X2
assert s.simplify(Rp.det())==0 and s.simplify(Rm.det())==0
pd=s.Rational(12,5);pb=s.Rational(11,20);pc=-s.Rational(1,25)
PU=s.Matrix([[alpha*pd,-alpha*pd],[pc,pc]])
PV=s.Matrix([[1,pb/(alpha*pd)],[1,-pb/(alpha*pd)]])
assert s.simplify(PU.det())!=0 and s.simplify(PV.det())!=0
diag_transform=lambda Z:s.simplify(PU.inv()*Z*PV.inv())
assert diag_transform(Rp)==s.diag(1,0)
assert diag_transform(Rm)==s.diag(0,1)
assert diag_transform(X1)==s.diag(s.Rational(1,2),s.Rational(1,2))
assert diag_transform(X2)==s.diag(1/(2*alpha),-1/(2*alpha))
all_transformed=[]
for xi in X:
    Zi=diag_transform(s.Matrix(xi))
    assert Zi[0,1]==Zi[1,0]==0
    all_transformed.append(str(Zi))

result={'status':'EXACT_DERIVED_EXTENSION; physical completion independently ACCEPTED; later Mueller application not independently reviewed',
        'independent_physical_review':'../../hopf/physical_review/REVIEW.md and its independently reconstructed replay',
        'imported_premise':'accepted strict ROC of the literal Hopf energy and accepted aligned-family support gaps; not inferred from finite checks',
        'determinants_A_B0_B1_B2':[str(v) for v in determinants],
        'weights':[str(v) for v in weights],
        'matrix_mean_exact':True,'determinant_mean_exact':True,'all_witness_determinants_above_delta':True,
        'delta_exact':'1/2','quartic_Jensen_gap_exact':str(gapF),'completed_Jensen_gap_exact':str(gapW),
        'barrier_at_all_witness_points':'exactly zero by q>=delta, not numerically quadrature-estimated',
        'SOS_completion_identity_exact':True,'main_c_exact':str(co),
        'natural_well_A0':'diag(s,1/s), s^2=sqrt(1+(99/100)^2)-99/100',
        'natural_well_det_exact':'1','gradient_at_natural_well_exact':gradient,
        'normalized_energy':'V(A)=W(A A0); zero set SO(2); non-PC witness base A A0^-1 is not I',
        'normalized_material_anisotropy_difference_exact':str(anisotropy),
        'family_tstar_in_m197_plus_t':str(tstar),
        'family_tstar_lower_sign_numerator_coefficients':[str(v) for v in positive_numerator.all_coeffs()],
        'family_tstar_below_4over97_exact':True,
        'family_det_at_tstar_exact':str(q_at_tstar),
        'family_det_above_8989over9409_exact':True,
        'actual_support_plane_determinant_exact':str(plane_det),
        'actual_support_plane_diagonalization_exact':True,
        'actual_support_plane_alpha_exact':str(alpha),
        'actual_support_plane_U_exact':str(PU),
        'actual_support_plane_V_exact':str(PV),
        'actual_transformed_increments_exact':all_transformed,
        'actual_measure_not_bounded_homogeneous_gradient_YM':'Mueller 1999 Theorem 2 plus exact diagonalization and accepted ROC Jensen gap; see JENSEN_COMPATIBILITY.md',
        'barrier_smoothness_convexity_divergence':'analytic proof in PHYSICAL_DOMAIN.md; no numerical positivity premise',
        'well_scope':'nonnegative energy is automatically PC-supported and quasiconvex at its zero well; no non-PC-at-stress-free-identity claim',
        'global_quasiconvexity':'UNKNOWN','historical_priority':'UNKNOWN','material_qualification':'NOT_PERFORMED'}
(OUT/'COMPLETION_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
