#!/usr/bin/env python3
from fractions import Fraction as F
from math import isqrt,factorial
from pathlib import Path
import json,hashlib
P=Path(__file__).parent
# Positive Taylor lower sums prove log(200)<6 and log(2,000,000)<15.
assert sum(F(6)**k/factorial(k) for k in range(21))>200
assert sum(F(15)**k/factorial(k) for k in range(51))>2000000
def ceil_sqrt(x,scale=10**12):
 n=isqrt(x.numerator*scale*scale//x.denominator)
 if n*n*x.denominator<x.numerator*scale*scale:n+=1
 y=F(n,scale);assert y*y>=x
 return y
def ceil_q(x,scale=10**9):return F((x.numerator*scale+x.denominator-1)//x.denominator,scale)
def data(x):return {'exact':str(x),'decimal':format(float(x),'.12g')}
rows=[]
for power,t in zip(range(20,26),[10000,15848,25118,39810,63095,100000]):
 assert t**5<=10**power<(t+1)**5
 v=F(1449,800*t)+F(1285200,t**3);j=F(27,25*t)
 row={'N_power10':power,'T_lower':t,'v_upper_exact':str(v),'j_upper_exact':str(j)}
 for tag,ld in [('delta_0p01',6),('delta_1e_minus6',15)]:
  z=j*ld/3;m=z+ceil_sqrt(2*v*ld+z*z);mu=ceil_q(m)
  assert mu>=m
  row[tag]={'Ldelta_upper':ld,'m_upper':data(mu)}
 rows.append(row)
out={'status':'PASS_EXACT_OUTWARD_MARTINGALE_THRESHOLDS','scope':'Conditional full-q martingale only, not total gate failure or clearance interval. Two-sided Freedman with literal upper Ldelta, integer T lower bounds, rational outward square roots.','full_freeze_sha256':hashlib.sha256((P/'FULL_FREEZE.json').read_bytes()).hexdigest(),'examples':rows}
(P/'finite_bracket_examples.json').write_text(json.dumps(out,indent=2)+'\n')
fs=['check_finite_bracket_examples.py','finite_bracket_examples.json']
manifest={'status':'AUTHOR_EXAMPLE_CHECKS','full_freeze_sha256':out['full_freeze_sha256'],'files':[{'file':f,'sha256':hashlib.sha256((P/f).read_bytes()).hexdigest()} for f in fs]}
(P/'EXAMPLES_FREEZE.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(out,indent=2))
