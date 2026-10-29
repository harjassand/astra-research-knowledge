from fractions import Fraction as F
import random, json, math
import numpy as np
import mpmath as mp
mp.mp.dps=100
rng=random.Random(202610291303)
def ceilbits(x):
 b=0
 while F(1,2**b)>x:b+=1
 return b
def to_mp(x):return mp.mpf(x.numerator)/x.denominator
def gauss(u,v):
 r=mp.sqrt(-mp.log(u)); th=2*mp.pi*v
 return r*mp.cos(th),r*mp.sin(th)
def polar(A):
 U,s,V=np.linalg.svd(A);return U@V,s[-1]
rows=[]
for nu in [F(1,2),F(1,10),F(1,100),F(1,1000)]:
 u0=nu/128;a=nu/16;b=ceilbits(nu*a*u0*u0/512);c=ceilbits(nu*a/512)
 maxratio=0.;maxpolar=0.;good=0
 for case in range(32):
  exact=[]; rounded=[]; interior=True
  for i in range(16):
   us=[];rs=[]
   for j in range(2):
    z=rng.getrandbits(160); x=F(2*z+1,2**161)
    k=(x.numerator*2**b)//x.denominator; y=F(2*k+1,2**(b+1))
    us.append(to_mp(x));rs.append(to_mp(y))
    assert abs(x-y)<=F(1,2**(b+1))
    if j==0:interior &= u0<=x<=1-u0
   v=gauss(*us);w=gauss(*rs)
   wr=[]
   for component in w:
    z=int(mp.nint(component*2**c)); value=F(z,2**c)
    assert abs(to_mp(value)-component)<=to_mp(nu*a/512)
    wr.append(to_mp(value))
   exact.append(mp.mpc(*v));rounded.append(mp.mpc(*wr))
  err=mp.sqrt(sum(abs(x-y)**2 for x,y in zip(exact,rounded)))
  A=np.array([complex(z) for z in exact]).reshape(4,4);B=np.array([complex(z) for z in rounded]).reshape(4,4)
  Q,smin=polar(A);Qb,sminb=polar(B)
  if interior:
   assert err<to_mp(nu*a/4)
   maxratio=max(maxratio,float(err/to_mp(nu*a/4)))
  if interior and smin>float(a):
   good+=1
   assert sminb>7*float(a)/8
   pe=np.linalg.norm(Q-Qb,'fro');bound=2*float(err)/float(a)
   assert pe<=bound+1e-13
   maxpolar=max(maxpolar,pe)
 rows.append(dict(nu=str(nu),uniform_bits=b,scalar_bits=c,cases=32,good=good,max_matrix_error_to_budget=maxratio,max_polar_error=maxpolar))
# Exact arithmetic bounds for the public constants, independent of numerical matrices.
for nu in [F(i,2000) for i in range(1,1001)]:
 a=nu/16;u0=nu/128;h=nu*a*u0*u0/512
 assert 60*h/(u0*u0)+6*nu*a/512<nu*a/4
 assert 32*u0+16*a*a<=9*nu/32<nu/2
 assert a-nu*a/4-a/16>=13*a/16
print(json.dumps(dict(scope='128 high-precision coupling diagnostics and1000 exact parameter cases; not certified interval implementation, not a full design or decoder run',rows=rows),indent=2))
