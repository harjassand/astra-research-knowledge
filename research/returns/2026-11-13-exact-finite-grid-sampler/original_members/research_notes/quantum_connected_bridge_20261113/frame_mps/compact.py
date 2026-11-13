"""Exact basis-leg compaction, retaining all virtual correlations on removal."""
import bisect,numpy as np
class CompactMPS:
 def __init__(self,m,n,order,weights=None,birth_order=False,gate_budget=None):
  self.weights=weights;self.birth_order=birth_order;self.gate_budget=gate_budget;self.pair_calls=0
  self.m=m;self.n=n;self.order=list(order);self.rank={s:i for i,s in enumerate(order)};self.ids=[];self.bits=[0]*n;self.max_active=0
  m.ts=[];m.center=0
 def __getattr__(self,k):return getattr(self.m,k)
 def activate(self,s,where=None):
  if self.bits[s] is None:return
  k=bisect.bisect_left([self.rank[x] for x in self.ids],self.rank[s]) if where is None else where;oldlen=len(self.ids)
  bond=self.m.ts[k].shape[0] if k<oldlen else 1
  t=np.zeros((bond,2,bond),complex);t[:,self.bits[s],:]=np.eye(bond)
  self.m.ts.insert(k,t);self.ids.insert(k,s)
  if oldlen and self.m.center>=k:self.m.center+=1
  elif not oldlen:self.m.center=0
  self.bits[s]=None;self.max_active=max(self.max_active,len(self.ids))
 def gap(self,sites,choices=None):
  positions=np.arange(len(self.ids));weights=np.array([sum(self.weights[s,w] for s in sites) for w in self.ids])
  if choices is None:choices=range(len(self.ids)+1)
  return min(choices,key=lambda k:float(np.dot(weights,abs(positions+.5-k))))
 def pair(self,s,t,g):
  if self.birth_order:
   new_s=self.bits[s] is not None;new_t=self.bits[t] is not None
   if new_s and new_t:
    k=self.gap([s,t]);self.activate(s,k);self.activate(t,k+1)
   elif new_s:
    k=self.ids.index(t);self.activate(s,self.gap([s],[k,k+1]))
   elif new_t:
    k=self.ids.index(s);self.activate(t,self.gap([t],[k,k+1]))
  else:self.activate(s);self.activate(t)
  i=self.ids.index(s);j=self.ids.index(t);self.pair_calls+=1
  if self.gate_budget is not None:
   # This wrapper is used with MPO compression: exactly distance SVDs per gate.
   self.m.tol=self.gate_budget/max(1,abs(i-j))
  self.m.pair(i,j,g)
 def product_sum(self,terms):
  for s in sorted(set().union(*(set(o) for c,o in terms)),key=lambda s:self.rank[s]):self.activate(s)
  pos={s:i for i,s in enumerate(self.ids)};self.m.product_sum([(c,{pos[s]:op for s,op in ops.items()}) for c,ops in terms])
 def one(self,s,g):
  if self.bits[s] is not None:
   col=g[:,self.bits[s]];support=np.flatnonzero(col!=0)
   if len(support)==1:self.bits[s]=int(support[0]);return
   self.activate(s)
  self.m.one(self.ids.index(s),g)
 def measure(self,s,rng,forced=None):
  self.m.check_budget()
  if self.bits[s] is not None:
   if forced is None:rng.random() # preserve draw schedule against uncompressed implementation
   elif forced!=self.bits[s]:raise ArithmeticError('Forced incompatible known-basis result')
   return self.bits[s],1.
  k=self.ids.index(s);b,p=self.m.measure(k,rng,forced);B=self.m.ts[k][:,b,:]
  if k+1<len(self.ids):
   self.m.ts[k+1]=np.einsum('ab,bsc->asc',B,self.m.ts[k+1]);self.m.ts.pop(k);self.m.center=k
  elif k>0:
   self.m.ts[k-1]=np.einsum('asb,bc->asc',self.m.ts[k-1],B);self.m.ts.pop(k);self.m.center=k-1
  else:self.m.ts=[];self.m.center=0
  self.ids.pop(k);self.bits[s]=b
  return b,p
 def vector(self):
  q=self.m.vector() if self.ids else np.ones(1,complex);out=np.zeros(1<<self.n,complex);base=sum(b<<s for s,b in enumerate(self.bits) if b is not None)
  for idx,a in enumerate(q):
   j=base
   for k,s in enumerate(self.ids):j|=((idx>>k)&1)<<s
   out[j]=a
  return out
