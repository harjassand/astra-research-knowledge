"""Exact query-local marked-Poisson ancestor exploration.
Returns every accepted loop touching a finite vertex query, on Z² by default
or in a specified open box. No spatial, temporal, path or ancestor cutoff.
Correctness uses the explicit conditional unexplored-Poisson invariant.
"""
from pathlib import Path
from collections import defaultdict,deque,Counter
from fractions import Fraction as F
import random,time,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_boundary_operation_20261105'))
from perfect_loop_sampler import poisson_exact,geometry,exact_small_box
from local_birth_oracle import LocalLoopBirthSampler
from exact_lazy_time import ZERO,exponential_time

class LocalPerfectLoopSampler:
 def __init__(self,query_vertices,box=None,seed=0):
  self.query=frozenset(tuple(v) for v in query_vertices)
  if not self.query:raise ValueError('A nonempty finite vertex query is required.')
  self.box=box;self.birth=LocalLoopBirthSampler(seed+1);self.rng=random.Random(seed)
 def sample(self,query_vertices=None):
  query=self.query if query_vertices is None else frozenset(tuple(v) for v in query_vertices)
  if not query:raise ValueError("A nonempty finite vertex query is required.")
  if any(len(v)!=2 or any(not isinstance(a,int) for a in v) for v in query):raise ValueError("Query vertices must be integer coordinate pairs.")
  rng=self.rng;pool={};queue=deque();queried=[];targets=[];marks={};nextid=0
  stats=Counter();index=defaultdict(set)
  def add(route,birth,death,target=False):
   nonlocal nextid
   i=nextid;nextid+=1;g=geometry(route)
   pool[i]={'route':route,'geometry':g,'birth':birth,'death':death,'parents':set()}
   for v in g[0]:index[v].add(i)
   queue.append(i)
   if target:targets.append(i)
   stats['retained_loop_edges']+=len(route);stats['maximum_loop_length']=max(stats['maximum_loop_length'],len(route))
   return i
  def flip_conflict(g,h):
   stats['conflict_mark_draws']+=1
   if g[1]&h[1]:return True
   k=len(g[0]&h[0])
   return bool(k and rng.randrange(5**k)>=3**k)
  def covers(obj,t):
   stats['time_comparisons']+=1
   if not(obj['birth']<t):return False
   stats['time_comparisons']+=1
   return t<obj['death']
  # Seed the whole stationary cylinder process restricted to alive0 and
  # loops meeting the requested vertices, not an approximate boundary.
  n=poisson_exact(self.birth.rate(query),rng);stats['seed_proposals']=n
  for _ in range(n):
   route=self.birth.propose(query,self.box)
   if route is None:continue
   stats['exponential_atoms']+=2
   add(route,-exponential_time(rng),exponential_time(rng),True)
  stats['seed_cylinders']=len(targets)
  while queue:
   stats['maximum_queue']=max(stats['maximum_queue'],len(queue));child=queue.popleft();c=pool[child];t=c['birth'];g=c['geometry']
   # Known atoms are reused. Only their previously unexposed pair marks
   # can be sampled; shared ancestors must not be independently redrawn.
   possible=set()
   for v in g[0]:possible.update(index[v])
   possible.discard(child)
   for parent in sorted(possible):
    stats['known_atom_tests']+=1;p=pool[parent]
    if not covers(p,t):continue
    key=tuple(sorted((parent,child)))
    if key not in marks:marks[key]=flip_conflict(g,p['geometry'])
    if marks[key]:c['parents'].add(parent)
   # The unknown process is PPP on the complement of all earlier exposed
   # marked regions. Generate from the new region, then exactly thin by
   # the old-region exclusions; do not match these proposals to old atoms.
   n=poisson_exact(self.birth.rate(g[0]),rng);stats['parent_proposals']+=n
   for _ in range(n):
    route=self.birth.propose(g[0],self.box)
    if route is None:continue
    h=geometry(route);stats['parent_loop_proposals']+=1
    if not flip_conflict(g,h):continue
    stats['exponential_atoms']+=2
    p={'birth':t-exponential_time(rng),'death':t+exponential_time(rng),'geometry':h}
    if h[0]&query:
     stats['time_comparisons']+=1
     if ZERO<p['death']:
      stats['rejected_seed_region']+=1;continue
    false_previous=[];reject=False
    for old in queried:
     d=pool[old]
     if not(h[0]&d['geometry'][0]):continue
     stats['previous_region_tests']+=1
     if covers(p,d['birth']):
      if flip_conflict(h,d['geometry']):reject=True;break
      false_previous.append(old)
    if reject:
     stats['rejected_previous_region']+=1;continue
    parent=add(route,p['birth'],p['death'])
    for old in false_previous:marks[tuple(sorted((parent,old)))]=False
    marks[tuple(sorted((parent,child)))]=True;c['parents'].add(parent)
   queried.append(child)
  # A topological order of actual conflict dependencies is enough. It
  # avoids extra real-time sorting, while retaining shared ancestor IDs.
  remaining={i:len(c['parents']) for i,c in pool.items()};children=defaultdict(list)
  for i,c in pool.items():
   for p in c['parents']:children[p].append(i)
  ready=deque(i for i,k in remaining.items() if k==0);accepted=set();processed=0
  while ready:
   i=ready.popleft();processed+=1
   if all(p not in accepted for p in pool[i]['parents']):accepted.add(i)
   for j in children[i]:
    remaining[j]-=1
    if remaining[j]==0:ready.append(j)
  assert processed==len(pool),'Strict birth ordering must make the clan acyclic.'
  result=[pool[i]['route'] for i in targets if i in accepted]
  stats['clan_size']=len(pool);stats['queried_cylinders']=len(queried);stats['known_pair_marks']=len(marks)
  return result,dict(stats)

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=1000);ap.add_argument('--box',type=int,default=3);ap.add_argument('--infinite',action='store_true');a=ap.parse_args()
 s=LocalPerfectLoopSampler([(1,1)],box=None if a.infinite else(a.box,a.box),seed=20261105)
 start=time.monotonic();hist=Counter();work=Counter();maxclan=0
 for k in range(a.samples):
  loops,stats=s.sample();hist[len(loops)]+=1;work.update(stats);maxclan=max(maxclan,stats['clan_size'])
  if(k+1)%max(1,a.samples//5)==0:print('sample',k+1,'elapsed',time.monotonic()-start,flush=True)
 r={'query':[[1,1]],'box':None if a.infinite else[a.box,a.box],'samples':a.samples,'mean_observed_loops':sum(k*v for k,v in hist.items())/a.samples,
 'count_histogram':dict(hist),'mean_work':{k:v/a.samples for k,v in work.items()},'max_clan':maxclan,'elapsed_seconds':time.monotonic()-start,
 'scope':'Exact local loop-gas marginal; pending independent exposure and implementation audit.'}
 out=Path(__file__).parent/('local_infinite_test.json' if a.infinite else f'local_box{a.box}_test.json');out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
