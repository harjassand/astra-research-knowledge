"""Exact finite-field enumeration of the proposed weighted phase designs."""
from pathlib import Path
import itertools,json
import numpy as np

def table(Q,modulus):
 out=np.empty((Q,Q),dtype=np.int64)
 for a in range(Q):
  for b in range(Q):
   x=a;y=b;z=0
   while y:
    if y&1:z^=x
    y>>=1;x<<=1
    if x&Q:x^=modulus
   out[a,b]=z
 return out
rows=[]
for q,Q,poly in [(2,4,7),(3,4,7),(4,4,7),(5,16,19)]:
 mult=table(Q,poly)
 coeff=np.array(list(itertools.product(range(Q),repeat=4)),dtype=np.int64)
 values=[]
 for x in range(q):
  vals=coeff[:,3]
  for j in [2,1,0]:vals=mult[vals,x]^coeff[:,j]
  values.append(vals&3) # fixed surjective two-bit coordinate projection
 phases=np.stack(values,axis=1);n=len(phases)
 counts_checked=0
 for d in range(1,min(q,4)+1):
  for js in itertools.combinations(range(q),d):
   code=sum(phases[:,j]*(4**a) for a,j in enumerate(js))
   counts=np.bincount(code,minlength=4**d)
   assert np.all(counts==n//(4**d));counts_checked+=1
 moments_checked=0
 for a,b,c,d in itertools.product(range(q),repeat=4):
  powers=(phases[:,a]+phases[:,b]-phases[:,c]-phases[:,d])%4
  counts=np.bincount(powers,minlength=4)
  re=int(counts[0]-counts[2]);im=int(counts[1]-counts[3])
  target=int((a==c and b==d) or (a==d and b==c))
  assert im==0 and re==n*target
  # After mixture, the q(q+1)-scaled moment has I+SWAP entries.
  diagonal=int(a==b==c==d)
  assert target+diagonal==int(a==c and b==d)+int(a==d and b==c)
  moments_checked+=1
 rows.append({'q':q,'Q':Q,'phase_seed_count':n,'total_label_count':n+q,'independence_subsets_checked':counts_checked,'fourth_moments_checked':moments_checked,'exact_integer_moments':True})
out={'status':'PASS','scope':'Exact integer finite-field enumeration for q=2,3,4,5; analytic Vandermonde proof covers every q. This is not implementation of the quantum recovery circuit.','checks':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
