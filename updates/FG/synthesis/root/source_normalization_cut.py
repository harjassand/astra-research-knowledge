"""Exact finite retained-source envelope compiler; standard library only.

No hidden bath enumeration. The represented retained matrix and its dense
positive Green kernel remain supplied/charged. This implements an application
of established fractional programming and attractive graph-cut machinery.
"""
from fractions import Fraction as F
from collections import deque
from itertools import product
from pathlib import Path
import argparse,json,random,time,platform

def inverse(a):
 n=len(a);m=[[F(z) for z in a[i]]+[F(int(i==j)) for j in range(n)] for i in range(n)]
 for j in range(n):
  p=next(i for i in range(j,n) if m[i][j]);m[j],m[p]=m[p],m[j];v=m[j][j]
  m[j]=[z/v for z in m[j]]
  for i in range(n):
   if i!=j:
    c=m[i][j];m[i]=[z-c*y for z,y in zip(m[i],m[j])]
 return [row[n:] for row in m]
def mv(a,b):return [sum(x*y for x,y in zip(row,b)) for row in a]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def ratio(g,s):return dot(s,mv(g,s))/sum(s)

def mincut(cap,source,sink):
 """Exact Edmonds-Karp, then greatest source-side minimum cut."""
 n=len(cap);r=[row.copy() for row in cap];flow=F(0);augmentations=0
 while True:
  prev=[-1]*n;prev[source]=source;q=deque([source])
  while q and prev[sink]<0:
   i=q.popleft()
   for j in range(n):
    if r[i][j]>0 and prev[j]<0:prev[j]=i;q.append(j)
  if prev[sink]<0:break
  path=[];j=sink
  while j!=source:i=prev[j];path.append((i,j));j=i
  step=min(r[i][j] for i,j in path);flow+=step;augmentations+=1
  for i,j in path:r[i][j]-=step;r[j][i]+=step
 # A greatest closed residual source set is the complement of vertices that
 # can reach the sink. It is a min cut for any completed maximum flow.
 reach={sink};q=deque([sink])
 while q:
  j=q.popleft()
  for i in range(n):
   if r[i][j]>0 and i not in reach:reach.add(i);q.append(i)
 side=set(range(n))-reach;assert source in side and sink not in side
 cut=sum(cap[i][j] for i in side for j in range(n) if j not in side)
 assert flow==cut
 return flow,side,augmentations

def maximize_source(g,ell,u):
 n=len(ell);assert len(u)==n and len(g)==n and all(len(row)==n for row in g)
 assert all(g[i][j]==g[j][i] for i in range(n) for j in range(n))
 assert all(0<x<=y for x,y in zip(ell,u));assert all(z>=0 for row in g for z in row)
 ids=[i for i in range(n) if u[i]>ell[i]];d=[u[i]-ell[i] for i in ids];m=len(ids)
 ge=mv(g,ell);q0=dot(ell,ge);z0=sum(ell)
 b=[[d[i]*d[j]*g[ids[i]][ids[j]] if i!=j else F(0) for j in range(m)] for i in range(m)]
 alpha=[2*d[i]*ge[ids[i]]+d[i]**2*g[ids[i]][ids[i]]+sum(b[i]) for i in range(m)]
 t=F(0);history=[];last=set(range(m))
 for iteration in range(m+2):
  src=m;snk=m+1;cap=[[F(0) for _ in range(m+2)] for _ in range(m+2)]
  for i in range(m):
   cap[src][i]=alpha[i];cap[i][snk]=t*d[i]
   for j in range(m):cap[i][j]=b[i][j]
  cut,side,aug=mincut(cap,src,snk);active=side&set(range(m));assert active<=last
  s=ell.copy()
  for i in active:s[ids[i]]=u[ids[i]]
  excess=q0-t*z0+sum(alpha)-cut
  assert excess==dot(s,mv(g,s))-t*sum(s)
  assert excess>=0
  history.append(dict(threshold=str(t),active_indices=[ids[i] for i in sorted(active)],excess=str(excess),augmentations=aug))
  if excess==0:return t,s,history
  new_t=ratio(g,s);assert new_t>t;t=new_t;last=active
 raise AssertionError('Nested-set iteration bound exceeded')

def minimize_trial(ell,u,v,energy):
 # For optimum threshold t, choose u exactly where 2v_i<t. Sorting these
 # breakpoints leaves at most n+1 prefix profiles, including tied cases.
 order=sorted(range(len(ell)),key=lambda i:2*v[i]);s=ell.copy()
 val=(2*dot(s,v)-energy)/sum(s);best=s.copy()
 for i in order:
  s[i]=u[i];r=(2*dot(s,v)-energy)/sum(s)
  if r<val:val=r;best=s.copy()
 return val,best

def east_envelope(feature,R):
 n=4;N=1<<n;q=F(1,26);eps=F(1,10000)
 mass=[q**g.bit_count()*(1-q)**(n-g.bit_count()) for g in range(N)]
 indicator={'all_open':lambda g:g==N-1,'first_open':lambda g:g&1,'all_closed':lambda g:g==0}[feature]
 wl=[F(1)]*N;wu=[F(1)+(R-1)*int(bool(indicator(g))) for g in range(N)]
 def form(w):
  a=[[F(0) for _ in range(N)] for _ in range(N)]
  for g in range(N):
   a[g][g]+=mass[g]*w[g]*q*(1 if (g>>(n-1))&1 else eps)
   for i in range(n):
    if (g>>i)&1:continue
    h=g|(1<<i);c=mass[g]*q*(1 if i==0 or (g>>(i-1))&1 else eps)*min(w[g],w[h])
    a[g][g]+=c;a[h][h]+=c;a[g][h]-=c;a[h][g]-=c
  return a
 lo=[x*y for x,y in zip(mass,wl)];hi=[x*y for x,y in zip(mass,wu)]
 gm=inverse(form(wl));gp=inverse(form(wu));v=mv(gp,lo);energy=dot(lo,v)
 old_l=energy/sum(hi);old_u=dot(hi,mv(gm,hi))/sum(lo)
 upper,profile,history=maximize_source(gm,lo,hi);lower,lprofile=minimize_trial(lo,hi,v,energy)
 assert old_l<=lower<=upper<=old_u
 return dict(feature=feature,R=R,retained_states=N,uncertain_sources=sum(x<y for x,y in zip(lo,hi)),
  old_lower=old_l,old_upper=old_u,new_lower=lower,new_upper=upper,old_ratio=old_u/old_l,new_ratio=upper/lower,
  upper_source=profile,lower_source=lprofile,cut_calls=len(history),cut_history=history,hidden_states_constructed=0)

def serial(o):
 if isinstance(o,F):return dict(exact=str(o),approximate=float(o))
 if isinstance(o,list):return [serial(x) for x in o]
 if isinstance(o,dict):return {str(k):serial(v) for k,v in o.items()}
 return o

def main(out):
 st=time.monotonic();rng=random.Random(20261014);checks=0;examples=[]
 for n in range(1,9):
  for case in range(10):
   a=[[F(0) for _ in range(n)] for _ in range(n)]
   for i in range(n):a[i][i]=F(rng.randint(1,9),rng.randint(1,9))
   for i in range(n):
    for j in range(i):
     c=F(rng.randint(0,9),rng.randint(1,9));a[i][i]+=c;a[j][j]+=c;a[i][j]-=c;a[j][i]-=c
   g=inverse(a);ell=[F(rng.randint(1,9),rng.randint(1,9)) for _ in range(n)]
   u=[z+F(rng.randint(0,9),rng.randint(1,9)) for z in ell]
   val,s,history=maximize_source(g,ell,u)
   brute=max(ratio(g,[u[i] if z[i] else ell[i] for i in range(n)]) for z in product([0,1],repeat=n))
   assert val==brute;checks+=1
   v=mv(g,ell);energy=dot(ell,v);lower,_=minimize_trial(ell,u,v,energy)
   brute_l=min((2*dot([u[i] if z[i] else ell[i] for i in range(n)],v)-energy)/sum(u[i] if z[i] else ell[i] for i in range(n)) for z in product([0,1],repeat=n))
   assert lower==brute_l;checks+=1
   assert len(history)<=sum(x<y for x,y in zip(ell,u))+2;checks+=1
   if case==0:examples.append(dict(n=n,cut_calls=len(history),upper=val,lower=lower))
 # Positivity preservation is essential for the cut reduction, not merely SPD.
 negative=[[F(2),F(-1)],[F(-1),F(2)]]
 try:maximize_source(negative,[F(1),F(1)],[F(2),F(2)])
 except AssertionError:checks+=1
 else:raise AssertionError('Negative kernel must be rejected')
 closure=[east_envelope(f,R) for f in ['all_open','first_open','all_closed'] for R in [3,100]]
 sharp=[]
 for R in [3,10,100]:
  for n in [10,1000,1000000]:
   delta=F(1,n);T=F(n)
   base=((1+delta)**2+T)/(1+delta)
   changed=((1+R*delta)**2+R*R*T)/(1+R*delta)
   rr=changed/base;assert 1<=rr<R*R;checks+=1
   lower=((R+delta)**2+T)/(R*(R+delta));lr=lower/base
   assert F(1,R*R)<lr<=1;assert changed/lower<R**4;checks+=2
   sharp.append(dict(R=R,delta=delta,T=T,ratio=rr,relative_to_R_squared=rr/(R*R),
      lower_ratio=lr,lower_relative_to_inverse_R_squared=lr*R*R,
      width_ratio=changed/lower,width_relative_to_R_fourth=(changed/lower)/R**4))
 report=dict(status='PASS',python=platform.python_version(),exact_assertions=checks,random_graphs=80,examples=examples,
  conditional_envelope_comparisons=closure,R_squared_sharpness_family=sharp,seconds=time.monotonic()-st,
  scope='Exact finite represented retained-source relaxation. Does not acquire global physical envelopes or a128-coordinate Green matrix. Historical novelty/external validation UNKNOWN.')
 out.mkdir(parents=True,exist_ok=True);(out/'SOURCE_NORMALIZATION_CUT_RESULTS.json').write_text(json.dumps(serial(report),indent=2)+'\n')
 print(json.dumps(serial(dict(status=report['status'],exact_assertions=checks,random_graphs=80,seconds=report['seconds'],
    closure=[{k:x[k] for k in ['feature','R','old_ratio','new_ratio','cut_calls']} for x in closure])),indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True,type=Path);main(p.parse_args().output_dir)
