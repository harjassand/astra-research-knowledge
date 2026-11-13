"""Diagonal-frame MPS quantum trajectories. No claim of scalable certified rank."""
import numpy as np,time,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'frame_sampler'))
from sampler import plan,PHI,A,B
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);SWAP=np.eye(4)[[0,2,1,3]]
Q=A*np.eye(4)-1j*B*np.kron(X,X)
def zz(theta):return np.diag(np.exp(1j*theta*np.array([1,-1,-1,1])))
class ResourceLimit(Exception):
 pass
class MPS:
 def __init__(self,n,chi=None,tol=0,strict=False):
  self.strict=strict
  self.ts=[np.array([1,0],complex).reshape(1,2,1) for _ in range(n)];self.center=0;self.chi=chi;self.tol=tol;self.error=0.;self.maxchi=1;self.truncations=0;self.svds=0;self.peakbytes=16*2*n
 def check_budget(self):
  if (getattr(self,'wall_deadline',float('inf'))<time.perf_counter() or getattr(self,'cpu_deadline',float('inf'))<time.process_time()):
   raise ResourceLimit(dict(aborted=True,reason='time_budget',**getattr(self,'extra_stats',{}),max_bond=self.maxchi,path_error_sum=float(self.error),svds=self.svds,peak_array_bytes=self.peakbytes))
 def move(self,i):
  self.check_budget()
  while self.center<i:
   j=self.center;t=self.ts[j];l,d,r=t.shape;q,s=np.linalg.qr(t.reshape(l*d,r));self.ts[j]=q.reshape(l,d,-1);self.ts[j+1]=np.einsum('ab,bsc->asc',s,self.ts[j+1]);self.center+=1
  while self.center>i:
   j=self.center;t=self.ts[j];l,d,r=t.shape;q,s=np.linalg.qr(t.reshape(l,d*r).T);self.ts[j]=q.T.reshape(-1,d,r);self.ts[j-1]=np.einsum('asb,bc->asc',self.ts[j-1],s.T);self.center-=1
 def adj(self,i,g):
  self.move(i);t=np.einsum('asb,btc->astc',self.ts[i],self.ts[i+1]);l,_,_,r=t.shape;t=np.einsum('uvst,astb->auvb',g.reshape(2,2,2,2),t).reshape(2*l,2*r)
  self.check_budget();u,s,v=np.linalg.svd(t,full_matrices=False);self.svds+=1;w=s*s;total=sum(w);rank=len(s)
  # tol is an amplitude error allowance at EACH SVD (zero means exact).
  if self.tol>0:
   for k in range(1,len(s)+1):
    if sum(w[k:])<=self.tol**2*total:rank=k;break
  if self.chi is not None and rank>self.chi and self.strict:
   raise ResourceLimit(dict(aborted=True,reason='rank_cap',**getattr(self,'extra_stats',{}),required_bond=rank,max_bond=self.maxchi,path_error_sum=float(self.error),svds=self.svds,peak_array_bytes=self.peakbytes))
  if self.chi is not None:rank=min(rank,self.chi)
  lost=float(sum(w[rank:])/total);self.error+=np.sqrt(max(0,lost));self.truncations+=int(lost>1e-28)
  s=s[:rank]/np.sqrt(max(1e-300,1-lost));self.ts[i]=u[:,:rank].reshape(l,2,rank);self.ts[i+1]=(s[:,None]*v[:rank]).reshape(rank,2,r);self.center=i+1;self.maxchi=max(self.maxchi,rank);self.peakbytes=max(self.peakbytes,sum(x.nbytes for x in self.ts)+t.nbytes+u.nbytes+v.nbytes)
 def pair(self,i,j,g):
  if i>j:i,j=j,i;g=SWAP@g@SWAP
  for k in range(j-1,i,-1):self.adj(k,SWAP)
  self.adj(i,g)
  for k in range(i+1,j):self.adj(k,SWAP)
 def one(self,i,g):self.ts[i]=np.einsum('st,atb->asb',g,self.ts[i])
 def measure(self,i,rng,forced=None):
  self.move(i);p1=float(np.sum(abs(self.ts[i][:,1,:])**2));b=int(rng.random()<np.clip(p1,0,1)) if forced is None else forced;p=p1 if b else 1-p1
  if p<1e-16:raise ArithmeticError('Unsupported zero probability')
  self.ts[i][:,1-b,:]=0;self.ts[i]/=np.sqrt(p);return b,p
 def vector(self):
  v=self.ts[0]
  for t in self.ts[1:]:v=np.tensordot(v,t,axes=(-1,0))
  # reverse tensor axes to little-endian dense vector
  n=len(self.ts);return v.reshape([2]*n).transpose(list(range(n-1,-1,-1))).ravel()
class MPOMPS(MPS):
 def product_sum(self,terms):
  sites=set().union(*(set(ops) for c,ops in terms));i=min(sites);j=max(sites);K=len(terms)
  self.move(i)
  if i==j:return self.one(i,sum(c*ops.get(i,I) for c,ops in terms))
  for k in range(i,j+1):
   t=self.ts[k];l,d,r=t.shape;parts=[np.einsum('st,atb->asb',ops.get(k,I),t) for c,ops in terms]
   if k==i:self.ts[k]=np.concatenate([c*a for (c,_),a in zip(terms,parts)],axis=2)
   elif k==j:self.ts[k]=np.concatenate(parts,axis=0)
   else:
    z=np.zeros((K*l,d,K*r),complex)
    for a,tpart in enumerate(parts):z[a*l:(a+1)*l,:,a*r:(a+1)*r]=tpart
    self.ts[k]=z
  self.center=j;self.move(i)
  for k in range(i,j):self.adj(k,np.eye(4))
 def pair(self,i,j,g):
  if i>j:i,j=j,i;g=SWAP@g@SWAP
  if j==i+1:return self.adj(i,g)
  a=np.trace(g)/4
  pp=Z if abs(np.trace(np.kron(Z,Z)@g))>1e-12 else X
  b=np.trace(np.kron(pp,pp)@g)/4
  if np.max(abs(g-a*np.eye(4)-b*np.kron(pp,pp)))>1e-10:
   u,s,v=np.linalg.svd(g.reshape(2,2,2,2).transpose(0,2,1,3).reshape(4,4))
   return self.product_sum([(s[k],{i:u[:,k].reshape(2,2),j:v[k].reshape(2,2)}) for k in range(len(s))])
  self.move(i)
  t=self.ts[i];pt=np.einsum('st,atb->asb',pp,t);self.ts[i]=np.concatenate([a*t,b*pt],axis=2)
  for k in range(i+1,j):
   t=self.ts[k];l,d,r=t.shape;z=np.zeros((2*l,d,2*r),complex);z[:l,:,:r]=t;z[l:,:,r:]=t;self.ts[k]=z
  t=self.ts[j];pt=np.einsum('st,atb->asb',pp,t);self.ts[j]=np.concatenate([t,pt],axis=0)
  # Re-establish canonical form after exact MPO application, then compress.
  self.center=j;self.move(i)
  for k in range(i,j):self.adj(k,np.eye(4))

def sample(n,layers,r,eps,rng,chi=None,tol=0,validate=False,physical=False,distribution=False,basis_prune=True,strict=False,ordering=None,mpo=False,error_budget=None,combined_frame=False,combined_physical=False,early=False,max_wall=None,max_cpu=None,compact=False,birth_order=False,per_gate_budget=False,bridge_prune=False,spectator=False,cycle_measure=False):
 if chi is not None and (not isinstance(chi,int) or chi<1):raise ValueError("chi must be a positive integer")
 if tol<0 or (error_budget is not None and error_budget<0):raise ValueError("Error budgets must be nonnegative")
 start=time.perf_counter();cpu_start=time.process_time();records,roots,supports,neigh=plan(n,layers,r,eps,rng);m=(MPOMPS if mpo else MPS)(n,chi,tol,strict);counts={tuple(sorted((u,v))):0 for u in range(n) for v in neigh[u] if u<v};direct=np.zeros(1<<n,complex) if validate else None
 bridge_flips=[[] for _ in records];coherent_count=None;pruned_count=0
 if bridge_prune:
  if not physical:raise ValueError('Bridge pruning currently supports physical representation only')
  from segment_cycle_sampler import graph
  total_q,cycles=graph(n,records);cycmask=0
  for c in cycles:cycmask|=c
  coherent_count=cycmask.bit_count();qidx=0
  for t,(ev,cuts,before,after) in enumerate(records):
   new=[]
   for (u,v),reset,israre,cand in ev:
    if israre:
     keep=(cycmask>>qidx)&1;qidx+=1
     if not keep:
      pruned_count+=1;israre=False
      if rng.random()<B*B:bridge_flips[t].append((u,v))
    new.append(((u,v),reset,israre,cand))
   records[t]=(new,cuts,before,after)
 hidden_births=set();spectator_contacts={};spectator_measurements=0
 if spectator:
  if not physical or bridge_prune or birth_order:raise ValueError('Spectator compiler initially only supports uncombined physical fixed-order mode')
  import importlib.util
  module_path=Path(__file__).resolve().parents[3]/'north_bridge/erased_spectator/compiler.py'
  spec=importlib.util.spec_from_file_location('spectator_compiler',module_path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  compiled=module.compile_plan(n,[[(u,v,2 if reset else 1 if israre else 0) for (u,v),reset,israre,cand in ev] for ev,_,_,_ in records])
  hidden_births={(x['birth'],x['site']) for x in compiled['accepted']}
  spectator_contacts={(x['contact'],tuple(sorted((x['site'],x['target'])))):x['target'] for x in compiled['accepted']}
 m.extra_stats=dict(spectator_contacts=len(spectator_contacts),spectator_measurements=0,spectator_active_measurements=0,pruned_bridge_Q=pruned_count,coherent_Q=coherent_count)
 if max_wall is not None:m.wall_deadline=start+max_wall
 if max_cpu is not None:m.cpu_deadline=cpu_start+max_cpu
 if validate:direct[0]=1
 from ordering import OrderedMPS,choose_order,interaction_weights,last_q_sites
 if cycle_measure:
  from cycle_cuts import schedule
  early_sets,cycle_meta=schedule(n,records);early=True
 else:early_sets=last_q_sites(n,records) if early else None
 order=list(range(n)) if (ordering is None or birth_order) else choose_order(n,records,neigh,ordering,physical,early_sets)
 pos=np.argsort(order);W=interaction_weights(n,records,neigh,physical,basis_prune,early_sets)
 predicted=int(sum(W[u,v]*(abs(int(pos[u])-int(pos[v])) if mpo else 2*abs(int(pos[u])-int(pos[v]))-1) for u in range(n) for v in range(u+1,n)))
 gate_count=int(W.sum()/2)
 if birth_order:
  if not compact or not mpo or combined_frame or combined_physical:raise ValueError("birth_order requires compact sequential MPO")
  predicted=gate_count*(n-1)
 if error_budget is not None:m.tol=error_budget/max(1,predicted)
 if compact:
  from compact import CompactMPS
  m=CompactMPS(m,n,order,W,birth_order,error_budget/max(1,gate_count) if (birth_order or per_gate_budget) and error_budget is not None else None)
 elif ordering is not None:m=OrderedMPS(m,order)
 bornerr=0.;rare=0;resets=0;known=[0]*n;skipped=0
 def phasepair(u,v,theta):
  nonlocal skipped
  if basis_prune and (known[u] is not None or known[v] is not None):
   skipped+=1
   if known[u] is not None and known[v] is not None:return # irrelevant global phase
   if known[v] is not None:u,v=v,u
   m.one(v,np.diag(np.exp(1j*theta*(1-2*known[u])*np.array([1,-1]))))
  else:m.pair(u,v,zz(theta))
 from sampler import bitphase,qgate,project
 for recidx,(ev,cuts,before,after) in enumerate(records):
  for (u,v),reset,israre,cand in ev:
   counts[tuple(sorted((u,v)))]+=1
   contact=spectator_contacts.get((recidx,tuple(sorted((u,v)))))
   if contact is not None:
    if rng.random()<18/25:
     was_active=known[contact] is None
     a,p=m.measure(contact,rng);known[contact]=a;spectator_measurements+=1
     m.extra_stats["spectator_measurements"]+=1;m.extra_stats["spectator_active_measurements"]+=int(was_active)
     if validate:direct,pd=project(direct,contact,a);bornerr=max(bornerr,abs(pd-p))
    else:
     m.one(contact,Z)
     if validate:direct*=1-2*((np.arange(1<<n)>>contact)&1)
   else:
    if physical and not (combined_physical and (reset or israre)):phasepair(u,v,PHI)
    if validate:direct*=bitphase(n,[u,v],PHI)
  for (u,v),reset,israre,cand in ev:
   if not israre:continue
   rare+=1;edges=[(e,k) for e,k in counts.items() if k and (u in e or v in e) and set(e)!={u,v}]
   if combined_frame and not physical:
    if not mpo:raise ValueError('combined_frame needs mpo=True')
    terms=[(A,{u:I,v:I})]
    for bu in [0,1]:
     for bv in [0,1]:
      if (known[u] is not None and known[u]!=bu) or (known[v] is not None and known[v]!=bv):continue
      ou=np.zeros((2,2));ou[1-bu,bu]=1;ov=np.zeros((2,2));ov[1-bv,bv]=1;ops={u:ou,v:ov};c=-1j*B
      for w in (neigh[u]|neigh[v])-{u,v}:
       angle=2*PHI*((1-2*bu)*counts.get(tuple(sorted((u,w))),0)+(1-2*bv)*counts.get(tuple(sorted((v,w))),0))
       if angle==0:continue
       if known[w] is not None:c*=np.exp(1j*angle*(1-2*known[w]))
       else:ops[w]=np.diag(np.exp(1j*angle*np.array([1,-1])))
      terms.append((c,ops))
    m.product_sum(terms);known[u]=None;known[v]=None
   else:
    if not physical:
     for e,k in edges:phasepair(*e,k*PHI)
    m.pair(u,v,Q@zz(PHI) if physical and combined_physical else Q);known[u]=None;known[v]=None
    if not physical:
     for e,k in reversed(edges):phasepair(*e,-k*PHI)
   if validate:direct=qgate(direct,(1<<u)|(1<<v))
  for u,v in bridge_flips[recidx]:
   for site in (u,v):
    m.one(site,X)
    if known[site] is not None:known[site]^=1
    if validate:direct=direct[np.arange(1<<n)^(1<<site)]
  if early:
   for site in sorted(early_sets[recidx]):
    a,p=m.measure(site,rng);known[site]=a
    if validate:direct,pd=project(direct,site,a);bornerr=max(bornerr,abs(pd-p))
  for (u,v),reset,israre,cand in ev:
   if not reset:continue
   resets+=1;aa=[]
   for s in(u,v):
    a,p=m.measure(s,rng);aa.append(a)
    if validate:direct,pd=project(direct,s,a);bornerr=max(bornerr,abs(pd-p))
   bb=[int(rng.integers(2)),int(rng.integers(2))]
   bb=[0 if (recidx,site) in hidden_births else b for site,b in zip((u,v),bb)]
   for s,a,b in zip((u,v),aa,bb):
    known[s]=b
    if a!=b:
     m.one(s,X)
     if validate:direct=direct[np.arange(1<<n)^(1<<s)]
   if not physical:
    for s,a,b in zip((u,v),aa,bb):
     for w in neigh[s]-{u,v}:m.one(w,np.diag(np.exp(1j*counts[tuple(sorted((s,w)))]*PHI*((1-2*a)-(1-2*b))*np.array([1,-1]))))
 if birth_order and m.pair_calls!=gate_count:raise AssertionError(('Pair gate count mismatch',m.pair_calls,gate_count))
 if (m.svds>predicted if (combined_frame or combined_physical or compact or spectator) else m.svds!=predicted):raise AssertionError(('SVD count mismatch',m.svds,predicted))
 stats=dict(spectator_active_measurements=m.extra_stats["spectator_active_measurements"],spectator_contacts=len(spectator_contacts),spectator_measurements=spectator_measurements,pruned_bridge_Q=pruned_count,coherent_Q=coherent_count,pair_gate_bound=gate_count,pair_gate_calls=getattr(m,'pair_calls',None),max_active_legs=getattr(m,'max_active',n),predicted_svds=predicted,per_svd_tolerance=m.tol,skipped_basis_pair_gates=skipped,seconds=time.perf_counter()-start,max_bond=m.maxchi,svds=m.svds,truncations=m.truncations,path_error_sum=m.error,peak_array_bytes=m.peakbytes,rare=rare,resets=resets,born_error=bornerr,max_component=max(map(len,supports.values())))
 if validate or distribution:
  v=m.vector();p=abs(v)**2
  if validate:stats['conditional_TV']=float(sum(abs(p-abs(direct)**2))/2)
  if distribution:
   stats["seconds"]=time.perf_counter()-start
   return p,stats
 result=0
 for s in range(n):b,_=m.measure(s,rng);result|=b<<s
 stats["seconds"]=time.perf_counter()-start
 return result,stats


def safe_sample(*args,**kwargs):
 start=time.perf_counter()
 try:
  x,s=sample(*args,**kwargs);s['aborted']=False;s['seconds']=time.perf_counter()-start;return x,s
 except ResourceLimit as e:
  s=e.args[0];s['seconds']=time.perf_counter()-start;return 0,s
