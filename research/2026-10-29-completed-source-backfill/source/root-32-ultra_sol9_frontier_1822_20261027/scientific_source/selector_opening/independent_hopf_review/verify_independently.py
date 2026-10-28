#!/usr/bin/env python3
"""Independent symbolic acoustic derivation and direct Fraction witness.

Does not import or execute producer code. Only review outputs are written.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import time
import sympy as s

started=time.perf_counter()
OUT=Path(__file__).resolve().parent
a,b,c,d,t=s.symbols('a b c d t',real=True)
A=s.Matrix([a,b,c,d])
u,v,w,q=a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
beta,r=s.Rational(99,100),s.Rational(88,25)
F=s.expand((u+v)**2+s.Rational(252,25)*q*q+s.Rational(99,25)*q*(u-v))
h=s.Matrix([u-v,2*w,2*q])
K=s.Matrix([[1,0,beta],[0,1,0],[beta,0,r]])
assert s.expand(F-(h.T*K*h)[0])==0
assert r-beta*beta==s.Rational(25399,10000)>0
H=s.hessian(F,A)
R=s.Matrix(s.symbols('R0:4',real=True))
HR=H.subs(dict(zip(A,R)),simultaneous=True)
assert s.expand((A.T*HR*A)[0]-(R.T*H*R)[0])==0

# Normalize rank-one R by a left row rotation: R=e1 tensor (co,si).
# Rotate coordinates of the arbitrary perturbation, keeping the literal
# energy's anisotropy. Equality is checked modulo co^2+si^2=1.
co,si=s.symbols('co si',real=True)
Runit=s.Matrix([co,si,0,0])
Arot=s.Matrix([a*co-b*si,a*si+b*co,c*co-d*si,c*si+d*co])
literal_Q=s.expand((Arot.T*H.subs(dict(zip(A,Runit)),simultaneous=True)*Arot)[0]/2)
cos2,sin2=co*co-si*si,2*co*si
claimed_Q=(6*a*a+2*b*b+2*c*c+(4*r-2)*d*d
           +12*beta*cos2*a*d-4*beta*cos2*b*c-8*beta*sin2*b*d)
remainder=s.div(s.expand(literal_Q-claimed_Q),co*co+si*si-1,co)[1]
assert s.expand(remainder)==0

C,S,z=s.symbols('C S z',real=True)
M=s.Matrix([[6,0,0,6*beta*C],[0,2,-2*beta*C,-4*beta*S],
            [0,-2*beta*C,2,0],[6*beta*C,-4*beta*S,0,4*r-2]])
# Permute a,c,b,d to obtain a leading diagonal block diag(6,2).
Mp=M.extract([0,2,1,3],[0,2,1,3])
D=Mp[:2,:2]
cross=Mp[:2,2:]
schur=s.simplify(Mp[2:,2:]-cross.T*D.inv()*cross)
N=s.Matrix([[1-beta**2*C**2,-2*beta*S],
             [-2*beta*S,2*r-1-3*beta**2*C**2]])
assert schur==2*N
assert D.inv()*cross==s.Matrix([[0,beta*C],[-beta*C,0]])
detN=s.expand(N.det()).subs(S*S,1-C*C)
detN=s.Poly(s.expand(detN),C).as_expr().subs(C**4,z*z).subs(C*C,z)
expected=3*beta**4*z*z+2*beta**2*(1-r)*z+2*r-1-4*beta**2
assert s.expand(detN-expected)==0
vertex=s.factor(-expected.coeff(z,1)/(2*expected.coeff(z,2)))
minimum=s.factor(expected.subs(z,vertex))
assert vertex==s.Rational(2800,3267)
assert minimum==s.Rational(7,2500)
assert 0<vertex<1
assert 1-beta**2==s.Rational(199,10000)>0
assert s.factor(2*r)==s.Rational(176,25)
N_margin=minimum/(2*r)
half_margin=2*N_margin/4
assert N_margin==s.Rational(7,17600)
assert half_margin==s.Rational(7,35200)

# Clifford identities give the claimed perturbation constant independently.
Hopf=[s.diag(1,-1,1,-1),
      s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]]),
      s.Matrix([[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]])]
for i in range(3):
    assert Hopf[i]*Hopf[i]==s.eye(4)
    for j in range(i):
        assert Hopf[i]*Hopf[j]+Hopf[j]*Hopf[i]==s.zeros(4)
BR=s.Matrix.hstack(*(Hi*R for Hi in Hopf))
normR2=(R.T*R)[0]
assert s.simplify(BR.T*BR)==normR2*s.eye(3)
e00,e01,e02,e11,e12,e22=s.symbols('e00 e01 e02 e11 e12 e22',real=True)
pert=s.Matrix([[e00,e01,e02],[e01,e11,e12],[e02,e12,e22]])
pertF=(h.T*pert*h)[0]
pert_H=s.hessian(pertF,A).subs(dict(zip(A,R)),simultaneous=True)
hA=s.Matrix([(A.T*Hi*A)[0] for Hi in Hopf])
hR=s.Matrix([(R.T*Hi*R)[0] for Hi in Hopf])
mixed=s.Matrix([(A.T*Hi*R)[0] for Hi in Hopf])
assert s.expand((A.T*pert_H*A)[0]/2-
                (2*(hA.T*pert*hR)[0]+4*(mixed.T*pert*mixed)[0]))==0
epsilon=s.Rational(1,1000000)
perturbed_half_margin=half_margin-18*epsilon
assert perturbed_half_margin==s.Rational(3979,22000000)>0

# Literal quartic cuts reconstructed by symbolic univariate substitution.
base=(36,0,0,35)
plus=(0,55,-4,0)
minus=(1,0,0,-2)
def symbolic_cut(direction):
    line=F.subs(dict(zip(A,[rr+t*aa for rr,aa in zip(direction,base)])),simultaneous=True)
    poly=s.Poly(line,t)
    coeff=[poly.nth(i) for i in range(5)]
    det=direction[0]*direction[3]-direction[1]*direction[2]
    value=coeff[2]-coeff[1]**2/(4*coeff[0])
    return coeff,s.factor(value/det)
plus_coeff,upper=symbolic_cut(plus)
minus_coeff,lower=symbolic_cut(minus)
assert upper==s.Rational(14923057,550)
assert lower==s.Rational(12087326489,445400)
assert lower-upper==s.Rational(25999623,4899400)>0

# Separately evaluate the finite witness directly using Fraction, without
# its cut reduction, symbolic Hessian, or source verifier.
def det4(B):return B[0]*B[3]-B[1]*B[2]
def literal_energy(B):
    aa,bb,cc,dd=B
    uu,vv=aa*aa+cc*cc,bb*bb+dd*dd
    qq=aa*dd-bb*cc
    return (uu+vv)**2+Q(252,25)*qq*qq+Q(99,25)*qq*(uu-vv)
def hopf(B):
    aa,bb,cc,dd=B
    return (aa*aa+cc*cc-bb*bb-dd*dd,2*(aa*bb+cc*dd),2*det4(B))
weights=(Q(5749,11542),Q(1,2),Q(11,5771))
increments=((Q(-264,28745),Q(-63481,114980),Q(5771,143725),Q(528,28745)),
            (Q(0),Q(11,20),Q(-1,25),Q(0)),
            (Q(12,5),Q(0),Q(0),Q(-24,5)))
assert all(ww>0 for ww in weights) and sum(weights)==1
assert all(sum(ww*XX[i] for ww,XX in zip(weights,increments))==0 for i in range(4))
assert sum(ww*det4(XX) for ww,XX in zip(weights,increments))==0
points=[tuple(Q(aa)+xx for aa,xx in zip(base,XX)) for XX in increments]
assert all(sum(ww*BB[i] for ww,BB in zip(weights,points))==base[i] for i in range(4))
assert sum(ww*det4(BB) for ww,BB in zip(weights,points))==det4(base)
defect=sum(ww*literal_energy(BB) for ww,BB in zip(weights,points))-literal_energy(base)
assert defect==Q(-13534664264487807,296890944920312500)<0
ha=hopf(base)
moment=[[sum(ww*hopf(BB)[i]*hopf(BB)[j] for ww,BB in zip(weights,points))-ha[i]*ha[j]
         for j in range(3)] for i in range(3)]
moment_l1=sum(abs(value) for row in moment for value in row)
assert moment_l1==Q(236878462368814585323,59378188984062500)
perturbed_defect=defect+Q(1,1000000)*moment_l1
assert perturbed_defect==Q(-2470054390528746814677,59378188984062500000000)<0

# Aligned-family endpoint classification, reviewed algebraically.
B2,rr,ss=s.symbols('B2 rr ss',real=True)
bound=(1+3*B2*ss+4*B2*(1-ss)/(1-B2*ss))/2
assert s.factor(s.diff(bound,ss)-B2*(s.Rational(3,2)-2*(1-B2)/(1-B2*ss)**2))==0
endpoint=(3*ss**2+2*(1-rr)*ss+2*rr-5)
assert s.expand(endpoint-(ss-1)*(3*ss-(2*rr-5)))==0

result={
    'status':'INDEPENDENT_SUBSTANTIVE_REPLAY_PASS',
    'literal_Hopf_identity':'PASS',
    'quartic_Hessian_reciprocity':'PASS',
    'literal_rank_one_Hessian_rotation_identity':'PASS_MOD_UNIT_CIRCLE',
    'Schur_complement_identity':'PASS',
    'N_determinant_vertex':str(vertex),'N_determinant_minimum':str(minimum),
    'N11_lower':str(1-beta**2),'half_Hessian_ROC_lower':str(half_margin),
    'full_six_box_radius':str(epsilon),
    'perturbed_half_Hessian_ROC_lower':str(perturbed_half_margin),
    'Clifford_and_perturbation_Hessian_identities':'PASS',
    'upper_support_cut':str(upper),'lower_support_cut':str(lower),
    'support_cut_gap':str(lower-upper),
    'cut_plus_literal_coefficients':list(map(str,plus_coeff)),
    'cut_minus_literal_coefficients':list(map(str,minus_coeff)),
    'three_positive_weights_sum_one':'PASS',
    'matrix_barycenter':list(map(str,base)),
    'determinant_barycenter':str(det4(base)),
    'Jensen_defect_direct_Fraction':str(defect),
    'moment_entry_l1':str(moment_l1),
    'perturbed_Jensen_defect_upper':str(perturbed_defect),
    'aligned_family_classification_derivative_and_endpoint':'PASS',
    'QC':'UNKNOWN_NO_COMPATIBLE_GRADIENT_WITNESS',
    'runtime_seconds':time.perf_counter()-started}
(OUT/'REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
