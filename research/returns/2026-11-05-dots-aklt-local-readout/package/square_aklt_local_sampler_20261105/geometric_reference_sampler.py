"""Independent reference: reveal whole geometric Poisson regions, not soft complements."""
from collections import defaultdict,deque
from local_perfect_sampler import LocalPerfectLoopSampler
from perfect_loop_sampler import poisson_exact,geometry
from exact_lazy_time import ZERO,exponential_time

class GeometricReferenceSampler(LocalPerfectLoopSampler):
 def sample(self):
  rng=self.rng;pool=[];queue=deque();queried=[];targets=[];marks={};index=defaultdict(set)
  def add(route,birth,death,needed=False,target=False):
   i=len(pool);g=geometry(route)
   pool.append(dict(route=route,geometry=g,birth=birth,death=death,needed=needed,parents=set()))
   for v in g[0]:index[v].add(i)
   if needed:queue.append(i)
   if target:targets.append(i)
   return i
  def conflict(g,h):
   if g[1]&h[1]:return True
   k=len(g[0]&h[0]);return bool(k and rng.randrange(5**k)>=3**k)
  def covers(p,t):return p['birth']<t and t<p['death']
  def connect(child,parent):
   key=tuple(sorted((child,parent)))
   if key not in marks:marks[key]=conflict(pool[child]['geometry'],pool[parent]['geometry'])
   if marks[key]:
    pool[child]['parents'].add(parent)
    if not pool[parent]['needed']:pool[parent]['needed']=True;queue.append(parent)
  for _ in range(poisson_exact(self.birth.rate(self.query),rng)):
   route=self.birth.propose(self.query,self.box)
   if route is not None:add(route,-exponential_time(rng),exponential_time(rng),True,True)
  while queue:
   c=queue.popleft();obj=pool[c];t=obj['birth'];vertices=obj['geometry'][0]
   known=set().union(*(index[v] for v in vertices));known.discard(c)
   for p in sorted(known):
    if covers(pool[p],t):connect(c,p)
   for _ in range(poisson_exact(self.birth.rate(vertices),rng)):
    route=self.birth.propose(vertices,self.box)
    if route is None:continue
    g=geometry(route);birth=t-exponential_time(rng);death=t+exponential_time(rng)
    p=dict(birth=birth,death=death)
    if g[0]&self.query and ZERO<death:continue
    if any(g[0]&pool[q]['geometry'][0] and covers(p,pool[q]['birth']) for q in queried):continue
    parent=add(route,birth,death)
    connect(c,parent)
   queried.append(c)
  needed={i for i,p in enumerate(pool) if p['needed']};counts={i:len(pool[i]['parents']) for i in needed};children=defaultdict(list)
  for i in needed:
   for p in pool[i]['parents']:assert p in needed;children[p].append(i)
  ready=deque(i for i,n in counts.items()if n==0);accepted=set();processed=0
  while ready:
   i=ready.popleft();processed+=1
   if not(pool[i]['parents']&accepted):accepted.add(i)
   for c in children[i]:
    counts[c]-=1
    if counts[c]==0:ready.append(c)
  assert processed==len(needed)
  return [pool[i]['route']for i in targets if i in accepted],{'clan_size':len(needed),'geometrically_exposed':len(pool)}
