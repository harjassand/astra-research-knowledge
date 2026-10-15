"""Interval Taylor check of LP duals on the full compactified RC half-line.
Uses mpmath interval arithmetic, exact rational dual weights, exact cancellation
of unrestricted series inductance, and a positive measurement-derived mass.
This is an executable mathematical certificate, not a proof-assistant proof.
"""
from pathlib import Path
from fractions import Fraction
import json, time, math
import numpy as np
from mpmath import iv
from compact_model import BASE
iv.dps=35

def I(x):
 if isinstance(x,Fraction): return iv.mpf(x.numerator)/x.denominator
 return iv.mpf(x)
ZERO=I(0); ONE=I(1); TWO=I(2)

def upper(x): return math.nextafter(float(x.b), math.inf)
def lower(x): return math.nextafter(float(x.a), -math.inf)
def mag(x): return max(abs(lower(x)),abs(upper(x)))

class J:
 """Value, first derivative, and second derivative intervals."""
 def __init__(self,v,d=ZERO,dd=ZERO): self.v,self.d,self.dd=v,d,dd
 @staticmethod
 def const(x): return J(I(x))
 def __add__(self,o):
  if not isinstance(o,J): o=J.const(o)
  return J(self.v+o.v,self.d+o.d,self.dd+o.dd)
 __radd__=__add__
 def __neg__(self): return J(-self.v,-self.d,-self.dd)
 def __sub__(self,o): return self+-o if isinstance(o,J) else self+J.const(-o)
 def __rsub__(self,o): return -self+o
 def __mul__(self,o):
  if not isinstance(o,J): o=J.const(o)
  return J(self.v*o.v,self.d*o.v+self.v*o.d,self.dd*o.v+TWO*self.d*o.d+self.v*o.dd)
 __rmul__=__mul__
 def inv(self):
  return J(ONE/self.v,-self.d/self.v**2,TWO*self.d**2/self.v**3-self.dd/self.v**2)
 def __truediv__(self,o):
  if not isinstance(o,J): o=J.const(o)
  return self*o.inv()
 def __rtruediv__(self,o): return self.inv()*o
 def __pow__(self,n):
  if n==0:return J.const(1)
  if n<0:return (self**(-n)).inv()
  if n==1:return self
  h=self**(n//2); r=h*h
  return r*self if n%2 else r
 def exp(self):
  e=iv.exp(self.v); return J(e,e*self.d,e*(self.dd+self.d**2))

def erel(u):
 # E(u) = int_0^1 exp(-u z) dz, including a certified Taylor remainder.
 # Called only for 0 <= u <= 1.1. Series through n=22.
 vals=[]
 for k in range(3):
  term=ONE; out=ZERO
  for n in range(23):
   if n:term=term*(-u.v)/n
   out+=term/(n+k+1)
  # Lagrange remainder of exp(-u z): <= u^23 z^23 / 23! for u>=0.
  import math
  rem=upper(u.v)**23/(math.factorial(23)*(24+k))
  # Slightly enlarge double-derived remainder before embedding it.
  rem=repr(rem*1.00000000000001+1e-40)
  out+=iv.mpf(['-'+rem,rem])
  vals.append(out if k%2==0 else -out)
 return J(vals[0],vals[1]*u.d,vals[2]*u.d**2+vals[1]*u.dd)

def weights_exact(rec,key):
 f=[Fraction(str(z)) for z in rec['frequencies']]
 v=[Fraction(str(z)) for z in rec[key]['weights']]; n=len(f)
 # Enforce sum imaginary coefficient * frequency = 0 exactly.
 pivot=next((j for j in range(n) if v[n+j]),0)
 v[n+pivot]=-sum((v[n+j]*f[j] for j in range(n) if j!=pivot),Fraction(0))/f[pivot]
 assert sum((v[n+j]*f[j] for j in range(n)),Fraction(0))==0
 return f,v

def make_residual(rec,key):
 f,v=weights_exact(rec,key); n=len(f); pairs=[]
 for j in range(n):
  if v[j] or v[n+j]: pairs.append((I(f[j]*100),I(v[j]),I(v[n+j])))
 alpha=I(2)*iv.pi*I(Fraction(str(rec['time_s']))/100)
 sign=1 if key=='lower' else -1
 def evaluate(a,b,jet=True):
  S=J(iv.mpf([a,b]),ONE,ZERO); Q=1-S
  d1=Q*Q+S*S; dh=Q*Q+10000*S*S; B=Q*Q*Q+S*S*(10000-S)
  fac=d1*dh/B
  g=J.const(0)
  for r,vr,vi in pairs:
   g+=(Q*vr-S*(vi*r))/(Q*Q+S*S*(r*r))
  if a==0:
   # Direct range for the fast tail; no derivative is used here.
   umin=alpha*(ONE-I(b))/I(b)
   e=iv.mpf([0,upper(iv.exp(-umin))])
   h=(ONE-e)/(ONE-S.v)
   return sign*(fac.v*(h-g.v))
  u=Q*alpha/S
  if upper(u.v)<=1.1:
   h=J.const(alpha)/S*erel(u)
  else:
   h=(1-(-u).exp())/Q
  out=(h-g)*fac*sign
  return out
 return evaluate,f,v

def verify(rec,key,delta,max_seconds=60.):
 start=time.perf_counter(); ev,f,v=make_residual(rec,key)
 # Exact dyadic cover of [0,1]. The first tiny interval avoids exp at infinity.
 a0=2.**-42
 tail=ev(0.,a0)
 if lower(tail)<-delta:return {'pass':False,'reason':'fast_tail','lower':lower(tail)}
 stack=[(a0,1.)]; count=1; accepted=1; worst=lower(tail); maxdepth=0
 while stack:
  a,b=stack.pop(); m=(a+b)/2; h=math.nextafter(max(m-a,b-m), math.inf)
  full=ev(a,b)
  # Range check first. Dependency overestimation usually benefits from Taylor.
  lb=lower(full.v)
  if lb < -delta:
   center=ev(m,m)
   # Use intervals for Taylor's bound, not a rounded scalar decision.
   deriv=iv.mpf([-mag(center.d),mag(center.d)])
   second=iv.mpf([-mag(full.dd),mag(full.dd)])
   lb=max(lb,lower(center.v+deriv*I(h)+second*I(h)*I(h)/2))
  count+=1
  if lb>=-delta:
   accepted+=1; worst=min(worst,lb); continue
  if b-a<2**-50:return {'pass':False,'reason':'unresolved','interval':[a,b],'lower':lb}
  stack.append((m,b)); stack.append((a,m))
  if time.perf_counter()-start>max_seconds:
   return {'pass':False,'reason':'time_limit','visited':count,'remaining':len(stack),'elapsed_seconds':time.perf_counter()-start}
 # Certified scalar conservative dual bound, evaluated in exact rational arithmetic.
 raw=np.loadtxt(BASE/'data/cell_001_eis.csv',delimiter=',',skiprows=1)
 raw=raw[raw[:,0]<=rec['fmax_hz']]
 y=[Fraction(str(z))*1000 for z in np.r_[raw[:,1],raw[:,2]]]
 eps=Fraction(str(rec['eps_mohm'])); de=Fraction(str(delta))
 dot=sum((vi*yi for vi,yi in zip(v,y)),Fraction(0)); noise=eps*sum(abs(vi) for vi in v)
 n=len(f)
 if de:
  f0=f.index(Fraction(1,100)); f1=f.index(Fraction(1))
  mass=y[f0]-y[n+f0]+Fraction(1,100)*y[n+f1]+eps*Fraction(201,100)
 else:
  mass=Fraction(0) # No mass correction; unused frequencies are not acquired.
 bound=dot-noise-de*mass if key=='lower' else dot+noise+de*mass
 return {'pass':True,'time_s':rec['time_s'],'side':key,'repair_delta':delta,'bound_mohm':float(bound),'bound_exact_rational':str(bound),'mass_upper_mohm':float(mass),'visited_intervals':count,'accepted_intervals':accepted,'elapsed_seconds':time.perf_counter()-start,'worst_interval_lower':worst,'exact_weights':[str(vi) for vi in v], 'arithmetic':'mpmath.iv, 35 decimal digits; rational scalar bound and inductance cancellation'}

if __name__=='__main__':
 rr=json.loads((BASE/'results/compact_lp.json').read_text())[-2:]
 out=[]
 for rec in rr:
  for key in ['lower','upper']:
   r=verify(rec,key,5e-5 if rec['time_s']==10. else .005,max_seconds=50.)
   out.append(r); print({k:z for k,z in r.items() if k not in ['exact_weights','bound_exact_rational']},flush=True)
 (BASE/'results/continuum_certificates.json').write_text(json.dumps(out,indent=2))
