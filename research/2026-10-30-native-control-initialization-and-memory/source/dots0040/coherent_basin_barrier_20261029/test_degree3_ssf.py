import sys,numpy as np,itertools,json,random
sys.path.insert(0,'producer-workspace/online_ssf_stress_20261029')
from stress import syndrome,choose
n=5;m=5;N=n*n+m*m
H=[[int((j-i)%n in (0,1,3)) for j in range(n)] for i in range(m)]
HX=[];HZ=[]
for a in range(m):
 for b in range(n):
  HX.append(sum(H[a][j]<<(j*n+b) for j in range(n))|sum(H[j][b]<<(n*n+a*m+j) for j in range(m)))
for a in range(n):
 for b in range(m):
  HZ.append(sum(H[b][j]<<(a*n+j) for j in range(n))|sum(H[j][a]<<(n*n+j*m+b) for j in range(m)))
assert all((x&z).bit_count()%2==0 for x in HX for z in HZ)
cols=[syndrome(1<<q,HZ) for q in range(N)];families=[]
for g in HX:
 supp=[q for q in range(N) if g>>q&1];family=[]
 for mask in range(1,1<<len(supp)):
  f=sum(1<<q for j,q in enumerate(supp) if mask>>j&1);sf=syndrome(f,HZ);w=sf.bit_count()
  if sf and 2*w>=3*f.bit_count():family.append((f,sf,w))
 families.append(family)
M=len(HZ);adj=[0]*M
for c in cols:
 for i in range(M):
  if c>>i&1:adj[i]|=c^(1<<i)
animals={1<<i for i in range(M)};front=animals.copy()
for size in range(2,5):
 nxt=set()
 for A in front:
  neigh=0
  for i in range(M):
   if A>>i&1:neigh|=adj[i]
  neigh&=~A
  while neigh:
   bit=neigh&-neigh;neigh-=bit;nxt.add(A|bit)
 animals|=nxt;front=nxt
AA=list(animals);sizes=np.array([x.bit_count() for x in AA]);theta=.03;a=.3
cache={}
def VW(s):
 if s not in cache:
  holes=sizes-np.array([(s&A).bit_count() for A in AA]);f=np.exp(a*sizes)*theta**holes;cache[s]=(f.sum(),f@sizes)
 return cache[s]
rng=random.Random(29);rows=[];positive_move=None
for trial in range(500):
 weight=rng.randrange(1,9);qs=rng.sample(range(N),weight);e=sum(1<<q for q in qs);s=syndrome(e,HZ);v,w=VW(s);dr=0.;moves=0
 for h,fam in enumerate(families):
  mv=choose(s,fam)
  if mv:
   f,sf,dec=mv;dv=VW(s^sf)[0]-v;dr+=dv;moves+=1
   if dv>1e-8 and positive_move is None:positive_move=dict(error=e,weight=weight,syndrome=s,hub=h,flip=f,syndrome_delta=sf,syndrome_decrease=dec,V_before=v,V_after=VW(s^sf)[0],syndrome_weight_before=s.bit_count(),syndrome_weight_after=(s^sf).bit_count())
 rows.append(dict(error=e,input_weight=weight,syndrome=s,syndrome_weight=s.bit_count(),drift=dr,W=w,ratio=dr/w,moves=moves))
print(json.dumps(dict(control='degree-3 circulant HGP; expansion constants NOT certified',H=H,N=N,checks=M,animals=len(AA),theta=theta,a=a,ell=4,trials=len(rows),positive_move=positive_move,max_drift_row=max(rows,key=lambda r:r['ratio']),positive_total_drifts=sum(r['drift']>1e-8 for r in rows)),indent=2,default=lambda x: x.item()))
