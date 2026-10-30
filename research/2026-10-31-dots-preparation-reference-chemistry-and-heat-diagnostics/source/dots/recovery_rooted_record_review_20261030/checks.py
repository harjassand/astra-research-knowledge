import math,random,json
from collections import Counter
random.seed(1029)
def row(v,k):
 i,x,y=v;s=2*2**i
 out=Counter()
 for a,b in [(x+2*y,y),(x-2*y,y),(x+2*y+1,y),(x-2*y-1,y),(x,y+2*x),(x,y-2*x),(x,y+2*x+1),(x,y-2*x-1)]:out[(i,a%s,b%s)]+=1
 if i:out[(i-1,x%(s//2),y%(s//2))]+=1
 if i<k:
  for a in range(2):
   for b in range(2):out[(i+1,x+a*s,y+b*s)]+=1
 out[v]+=26-sum(out.values())
 return out
def vertices(k):return [(i,x,y) for i in range(k+1) for x in range(2*2**i) for y in range(2*2**i)]
def project(v,k):
 i,x,y=v;s=2*2**k
 return (k,x%s,y%s) if i==k+1 else v
for k in range(4):
 for v in vertices(k+1):
  pv=project(v,k)
  for w in row(v,k+1):assert project(w,k) in row(pv,k)
def walks(k,L):
 c=Counter({(0,0,0):1})
 for _ in range(L):
  out=Counter()
  for v,a in c.items():
   for w,b in row(v,k).items():out[w]+=a*b
  c=out
 return c
for L in range(1,5):assert walks(L,L)==walks(L+1,L)
max_entropy_residual=-1e9
for _ in range(10000):
 n=random.randrange(1,100);sizes=[random.randrange(1,30) for j in range(n)]
 L=random.uniform(.1,5);tau=random.uniform(.1,4);K=math.exp(random.uniform(-10,5))
 f=[math.exp(random.uniform(-10,L*s)) for s in sizes]
 V=sum(f);W=sum(s*v for s,v in zip(sizes,f));Z=1+K*V;Ct=sum(math.exp(-tau*s) for s in sizes)
 residual=math.log(Z)-(L+tau)*K*W/Z-math.log1p(K*Ct)
 max_entropy_residual=max(max_entropy_residual,residual);assert residual<1e-10
print(json.dumps({'base_retraction_k_0_to_3':'pass','root_weighted_walk_stabilization_L_1_to_4':'pass','entropy_random_tests':10000,'max_entropy_residual':max_entropy_residual},indent=2))
