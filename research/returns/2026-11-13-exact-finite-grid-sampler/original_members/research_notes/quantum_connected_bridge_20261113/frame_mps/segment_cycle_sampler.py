"""Exact-arithmetic construction; NumPy small-system validation implementation."""
import numpy as np,json,sys,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'frame_sampler'))
from sampler import plan,UF,bitphase,PHI,A,B

def graph(n,records):
 uf=UF(n);cur=list(range(n));adj=[[] for _ in range(n)];cycles=[];qidx=0
 for ev,_,_,_ in records:
  for(u,v),reset,rare,cand in ev:
   if not rare:continue
   a,b=cur[u],cur[v]
   if uf.root(a)!=uf.root(b):uf.union(a,b);adj[a].append((b,qidx));adj[b].append((a,qidx))
   else:
    stack=[a];prev={a:None}
    while stack and b not in prev:
     z=stack.pop()
     for w,e in adj[z]:
      if w not in prev:prev[w]=(z,e);stack.append(w)
    mask=1<<qidx;z=b
    while z!=a:z,e=prev[z];mask^=1<<e
    cycles.append(mask)
   qidx+=1
  for(u,v),reset,rare,cand in ev:
   if reset:
    for s in(u,v):cur[s]=uf.add();adj.append([])
 return qidx,cycles

def replay(n,records,prep,z):
 bits=[0]*n;amp=1+0j;qi=0;ri=0;record=[]
 for ev,_,_,_ in records:
  for(u,v),reset,rare,cand in ev:amp*=(3+4j*(1-2*bits[u])*(1-2*bits[v]))/5
  for(u,v),reset,rare,cand in ev:
   if rare:
    f=(z>>qi)&1;qi+=1;amp*=(-1j*B if f else A)
    if f:bits[u]^=1;bits[v]^=1
  for(u,v),reset,rare,cand in ev:
   if reset:
    record.extend([bits[u],bits[v]]);bits[u],bits[v]=prep[ri];ri+=1
 record.extend(bits);return amp,tuple(record),sum(b<<s for s,b in enumerate(bits))

def coset(z,cycles):
 vals=[z]
 for c in cycles:vals += [x^c for x in vals]
 return vals

def sample_fixed(n,records,prep,rng,max_attempts=None):
 m,cycles=graph(n,records);K=len(cycles);tries=0
 while max_attempts is None or tries<max_attempts:
  tries+=1;z=sum(int(rng.random()<B*B)<<j for j in range(m));amplitudes=[];record=None;final=None
  for h in coset(z,cycles):
   a,y,f=replay(n,records,prep,h)
   if record is not None and record!=y:raise AssertionError('Cycle changed measured record')
   amplitudes.append(a);record=y;final=f
  p0=sum(abs(a)**2 for a in amplitudes);p=abs(sum(amplitudes))**2
  if rng.random()<min(1,p/(2**K*p0)):return final,dict(attempts=tries,cycle_rank=K,aborted=False)
 return 0,dict(attempts=tries,cycle_rank=K,aborted=True)

def dense(n,records,prep,prune=False):
 m,cycles=graph(n,records);cycmask=0;qi=0
 for c in cycles:cycmask|=c
 d=1<<n;x=np.arange(d);rho=np.zeros((d,d),complex);rho[0,0]=1;ri=0
 for ev,_,_,_ in records:
  for(u,v),reset,rare,cand in ev:
   ph=bitphase(n,[u,v],PHI);rho=ph[:,None]*rho*ph.conj()[None,:]
  for(u,v),reset,rare,cand in ev:
   if rare:
    perm=x^((1<<u)|(1<<v));cross=not prune or ((cycmask>>qi)&1);qi+=1;rho=A*A*rho+B*B*rho[np.ix_(perm,perm)]+(1j*A*B*(rho[:,perm]-rho[perm,:]) if cross else 0)
  for(u,v),reset,rare,cand in ev:
   if reset:
    mask=(1<<u)|(1<<v);rest=x[(x&mask)==0];sh=[0,1<<u,1<<v,mask];block=sum(rho[np.ix_(rest+s,rest+s)] for s in sh);b,c=prep[ri];ri+=1;dest=(b<<u)|(c<<v);rho=np.zeros_like(rho);rho[np.ix_(rest+dest,rest+dest)]=block
 return np.diag(rho).real
if __name__=='__main__':
 rows=[]
 for seed in range(40):
  rng=np.random.default_rng(seed);rec,*_=plan(4,[[(0,1),(2,3)],[(0,2),(1,3)]]*4,.2,.4,rng);m,cy=graph(4,rec);R=sum(reset for ev,*_ in rec for e,reset,*_ in ev);prep=[tuple(map(int,rng.integers(2,size=2))) for _ in range(R)];sums=collections.defaultdict(complex);p0=collections.defaultdict(float);last={}
  for z in range(1<<m):
   a,y,f=replay(4,rec,prep,z);sums[y]+=a;p0[y]+=abs(a)**2;last[y]=f
  prob=np.zeros(16)
  for y,a in sums.items():prob[last[y]]+=abs(a)**2
  oracle=dense(4,rec,prep);ratios=[abs(sums[y])**2/p0[y] for y in sums];rows.append(dict(seed=seed,Q=m,K=len(cy),TV=float(sum(abs(prob-oracle))/2),total=float(sum(prob)),envelope_ratio=max(ratios),envelope=2**len(cy),forest_delta=max(abs(abs(sums[y])**2-p0[y]) for y in sums) if not cy else None))
 Path(__file__).with_name('segment_cycle_validation.json').write_text(json.dumps(rows,indent=2));print('40cases maxTV',max(s['TV'] for s in rows),'Krange',sorted(set(s['K'] for s in rows)),'forests',sum(s['K']==0 for s in rows))
