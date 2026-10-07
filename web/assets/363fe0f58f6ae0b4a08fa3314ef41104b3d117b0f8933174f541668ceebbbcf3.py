import random, math, sys
n=int(sys.argv[1]) if len(sys.argv)>1 else 12
rounds=int(sys.argv[2]) if len(sys.argv)>2 else 100
best=(0,None)
for trial in range(rounds):
    density=random.random()
    scale=random.choice([0,.2,1,3,8])
    b=[[0.]*n for _ in range(n)]
    for i in range(n):
      for j in range(i):
        if random.random()<density:
          b[i][j]=b[j][i]=math.exp(random.gauss(0,scale))
    h=[0.]*(1<<n); h[0]=1
    a=[0.]*(n//2+1)
    for s in range(1<<n):
      count=s.bit_count()
      if count%2: continue
      if s:
        ib=s&-s;i=ib.bit_length()-1;rem=s^ib;t=rem
        val=0.
        while t:
          jb=t&-t;j=jb.bit_length()-1
          val+=b[i][j]*h[rem^jb]
          t^=jb
        h[s]=val
      a[count//2]+=h[s]**2
    c=[a[k]/math.comb(2*k,k) for k in range(len(a))]
    ratios=[]
    for k in range(1,len(a)-1):
      if c[k]>0 and c[k-1]>0 and c[k+1]>0:
        r=c[k-1]*c[k+1]/c[k]**2
        if r>best[0]:
          best=(r,(trial,k,density,scale,a,b))
          print('BEST',r,'trial,k,dens,scale',trial,k,density,scale,'a',a,flush=True)
print('DONE',best[0],best[1][0:4])
