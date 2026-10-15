"""Exact optional strengthening: degree-four products of original voltage bounds."""
from pathlib import Path
from fractions import Fraction as F
import json,itertools
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'EXACT_COUNTEREXAMPLE.json').read_text())
m={(r['k'],r['l']):F(r['value']) for r in d['moments']}
def L(p):return sum(c*m[tuple(sorted(t))] for t,c in p.items())
def multiply(p,q):
 r={}
 for a,c in p.items():
  for b,e in q.items():
   k=(a[0]+b[0],a[1]+b[1]);r[k]=r.get(k,F(0))+c*e
 return r
def bounds(label,square,lo,hi):
 lower=dict(square);lower[(0,0)]=lower.get((0,0),F(0))-lo
 upper={t:-c for t,c in square.items()};upper[(0,0)]=upper.get((0,0),F(0))+hi
 return [(label+'_lower',lower),(label+'_upper',upper)]
basic=[];passive=[]
for label,t in [('x',(2,0)),('y',(0,2)),('u',(-2,0)),('v',(0,-2))]:
 lo,hi=map(F,d['bounds'][label]);basic+=bounds(label,{t:F(1)},lo,hi)
for label,poly,lo,hi in [('x',{(2,0):F(1)},F(1),F(4)),('y',{(0,2):F(1)},F(1),F(4)),('w',{(2,0):F(1),(-2,0):F(1),(0,0):F(-2)},F(1,10000),F(100)),('t',{(0,2):F(1),(0,-2):F(1),(0,0):F(-2)},F(1,10000),F(100))]:
 passive+=bounds(label,poly,lo,hi)
result={}
for name,gs in [('selected_coordinate_embedding',basic),('connected_passive_embedding',passive)]:
 vals=[{'first':a,'second':b,'value':str(L(multiply(p,q)))} for i,(a,p) in enumerate(gs) for b,q in gs[i:]]
 result[name]={'all_nonnegative':all(F(v['value'])>=0 for v in vals),'values':vals}
out={'status':'EXACT_BOUND_PRODUCT_CHECK','arithmetic':'Fraction','original_bounds_per_embedding':8,'products_per_embedding_including_self':36,'results':result,'boundary':'Checks scalar products of pairs of the listed quadratic bounds, as in the degree-four preordering. It does not audit a named QC/RLT/OBBT implementation.'}
(ROOT/'BOUND_PRODUCT_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v['all_nonnegative'] for k,v in result.items()},indent=2))
