import numpy as np,itertools
T=[(tuple(j for j in range(5) if j!=i),(-1)**i) for i in range(5)]
def dat(p):
 m={(i,j):int(np.floor(p[j]-p[i]+.5)) for i,j in itertools.combinations(range(5),2)}
 n={(i,j,k):m[j,k]-m[i,k]+m[i,j] for i,j,k in itertools.combinations(range(5),3)}
 q=sum(s*m[a,b]*n[b,c,d] for (a,b,c,d),s in T)
 return q,m,n
rng=np.random.default_rng(2)
for i in range(100000):
 p=rng.random(5);p2=p.copy();p2[0]=rng.random()
 q,m,n=dat(p);q2,m2,n2=dat(p2)
 if abs(q2-q)==1:
  print(p,p2,q,q2,m,m2,n,n2);break
else:print('NONE')
