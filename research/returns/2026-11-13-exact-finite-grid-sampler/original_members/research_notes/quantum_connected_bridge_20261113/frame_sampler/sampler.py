"""Small-circuit diagonal-frame trajectory sampler. Floating reference implementation."""
import numpy as np,time
PHI=np.arctan2(4.,3.); A=12/13; B=5/13
class UF:
 def __init__(self,n):self.p=list(range(n))
 def add(self):self.p.append(len(self.p));return len(self.p)-1
 def root(self,x):
  while self.p[x]!=x:self.p[x]=self.p[self.p[x]];x=self.p[x]
  return x
 def union(self,x,y):self.p[self.root(x)]=self.root(y)
def bitphase(n,e,theta):
 x=np.arange(1<<n);z=np.ones(len(x),int)
 for i in e:z*=1-2*((x>>i)&1)
 return np.exp(1j*theta*z)
def qgate(v,mask):return A*v-1j*B*v[np.arange(len(v))^mask]
def project(v,i,b):
 keep=((np.arange(len(v))>>i)&1)==b;p=float(np.sum(abs(v[keep])**2))
 if p<1e-25:raise ArithmeticError('Zero-probability forced outcome')
 z=v.copy();z[~keep]=0;return z/np.sqrt(p),p

def plan(n,layers,r,epsilon,rng):
 if not(0<r<1 and 0<=epsilon<=1-r):raise ValueError('Invalid channel probabilities')
 neigh=[set() for _ in range(n)]
 for lay in layers:
  used=set()
  for u,v in lay:
   if u==v or min(u,v)<0 or max(u,v)>=n or u in used or v in used:raise ValueError('Layers must be disjoint valid pairs')
   used|={u,v};neigh[u].add(v);neigh[v].add(u)
 p=r/2;r0=2*p-p*p;extra=(r-r0)/(1-r0);k=epsilon/(1-r)
 uf=UF(n);site=list(range(n));cur=list(range(n));records=[]
 for lay in layers:
  matched=set(sum(([u,v] for u,v in lay),[]));cuts={i for i in matched if rng.random()<p};ev=[];before=cur.copy()
  for e in lay:
   u,v=e;reset=(u in cuts or v in cuts)
   if not reset:reset=rng.random()<extra
   cand=rng.random()<k;rare=cand and not reset
   if cand:
    star={u,v}|neigh[u]|neigh[v];ids=[cur[i] for i in star]
    for a in ids[1:]:uf.union(ids[0],a)
   ev.append((e,reset,rare,cand))
  for i in cuts:cur[i]=uf.add();site.append(i)
  records.append((ev,cuts,before,cur.copy()))
 roots=[uf.root(i) for i in range(len(site))];supports={}
 for j,s in enumerate(site):supports.setdefault(roots[j],set()).add(s)
 return records,roots,{c:sorted(s) for c,s in supports.items()},neigh

def sample(n,layers,r,epsilon,rng,cap=None,validate=False,distribution=False):
 start=time.perf_counter();records,roots,supports,neigh=plan(n,layers,r,epsilon,rng)
 largest=max(map(len,supports.values()));stats={'max_component_physical_sites':largest,'components':len(supports),'segments':len(roots),'aborted':False,'measurement_probability_error':0.,'actual_rare':0,'actual_resets':0}
 if cap is not None and largest>cap:
  stats['aborted']=True;stats['seconds']=time.perf_counter()-start
  return (np.eye(1,1<<n,0).ravel() if distribution else 0),stats
 loc={c:{s:i for i,s in enumerate(sites)} for c,sites in supports.items()}
 states={c:np.eye(1,1<<len(sites),0,dtype=complex).ravel() for c,sites in supports.items()};cur=list(range(n));counts={tuple(sorted((u,v))):0 for u in range(n) for v in neigh[u] if u<v}
 stats['allocated_complex_amplitudes']=sum(map(len,states.values()));stats['amplitude_storage_bytes']=16*stats['allocated_complex_amplitudes']
 direct=np.eye(1,1<<n,0,dtype=complex).ravel() if validate else None
 def phase(site,theta):
  c=roots[cur[site]];states[c]*=bitphase(len(supports[c]),[loc[c][site]],theta)
 def measure(site):
  c=roots[cur[site]];i=loc[c][site];prob1=float(np.sum(abs(states[c][((np.arange(len(states[c]))>>i)&1)==1])**2));b=int(rng.random()<min(1,max(0,prob1)));states[c],p=project(states[c],i,b);return b,p
 def flip(c,s):states[c]=states[c][np.arange(len(states[c]))^(1<<loc[c][s])]
 for ev,cuts,before,after in records:
  for (u,v),_,_,_ in ev:
   counts[tuple(sorted((u,v)))]+=1
   if validate:direct*=bitphase(n,[u,v],PHI)
  # All dressed rare operations before reset instruments in the common layer frame.
  for (u,v),reset,rare,cand in ev:
   if not rare:continue
   stats['actual_rare']+=1;c=roots[cur[u]]
   active_edges=[(e,m) for e,m in counts.items() if m and (u in e or v in e)]
   for e,m in active_edges:
    assert all(roots[cur[s]]==c for s in e)
    states[c]*=bitphase(len(supports[c]),[loc[c][s] for s in e],m*PHI)
   states[c]=qgate(states[c],(1<<loc[c][u])|(1<<loc[c][v]))
   for e,m in active_edges:states[c]*=bitphase(len(supports[c]),[loc[c][s] for s in e],-m*PHI)
   if validate:direct=qgate(direct,(1<<u)|(1<<v))
  for (u,v),reset,rare,cand in ev:
   if not reset:continue
   stats['actual_resets']+=1;aa=[]
   for s in (u,v):
    z,prob=measure(s);aa.append(z)
    if validate:
     direct,pd=project(direct,s,z);stats['measurement_probability_error']=max(stats['measurement_probability_error'],abs(prob-pd))
   bb=[int(rng.integers(2)),int(rng.integers(2))]
   for s,a,b in zip((u,v),aa,bb):
    old=roots[cur[s]];new=roots[after[s]]
    if old==new:
     if a!=b:flip(old,s)
    else:
     if a:flip(old,s)
     # Previously used register at this site was cleared at its prior departure.
     idx=np.arange(len(states[new]));bad=float(np.sum(abs(states[new][((idx>>loc[new][s])&1)==1])**2))
     if bad>1e-10:raise AssertionError('Future/live register was not a fresh zero')
     if b:flip(new,s)
    cur[s]=after[s]
    if validate and a!=b:direct=direct[np.arange(1<<n)^(1<<s)]
   for s,a,b in zip((u,v),aa,bb):
    for w in neigh[s]-{u,v}:
     m=counts[tuple(sorted((s,w)))];phase(w,m*PHI*((1-2*a)-(1-2*b)))
  assert cur==after
 # Construct small global conditional distribution only when requested for testing.
 if distribution or validate:
  frame=np.ones(1<<n,complex);xx=np.arange(1<<n)
  for c,sites in supports.items():
   ix=np.zeros(1<<n,int)
   for s in sites:
    if roots[cur[s]]==c:ix|=((xx>>s)&1)<<loc[c][s]
   frame*=states[c][ix]
  if abs(np.sum(abs(frame)**2)-1)>1e-9:raise AssertionError('Component product lost normalization')
  if validate:
   physical=frame.copy()
   for e,m in counts.items():physical*=bitphase(n,e,m*PHI)
   stats['trajectory_infidelity']=max(0.,float(1-abs(np.vdot(physical,direct))**2));stats['conditional_output_max_error']=float(max(abs(abs(frame)**2-abs(direct)**2)))
  result=abs(frame)**2 if distribution else int(rng.choice(1<<n,p=abs(frame)**2))
 else:
  result=0
  for s in range(n):b,_=measure(s);result|=b<<s
 stats['seconds']=time.perf_counter()-start
 return result,stats

def exact_density(n,layers,r,epsilon):
 d=1<<n;x=np.arange(d);rho=np.zeros((d,d),complex);rho[0,0]=1
 for lay in layers:
  for u,v in lay:
   ph=bitphase(n,[u,v],PHI);a=ph[:,None]*rho*ph.conj()[None,:];mask=(1<<u)|(1<<v);perm=x^mask
   rare=A*A*a+B*B*a[np.ix_(perm,perm)]+1j*A*B*(a[:,perm]-a[perm,:])
   reset=np.zeros_like(rho);rest=[z for z in x if z&mask==0];shifts=[0,1<<u,1<<v,mask]
   for i in rest:
    for j in rest:
     z=sum(a[i+s,j+s] for s in shifts)/4
     for s in shifts:reset[i+s,j+s]=z
   rho=(1-r-epsilon)*a+epsilon*rare+r*reset
 return np.diag(rho).real
