"""Full-Fock Hubbard Gaussian sorter and rational existence certificate.

The physical controls are fixed equal onsite U, zero detuning, and positive
spin-independent tunnel g(t). No projection onto singly occupied states.
The certified object is a root specifying three rectangular pulses, not a
hardware certificate. All interval arithmetic uses exact fractions. The
floating matrix checks and sensitivity calculations are separate.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from math import factorial
import math, json, sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm, expm_frechet
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'p2_physical_bridge'))
from orbital_echo import model

class Iv:
 def __init__(self,lo,hi=None):
  self.lo=lo if isinstance(lo,F) else F(lo)
  self.hi=self.lo if hi is None else (hi if isinstance(hi,F) else F(hi))
  assert self.lo<=self.hi
 def __add__(self,o):
  o=cv(o);return Iv(self.lo+o.lo,self.hi+o.hi)
 __radd__=__add__
 def __neg__(self):return Iv(-self.hi,-self.lo)
 def __sub__(self,o):return self+-cv(o)
 def __rsub__(self,o):return cv(o)+-self
 def __mul__(self,o):
  o=cv(o);v=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi];return Iv(min(v),max(v))
 __rmul__=__mul__
 def __truediv__(self,o):
  o=cv(o);assert not(o.lo<=0<=o.hi);return self*Iv(1/o.hi,1/o.lo)
 def __rtruediv__(self,o):return cv(o)/self
 def mag(self):return max(abs(self.lo),abs(self.hi))
 def __repr__(self):return f'[{float(self.lo):.17g},{float(self.hi):.17g}]'
def cv(x):return x if isinstance(x,Iv) else Iv(x)

class Dual:
 def __init__(self,v,d=(0,0)):self.v=v;self.d=tuple(d)
 def __add__(self,o):
  o=du(o);return Dual(self.v+o.v,[a+b for a,b in zip(self.d,o.d)])
 __radd__=__add__
 def __neg__(self):return Dual(-self.v,[-a for a in self.d])
 def __sub__(self,o):return self+-du(o)
 def __rsub__(self,o):return du(o)+-self
 def __mul__(self,o):
  o=du(o);return Dual(self.v*o.v,[a*o.v+self.v*b for a,b in zip(self.d,o.d)])
 __rmul__=__mul__
 def __truediv__(self,o):
  o=du(o);return Dual(self.v/o.v,[(a*o.v-self.v*b)/(o.v*o.v) for a,b in zip(self.d,o.d)])
 def __rtruediv__(self,o):return du(o)/self

def du(x):return x if isinstance(x,Dual) else Dual(x)

def pi_interval():
 # Machin: pi=16 atan(1/5)-4 atan(1/239), alternating rational remainders.
 def at(n,K):
  s=sum((F((-1)**k,(2*k+1)*n**(2*k+1)) for k in range(K)),F(0))
  nextterm=F((-1)**K,(2*K+1)*n**(2*K+1))
  return Iv(min(s,s+nextterm),max(s,s+nextterm))
 p=16*at(5,90)-4*at(239,25)
 # Round outward to manageable rational denominators.
 den=10**90;lo=p.lo*den;hi=p.hi*den
 return Iv(F(lo.numerator//lo.denominator,den),F(-((-hi.numerator)//hi.denominator),den))

def cs(s,n=38):
 # Entire functions cos(sqrt s) and sin(sqrt s)/sqrt s.
 # Taylor remainder bounds hold on the nonnegative real interval.
 if isinstance(s,Iv):
  c=Iv(F((-1)**n,factorial(2*n)));q=Iv(F((-1)**n,factorial(2*n+1)))
  for k in range(n-1,-1,-1):
   c=c*s+F((-1)**k,factorial(2*k));q=q*s+F((-1)**k,factorial(2*k+1))
  assert s.lo>=0
  e=s.hi**(n+1)/factorial(2*n+2);f=s.hi**(n+1)/factorial(2*n+3)
  return c+Iv(-e,e),q+Iv(-f,f)
 c=Decimal((-1)**n)/Decimal(factorial(2*n));q=Decimal((-1)**n)/Decimal(factorial(2*n+1))
 for k in range(n-1,-1,-1):
  c=c*s+Decimal((-1)**k)/Decimal(factorial(2*k));q=q*s+Decimal((-1)**k)/Decimal(factorial(2*k+1))
 return c,q

def quat(x,z):
 s=x*x+z*z;c,q=cs(s.v)
 cd=Dual(c,[-q*a/2 for a in s.d])
 qprime=(c-q)/(2*s.v)
 qd=Dual(q,[qprime*a for a in s.d])
 return cd,x*qd,z*qd

def equations(g,t,pi):
 q1=quat(2*g*t,t/2);q2=quat(9*du(pi)/2-4*g*t,3*du(pi)-t)
 c,a,b=q1;d,e,f=q2;ae=a*e+b*f
 w=d*(2*c*c-1)-2*c*ae
 z=f+2*(c*d-ae)*b
 x=e+2*(c*d-ae)*a
 return w,z,x

def root_and_certificate():
 pi=pi_interval()
 with localcontext() as ctx:
  ctx.prec=80
  p=(Decimal(pi.lo.numerator)/Decimal(pi.lo.denominator)+Decimal(pi.hi.numerator)/Decimal(pi.hi.denominator))/2
  g=Decimal('0.4252917839937362');t=Decimal('7.806164085752481')
  for _ in range(9):
   w,z,_=equations(Dual(g,(Decimal(1),Decimal(0))),Dual(t,(Decimal(0),Decimal(1))),p)
   j00,j01=w.d;j10,j11=z.d;det=j00*j11-j01*j10
   g-=(j11*w.v-j01*z.v)/det;t-=(-j10*w.v+j00*z.v)/det
  gd,td=str(g),str(t)
  # Fifty decimal significant digits are more than enough for radius 1e-24.
  y=[[j11/det,-j01/det],[-j10/det,j00/det]]
  Y=[[F(str(v)) for v in row] for row in y]
 x0=[F(gd),F(td)];radius=F(1,10**24)
 X=[Iv(v-radius,v+radius) for v in x0]
 wi,zi,xi=equations(Dual(X[0],(Iv(1),Iv(0))),Dual(X[1],(Iv(0),Iv(1))),pi)
 J=[wi.d,zi.d]
 f0=equations(Dual(Iv(x0[0])),Dual(Iv(x0[1])),pi)[:2]
 K=[];norm_bound=F(0)
 for i in range(2):
  v=Iv(x0[i])-sum((Y[i][j]*f0[j].v for j in range(2)),Iv(0))
  row_norm=F(0)
  for j in range(2):
   m=Iv(int(i==j))-sum((Y[i][k]*J[k][j] for k in range(2)),Iv(0))
   row_norm+=m.mag();v+=m*Iv(-radius,radius)
  norm_bound=max(norm_bound,row_norm);K.append(v)
 assert all(X[i].lo<K[i].lo and K[i].hi<X[i].hi for i in range(2))
 assert norm_bound<1 and xi.v.hi<0
 return gd,td,dict(method='Exact Fraction interval Krawczyk; Machin pi enclosure; entire Taylor series with rational remainders',root_g1=gd,root_Ut1=td,enclosing_radius='1e-24',krawczyk_contraction_bound=float(norm_bound),krawczyk_radius_about_center=[float(max(abs(k.lo-x0[i]),abs(k.hi-x0[i]))) for i,k in enumerate(K)],positive_x_lower=float(-xi.v.hi),pi_lower=str(pi.lo),pi_upper=str(pi.hi))

def checks():
 gs,ts,cert=root_and_certificate();g=float(gs);t=float(ts)
 T=6*np.pi;t2=T-2*t;g2=(9*np.pi/4-2*g*t)/t2
 m=model(U=1,g=0);D=m['double'];K=m['hop']
 pulses=[(g,t),(g2,t2),(g,t)]
 us=[expm(-1j*(D+gg*K)*tt) for gg,tt in pulses]
 actual=us[2]@us[1]@us[0];ideal=expm(-1j*np.pi/4*K)
 e=actual-ideal
 sensitivities={}
 for what in ['U','g1','g2','time1','time2']:
  deriv=np.zeros((16,16),complex)
  for idx,(gg,tt) in enumerate(pulses):
   dA=np.zeros((16,16),complex)
   if what=='U':dA=-1j*tt*D
   if what=='g1' and idx in [0,2]:dA=-1j*tt*K
   if what=='g2' and idx==1:dA=-1j*tt*K
   if what=='time1' and idx in [0,2]:dA=-1j*(D+gg*K)
   if what=='time2' and idx==1:dA=-1j*(D+gg*K)
   du_=expm_frechet(-1j*(D+gg*K)*tt,dA,compute_expm=False)
   term=du_
   for j in range(idx-1,-1,-1):term=term@us[j]
   for j in range(idx+1,3):term=us[j]@term
   deriv+=term
  sensitivities[what]=float(np.linalg.norm(deriv,2))
 # An exact real sorter follows by diagonal Gaussian site phases before/after
 # the x mixer, or by using the same sequence with a common hopping phase pi/2.
 V=.17
 mv=model(U=1,g=0,V=V);Nv=mv['N'];qphase=expm(-1j*V*T*Nv@(Nv-np.eye(16))/2)
 uv=np.eye(16,dtype=complex)
 for gg,tt in pulses:uv=expm(-1j*(mv['H']+gg*K)*tt)@uv
 number_block={}
 for n in range(5):
  idx=[x for x in range(16) if x.bit_count()==n]
  number_block[str(n)]=float(np.linalg.norm(e[np.ix_(idx,idx)],2))
 return dict(certificate=cert,pulses=[dict(g_over_U=gg,U_time=tt) for gg,tt in pulses],total_U_time=T,total_hop_area=sum(gg*tt for gg,tt in pulses),full_Fock_operator_error=float(np.linalg.norm(e,2)),errors_by_particle_number=number_block,intradimer_V=.17,numberphase_factorization_error=float(np.linalg.norm(uv-qphase@ideal,2)),derivative_operator_norms=sensitivities)

if __name__=='__main__':
 r=checks();Path(__file__).with_name('gaussian_sorter_positive_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
