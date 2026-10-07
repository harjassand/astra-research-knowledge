"""Owned exact cross-review diagnostics; no peer scripts or peer outputs written."""
import itertools
import json
import random
import time
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

assertions = 0

def check(x):
    global assertions
    assertions += 1
    assert x


def add(a,b):
    return a[0]+b[0],a[1]+b[1]


def mul(a,b):
    return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]


def determinant(a):
    out=(0,0)
    for p in itertools.permutations(range(len(a))):
        z=(1,0)
        for i,j in enumerate(p): z=mul(z,a[i][j])
        s=(-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
        out=add(out,(s*z[0],s*z[1]))
    return out


def squared(z): return z[0]*z[0]+z[1]*z[1]


def variance(a): return Fraction((a[0]-a[1])**2,4)


def energy(a,b,kind):
    out=Fraction(0)
    for x,y in itertools.product((0,1),repeat=2):
        old=a[x]+b[y]
        if kind=='xor':
            nexts=[(xx,yy,Fraction(1,2)) for xx,yy in itertools.product((0,1),repeat=2) if xx^yy==x^y]
        elif kind=='involution': nexts=[(1-y,1-x,Fraction(1))]
        elif kind=='one_refresh':
            nexts=[(xx,y,Fraction(1,4)) for xx in (0,1)]+[(x,yy,Fraction(1,4)) for yy in (0,1)]
        else: raise ValueError(kind)
        for xx,yy,p in nexts:
            out+=Fraction(1,8)*p*(old-a[xx]-b[yy])**2
    return out


def poly_add(a,b):
    c=dict(a)
    for key,v in b.items(): c[key]=c.get(key,0)+v
    return {key:v for key,v in c.items() if v}


def poly_mul(a,b):
    c={}
    for (i,j),x in a.items():
        for (h,l),y in b.items(): c[i+h,j+l]=c.get((i+h,j+l),0)+x*y
    return {key:v for key,v in c.items() if v}


def polynomial_soft_partition():
    import math
    n=6
    f=[[{} for _ in range(n)] for _ in range(n)]
    for i in range(3):
        j=(i+1)%3
        f[i][j]={(1,0):1}; f[i][j+3]={(0,1):-1}
        f[i+3][j]={(0,1):1}; f[i+3][j+3]={(1,0):1}
    @lru_cache(None)
    def minor(rows,cols):
        if not rows: return {(0,0):1}
        ans={}
        for h,j in enumerate(cols):
            if f[rows[0]][j]:
                term=poly_mul(f[rows[0]][j],minor(rows[1:],cols[:h]+cols[h+1:]))
                ans=poly_add(ans,{key:((-1)**h)*v for key,v in term.items()})
        return ans
    total={}; records=[]
    for k in range(n+1):
        for t in itertools.combinations(range(n),k):
            for r in itertools.combinations(range(n),k):
                u=set(range(n))-set(r)
                split=len(u^set(t))
                p=minor(t,r)
                w=poly_mul(p,p)
                records.append((u,set(t),split,p))
                for (i,j),v in w.items(): total[i,j,split]=total.get((i,j,split),0)+v
    total={key:v for key,v in total.items() if v}
    check(all(i%2==j%2==0 for (i,j,_e) in total))
    reduced={}
    for (i,j,e),v in total.items():
        for h in range(i//2+1):
            key=(j//2+h,e)
            reduced[key]=reduced.get(key,0)+v*((-1)**h)*math.comb(i//2,h)
    reduced={key:v for key,v in reduced.items() if v}
    a=[1,-3,6,-4]; b=[0,3,-6,4]
    left={2:36,4:24,6:4}; right={0:2,2:30,4:30,6:2}
    expected={}
    for h in range(4):
        for e,v in left.items(): expected[h,e]=expected.get((h,e),0)+a[h]*v
        for e,v in right.items(): expected[h,e]=expected.get((h,e),0)+b[h]*v
    expected={key:v for key,v in expected.items() if v}
    check(reduced==expected)
    # One exact rational marginal/overlap diagnostic, separately from the
    # coefficient identity above (which is a symbolic identity modulo c²+s²=1).
    z=Fraction(1,4096); c=(1-z*z)/(1+z*z); s=2*z/(1+z*z); eps=Fraction(1,64)
    partition=Fraction(0); hard=Fraction(0); marginals=[Fraction(0) for _ in range(12)]
    for u,t,split,p in records:
        determinant_value=sum(Fraction(v)*c**i*s**j for (i,j),v in p.items())
        weight=determinant_value**2*eps**split
        partition+=weight
        if split==0: hard+=weight
        for i in u: marginals[2*i]+=weight
        for i in t: marginals[2*i+1]+=weight
    aa=c**6+3*c*c*s**4; bb=3*c**4*s*s+s**6
    check(aa+bb==1)
    check(partition==aa*(6*eps+2*eps**3)**2+bb*((1+eps)**6+(eps-1)**6))
    check(hard==2*bb)
    for marginal in marginals: check(marginal==partition/2)
    return {'ordinary_bases_enumerated':len(records),'symbolic_identity_modulo':'c^2+s^2=1',
            'hard_probability':str(hard/partition),'decimal_diagnostic':float(hard/partition),
            'all_column_marginals':'1/2 exactly'}


def main():
    started=time.monotonic()
    for entries in itertools.product(range(-2,3),repeat=4):
        a,b=entries[:2],entries[2:]
        check(variance(a)<=energy(a,b,'xor'))
        check(variance(a)<=2*energy(a,b,'one_refresh'))
        check(variance(a)==energy(a,(0,0),'involution'))
    check(energy((0,1),(0,-1),'involution')==0)
    # The pair-invariant xor function is unchanged at every transition.
    for x,y,xx,yy in itertools.product((0,1),repeat=4):
        if x^y==xx^yy: check((-1)**(x^y)==(-1)**(xx^yy))
    plucker_instances=0
    rng=random.Random(19103)
    for fixture in range(6):
        rank,m=3,6
        v=[[(rng.randrange(-2,3),rng.randrange(-2,3)) for _ in range(m)] for _ in range(rank)]
        bases=list(itertools.combinations(range(m),rank))
        weights={base:squared(determinant([[v[i][j] for j in base] for i in range(rank)])) for base in bases}
        for aa,bb in itertools.product(bases,repeat=2):
            if not weights[aa]*weights[bb]: continue
            a,b=set(aa),set(bb); d=len(b-a)
            for pivot in a-b:
                products=[]
                for j in b-a:
                    ax=tuple(sorted((a-{pivot})|{j})); bx=tuple(sorted((b-{j})|{pivot}))
                    products.append(weights[ax]*weights[bx])
                lhs=weights[aa]*weights[bb]
                check(lhs<=d*sum(products))
                accept=sum(min(Fraction(1),Fraction(w,lhs)) for w in products)/d
                check(accept>=Fraction(1,d*d))
                plucker_instances+=1
    # Exact refutation of the claimed individual-coordinate LP bound.
    for m in (1,2,1000000):
        y=(m,-m,-m)
        check(all(y[i]+y[j]<=0 for i,j in itertools.combinations(range(3),2)))
        check(y[0]>0)
        check(sum(y)<=0)
    soft=polynomial_soft_partition()
    result={'status':'PASS','assertions':assertions,'plucker_and_acceptance_instances':plucker_instances,
            'binary_quantifier_assignments':625,'balance_coordinate_bound':'REFUTED; objective-sum repair valid',
            'soft_overlap':soft,'elapsed_seconds':time.monotonic()-started,
            'scope':'Exact finite diagnostic plus symbolic six-site partition identity; no determinant mixing or general balance acquisition.'}
    Path(__file__).with_name('review_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
