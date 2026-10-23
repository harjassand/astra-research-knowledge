import numpy as np,json,time
from pathlib import Path
rng=np.random.default_rng(20261023)
out=[]
for n in [4,8,16,32]:
 t=time.perf_counter();d=8
 pairs=[(i,j) for i in range(n) for j in range(i+1,n)];ind={p:k for k,p in enumerate(pairs)};m=len(pairs)
 hs=[];maps=[];signs=[]
 for s in range(d):
  order=rng.permutation(n);p=np.empty(n,dtype=int);sg=np.empty(n,dtype=np.int64)
  for i,j in order.reshape(-1,2):
   v=int(rng.choice([-1,1]));p[i]=j;p[j]=i;sg[i]=sg[j]=v
  h=np.zeros((n,n));h[np.arange(n),p]=sg;hs.append(h)
  mp=[];ss=[]
  for i,j in pairs:
   a,b=int(p[i]),int(p[j]);mp.append(ind[(min(a,b),max(a,b))]);ss.append(int(sg[i]*sg[j]*(1 if a<b else -1)))
  maps.append(np.array(mp));signs.append(np.array(ss,dtype=np.int64))
 Adj=np.zeros((m,m),dtype=np.int64)
 for p,s in zip(maps,signs):Adj[np.arange(m),p]+=s
 assert np.array_equal(Adj,Adj.T)
 ev=np.linalg.eigvalsh(Adj/d);P=np.eye(m,dtype=np.int64);cert=None
 for k in range(1,21):
  P=sum((sg[:,None]*P[mp,:] for mp,sg in zip(maps,signs)),start=np.zeros_like(P))
  rowmax=max(int(x) for x in np.abs(P).sum(axis=1))
  assert rowmax<=d**k
  if rowmax<=7**k:
   cert={'power':k,'max_abs_row_sum_integer':rowmax,'denominator':d**k,'target_rhs':7**k,'rho_upper':7/8,'g_lower':1/4,'s0_lower':1/2};break
 row={'n':n,'d':d,'skew_dim':m,'max_eigen_channel':float(ev[-1]),'spectral_radius':float(max(abs(ev))),'certificate':cert,'seconds':time.perf_counter()-t,'H':[h.astype(int).tolist() for h in hs]};out.append(row)
 print(json.dumps({k:v for k,v in row.items() if k!='H'}),flush=True)
(Path(__file__).resolve().parent/'expander_designs.json').write_text(json.dumps(out,indent=2)+'\n')
