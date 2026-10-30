"""Synthetic screen only: frozen internal-mode average is NOT a recurrence proof."""
import random,json
import sympy as s
from math import prod
x=s.Symbol('x'); rng=random.Random(43017)
def fall(a): return s.prod(x-k for k in range(a))
results=[]
for trial in range(250):
    m=rng.choice([2,3]); C=[(j,a) for j in range(m) for a in range(4)]
    E=[]
    # A base complex cycle ensures weak reversibility and all modes connected.
    for rep in range(rng.randint(1,3)):
        cyc=rng.sample(C,rng.randint(m+1,min(len(C),7)))
        for u,v in zip(cyc,cyc[1:]+cyc[:1]): E.append((u,v,rng.randint(1,5)))
    Q=s.zeros(m); drift=[0]*m
    for (j,a),(k,b),r in E:
        z=r*fall(a); drift[j]+=z*(b-a)
        if j!=k: Q[j,k]+=z;Q[j,j]-=z
    weights=[]
    for j in range(m): weights.append(s.expand((-Q).minor_submatrix(j,j).det()))
    if any(w==0 for w in weights): continue
    num=s.Poly(s.expand(sum(weights[j]*drift[j] for j in range(m))),x)
    sign=0 if num.is_zero else s.sign(num.LC())
    result={'trial':trial,'modes':m,'sign':int(sign),'degree':None if num.is_zero else int(num.degree())}
    if sign>0:
        result.update(edges=E,numerator=str(num.as_expr()),weights=[str(w) for w in weights]);results.append(result);break
    results.append(result)
out={'seed':43017,'tested':len(results),'positive':sum(r['sign']>0 for r in results),'zero':sum(r['sign']==0 for r in results),'negative':sum(r['sign']<0 for r in results),'last':results[-1] if results else None,'warning':'Frozen-phase average only; no universal theorem or recurrence implication.'}
print(json.dumps(out,indent=2))
