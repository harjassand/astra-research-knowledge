import itertools,math,json,numpy as np
from pathlib import Path
rows=[]
for r in [1,2,3]:
 m=2*r;n=m-1;dim=2**n
 Jz=np.diag([n-2*i.bit_count() for i in range(dim)]);Jp=np.zeros((dim,dim),dtype=np.int64)
 for i in range(dim):
  for bit in range(n):
   if (i>>bit)&1:Jp[i^(1<<bit),i]=1
 targetz=np.diag([1,-1]);targetp=np.array([[0,1],[0,0]],dtype=np.int64)
 effect=np.zeros((2,2),dtype=np.int64);nonzero=0
 for junk in itertools.product(range(r),repeat=m):
  if any(junk.count(a)!=2 for a in range(r)):continue
  M=np.zeros((dim,2),dtype=np.int64)
  for index,bits in enumerate(itertools.product([0,1],repeat=n)):
   for logical in [0,1]:
    cols=[r*b+a for b,a in zip(bits+(logical,),junk)]
    if len(set(cols))!=m:continue
    inv=sum(cols[i]>cols[j] for i in range(m) for j in range(i+1,m))
    newindex=(dim-1)^index
    M[newindex,logical]=(-1)**(inv+n-sum(bits))
  assert np.array_equal(Jz@M,M@targetz)
  assert np.array_equal(Jp@M,M@targetp)
  effect+=M.T@M;nonzero+=1
 assert np.array_equal(effect,(math.factorial(m)//2)*np.eye(2,dtype=int))
 rows.append(dict(junk_dimension=r,program_calls=n,nonzero_junk_strings=nonzero,unnormalized_effect=effect.tolist(),exact_SU2_generator_intertwining=True))
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
