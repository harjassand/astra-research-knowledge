from fractions import Fraction as F
import json
rows=[]
for Delta in [F(1),F(1,2),F(1,10),F(1,100)]:
 for eps in [Delta/8,Delta/100]:
  for d in [2,4,100]:
   for n in [1,10,10000]:
    gamma=Delta*eps/(64*d); zeta=Delta*eps/(128*(n+1)); delta=Delta*eps/(256*(n+1))
    Dmin=256*d/(Delta*eps)
    tmin=Delta-d*gamma-zeta
    assert tmin>=Delta/2
    assert 1/Dmin<=gamma/4
    bmax=d/Dmin
    assert bmax/(Delta/2)<=eps/128
    assert tmin-delta>=Delta/2
    outside=(n+1)*2*zeta/Delta
    impl=n*4*delta/Delta+delta
    recovery=2*bmax/(Delta/2)+eps/32
    loss=d*gamma+zeta+recovery+outside+impl+eps/16+eps/16
    assert loss<eps
    rows.append(dict(Delta=str(Delta),epsilon=str(eps),d=d,n=n,overhead_over_epsilon=str(loss/eps)))
print(json.dumps(dict(scope='Exact rational bookkeeping only; not physical simulation or theorem acceptance',cases=len(rows),max_overhead_ratio=str(max(F(x['overhead_over_epsilon']) for x in rows)),rows=rows),indent=2))
