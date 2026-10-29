from fractions import Fraction as F
from math import comb
from pathlib import Path
import json,hashlib
rows=[]
for k in [10,20,50,100]:
 p=1-F(1,k);q=1-p
 probs=[]
 for l in range(k//2+1):
  d=comb(k,l)-(comb(k,l-1) if l else 0)
  sch=(p**(k-l+1)*q**l-p**l*q**(k-l+1))/(p-q)
  probs.append(d*sch)
 assert sum(probs)==1
 for j in [0,1,2,4,6]:
  actual=sum(probs[j+1:]);bound=sum(F(comb(k,r))*q**r*p**(k-r) for r in range(j+1,k+1));assert actual<=bound
  rows.append({'k':k,'j':j,'actual_rank2_schur_defect_tail':float(actual),'binomial_upper':float(bound),'pure_block_trace_distance':float(1-p**k)})
x={'status':'exact rational rank2 spectrum check; arbitrary-rank dominance proved separately','rows':rows,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
