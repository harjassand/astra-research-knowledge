"""Exact random-bit stationary sampler for the FULL finite-box AKLT loop gas.
Uses an unbounded-length rational birth oracle and a marked backwards clan.
Continuous event times are integrated out using the reversible dominant
immigration/death chain. No floating-point decision or time cutoff is used.
"""
from fractions import Fraction as F
from math import factorial
from functools import lru_cache
from pathlib import Path
import random,json,time,sys
from collections import Counter,defaultdict
from exact_loop_birth_sampler import LoopBirthSampler,edge

@lru_cache(maxsize=4096)
def poisson_cdf_bounds(rate,k,terms):
 # 0<=rate<=1. Alternating exp(-rate) bounds are exact.
 assert 0<=rate<=1
 up=sum(((-rate)**j/F(factorial(j)) for j in range(2*terms+1)),F(0))
 lo=up-rate**(2*terms+1)/F(factorial(2*terms+1))
 series=sum((rate**j/F(factorial(j)) for j in range(k+1)),F(0))
 return lo*series,min(F(1),up*series)

def poisson_small(rate,rng):
 if not rate:return 0
 bits=32;u=rng.getrandbits(bits);k=0;terms=12
 while True:
  lo,hi=poisson_cdf_bounds(rate,k,terms);den=1<<bits
  if (u+1)*lo.denominator<=lo.numerator*den:return k
  if u*hi.denominator>=hi.numerator*den:k+=1;continue
  u=(u<<32)|rng.getrandbits(32);bits+=32;terms*=2

def poisson_exact(rate,rng):
 whole=rate.numerator//rate.denominator
 return sum(poisson_small(F(1),rng) for _ in range(whole))+poisson_small(rate-whole,rng)

def geometry(route):
 return frozenset(route),frozenset(edge(route[i],route[(i+1)%len(route)]) for i in range(len(route)))

def conflict(a,b,rng):
 av,ae=a;bv,be=b
 if ae&be:return True
 k=len(av&bv)
 return k>0 and rng.randrange(5**k)>=3**k

class PerfectLoopSampler:
 def __init__(self,width,height,seed=0,birth_factory=LoopBirthSampler,bond_weights=None):
  if not isinstance(width,int) or not isinstance(height,int) or width<1 or height<1:raise ValueError("Positive integer box dimensions are required.")
  self.width=width;self.height=height;self.birth=birth_factory(seed=seed+1);self.rng=random.Random(seed)
  self.rate=self.birth.rate_per_vertex*width*height
  self.bond_weights={} if bond_weights is None else {tuple(sorted(e)):F(t) for e,t in bond_weights.items()}
  if any(not(0<=t<=1) for t in self.bond_weights.values()):raise ValueError("Bond weights must be rational numbers in [0,1].")
 def sample(self):
  rng=self.rng;objects={};active=[];targets=[];resolved=[];nextid=0;pending=0;events=0;maxpending=0;index=defaultdict(set);comparisons=0;proposals=0
  def draw(target=False):
   nonlocal nextid,pending,proposals
   proposals+=1
   route=self.birth.propose(self.width,self.height)
   if route is None:return None
   if self.bond_weights:
    factor=F(1)
    for k in range(len(route)):factor*=self.bond_weights.get(edge(route[k],route[(k+1)%len(route)]),F(1))
    if factor<1 and rng.randrange(factor.denominator)>=factor.numerator:return None
   i=nextid;nextid+=1
   objects[i]={'route':route,'geometry':geometry(route),'needed':target,'parents':[]}
   for v in objects[i]['geometry'][0]:index[v].add(i)
   if target:targets.append(i);pending+=1
   return i
  # This Poisson stationary seed is exact, including rejected proposal marks.
  for _ in range(poisson_exact(self.rate,rng)):active.append(draw(True))
  while pending:
   events+=1;k=len(active);maxpending=max(maxpending,pending)
   # Reverse stationary immigration/death dynamics; times are unnecessary.
   if rng.randrange(self.rate.numerator+k*self.rate.denominator)<self.rate.numerator:
    active.append(draw(False));continue
   j=rng.randrange(k);i=active[j];active[j]=active[-1];active.pop()
   if i is None:continue
   obj=objects[i]
   for v in obj['geometry'][0]:
    index[v].discard(i)
    if not index[v]:del index[v]
   if not obj['needed']:
    del objects[i];continue
   pending-=1
   # All earlier cylinders alive at this birth are now in active.
   possible=set()
   for v in obj['geometry'][0]:possible.update(index.get(v,()))
   for parent in sorted(possible):
    comparisons+=1
    p=objects[parent]
    if conflict(obj['geometry'],p['geometry'],rng):
     obj['parents'].append(parent)
     if not p['needed']:p['needed']=True;pending+=1
   resolved.append(i)
  accepted=set()
  for i in reversed(resolved):
   if all(p not in accepted for p in objects[i]['parents']):accepted.add(i)
  result=[objects[i]['route'] for i in targets if i in accepted]
  return result,{'reverse_events':events,'clan_size':len(resolved),'max_unresolved_clan':maxpending,'target_candidates':len(targets),'birth_proposals':proposals,'candidate_comparisons':comparisons}

def exact_small_box(width,height):
 # Complete independently enumerated catalog only for boxes with<=12edges.
 from crossed_loop_influence import variants
 assert (width-1)*height+(height-1)*width<=12
 root=Path(__file__).resolve().parents[1]
 cat=json.loads((root/'square_aklt_loop_audit_20261105/loop_catalog_through12.json').read_text())
 from exact_loop_birth_sampler import canonical
 loops={}
 for item in cat:
  for p in variants(item['cyclic_vertices']):
   mx=max(x for x,y in p);my=max(y for x,y in p)
   for dx in range(width-mx):
    for dy in range(height-my):
     q=canonical([(x+dx,y+dy) for x,y in p]);loops[q]=F(item['activity'])
 items=list(loops.items());geoms=[geometry(p) for p,w in items];Z=F(0);occ=F(0);by_count=Counter()
 def dfs(i,chosen,weight):
  nonlocal Z,occ
  if i==len(items):Z+=weight;occ+=len(chosen)*weight;by_count[len(chosen)]+=weight;return
  dfs(i+1,chosen,weight)
  fac=F(1)
  for j in chosen:
   av,ae=geoms[i];bv,be=geoms[j]
   if ae&be:return
   fac*=F(3,5)**len(av&bv)
  dfs(i+1,chosen+[i],weight*items[i][1]*fac)
 dfs(0,[],F(1))
 return {'loop_types':len(items),'partition_function':Z,'mean_occupancy':occ/Z,'occupancy_distribution':{k:v/Z for k,v in by_count.items()}}

if __name__=='__main__':
 n=int(sys.argv[1]) if len(sys.argv)>1 else 1000
 exact=exact_small_box(3,3);sampler=PerfectLoopSampler(3,3,20261105);hist=Counter();work=[];start=time.monotonic()
 for i in range(n):
  loops,stats=sampler.sample();hist[len(loops)]+=1;work.append(stats)
  if (i+1)%100==0:print('samples',i+1,'elapsed',time.monotonic()-start,flush=True)
 result={'samples':n,'box':[3,3],'exact_loop_types':exact['loop_types'],
  'exact_partition_function':str(exact['partition_function']),'exact_mean_occupancy':str(exact['mean_occupancy']),
  'empirical_mean_occupancy':sum(k*v for k,v in hist.items())/n,'sample_histogram':dict(hist),
  'exact_occupancy_distribution':{str(k):str(v) for k,v in exact['occupancy_distribution'].items()},
  'mean_reverse_events':sum(x['reverse_events'] for x in work)/n,'max_reverse_events':max(x['reverse_events'] for x in work),
  'mean_clan_size':sum(x['clan_size'] for x in work)/n,'elapsed_seconds':time.monotonic()-start,
  'scope':'Full finite-box loop Gibbs measure. Exact rational random-bit decisions; no loop-length, time or ancestor cutoff. Not a quantum-state preparation or gap proof.'}
 (Path(__file__).parent/'perfect_sampler_test.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
