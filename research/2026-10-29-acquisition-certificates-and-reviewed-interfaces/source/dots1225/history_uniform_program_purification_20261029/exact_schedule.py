"""Finite rational outward-rounded safe schedule, no floating branch decisions."""
from fractions import Fraction as F
import json
from pathlib import Path

def ceilq(q):return -(-q.numerator//q.denominator)
def up(q,b):return F(ceilq(q*(1<<b)),1<<b)
def schedule(eta,target,attempts=7,b=80):
 assert 0<=eta<1 and 0<target<1 and attempts>=1
 e=up(8*eta/(1+8*eta),b); M=up(F(41481,140),b);j=0
 assert e<F(8,9),'increase public precision to resolve the promised gap'
 while e>target:
  den=2-2*e+F(9,8)*e*e
  ne=up(e*(1+e/8)/den,b);nM=up(4*M/den,b)
  assert ne<e,'increase public precision to resolve target'
  e,M=ne,nM;j+=1
 return dict(eta_upper=str(eta),target=str(target),levels=j,uniform_error_upper=str(e),expected_calls_upper=str(M),attempt_call_cap=ceilq(2*M),total_call_cap=attempts*ceilq(2*M),abort_upper=str(F(1,2**attempts)),rounding_bits=b)
if __name__=='__main__':
 rows=[schedule(eta,target) for eta in [F(1,100),F(1,10),F(1,2)] for target in [F(1,100),F(1,10000),F(1,1000000)]]
 Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows[:3],indent=2))
