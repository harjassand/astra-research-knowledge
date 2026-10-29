import sympy as s,json
from pathlib import Path
pairs=[(i,j) for i in range(9) for j in range(i,9)];ix={p:k for k,p in enumerate(pairs)}
def poly(terms):
 a=[0]*45
 for i,j,c in terms:a[ix[tuple(sorted((i,j)))]]+=c
 return a
rows=[]
for i in range(3):
 for j in range(i+1,3):
  rows.append(poly([(3*i+k,3*j+k,1) for k in range(3)]))
for i in range(3):
 for j in range(i+1,3):
  rows.append(poly([(3*k+i,3*k+j,1) for k in range(3)]))
for j in [1,2]:
 rows.append(poly([(k,k,1) for k in range(3)]+[(3*j+k,3*j+k,-1) for k in range(3)]))
for j in [1,2]:
 rows.append(poly([(3*k,3*k,1) for k in range(3)]+[(3*k+j,3*k+j,-1) for k in range(3)]))
A=s.Matrix(rows);assert A.rank()==10
Path(__file__).with_suffix('.json').write_text(json.dumps({'constraint_rank':10,'symmetric_feature_dimension':45,'universal_linear_span_upper_bound':35,'relations':rows,'scope':'Universal row/column orthogonality and equal-norm homogeneous identities; combine with author anchor lower bound35.'},indent=2))
print('PASS rank10, universal feature span≤35')
