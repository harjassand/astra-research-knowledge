"""Exploratory birth-SUPPRESSED upper-return matrix; NOT a proof or full tail closure."""
import math,json
import sympy as S
import mpmath as mp
mp.mp.dps=90

def fall(n,k): return math.factorial(n)//math.factorial(n-k) if n>=k else 0
def g(n):return 4*(n//3)+n%3
# Cubic fast graph with missing complex 2A+C. All rates one.
fast=[(0,1),(1,0),(1,3),(3,1),(3,0),(0,3)]
def absorption(n):
 Q=S.zeros(n+1);K=S.zeros(n+1,n-2)
 for a in range(n+1):
  c=n-a
  for y,z in fast:
   rate=fall(a,y)*fall(c,3-y)
   if rate:Q[a,a+z-y]+=rate;Q[a,a]-=rate
  k=fall(a,3)
  Q[a,a]-=k
  if k:K[a,a-3]+=k
 P=(-Q).inv()*K
 assert all(sum(P[i,j] for j in range(n-2))==1 for i in range(n+1))
 return P

def run(H,B,alpha):
 st=[(a,n-a) for n in range(H+1) for a in range(n+1)];ix={x:i for i,x in enumerate(st)}
 Ps={n:absorption(n) for n in (H+1,H+2)}
 G=mp.matrix(len(st));r=mp.mpf(B)
 for i,(a,c) in enumerate(st):
  n=a+c;b=r+g(n)
  def add(aa,cc,db,rate):
   if not rate:return
   nn=aa+cc;delta=db-g(nn)+g(n);tilt=r**(alpha*delta)
   G[i,i]-=rate
   if nn<=H:G[i,ix[aa,cc]]+=rate*tilt
   else:
    P=Ps[nn]
    for z in range(nn-2):
     p=P[aa,z]
     if p:G[i,ix[z,nn-3-z]]+=rate*tilt*mp.mpf(int(p.p))/int(p.q)
  add(a+1,c,1,mp.mpf(1));add(a+2,c,3,a*b)
  if a>=3:add(a-3,c,-4,fall(a,3)*b*(b-1)*(b-2)*(b-3))
  for y,z in fast:
   k=fall(a,y)*fall(c,3-y)
   if k:add(a+z-y,c+y-z,0,k*b*(b-1)*(b-2)*(b-3))
 v=mp.lu_solve(-G,mp.matrix([1]*len(st)))
 return {'H':H,'B':str(B),'alpha':str(alpha),'min_v':str(min(v)), 'max_v':str(max(v)), 'all_positive':bool(min(v)>0), 'hole_v':str(v[ix[2,1]])}
if __name__=='__main__':
 out=[run(H,B,mp.mpf('0.02')) for H in [5,8] for B in [100,1000,10000]]
 print(json.dumps(out,indent=2))
