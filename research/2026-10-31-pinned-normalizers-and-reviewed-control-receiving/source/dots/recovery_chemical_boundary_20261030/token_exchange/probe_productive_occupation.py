"""Exact dynamic equations, floating evaluation; exploratory, not a proof."""
import numpy as np,json,math

def solve(n,m,ell=2):
    T=np.zeros((n+1,n+1)); U=np.zeros_like(T)
    best=(-1,None)
    for y in range(n,-1,-1):
      entry=n-y
      for a in range(y,-1,-1):
        prog=y-a
        kill=math.prod(range(a-m+1,a+1)) if a>=m else 0
        rate=entry+prog+kill
        p=a/(y+ell)
        nt=nu=0.
        if entry:
          nt=entry*((1-p)*T[y+1,a]+(p*T[y+1,a-1] if a else 0))
          nu=entry*((1-p)*U[y+1,a]+(p*U[y+1,a-1] if a else 0))
        if prog:
          nt+=prog*T[y,a+1];nu+=prog*U[y,a+1]
        T[y,a]=(1+nt)/rate
        U[y,a]=(a+nu)/rate
        ratio=T[y,a]/U[y,a]
        if ratio>best[0]:best=(ratio,[a,y])
    return {'n':n,'m':m,'max_T_over_U':best[0], 'argmax_A_Y':best[1],
      'all_source_T':T[0,0], 'all_source_U':U[0,0],
      'scaled_ratio':best[0]*n**(1/(2*m+1)),
      'scale_candidate':'n^(-1/(2m+1)); exploratory only'}
rows=[solve(n,m) for m in [2,4] for n in [20,50,100,200,500]]
print(json.dumps(rows,indent=2))
