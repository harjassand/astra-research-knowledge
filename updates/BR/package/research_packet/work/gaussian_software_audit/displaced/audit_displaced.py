from pathlib import Path
import sys,random,json,math,time,hashlib
from fractions import Fraction as F
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[2]/'gaussian_transfer'
sys.path.insert(0,str(ROOT))
from displaced_sampler import ParityEnvelope,DisplacedAggregateMatching,DisplacedHeraldGaussian
from displaced_evaluator import log_H
from bigint_sampler_arb import _as_iv
from flint import arb,ctx
DIR=Path(__file__).resolve().parent
files=['displaced_sampler.py','displaced_evaluator.py']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}
out={'hashes':hashes}

def H(n,a,c):
 return sum(((a/2)**q*c**(n-2*q)/(math.factorial(q)*math.factorial(n-2*q)) for q in range(n//2+1)),F(0))
def ws(h,a,b,c):return [b**k*H(h-k,a,c)**2/math.factorial(k) for k in range(h+1)]

cases=0;pointchecks=0;conditional=0;max_tv=F(0)
for h in [1,2,3,4,7,10,15]:
 for a,b,c in [(F(0),F(1),F(1)),(F(1,4),F(7,40),F(1,100)),(F(1,3),F(2,7),F(3,11)),(F(7,8),F(1,100),F(1,10**10)),(F(1,10**15),F(11),F(10))]:
  tol=F(1,1000);law=ParityEnvelope(a,b,c,h,tol);weights=ws(h,a,b,c)
  support=[];accepted=[]
  with ctx.workprec(500):
   G=sum((_as_iv(w)*(-law.reference).exp() for w in weights),arb(0))
   assert G.lower()>arb(1)/2,(h,a,b,c,'reference too high',G)
   for e,l,r,height in law.blocks:
    for j in range(l,r+1):
     k=e+2*j;support.append(k)
     exact=law.scale*_as_iv(weights[k])*(-law.reference).exp()
     lo,hi=law.bounds(k)
     assert arb(lo)<=exact.lower() and arb(hi)>=exact.upper(),(h,a,b,c,k,'enclosure')
     assert arb(height)>=exact.upper(),(h,a,b,c,k,'envelope')
     assert hi-lo<=2
     pointchecks+=1
   assert sorted(support)==list(range(h+1))
   assert arb(law.total)/law.scale<=12*G+arb(4*(h+1))/law.scale
  accepted=[law.bounds(k)[0] for k in range(h+1)]
  assert sum(accepted)>0
  tv=sum(abs(F(x,sum(accepted))-w/sum(weights)) for x,w in zip(accepted,weights))/2
  assert tv<tol/16,(h,a,b,c,tv)
  max_tv=max(tv,max_tv);cases+=1
  model=DisplacedAggregateMatching(a,b,c,h)
  for n in range(h+1):
   qlaw=model.conditional_law(n,tol)
   qweights=[(a/2)**q*c**(n-2*q)/(math.factorial(q)*math.factorial(n-2*q)) for q in range(n//2+1)]
   if qlaw is None:
    assert not any(qweights[1:]);continue
   assert qweights[qlaw.mode]==max(qweights)
   for q,w in enumerate(qweights):
    lo,hi=qlaw.bounds(q);target=qlaw.scale*w/qweights[qlaw.mode]
    assert lo<=target<=hi;conditional+=1
out['exact_parity_cross_checks']={'laws':cases,'point_bounds':pointchecks,'conditional_q_bounds':conditional,'max_exact_rounding_TV':str(max_tv)}
print('exact laws completed',flush=True)

# A large-count regression specifically detects low-context precision during
# extraction of the common log reference (the prefreeze bug).
large=[]
for h in [10**10,10**20,10**50]:
 law=ParityEnvelope(F(0),F(1),F(1),h,F(1,1000))
 with ctx.workprec(1000):
  w=law._logweight(law.reference_k,250)
  gap=law.reference-w
  assert gap.lower()>=0 and gap.upper()<arb(1)/8,(h,gap)
 lo,hi=law.bounds(law.reference_k)
 assert lo>law.scale//2
 val=law.draw(random.Random(737))
 assert not law.used_fallback
 large.append({'h_bits':h.bit_length(),'reference_gap':str(gap),'anchor_lower_fraction':str(F(lo,law.scale)),'attempts':law.last_attempts,'output_bits':val.bit_length()})
out['large_reference_regression']=large
print('large references completed',flush=True)

# Product coherent state: herald is independent, unobserved n~Pois(g^2).
rng=random.Random(727261);emp=[]
def pgf_check(vals,z,target):
 ys=[float(z**x) for x in vals];mean=sum(ys)/len(ys)
 se=math.sqrt(sum((x-mean)**2 for x in ys)/(len(ys)*(len(ys)-1)))
 score=(mean-target)/se
 assert abs(score)<5,(mean,target,se,score)
 return {'z':str(z),'target':target,'mean':mean,'standard_error':se,'z_score':score}
for h in [0,3,10**20]:
 model=DisplacedHeraldGaussian.from_pure([[F(0),F(0)],[F(0),F(0)]],[F(1,3),F(3,4)],0,h)
 vals=[model.sample(rng,F(1,10**8))[0] for _ in range(1200)]
 emp.append({'kind':'coherent','h':str(h),'draws':len(vals),'checks':[pgf_check(vals,z,math.exp(float(F(9,16)*(z-1)))) for z in [F(1,2),F(3,4)]]})
# Independent squeezed displaced outputs with a closed Mehler PGF.
h=7;s=F(1,3);g=F(2,5)
model=DisplacedHeraldGaussian.from_pure([[F(1,4),0],[0,s]],[F(1,7),g],0,h)
vals=[model.sample(rng,F(1,10**8))[0] for _ in range(1600)]
emp.append({'kind':'squeezed_coherent','h':str(h),'draws':len(vals),'checks':[pgf_check(vals,z,math.sqrt(float((1-s*s)/(1-s*s*z*z)))*math.exp(float(g*g*z/(1-s*z)-g*g/(1-s)))) for z in [F(1,2),F(3,4)]]})
print('product states completed',flush=True)

# Independent pure displaced amplitude recurrence, with nonzero cross coupling.
B=[[F(1,5),F(1,7)],[F(1,7),F(1,4)]];g=[F(1,10),F(1,5)]
@lru_cache(None)
def amplitude(n):
 if not any(n):return F(1)
 i=next(i for i,x in enumerate(n) if x)
 rest=list(n);rest[i]-=1
 v=g[i]*amplitude(tuple(rest))
 for j in range(2):
  if rest[j]:
   nn=rest.copy();nn[j]-=1
   v+=B[i][j]*amplitude(tuple(nn))
 return v/n[i]
for h in [1,4]:
 cutoff=60
 weights=[F(math.factorial(h)*math.factorial(x))*amplitude((h,x))**2 for x in range(cutoff+1)]
 # No omitted-tail guarantee inferred from normalized cutoff agreement here.
 model=DisplacedHeraldGaussian.from_pure(B,g,0,h)
 vals=[model.sample(rng,F(1,10**8))[0] for _ in range(1800)]
 emp.append({'kind':'coupled_pure_displaced_cutoff_Fock','h':str(h),'cutoff':cutoff,'draws':len(vals),'checks':[pgf_check(vals,z,float(sum(w*z**x for x,w in enumerate(weights))/sum(weights))) for z in [F(1,2),F(3,4)]]})
out['full_program_independent_PGF_checks']=emp
print('coupled states completed',flush=True)
assert hashes=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files},'sampler/evaluator modified during run'
(DIR/'audit_displaced_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
