#!/usr/bin/env python3
"""Exact rotated amplitude-damping polar/Gram example with genuine spectator factor."""
from pathlib import Path
import json,itertools
import sympy as s
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z]
def k(*xs):
 r=s.ones(1,1)
 for a in xs:r=s.kronecker_product(r,a)
 return r
def clean(a):return a.applyfunc(s.simplify)
def ad(U,A):return clean(U*A*U.H)
def ptlast(A):return s.Matrix(4,4,lambda i,j:sum(A[2*i+a,2*j+a] for a in range(2)))
def bloch(U):return clean(s.Matrix(3,3,lambda a,b:s.trace(P[a]*U*P[b]*U.H)/2))
Uin=(3*I-4*s.I*Y)/5; Uout=(5*I-12*s.I*X)/13
Oi=bloch(Uin);Oo=bloch(Uout)
K=[s.diag(1,s.Rational(3,5)),s.Matrix([[0,s.Rational(4,5)],[0,0]])]
def E(A):return clean(sum((ad(Uout,L*ad(Uin,A)*L.H) for L in K),s.zeros(2)))
T=s.Matrix(3,3,lambda a,b:s.trace(P[a]*E(P[b]))/2);t=s.Matrix([s.trace(A*E(I/2)) for A in P])
D=s.diag(s.Rational(3,5),s.Rational(3,5),s.Rational(9,25));S=clean(Oi.T*D*Oi);O=clean(Oo*Oi)
assert clean(T-O*S)==s.zeros(3) and clean(T.T*T-S*S)==s.zeros(3) and O.det()==1 and all(v>0 for v in S.eigenvals())
U=clean(Uout*Uin)
def Ep(A):return ad(U.H,E(A))
assert s.Matrix(3,3,lambda a,b:s.trace(P[a]*Ep(P[b]))/2)==S
assert s.Matrix([s.trace(A*Ep(I/2)) for A in P])==clean(O.T*t)
CNOT=s.zeros(4)
for a,b in itertools.product(range(2),repeat=2):CNOT[2*a+(a^b),2*a+b]=1
V=k(CNOT,I);Veff=V*k(U,I,I)
rho2=(I+s.Rational(3,5)*X)/2;rho3=(I+s.Rational(4,5)*Z)/2
R=ad(Veff,k(I/2,rho2,rho3));RJ=ptlast(R)
B=[ad(Veff,k(A,I,I)) for A in P];BJ=[s.Matrix(4,4,lambda a,b:Bi[2*a,2*b]) for Bi in B]
assert all(Bi==k(Bj,I) for Bi,Bj in zip(B,BJ))
contrasts=[]
for j in range(3):
 actual=ad(V,k(E(P[j])/2,rho2,rho3))
 expected=clean(sum((S[a,j]*B[a]*R for a in range(3)),s.zeros(8)))
 assert actual==expected
 local=ptlast(actual);assert local==clean(sum((S[a,j]*BJ[a]*RJ for a in range(3)),s.zeros(4)))
 contrasts.append(local)
g=s.trace(RJ*RJ);G=clean(s.Matrix(3,3,lambda a,b:s.trace(contrasts[a]*contrasts[b])))
assert G==g*S*S
Ginv=S.inv()/s.sqrt(g)
assert clean(Ginv*G*Ginv)==s.eye(3)
F=[clean(sum((contrasts[k]*Ginv[k,j] for k in range(3)),s.zeros(4))) for j in range(3)]
for j in range(3):
 assert F[j]==clean(BJ[j]*RJ/s.sqrt(g))
 assert clean(F[j]*F[j])==RJ*RJ/g
 assert clean(F[j]*(s.sqrt(g)*RJ.inv()))==BJ[j]
 assert F[j]*F[j]!=s.eye(4) # Whitening alone is NOT a reflection.
assert all(v>0 for v in RJ.eigenvals())
# Actual global canonical rewrite holds on a basis, not only on selected contrasts.
checks=0
for a,b in itertools.product(range(2),repeat=2):
 A=s.zeros(2);A[a,b]=1
 for C,Dm in itertools.product([I,X,Y,Z],repeat=2):
  assert ad(V,k(E(A),C,Dm))==ad(Veff,k(Ep(A),C,Dm));checks+=1
# Physical improper orientation: random X/Y/Z, each weight1/3, gives T=-I/3.
Tneg=s.Matrix(3,3,lambda a,b:sum(s.trace(P[a]*Q*P[b]*Q)/6 for Q in P))
assert Tneg==-s.eye(3)/3 and Tneg.det()<0
Ominus=-s.eye(3);assert Ominus.det()==-1
# Canonical inversion would require X,Y,Z -> -X,-Y,-Z, violating proper Pauli multiplication.
assert (-X)*(-Y)!=s.I*(-Z)
# Singular complete Z dephasing destroys X,Y directions.
Tsing=s.diag(0,0,1);assert Tsing.det()==0
out={'status':'PASS_EXACT_POLAR_GRAM_PARTIAL_TRACE_AND_BOUNDARIES','source_draws':0,'rng_draws':0,'physical_qubits':3,'local_envelope_qubits':2,'global_rewrite_basis_cases':checks,'gram_factor_g':str(g),'local_factor_eigenvalues':{str(a):int(b) for a,b in RJ.eigenvals().items()},'nonflat_factor':True,'whitening_is_reflection':False,'sign_after_whitening_is_canonical_generator':True,'positive_polar_matrix':str(S),'proper_rotation':str(O),'negative_determinant_CPTP_example':'equal mixture of X,Y,Z: T=-I/3','finite_acquisition_or_hardware_executed':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
