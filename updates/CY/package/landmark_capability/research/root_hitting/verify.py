"""Exact finite checks; Python standard library only. Not a universal proof."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def solve(a,b):
    a=[list(row)+[v] for row,v in zip(a,b)]
    n=len(b)
    for i in range(n):
        j=next(j for j in range(i,n) if a[j][i])
        a[i],a[j]=a[j],a[i]
        z=a[i][i]; a[i]=[v/z for v in a[i]]
        for j in range(n):
            if j!=i:
                z=a[j][i]
                if z: a[j]=[v-z*w for v,w in zip(a[j],a[i])]
    return [row[-1] for row in a]

def prod(xs):
    out=F(1)
    for x in xs: out*=x
    return out

def hit_transform(p,lam,mu,s):
    n=len(p); target=(1<<n)-1; m=target
    a=[[F(0) for _ in range(m)] for _ in range(m)]; b=[F(0)]*m
    for x in range(m):
        a[x][x]=s
        for i in range(n):
            rate=lam[i]*((1-p[i]) if x>>i&1 else p[i])
            y=x^(1<<i); a[x][x]+=rate
            if y==target: b[x]+=rate
            else: a[x][y]-=rate
    h=solve(a,b)+[F(1)]
    return sum(u*v for u,v in zip(mu,h))

def product_law(r):
    return [prod(r[i] if x>>i&1 else 1-r[i] for i in range(len(r)))
            for x in range(1<<len(r))]

def delay_transform(a,lam,s):
    # CDF product_i(1-a_i exp(-lambda_i t)); includes the atom at zero.
    return sum((-1)**sum(mask)*prod(a[i] for i,z in enumerate(mask) if z)*s/
               (s+sum(lam[i] for i,z in enumerate(mask) if z))
               for mask in product((0,1),repeat=len(a)))

checks=[]
for n in range(1,6):
    p=[F(i+2,i+4) for i in range(n)]
    lam=[F((i+1)**2,i+2) for i in range(n)]
    for variant in range(3):
        r=[p[i]*(F(0) if variant==0 else F(1) if variant==1 else F(i+1,i+3)) for i in range(n)]
        for s in (F(1,7),F(1),F(13,2)):
            lhs=hit_transform(p,lam,product_law(r),s)
            rhs=hit_transform(p,lam,product_law(p),s)*delay_transform([1-r[i]/p[i] for i in range(n)],lam,s)
            assert lhs==rhs
            checks.append({'type':'product','n':n,'variant':variant,'s':str(s),'residual':'0'})

for n in range(2,6):
    p=[F(2,3)]*n; lam=[F(i+1) for i in range(n)]
    subsets=[set(),{0},set(range(n))]; weights=[F(1,5),F(1,3),F(7,15)]
    mu=[F(0)]*(1<<n)
    for subset,w in zip(subsets,weights):
        law=product_law([F(0) if i in subset else p[i] for i in range(n)])
        mu=[u+w*v for u,v in zip(mu,law)]
    for s in (F(1,5),F(3),F(17,2)):
        dt=sum(w*delay_transform([F(int(i in subset)) for i in range(n)],lam,s)
               for subset,w in zip(subsets,weights))
        lhs=hit_transform(p,lam,mu,s)
        rhs=hit_transform(p,lam,product_law(p),s)*dt
        assert lhs==rhs
        checks.append({'type':'correlated_erasure','n':n,'s':str(s),'residual':'0'})

result={'status':'PASS','exact_rational_cases':len(checks),'checks':checks,
        'outside_contract_counterexample':{'n':1,'p':'1/3','r':'2/3','reason':'initial target atom exceeds stationary atom'}}
path=Path(__file__).with_name('verification.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'exact_rational_cases':len(checks)}))
