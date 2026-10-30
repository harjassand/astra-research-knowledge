#!/usr/bin/env python3
import random,heapq,json

def test(seed,n=17):
 rng=random.Random(seed);D=n+1;B={0:0,n-1:3};H=list(range(1,n-1)); Q=8*D+1
 # Integer fixture with extremely forged low values and arbitrary initial ranks.
 z={x:None if rng.random()<.12 else (rng.randrange(-1000,1000),rng.randrange(D+1)) for x in H}
 u={x:min(c+abs(x-b) for b,c in B.items()) for x in H}
 opt={x:min((c+abs(x-b),abs(x-b)) for b,c in B.items()) for x in H}
 legitimate=lambda x,t: t is None or any(t==(c+d,d) and d>=abs(x-b) and (d-abs(x-b))%2==0 for b,c in B.items() for d in [t[1]])
 max_false=[]
 for sweep in range(1,2*D+2):
  order=H[:];rng.shuffle(order)
  # Random extra updates retain sweep semantics.
  order=[rng.choice(H) for _ in range(rng.randrange(n))]+order+[rng.choice(H) for _ in range(rng.randrange(n))]
  for x in order:
   cand=[]
   for y in [x-1,x+1]:
    if y in B:cand.append((B[y]+1,1))
    elif z[y] is not None and z[y][1]<D:cand.append((z[y][0]+1,z[y][1]+1))
   z[x]=min(cand) if cand else None
  false=[t[1] for x,t in z.items() if not legitimate(x,t)]
  assert not false or min(false)>=sweep,(seed,sweep,false,z)
  if sweep==D+1:assert not false
 assert z==opt,(seed,z,opt)
 return {'seed':seed,'sites':n,'D':D,'sweeps':2*D+1,'exact':True}
print(json.dumps({'scope':'Random asynchronous finite-path dirty-state regression, not a whole purge theorem','cases':[test(s) for s in range(100)]},indent=2))
