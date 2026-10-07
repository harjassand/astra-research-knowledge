import random, itertools, json, time
from pathlib import Path
rng=random.Random(6240202)
def det(a):
 n=len(a)
 if not n:return 1
 a=[list(r) for r in a];prev=1;s=1
 for k in range(n-1):
  if not a[k][k]:
   j=next((j for j in range(k+1,n) if a[j][k]),None)
   if j is None:return 0
   a[k],a[j]=a[j],a[k];s=-s
  p=a[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):a[i][j]=(p*a[i][j]-a[i][k]*a[k][j])//prev
  for i in range(k+1,n):a[i][k]=0
  prev=p
 return s*a[-1][-1]
def sig(lines):
 n=len(lines[0][0]); ans={}
 for U in itertools.chain.from_iterable(itertools.combinations(range(n),r) for r in range(0,n+1,2)):
  R=[i for i in range(n) if i not in U];w=0
  for L in itertools.combinations(range(len(lines)),len(R)//2):
   cols=[v for i in L for v in lines[i]]
   w+=det([[v[r] for v in cols] for r in R])**2
  ans[tuple(U)]=w
 return ans
def rayleigh4(f,i,j,x,y):
 k,l=[a for a in range(4) if a not in (i,j)];b=lambda a,c:f[tuple(sorted((a,c)))];a=f[()]
 return a*b(i,j)+b(i,k)*b(j,k)*x*x+b(i,l)*b(j,l)*y*y+(b(i,k)*b(j,l)+b(i,l)*b(j,k)-b(i,j)*b(k,l)-a)*x*y+b(k,l)*x*x*y*y
start=time.time(); witness=None
for t in range(1000):
 m=rng.randrange(2,7);lines=[[[rng.randrange(-2,3) for _ in range(4)] for _ in range(2)] for _ in range(m)]
 f=sig(lines)
 for i,j in itertools.combinations(range(4),2):
  for x,y in itertools.product((-4,-2,-1,0,1,2,4),repeat=2):
   d=rayleigh4(f,i,j,x,y)
   if d<0:witness={'trial':t,'lines':lines,'f':{str(k):v for k,v in f.items()},'ij':[i,j],'xy':[x,y],'rayleigh':d};break
  if witness:break
 if witness:break
out={'seed':6240202,'trials':t+1,'witness':witness,'seconds':time.time()-start}
Path('work/cycle6/c02_s02/auxiliary_probe.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
