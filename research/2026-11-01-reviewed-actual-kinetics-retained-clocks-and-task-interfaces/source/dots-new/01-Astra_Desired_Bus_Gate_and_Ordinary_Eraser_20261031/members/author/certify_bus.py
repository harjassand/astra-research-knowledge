"""Exact dyadic interval gate/receiver certificate; no floating functions in proof path."""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import json
BITS=180
SCALE=1<<BITS

def down(x):
 x=Q(x);return Q((x.numerator*SCALE)//x.denominator,SCALE)
def up(x):
 x=Q(x);return -down(-x)
class IV:
 def __init__(self,lo,hi=None):
  self.lo=down(lo);self.hi=up(lo if hi is None else hi);assert self.lo<=self.hi
 def __add__(self,y):
  y=iv(y);return IV(self.lo+y.lo,self.hi+y.hi)
 __radd__=__add__
 def __neg__(self):return IV(-self.hi,-self.lo)
 def __sub__(self,y):return self+-iv(y)
 def __rsub__(self,y):return iv(y)+-self
 def __mul__(self,y):
  y=iv(y);v=[a*b for a in (self.lo,self.hi) for b in (y.lo,y.hi)];return IV(min(v),max(v))
 __rmul__=__mul__
 def __truediv__(self,y):
  y=iv(y);assert y.lo*y.hi>0;return self*IV(1/y.hi,1/y.lo)
 def __rtruediv__(self,y):return iv(y)/self
 def __pow__(self,n):
  assert n>=0 and isinstance(n,int);r=IV(1);a=self
  while n:
   if n&1:r=r*a
   a=a*a;n//=2
  return r
 def record(self):return {'interval':[str(self.lo),str(self.hi)],'decimal_diagnostic':[float(self.lo),float(self.hi)]}
def iv(x):return x if isinstance(x,IV) else IV(x)
def sqrt(x):
 x=iv(x);assert x.lo>=0
 def lower(a):return Q(isqrt((a.numerator*SCALE*SCALE)//a.denominator),SCALE)
 return IV(lower(x.lo),lower(x.hi)+Q(1,SCALE))
def atan_small(x,n=96):
 x=Q(x);s=Q(0)
 for j in range(n):s+=(-1)**j*x**(2*j+1)/(2*j+1)
 t=(-1)**n*x**(2*n+1)/(2*n+1)
 return IV(min(s,s+t),max(s,s+t))
def pi_interval():return 16*atan_small(Q(1,5))-4*atan_small(Q(1,239))
def exp_neg_scalar(x):
 x=Q(x);assert x>=0
 steps=0
 while x>Q(1,8):x/=2;steps+=1
 # Positive exponential Taylor with geometric tail beyond degree 40.
 s=Q(1);t=Q(1)
 for k in range(1,41):t=t*x/k;s+=t
 next_term=t*x/41;tail=next_term/(1-x/42)
 r=1/IV(s,s+tail)
 for _ in range(steps):r=r*r
 return r
def exp_neg(x):
 x=iv(x);assert x.lo>=0
 return IV(exp_neg_scalar(x.hi).lo,exp_neg_scalar(x.lo).hi)

def certify(beta):
 pi=pi_interval();T=2*pi;I=pi/8;beta=Q(beta);W=1/beta
 eta=Q(999,1000);kappa=Q(1,5);gamma=Q(1,10000);h=Q(1,100000);R=Q(5);tz=Q(1,100);other=Q(1,1000)
 D=beta*beta+1;r=exp_neg(beta*T)
 F_inf=(T*(1+beta*beta/(2*D))-(1-r)/(beta*D*D))/24
 tail=(1-r)**2*exp_neg(2*beta*W)/(48*beta*D*D)
 Fw=F_inf-tail;Ac=eta*kappa*Fw;L=kappa*I-Ac
 assert 0<Fw.lo<Fw.hi<I.hi and L.lo>0
 a=exp_neg(2*L);w=1-a;q=1-a**4
 assert q.lo>=2*w.hi, 'this certificate frontend requires the small-loss branch'
 data=4*gamma*(T+W+tz)
 adc=4*sqrt(Ac/2)*h
 saturation=2*exp_neg(R*R)/(R*sqrt(pi))
 total=q+data+adc+saturation+other
 return {'parameters':{'beta':str(beta),'T':'2*pi','W':str(W),'kappa':str(kappa),'eta_detector':str(eta),'ADC_step':str(h),'saturation_R':str(R),'gamma_per_qubit':str(gamma),'correction_time':str(tz),'other_complete_error_allowance':str(other)},'integrated_bus_occupation':I.record(),'captured_fraction':(Fw/I).record(),'captured_displacement_energy':Ac.record(),'inaccessible_displacement_energy':L.record(),'small_loss_margin':(q-2*w).record(),'exact_bus_diamond':q.record(),'continuing_data_upper':data.record(),'ADC_upper':adc.record(),'saturation_upper':saturation.record(),'complete_error_upper':total.record(),'meets_0_01':total.hi<=Q(1,100)}

def main():
 pi=pi_interval();g=sqrt(Q(17,75));slew=Q(53,20)/sqrt(6);I=pi/8
 assert g.hi<Q(477,1000) and slew.hi<Q(1083,1000)
 bare=1-exp_neg(pi/5)
 T=2*pi;ph=pi/8;K2=Q(13,50);drive_cap=Q(477,1000);energy_cap=drive_cap**2*T
 Imin=2*ph**2/(energy_cap+sqrt(energy_cap**2-4*K2*ph**2))
 unmonitored_lower=1-exp_neg(Q(8,5)*Imin)
 a=exp_neg(pi/20);assert (1-a**4).lo>=2*(1-a).hi
 result={'format':'exact-closed-bus-eraser-certificate-v1','scope':'Supplied vacuum linear bus, passive filter, ideal matched quadrature subject to declared ADC and extra error allowance; no acquired hardware','interval_bits':BITS,'pi':pi.record(),'force_peak_upper':g.record(),'force_slew_upper':slew.record(),'integrated_drive_energy':(I*(Q(4,3)+Q(1,100))).record(),'local_Z_coefficient_requirement':(pi/(2*Q(1,100))).record(),'unmonitored_exact_bus_diamond':bare.record(),'all_closed_fixed_B_drive_cap':str(drive_cap),'all_closed_fixed_B_minimum_I':Imin.record(),'all_closed_fixed_B_unmonitored_diamond_lower':unmonitored_lower.record(),'rows':[certify(x) for x in [1,2,4,8,16]]}
 out=Path(__file__).with_name('bus_certificates.json');out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'exact_certificate':out.name,'rows':len(result['rows']),'passing_beta':[r['parameters']['beta'] for r in result['rows'] if r['meets_0_01']],'beta8_complete_upper':result['rows'][3]['complete_error_upper']['decimal_diagnostic'][1]},indent=2))
if __name__=='__main__':main()
