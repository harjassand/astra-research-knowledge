"""Fix local qubit bases before constructing the family; do not relabel errors afterward.
Checks both projection column weights and inclusion row weights on degree4 tree resolution.
"""
import json
from sheaf_incidence_compiler import echelon,solve
out=[]
for name,old,new,aux in [('Rep4',[15],[19,28],3),('Par4',[3,5,12],[3,17,12,20],1)]:
 def p2(s):return (s&15)^(aux if s>>4&1 else 0)
 P=[solve(echelon(old),p2(g)) for g in new]
 I=[solve(echelon(new),g) for g in old]
 assert all(x.bit_count()<=1 for x in P)
 rows=[sum(((g>>j)&1)<<i for i,g in enumerate(I)) for j in range(len(new))]
 assert all(x.bit_count()<=1 for x in rows)
 out.append(dict(template=name,old_basis=old,new_basis=new,P1_columns=P,I1_columns=I,max_P1_column_weight=max(map(int.bit_count,P)),max_I1_row_weight=max(map(int.bit_count,rows))))
print(json.dumps(out,indent=2))
