from fractions import Fraction as F
import itertools,json
# Exact toy: four graph vertices, path plus the changed-set triangle 0,1,2.
n=4;edges=[(0,1),(1,2),(2,3),(0,2)];adj=[0]*n
for i,j in edges:adj[i]|=1<<j;adj[j]|=1<<i
animals=[]
for A in range(1,1<<n):
 seen=A&-A
 while True:
  new=seen
  for i in range(n):
   if seen>>i&1:new|=adj[i]&A
  if new==seen:break
  seen=new
 if seen==A:animals.append(A)
theta=F(1,1024);exp_a=F(512);D=7;k=3
f=lambda A,s:exp_a**A.bit_count()*theta**(A.bit_count()-(A&s).bit_count())
V=lambda s:sum(f(A,s) for A in animals)
rows=[]
for s in range(1<<n):
 mminus=(s&D).bit_count();mplus=k-mminus;d=mminus-mplus
 if d<=0:continue
 R=exp_a**mminus*theta**mplus
 assert R>=2**(k+1)/(1-theta)
 actual=V(s^D)-V(s)
 slack=-(1-theta)/2*sum(f(A,s) for A in animals if A&D==D)
 assert actual<=slack
 rows.append({'source':s,'target':s^D,'decrease':d,'deltaV':str(actual),'upper_bound':str(slack)})
print(json.dumps({'animals':len(animals),'theta':str(theta),'exp_a':str(exp_a),'checks':rows},indent=2))
