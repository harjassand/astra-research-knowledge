from fractions import Fraction as F
from pathlib import Path
import json
def logbounds(x,n=50):
 z=(x-1)/(x+1)
 assert 0<z<1
 lo=2*sum((z**(2*j+1)/F(2*j+1) for j in range(n)),F(0))
 return lo,lo+2*z**(2*n+1)/(F(2*n+1)*(1-z*z))
a,aa=logbounds(F(128,121));b,bb=logbounds(F(625,128));c,cc=logbounds(F(88,25))
upper=8*aa-b-F(2,3)*c+F(42,25)
assert upper<-F(29,100)
# Actual Delta positivity, using log8=3log2 and log(1/8)=-3log2.
l2,h2=logbounds(F(2));l11,h11=logbounds(F(11,4))
delta_lower=F(51,2)*l2-F(33,2)*h11
assert delta_lower>F(98,100)
report={'status':'PASS','J_plus_payment_upper_float':float(upper),'strict_upper':'-29/100','actual_Delta_lower_float':float(delta_lower),'optimal_global_output_bound':'11/4','scope':'faithful isotropic physical3/reference3; sufficient certificate failure only'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
