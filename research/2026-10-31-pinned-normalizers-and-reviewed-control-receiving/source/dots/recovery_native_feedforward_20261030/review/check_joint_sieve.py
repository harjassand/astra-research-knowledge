import itertools,math,json
from pathlib import Path
# Two recipient regions each with two terminal decoder events and one gate event.
# Two disjoint computation faults: computation bad iff both occur.
# Region bad iff any of its three local events occurs.
maxerr=0;n=0
for bits in itertools.product((0,1),repeat=8):
 comp=bits[0]*bits[1]
 region=[int(any(bits[2:5])),int(any(bits[5:8]))]
 # exact OR expansion
 vals=[]
 for offset in (2,5):
  v=0
  for mask in range(1,8):
   s=mask.bit_count();prod=1
   for j in range(3):
    if mask>>j&1:prod*=bits[offset+j]
   v+=(-1)**(s-1)*prod
  vals.append(v)
 # at least K regions sieve identity
 for K in (1,2):
  v=0
  for mask in range(1,4):
   s=mask.bit_count()
   if s<K:continue
   prod=1
   for j in range(2):
    if mask>>j&1:prod*=vals[j]
   v+=(-1)**(s-K)*math.comb(s-1,K-1)*prod
  target=int(sum(region)>=K)
  maxerr=max(maxerr,abs(v-target),abs(comp*v-comp*target))
  # split total bad = comp + (1-comp)*tail
  maxerr=max(maxerr,abs(comp+(1-comp)*v-int(comp or target)))
  n+=1
out={'checks':n,'max_exact_identity_residual':maxerr,'scope':'Exact signed disjoint computation/region OR and cardinality identities; no independence probabilities or numerical threshold certification'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
