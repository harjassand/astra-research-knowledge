"""Sound bounded-bit online gap counter; raw certificates retained separately."""
import json,sys,hashlib
from pathlib import Path
from fractions import Fraction as F
sys.set_int_max_str_digits(0)
class Counter:
 def __init__(self,bits,cap):
  assert isinstance(bits,int) and bits>=0;self.bits=bits;self.den=1<<bits;self.cap=F(cap);assert self.cap>=0 and (self.cap*self.den).denominator==1;self.cap_units=int(self.cap*self.den);self.units=0;self.calls=0
 def add(self,gap):
  gap=F(gap);assert 0<=gap<=self.cap;v=gap*self.den;k=(v.numerator+v.denominator-1)//v.denominator;k=min(k,self.cap_units);rounded=F(k,self.den);assert gap<=rounded<=gap+F(1,self.den);self.units+=k;self.calls+=1;return rounded
 def report(self):return dict(bits=self.bits,calls=self.calls,integer_units=str(self.units),integer_counter_bits=max(1,self.units.bit_length()),certified_gap_sum_upper=str(F(self.units,self.den)),maximum_total_rounding_excess=str(F(self.calls,self.den)),public_per_query_cap=str(self.cap))
if __name__=='__main__':
 r=Path(__file__).parent;out={}
 for name in ['offline_query_results.json','bounded_sos_offline_query_results.json']:
  path=r/name;j=json.load(open(path));T=120;b=(T-1).bit_length()+32;cs=[Counter(b,j['public_gap_bound']) for _ in range(3)]
  for row in j['rows']:cs[row['edge']].add(row['certificate']['gap'])
  for e,c in enumerate(cs):
   exact=F(j['per_edge_realized_gap_sums'][e]);assert exact<=F(c.units,c.den)<=exact+F(c.calls,c.den)
  out[name]=dict(source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),per_edge=[c.report() for c in cs])
 # Boundary/error cases are deterministic and independent of researchdata.
 for bits in [0,1,7,40]:
  c=Counter(bits,F(2));assert c.add(0)==0 and c.add(2)==2
  assert c.add(F(1,3))>=F(1,3)
 (r/'dyadic_gap_counter_results.json').write_text(json.dumps(dict(results=out,scope='Exact upward-rounded gap counters only. They do not turn offline observations into a live quantum readiness theorem.'),indent=2)+'\n');print(json.dumps(out,indent=2))
