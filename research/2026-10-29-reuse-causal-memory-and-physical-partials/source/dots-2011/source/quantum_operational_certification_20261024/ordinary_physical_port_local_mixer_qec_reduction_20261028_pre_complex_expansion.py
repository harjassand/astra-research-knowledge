#!/usr/bin/env python3
"""Exact complete physical-input/local-marginal identities, no acquisition outcomes."""
import itertools,json,hashlib,math
from pathlib import Path
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);Ps=[I,X,Y,Z]
def kron(*xs):
 r=s.ones(1,1)
 for a in xs:r=s.kronecker_product(r,a)
 return r
def clean(A):return A.applyfunc(s.expand)
def mm(a,b):
 E=s.zeros(2);E[a,b]=1;return E
n=3;d=8
CN=s.zeros(4)
for a,b in itertools.product(range(2),repeat=2):CN[2*a+(b^a),2*a+b]=1
R=s.diag(s.Rational(3,5)-s.I*s.Rational(4,5),s.Rational(3,5)+s.I*s.Rational(4,5));V=kron(CN,R)
assert V.H*V==s.eye(d)
Ls=[s.diag(s.Rational(3,5),s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[s.Rational(4,5),0]])]
assert sum((L.H*L for L in Ls),s.zeros(2))==I
rates=[s.Rational(1,10),s.Rational(1,4)]
labels=list(itertools.product(range(4),repeat=3));PP=[kron(*[Ps[a] for a in lab]) for lab in labels]
weights=[]
for p in rates:weights.append([s.prod(1-p if a==0 else p/3 for a in lab) for lab in labels])
assert all(sum(ws)==1 for ws in weights)
def reduced(M,J):
 out=s.zeros((1<<len(J))*2);outside=[i for i in range(n) if i not in J]
 for x,y in itertools.product(range(d),repeat=2):
  bx=[x>>(n-1-i)&1 for i in range(n)];by=[y>>(n-1-i)&1 for i in range(n)]
  if any(bx[i]!=by[i] for i in outside):continue
  xx=sum(bx[i]<<(len(J)-1-j) for j,i in enumerate(J));yy=sum(by[i]<<(len(J)-1-j) for j,i in enumerate(J))
  for a,b in itertools.product(range(2),repeat=2):out[2*xx+a,2*yy+b]+=M[2*x+a,2*y+b]
 return clean(out)
local={(0,1):([0,1],kron(X,X)),(0,3):([0,1],kron(Z,I)),
       (1,1):([0,1],kron(I,X)),(1,3):([0,1],kron(Z,Z)),
       (2,1):([2],clean(R*X*R.H)),(2,3):([2],Z)}
full=0;loc=0
for a,b in itertools.product(range(2),repeat=2):
 om=mm(a,b);K=[L*om*L.H for L in Ls];T=sum(K,s.zeros(2))
 FF=[sum((weights[u][f]*K[u] for u in range(2)),s.zeros(2)) for f in range(64)]
 flat=sum((kron(P*(s.eye(d)/d)*P.H,F) for P,F in zip(PP,FF)),s.zeros(16))
 flat=clean(kron(V,I)*flat*kron(V.H,I));assert flat==kron(s.eye(d)/d,T);full+=256
 for i,j in itertools.product(range(n),[1,3]):
  sigma=kron(*[Ps[j] if q==i else I for q in range(n)])
  chars=[]
  for P in PP:
   if P*sigma*P.H==sigma:chars.append(1)
   else:assert P*sigma*P.H==-sigma;chars.append(-1)
  H=sum((chi*F for chi,F in zip(chars,FF)),s.zeros(2))
  # Independent branchwise CP order proof; the bias equals 1-4p/3.
  assert H==sum(((1-4*p/3)*K[u] for u,p in enumerate(rates)),s.zeros(2))
  actual=sum((kron(P*(sigma/d)*P.H,F) for P,F in zip(PP,FF)),s.zeros(16))
  actual=clean(kron(V,I)*actual*kron(V.H,I));target=clean(kron(V*sigma*V.H/d,H))
  assert actual==target;full+=256
  J,B=local[i,j];assert reduced(actual,J)==kron(B/(1<<len(J)),H);loc+=((1<<len(J))*2)**2
  assert reduced(flat,J)==kron(s.eye(1<<len(J))/(1<<len(J)),T);loc+=((1<<len(J))*2)**2
# Native CP-tail premise's scalar iid domination, not a claimed decoder execution.
tails=[]
for n,t,pm in [(3,1,s.Rational(1,10)),(5,1,s.Rational(1,20)),(7,2,s.Rational(1,8))]:
 site=[pm*s.Rational(i+1,n) for i in range(n)]
 bad=sum((s.prod(site[i] if bits[i] else 1-site[i] for i in range(n)) for bits in itertools.product([0,1],repeat=n) if sum(bits)>t),s.Integer(0))
 upper=sum((s.binomial(n,r)*pm**r*(1-pm)**(n-r) for r in range(t+1,n+1)),s.Integer(0))
 assert 0<=bad<=upper<=1;tails.append({'n':n,'t':t,'p_max':str(pm),'actual_independent_unequal_tail':str(bad),'binomial_upper':str(upper)})
out={'status':'PASS_FULL_PHYSICAL_INPUT_COMPLETE_MOMENTS_AND_AUTOMATIC_LOCAL_EXCITATION',
 'source_outcomes':0,'rng_draws':0,'physical_qubits':3,'memory_dimension':2,
 'nontrivial_mixer':'CNOT_01 tensor rational local complex Z rotation',
 'full_output_memory_entries':full,'local_output_memory_entries':loc,
 'physical_Pauli_patterns':64,'coherent_state_dependent_memory_instrument':True,
 'all_generators_support_width_at_most':2,'complete_CP_biases':[str(1-4*p/3) for p in rates],
 'scalar_tail_checks':tails,
 'scope':'complete port/localization identities and branchwise CP-tail arithmetic; received local learner/CP-domination and a supplied known code contract are imported, not newly simulated',
 'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
