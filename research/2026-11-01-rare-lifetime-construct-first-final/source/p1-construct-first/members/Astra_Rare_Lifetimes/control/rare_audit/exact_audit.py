"""Independent Fraction-arithmetic audit of screened hitting and cycle stability."""
from fractions import Fraction as F
from pathlib import Path
import random,json

def zeros(n,m=None):return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]
def solve(a,b):
    n=len(b);a=[list(row)+[b[i]] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if a[i][j])
        a[j],a[pivot]=a[pivot],a[j]
        t=a[j][j];a[j]=[x/t for x in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                t=a[i][j];a[i]=[x-t*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]

def stats(q,pi,a,s):
    n=len(q);a=set(a);b=[i for i in range(n) if i not in a]
    p=sum(pi[i] for i in a);mass=1-p
    l=[[-q[i][j] for j in b] for i in b]
    mean=solve(l,[F(1)]*len(b))
    m=sum(pi[i]*mean[j] for j,i in enumerate(b))/mass
    ls=[[l[i][j]+(s if i==j else 0) for j in range(len(b))]for i in range(len(b))]
    rhs=[sum(q[i][j] for j in a) for i in b]
    ub=solve(ls,rhs)
    u=[F(1)]*n
    for j,i in enumerate(b):u[i]=ub[j]
    flux=sum(pi[i]*sum(q[i][j]*(1-u[j]) for j in b) for i in a)/p
    r=s+flux
    bigr=1/(p*r)-1/s
    stationarity_identity=s*sum(pi[i]*u[i] for i in b)
    assert p*flux==stationarity_identity
    assert p*r==s*sum(pi[i]*u[i] for i in range(n))
    mean_screen=sum(pi[i]*(1-u[i])/s for i in b)/mass
    assert bigr==mass*mean_screen/(1-s*mass*mean_screen)
    return dict(p=p,b=mass,M=m,r=r,R=bigr,flux=flux)

def nonuniform_generator(n,rng):
    weights=[rng.randint(1,9) for _ in range(n)]
    pi=[F(w,sum(weights)) for w in weights]
    nu=F(rng.randint(1,5),7)
    q=zeros(n)
    for i in range(n):
        for j in range(n):
            if i!=j:q[i][j]=nu*pi[j]
    for _ in range(n+2):
        k=rng.randint(2,n)
        cyc=rng.sample(range(n),k)
        flow=F(rng.randint(1,8),11)
        for i,j in zip(cyc,cyc[1:]+cyc[:1]):q[i][j]+=flow/pi[i]
    for i in range(n):q[i][i]=-sum(q[i][j] for j in range(n) if j!=i)
    for j in range(n):assert sum(pi[i]*q[i][j] for i in range(n))==0
    return q,pi,nu

def perm(n,cyc):
    p=list(range(n))
    for i,j in zip(cyc,cyc[1:]+cyc[:1]):p[i]=j
    return p

def from_perms(ps,rates):
    n=len(ps[0]);q=zeros(n)
    for p,rate in zip(ps,rates):
        for i in range(n):q[i][p[i]]+=rate;q[i][i]-=rate
    return q

def main():
    rng=random.Random(271828)
    soft_count=0;cycle_count=0;max_soft_ratio=0;max_cycle_ratio=0
    for n in range(2,10):
        for _ in range(6):
            q,pi,g=nonuniform_generator(n,rng)
            for _ in range(5):
                a=rng.sample(range(n),rng.randint(1,n-1))
                s=g*F(rng.randint(1,20),10)
                z=stats(q,pi,a,s)
                k=1+s/g
                assert z['R']/(z['b']*k)<=z['M']<=k*z['R']/z['b']
                ratio=z['R']/(z['b']*z['M'])
                max_soft_ratio=max(max_soft_ratio,float(max(ratio,1/ratio)))
                soft_count+=1
    e=F(1,5)
    for ell,c2 in [(2,F(1)),(3,F(4,3)),(4,F(2)),(6,F(4))]:
        for n in range(max(3,ell),10):
            for _ in range(5):
                ps=[perm(n,[i,i+1]) for i in range(n-1)]
                ps.extend(perm(n,rng.sample(range(n),rng.randint(2,ell))) for _ in range(n))
                lam=[F(rng.randint(1,9),7) for p in ps]
                pert=[v*(1+e*F(rng.randint(-4,4),4)) for v in lam]
                q=from_perms(ps,lam);qh=from_perms(ps,pert)
                pi=[F(1,n)]*n
                a=rng.sample(range(n),rng.randint(1,n-1))
                x=stats(q,pi,a,F(1,10))['M']
                y=stats(qh,pi,a,F(1,10))['M']
                d2=e*e*c2/(1-e)
                assert (y-x)**2<=d2*x*y
                ratio=y/x;max_cycle_ratio=max(max_cycle_ratio,float(max(ratio,1/ratio)))
                cycle_count+=1
    n=6;q=from_perms([perm(n,list(range(n)))],[F(1)])
    z=stats(q,[F(1,n)]*n,[0],F(1,10))
    assert z['R']>z['b']*z['M']
    monotonicity_counter={k:str(v) for k,v in z.items()}
    n=12
    shift=perm(n,list(range(n)));rev=perm(n,list(reversed(range(n))))
    q=from_perms([shift,rev],[F(1),F(1)])
    qh=from_perms([shift,rev],[1+e,1-e])
    m=stats(q,[F(1,n)]*n,[0],F(1,10))['M']
    mh=stats(qh,[F(1,n)]*n,[0],F(1,10))['M']
    ratio=mh/m
    violates_unit_sector=(mh-m)**2>e*e/(1-e)*m*mh
    assert violates_unit_sector
    result=dict(exact_fraction_screened_checks=soft_count,
        exact_fraction_cycle_perturbation_checks=cycle_count,
        max_observed_two_sided_screened_ratio=max_soft_ratio,
        max_observed_two_sided_rate_ratio=max_cycle_ratio,
        nonmonotone_directed_six_cycle=monotonicity_counter,
        long_cycle_cannot_use_sector_one=dict(N=n,epsilon=str(e),ratio=str(ratio),
            ratio_float=float(ratio),violates_unit_sector=violates_unit_sector),
        scope='Exact finite checks supplement the all-size proof; no empirical process qualification.')
    path=Path(__file__).with_name('exact_audit_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
