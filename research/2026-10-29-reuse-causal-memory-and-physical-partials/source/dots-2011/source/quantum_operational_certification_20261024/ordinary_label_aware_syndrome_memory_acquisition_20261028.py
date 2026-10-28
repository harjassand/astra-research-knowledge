#!/usr/bin/env python3
"""Source-disabled exact coherent-memory/label-aware physical identities; no sampled data."""
from pathlib import Path
import itertools, json, hashlib
import sympy as s
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
def kron(*xs):
 r=s.ones(1,1)
 for a in xs:r=s.kronecker_product(r,a)
 return r
def clean(M):return M.applyfunc(s.expand)
def rot(P,t):return ((1-t*t)*s.eye(P.rows)-2*s.I*t*P)/(1+t*t)
ESET=[0,4,2,1]; enc=s.zeros(8,2);enc[0,0]=enc[7,1]=1
Um=s.zeros(8)
for l,g in itertools.product(range(2),range(4)):Um[7*l^ESET[g],4*l+g]=1
xs=[kron(*[X if f&(1<<(2-i)) else I for i in range(3)]) for f in range(8)]
zs=[kron(*[Z if i==j else I for i in range(3)]) for j in range(3)]
LX=kron(X,X,X); LZ=(zs[0]+zs[1]+zs[2]-zs[0]*zs[1]*zs[2])/2
assert LZ*LZ==s.eye(8) and LX*LZ==-LZ*LX
assert Um*kron(Z,s.eye(4))*Um.H==LZ
V=clean(rot(kron(X,Y,Z),s.Rational(1,5))*rot(kron(Z,I,X),s.Rational(1,7)))
assert clean(V.H*V)==s.eye(8)
U=clean(V*Um)
Cs=[clean(V*z*V.H) for z in zs]; CX=clean(V*LX*V.H); BZ=clean(V*LZ*V.H)
assert clean((Cs[0]+Cs[1]+Cs[2]-Cs[0]*Cs[1]*Cs[2])/2)==BZ
# Genuinely state-dependent quantum instrument, preserving/transferring off-diagonal memory.
Ls=[s.diag(s.Rational(3,5),s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[s.Rational(4,5),0]])]
assert sum((L.H*L for L in Ls),s.zeros(2))==I
cases=[
 ('iid_memory',[(s.Rational(0),)*3,(s.Rational(2,5),)*3]),
 ('iid_memory_endpoint',[(s.Rational(1,13),)*3,(s.Rational(1,2),)*3]),
 ('unequal_memory',[(s.Rational(1,4),s.Rational(1,4),s.Rational(1,100)),(s.Rational(49,100),s.Rational(49,100),s.Rational(0))])]
def weight(f,ps):
 r=s.Integer(1)
 for i,p in enumerate(ps):r*=p if f&(1<<(2-i)) else 1-p
 return r
def mm(a,b):
 E=s.zeros(2);E[a,b]=1;return E
entries=0;contrasts=0;records=[]
for name,pps in cases:
 ws=[[weight(f,ps) for f in range(8)] for ps in pps]
 assert all(sum(row)==1 for row in ws)
 for a,b in itertools.product(range(2),repeat=2):
  om=mm(a,b); K=[clean(L*om*L.H) for L in Ls];Tm=sum(K,s.zeros(2))
  F=[sum((ws[k][f]*K[k] for k in range(2)),s.zeros(2)) for f in range(8)]
  H=[sum(((-1 if f&(1<<(2-i)) else 1)*F[f] for f in range(8)),s.zeros(2)) for i in range(3)]
  AI=[sum((F[e^g] for e in ESET),s.zeros(2))/4 for g in ESET]
  AX=[sum((F[e^g^7] for e in ESET),s.zeros(2))/4 for g in ESET]
  assert all(AI[g]+AX[g]==Tm/4 for g in range(4))
  if name.startswith('iid'):
   ts=[1-2*ps[0] for ps in pps]
   hz=[sum((((3*t-t**3)/8 if g==0 else (t+t**3)/8)*K[k] for k,t in enumerate(ts)),s.zeros(2)) for g in range(4)]
   assert all(AI[g]-AX[g]==hz[g] for g in range(4))
  for la,lb in itertools.product(range(2),repeat=2):
   M=mm(la,lb); code=enc*M*enc.H;physical=s.zeros(16)
   for e,f in itertools.product(ESET,range(8)):physical+=kron(xs[e^f]*code*xs[e^f].H,F[f])/4
   model=s.zeros(16)
   for g in range(4):
    P=s.zeros(4);P[g,g]=1
    model+=kron(M,P,AI[g])+kron(X*M*X,P,AX[g])
   model=kron(Um,I)*model*kron(Um.H,I)
   assert clean(physical)==clean(model);entries+=256
  # Complete output/memory moments from actual sign+injection preparation labels.
  calc=[s.zeros(16) for _ in range(5)] # unsigned, X, three coordinates
  for axis,P in [('X',X),('Z',Z)]:
   for sign,e in itertools.product([-1,1],ESET):
    code=xs[e]*enc*((I+sign*P)/2)*enc.H*xs[e].H
    out=sum((kron(xs[f]*code*xs[f].H,F[f]) for f in range(8)),s.zeros(16))
    calc[0]+=out/16
    if axis=='X':calc[1]+=sign*out/8
    else:
     for i in range(3):calc[2+i]+=(sign*(-1 if e&(1<<(2-i)) else 1))*out/8
  targets=[kron(s.eye(8)/8,Tm),kron(LX/8,Tm)]+[kron(zs[i]/8,H[i]) for i in range(3)]
  for got,want in zip(calc,targets):assert clean(got)==clean(want);contrasts+=256
  # Verify a nontrivial retained-memory matrix unit also after the actual entangling V.
  if a==0 and b==1:
   for got,want in zip(calc,targets):
    assert clean(kron(V,I)*got*kron(V.H,I))==clean(kron(V,I)*want*kron(V.H,I))
 # CP inequalities via nonnegative scalar Kraus weights, including coherent inputs.
 for i in range(3):
  for k,ps in enumerate(pps):
   assert sum(((-1 if f&(1<<(2-i)) else 1)*ws[k][f] for f in range(8)))==1-2*ps[i]>=0
 records.append({'name':name,'instrument_rate_triples':[[str(p) for p in ps] for ps in pps],
                 'coordinate_biases':[[str(1-2*p) for p in ps] for ps in pps]})
# Exact class-extension/comparator boundary.
ps=(s.Rational(1,4),s.Rational(1,4),s.Rational(1,100));ws=[weight(f,ps) for f in range(8)]
assert ws[1]-ws[6]==-s.Rational(9,160)
majority=sum(ws[g^7] for g in ESET);optimal=sum(min(ws[g],ws[g^7]) for g in ESET)
assert majority==s.Rational(53,800) and optimal==s.Rational(1,100)
psneg=(s.Rational(49,100),s.Rational(49,100),s.Rational(0));wn=[weight(f,psneg) for f in range(8)]
injected_hz=[sum(wn[e^g]-wn[e^g^7] for e in ESET)/4 for g in ESET]
assert injected_hz[3]==-s.Rational(2399,20000)
assert all(1-2*p>0 for p in psneg)
# Symbolic iid vs coordinate information comparison, no sampling or numerical fit.
t=s.symbols('t',real=True);cal=t*(1+t*t)/16;label=t/8
assert s.expand(label-cal-t*(1-t)*(1+t)/16)==0
assert s.expand(2*cal-label-t**3/8)==0
# All-generation stage budget and assembly bound arithmetic over nontrivial exact grid.
guards=0
for b in [s.Rational(1,4),s.Rational(1,8),s.Rational(1,32)]:
 c=b/8;e=3*c+b/8;assert e==b/2 and 2*e/(2-e)<b
 for gamma in [s.Rational(1,8),s.Rational(1,32),s.Rational(1,1000)]:
  a=c*gamma/5;ee=5*a/4;h=gamma-ee
  assert h>ee and 2*ee<=c*(2*h-ee);guards+=1
out={'status':'PASS exact full-memory injected channel, label-aware moments and broader-class boundary',
 'source_outcomes':0,'rng_draws':0,'full_operator_channel_entries':entries,
 'full_output_memory_moment_entries':contrasts,'retained_memory_matrix_units':4,
 'coherent_state_dependent_memory_instrument':True,'matrix_moment_records_per_block':4,
 'fixtures':records,'negative_native_majority_sector':'-9/160',
 'majority_loss':'53/800','full_CPTP_optimal_syndrome_loss':'1/100',
 'positive_coordinate_but_negative_injected_majority':{'p':[str(p) for p in psneg], 'signed_blocks':[str(h) for h in injected_hz]},
 'rational_guard_cases':guards,
 'scope':'exact mathematical identities, not acquired data or an executed finite-rational decoder compiler',
 'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
