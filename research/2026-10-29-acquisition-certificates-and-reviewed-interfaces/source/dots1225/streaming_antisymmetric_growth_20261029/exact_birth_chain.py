import sys; sys.set_int_max_str_digits(0)
from fractions import Fraction as F
from pathlib import Path
import json
weights=[4480,980,560,350,224,140,80,35];den=10080;budgets=[512,1024,1536,2048,3072,4096];rows=[]
for programs in [1,2]:
 rates=weights*programs;m=len(rates);v=[1]+[0]*m;denpower=1
 for t in range(1,max(budgets)+1):
  new=[0]*(m+1)
  for j in range(m):new[j]+=(den-rates[j])*v[j];new[j+1]+=rates[j]*v[j]
  new[m]+=den*v[m];v=new;denpower*=den
  if t in budgets:
   p=F(v[-1],denpower);rows.append(dict(source_call_cap=t,programs=programs,lower_probability=str(p),lower_probability_float=float(p)))
mean=sum(F(den,w) for w in weights)
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(rates=[str(F(w,den)) for w in weights],expected_calls_one_program_upper=str(mean),rows=rows,scope='Exact conservative birth-chain lower bound for informative memoryless two-axis source; conditional quantum correctness is broader, readiness is not'),indent=2)+'\n')
print('expected',float(mean))
for row in rows:print(row['source_call_cap'],row['programs'],row['lower_probability_float'])
