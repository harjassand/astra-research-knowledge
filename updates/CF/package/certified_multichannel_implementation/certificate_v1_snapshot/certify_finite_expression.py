"""Exact-integer a posteriori certificates for polynomial-phase expressions.

All returned bounds use integer/rational arithmetic. Approximate eigensystems
only propose coefficients. The certificate uses the original exact Hamiltonian.
No sampled residual or unknown analytic Taylor tail is used.
"""
from fractions import Fraction as F
from math import factorial,pi
import numpy as np

P=128;Q=1<<P;EP=256;EQ=1<<EP;CP=160;CQ=1<<CP

def ceildiv(a,b):return -(-a//b)
def upper(x,scale=CQ):return ceildiv(x.numerator*scale,x.denominator)
def ipair(A):
 return (np.array([[round(F(float(x.real))*Q) for x in row] for row in A],dtype=object),
         np.array([[round(F(float(x.imag))*Q) for x in row] for row in A],dtype=object))
def zero():return np.zeros((3,3),dtype=object)
def entrynorm(pair):return sum(abs(int(x)) for a in pair for x in a.flat)
def mul(a,b):return a[0]@b[0]-a[1]@b[1],a[0]@b[1]+a[1]@b[0]
def adj(a):return a[0].T,-a[1].T

def atan_bounds(base):
 lo=hi=0;j=0
 while True:
  den=(2*j+1)*base**(2*j+1);f=EQ//den;c=ceildiv(EQ,den)
  if j%2==0:lo+=f;hi+=c
  else:lo-=c;hi-=f
  nd=(2*j+3)*base**(2*j+3);r=ceildiv(EQ,nd)
  if r<=1:
   if (j+1)%2==0:hi+=r
   else:lo-=r
   return lo,hi
  j+=1
p5=atan_bounds(5);p239=atan_bounds(239)
PI_LO=16*p5[0]-4*p239[1];PI_HI=16*p5[1]-4*p239[0]

def exp_minus_i(x):
 # x is an exact integer divided by Q. Any reduction integer is valid provided
 # the subsequently checked reduced center is at most 4 in magnitude.
 xe=x<<(EP-P);m=round(float(F(x,Q))/(2*pi));twopi_mid=PI_LO+PI_HI
 th=xe-m*twopi_mid
 if abs(th)>4*EQ:raise ValueError('argument reduction center exceeded certified range')
 M=64;re=EQ//factorial(M);im=0
 for k in range(M-1,-1,-1):
  # Multiply by -i theta, round down coordinatewise, add rounded 1/k!.
  re,im=(im*th)//EQ+EQ//factorial(k),(-re*th)//EQ
 err=F(abs(m)*(PI_HI-PI_LO),EQ)+F(2*(M+1)*4**M,EQ)+F(4**(M+1),factorial(M+1))
 return (re,im),err

def original_A(c,h,k):
 c,h,k=F(float(c)),F(float(h)),F(float(k))
 D2=[[1,0,0],[0,0,0],[0,0,-1]];D1=[[0,0,0],[0,F(1,3),0],[0,0,-F(1,3)]];D0=[[-1,1,F(1,3)],[1,0,2],[F(1,3),2,1]]
 a=[]
 for r in range(3):
  out=[]
  for i in range(3):
   row=[]
   for j in range(3):
    x=(h*k*(c*c*D2[i][j]+c*D1[i][j]+D0[i][j]) if r==0 else h*h*k*(2*c*D2[i][j]+D1[i][j]) if r==1 else h**3*k*D2[i][j])
    y=x*3*Q
    assert y.denominator==1
    row.append(y.numerator)
   out.append(row)
  a.append(np.array(out,dtype=object))
 return a

def certify_panel(c,h,k,polynomials,phases):
 A=original_A(c,h,k);Cs=[[ipair(x) for x in poly] for poly in polynomials]
 Ph=[[round(F(float(x))*Q) for x in phase] for phase in phases]
 center=(sum((C[0][0] for C in Cs),zero())-Q*np.eye(3,dtype=object),sum((C[0][1] for C in Cs),zero()))
 initial=F(entrynorm(center),Q);residual=F(0)
 for C,phi in zip(Cs,Ph):
  dp=[(r+1)*phi[r+1] for r in range(len(phi)-1)]
  maxdegree=max(len(C)+len(dp)-2,len(C)+1)
  for r in range(maxdegree+1):
   re=zero();im=zero()
   if r+1<len(C):re-=3*Q*(r+1)*C[r+1][1];im+=3*Q*(r+1)*C[r+1][0]
   for j in range(max(0,r-len(C)+1),min(r,len(dp)-1)+1):re+=3*dp[j]*C[r-j][0];im+=3*dp[j]*C[r-j][1]
   for j in range(max(0,r-len(C)+1),min(r,2)+1):re-=A[j]@C[r-j][0];im-=A[j]@C[r-j][1]
   residual+=F(entrynorm((re,im)),3*Q*Q*(r+1))
 e=initial+residual;ends=[];evalerrors=[]
 for sign in (1,-1):
  fre=zero();fim=zero();ee=F(0)
  for C,phi in zip(Cs,Ph):
   cr=sum((sign**r*x[0] for r,x in enumerate(C)),zero());ci=sum((sign**r*x[1] for r,x in enumerate(C)),zero())
   x=sum(sign**r*v for r,v in enumerate(phi));(er,ei),bound=exp_minus_i(x)
   fre+=cr*er-ci*ei;fim+=cr*ei+ci*er;ee+=F(entrynorm((cr,ci)),Q)*bound
  ends.append((fre,fim));evalerrors.append(ee)
 # Endpoint expressions have denominator Q*EQ. Their product is rounded to Q.
 vre,vim=mul(ends[0],adj(ends[1]));den=Q*EQ*EQ
 vre=np.array([[int(x)//den for x in row] for row in vre],dtype=object);vim=np.array([[int(x)//den for x in row] for row in vim],dtype=object)
 rounding=F(18,Q) # Entrywise l1 bound: 9 complex entries, 2 coordinates each.
 ep=e+evalerrors[0];em=e+evalerrors[1]
 error=ep+em+ep*em+rounding
 return (vre,vim),upper(error),{'initial_defect_upper':float(initial),'integrated_residual_each_half_upper':float(residual),'endpoint_evaluation_error_upper':float(max(evalerrors)),'local_operator_error_upper':float(F(upper(error),CQ))}

def compose(V,U,error,local):
 re,im=mul(V,U)
 re=np.array([[int(x)//Q for x in row] for row in re],dtype=object);im=np.array([[int(x)//Q for x in row] for row in im],dtype=object)
 new=error+local+ceildiv(error*local,CQ)+18*(CQ//Q)
 return (re,im),new
