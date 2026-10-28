#!/usr/bin/env python3
"""Exact unframed extraction on a reduced-Pauli but coherently flagged memory completion."""
from pathlib import Path
import itertools,json,hashlib
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
def kron(*xs):
 r=s.ones(1,1)
 for a in xs:r=s.kronecker_product(r,a)
 return r
def clean(M):return M.applyfunc(s.expand)
def mm(d,a,b):
 E=s.zeros(d);E[a,b]=1;return E
V=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
K0=kron(s.diag(s.Rational(4,5),s.Rational(12,13)),s.Matrix([1,0]));K1=kron(s.diag(s.Rational(3,5),s.Rational(5,13)),s.Matrix([0,1]))
A=kron(I,K0)+kron(Z,K1);assert A.H*A==s.eye(4)
N=kron(V,s.eye(4))*A
E0=K0.H*K0;E1=K1.H*K1;assert E0+E1==I and E0-E1==s.diag(s.Rational(7,25),s.Rational(119,169))
cal=0
for a,b in itertools.product(range(2),repeat=2):
 om=mm(2,a,b)
 for P in [I,X,Z]:
  out=N*kron(P/2,om)*N.H;red=s.zeros(2)
  for x,y in itertools.product(range(2),repeat=2):red[x,y]=sum(out[4*x+g,4*y+g] for g in range(4))
  effect=(E0-E1 if P==X else I)
  assert clean(red)==clean(V*P*V.H*s.trace(effect*om)/2);cal+=4
# The completion retains true alpha-beta memory coherences; it is not the CP-instrument sum.
inp=kron((I+X)/2,(I+X)/2);coh=A*inp*A.H
instrument=kron(I,K0)*inp*kron(I,K0).H+kron(Z,K1)*inp*kron(Z,K1).H
assert coh!=instrument and any(coh[2*x,2*y+1]!=0 for x,y in itertools.product(range(4),repeat=2))
Swap=s.zeros(4)
for a,b in itertools.product(range(2),repeat=2):Swap[2*b+a,2*a+b]=1
rows=[];channel_entries=0;complete_entries=0
for t in [s.Rational(1,10),s.Rational(1,100),s.Rational(1,1000)]:
 c=(1-t*t)/(1+t*t);u=2*t/(1+t*t);R=s.Matrix([[c,-u],[u,c]]);U=V*R
 BX=V*X*V.H;BZ=V*Z*V.H;SX=U*X*U.H;SZ=U*Z*U.H;delta=2*u
 assert clean((SX-BX)**2)==delta**2*I and clean((SZ-BZ)**2)==delta**2*I
 QZ=kron((I+SZ)/2,I)+kron((I-SZ)/2,X)
 CX=kron(I,s.diag(1,0))+kron(SX,s.diag(0,1))
 W=clean(QZ*CX*QZ);assert W.H*W==s.eye(4)
 assert W==clean(kron(U,I)*Swap*kron(U.H,I))
 phi={}
 for a,b in itertools.product(range(2),repeat=2):
  out=W*kron(mm(2,a,b),I/2)*W.H;decoded=s.zeros(2)
  for x,y in itertools.product(range(2),repeat=2):decoded[x,y]=sum(out[2*p+x,2*p+y] for p in range(2))
  assert clean(decoded)==clean(U.H*mm(2,a,b)*U);phi[a,b]=clean(decoded);channel_entries+=4
 for a,b in itertools.product(range(4),repeat=2):
  M=mm(4,a,b);out=N*M*N.H
  actual=sum((kron(phi[x,y],out[4*x:4*x+4,4*y:4*y+4]) for x,y in itertools.product(range(2),repeat=2)),s.zeros(8))
  desired=kron(R.H,s.eye(4))*A*M*A.H*kron(R,s.eye(4))
  assert clean(actual)==clean(desired);complete_entries+=64
 # Pure complete Choi outputs retain all memory coherences. Exact distance squared is u^2.
 overlap=s.trace(A.H*kron(R.H,s.eye(4))*A)/4
 assert overlap==c and 1-overlap**2==u**2
 assert u<=3*delta and s.sqrt(2-2*c)<=3*delta
 rows.append({'rational_fit_t':str(t),'each_generator_operator_error':str(delta),'actual_complete_Choi_distance':str(u),'declared_three_gate_operator_bound':str(3*delta)})
budgets=0
for n in [1,3,20]:
 for zeta in [s.Rational(1,10),s.Rational(1,100)]:
  delta=s.Rational(1,1)
  while delta>zeta/(3*n):delta/=2
  assert delta<=s.Rational(1,4) and delta>zeta/(6*n)
  for W in [1,3]:
   gamma=s.Rational(1,5*(2**W));a=s.Rational(1,16*(2**W))
   while a>delta*gamma/5:a/=2
   Nfine=8*3**W/a**2
   assert Nfine<800*3**W/(delta**2*gamma**2)<28800*n*n*3**W/(zeta**2*gamma**2);budgets+=1
out={'status':'PASS_UNFRAMED_LOCAL_INVERSE_ON_COHERENT_REDUCED_PAULI_COMPLETION',
 'source_outcomes':0,'rng_draws':0,'reduced_calibration_entries':cal,
 'actual_three_controlled_reflection_channel_entries':channel_entries,
 'complete_coherent_memory_matrix_entries':complete_entries,
 'coherent_flag_cross_terms_nonzero':True,'reduced_effect_X_bias':['7/25','119/169'],
 'fixtures':rows,'finite_rate_cases':budgets,
 'scope':'source-disabled exact physical circuit and complete memory tests; no sampled learning or generic compiler execution',
 'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
