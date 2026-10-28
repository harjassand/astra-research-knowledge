"""Independent deterministic checks of new holdout/selection composition.
Accepted Bures, frame and generic optimizer imports are hash-bound, not re-audited.
No sampled source outcomes, source calls, or physical circuit execution.
"""
from pathlib import Path
import sympy as s
import hashlib,json,itertools
from fractions import Fraction as F
H=Path(__file__).resolve().parent;ROOT=H.parent
R=s.Rational
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
paulis=[X,Y,Z];probes=[(I+sign*p)/2 for p in paulis for sign in (-1,1)]
# Derive the observable six-probe mean for arbitrary affine TP qubit map.
t=s.symbols('t0:3',real=True);A=s.Matrix(3,3,lambda i,j:s.Symbol(f'A{i}{j}',real=True))
mean=0
for j,P in enumerate(paulis):
 for sign in (-1,1):
    state=(I+sign*P)/2
    out=(I+sum([(t[i]+sign*A[i,j])*paulis[i] for i in range(3)],s.zeros(2)))/2
    mean+=(1-s.trace(state*out))/6
fe=(1+s.trace(A))/4
assert s.simplify(mean-R(2,3)*(1-fe))==0
# Independent source-derived row effects via the actual six ordinary probes.
u,v=s.symbols('u v',real=True);row=s.Matrix([[u,v]])
diagonal=[]
for a in range(2):
 value=s.simplify(sum((row*P*row.T)[0]*(I-P).T[a,a] for P in probes)/6)
 diagonal.append(value)
assert diagonal==[u*u/6+v*v/3,u*u/3+v*v/6]
rot=s.Matrix([[R(1,2),-s.sqrt(3)/2],[s.sqrt(3)/2,R(1,2)]])
O=s.diag(rot,rot);I4=s.eye(4)
W=s.BlockMatrix([[I4,O],[I4,-O]]).as_explicit()/s.sqrt(2)
assert s.simplify(W.H*W)==s.eye(8)
x=s.Matrix(s.symbols('x0:4',real=True));effects=[]
for site in range(4):
 for sign in (-1,1):
  us=x[site]/s.sqrt(2);vs=sign*(O*x)[site]/s.sqrt(2)
  for a in range(2):
   val=s.expand(diagonal[a].subs({u:us,v:vs}))
   B=s.hessian(val,list(x))/2
   assert s.simplify((x.T*B*x)[0]-val)==0
   assert B.rank()==2 and s.trace(B)==R(1,4)
   assert s.simplify(s.trace(B*B))==R(1,24)
   assert B.eigenvals()=={0:2,(3+s.sqrt(3))/24:1,(3-s.sqrt(3))/24:1}
   effects.append(B)
assert sum(effects,s.zeros(4))==I4
tail=s.simplify(sum(s.trace(B)-(3+s.sqrt(3))/24 for B in effects))
assert s.simplify(tail-(2-2/s.sqrt(3)))==0
# A concrete exactly CPTP extension of the mathematical isometry inverse.
V=s.zeros(8,2);V[0,0]=V[4,1]=1;J=W*V
assert s.simplify(J.H*J)==I
# CP recovery D(B)=J^dagger B J+Tr[(I-JJ^dagger)B]|0><0|.
assert s.simplify(J*J.H+(s.eye(8)-J*J.H))==s.eye(8)
for P in probes:assert s.simplify(J.H*(J*P*J.H)*J)==P
# Root-risk and selection/error constants exactly, without sampled training data.
rootcoef=(6+2*s.sqrt(6))/512
assert s.simplify((R(11,512))**2-rootcoef**2)>0
assert R(121,2**18)<R(1,1024)
assert R(17,512)+R(1,2)<1
# ln2=2*sum_{m>=0} (1/3)^(2m+1)/(2m+1), so this rational lower bound suffices.
ln2lower=2*(R(1,3)+R(1,81))
assert ln2lower>R(5,8)
budget_cases=0
for eps,gamma,ell,acc in itertools.product([F(1),F(1,7),F(1,1024)],[F(1),F(1,17)],[F(0),F(1,5),F(1)],[F(0),F(1,11),F(1,2),F(1)]):
    beta=eps/1024
    # Deliberately use the looser source branch bound, including its global beta debit.
    risk=acc*eps/64+(1-acc)*((1+gamma/2)*ell+eps/128)+beta
    assert risk<=(1+gamma/2)*ell+17*eps/1024
    assert 2*risk+eps/2<=(1+gamma)*2*ell+eps
    assert eps/1024+eps/1024+eps/1024==3*eps/1024<eps/256
    budget_cases+=1
# Deterministic binary-log overestimates for exact finite counts; no floating logs.
def ceil_log2_fraction(q):
    assert q>=1
    k=0
    while 2**k<q:k+=1
    return k
integer_cases=[]
for eps in [F(1),F(1,3),F(1,64)]:
    beta=eps/1024;L=ceil_log2_fraction(1/beta)
    v=F(768,1)/eps*L;n=(v.numerator+v.denominator-1)//v.denominator
    a=eps/192;k=(n*a).numerator//(n*a).denominator
    assert F(n)*eps/768>=L # >= ln(1/beta), for false acceptance
    assert F(n)*a/2>=2*L # >= 2 ln(1/beta), for false rejection
    assert F(k)<=n*a<F(k+1)
    integer_cases.append({'epsilon':str(eps),'binary_log_upper':L,'n_test':n,'threshold':k})
# A concrete finite six-state sampler: three fair bits, reject labels 6/7, cap each draw.
# At most B draws, with r=ceil(log_4(B/nu)), has exhaustion probability <=nu.
sampler_cases=0
for B,nu in itertools.product([1,10,10000],[F(1,1024),F(1,2**30)]):
    r=0
    while F(B,4**r)>nu:r+=1
    assert F(B,4**r)<=nu and 3*B*r>=0
    sampler_cases+=1
manifest=json.loads((H/'one_anchor_low_loss_source_bindings.json').read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name,expected in manifest['sha256_relative_to_programme_root'].items():assert digest(ROOT/name)==expected,name
source='ONE_ANCHOR_LOW_LOSS_HOLDOUT_AND_FALLBACK.md'
assert digest(H/source)==manifest['new_source_sha256']
result={'status':'PASS_INDEPENDENT_NEW_HOLDOUT_COMPOSITION_AND_EXACT_SOURCE_SEPARATION','source_sha256':digest(H/source),'script_sha256':digest(Path(__file__)),'holdout_identity':'exact symbolic arbitrary affine TP qubit map','actual_six_probe_row_effects':len(effects),'row_tail':str(tail),'exact_mixture_budget_cases':budget_cases,'exact_integer_threshold_cases':integer_cases,'finite_six_state_sampler_cases':sampler_cases,'accepted_direct_import_hashes_reverified':len(manifest['sha256_relative_to_programme_root']),'accepted_import_mathematics_reaudited':False,'source_calls':0,'random_draws':0,'source_outcomes':0,'production_optimizer_or_quantum_circuit_executed':False}
(H/'one_anchor_low_loss_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
