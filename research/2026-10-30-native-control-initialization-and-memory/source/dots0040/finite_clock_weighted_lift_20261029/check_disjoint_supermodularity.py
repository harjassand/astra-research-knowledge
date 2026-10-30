from fractions import Fraction as F
import json
n=6
edges=[(0,1),(0,2),(1,2),(2,3),(3,4),(3,5),(4,5)]
adj={i:set() for i in range(n)}
for i,j in edges:adj[i].add(j);adj[j].add(i)
def connected(A):
 seen={next(iter(A))};todo=list(seen)
 while todo:
  v=todo.pop()
  for u in adj[v]&A-seen:seen.add(u);todo.append(u)
 return seen==A
animals=[m for m in range(1,1<<n) if connected({i for i in range(n) if m>>i&1})]
def f(m,x):
 exponent=9*m.bit_count()-10*(m&~x).bit_count()
 return F(2)**exponent
def V(x):return sum((f(m,x) for m in animals),F(0))
d1=7;d2=56
rows=[]
for x in range(1<<n):
 if (x&d1).bit_count()>=2 and (x&d2).bit_count()>=2:
  cross=V(x^d1^d2)-V(x^d1)-V(x^d2)+V(x)
  assert cross>=0
  rows.append({'x':x,'positive':cross>0})
out={'n_animals':len(animals),'accepted_pair_cases':len(rows),'strictly_positive_cross_terms':sum(r['positive'] for r in rows),'exact_fraction_arithmetic':True}
print(json.dumps(out,indent=2))
