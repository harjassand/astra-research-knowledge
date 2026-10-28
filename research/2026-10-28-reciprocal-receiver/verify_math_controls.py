"""Intake-owner exact controls;not producer-code replay or a hardware experiment."""
from fractions import Fraction as F
import json
from pathlib import Path

# Complex rational arithmetic keeps the controls independent of producer modules.
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[0],-a[1])
def sub(a,b):return add(a,neg(b))
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,c):return(a[0]*c,a[1]*c)
def norm2(a):return a[0]*a[0]+a[1]*a[1]
def div(a,b):
 d=norm2(b);assert d
 return scale(mul(a,(b[0],-b[1])),1/d)
Z=(F(0),F(0));ONE=(F(1),F(0))
def psi(c,d):return sub(c,div(mul(d,d),c))if c!=Z else Z
def response(a,s,z,h0=Z):return add(h0,div(scale(a,z),sub(ONE,scale(s,z))))
def intensity(h,reference):return norm2(add(h,reference))/2

def run():
 count=0;r=F(1,2);phases=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
 for x in range(-3,4):
  for y in range(-3,4):
   a=(F(x,64),F(y,64));s=(F(y,10),F(x,10));h0=(F(1,8),F(-1,16))
   hm,hz,hp=[response(a,s,z,h0)for z in[-r,F(0),r]]
   c=scale(sub(hp,hm),1/(2*r));d=scale(sub(add(hp,hm),scale(hz,2)),1/(2*r))
   assert norm2(d)<=r*r*norm2(c)
   assert psi(c,d)==a
   for h in[hm,hz,hp]:
    values=[intensity(h,v)for v in phases]
    assert((values[0]-values[2])/2,(values[1]-values[3])/2)==h
   count+=1
 # Algebraic two-feasible-pair Lipschitz identity,not a floating derivative.
 pairs=[((F(j,11),F(j-2,17)),(F(j,31),F(2-j,41)))for j in range(1,8)]
 for(c,d),(cp,dp)in zip(pairs,pairs[1:]):
  k,kp=div(d,c),div(dp,cp)
  assert sub(psi(c,d),psi(cp,dp))==sub(mul(add(ONE,mul(k,kp)),sub(c,cp)),mul(add(k,kp),sub(d,dp)))
 # Exact one-known-load and uncalibrated-scale witnesses.
 h1=lambda z:F(1,16)*z
 h2=lambda z:F(1,25)*z/(1-F(18,25)*z)
 assert h1(0)==h2(0)==0 and h1(r)==h2(r)==F(1,32)
 assert h1(-r)==-F(1,32)and h2(-r)==-F(1,68)
 for z in[-r,F(0),r]:assert F(1,16)*z==F(1,4)*(z/4)
 # Full twelve-power phase counterfeit,with no target in the true source.
 A=(F(1,10),F(0));k=F(1,5);counterfeit=[]
 for z in[-r,F(0),r]:
  phase=div((F(1),k*z),(F(1),-k*z));assert norm2(phase)==1
  false=scale(phase,F(1,10));actual_phase=(phase[0],-phase[1])
  assert false==response((F(0),F(1,25)),(F(0),k),z,A)
  for v in phases:assert intensity(A,mul(v,actual_phase))==intensity(false,v)
  counterfeit.append({'load':str(z),'phase':[str(v)for v in phase]})
 theta=F(23,2)*F(1,1000)/(1-F(51,100))**2
 assert theta==F(115,2401)<1
 # A conservative rational proof of the dimension constant: sqrt(8)<3.
 assert F(5,2)*3+F(13,4)==F(43,4)<11
 return dict(scope='Exact finite owner controls support these identities only. Complete general arguments are in the source-exposed owner review. No producer module imported/executed;no random sample,measurement,code-archive replay or novelty claim.',complex_rational_residue_cases=count,quadrature_identity_checks=3*count,feasible_pair_identity_checks=len(pairs)-1,one_load_and_scale_witnesses='PASS',twelve_power_counterfeit=counterfeit,shared_calibration_theta=str(theta),all_input_constant_rational_majorant='43/4 < 11')
if __name__=='__main__':
 result=run();path=Path(__file__).resolve().parent/'evaluation/MATH_CONTROLS.json';path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
