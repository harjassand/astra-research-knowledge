import json
base=[0b1111000,0b1100110,0b1010101]
rows=base[:];n=7;out=[]
def rank(xs):
 d={}
 for x in xs:
  while x:
   k=x.bit_length()-1
   if k in d:x^=d[k]
   else:d[k]=x;break
 return len(d)
for r in range(1,4):
 if r>1:
  old=rows;n0=n;n*=7
  rows=[x<<(j*n0) for j in range(7) for x in old]
  rows += [sum(((1<<n0)-1)<<(j*n0) for j in range(7) if (b>>j)&1) for b in base]
 assert rank(rows)==(n-1)//2
 assert all(x.bit_count()%4==0 for x in rows)
 assert all((x&y).bit_count()%2==0 for x in rows for y in rows)
 ext=rows+[(1<<(n+1))-1]
 assert rank(ext)==(n+1)//2
 typeii=all(x.bit_count()%4==0 for x in ext)
 assert typeii==(r%2==1)
 out.append(dict(r=r,n=n,rank=len(rows),self_orthogonal=True,all_generator_weights_divisible_by_4=True,extended_type_ii=typeii,smallest_displayed_stabilizer_weight=min(x.bit_count() for x in rows)))
print(json.dumps(dict(result='PASS',checks=out,scope='generator algebra only; distance proof is recursive, not enumerated'),indent=2))
