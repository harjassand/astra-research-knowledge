"""Deterministic Wick-moment algebra checks; no Gaussian simulation is needed."""
from pathlib import Path
from itertools import permutations
import json
import numpy as np
import sympy as sy
rng=np.random.default_rng(715019);tol=2e-10
pauli=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1]).astype(complex)]

def cycles(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  c=[];j=i
  while j not in seen:seen.add(j);c.append(j);j=p[j]
  out.append(c)
 return out

def wick_np(mats):
 out=0
 for p in permutations(range(3)):
  val=1
  for c in cycles(p):
   prod=np.eye(len(mats[0]),dtype=complex)
   for j in c:prod=prod@mats[j]
   val*=np.trace(prod)
  out+=val
 return float(out.real)
def pt(a,d):return a.reshape(2,d,2,d).transpose(2,1,0,3).reshape(2*d,2*d)
def rb(a,d):return np.einsum('aiaj->ij',a.reshape(2,d,2,d))
cases=[]
for d in [2,3,4,5,8]:
 for rep in range(4):
  z=(rng.normal(size=(2*d,2*d))+1j*rng.normal(size=(2*d,2*d)))
  rho=z@z.conj().T
  rho+=(max(0,-np.linalg.eigvalsh(pt(rho,d))[0])+.1)*np.eye(2*d)
  rho/=np.trace(rho)
  l,u=np.linalg.eigh(rho);sqrt=(u*np.sqrt(l))@u.conj().T
  B=[sqrt@np.kron(s,np.eye(d))@sqrt for s in pauli]
  a=sum(float(np.trace(b).real)**2 for b in B)
  b=sum(float(np.trace(x@x).real) for x in B)
  c=sum(float(np.trace(rho@x@x).real) for x in B)
  cross=sum(float(np.trace(rho@x).real)*float(np.trace(x).real) for x in B)
  A=a+b;K=sum(wick_np([rho,x,x]) for x in B)
  predicted=A+2*cross+2*c
  purity_identity=2*float(np.trace(rb(rho,d)@rb(rho,d)).real)-float(np.trace(rho@rho).real)
  assert abs(b-purity_identity)<tol
  assert abs(K-predicted)<tol
  assert K<=4*A+tol and A>=1/d-tol
  assert A*A/(2*K)>=1/(8*d)-tol
  cases.append({'d':d,'A':A,'third_moment':K,'third_moment_upper':4*A,'certified_deficit_from_moments':A*A/(2*K),'uniform_deficit':1/(8*d),'wick_identity_error':abs(K-predicted)})
# Exact rational/radical examples, including singular rho.
S=[sy.Matrix([[0,1],[1,0]]),sy.Matrix([[0,-sy.I],[sy.I,0]]),sy.diag(1,-1)]
exact=[]
for weights in [[sy.Rational(1,10),sy.Rational(2,10),sy.Rational(3,10),sy.Rational(4,10)],[sy.Rational(1,2),0,0,sy.Rational(1,2)]]:
 H=sy.Matrix([[1,1],[1,-1]])/sy.sqrt(2);U=sy.kronecker_product(H,sy.eye(2))
 rho=U*sy.diag(*weights)*U.H
 sqrt=U*sy.diag(*[sy.sqrt(x) for x in weights])*U.H
 B=[sqrt*sy.kronecker_product(x,sy.eye(2))*sqrt for x in S]
 A=sum((sy.trace(x)**2+sy.trace(x*x) for x in B),sy.S(0))
 K=sy.S(0)
 for x in B:
  mats=[rho,x,x]
  for p in permutations(range(3)):
   val=sy.S(1)
   for c0 in cycles(p):
    prod=sy.eye(4)
    for j in c0:prod=prod*mats[j]
    val*=sy.trace(prod)
   K+=val
 predicted=A+2*sum((sy.trace(rho*x)*sy.trace(x)+sy.trace(rho*x*x) for x in B),sy.S(0))
 assert sy.simplify(K-predicted)==0
 assert sy.simplify(4*A-K)>=0
 assert sy.simplify(A-sy.Rational(1,2))>=0
 exact.append({'rank':int(rho.rank()),'A':str(sy.simplify(A)),'third_moment':str(sy.simplify(K)),'deficit_bound':str(sy.simplify(A*A/(2*K)))})
report={'status':'PASS','numerical_cases':cases,'exact_cases':exact,'absolute_tolerance':tol,'gaussian_simulations':0,'scope':'Wick third moment evaluated by all six permutations, plus exact rational/radical cases and deterministic PPT moment inequalities. No convex-roof optimization.'}
Path(__file__).with_name('gaussian_concurrence_gap_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','numerical_cases':len(cases),'exact_cases':exact,'gaussian_simulations':0,'max_wick_identity_error':max(c['wick_identity_error'] for c in cases)},indent=2))
