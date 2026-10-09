from pathlib import Path
import sys,random,json,math,hashlib
from fractions import Fraction as F
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[2]/'gaussian_transfer';sys.path.insert(0,str(ROOT))
from displaced_sampler import DisplacedHeraldGaussian,DisplacedAggregateMatching,ParityEnvelope
from rational_gaussian_arb import pure_kernel
DIR=Path(__file__).resolve().parent
files=['displaced_sampler.py','displaced_evaluator.py'];hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}

def kernel(C):
 m=len(C);return [[F(0) if (i<m)==(j<m) else C[i%m][j%m] for j in range(2*m)] for i in range(2*m)]
def check(vals,z,target):
 n=len(vals);ys=[float(z**x) for x in vals];avg=sum(ys)/n
 se=math.sqrt(sum((v-avg)**2 for v in ys)/(n*(n-1)))
 zs=(avg-target)/se;assert abs(zs)<5,(zs,avg,target,se)
 return {'z':str(z),'target':target,'mean':avg,'standard_error':se,'z_score':zs}

rng=random.Random(667641);emp=[]
t=F(1,3);g=F(2,5);C=[[F(1,4),0],[0,t]];ell=[F(1,5),g]*2
for h in [3,10**20]:
 model=DisplacedHeraldGaussian(kernel(C),ell,0,h)
 vals=[model.sample(rng,F(1,10**8))[0] for _ in range(1400)]
 pgfs=[]
 for z in [F(1,2),F(3,4)]:
  target=float((1-t)/(1-t*z))*math.exp(float(g*g*z/(1-t*z)-g*g/(1-t)))
  pgfs.append(check(vals,z,target))
 emp.append({'kind':'product_displaced_thermal','h':str(h),'draws':len(vals),'checks':pgfs})
print('product mixed done',flush=True)

# Independent full density-kernel coefficient recurrence for a coupled mixed
# physical Gaussian: C PSD rank1, ell real nonnegative.
C=[[F(1,8),F(1,8)],[F(1,8),F(1,8)]];K=kernel(C);ell=[F(1,10),F(1,5)]*2
@lru_cache(None)
def coeff(n):
 if not any(n):return F(1)
 i=next(i for i,v in enumerate(n) if v);rest=list(n);rest[i]-=1
 v=ell[i]*coeff(tuple(rest))
 for j in range(4):
  if rest[j] and K[i][j]:
   nn=rest.copy();nn[j]-=1;v+=K[i][j]*coeff(tuple(nn))
 return v/n[i]
h=2;cutoff=30
weights=[F(math.factorial(h)*math.factorial(x))*coeff((h,x,h,x)) for x in range(cutoff+1)]
model=DisplacedHeraldGaussian(K,ell,0,h)
vals=[model.sample(rng,F(1,10**8))[0] for _ in range(2400)]
emp.append({'kind':'correlated_displaced_thermal_cutoff_Fock','h':h,'cutoff':cutoff,'coefficient_states':coeff.cache_info().currsize,'draws':len(vals),'checks':[check(vals,z,float(sum(w*z**x for x,w in enumerate(weights))/sum(weights))) for z in [F(1,2),F(3,4)]]})

edges=[]
for a,b,c,h in [(0,0,0,0),(0,0,F(1,3),10**20),(F(1,4),0,F(1,10),30),(0,F(1,3),0,10**20),(F(1,4),0,0,30)]:
 model=DisplacedAggregateMatching(a,b,c,h);counts=model.sample(random.Random(1),F(1,1000))
 q1,k,s1=counts[0];q2,s2=counts[1][1:]
 assert 2*q1+k+s1==h and 2*q2+k+s2==h
 edges.append({'a':str(a),'b':str(b),'c':str(c),'h':str(h),'counts':counts})
for a,b,c,h in [(0,0,0,1),(F(1,4),0,0,3)]:
 try:DisplacedAggregateMatching(a,b,c,h);raise AssertionError('zero event accepted')
 except ValueError:pass
one_mode=DisplacedHeraldGaussian.from_pure([[F(1,4)]],[F(1,3)],0,10**8)
assert one_mode.sample(random.Random(16),F(1,1000))==[]
B=[[F(1,5),F(1,7)],[F(1,7),F(1,4)]];g=[F(1,10),F(1,5)]
class Ones:
 def getrandbits(self,k):return (1<<k)-1
model=DisplacedHeraldGaussian.from_pure(B,g,0,8)
assert model.sample(Ones(),F(1,100))==[0] and model.last_ticket_fallback
cap={'calls':model.last_ticket_count,'call_bound':model.last_ticket_bound,'bits':model.last_random_bits,'attempt_cap':model.last_ticket_attempt_cap}
# Reachable call count includes cross + two q + ghost + reverse scalar draws.
for seed in range(10):
 model.sample(random.Random(seed),F(1,1000));assert model.last_ticket_count<=model.last_ticket_bound
invalid=0
for x in [True,F(1,2),1.0,'1',-1]:
 for f in [lambda x:DisplacedHeraldGaussian.from_pure(B,g,0,x),lambda x:DisplacedHeraldGaussian.from_pure(B,g,x,1)]:
  try:f(x);raise AssertionError(('invalid accepted',x))
  except (ValueError,TypeError):invalid+=1
out={'hashes':hashes,'mixed_state_PGF':emp,'degenerate_matching':edges,'zero_events_rejected':2,'one_mode_empty_output':True,'forced_ticket_fallback':cap,'invalid_inputs_rejected':invalid}
assert hashes=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files},'source mutated'
(DIR/'audit_mixed_and_edges_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
