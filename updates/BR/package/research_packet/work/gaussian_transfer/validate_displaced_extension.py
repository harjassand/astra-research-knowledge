from fractions import Fraction as F
from functools import lru_cache
from math import factorial
from pathlib import Path
from flint import arb,ctx
import json,time,random,hashlib
from displaced_sampler import ParityEnvelope,DisplacedAggregateMatching,DisplacedHeraldGaussian
from rational_gaussian_arb import RationalGaussian
from bigint_sampler_arb import _as_iv
ROOT=Path(__file__).resolve().parent
source_files=['displaced_evaluator.py','displaced_sampler.py']
hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in source_files}
rng=random.Random(84091);out={'source_sha256':hashes,'seed':84091}
def H(n,a,c):
 return sum((F(1,factorial(q)*factorial(n-2*q))*(a/2)**q*c**(n-2*q) for q in range(n//2+1)),F(0))
checks=0;maxTV=F(0);envchecks=0
for h in range(1,21):
 for a,b,c in [(F(1,4),F(7,40),F(1,100)),(F(1,3),F(1,5),F(2,7)),(F(0),F(1),F(1)),(F(2),F(1,100),F(7))]:
  law=ParityEnvelope(a,b,c,h,F(1,10**9))
  w=[b**k*H(h-k,a,c)**2/factorial(k) for k in range(h+1)]
  ws=sum(w);lbs=[law.bounds(k)[0] for k in range(h+1)];ls=sum(lbs)
  tv=sum((abs(w[k]/ws-F(lbs[k],ls)) for k in range(h+1)),F(0))/2
  assert tv<F(1,10**9);maxTV=max(maxTV,tv);checks+=1
  with ctx.workprec(250):
   for e,low,high,height in law.blocks:
    for j in range(low,high+1):
     k=e+2*j
     truth=(_as_iv(w[k]).log()-law.reference).exp()*law.scale
     lo,hi=law.bounds(k)
     assert lo<=truth.lower() and truth.upper()<=hi,(h,a,b,c,k,lo,truth,hi)
     assert truth.upper()<=height
     envchecks+=1
out['exact_law_checks']=checks;out['exact_normalized_grid_TV_max']=float(maxTV);out['envelope_and_interval_checks']=envchecks

B=[[F(1,5),F(1,7),F(1,11)],[F(1,7),F(1,4),F(1,13)],[F(1,11),F(1,13),F(1,6)]]
g=[F(1,8),F(1,10),F(1,9)];h=3;cut=22
@lru_cache(None)
def amp(n):
 if sum(n)==0:return F(1)
 i=next(i for i,v in enumerate(n) if v)
 rest=list(n);rest[i]-=1
 value=g[i]*amp(tuple(rest))
 for j in range(3):
  if rest[j]:
   nn=rest.copy();nn[j]-=1
   value+=B[i][j]*amp(tuple(nn))
 return value/n[i]
weights=[]
for x in range(cut+1):
 for y in range(cut+1):
  nn=(h,x,y);cc=amp(nn)
  weights.append((x,y,F(factorial(h)*factorial(x)*factorial(y))*cc*cc))
Z=sum(v for x,y,v in weights)
old=RationalGaussian.from_pure(B,g,herald_modes=[0],herald_counts=[h])
model=DisplacedHeraldGaussian.from_pure(B,g,0,h)
with ctx.workprec(250):
 full=_as_iv(old.matching.partition)*_as_iv(old.source_rate).exp()/_as_iv(old.engine.determinant).sqrt()/factorial(h)
 tail=1-_as_iv(Z)/full
 assert 0<tail.lower() and tail.upper()<arb('1e-9')
 tailstr=str(tail)
zs=[(F(1,2),F(3,4)),(F(9,10),F(4,5)),(F(1),F(1,3))]
exact=[]
for z in zs:
 det,src,match=old.pgf_parts(z)
 with ctx.workprec(100):exact.append(float(_as_iv(det).sqrt()*_as_iv(src).exp()*_as_iv(match)))
trunc=[float(sum(v*z[0]**x*z[1]**y for x,y,v in weights)/Z) for z in zs]
assert max(abs(a-b) for a,b in zip(exact,trunc))<1e-9
N=1600;sums=[0.]*3;squares=[0.]*3
start=time.perf_counter()
for _ in range(N):
 x,y=model.sample(rng,F(1,10**10))
 for i,z in enumerate(zs):
  v=float(z[0]**x*z[1]**y);sums[i]+=v;squares[i]+=v*v
rows=[]
for i,z in enumerate(zs):
 mean=sums[i]/N;se=((squares[i]/N-mean*mean)/N)**.5
 rows.append({'z':list(map(str,z)),'exact_pgf':exact[i],'truncated_independent_fock_pgf':trunc[i],'mean':mean,'se':se,'z_score':(mean-exact[i])/se})
out['independent_fock']={'h':h,'cutoff_each':cut,'rigorous_omitted_mass':tailstr,'draws':N,'seconds':time.perf_counter()-start,'diagnostics':rows}
print('finite displaced checks passed',flush=True)

# Source DP comparator, same public input and tolerance. Warm and setup both retained.
comparison=[]
for h in [10,40,80]:
 start=time.perf_counter();old=RationalGaussian.from_pure(B,g,herald_modes=[0],herald_counts=[h]);old_setup=time.perf_counter()-start
 start=time.perf_counter();new=DisplacedHeraldGaussian.from_pure(B,g,0,h);new_setup=time.perf_counter()-start
 ot=[];nt=[]
 for seed in [61,62,63]:
  start=time.perf_counter();old.sample(random.Random(seed),F(1,10**10));ot.append(time.perf_counter()-start)
  start=time.perf_counter();new.sample(random.Random(seed),F(1,10**10));nt.append(time.perf_counter()-start)
 comparison.append({'h':h,'old_setup_s':old_setup,'new_setup_s':new_setup,'old_DP_states':old.matching.Z.cache_info().currsize,'old_draw_seconds':ot,'new_draw_seconds':nt})
out['matched_DP_comparison']=comparison

scaling=[]
for h in [10**3,10**6,10**12]:
 start=time.perf_counter();new=DisplacedHeraldGaussian.from_pure(B,g,0,h);setup=time.perf_counter()-start
 start=time.perf_counter();v=new.sample(random.Random(761),F(1,10**8));elapsed=time.perf_counter()-start
 law=next(iter(new.matching.cached.values()))
 scaling.append({'h':str(h),'h_bits':h.bit_length(),'setup_s':setup,'first_draw_s':elapsed,'output':list(map(str,v)),'output_bits':[x.bit_length() for x in v],'coefficient_calls':law.num_log_H,'cross_blocks':len(law.blocks),'cross_grid_bits':law.bits,'cross_precision_bits':law.max_precision_used,'cross_proposals':law.total_attempts,'cross_fallbacks':law.fallback_count,'ticket_count':new.last_ticket_count,'random_bits':new.last_random_bits,'ticket_fallback':new.last_ticket_fallback})
 print('displaced scaling',h,elapsed,flush=True)
out['scaling']=scaling
assert hashes=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in source_files},'Product files changed during validation'
(ROOT/'displaced_validation_results.json').write_text(json.dumps(out,indent=2))
print('done',flush=True)
