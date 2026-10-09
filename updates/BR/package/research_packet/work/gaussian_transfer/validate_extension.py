from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import time, random, json, math, statistics, platform, sys, tracemalloc
import flint
from large_herald_arb import AggregateMatching, LargeHeraldGaussian, CappedTickets
from rational_gaussian_arb import RationalLoopMatching, RationalGaussian, pure_kernel
from bigint_sampler_arb import DyadicUnimodal, _as_iv
from flint import arb
ROOT=Path(__file__).resolve().parent
out={'revision':'capped-ticket-v2','python':sys.version,'flint':flint.__version__,'platform':platform.platform(),'seed':7621926,'tolerance':'1e-10'}
rng=random.Random(out['seed'])

def weight(a,b,h,k):
 q=(h-k)//2
 return F(math.factorial(h)**2,math.factorial(k)*2**(h-k)*math.factorial(q)**2)*a**(h-k)*b**k

# Exact independently indexed pairing recurrence against aggregate partition.
checks=0; bounds_checks=0; mode_checks=0
for h in range(0,31):
 for a,b in [(F(1,3),F(2,7)),(F(1,1000),F(2,3)),(F(7,8),F(1,100)),(F(1),F(1))]:
  model=AggregateMatching(a,b,h)
  ws=[weight(a,b,h,k) for k in range(h%2,h+1,2)]
  dp=RationalLoopMatching([[a,b],[b,a]],[F(0),F(0)],[h,h])
  assert sum(ws)==dp.partition;checks+=1
  assert ws[model.mode]==max(ws);mode_checks+=1
  if model.deterministic is None:
   law=model.law(F(1,10**12))
   for j,w in enumerate(ws):
    lo,hi=law.bounds(j); exact=law.scale*w/ws[model.mode]
    assert lo<=exact<=hi,(h,a,b,j,lo,exact,hi)
    assert hi-lo<=2;bounds_checks+=1
out['exact_matching_checks']=checks;out['exact_mode_checks']=mode_checks;out['exact_arb_enclosure_checks']=bounds_checks

# All scalar kinds used by this zero-displacement extension.
scalar_checks=0
for n in [1,2,4,9,30]:
 for p in [F(1,9),F(1,2),F(7,9)]:
  m=min(n,((n+1)*p.numerator)//p.denominator)
  def lr(k,m):
   return arb(m+1).lgamma()+arb(n-m+1).lgamma()-arb(k+1).lgamma()-arb(n-k+1).lgamma()+(k-m)*(_as_iv(p).log()-_as_iv(1-p).log())
  law=DyadicUnimodal(n,m,lr,F(1,10**12),50)
  probs=[F(math.comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1)]
  for k in range(n+1):
   l,u=law.bounds(k);v=law.scale*probs[k]/probs[m];assert l<=v<=u;scalar_checks+=1
for r in [F(1,2),F(3,2),F(9,2),F(11)]:
 for p in [F(1,9),F(1,2),F(7,9)]:
  m=max(0,math.floor((r-1)*(1-p)/p));T=max(40,m+20)
  def lr(k,m):
   rr=_as_iv(r)
   return (k+rr).lgamma()-arb(k+1).lgamma()-(m+rr).lgamma()+arb(m+1).lgamma()+(k-m)*_as_iv(1-p).log()
  law=DyadicUnimodal(T,m,lr,F(1,10**12),50)
  rel=[F(1)]
  for k in range(T):rel.append(rel[-1]*(r+k)*(1-p)/(k+1))
  for k in range(T+1):
   l,u=law.bounds(k);v=law.scale*rel[k]/rel[m];assert l<=v<=u;scalar_checks+=1
out['exact_arb_scalar_checks']=scalar_checks

# Pointwise full-program identity for B=[[a,t],[t,0]]: output equals K.
physical_checks=0
for h in [0,1,2,3,10,31,1000,10**20]:
 for seed in range(10):
  model=LargeHeraldGaussian.from_pure([[F(1,4),F(1,2)],[F(1,2),F(0)]],0,h)
  a,b=model.matching.a,model.matching.b
  eps=F(1,10**10);S=max(1,model.base.engine.max_scalar_calls)
  mtol=3*eps/8;stol=3*eps/(8*S)
  max_attempts=max(4*(q.denominator.bit_length()+4) for q in (mtol,stol))
  R=3*(model.base.engine.max_scalar_calls+1)*max_attempts
  k=AggregateMatching(a,b,h).draw_k(CappedTickets(random.Random(seed),R,eps/4),mtol)
  assert model.sample(random.Random(seed),F(1,10**10))==[k]
  physical_checks+=1
out['full_program_exact_output_identity_checks']=physical_checks

# Three-mode independent photon-amplitude recurrence at small herald.
B=[[F(1,5),F(1,7),F(1,11)],[F(1,7),F(1,4),F(1,13)],[F(1,11),F(1,13),F(1,6)]]
@lru_cache(None)
def amplitude(n):
 if sum(n)==0:return F(1)
 if sum(n)%2:return F(0)
 i=next(i for i,k in enumerate(n) if k)
 rest=list(n);rest[i]-=1
 # derivative recurrence: n_i c_n = sum_j B_ij c_(n-e_i-e_j)
 val=F(0)
 for j in range(3):
  if rest[j]:
   nn=rest.copy();nn[j]-=1
   val+=B[i][j]*amplitude(tuple(nn))
 return val/n[i]
h=4;cut=20
weights=[]
for x in range(cut+1):
 for y in range(cut+1):
  n=(h,x,y);c=amplitude(n)
  weights.append((x,y,F(math.factorial(h)*math.factorial(x)*math.factorial(y))*c*c))
Z=sum(w for _,_,w in weights)
pgfz=[(F(1,2),F(3,4)),(F(9,10),F(4,5)),(F(1),F(1,3))]
# Truncated independent expansion; its missing mass is diagnosed versus exact marginal normalizer.
model=LargeHeraldGaussian.from_pure(B,0,h)
small=RationalGaussian.from_pure(B,herald_modes=[0],herald_counts=[h])
exact_parts=[small.pgf_parts(z) for z in pgfz]
exact_pgf=[math.sqrt(float(d))*float(w) for d,e,w in exact_parts]
fock_pgf=[float(sum(w*z[0]**x*z[1]**y for x,y,w in weights)/Z) for z in pgfz]
assert max(abs(x-y) for x,y in zip(exact_pgf,fock_pgf))<1e-10
samples=1200
sums=[0.]*len(pgfz);squares=[0.]*len(pgfz)
t0=time.perf_counter()
for _ in range(samples):
 x,y=model.sample(rng,F(1,10**10))
 for i,z in enumerate(pgfz):
  v=float(z[0]**x*z[1]**y);sums[i]+=v;squares[i]+=v*v
emp=[]
for i in range(len(pgfz)):
 mean=sums[i]/samples;se=math.sqrt(max(0,squares[i]/samples-mean*mean)/samples)
 emp.append({'z':list(map(str,pgfz[i])),'exact_pgf':exact_pgf[i],'independent_fock_cutoff_pgf':fock_pgf[i],'empirical':mean,'standard_error':se,'z_score':(mean-exact_pgf[i])/se})
from flint import ctx
with ctx.workprec(200):
 part=small.matching.partition;det=small.engine.determinant
 Zfull=_as_iv(part)/_as_iv(det).sqrt()/arb(math.factorial(h))
 tail=1-_as_iv(Z)/Zfull
 tail_report=str(tail)
 assert tail.upper()<arb('1e-9')
out['three_mode_pgf']={'rigorous_fock_omitted_mass_interval':tail_report,'herald':h,'fock_cutoff_each':cut,'draws':samples,'seconds':time.perf_counter()-t0,'checks':emp}
print('finite checks complete',flush=True)

# Matched source-DP vs new matching initialisation/sampling at exact same rational input.
bench=[]
for h in [4,10,20,40,80,160]:
 t=time.perf_counter();old=RationalGaussian.from_pure(B,herald_modes=[0],herald_counts=[h]);old_setup=time.perf_counter()-t
 states=old.matching.Z.cache_info().currsize
 t=time.perf_counter();new=LargeHeraldGaussian.from_pure(B,0,h);new_setup=time.perf_counter()-t
 t=time.perf_counter();old.sample(random.Random(800+h),F(1,10**10));old_sample=time.perf_counter()-t
 t=time.perf_counter();new.sample(random.Random(800+h),F(1,10**10));new_sample=time.perf_counter()-t
 bench.append({'h':str(h),'old_setup_s':old_setup,'old_sample_s':old_sample,'old_DP_states':states,'new_setup_s':new_setup,'new_sample_s':new_sample})
out['matched_DP_comparator']=bench

scaling=[]
for h in [10,10**6,10**20,10**50,10**100]:
 t=time.perf_counter();model=LargeHeraldGaussian.from_pure(B,0,h);setup=time.perf_counter()-t
 tracemalloc.start();ts=[];outputs=[]
 for seed in [1701,1702,1703]:
  t=time.perf_counter();v=model.sample(random.Random(seed),F(1,10**10));ts.append(time.perf_counter()-t);outputs.append(v)
 _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 law=model.matching.law(F(3,8*10**10))
 entries=sum(len(r.through)**2 for r in model.base.engine.records)
 coefficient_bits=max(max(abs(x.numerator).bit_length(),x.denominator.bit_length()) for r in model.base.engine.records for row in r.through for x in row)
 scaling.append({'h':str(h),'h_bits':h.bit_length(),'setup_s':setup,'draw_seconds':ts,'median_s':statistics.median(ts),'peak_python_traced_bytes':peak,'routing_rational_entries':entries,'max_routing_coefficient_bits':coefficient_bits,'max_scalar_calls':model.base.engine.max_scalar_calls,'matching_blocks':len(law.blocks),'matching_grid_bits':law.bits,'matching_max_precision_bits':law.max_precision_used,'matching_enclosure_evaluations':law.num_bounds,'matching_total_proposals':law.total_attempts,'matching_fallbacks':law.fallback_count,'output_bits':[max(x.bit_length() for x in v) for v in outputs],'first_output':list(map(str,outputs[0])),'last_sample_random_bits':model.last_random_bits,'last_sample_ticket_count':model.last_ticket_count,'ticket_attempt_cap':model.last_ticket_attempt_cap,'max_uniform_tickets':model.last_ticket_bound,'ticket_fallback':model.last_ticket_fallback})
 print('scaling',h.bit_length(),flush=True)
out['binary_herald_scaling']=scaling

# Exact calibration lower-bound algebra at finite rational h.
acq=[]
for m in [1,2,4,10,100]:
 h=4*m*m;a=F(1,4);t=F(1,4*m);b=t*t
 ratio=(b/a)**2*h*h/2
 D=1-a*a-2*t*t+t**4
 x=F(8*h-1,15*h*h)
 assert ratio==F(1,2);assert D/(1-a*a)==1-x
 # exact conditional mass, feasible only for modest h; lower bound universal
 tv=None
 if h<=400:
  w=[weight(a,b,h,k) for k in range(0,h+1,2)]
  tv=str(1-w[0]/sum(w))
 acq.append({'h':h,'ratio_w2_w0':str(ratio),'fidelity_squared_squared':str(1-x),'TV_lower_bound':'1/3','exact_TV_when_enumerated':tv,'N_lower_bound':str(F(5*h,96))})
out['exact_acquisition_checks']=acq
(ROOT/'validation_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if 'scaling' not in k and 'comparator' not in k},indent=2))
