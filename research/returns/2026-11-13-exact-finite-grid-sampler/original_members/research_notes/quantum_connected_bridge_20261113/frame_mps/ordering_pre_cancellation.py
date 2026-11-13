import numpy as np
class OrderedMPS:
 def __init__(self,m,order):self.m=m;self.order=list(order);self.pos={x:i for i,x in enumerate(order)}
 def __getattr__(self,k):return getattr(self.m,k)
 def pair(self,i,j,g):self.m.pair(self.pos[i],self.pos[j],g)
 def one(self,i,g):self.m.one(self.pos[i],g)
 def measure(self,i,rng,forced=None):return self.m.measure(self.pos[i],rng,forced)
 def vector(self):
  v=self.m.vector();x=np.arange(len(v));ix=np.zeros(len(v),int)
  for old,new in self.pos.items():ix|=((x>>old)&1)<<new
  return v[ix]
def interaction_weights(n,records,neigh,physical):
 W=np.zeros((n,n));known=[True]*n;counts={tuple(sorted((u,v))):0 for u in range(n) for v in neigh[u] if u<v}
 def phase(u,v):
  if not known[u] and not known[v]:W[u,v]+=1;W[v,u]+=1
 for ev,_,_,_ in records:
  for (u,v),reset,rare,cand in ev:
   counts[tuple(sorted((u,v)))]+=1
   if physical:phase(u,v)
  for (u,v),reset,rare,cand in ev:
   if not rare:continue
   edges=[e for e,k in counts.items() if k and(u in e or v in e)]
   if not physical:
    for a,b in edges:phase(a,b)
   W[u,v]+=1;W[v,u]+=1;known[u]=known[v]=False
   if not physical:
    for a,b in edges:phase(a,b)
  for(u,v),reset,rare,cand in ev:
   if reset:known[u]=known[v]=True
 return W

def choose_order(n,records,neigh,mode,physical=False):
 if not isinstance(mode,str):return mode
 if mode=='snake':
  w=int(np.sqrt(n));return [y*w+x for y in range(n//w) for x in (range(w) if y%2==0 else range(w-1,-1,-1))]
 W=interaction_weights(n,records,neigh,physical)
 # Connected pieces of the ACTUAL two-site circuit may be ordered independently.
 seen=set();pieces=[]
 for x in range(n):
  if x in seen:continue
  stack=[x];seen.add(x);c=[]
  while stack:
   v=stack.pop();c.append(v)
   for u in np.flatnonzero(W[v]):
    if int(u) not in seen:seen.add(int(u));stack.append(int(u))
  pieces.append(c)
 order=[]
 for c in sorted(pieces,key=lambda c:-len(c)):
  if len(c)<=2:order+=c;continue
  a=W[np.ix_(c,c)];L=np.diag(a.sum(1))-a;vals,V=np.linalg.eigh(L);p=list(np.array(c)[np.argsort(V[:,1])])
  if mode=='spectral':order+=p;continue
  # Coordinate descent for weighted minimum linear arrangement, deterministic.
  def cost(p):
   pos=np.empty(n,int);pos[p]=np.arange(len(p));return sum(W[u,v]*abs(pos[u]-pos[v]) for u in p for v in np.flatnonzero(W[u]))/2
  best=cost(p)
  for sweep in range(3):
   changed=False
   for i in range(len(p)):
    for j in range(i+1,min(len(p),i+9)):
     p[i],p[j]=p[j],p[i];new=cost(p)
     if new<best-1e-9:best=new;changed=True
     else:p[i],p[j]=p[j],p[i]
   if not changed:break
  order+=p
 return order
