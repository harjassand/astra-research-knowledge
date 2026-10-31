#!/usr/bin/env python3
"""Independent exact polynomial and nonsmooth checks; not a general cone finder."""
from fractions import Fraction as F
from itertools import product
from math import factorial,prod
import json

def clean(p):return {a:c for a,c in p.items() if c}
def add(p,q):
 r=dict(p)
 for a,c in q.items():r[a]=r.get(a,F(0))+c
 return clean(r)
def scale(p,k):return clean({a:c*k for a,c in p.items()})
def mul(p,q):
 r={}
 for a,c in p.items():
  for b,d in q.items():
   z=tuple(x+y for x,y in zip(a,b));r[z]=r.get(z,F(0))+c*d
 return clean(r)
def power(p,n):
 r={(0,0,0):F(1)}
 for _ in range(n):r=mul(r,p)
 return r
def ev(p,x):return sum(c*prod(F(z)**e for z,e in zip(x,a)) for a,c in p.items())
def shift(p,z):
 r={}
 for a,c in p.items():
  t={(0,0,0):c}
  for i,ai in enumerate(a):
   unit=tuple(int(i==j) for j in range(3))
   t=mul(t,power(add({unit:F(1)},{(0,0,0):F(z[i])}),ai))
  r=add(r,t)
 return r
def ffpoly(u):
 r={(0,0,0):F(1)}
 for i,ui in enumerate(u):
  unit=tuple(int(i==j) for j in range(3))
  for k in range(ui):r=mul(r,add({unit:F(1)},{(0,0,0):-F(k)}))
 return r
def generator_poly(raw,H):
 r={}
 for u,w,k in raw:
  r=add(r,scale(mul(ffpoly(u),add(shift(H,tuple(v-a for a,v in zip(u,w))),scale(H,-1))),k))
 return r
def ff(x,u):
 if any(a<b for a,b in zip(x,u)):return 0
 return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,u))
def raw(rates):
 lam,death,p,q,r,s,u,v=map(F,rates)
 return [((0,0,0),(1,0,0),lam),((1,0,0),(0,0,0),death),
 ((0,2,0),(0,1,1),p),((0,1,1),(0,2,0),q),
 ((0,1,1),(0,0,2),r),((0,0,2),(0,1,1),s),
 ((0,1,1),(1,1,0),u),((1,1,0),(0,1,1),v)]
def comps(N):
 for a in range(N+1):
  for b in range(N-a+1):yield a,b,N-a-b

def check_case(name,rates,t=F(2),degree=2,limit=18):
 lam,death,p,q,r,s,u,v=map(F,rates);rs=raw(rates)
 eta=min(F(1),u/(2*(p+q+u)),u/(2*(r+s)))
 H2={(2,0,0):F(1),(1,1,0):F(1),(1,0,1):F(1),(0,1,1):eta}
 Np={(1,0,0):F(1),(0,1,0):F(1),(0,0,1):F(1)}
 H=mul(H2,power(Np,degree-2));LG=generator_poly(rs[2:],H)
 G={a:c for a,c in LG.items() if sum(a)==degree+1};rem={a:c for a,c in LG.items() if sum(a)<=degree}
 assert len(LG)==len(G)+len(rem)
 for alpha,c in H.items():
  multinomial=F(factorial(degree),prod(factorial(e) for e in alpha))
  assert 0<=c/multinomial<=1
 assert H[(degree,0,0)]==1
 beta=min(G.get((0,degree+1,0),F(0)),G.get((0,0,degree+1),F(0)))
 assert beta==eta*min(p,s)>0 and all(c>=0 for a,c in G.items() if not a[0])
 if degree==2:
  expected={(0,3,0):eta*p,(0,0,3):eta*s,(0,2,1):u+eta*(-p-q+r-u),
   (0,1,2):u+eta*(q-r-s),(2,1,0):-v,(1,2,0):-v*(1-eta),(1,1,1):u-v}
  assert G==clean(expected)
  expectedR={(0,2,0):-2*eta*p,(0,0,2):-2*eta*s,(0,1,1):eta*(p-q-r+s),(0,1,0):eta*p,(0,0,1):eta*s}
  assert rem==clean(expectedR)
 else:assert LG==mul(power(Np,degree-2),generator_poly(rs[2:],H2))
 K=sum(-c for a,c in G.items() if a[0] and c<0);CR=sum(abs(c) for c in rem.values())
 D=death*(1-1/t);e=min(F(1,2),D/(4*K)) if K else F(1,2)
 C=lam*(t/(1-e)-1)+death*e*degree/(t*(1-e))+e*CR/(1-e)
 kap=min(D/4,e*beta/(2**(2*degree+1)*2**degree))
 etamin=min(F(1,2),u/(2*(u+p+q+r+s)));betamin=etamin*min(p,s)/2
 emin=min(F(1,2),D/(4*v));Cmin=lam*(t-1)+death*emin/(t*(1-emin))+emin*betamin/(1-emin)
 kapmin=min(D/4,emin*betamin/16)
 def Hval(x):return ev(H,x)
 def Pval(x):return x[0]+etamin*min(x[1:])
 def h(x):return 1-e*Hval(x)/F((sum(x)+1)**degree)
 def hmin(x):return 1-emin*Pval(x)/F(sum(x)+1)
 def state(x):
  N=sum(x);a,b,c=x;assert 0<=Hval(x)<=N**degree and a<=Pval(x)<=N
  lintH=lintP=quot=quotmin=F(0)
  for u0,w,k in rs:
   rate=k*ff(x,u0)
   if not rate:continue
   xp=tuple(xx-u+v0 for xx,u,v0 in zip(x,u0,w))
   quot+=rate*(t**(sum(w)-sum(u0))*h(xp)/h(x)-1)
   quotmin+=rate*(t**(sum(w)-sum(u0))*hmin(xp)/hmin(x)-1)
   if sum(u0)==sum(w):
    lintH+=rate*(Hval(xp)-Hval(x));lintP+=rate*(Pval(xp)-Pval(x))
  assert lintH==ev(LG,x)
  assert lintH>=beta*(b**(degree+1)+c**(degree+1))-K*a*N**degree-CR*(N+1)**degree
  assert lintP>=betamin*(b*(b-1)+c*(c-1))-v*a*N
  assert quot<=C-D*a/2-e*beta*(b+c)**(degree+1)/(2**degree*F((N+1)**degree))<=C-kap*N
  assert quotmin<=Cmin-D*a/2-emin*betamin*(b+c)**2/(2*F(N+1))<=Cmin-kapmin*N
  if a:
   xd=(a-1,b,c)
   assert h(xd)-h(x)<=e*degree/F(N)
  return True
 count=0
 for N in range(limit+1):
  for x in comps(N):state(x);count+=1
 huge=0
 for N in [10**6,10**50]:
  for x in [(0,N,0),(0,0,N),(1,N-1,0),(1,0,N-1),(0,N//2,N-N//2),(N//3,N//3,N-2*(N//3))]:state(x);huge+=1
 return {'case':name,'degree':degree,'rates':list(map(str,rates)),'t':str(t),'polynomial_eta':str(eta),'polynomial_beta':str(beta),
 'polynomial_K':str(K),'polynomial_C_R':str(CR),'min_eta':str(etamin),'min_beta':str(betamin),
 'ordinary_states_each_comparator':count,'huge_states_each_comparator':huge}

def main():
 rates=[1,1,1,1,2,1,1,1]
 cases=[check_case('noncomplexbalanced_pair_family',rates),
 check_case('small_exponent',rates,F(65,64)),check_case('large_exponent',rates,F(100)),
 check_case('unequal_rates',[F(2,9),F(7,4),F(1,7),F(3,5),2,F(1,11),100,F(5,3)]),
 check_case('small_restoration',[1,F(1,100),100,3,1,7,F(1,1000),100]),
 check_case('degree3_lift',rates,degree=3,limit=10),check_case('degree5_lift',rates,degree=5,limit=8)]
 print(json.dumps({'exact_symbolic_generator_and_remainder_verified':True,'Bernstein_coefficient_bounds_verified':True,
 'degree_lifts_verified':True,'polynomial_and_nonsmooth_comparators_checked':True,'cases':cases},indent=2))
if __name__=='__main__':main()
