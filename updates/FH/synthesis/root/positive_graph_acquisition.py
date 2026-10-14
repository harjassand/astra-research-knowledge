"""Exact energy-oracle implementation of established positive graph group tests.

No claim of a new graph-query primitive. A globally pairwise ferromagnetic
class and a deterministic energy/weight oracle are premises,not learned facts.
The generic learner reconstructs support/couplings;only a separately checked
homogeneous ring can use the incoming slow-complement kinetic certificate.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,itertools,json,math,platform,random,time

class Oracle:
 def __init__(self,n,edges,couplings,fields):
  self.n=n;self._edges=list(edges);self._couplings=list(map(F,couplings));self._fields=list(map(F,fields));self.transcript=[]
 def __call__(self,mask):
  value=F(1)
  for (i,j),t in zip(self._edges,self._couplings):
   if ((mask>>i)&1)==((mask>>j)&1):value*=t
  for i,r in enumerate(self._fields):
   if mask>>i&1:value*=r
  self.transcript.append(dict(mask=str(mask),weight=str(value)));return value

def positive_sqrt(q):
 a=math.isqrt(q.numerator);b=math.isqrt(q.denominator)
 if a*a!=q.numerator or b*b!=q.denominator:raise ValueError('Rational coupling input promise violated;algebraic/interval representation required')
 return F(a,b)

def learn(n,oracle,cycle=False):
 """Call-only access: learner never reads planted graph/coupling attributes."""
 if n<4:raise ValueError('n>=4')
 V=(1<<n)-1;cache={};transcript=[];contrasts=0
 def weight(S):
  if S not in cache:
   cache[S]=F(oracle(S));transcript.append(dict(mask=str(S),weight=str(cache[S])))
  return cache[S]
 w0=weight(0);singles=[weight(1<<i) for i in range(n)];wv=weight(V)
 def ratio(i,S):
  nonlocal contrasts
  assert not S&(1<<i);contrasts+=1
  return weight(S|(1<<i))*w0/(weight(S)*singles[i])
 q=None
 if cycle:
  q=positive_sqrt(ratio(0,V^1))
  if q<=1:raise ValueError('Strict ferromagnetic cycle requires t>1')
 adjacency=[{} for _ in range(n)];visits=[]
 for i in range(n):
  total=q*q if cycle else ratio(i,V^(1<<i));visited=0
  def walk(ids,product):
   nonlocal visited
   if product==1:return
   if product<1:raise ValueError('Positive-coupling support query became negative')
   if len(ids)==1:
    j=ids[0];assert j!=i
    adjacency[i][j]=product;return
   visited+=1;cut=len(ids)//2;left,right=ids[:cut],ids[cut:]
   queried,other=(right,left) if i in left else(left,right)
   S=sum(1<<j for j in queried);assert not S&(1<<i)
   first=ratio(i,S);second=product/first
   if cycle and (first not in [F(1),q,q*q] or second not in [F(1),q,q*q]):raise ValueError('Outside uniform degree2 promise')
   walk(queried,first);walk(other,second)
  walk(list(range(n)),total);visits.append(visited)
 edges=[];couplings={}
 for i in range(n):
  for j,value in adjacency[i].items():
   if adjacency[j].get(i)!=value:raise ValueError('Asymmetric inferred interaction')
   if i<j:edges.append((i,j));couplings[(i,j)]=positive_sqrt(value)
 fields=[]
 for i in range(n):
  factor=F(1)
  for j,value in adjacency[i].items():factor*=positive_sqrt(value)
  fields.append(singles[i]/w0*factor)
 order=None
 if cycle:
  if any(len(row)!=2 for row in adjacency) or len(set(couplings.values()))!=1 or len(set(fields))!=1:raise ValueError('Outside uniform cycle and field promise')
  order=[0,min(adjacency[0])]
  while len(order)<n:
   nxt=next(j for j in adjacency[order[-1]] if j!=order[-2])
   if nxt in order:raise ValueError('Disconnected degree2 graph')
   order.append(nxt)
  assert 0 in adjacency[order[-1]]
 edges.sort();h=(n-1).bit_length();m=len(edges)
 bound=n*(2*h+1)+1 if cycle else 3*n+2*m*h+1
 assert len(cache)<=bound
 return dict(n=n,edges=edges,couplings={str(e):str(t) for e,t in couplings.items()},fields=list(map(str,fields)),order=order,
  unique_weight_queries=len(cache),contrasts=contrasts,positive_internal_nodes=sum(visits),per_vertex_nodes=visits,
  proven_query_bound=bound,pairwise_source_queries=1+n+n*(n-1)//2,full_states=str(1<<n),query_transcript=transcript,
  legal_access='Exact positive rational configuration-weight calls;global pairwise and positive rational coupling promises;no access to oracle graph internals.')

def check_case(n,seed,cycle=True):
 rng=random.Random(seed);order=list(range(n));rng.shuffle(order)
 if cycle:edges=sorted({tuple(sorted((order[j],order[(j+1)%n]))) for j in range(n)});couplings=[F(3,2)]*n;fields=[F(5,3)]*n
 else:
  edges=[(i,j) for i in range(n) for j in range(i+1,n) if rng.random()<.3]
  couplings=[F(rng.randint(3,12),2) for _ in edges];fields=[F(rng.randint(1,9),rng.randint(1,9)) for _ in range(n)]
 oracle=Oracle(n,edges,couplings,fields);res=learn(n,oracle,cycle)
 assert res['edges']==edges and res['couplings']=={str(e):str(t) for e,t in zip(edges,couplings)} and res['fields']==list(map(str,fields))
 assert len({r['mask'] for r in res['query_transcript']})==len(res['query_transcript'])
 return {k:v for k,v in res.items() if k not in ['query_transcript','couplings','fields','edges','order','per_vertex_nodes']}

def main(out):
 started=time.monotonic();rows=[]
 for n in [4,5,6,8,12,16,24,32,64,128]:
  for seed in range(12):rows.append(check_case(n,seed))
 for n in range(4,11):
  for seed in range(20):rows.append(check_case(n,seed,False))
 # Actual source layout/parameters;exact oracle and recovered law,not rare trajectories.
 n=24;rng=random.Random(17);order=list(range(n));rng.shuffle(order);edges=sorted({tuple(sorted((order[j],order[(j+1)%n]))) for j in range(n)})
 oracle=Oracle(n,edges,[F(1000)]*n,[F(1)]*n);law=learn(n,oracle,True)
 assert len(law['edges'])==n and set(law['couplings'].values())=={'1000'} and set(law['fields'])=={'1'}
 out.mkdir(parents=True,exist_ok=True);(out/'ACQUIRED_CYCLE_TRANSCRIPT.json').write_text(json.dumps(law,indent=2)+'\n')
 report=dict(status='PASS',cases=len(rows),cycle_cases=120,heterogeneous_graph_cases=140,rows=rows,
  source_n24_queries=law['unique_weight_queries'],source_n24_pairwise_queries=301,
  source_n24_proven_bound=law['proven_query_bound'],python=platform.python_version(),seconds=time.monotonic()-started,
  prior_status='Positive support/additive graph group testing is established prior art;this is an energy-oracle implementation and conditional acquisition improvement,not a new primitive.',
  limits='Pairwise class,strict coupling signs,energy precision and microscopic dynamics remain premises. No general complement bound,physical sensor or operational molecular advantage acquired.')
 (out/'GRAPH_ACQUISITION_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True,type=Path);main(ap.parse_args().output_dir)
