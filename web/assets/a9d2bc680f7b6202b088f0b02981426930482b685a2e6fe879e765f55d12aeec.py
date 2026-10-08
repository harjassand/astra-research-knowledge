from itertools import product
from pathlib import Path
import json
from parity_lift_check import trace

C=[(0,1),(0,2),(0,3)]
D=[(2,3),(1,3),(1,2)]
def tree(edges):
 p=list(range(4))
 def find(x):
  while p[x]!=x:x=p[x]
  return x
 for x,y in edges:
  a,b=find(x),find(y)
  if a==b:return False
  p[a]=b
 return len({find(i) for i in range(4)})==1
bases=[]
for q in product('cd',repeat=3):
 if tree([(C[i] if z=='c' else D[i]) for i,z in enumerate(q)]):bases.append(''.join(q))
assert bases==['ccc','cdd','dcd','ddc']
rows=[]
for word in product('acd',repeat=3):
 rhs=2*sum(all(s=='a' or s==q[i] for i,s in enumerate(word)) for q in bases)
 lhs,_=trace(3,[(0,1),(0,2),(1,2)],word)
 assert lhs==rhs
 rows.append({'selector':''.join(word),'physical_trace':lhs,'common_bases_with_identity_refinements':rhs//2})
res={'C_edges':C,'D_edges':D,'common_bases':bases,'all_27_trace_coefficients_equal':True,'rows':rows,'convention':'C=2|psi+><psi+|, D=XX SWAP; C is not SWAP'}
Path('work/agents/epr_parity/results/triangle_matroid_lift.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'common_bases':bases,'all_27_trace_coefficients_equal':True,'convention':res['convention']},indent=2))
