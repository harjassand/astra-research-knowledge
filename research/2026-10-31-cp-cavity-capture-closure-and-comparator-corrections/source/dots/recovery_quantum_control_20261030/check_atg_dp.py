import itertools,json
cases=[]
for n,H,L in [(2,[3],4),(3,[3,6],3)]:
 m=len(H)
 syn=lambda d:sum((((h&d).bit_count()&1)<<i) for i,h in enumerate(H))
 best={}
 for cs in itertools.product(range(1<<m),repeat=L):
  for ds in itertools.product(range(1<<n),repeat=L-1):
   y=tuple(cs[j]^cs[j+1]^syn(ds[j]) for j in range(L-1))
   w=sum(x.bit_count() for x in cs+ds)
   best[y]=min(best.get(y,10**9),w)
 for y,opt in best.items():
  V={c:c.bit_count() for c in range(1<<m)}
  for yi in y:
   W={c:10**9 for c in range(1<<m)}
   for c,v in V.items():
    for d in range(1<<n):
     cp=c^syn(d)^yi
     W[cp]=min(W[cp],v+d.bit_count()+cp.bit_count())
   V=W
  assert min(V.values())==opt,(n,H,L,y,opt,V)
 cases.append(dict(n=n,m=m,layers=L,metasyndromes=len(best),result='PASS'))
print(json.dumps(dict(result='PASS',cases=cases,scope='exact serial MW dynamic-program costs; not noisy classical hardware'),indent=2))
