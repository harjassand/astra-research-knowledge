if not __debug__:
    raise RuntimeError("Run without -O / PYTHONOPTIMIZE; validation assertions are required")
"""Integer interval certificate; fixed-N iid fair bits are an explicit assumption."""
from fractions import Fraction as Q
from math import isqrt
import random,sys,time,json
P=320; S=1<<P
n=400; K=128; T=Q(1,5)
a=Q('0.7385658319646086'); p=Q('0.7821972683346718')
def ceildiv(x,y): return -((-x)//y)
class I:
 def __init__(self,l,h=None): self.l=l; self.h=l if h is None else h
 @staticmethod
 def q(q):
  q=Q(q);return I(q.numerator*S//q.denominator,ceildiv(q.numerator*S,q.denominator))
 def __add__(x,y):
  if not isinstance(y,I):y=I.q(y)
  return I(x.l+y.l,x.h+y.h)
 __radd__=__add__
 def __neg__(x):return I(-x.h,-x.l)
 def __sub__(x,y):return x+-asI(y)
 def __mul__(x,y):
  y=asI(y); v=[x.l*y.l,x.l*y.h,x.h*y.l,x.h*y.h];return I(min(v)//S,ceildiv(max(v),S))
 __rmul__=__mul__
 def __truediv__(x,y):
  y=asI(y);assert y.l>0
  pairs=[(x.l*S,y.l),(x.l*S,y.h),(x.h*S,y.l),(x.h*S,y.h)]
  return I(min(a//b for a,b in pairs),max(ceildiv(a,b) for a,b in pairs))
 def sqrt(x):
  assert x.l>=0
  lo=isqrt(x.l*S); hi=isqrt(x.h*S);return I(lo,hi+(hi*hi<x.h*S))
def asI(x):return x if isinstance(x,I) else I.q(x)
LOG2=None
def logpoint(q):
 global LOG2
 q=Q(q);assert q>0
 k=q.numerator.bit_length()-q.denominator.bit_length()
 v=q/(Q(2)**k)
 if v<1:k-=1;v*=2
 assert 1<=v<2
 def series(v):
  y=I.q((v-1)/(v+1)); y2=y*y;term=y;z=I(0)
  for j in range(140):z=z+term/(2*j+1);term=term*y2
  # 2 sum_{j>=140} y^(2j+1)/(2j+1) <= 3*(1/3)^281 < 1/S.
  return I(2*z.l,2*z.h+1)
 z=series(v)
 if k:
  if LOG2 is None:LOG2=series(Q(2))
  z=z+LOG2*k
 return z
def log(x):
 x=asI(x);assert x.l>0
 return I(logpoint(Q(x.l,S)).l,logpoint(Q(x.h,S)).h)
def expneg(x):
 x=asI(x);assert x.h<=0 and x.l>=-2048*S
 # v in [0,1/2]; Taylor through degree100, absolute remainder <1/S.
 v=(-x)/4096; term=I.q(1); z=term
 for j in range(1,101):
  term=term*v/j
  z=z+(-term if j%2 else term)
 z=I(max(0,z.l-1),min(S,z.h+1))
 for _ in range(12):z=z*z
 return I(max(0,z.l),min(S,z.h))
def encode(x):return {'lo':str(Q(x.l,S)),'hi':str(Q(x.h,S)),'approx_lo':float(Q(x.l,S)),'approx_hi':float(Q(x.h,S))}
def prepare():
 F=1-(K+2)*p**(K+1)+(K+1)*p**(K+2)
 cdfs=[];zs=[]
 for lam in [Q(1,2),Q(3,2)]:
  w=[(m+1)*p**m*lam/(lam+a*m) for m in range(K+1)];total=sum(w);zs.append((1-p)**2*total)
  acc=Q(0);thresholds=[]
  for v in w[:-1]:acc+=v;thresholds.append((acc/total*S).__floor__())
  cdfs.append(thresholds)
 norm=(I.q(1/(1-p)-1)+logpoint(1-p))*a
 C=(norm*T).sqrt()*(2*n)
 logF=logpoint(F)
 logM=sum((logpoint(z)*200 for z in zs),I(0))+C-logF*n
 M=expneg(logM)
 bias=n*(1-F)+Q(n*K,S)+Q(n,2**64)+Q(2*n*n*100,2**126)+Q(2*n*3,2**126)+Q(1,2**100)
 bias=Q(I.q(bias).h,S)
 return F,cdfs,C,logF,M,bias,logM

def run(N,seed):
 assert N>=2 and __debug__
 start=time.perf_counter();F,cdfs,C,logF,M,bias,logM=prepare();prep=time.perf_counter()-start
 rng=random.Random(seed);sumz=0;sumz2=0;events=0;exception=0; maxwidth=0
 import bisect
 base=logF*n-C-logpoint(1-p)*(2*n)
 for draw in range(N):
  times=[];bad=False
  for i in range(n):
   m=bisect.bisect_right(cdfs[i//200],rng.getrandbits(P)); rate=Q(1+2*(i//200),2)+a*m
   R=rng.getrandbits(P)
   if R<1<<(P-64):bad=True
   if bad:continue
   U=Q(2*R+1,2*S)
   e=(-logpoint(U))/rate
   # Store midpoint on a 2^-128 grid; check absolute enclosure width.
   midpoint=(e.l+e.h)//2; grid=(midpoint+(1<<(P-129)))>>(P-128)
   assert max(abs((grid<<(P-128))-e.l),abs((grid<<(P-128))-e.h)) <= 1<<(P-127)
   times.append(grid)
  z=0
  if bad:exception+=1
  else:
   ts=sorted(times);tau_num=sum((2*(n-j)-1)*v for j,v in enumerate(ts))
   if 5*tau_num<=n*n*(1<<128):
    events+=1; exponent=base
    for v in times:
     ee=expneg(-I.q(Q(v,1<<128))*a)
     exponent=exponent+log(I.q(1)-ee*p)*2
    # Cauchy-Schwarz proves true exponent <=n logF<0 for this exact candidate event.
    assert exponent.l<=0
    weight=expneg(I(exponent.l,min(0,exponent.h)))
    maxwidth=max(maxwidth,weight.h-weight.l)
    assert weight.h-weight.l<=1<<(P-99)
    z=(weight.l+weight.h)//2
  sumz+=z;sumz2+=z*z
 mean=Q(sumz,N*S);var=Q(sumz2*N-sumz*sumz,N*(N-1)*S*S)
 # exp(4.383)>80 verified by a finite positive Taylor sum.
 x=Q(4383,1000);term=Q(1);s=term
 for j in range(1,40):term=term*x/j;s+=term
 assert s>80
 radius=(I.q(2*var*x/N)).sqrt()+Q(7)*x/(3*(N-1))
 radiusq=Q(radius.h,S)
 lower=max(Q(0),mean-radiusq-bias); upper=min(Q(1),mean+radiusq+bias)
 result={'N':N,'seed':seed,'assumption':'iid fair bits; seeded random.Random is reproducibility only','a':str(a),'p':str(p),'prep_seconds':prep,'total_seconds':time.perf_counter()-start,'events':events,'exceptional_draws':exception,'mean':float(mean),'sample_variance':float(var),'radius_upper':float(radiusq),'bias_upper':float(bias),'bias_exact':str(bias),'M':encode(M),'logM':encode(logM),'probability_interval':{'lo':str(Q(M.l,S)*lower),'hi':str(Q(M.h,S)*upper),'approx_lo':float(Q(M.l,S)*lower),'approx_hi':float(Q(M.h,S)*upper)},'max_weight_interval_width':float(Q(maxwidth,S)),'sum_output_units':str(sumz),'sum_squared_output_units':str(sumz2),'output_scale_bits':P}
 return result
if __name__=='__main__':
 N=int(sys.argv[1]) if len(sys.argv)>1 else 20;seed=int(sys.argv[2]) if len(sys.argv)>2 else 83471
 result=run(N,seed); out=f'/workspace/shared/geometric_failure_certificate/results_{N}_{seed}.json';open(out,'w').write(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
