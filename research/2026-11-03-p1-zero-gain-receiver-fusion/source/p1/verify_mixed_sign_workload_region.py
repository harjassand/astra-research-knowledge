"""Exact integer/rational verification of the mixed-sign high-workload drift identities.
Each finite fixture tests all eight sources plus both core jumps.
"""
from fractions import Fraction
from itertools import product

aw=11

def ff(n,k):
 v=1
 for i in range(k):v*=n-i
 return v

def p(t):return 2*(t%2)+t//2

def psi(x):
 a,b,c,d,e,f=x
 return sum([3*max(b-c,0),aw*max(c-b,0),p(min(b,c)),3*max(e-f,0),aw*max(f-e,0),p(min(e,f))])

def g(x):
 a,b,c,d,e,f=x
 h=lambda b,c:abs(b-c)+Fraction(3*min(b,c),2)+Fraction(min(b,c)%2,2)
 return max(0,a-h(b,c)),max(0,d-h(e,f))

def react(x):
 a,b,c,d,e,f=x
 vs=((1,1,0),(1,0,1),(1,1,1),(-3,-2,-2))
 for port in (0,1):
  ids=(0,1,2) if port==0 else (3,4,5)
  aa,bb,cc=(x[i] for i in ids)
  lam=(1,aa*bb,ff(aa,2)*bb*cc,ff(aa,3)*ff(bb,2)*ff(cc,2))
  for s in range(4):
   if lam[s]<=0:continue
   y=list(x)
   for i,dv in zip(ids,vs[s]):y[i]+=dv
   assert min(y)>=0
   yield 's',port,s,Fraction(lam[s]),tuple(y)
 if a*d>0:
  if b>=2 and c>=2:yield 'c',0,0,Fraction(2*a*d*ff(b,2)*ff(c,2)),(a,b-2,c-2,d,e+2,f+2)
  if e>=2 and f>=2:yield 'c',1,0,Fraction(a*d*ff(e,2)*ff(f,2)),(a,b+2,c+2,d,e-2,f-2)

N=0
for a,d in product(range(3,8),repeat=2):
 for sign1,sign2 in product((-1,1),repeat=2):
  for r1,r2 in product((65,70,80),repeat=2):
   for t1,t2 in product((0,1,2,3,4,7,15,50),repeat=2):
    b,c=(r1+t1,t1) if sign1>0 else (t1,r1+t1)
    e,f=(r2+t2,t2) if sign2>0 else (t2,r2+t2)
    x=(a,b,c,d,e,f)
    assert g(x)==(0,0)
    L=Fraction(0);q=Fraction(0)
    for kind,port,src,rate,y in react(x):
     assert g(y)==(0,0),(x,kind,port,src,y,g(y))
     if kind=='c':assert psi(x)==psi(y)
     else:
      L+=rate*(psi(y)-psi(x))
      q+=rate
    assert L<=-q/4,(x,float(L/q))
    N+=1
print('PASS:',N,'mixed-sign, both positive and negative, arbitrary minorities, full core routes, g remains zero, L Psi <= -q/4 for unit raw rates and a_work=11.')
