from decimal import Decimal,getcontext
import json
from pathlib import Path
getcontext().prec=60;D=Decimal;rows=[]
for eta in [D('.01'),D('.1'),D('.5')]:
 for target in [D('.01'),D('.0001'),D('.000001')]:
  e=8*eta/(1+8*eta);M=D(41481)/140;j=0
  while e>target:
   z=2-2*e+D(9)*e*e/8;M*=4/z;e=e*(1+e/8)/z;j+=1
  rows.append(dict(eta_upper=str(eta),target=str(target),levels=j,uniform_output_error=str(e),uniform_expected_call_bound=str(M),seven_attempt_call_cap=int((2*M).to_integral_value(rounding='ROUND_CEILING'))*7,abort_upper='1/128',scope='Decimal evaluation; obtain rational outward-rounded schedules for deployment'))
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows[:3],indent=2))
