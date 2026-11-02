"""Enumerate every binary subspace through n=5 and all occupied coordinate sets."""
import json
out=[]
for n in range(1,6):
 spaces={frozenset([0])};todo=list(spaces)
 while todo:
  C=todo.pop()
  for v in range(1,1<<n):
   if v in C:continue
   D=C|frozenset(x^v for x in C)
   if D not in spaces:spaces.add(D);todo.append(D)
 max_excess=0.;tests=0
 for qs in [[.17]*n,[.11,.23,.37,.59,.83][:n]]:
  weights=[__import__('math').prod(qs[i] for i in range(n) if x>>i&1) for x in range(1<<n)]
  for C in spaces:
   Z=sum(weights[x] for x in C)
   for T in range(1<<n):
    p=sum(weights[x] for x in C if x&T==T)/Z
    bound=weights[T];max_excess=max(max_excess,p-bound);tests+=1
    assert p<=bound+2e-14
 out.append(dict(n=n,subspaces=len(spaces),support_tests=tests,max_excess=max_excess))
print(json.dumps(out,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(out,indent=2)+'\n')
