from fractions import Fraction as F
from itertools import product

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mv(A,x):return [dot(row,x) for row in A]
def toward_grid(x,h):
 z=x/h
 return h*(z.numerator//z.denominator if z>=0 else -((-z).numerator//(-z).denominator))
def obj(G,k,c):return dot(c,mv(G,c))-2*dot(k,c)
count=0
for m in [1,2,3]:
 B=F(m);lam=F(1,2048);b=1
 while b<m:b*=2
 alpha=lam/(128*(b+4)*b*b);delta=B*B*alpha;C=16*m*B*B;theta=delta/C
 h=F(1)
 while h>delta*delta/(24*C*B*m):h/=2
 # Rank-one physical Gram plus PSD repair: exactly singular underlying geometry.
 G=[[F(1)+(m*alpha if i==j else 0) for j in range(m)] for i in range(m)]
 for signs in product([-1,1],repeat=m):
  k=[F(s,3) for s in signs]
  c=[toward_grid(F(s,2*m),h) for s in signs]
  for step in range(25):
   g=[2*(x-y) for x,y in zip(mv(G,c),k)]
   j=max(range(m),key=lambda j:abs(g[j]));s=[F(0)]*m;s[j]=-B if g[j]>=0 else B
   gap=dot(g,[x-y for x,y in zip(c,s)])
   if gap<=delta:break
   exact=[(1-theta)*x+theta*y for x,y in zip(c,s)]
   nxt=[toward_grid(x,h) for x in exact]
   assert sum(map(abs,nxt))<=B
   assert obj(G,k,c)-obj(G,k,nxt)>=delta*delta/(4*C)
   assert all((x/h).denominator==1 for x in nxt)
   c=nxt;count+=1
print('PASS',count,'exact rational rounded-FW descent and feasibility checks; no optimization-completion simulation claimed')
