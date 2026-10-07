from fractions import Fraction as Q
from itertools import combinations,permutations,product
from pathlib import Path
import random,json,time
rng=random.Random(6200233)
def det(a):
 n=len(a)
 return sum(((-1 if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2 else 1)*__import__('functools').reduce(lambda a,b:a*b,(a[i][p[i]] for i in range(n)),1) for p in permutations(range(n))),0)
def signature(lines,tables):
 cols=[v for uv in lines for v in uv];n=len(cols[0]);f={}
 for U in range(1<<n):
  R=[i for i in range(n) if not (U>>i&1)];total=0
  for B in combinations(range(len(cols)),len(R)):
   B=set(B);w=1
   for l,b in enumerate(tables):
    w*=b[(1 if 2*l in B else 0)+(2 if 2*l+1 in B else 0)]
   if w:total+=w*det([[cols[j][i] for j in sorted(B)] for i in R])**2
  f[U]=total
 return f
def rows(f,fields):
 n=len(fields);checks=0
 for pins in product((-1,0,1),repeat=n):
  forced=sum(1<<i for i,b in enumerate(pins) if b==1);excluded=sum(1<<i for i,b in enumerate(pins) if b==-1)
  ws={}
  for U,v in f.items():
   if not v or U&forced!=forced or U&excluded:continue
   w=Q(v)
   for i in range(n):
    if U>>i&1:w*=fields[i]
   ws[U]=w
  z=sum(ws.values(),Q(0))
  if not z:continue
  p=[sum((w for U,w in ws.items() if U>>i&1),Q(0))/z for i in range(n)]
  for i in range(n):
   if p[i] in (0,1):continue
   row=Q(0)
   for j in range(n):
    if i==j:continue
    pij=sum((w for U,w in ws.items() if U>>i&1 and U>>j&1),Q(0))/z
    row+=abs((pij-p[i]*p[j])/(p[i]*(1-p[i])))
   assert row<=1,(row,f,tables)
   checks+=1
 return checks
start=time.time();checks=0;fixtures=[]
for t in range(24):
 lines=[[[rng.randrange(-2,3) for _ in range(4)] for _ in range(2)] for _ in range(2)]
 tables=[[rng.randrange(0,5) for _ in range(4)] for _ in range(2)]
 f=signature(lines,tables)
 for fields in ((Q(1),)*4,(Q(1,2),Q(2),Q(3),Q(1,3))):checks+=rows(f,fields)
 fixtures.append({'lines':lines,'tables':tables,'f':f})
result={'status':'PASS','seed':6200233,'fixtures':fixtures,'influence_rows':checks,'seconds':time.time()-start,'scope':'Exact local two-column filter coefficients and absolute-influence rows under all pinnings; no mixing/sampler execution.'}
Path('work/cycle6/c02_s02/revisions/arbitrary_local_tables_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='fixtures'}))
