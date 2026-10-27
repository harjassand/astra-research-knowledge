"""Outward-rounded binary64 interval enclosure of the Haar phase integral.
Trigonometric endpoints are certified by exact rational Taylor sums and
a Machin-formula enclosure of pi; no libm trig calls are used.
Every subsequent arithmetic operation is enlarged by np.nextafter.
"""
import numpy as np, math, time, json, sys
from fractions import Fraction
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
NEG=-np.inf; POS=np.inf

def dn(x): return np.nextafter(x,NEG)
def up(x): return np.nextafter(x,POS)
def add(a,b): return (dn(a[0]+b[0]),up(a[1]+b[1]))
def neg(a): return (-a[1],-a[0])
def sub(a,b): return add(a,neg(b))
def mul(a,b):
 p=[a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]]
 return dn(np.minimum.reduce(p)),up(np.maximum.reduce(p))
def scale(a,s):
 return (dn(a[0]*s),up(a[1]*s)) if s>=0 else (dn(a[1]*s),up(a[0]*s))
def square(a):
 l=np.minimum(a[0]*a[0],a[1]*a[1]); l=np.where((a[0]<=0)&(a[1]>=0),0,dn(l))
 return l,up(np.maximum(a[0]*a[0],a[1]*a[1]))
def const(n): return (n,n)
def div(a,b):
 return mul(a,(dn(1/b[1]),up(1/b[0])))
def atan_bounds(q,n):
 # n is odd: alternating partial sum through n is a lower bound.
 assert n%2==1
 s=sum((Fraction((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n+1)),Fraction(0))
 return s,s+Fraction(1,(2*n+3)*q**(2*n+3))
def pi_bounds():
 # Machin: pi = 16 atan(1/5) - 4 atan(1/239).
 a,b=atan_bounds(5,47); c,d=atan_bounds(239,13)
 lo,hi=16*a-4*d,16*b-4*c
 den=2**200
 return Fraction((lo*den).__floor__(),den),Fraction((hi*den).__ceil__(),den)
def fraction_lower(q):
 f=float(q)
 while Fraction.from_float(f)>q: f=math.nextafter(f,-math.inf)
 return f
def fraction_upper(q):
 f=float(q)
 while Fraction.from_float(f)<q: f=math.nextafter(f,math.inf)
 return f
def cos_taylor(q,n):
 s=Fraction(1);t=Fraction(1)
 for j in range(1,n+1):
  t=-t*q*q/((2*j-1)*(2*j));s+=t
 return s
def cosgrid(N):
 # Exact rational Taylor certificates, no floating-point trigonometric calls.
 assert N%4==0
 pl,ph=pi_bounds(); quad=[]
 for k in range(N//4+1):
  if k==0:quad.append((1.,1.));continue
  if k==N//4:quad.append((0.,0.));continue
  # cos decreases on [0,pi/2]. Odd/even Taylor truncations enclose it.
  lower=cos_taylor(2*k*ph/N,21);upper=cos_taylor(2*k*pl/N,20)
  quad.append((fraction_lower(lower),fraction_upper(upper)))
 points=[]
 for k in range(N+1):
  r=k%N
  if r<=N//4: a,b=quad[r]
  elif r<=N//2: b,a=quad[N//2-r];a,b=-a,-b
  elif r<=3*N//4: b,a=quad[r-N//2];a,b=-a,-b
  else:a,b=quad[N-r]
  points.append((a,b))
 lo=[min(points[k][0],points[k+1][0]) for k in range(N)]
 hi=[max(points[k][1],points[k+1][1]) for k in range(N)]
 return np.array(lo+lo),np.array(hi+hi)

def outward_decimal(x, lower):
 with localcontext() as ctx:
  ctx.prec=80
  return str(Decimal.from_float(x).quantize(Decimal('0.000000000000001'),rounding=ROUND_FLOOR if lower else ROUND_CEILING))

def certify(N=1024,block=32):
 assert N in (1024,2048), "Only the requested bounded resolutions are supported."
 assert N%block==0 and (block*N)<2**24
 start=time.monotonic(); cl,ch=cosgrid(N)
 # Fixed, power-of-two bounds on every LOWER AND UPPER interval summand.
 # These are verified below. They bound computed endpoints, not just true values.
 caps={'s':1.,'m1':64.,'m2':32.,'m3_1':32.,'m3_2':32.,'m4_1':16.,'m4_2':16.,'A4':256.,'B4':128.,'C4':64.}
 sums={name:[0.,0.] for name in caps}
 extrem={name:[math.inf,-math.inf] for name in caps}
 max_errors={name:0. for name in caps}
 mindenom=math.inf; minDhi=math.inf
 for i in range(0,N,block):
  ii=np.arange(i,min(i+block,N))[:,None]; jj=np.arange(N)[None,:]
  u=(np.broadcast_to(cl[ii],(len(ii),N)),np.broadcast_to(ch[ii],(len(ii),N)))
  v=(np.broadcast_to(cl[jj],(len(ii),N)),np.broadcast_to(ch[jj],(len(ii),N)))
  w=(np.minimum(cl[ii+jj],cl[ii+jj+1]),np.maximum(ch[ii+jj],ch[ii+jj+1]))
  B=add(const(-9.),sub(scale(u,8.),scale(add(v,w),4.)))
  C=sub(add(scale(u,2.),scale(mul(u,add(v,w)),4.)),add(scale(mul(v,w),2.),scale(add(v,w),4.)))
  D=add(square(B),scale(C,32.))
  # D is nonnegative on the actual cosine torus, by the exact real-root/Gram argument.
  S=(dn(np.sqrt(np.maximum(D[0],0))),up(np.sqrt(np.maximum(D[1],0))))
  den=sub(scale(S,3.),B)
  assert np.all(D[1]>=0)
  assert np.all(den[0]>0), "Denominator positivity not certified on every box."
  mindenom=min(mindenom,float(np.min(den[0])));minDhi=min(minDhi,float(np.min(D[1])))
  shift=div(scale(C,2.),den)
  U=sub(u,shift);V=add(v,scale(shift,2.));W=add(w,scale(shift,2.))
  assert all(np.all(a>=-2.) and np.all(b<=2.) for a,b in (U,V,W))
  tau=scale(add(add(U,V),scale(W,2.)),.5)
  y1=scale(sub(U,V),.5); y2=W
  H=add(square(y1),square(y2))
  # H is a sum of squares, so intersect with the known nonnegative half-line.
  H=(np.maximum(H[0],0.),H[1])
  tau2=square(tau)
  values={'s':square(shift),'m1':mul(tau2,tau),'m2':mul(tau,H),
          'm3_1':mul(tau2,y1),'m3_2':mul(tau2,y2),
          'm4_1':mul(H,y1),'m4_2':mul(H,y2),
          'A4':square(tau2),'B4':mul(tau2,H),'C4':square(H)}
  for name,(lo,hi) in values.items():
   cap=caps[name];count=lo.size;eps=np.finfo(float).eps
   assert np.all(np.isfinite(lo)) and np.all(np.isfinite(hi))
   assert np.all(lo<=hi) and np.all(lo>=-cap) and np.all(hi<=cap), name
   extrem[name][0]=min(extrem[name][0],float(np.min(lo)))
   extrem[name][1]=max(extrem[name][1],float(np.max(hi)))
   # At these resolutions/counts all operations before division below are exact.
   # epsilon is twice binary64 unit roundoff. The nextafter bounds gamma_n sum |x|.
   err=math.nextafter(cap*count*count*eps/(1-count*eps),math.inf)
   max_errors[name]=max(max_errors[name],err)
   sums[name][0]=math.nextafter(sums[name][0]+math.nextafter(float(np.sum(lo))-err,-math.inf),-math.inf)
   sums[name][1]=math.nextafter(sums[name][1]+math.nextafter(float(np.sum(hi))+err,math.inf),math.inf)
 moments={}
 for name,(sl,sh) in sums.items():
  lo=math.nextafter(sl/(N*N),-math.inf);hi=math.nextafter(sh/(N*N),math.inf)
  moments[name]={'lower':lo,'upper':hi,'lower_decimal':outward_decimal(lo,True),'upper_decimal':outward_decimal(hi,False),
                 'lower_hex':lo.hex(),'upper_hex':hi.hex(),'sum_lower_hex':sl.hex(),'sum_upper_hex':sh.hex(),
                 'summand_abs_cap':caps[name],'observed_interval_min':extrem[name][0],'observed_interval_max':extrem[name][1],
                 'max_strip_sum_error':max_errors[name]}
 out={'law':'nu1 = R# (cos x, cos y, cos(x+y)), x,y independent Haar phases',
      'root_map':'shift = 2C/(3sqrt(B^2+32C)-B); R=(u-shift,v+2shift,w+2shift)',
      'coordinate_definitions':{'tau':'(U+V+2W)/2','y1':'(U-V)/2','y2':'W','H':'y1^2+y2^2'},
      'moment_definitions':{'s':'E shift^2','m1':'E tau^3','m2':'E tau H','m3_1':'E tau^2 y1','m3_2':'E tau^2 y2','m4_1':'E H y1','m4_2':'E H y2','A4':'E tau^4','B4':'E tau^2 H','C4':'E H^2'},
      'N':N,'block':block,'phase_boxes':N*N,'omitted_boxes':0,'min_den_lower':mindenom,'min_discriminant_upper':minDhi,
      'moments':moments,'seconds':time.monotonic()-start,
      'arithmetic_model':'IEEE-754 correctly rounded binary64 elementary arithmetic, gradual underflow, exact-rational trigonometric enclosure'}
 print(json.dumps(out,indent=2),flush=True)
 return out
if __name__=='__main__':
 N=int(sys.argv[1]) if len(sys.argv)>1 else 1024
 certify(N)
