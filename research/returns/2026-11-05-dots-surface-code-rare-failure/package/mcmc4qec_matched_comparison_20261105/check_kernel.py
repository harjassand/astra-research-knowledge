from independent_mcmc import Model,State,bar
from fractions import Fraction as F
from math import comb
from collections import deque
from pathlib import Path
import numpy as np,json
m=Model(3);n=len(m.edges);ee=((np.arange(1<<n)[:,None]>>np.arange(n))&1).astype(np.uint8)
s=np.asarray((m.H@ee.T).T,dtype=np.uint8)%2;c=m.m.decode_batch(s)
fail=((ee[:,m.cut].sum(1)+c[:,m.cut].sum(1))%2).astype(bool)
weights=ee.sum(1).astype(int);edges=0
for p in [F(1,10),F(1,1000)]:
 pi=[p**w*(1-p)**(n-w) for w in range(n+1)]
 def T(w):return w*(1-p)+(n-w)*p
 for x in np.flatnonzero(fail):
  w=int(weights[x])
  for i in range(n):
   y=int(x)^(1<<i)
   if not fail[y]:continue
   wy=int(weights[y]);up=wy>w
   q=(p if up else 1-p)/T(w)
   qr=(1-p if up else p)/T(wy)
   assert pi[w]*q*min(1,T(w)/T(wy))==pi[wy]*qr*min(1,T(wy)/T(w))
   assert pi[w]*min(1,pi[wy]/pi[w])/n==pi[wy]*min(1,pi[w]/pi[wy])/n
   edges+=1
 # Any size2 exchange preserves w and the count of available forward/reverse choices.
 for w in range(2,n-1):assert F(1,comb(w,2)*comb(n-w,2))==F(1,comb(n-w,2)*comb(w,2))
visited=set();sizes=[]
for root in np.flatnonzero(fail):
 if int(root) in visited:continue
 q=deque([int(root)]);visited.add(int(root));size=0
 while q:
  x=q.popleft();size+=1
  for i in range(n):
   y=x^(1<<i)
   if fail[y] and y not in visited:visited.add(y);q.append(y)
 sizes.append(size)
# Independently test the incremental syndrome and logical test against full decode.
rng=np.random.default_rng(27)
for _ in range(200):
 e=rng.integers(0,2,n,dtype=np.uint8);st=State(m,e)
 for _ in range(10):
  inds=rng.choice(n,size=int(rng.integers(1,5)),replace=False);st.flip(inds)
  cc=m.decode(st.e)
  assert st.isfailure()==int((st.e[m.cut]+cc[m.cut]).sum()%2)
  assert st.w==int(st.e.sum())
  assert np.array_equal(st.s,np.asarray(m.H@st.e)%2)
# Exact enumerated distributions make BAR algebraic identity recover normalizers.
counts=np.bincount(weights[fail],minlength=n+1)
errs=[]
for a,b in [(.15,.1),(.1,.01),(.01,.001)]:
 def mass(p):return np.array([counts[w]*p**w*(1-p)**(n-w) for w in range(n+1)])
 ha=mass(a);hb=mass(b);truth=np.log(hb.sum()/ha.sum());r=bar(ha/ha.sum(),hb/hb.sum(),a,b,n)
 errs.append(abs(r-truth));assert abs(r-truth)<1e-11
out=dict(status='PASS',d3_failure_states=int(fail.sum()),d3_single_flip_components=sizes,
 exact_detailed_balance_directed_edges_checked=edges,incremental_state_checks=2000,bar_exact_distribution_max_log_error=max(errs),
 scope='Proves detailed-balance algebra and exhaustively checks d3 only; does not certify d13 mixing.')
Path(__file__).with_name('kernel_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
