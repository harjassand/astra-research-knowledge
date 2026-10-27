from fractions import Fraction as F
from pathlib import Path
import json
def logbounds(x,n=12):
 z=(x-1)/(x+1)
 assert 0<z<1
 lo=2*sum((z**(2*j+1)/F(2*j+1) for j in range(n)),F(0))
 return lo,lo+2*z**(2*n+1)/(F(2*n+1)*(1-z*z))
a,b=logbounds(F(32,25));c,d=logbounds(F(3481,3360))
lo,hi=2*a-14*d,2*b-14*c
assert hi<-F(1,1000)
report={'status':'PASS','J_lower':str(lo),'J_upper':str(hi),'J_upper_float':float(hi),'strict_upper':'-1/1000','scope':'generic commuting equal-trace pair; not physical marginal'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
