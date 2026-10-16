from fractions import Fraction as F
from math import factorial
import json
edges=[(0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(0,4),(1,5),(2,6),(3,7)]
b=lambda n:F(669,250)*n*(n-1)+F(54051,500)
d=lambda n:F(1,25)*n*(n-1)*(n-2)+F(37881,1000)*n
D=F(82207,10000)
rows=[]
for s in range(16,500):
 if s<=121:
  x=[16]+[0]*7; rem=s-16
  for k in range(1,8):x[k]=min(rem,15);rem-=x[k]
 else:
  q,r=divmod(s,100);x=[100]*q+[r]+[0]*(7-q)
 assert sum(x)==s and len(x)==8 and max(x)<=100
 grouped={-1:F(0),0:F(0),1:F(0),'hit':F(0)}
 transitions=[]
 for i,n in enumerate(x):
  y=x.copy();y[i]+=1;transitions.append((y,b(n)))
  if n:
   y=x.copy();y[i]-=1;transitions.append((y,d(n)))
 for i,j in edges:
  for u,v in [(i,j),(j,i)]:
   if x[u]:
    y=x.copy();y[u]-=1;y[v]+=1;transitions.append((y,D*x[u]))
 for y,rate in transitions:
  assert max(y)<=101
  grouped['hit' if max(y)<=15 else sum(y)-s]+=rate
 beta=sum(map(b,x));delta=sum(map(d,x))
 kappa=F(0)
 if s<=121:
  delta-=d(16);kappa=d(16)+16*D*sum(x[j]<=14 for i,j in [(0,1),(0,4)])
 assert (beta,delta,kappa)==(grouped[1],grouped[-1],grouped['hit'])
 rows.append((beta,delta,kappa))
def solve(clock):
 diag=[];rhs=[]
 for i,(beta,delta,kappa) in enumerate(rows):
  A=beta+delta+kappa-clock
  B=kappa if clock else F(0)
  if i==len(rows)-1:B+=beta
  if i:
   w=delta/diag[-1];A-=w*rows[i-1][0];B+=w*rhs[-1]
  assert A>0
  diag.append(A);rhs.append(B)
 x=[F(0)]*len(rows)
 for i in range(len(rows)-1,-1,-1):
  x[i]=(rhs[i]+(rows[i][0]*x[i+1] if i+1<len(rows) else 0))/diag[i]
 for i,(beta,delta,kappa) in enumerate(rows):
  l=(beta+delta+kappa-clock)*x[i]-(delta*x[i-1] if i else 0)-(beta*x[i+1] if i+1<len(rows) else beta)
  assert l==(kappa if clock else 0)
 return x
P=solve(F(0));M=solve(F(100));i=400-16
assert all(0<p<1 for p in P) and all(m>1 for m in M)
assert P[i]<F(1,10**18) and M[i]<100 and F(100**100,factorial(100))>10**42
print(json.dumps({'actual_rows':len(rows),'equations':len(rows)*2,'P400_float_diagnostic':float(P[i]),'M400_float_diagnostic':float(M[i]),'all_exact_checks':'PASS'},indent=2))
