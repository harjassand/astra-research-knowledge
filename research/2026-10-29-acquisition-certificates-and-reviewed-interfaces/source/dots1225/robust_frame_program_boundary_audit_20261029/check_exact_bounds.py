"""Exact sharpness checks for two scalar inequalities, not new hardware claims."""
from fractions import Fraction as F
from pathlib import Path
import json
checks=0
for c in [F(1,100),F(1,7),F(1,2),F(1)]:
 e=c/(1+c)
 # Orthogonal target Choi rays; positive coefficientwise comparison.
 Ja=[1-e,e];Jb=[e,1-e]
 assert all(x-c*y>=0 for x,y in zip(Ja,Jb))
 error=sum(abs(x-y) for x,y in zip(Ja,[1,0]))/2
 assert error==e==c/(1+c);checks+=1
for p,q in [(F(3,4),F(1,2)),(F(2,3),F(1,7)),(F(1),F(1,3))]:
 actual=[q,p-q,1-p];ideal=[q,0,1-q]
 Delta=sum(abs(x-y) for x,y in zip(actual,ideal))/2
 cond=[q/p,(p-q)/p];D=sum(abs(x-y) for x,y in zip(cond,[1,0]))/2
 assert D==Delta/max(p,q);checks+=1
out={'exact_sharpness_checks':checks,'scope':'Sharp under abstract CP-order for orthogonal target rays, and under flagged-state distance respectively; not optimal source-query bounds.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
