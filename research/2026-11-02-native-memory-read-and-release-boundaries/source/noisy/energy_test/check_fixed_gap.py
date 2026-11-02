import math,itertools
for q in [.001,.01,.05,.2]:
 p=lambda E:q+(1-2*q)/(1+math.exp(E))
 bc=math.log((1-p(1))/p(1));bh=math.log((1-p(2))/p(2))/2
 m=math.floor(bc/(2*(bc-bh)))+1
 logratio=2*m*(bc-bh)-bc
 print(f'q={q:g}, beta_c={bc:.8g}, beta_h={bh:.8g}, m={m}, log(a/b)={logratio:.8g}')
 assert logratio>0
# Exhaust all source patterns for m=2, simulate predicate-filtered triplet swaps.
m=2;dim=3*m
A=(1,)*m+(0,)*(2*m);B=(0,)*m+(1,)*(2*m)
for x in itertools.product([0,1],repeat=dim):
 f=x in [A,B];y=list(x)
 if f:
  for j in range(m):
   idx=[j,m+2*j,m+2*j+1];t=tuple(y[i] for i in idx)
   if t==(1,0,0):z=(0,1,1)
   elif t==(0,1,1):z=(1,0,0)
   else:continue
   for i,v in zip(idx,z):y[i]=v
 y=tuple(y)
 assert y==(B if x==A else A if x==B else x)
 assert (y in [A,B])==f
 E=lambda x:2*sum(x[:m])+sum(x[m:])
 assert E(x)==E(y)
print('Exhaustive m=2 circuit check: exact A/B swap, predicate invariance, energy conservation passed.')
