import itertools,json,math
from pathlib import Path
n=8;checks=0
for missing in [0,4,8]:
 canonical=[j for j in range(9) if j!=missing]
 for perm in itertools.permutations(canonical):
  a=list(perm);choices=[];parity=0
  for r in range(n,1,-1):
   j=a.index(canonical[r-1]);assert j<r;choices.append((r,j));parity^=int(j!=r-1);a[j],a[r-1]=a[r-1],a[j]
  assert a==canonical
  a=canonical.copy()
  for r,j in reversed(choices):a[j],a[r-1]=a[r-1],a[j]
  assert tuple(a)==perm
  inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));assert parity==inversions%2
  # Every selector sequence is in product radix8*7*...*2, hence bijective by reconstruction.
  assert all(0<=j<r for r,j in choices)
  checks+=1
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(cases=checks,missing_labels=[0,4,8],permutations_per_label=math.factorial(8),inverse_bijection=True,parity_matches=True,selector_qubits=sum((r-1).bit_length() for r in range(2,9)),scope='Exact reversible classical permutation-map check; coherent implementation follows by linearity, no full9^8 dense circuit simulation'),indent=2)+'\n');print(checks)
