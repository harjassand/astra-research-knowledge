"""Bounded exact Gaussian-integer diagnostics. No sampler/FPRAS implementation."""
from fractions import Fraction as Q
from itertools import combinations, product, permutations
from pathlib import Path
import random, json, time
rng=random.Random(6200202)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cj(a):return (a[0],-a[1])
def norm(a):return a[0]*a[0]+a[1]*a[1]
def gd(a):
 n=len(a);out=(0,0)
 for p in permutations(range(n)):
  s=-1 if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2 else 1
  t=(s,0)
  for i in range(n):t=mul(t,a[i][p[i]])
  out=add(out,t)
 return out

def signature(lines):
 n=len(lines[0][0]);f={}
 for u in range(1<<n):
  R=[i for i in range(n) if not (u>>i&1)]
  if len(R)%2:f[u]=0;continue
  value=0
  for a in combinations(range(len(lines)),len(R)//2):
   cols=[c for l in a for c in lines[l]]
   value+=norm(gd([[v[r] for v in cols] for r in R]))
  f[u]=value
 return f

def pd(lines,x,t):
 n=len(x);a=[[(x[i] if i==j else 0,0) for j in range(n)] for i in range(n)]
 for (u,v),s in zip(lines,t):
  for i in range(n):
   for j in range(n):
    z=add(mul(u[i],cj(u[j])),mul(v[i],cj(v[j])))
    a[i][j]=add(a[i][j],(s*z[0],s*z[1]))
 out=gd(a);assert out[1]==0
 return out[0]

def signed_extraction(lines,x):
 out=Q(0);m=len(lines)
 weights={0:Q(2),-1:Q(-1,2),1:Q(-1,2)}
 for t in product((0,-1,1),repeat=m):
  w=Q(1)
  for s in t:w*=weights[s]
  out+=w*pd(lines,x,t)
 return out

def signed_eval(f,x):
 n=len(x);out=0
 for u,w in f.items():
  if not w:continue
  v=w*(-1)**((n-u.bit_count())//2)
  for i in range(n):
   if u>>i&1:v*=x[i]
  out+=v
 return out

def conditional_dobrushin(f,fields,forced,excluded):
 n=len(fields);weights={}
 for u,c in f.items():
  if c and u&forced==forced and not u&excluded:
   w=Q(c)
   for i in range(n):
    if u>>i&1:w*=fields[i]
   weights[u]=w
 z=sum(weights.values(),Q(0))
 if not z:return 0
 p=[sum((w for u,w in weights.items() if u>>i&1),Q(0))/z for i in range(n)]
 checks=0
 for i in range(n):
  if p[i] in (0,1):continue
  row=Q(0)
  for j in range(n):
   if j==i:continue
   pij=sum((w for u,w in weights.items() if (u>>i&1) and (u>>j&1)),Q(0))/z
   row+=abs((pij-p[i]*p[j])/(p[i]*(1-p[i])))
  assert row<=1,{'i':i,'row':str(row),'f':f,'fields':fields}
  checks+=1
 return checks

start=time.time();identities=0;rows=0;fixtures=[]
for case in range(12):
 n=4;m=3 if case<11 else 5
 lines=[[[ (rng.randrange(-2,3),rng.randrange(-1,2)) for _ in range(n)] for _ in range(2)] for _ in range(m)]
 f=signature(lines)
 x=[rng.randrange(-3,4) for _ in range(n)]
 left=signed_extraction(lines,x);right=signed_eval(f,x)
 assert left==right
 identities+=1
 for field in ((Q(1),)*n,(Q(1,3),Q(2),Q(3,2),Q(5))):
  for pin in product((-1,0,1),repeat=n):
   forced=sum(1<<i for i,b in enumerate(pin) if b==1)
   excluded=sum(1<<i for i,b in enumerate(pin) if b==-1)
   rows+=conditional_dobrushin(f,field,forced,excluded)
 fixtures.append({'n':n,'m':m,'lines':lines,'hole_coefficients':f,'x':x,'signed_value':str(left)})

# Fixed-cardinality slicing does NOT preserve full Hurwitz stability.
# (1+x0*x1)(1+x2*x3), degree-two slice x0*x1+x2*x3 has a zero
# at x0=x1=exp(i*pi/4), x2=x3=exp(-i*pi/4), all Re positive.
# For equal masses its FLC Hessian along (1,1,-1,-1) is positive for alpha>1/2.
# Robust FLC obstruction for laws within TV delta of the cycle endpoints.
robust=[]
for q in (2,4,8,16,32):
 delta=Q(1,10);den=q*(1-delta-4*delta*delta)
 robust.append({'q':q,'TV':str(delta),'FLC_upper_bound':str(1/den)})
# Sharp full-law influence: one pair is empty/both with equal mass.
assert conditional_dobrushin({0:1,1:0,2:0,3:1},(Q(1),Q(1)),0,0)==2
result={'status':'PASS','seed':6200202,'exact_extraction_identities':identities,'exact_conditional_influence_rows':rows,'seconds':time.time()-start,'fixtures':fixtures,'robust_cycle_bounds':robust,'scope':'Exact finite coefficient/extraction and conditional influence checks only; universal stability follows from the written proof, no FPRAS or mixing execution.'}
Path('work/cycle6/c02_s02/general_pair_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='fixtures'}))
