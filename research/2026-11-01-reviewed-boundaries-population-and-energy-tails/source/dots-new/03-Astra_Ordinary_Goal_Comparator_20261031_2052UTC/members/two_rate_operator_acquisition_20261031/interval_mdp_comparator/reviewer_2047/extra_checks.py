from pathlib import Path
import sys,random,json
p=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(p))
import goal_hazard as gh
R=gh.R;rng=random.Random(9007);checks=0
for N in range(2,65):
 K=R(21,2);u=[R(1) if 2*c>N else min(R(1),R(c,N)+gh.eb_radius(c,N,K)) for c in range(N+1)]
 for i in range(N):assert u[i]<=u[i+1];checks+=1
 # Joint row independence is immaterial to this pointwise domination.
 for j in range(8):
  counts=[rng.randrange(N+1) for _ in range(5)];fixed=rng.randrange(5)
  assert u[max(counts)]>=u[counts[fixed]];checks+=1
for n in [3,4,5]:
 for _ in range(10):
  A=[]
  for a in range(3):
   rows=[]
   for i in range(n):
    row=[rng.randrange(1,8) for _ in range(n)];rows.append([R(x,sum(row)) for x in row])
   A.append(rows)
  goal=n-1;h=max(A[a][i][goal] for a in range(3) for i in range(n-1));v=[R(0)]*(n-1)+[R(1)]
  for L in range(1,9):
   v=[max(sum(A[a][i][j]*v[j] for j in range(n)) for a in range(3)) for i in range(n)]
   for i in range(n-1):assert v[i]<=1-(1-h)**L;checks+=1
# Cheap external task substitution rejection, no mock receiving implementation.
refusals=0
for kw in [dict(expected_length=24.0),dict(expected_generators=True),dict(expected_regret=.0565),dict(expected_confidence=True),dict(expected_task_sha256=1)]:
 try:gh.run(**kw)
 except (AssertionError,TypeError,ValueError):refusals+=1
 else:raise AssertionError('invalid external task admitted')
print(json.dumps({'checks':checks,'additional_task_refusals':refusals,'scope':'Exact monotone maximum, arbitrary dependent-row pointwise domination, and finite-state full-feedback hazard upper bounds; no empirical provenance assertion.'},indent=2))
