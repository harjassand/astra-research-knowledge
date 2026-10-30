"""Exhaustive limited CSS path-syndrome comparator, no native simulation."""
import json
out=[]
for n in range(4,20):
 m=n//2
 weights=[]
 for z in range(1<<n):
  syn=[((z>>i)^(z>>(i+1)))&1 for i in range(n-1)]
  if syn==[int(i==m-1) for i in range(n-1)]: weights.append(z.bit_count())
 assert sorted(weights)==sorted([m,n-m]),(n,weights)
 out.append(dict(n=n,flipped_check=m,preimage_weights=sorted(weights),minimum=min(weights)))
print(json.dumps(dict(result='PASS',scope='path CSS sign-selected Z-Pauli feedforward only',cases=out),indent=2))
