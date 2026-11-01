"""Exact rational outward qualification of the retained synthetic experiment.
Proof constants: relative primitive-rate error <=1/50;
K=2/sqrt(3)<=7/6. The conservative model factor is 300/293.
"""
from fractions import Fraction as F
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
from pathlib import Path
import json,math
P=Path(__file__).resolve().parent

def exp_lower(x,n=100):
 term=F(1);out=term
 for k in range(1,n+1):term*=x/k;out+=term
 return out

def decimal_out(x,up=False):
 with localcontext() as c:
  c.prec=18;c.rounding=ROUND_CEILING if up else ROUND_FLOOR
  return str(Decimal(x.numerator)/Decimal(x.denominator))

def serial(x):return dict(numerator=str(x.numerator),denominator=str(x.denominator))

def main():
 raw=json.loads((P/'large_results.json').read_text());rows=[]
 fmodel=F(300,293);fscreen=F(21,20);w=F(3,250)
 eps=F(1,50);T=F(raw['calibration_duration']);rate_floor=F(1,2)
 acal=F(2*raw['primitives'])/exp_lower(eps*eps*T*rate_floor/3)
 total=acal
 for row in raw['targets']:
  N=row['trials'];theta=F(row['successes'],N);p=F(1,2**row['target_constraints']);b=1-p
  s=F(row['killing_weight'],10*int(T));R=F(row['relevant_weight'],10*int(T))
  lo=max(F(0),theta-w);hi=min(F(1),theta+w)
  rlo=s+R*lo;rhi=s+R*hi
  low=(1/rhi-p/s)/(p*b*fscreen*fmodel)
  high=(1/rlo-p/s)*fscreen*fmodel/(p*b)
  assert low>0 and low<high
  alpha=F(2)/exp_lower(2*N*w*w);total+=alpha
  rows.append(dict(name=row['name'],target_mass=serial(p),theta_interval=[serial(lo),serial(hi)],
   exact_mean_lower=serial(low),exact_mean_upper=serial(high),
   mean_lower_outward=decimal_out(low),mean_upper_outward=decimal_out(high,True),
   failure_upper_outward=decimal_out(alpha,True),rare_condition=bool(p*(s+R)<=s/2)))
 result=dict(model_factor=serial(fmodel),screening_factor=serial(fscreen),hoeffding_radius=serial(w),
  calibration_failure_upper=decimal_out(acal,True),joint_failure_upper=decimal_out(total,True),
  confidence_lower=decimal_out(1-total),arithmetic='Fraction exact rational; decimal output directed outward',targets=rows)
 (P/'qualified_intervals.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
