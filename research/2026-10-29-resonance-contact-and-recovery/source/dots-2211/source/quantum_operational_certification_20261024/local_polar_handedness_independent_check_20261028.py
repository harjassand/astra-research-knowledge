#!/usr/bin/env python3
"""Anisotropic negative-det CPTP polar convention and imperfect Y commutator."""
from pathlib import Path
import json,itertools
import sympy as s
import numpy as np
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z]
def clean(A):return A.applyfunc(s.simplify)
def ad(U,A):return clean(U*A*U.H)
def k(*xs):
 r=s.ones(1,1)
 for A in xs:r=s.kronecker_product(r,A)
 return r
def bloch(U):return s.Matrix(3,3,lambda a,b:s.simplify(s.trace(P[a]*U*P[b]*U.H)/2))
Uin=(3*I-4*s.I*X)/5;Uout=(5*I-12*s.I*Y)/13
weights=[s.Rational(7,20),s.Rational(1,4),s.Rational(3,10),s.Rational(1,10)]
def E(A):return ad(Uout,sum((w*Q*ad(Uin,A)*Q for w,Q in zip(weights,[I,X,Y,Z])),s.zeros(2)))
T=s.Matrix(3,3,lambda a,b:s.trace(P[a]*E(P[b]))/2)
Oi=bloch(Uin);Oo=bloch(Uout);D0=s.diag(1,1,-1);D=s.diag(1,-1,1)
S=clean(Oi.T*s.diag(s.Rational(1,5),s.Rational(3,10),s.Rational(1,10))*Oi);O=clean(Oo*D0*Oi)
assert clean(T-O*S)==s.zeros(3) and O.det()==-1
Oeff=O*D;Ueff=clean(Uout*Uin.H*X)
assert bloch(Ueff)==Oeff and Oeff.det()==1
residual=D*S;assert residual!=residual.T
Eeff=lambda A:ad(Ueff.H,E(A))
assert s.Matrix(3,3,lambda a,b:s.trace(P[a]*Eeff(P[b]))/2)==residual
CNOT=s.zeros(4)
for a,b in itertools.product(range(2),repeat=2):CNOT[2*a+(a^b),2*a+b]=1
V=k(CNOT,I);Veff=V*k(Ueff,I,I);rho=(I+s.Rational(2,3)*Y)/2;rho3=(I+Z/2)/2
R=ad(V,k(I/2,rho,rho3));B=[ad(V,k(A,I,I)) for A in P]
C=[ad(V,k(E(A)/2,rho,rho3)) for A in P]
for j in range(3):assert C[j]==clean(sum((T[a,j]*B[a]*R for a in range(3)),s.zeros(8)))
def ptr(A):return s.Matrix(4,4,lambda i,j:sum(A[2*i+b,2*j+b] for b in range(2)))
RJ=ptr(R);CJ=list(map(ptr,C));BJ=[s.Matrix(4,4,lambda i,j:A[2*i,2*j]) for A in B]
g=s.trace(RJ*RJ);G=s.Matrix(3,3,lambda i,j:s.trace(CJ[i]*CJ[j]));assert clean(G-g*S*S)==s.zeros(3)
F=[clean(sum((CJ[k]*(S.inv()/s.sqrt(g))[k,j] for k in range(3)),s.zeros(4))) for j in range(3)]
A=[clean(sum((O[a,j]*BJ[a] for a in range(3)),s.zeros(4))) for j in range(3)]
for j in range(3):assert clean(F[j]-A[j]*RJ/s.sqrt(g))==s.zeros(4) and clean(A[j]*A[j])==s.eye(4)
assert clean(A[0]*A[2]+A[2]*A[0])==s.zeros(4)
Yeff=clean(s.I*A[0]*A[2]);assert Yeff==-A[1]
assert k(Yeff,I)==ad(Veff,k(Y,I,I))
assert clean(k(A[0],I)-ad(Veff,k(X,I,I)))==s.zeros(8)
assert clean(k(A[2],I)-ad(Veff,k(Z,I,I)))==s.zeros(8)
# scalar normalization identity with trace-one local factor.
assert s.trace(RJ)==1
assert clean((1/s.sqrt(g))*(s.sqrt(g)*S))==S
# Imperfect X,Z remain reflections, but iSX SZ need not be Hermitian.
rng=np.random.default_rng(202610282023);An=[np.array(a,dtype=complex) for a in A];maxratio=0;nonherm=0
for case in range(64):
 fits=[]
 for a in [An[0],An[2]]:
  H=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));H=(H+H.conj().T)/2
  vals,vec=np.linalg.eigh(H);Q=(vec*np.exp(1j*.04*vals))@vec.conj().T;fits.append(Q@a@Q.conj().T)
 sx,sz=fits;candidate=1j*(sx@sz-sz@sx)/2;true=np.array(Yeff,dtype=complex)
 assert np.linalg.norm(candidate-candidate.conj().T)<1e-12
 ex=np.linalg.norm(sx-An[0],2);ez=np.linalg.norm(sz-An[2],2);err=np.linalg.norm(candidate-true,2)
 assert err<=ex+ez+1e-12 and np.linalg.norm(candidate,2)<=1+1e-12
 maxratio=max(maxratio,err/(ex+ez));nonherm+=int(np.linalg.norm(1j*sx@sz-(1j*sx@sz).conj().T)>1e-10)
out={'status':'PASS_NEGATIVE_DETERMINANT_PHYSICAL_HANDEDNESS_AND_COMMUTATOR','source_draws':0,'symbolic_channel':'Anisotropic CPTP Pauli mixture plus input/output rotations','det_T':str(s.factor(T.det())),'det_O':-1,'det_O_eff':1,'residual_DS_is_symmetric':False,'residual_DS':str(residual),'local_gram_factor':str(g),'physical_Y_equals_negative_uncorrected_Y':True,'partial_trace_envelope_qubits':2,'numeric_imperfect_reflection_cases':64,'nonhermitian_raw_iXZ_cases':nonherm,'max_commutator_error_over_sum_errors':maxratio,'scope':'Exact algebraic source/target checks plus floating perturbation stress, not finite acquired observations or hardware.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
