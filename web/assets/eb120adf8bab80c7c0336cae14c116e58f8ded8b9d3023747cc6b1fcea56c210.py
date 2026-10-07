from itertools import combinations, permutations, product
from random import Random
from math import prod
rng=Random(6107); n=4

def det(a):
 m=len(a)
 if not m:return 1
 return sum(((-1)**sum(p[i]>p[j] for i in range(m) for j in range(i+1,m)))*prod(a[i][p[i]] for i in range(m)) for p in permutations(range(m)))
def ev(poly,x): return sum(c*prod(x[i] for i in range(n) if m>>i&1) for m,c in poly.items())
def der(poly,i): return {m^(1<<i):c for m,c in poly.items() if m>>i&1}
def coeff(F,u,v):
 pairs=[(tuple(int(i==j) for j in range(n)),tuple(F[i])) for i in range(n)]+[(tuple(u),tuple(v))]
 q={}
 for mask in range(1<<n):
  if mask.bit_count()%2: continue
  R=[i for i in range(n) if not mask>>i&1]; k=len(R)//2; val=0
  for ids in combinations(range(n+1),k):
   cols=[col for ix in ids for col in pairs[ix]]
   val+=det([[cols[j][i] for j in range(len(cols))] for i in R])**2
  q[mask]=(-1)**((n-mask.bit_count())//2)*val
 return q
xs=list(product(range(-2,3),repeat=2))
for trial in range(12000):
 F=[[rng.randrange(-2,3) for _ in range(n)] for _ in range(n)]
 u=[rng.randrange(-2,3) for _ in range(n)]; v=[rng.randrange(-2,3) for _ in range(n)]
 if all(u[i]*v[j]-u[j]*v[i]==0 for i in range(n) for j in range(i+1,n)): continue
 q=coeff(F,u,v); found=None
 for i,j in combinations(range(n),2):
  pi=der(q,i); pj=der(q,j); pij=der(pi,j)
  other=[k for k in range(n) if k not in (i,j)]
  for a,b in xs:
   x=[0]*n;x[other[0]]=a;x[other[1]]=b
   val=ev(pi,x)*ev(pj,x)-ev(q,x)*ev(pij,x)
   if val<0: found=(i,j,a,b,val);break
  if found: break
 if found:
  print({'trial':trial,'F':F,'u':u,'v':v,'coefficients':q,'violation':found})
  break
else: print('NO_VIOLATION_IN_12000_RANDOM_EXACT_INSTANCES')
