"""Exact rational entropy/purity cover for at most five SIC components.
This is interval arithmetic over a complete interval, not a sample grid.
"""
from fractions import Fraction as Q
from math import isqrt
from functools import lru_cache
from pathlib import Path
import json,time,sys
sys.set_int_max_str_digits(0)
OUT=Path(__file__).resolve().parent/'outputs';OUT.mkdir(exist_ok=True)
SQRT_BITS=60;LOG_TERMS=16;counts={'sqrt':0,'log':0}
def point(x):return (Q(x),Q(x))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[1],a[1]-b[0])
def mul(a,b):
 v=[x*y for x in a for y in b];return min(v),max(v)
def scale(a,x):return mul(a,point(x))
@lru_cache(None)
def sqrt_point(x):
 counts['sqrt']+=1;x=Q(x);assert x>=0
 z=isqrt((x.numerator<<(2*SQRT_BITS))//x.denominator);lo=Q(z,1<<SQRT_BITS)
 if lo*lo==x:return lo,lo
 return lo,Q(z+1,1<<SQRT_BITS)
def sqrt_interval(a):return sqrt_point(a[0])[0],sqrt_point(a[1])[1]
def log_series(y):
 z=(y-1)/(y+1);assert 0<=z<=Q(1,3)
 value=2*sum(z**(2*j+1)/Q(2*j+1) for j in range(LOG_TERMS))
 rem=2*z**(2*LOG_TERMS+1)/(Q(2*LOG_TERMS+1)*(1-z*z))
 return value,value+rem
LOG2=log_series(Q(2))
@lru_cache(None)
def log_point(x):
 counts['log']+=1;x=Q(x);assert x>0;y=x;k=0
 while y<1:y*=2;k-=1
 while y>=2:y/=2;k+=1
 return add(log_series(y),scale(LOG2,k))
def log_interval(a):return log_point(a[0])[0],log_point(a[1])[1]
def entropy_term(a):
 lo=max(Q(0),a[0]);hi=min(Q(1),a[1]);assert 0<=lo<=hi<=1
 if hi==0:return point(0)
 if lo==0:
  assert hi<=Q(1,4)
  return Q(0),(-hi*log_point(hi)[0])
 return scale(mul((lo,hi),log_interval((lo,hi))),-1)
def entropy(v):
 ans=point(0)
 for a in v:ans=add(ans,entropy_term(a))
 return ans
@lru_cache(None)
def hmax5(s):
 z=scale(add(point(1),sqrt_point(4*(5*s-1))),Q(1,5))
 small=scale(sub(point(1),z),Q(1,4))
 return add(entropy_term(z),scale(entropy_term(small),4))
@lru_cache(None)
def lmin3(q):
 assert Q(1,3)<=q<1
 if q<Q(1,2):
  a=scale(add(point(2),sqrt_point(6*q-2)),Q(1,6))
  return add(scale(entropy_term(a),2),entropy_term(sub(point(1),scale(a,2))))
 t=scale(add(point(1),sqrt_point(2*q-1)),Q(1,2))
 return entropy([t,sub(point(1),t)])
def bound(lo,hi):
 return 2*lmin3((1+3*hi)/4)[0]-hmax5(lo)[1]
def encode(x):return str(x.numerator)+'/'+str(x.denominator)
def certify():
 start=time.perf_counter();todo=[(Q(1,5),Q(63,64),0)];cells=[];examined=0
 while todo:
  lo,hi,depth=todo.pop();v=bound(lo,hi);examined+=1
  if v>=(1-lo)/128:cells.append((lo,hi,v,depth));continue
  assert depth<24,(lo,hi,v)
  mid=(lo+hi)/2
  todo.extend([(mid,hi,depth+1),(lo,mid,depth+1)])
 cells.sort();assert cells[0][0]==Q(1,5) and cells[-1][1]==Q(63,64)
 for a,b in zip(cells,cells[1:]):assert a[1]==b[0]
 assert all(v>0 for lo,hi,v,d in cells)
 assert all(v>=(1-lo)/128 for lo,hi,v,d in cells)
 c=Q(256,507);tail=Q(11,3)-Q(85,12)*c
 assert tail==Q(137,1521)
 assert tail>=Q(1,128)
 maximum=max(max(x.numerator.bit_length(),x.denominator.bit_length()) for row in cells for x in row[:3])
 result={'scope':'all SIC mixtures on at most five components; full scalar interval',
 'global_quantitative_bound':'Delta >= (1-sum p_i^2)/128',
 'sqrt_bits':SQRT_BITS,'atanh_terms':LOG_TERMS,'cells':len(cells),'examined_cells':examined,
 'max_depth':max(v[3] for v in cells),'minimum_cell_lower_float':float(min(v[2] for v in cells)),
 'maximum_rational_bit_length':maximum,'operation_counts':counts,
 'analytic_tail':{'s_lo':'63/64','s_hi':'1/1','strict_lower':'137/1521 * (1-s)'},
 'elapsed_seconds':time.perf_counter()-start,
 'cover':[{'lo':encode(a),'hi':encode(b),'lower':encode(v),'depth':d} for a,b,v,d in cells]}
 path=OUT/'SIC_SPARSE_INTERVAL_CERTIFICATE.json';path.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='cover'},indent=2))
if __name__=='__main__':certify()
