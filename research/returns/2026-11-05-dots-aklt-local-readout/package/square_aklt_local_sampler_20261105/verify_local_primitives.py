"""Complete finite-graph routing audit and high-precision time tests."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import random,time,json
import mpmath as mp
from local_birth_oracle import LocalLoopBirthSampler,D,edge,canonical
from exact_lazy_time import ExactTime,LazyExp,log_bounds
HERE=Path(__file__).resolve().parent

def catalog(w,h):
 # Every even edge subset is uniquely a GF(2) sum of bounded face boundaries.
 # Every degree-four vertex has exactly three pairings; trace all routed cycles.
 faces=[]
 for x in range(w-1):
  for y in range(h-1):
   p=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
   faces.append({edge(p[i],p[(i+1)%4]) for i in range(4)})
 out={};configs=0
 for mask in range(1<<len(faces)):
  es=set()
  for k,face in enumerate(faces):
   if mask>>k&1:es^=face
  adj={}
  for a,b in es:adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
  four=[v for v in adj if len(adj[v])==4];base={}
  for v,ns in adj.items():
   ns.sort()
   if len(ns)==2:base[v]={ns[0]:ns[1],ns[1]:ns[0]}
  for choice in product(range(3),repeat=len(four)):
   configs+=1;pairs=base.copy()
   for v,c in zip(four,choice):
    ns=adj[v];j=c+1;a,b=[k for k in[1,2,3] if k!=j]
    pairs[v]={ns[0]:ns[j],ns[j]:ns[0],ns[a]:ns[b],ns[b]:ns[a]}
   unused=es.copy()
   while unused:
    a,b=min(unused);first=(a,b);p=[]
    while True:
     p.append(a);unused.remove(edge(a,b));a,b=b,pairs[b][a]
     if(a,b)==first:break
    q=canonical(p);r=sum(n==2 for n in Counter(q).values());out[q]=F(3)**(1-len(q))*F(3,5)**r
 return out,configs

def rooted_raw_probability(s,p):
 # Actual oracle path probability, including direction, true contact thinning;
 # excluding root choice and reciprocal K visit count.
 ds=tuple(D.index((p[(k+1)%len(p)][0]-p[k][0],p[(k+1)%len(p)][1]-p[k][1])) for k in range(len(p)))
 ori=ds[0];nd=tuple((d-ori)%4 for d in ds);n=len(ds)
 opts={tuple(h):(i,r,k) for k,(i,h,r) in enumerate(s.options)}
 state,rm,oi=opts[nd if n<s.m else nd[:s.m]];prev=s.cumulative[oi-1] if oi else 0
 prob=F(s.cumulative[oi]-prev,4*s.total);N=len(s.states)
 if state>=0:
  x=sum(D[d][0] for d in ds[:s.m]);y=sum(D[d][1] for d in ds[:s.m])
  for dw in ds[s.m:]:
   d=(dw-ori)%4;j=s.directions[state].index(d);tar=int(s.to[state,j]);ww=int(s.w[state,j]);no=(ori+s.states[state][1])%4
   nx=x+D[dw][0];ny=y+D[dw][1]
   prob*=F(ww*int(s.g[no*N+tar,nx%s.side,ny%s.side]),15*int(s.g[ori*N+state,x%s.side,y%s.side]))
   rm+=ww==3;ori=no;state=tar;x,y=nx,ny
  prob*=F(s.scale,int(s.g[ori*N+state,x%s.side,y%s.side]))
 rt=sum(n==2 for n in Counter(p).values());assert rm<=rt
 return prob*F(3,5)**(rt-rm)

def verify_birth(w,h,s):
 loops,configs=catalog(w,h);queries=[{(0,0)},{(w//2,h//2)},{(0,0),(w-1,h-1)},{(x,y) for x in range(w) for y in range(h)}]
 probabilities={Kidx:F(0) for Kidx in range(len(queries))};counts=[0]*len(queries);encodings=0;cache={}
 for p,a in loops.items():
  raw=[]
  for q in(p,p[::-1]):
   for k in range(len(p)):
    r=q[k:]+q[:k];shape=tuple((x-r[0][0],y-r[0][1]) for x,y in r)
    if shape not in cache:cache[shape]=rooted_raw_probability(s,r)
    prob=cache[shape];assert prob==a/(3*s.rate_per_vertex)
    raw.append((r[0],prob));encodings+=1
  for z,K in enumerate(queries):
   visits=sum(v in K for v in p)
   if visits:
    got=sum(prob for root,prob in raw if root in K)/len(K)/visits
    assert got*s.rate(K)==a,(p,K,got,a)
    probabilities[z]+=got;counts[z]+=1
 return {'box':[w,h],'complete_routed_configuration_count':configs,'distinct_loop_types':len(loops),'rooted_oriented_encodings_checked':encodings,'max_length':max(map(len,loops)),
  'queries':[{'vertices':sorted(K),'meeting_loop_types':counts[z],'total_loop_birth_intensity':str(probabilities[z]*s.rate(K)),'proposal_acceptance_probability':str(probabilities[z])} for z,K in enumerate(queries)],
  'all_local_birth_intensities_exact':True}

class FixedBits:
 # Test fixture with a known 1024-bit dyadic U; zero tail after its bits.
 def __init__(self,value,bits=1024):self.value=value;self.bits=bits
 def getrandbits(self,n):
  if n<=self.bits:
   out=self.value>>(self.bits-n);self.value&=(1<<(self.bits-n))-1;self.bits-=n;return out
  out=self.value<<(n-self.bits);self.value=0;self.bits=0;return out

def mpf(q):return mp.mpf(q.numerator)/q.denominator

def verify_times():
 rng=random.Random(20261105);mp.mp.dps=200;tests=0
 # Wide magnitude range, both sides of range-reduction boundaries.
 for _ in range(200):
  x=F(rng.randrange(1,1<<128),rng.randrange(1,1<<128))*F(2)**rng.randrange(-200,201)
  lo,hi=log_bounds(x,20);v=mp.log(mpf(x));assert mpf(lo)<=v<=mpf(hi);tests+=1
 times=[];truth=[];atoms=[]
 for _ in range(80):
  n=rng.randrange(1,1<<1024);a=LazyExp(FixedBits(n));t=a.time();v=-mp.log(mp.mpf(n)/mp.mpf(2)**1024)
  for lev in range(3):
   lo,hi=t.bounds(lev);assert mpf(lo)<=v<=mpf(hi)
  times.append(t);truth.append(v);atoms.append(a)
 for _ in range(300):
  ia,ib,ic,idd=[rng.randrange(len(times)) for _ in range(4)]
  a=times[ia]+times[ib]-times[ic];b=times[idd];va=truth[ia]+truth[ib]-truth[ic];vb=truth[idd]
  expected=(va>vb)-(va<vb)
  # Symbolically identical combinations compare as exact zero, even if mpmath cancels imperfectly.
  d=a-b
  if not d.terms:expected=0
  assert a.compare(b)==expected;tests+=1
  assert(a+times[ic])-times[ic]==a;tests+=1
 # Nearly equal independently represented atoms force refinement beyond 32-bit uniforms.
 n=(1<<1023)+12345;a=LazyExp(FixedBits(n)).time();b=LazyExp(FixedBits(n+(1<<950))).time()
 assert b<a;tests+=1
 return {'log_bounds_and_comparison_checks':tests,'exponential_atoms_with_three_levels_checked':80,'near_tie_refinement_passed':True,'max_precision_reference_decimal_digits':mp.mp.dps,'all_time_ordering_uses_exact_rational_intervals':True}

def main():
 start=time.monotonic();s=LocalLoopBirthSampler(20261105)
 birth=[verify_birth(3,3,s),verify_birth(4,4,s)];times=verify_times()
 out={'local_proposal_rate_per_query_vertex':str(s.rate([(0,0)])),'birth_checks':birth,'time_checks':times,'seconds':time.monotonic()-start}
 (HERE/'primitive_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':main()
