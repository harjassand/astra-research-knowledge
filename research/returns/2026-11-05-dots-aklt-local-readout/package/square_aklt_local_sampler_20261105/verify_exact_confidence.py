from fractions import Fraction as F
from pathlib import Path
import json,mpmath as mp
from exact_confidence import required_attempts,confidence_radius
mp.mp.dps=100
C=F(301805115576299,500964985405440);R=9*C;rows=[]
for alpha in[F(1,20),F(1,100),F(1,1000000)]:
 for eps in[F(1,2),F(1,10),F(1,100),F(1,1000)]:
  n=required_attempts(R,eps,alpha);rad=confidence_radius(R,n,alpha)
  assert rad<=eps
  rr=mp.mpf(R.numerator)/R.denominator;ee=mp.mpf(eps.numerator)/eps.denominator;aa=mp.mpf(alpha.numerator)/alpha.denominator
  assert 2*mp.exp(-2*n*ee*ee/(rr*rr))<=aa
  # Show the integer budget also equals the true high-precision Hoeffding ceiling.
  assert n==int(mp.ceil(rr*rr*mp.log(2/aa)/(2*ee*ee)))
  rows.append({'failure_probability':str(alpha),'requested_error':str(eps),'required_attempts':n,'outward_radius':str(rad)})
Path(__file__).with_name('confidence_checks.json').write_text(json.dumps({'checks':rows,'reference_decimal_digits':100,'all_outward_bounds_passed':True},indent=2)+'\n')
print('All12 exact confidence bounds pass100-digit check.')
