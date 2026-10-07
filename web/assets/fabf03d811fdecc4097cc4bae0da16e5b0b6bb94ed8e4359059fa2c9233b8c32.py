#!/usr/bin/env python3
"""Exact rational digit packing and one diagonal readout gadget checks.
Finite algebraic diagnostics only; universal guarantees are proved in REPORT.txt.
"""
from fractions import Fraction as F
import random,json

def mm(a,b):
 return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def eye(d): return [[F(i==j) for j in range(d)] for i in range(d)]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,c): return [[c*x for x in ar] for ar in a]
def zeros(d): return [[F(0) for j in range(d)] for i in range(d)]
def eval_series(u,bs,v,xs,index):
 m=len(u);d=len(xs[0]);bigt=zeros(m*d)
 for b,x in zip(bs,xs):
  for i in range(m):
   for j in range(m):
    for a in range(d):
     for c in range(d): bigt[i*d+a][j*d+c]+=b[i][j]*x[a][c]
 power=eye(m*d);su=eye(m*d)
 for _ in range(1,index):power=mm(power,bigt);su=add(su,power)
 return [[sum((u[i]*su[i*d+a][j*d+c]*v[j] for i in range(m) for j in range(m)),F(0)) for c in range(d)] for a in range(d)]
def gadget(xs,k):
 d=len(xs[0]);a=[F(k**(d*i+1)) for i in range(d)];b=[F(k**j) for j in range(d)]
 result=[]
 for x in xs:
  y=zeros(d+2)
  for i in range(d):
   for j in range(d):y[i+1][j+1]=x[i][j]
  ax=[sum((a[i]*x[i][j] for i in range(d)),F(0)) for j in range(d)]
  xb=[sum((x[i][j]*b[j] for j in range(d)),F(0)) for i in range(d)]
  for j in range(d):y[0][j+1]=ax[j]
  for i in range(d):y[i+1][-1]=xb[i]
  y[0][-1]=sum((ax[j]*b[j] for j in range(d)),F(0))
  p=eye(d+2);p[-1][0]=1;pinv=eye(d+2);pinv[-1][0]=-1
  result.append(mm(mm(pinv,y),p))
 return result

def decode(y,num_digits,k,den_bound):
 z=y; digits=[F(0)]*num_digits
 for e in reversed(range(num_digits)):
  digits[e]=(z/F(k**e)).limit_denominator(den_bound)
  z-=digits[e]*k**e
 assert z==0
 return digits

rng=random.Random(5072026);cases=[]
for case in range(24):
 n=2;m=2;d=3
 u=[F(rng.randint(-2,2),rng.randint(1,5)) for _ in range(m)]
 v=[F(rng.randint(-2,2),rng.randint(1,5)) for _ in range(m)]
 bs=[[[F(rng.randint(-2,2),rng.randint(1,5)) for _ in range(m)] for _ in range(m)] for _ in range(n)]
 xs=[]
 for _ in range(n):
  x=zeros(d)
  for i in range(d):
   for j in range(i+1,d):x[i][j]=F(rng.randint(-2,2),rng.randint(1,5))
  xs.append(x)
 f=eval_series(u,bs,v,xs,d);c=sum((u[i]*v[i] for i in range(m)),F(0))
 digits=[c]+[f[i][j]-c*F(i==j) for i in range(d) for j in range(d)]
 den_bound=max(z.denominator for z in digits); mag=max(1,max(abs(z) for z in digits));k=int(8*mag*den_bound**2)+2
 y=sum((z*k**i for i,z in enumerate(digits)),F(0))
 got=eval_series(u,bs,v,gadget(xs,k),d+1)[0][0]
 assert y==got,(case,y,got)
 assert decode(y,len(digits),k,den_bound)==digits
 cases.append({'case':case,'scalar_numerator_bits':y.numerator.bit_length(),'scalar_denominator_bits':y.denominator.bit_length(),'radix_bits':k.bit_length(),'denominator_bound':den_bound})
# Exact denominator cancellation case: y=(1+3)/2=2; digits remain recoverable with sufficiently large radix.
assert decode(F(51),2,101,2)==[F(1,2),F(1,2)]
print(json.dumps({'status':'PASS','random_rational_cases':len(cases),'cases':cases},indent=2))
