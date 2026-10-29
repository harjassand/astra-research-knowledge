#!/usr/bin/env python3
"""Exact revealing-pointer transitions and complete quantum-reference burn-in."""
from pathlib import Path
import sympy as s
import itertools,json,math
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
A=(I+Z)/4;B=(I+X)/4;assert s.trace(A+B)==1 and A*B!=B*A
CQ=s.diag(1,0).kronecker_product(A) if False else s.kronecker_product(s.diag(1,0),A)+s.kronecker_product(s.diag(0,1),B)
ideal=s.kronecker_product(I/2,A+B);X4=s.kronecker_product(X,I)
def norm1(H):return s.simplify(sum(abs(x)*m for x,m in H.eigenvals().items()))
rows=[];paths=0
for q in [s.Rational(1,10),s.Rational(1,4),s.Rational(3,4),s.Rational(9,10)]:
 for N in range(1,7):
  # Every observed transition string has its iid physical flip probability,
  # for either initial pointer value (possibly recorded in a quantum reference).
  for ys in itertools.product([0,1],repeat=N):
   target=q**sum(ys)*(1-q)**(N-sum(ys))
   for start in [0,1]:
    x=start;actual=s.S.One
    for y in ys:
     nxt=x^y;actual*=q if nxt!=x else 1-q;x=nxt
    assert actual==target;paths+=1
 current=CQ
 for t in range(9):
  diff=s.simplify(current-ideal);formula=(1-2*q)**t*s.kronecker_product(Z/2,A-B)
  assert diff==formula
  error=norm1(diff)/2;assert error==abs(1-2*q)**t*norm1(A-B)/2 and error<=abs(1-2*q)**t/2
  rows.append({'q':str(q),'t':t,'complete_reference_error':str(error),'bound':str(abs(1-2*q)**t/2)})
  current=s.simplify((1-q)*current+q*X4*current*X4)
confidence=[];beta=.05
for N in [32,128]:
 rad=math.sqrt(math.log(2/beta)/(2*N))
 for q in [s.Rational(1,10),s.Rational(1,2),s.Rational(9,10)]:
  failure=s.S.Zero;accept=s.S.Zero
  for k in range(N+1):
   mass=s.binomial(N,k)*q**k*(1-q)**(N-k);lo=max(0,k/N-rad);hi=min(1,k/N+rad)
   if float(q)<lo or float(q)>hi:failure+=mass
   if lo>0 and hi<1:accept+=mass
  assert float(failure)<=beta
  confidence.append({'N':N,'q':str(q),'exact_binomial_failure_probability_evaluated':float(failure),'acceptance_probability':float(accept)})
out={'status':'PASS_REVEALING_POINTER_SINGLE_TRAJECTORY_AND_QUANTUM_REFERENCE_RESET','source_draws':0,'rng_draws':0,'exact_initial_pointer_transition_paths':paths,'noncommuting_reference_blocks':True,'reset_cases':rows,'confidence_checks':confidence,'scope':'Exact transition probabilities and finite matrix identities; numerical interval endpoints only in finite confidence illustration. General confidence is Hoeffding proof, not this enumeration.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['reset_cases','confidence_checks']},indent=2))
