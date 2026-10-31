"""Independent exact-arithmetic and parser checks, not model-truth tests."""
import copy,json,random
from fractions import Fraction as F
from pathlib import Path
from calibrate_affine_innovations import *
P=Path(__file__).parent
count=0
for den in range(2,150):
 for num in range(1,den):
  d=F(num,den); j=dyadic_confidence_exponent(d)
  assert F(1,1<<j)<=d<F(1,1<<(j-1)); count+=1
for j in [1,2,17,100,1000]:
 for d in [F(1,1<<j),F(2,1+(1<<j)),F(1,(1<<j)+1)]:
  z=dyadic_confidence_exponent(d); assert F(1,1<<z)<=d<F(1,1<<(z-1)); count+=1
base=dict(F=[[1]],G=[[1]],beta=0,transitions=[(0,i%2) for i in range(128)],N=128,radius='1/4',delta='1/4',b=0,T=1,p_slots=0,epsilon_model=18)
def reject(**kw):
 a=copy.deepcopy(base);a.update(kw)
 try: calibrate(**a)
 except ValueError:return
 raise AssertionError(kw)
mal=[dict(F=v) for v in [None,{},[],[[]],[[1],[0,1]],[[1.0]],[[True]],[[0]]]]
mal += [dict(G=v) for v in [None,[],[[]],[[0]],[[1,1]],[[True]],[[1],[0]]]]
mal += [dict(beta=v) for v in [True,-1,2,'0']]
for key in ['radius','delta','b','T','epsilon_model']:
 for value in [True,.25,None,{},'nan','1/0']:
  mal.append({key:value})
mal += [dict(N=v) for v in [False,0,-1,'128']]
mal += [dict(p_slots=v) for v in [True,-1,'0']]
mal += [dict(transitions=v) for v in [None,{},[],[(0,True)]*128,[(0,2)]*128,[(0,0,0)]*128]]
for x in mal:reject(**x)
# Dense histogram formula independent of sparse implementation, all outcomes.
rng=random.Random(517); hist=0
for n in range(1,6):
 I=[[int(i==j) for j in range(n)] for i in range(n)]
 D=1<<n; N=2*(D+2); radius=F(1)
 for rep in range(12):
  beta=rng.randrange(D); pairs=[]; vals=[]
  for _ in range(N):
   x=rng.randrange(D); r=rng.randrange(D);pairs.append((x,x^r^beta));vals.append(r)
  a=calibrate(I,I,beta,pairs,N=N,radius=radius,delta='1/4',b=0,T=0,p_slots=0,epsilon_model=100)
  exact=sum(abs(F(vals.count(v),N)-F(1,D)) for v in range(D))
  assert F(a['eta_hat'])==exact and a['m']==1; hist+=1
# Exhaustively test all residuals for every injective small G: off-image rejected.
valid=invalid=0
for n in range(1,4):
 for k in range(1,n+1):
  for bits in range(1<<(n*k)):
   G=[[(bits>>(i*k+j))&1 for j in range(k)] for i in range(n)]
   if rank(G)!=k:continue
   image={matvec(G,r):r for r in range(1<<k)}
   for v in range(1<<n):
    if v in image:assert recover(G,v)==image[v];valid+=1
    else:
     try:recover(G,v)
     except ValueError:invalid+=1;continue
     raise AssertionError('off image accepted')
before=copy.deepcopy(base); calibrate(**base); assert before==base
# Known illustrative cost ledger is sufficient and minimal for its conservative guard.
rows=json.loads((P/'calibration_sample_cost_examples.json').read_text())['rows']
for row in rows:
 r=F(row['radius']);N=row['sufficient_samples'];rhs=2*((1<<row['k'])+10)
 assert N*r*r>=rhs and (N-1)*r*r<rhs
result=dict(passed=True,dyadic_boundaries=count,malformed_rejected=len(mal),dense_histograms=hist,valid_recoveries=valid,off_image_rejected=invalid,cost_rows_verified=len(rows),input_mutated=False)
(P/'calibration_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
