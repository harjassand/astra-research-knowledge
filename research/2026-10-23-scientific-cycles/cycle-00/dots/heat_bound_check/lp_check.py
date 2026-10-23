import numpy as np
from scipy.optimize import linprog
rng=np.random.default_rng(182052)
worst=0
for trial in range(1000):
 n=int(rng.integers(1,31))
 a=rng.uniform(0,100,n)
 c=rng.uniform(0,300,n)
 A=np.triu(np.ones((n,n)))
 r=linprog(-np.ones(n),A_ub=A,b_ub=c,bounds=list(zip(np.zeros(n),a)),method='highs')
 bound=min(np.r_[c,0]+np.r_[0,np.cumsum(a)])
 assert r.success
 worst=max(worst,abs(bound+r.fun))
 assert abs(bound+r.fun)<1e-8
print('Independent fractional LP check: 1000 random cases; maximum absolute discrepancy:',worst)
a=np.array([50.,30.,20.]);c=np.array([80.,15.,8.]);r=linprog(-np.ones(3),A_ub=np.triu(np.ones((3,3))),b_ub=c,bounds=list(zip(np.zeros(3),a)),method='highs')
print('Illustrative a=',a.tolist(),'caps=',c.tolist(),'recovered per segment=',r.x.tolist(),'total=',-r.fun,'cut bound=',min(np.r_[c,0]+np.r_[0,np.cumsum(a)]))
