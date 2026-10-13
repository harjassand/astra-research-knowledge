"""Portable stdlib-only exact checks, independent of source acquisition code.

The written proof carries universal claims. These finite checks verify formulas,
strict counterexample inequalities, and implementation details on rational data.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,random,time,itertools,hashlib

ROOT=Path(__file__).resolve().parent

def inverse(a):
    n=len(a); x=[list(row)+[Q(int(i==j)) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k=next(i for i in range(j,n) if x[i][j])
        x[j],x[k]=x[k],x[j]
        z=x[j][j];x[j]=[v/z for v in x[j]]
        for i in range(n):
            if i!=j:
                z=x[i][j];x[i]=[v-z*w for v,w in zip(x[i],x[j])]
    return [row[n:] for row in x]

def dot(x,y):return sum((a*b for a,b in zip(x,y)),Q())
def mv(a,x):return [dot(row,x) for row in a]
def laplacian(edges,c,n):
    a=[[Q() for _ in range(n)] for _ in range(n)]
    for (i,j),v in zip(edges,c):
        a[i][i]+=v
        if j>=0:a[j][j]+=v;a[i][j]-=v;a[j][i]-=v
    return a
def stats(edges,c,m,e):
    k=inverse(laplacian(edges,c,len(m)));u=mv(k,m)
    d=[Q(int(i==edges[e][0])-int(i==edges[e][1])) for i in range(len(m))]
    return dot(m,u),dot(d,u),dot(d,mv(k,d))
def form(edges,c,m):return dot(m,mv(inverse(laplacian(edges,c,len(m))),m))
def serial(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,list):return [serial(y) for y in x]
    if isinstance(x,tuple):return [serial(y) for y in x]
    if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
    return x

def check():
    rng=random.Random(1400264);st=time.perf_counter();count=0;cases=0
    for n in range(2,6):
        for _ in range(6):
            edges=[(i,-1) for i in range(n)]+[(i,j) for i in range(n) for j in range(i+1,n) if rng.random()<.6]
            lo=[Q(rng.randint(1,5),rng.randint(1,5)) for e in edges]
            hi=[v+Q(rng.randint(1,6),rng.randint(1,6)) for v in lo]
            m=[Q(rng.randint(1,5),rng.randint(1,5)) for i in range(n)]
            for e in range(len(edges)):
                H,vm,rm=stats(edges,lo,m,e);L,vp,rp=stats(edges,hi,m,e)
                delta=hi[e]-lo[e]
                for wf in [Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)]:
                    w=delta*wf;D=delta-w
                    gh=D*vm**2/(1+D*rm);gl=D*vp**2/(1-D*rp)
                    worstR=max(H/(L+gl),(H-gh)/L)
                    worstW=H-L-min(gh,gl)
                    endpoints=[]
                    for a,b in [(lo[e],lo[e]+w),(hi[e]-w,hi[e])]:
                        ll=lo.copy();hh=hi.copy();ll[e]=a;hh[e]=b
                        f=form(edges,ll,m);g=form(edges,hh,m);endpoints.append((f/g,f-g))
                    assert worstR==max(x[0] for x in endpoints);count+=1
                    assert worstW==max(x[1] for x in endpoints);count+=1
                    # All main regimes at rational points and all shorter intervals.
                    for pf in [Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)]:
                        for sf in [Q(0),Q(1,2),Q(1)]:
                            sw=w*sf;a=lo[e]+(delta-sw)*pf;b=a+sw
                            ll=lo.copy();hh=hi.copy();ll[e]=a;hh[e]=b
                            f=form(edges,ll,m);g=form(edges,hh,m)
                            assert f/g<=worstR;count+=1
                            assert f-g<=worstW;count+=1
                # Verify ratio-of-quadratic derivative coefficients exactly at p.
                k=Q(4)
                if hi[e]>k*lo[e]:
                    bb=hi.copy();bb[e]=k*lo[e]
                    f0,a0,r=stats(edges,lo,m,e);g0,b0,s=stats(edges,bb,m,e)
                    alpha=f0;beta=f0*r-a0*a0;gamma=g0;dd=k*(g0*s-b0*b0)
                    ns=[alpha,beta+alpha*k*s,beta*k*s]
                    ds=[gamma,dd+gamma*r,dd*r]
                    zz=[ns[1]*ds[0]-ns[0]*ds[1],2*(ns[2]*ds[0]-ns[0]*ds[2]),ns[2]*ds[1]-ns[1]*ds[2]]
                    p=(hi[e]/k-lo[e])/3
                    N=ns[0]+ns[1]*p+ns[2]*p*p;Dt=ds[0]+ds[1]*p+ds[2]*p*p
                    Nd=ns[1]+2*ns[2]*p;Dd=ds[1]+2*ds[2]*p
                    assert Nd*Dt-N*Dd==zz[0]+zz[1]*p+zz[2]*p*p;count+=1
                    ll=lo.copy();hh=hi.copy();ll[e]+=p;hh[e]=k*(lo[e]+p)
                    assert N/Dt==form(edges,ll,m)/form(edges,hh,m);count+=1
            cases+=1
    # Exact factor-relative counterexample, direct independent grounded inversion.
    edges=[(0,-1),(1,-1),(0,1)];m=[Q(2),Q(8)]
    def relative_ratio(a):return form(edges,[Q(1),a,Q(8)],m)/form(edges,[Q(2),4*a,Q(10)],m)
    r0=relative_ratio(Q(1,8));r1=relative_ratio(Q(513,32));ri=relative_ratio(Q(6))
    assert r0==Q(89908,41245);assert r1==Q(1421100,408889);assert ri==Q(5698,1581);count+=3
    assert ri>r0 and ri>r1;count+=2
    # Derivative polynomial has one positive root in the legal interval.
    def pol(a):return 5221*a*a+1968*a-256936
    assert pol(Q(1,8))<0 and pol(Q(513,32))>0;count+=1
    assert 1968>0 and 5221>0;count+=1 # strictly increasing on a>=0
    result={'status':'PASS','scope':'Finite exact checks only; universal result is written proof; no external validation',
            'seed':1400264,'networks':cases,'exact_assertions':count,'seconds':time.perf_counter()-st,
            'relative_noise_counterexample':{'endpoint_low':r0,'endpoint_high':r1,'interior_a':Q(6),'interior_ratio':ri,
                'strict_gap_over_larger_endpoint':ri-max(r0,r1)},
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'independent_check_results.json').write_text(json.dumps(serial(result),indent=2))
    print(json.dumps(serial(result),indent=2))

if __name__=='__main__':check()
