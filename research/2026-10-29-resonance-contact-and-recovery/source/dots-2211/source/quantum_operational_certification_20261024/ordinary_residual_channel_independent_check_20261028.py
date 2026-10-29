#!/usr/bin/env python3
"""Exact residual normalization, local Choi repair, bad-record guard and finite scores.
No source outcomes or hardware execution.
"""
from pathlib import Path
import itertools,json,hashlib
import sympy as s
import numpy as np
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z]
def k(a,b):return s.kronecker_product(a,b)
def clean(A):return A.applyfunc(s.simplify)
def psd(A):
 return all(A.extract(S,S).det()>=0 for m in range(1,A.rows+1) for S in itertools.combinations(range(A.rows),m))
def choi(T,t):return clean((k(I,I)+sum((t[a]*k(P[a],I) for a in range(3)),s.zeros(4))+sum((T[a,b]*k(P[a],P[b].T) for a,b in itertools.product(range(3),repeat=2)),s.zeros(4))))/4
axis=s.Matrix([s.Rational(24,25),0,s.Rational(-7,25)]);gamma=s.Rational(9,25);T=s.Rational(4,5)*s.eye(3)-s.Rational(4,25)*axis*axis.T;t=gamma*axis
rho=(I+sum((t[j]*P[j] for j in range(3)),s.zeros(2)))/2;spec=s.diag(s.Rational(7,8),s.Rational(1,8));R=k(I/2,spec);B=[k(p,I) for p in P];rhofull=k(rho,spec);c=s.trace(R*R);assert c==s.Rational(25,64)
D=[sum((T[a,j]*B[a] for a in range(3)),s.zeros(4))*R for j in range(3)]
G=s.Matrix(3,3,lambda a,b:s.trace(D[a]*D[b]));assert G==c*T*T
W=s.Rational(8,5)*T.inv();F=[sum((D[a]*W[a,j] for a in range(3)),s.zeros(4)) for j in range(3)]
for j in range(3):
 assert F[j]==s.Rational(8,5)*B[j]*R
 assert sum(abs(v)*m for v,m in F[j].eigenvals().items())==s.Rational(8,5)
 assert s.trace(B[j]*rhofull)==t[j]
J=choi(T,t);assert psd(J);assert s.trace(J)==1
phi=s.Matrix([1,0,0,1])/s.sqrt(2);Phi=phi*phi.H
rows=[]
for a0 in [s.Rational(1,10000),s.Rational(1,100000)]:
 # Exact contrast/Gram data, deliberately imprecise normalization and unsigned mean.
 E=a0;vl=a0;el=4*E+vl;u=a0/10;g=a0;h=s.Rational(1,8);q=s.Rational(1);lhat=s.Rational(8,5)+a0
 H0=G*W;Shat=lhat*H0
 # Rational outward upper bound for Eq (4), d=4, q=1 and sqrt(h)+sqrt(h-g)>=h.
 DS=el+2*g/h+(2+el)*u
 assert np.linalg.norm(np.array(Shat-T,dtype=float),2)<=float(DS)
 rhohat=rhofull+a0*k(Y,I)/4
 that=s.Matrix([s.re(s.trace(B[j]*rhohat)) for j in range(3)]);delta=a0;tau=4*a0+delta
 assert all(abs(that[j]-t[j])<=tau for j in range(3))
 # sqrt(3)<=2 supplies a rational coefficient-l1 bound.
 e=3*tau+6*DS;Jh=choi(Shat,that);Jp=(Jh+e*s.eye(4)/4)/(1+e)
 assert psd(Jp);assert s.trace(Jp)==1
 partial=s.Matrix(2,2,lambda a,b:sum(Jp[2*x+a,2*x+b] for x in range(2)));assert partial==I/2
 diff=Jh-J
 assert np.linalg.norm(np.array(diff,dtype=complex),2)<=float(e/4)
 trnorm=sum(abs(x) for x in np.linalg.eigvalsh(np.array(Jp-J,dtype=complex)))
 eta=5*e/(2*(1+e));assert trnorm<=float(eta)
 losses=[];estimated=[]
 for U in [I,X,Y,Z]:
  actual=1-s.trace(Phi*k(U,I)*J*k(U,I).H)
  model=1-s.trace(Phi*k(U,I)*Jp*k(U,I).H)
  assert abs(actual-model)<=eta;losses.append(actual);estimated.append(model)
 chosen=min(range(4),key=lambda z:estimated[z]);regret=losses[chosen]-min(losses);assert regret<=2*eta
 rows.append({'unsigned_radius':str(a0),'normalization_l':'8/5','certified_local_half_diamond':str(eta),'measured_normalized_choi_trace_distance':float(trnorm),'selected_candidate':chosen,'actual_library_regret':str(regret),'all_15_principal_minors_nonnegative':True})
# A bad confidence record can defeat an ungarded theoretical-radius repair.
Jbad=choi(s.eye(3),s.Matrix([0,0,10]));ebad=s.Rational(1,100);Jbadp=(Jbad+ebad*s.eye(4)/4)/(1+ebad)
assert not psd(Jbadp)
out={'status':'PASS','scope':'Exact known-matrix residual and finite CPTP repair/library checks, not acquired samples or code discovery','source_outcomes':0,'rng_draws':0,'normalization_cases':3,'translation_cases':3,'repair_and_library_cases':rows,'bad_record_requires_explicit_psd_guard':True,'sha256':{Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
