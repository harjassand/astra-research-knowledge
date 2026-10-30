from fractions import Fraction as F
from random import Random
rng=Random(712)
def quart(x,y):return 2*x*x*y*y+y**4
def upper(a,b,x,y):
 f=quart(x,y)
 if f==0:return None
 h=4*y*y*a*a+16*x*y*a*b+(4*x*x+12*y*y)*b*b
 g=4*x*y*y*a+4*(x*x+y*y)*y*b
 return (h/2-g*g/(4*f))/(x*x-y*y)
for a in [F(0),F(1,4),F(1,2),F(1),F(2),F(3),F(4),F(10)]:
 b=F(1);lo=None;hi=None;lr=hr=None
 for i in range(-150,151):
  x=F(i,20);y=F(1)
  if x*x==y*y:continue
  cut=upper(a,b,x,y)
  if x*x>y*y and (hi is None or cut<hi):hi,hr=cut,(x,y)
  if x*x<y*y and (lo is None or cut>lo):lo,lr=cut,(x,y)
 print('base',a,b,'lower',float(lo),lr,'upper',float(hi),hr,'gap',float(lo-hi))
 if lo>hi:
  print('EXACT',lo,hi);break
