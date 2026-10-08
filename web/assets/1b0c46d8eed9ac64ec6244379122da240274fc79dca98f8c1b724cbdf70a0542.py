"""Exact rational stress checks, not a proof or a stochastic simulation."""
from fractions import Fraction as Q
from functools import cmp_to_key
from math import gcd, floor
import json
from pathlib import Path


def arrow(y, p, k=1):
    return (y, (p[0]-y[0], p[1]-y[1]), Q(k))


def dot(x, u):
    return x[0]*u[0]+x[1]*u[1]


def directions(rs):
    """Walls of all source-order and jump-sign changes, plus their sectors."""
    rays = {(1,0), (0,1), (-1,0), (0,-1)}
    def add(x, y):
        if x or y:
            g=gcd(abs(x), abs(y)); rays.add((x//g,y//g)); rays.add((-x//g,-y//g))
    for y,d,k in rs:
        add(-d[1],d[0])
        for z,e,l in rs: add(-(y[1]-z[1]),y[0]-z[0])
    def cmp(u,v):
        a=0 if u[1]>0 or (u[1]==0 and u[0]>0) else 1
        b=0 if v[1]>0 or (v[1]==0 and v[0]>0) else 1
        if a!=b: return -1 if a<b else 1
        cross=u[0]*v[1]-u[1]*v[0]
        return -1 if cross>0 else (1 if cross<0 else 0)
    rays=sorted(rays,key=cmp_to_key(cmp))
    return rays+[(u[0]+v[0],u[1]+v[1]) for u,v in zip(rays,rays[1:]+rays[:1])]


def endotactic(rs):
    for u in directions(rs):
        essential=[(y,d) for y,d,k in rs if dot(d,u)]
        if not essential: continue
        m=max(dot(y,u) for y,d in essential)
        if any(dot(y,u)==m and dot(d,u)>0 for y,d in essential): return False,u
    return True,None


def aggregate(rs, y):
    return tuple(sum((k*d[j] for s,d,k in rs if s==y),Q(0)) for j in (0,1))


def fall(a,n):
    if a<n: return 0
    p=1
    for i in range(n): p*=a-i
    return p


def gen(rs,a,b,V,order=None):
    ans=Q(0)
    for y,d,k in rs:
        if order is not None and sum(y)!=order: continue
        rate=k*fall(a,y[0])*fall(b,y[1])
        if rate: ans+=rate*(V(a+d[0],b+d[1])-V(a,b))
    return ans


def cutoff_case(name,rs):
    assert endotactic(rs)[0], (name,endotactic(rs))
    v=aggregate(rs,(1,2)); h=aggregate(rs,(2,0)); z=aggregate(rs,(1,1))
    G=2*v[0]+v[1]; H=2*h[0]+h[1]; Z=2*z[0]+z[1]
    if G<0:
        p=2+min(Q(1),-G/(2*(max(v[0],0)+1))); q=r=Q(1); regime='I'
    elif H<0:
        p=Q(2); q=r=Q(1); regime='II'
    else:
        assert Z<0
        eps=min(Q(1),-Z/(2*(h[1]+max(z[1],0)+1)))
        p=Q(4); r=Q(2); q=1+eps; regime='III'
    CA=p*v[0]+r*v[1]
    cubic=[a for a in rs if sum(a[0])==3]
    twob=[a for a in rs if a[0]==(0,2)]
    kap=sum((k*(q*(-d[1])-r*max(d[0],0)) for y,d,k in cubic),Q(0))
    TB=2*sum((k*max(q*d[1]+r*d[0],0) for y,d,k in twob),Q(0))
    D=max(abs(d[0]) for y,d,k in rs)
    K=floor(D+TB/kap+1)+1
    f=lambda a:max(a-K,0)
    V=lambda a,b:p*a*a+q*b*b+2*r*b*f(a)
    def bracket(a):
        R=sum((k*(2*p*a*d[0]+p*d[0]**2+q*d[1]**2+2*r*d[1]*f(a+d[0])) for y,d,k in cubic),Q(0))
        g=sum((k*(q*d[1]+r*(f(a+d[0])-f(a))) for y,d,k in cubic),Q(0))
        return R,g
    # The proof needs only finite-a boundedness. A closed envelope avoids
    # enumerating a potentially enormous strip: f>=0 and d_B<=0 there.
    const=sum((k*(p*d[0]**2+q*d[1]**2+2*r*d[0]*d[1]-2*r*K*d[1]) for y,d,k in cubic),Q(0))
    base=sum((k*(p*d[0]**2+q*d[1]**2) for y,d,k in cubic),Q(0))
    rho=-CA if CA<0 else Q(0)
    CR=max(Q(0),const,base+(2*p*max(v[0],0)+rho)*(K+D))
    as_={0,1,2, max(0,K-D),max(0,K-D+1),max(0,K-1),K,K+1,K+D,K+D+1,2*K+2*D,10*K+10*D}
    bs={0,1,2,3,10,100,10000}
    checks=0
    for a in sorted(as_):
        R,g=bracket(a)
        assert g<=-kap
        assert R<=-rho*a+CR
        for b in sorted(bs):
            exact=gen(rs,a,b,V,3)
            assert exact==a*b*(b-1)*(2*b*g+R)
            bound=-rho*a*a*b*b-2*kap*a*b**3+rho*a*a*b+(2*kap+CR)*a*b*b
            assert exact<=bound
            left=gen(twob,a,b,V)
            C2=sum((k*(2*p*a*d[0]+p*d[0]**2+q*d[1]**2) for y,d,k in twob),Q(0))
            assert left<=TB*b**3*(a>K-D)+C2*b*b
            assert TB*b**3*(a>K-D)<=kap*a*b**3
            for y,d,k in rs:
                if a<y[0] or b<y[1]: continue
                rhs=2*p*a*d[0]+p*d[0]**2+2*b*(q*d[1]+r*(f(a+d[0])-f(a)))+q*d[1]**2+2*r*d[1]*f(a+d[0])
                assert V(a+d[0],b+d[1])-V(a,b)==rhs
            checks+=1
    return dict(name=name,regime=regime,K=K,D=D,kappa=str(kap),TB=str(TB),states=checks,directions=len(directions(rs)),full_endotactic=True)


def both_pure_case(name,rs):
    cub=[r for r in rs if sum(r[0])==3]
    assert all(sum(d)<=0 for y,d,k in cub)
    alpha=min(-aggregate(rs,(3,0))[0],-aggregate(rs,(0,3))[1])
    S=sum((k*(abs(d[0])+abs(d[1])) for y,d,k in cub),Q(0))
    H=2*S; Dh=8*S; delta=min(Q(1,4),alpha/Dh)
    loss=next(k*(-sum(d)) for y,d,k in cub if sum(d)<0)
    ell0=loss*delta**3; eps=min(Q(1),ell0/(H+1)); c=min(ell0,eps*alpha)
    assert c>0
    def leading(t):
        F=[sum((k*(1-t)**y[0]*t**y[1]*d[j] for y,d,k in cub),Q(0)) for j in (0,1)]
        ell=-sum(F); h=2*((1-t)*F[0]+t*F[1])
        return ell,h,-2*ell+eps*h
    ts={Q(i,128) for i in range(129)}|{delta,delta/2,delta*2,1-delta,1-delta/2,1-delta*2}
    for t in ts:
        ell,h,L=leading(t)
        assert ell>=0 and abs(h)<=H and L<=-c
        if t<=delta or t>=1-delta: assert h<=-alpha
        else: assert ell>=ell0
    V=lambda a,b:(a+b)**2+eps*(a*a+b*b)
    C3=sum((k*(20*(abs(d[0])+abs(d[1]))+2*(abs(d[0])+abs(d[1]))**2) for y,d,k in cub),Q(0))
    states=0
    for a in [0,1,2,3,10,100,10**6]:
        for b in [0,1,2,3,10,100,10**6]:
            N=a+b
            L=N**4*leading(Q(b,N))[2] if N else Q(0)
            exact=gen(rs,a,b,V,3)
            assert abs(exact-L)<=C3*N**3
            assert exact<=-c*N**4+C3*N**3
            states+=1
    return dict(name=name,angles=len(ts),states=states,delta=str(delta),epsilon=str(eps),coercivity=str(c),positive_coercivity=True)


M=1000
common=[arrow((0,2),(M,2),Q(10**6)),arrow((0,0),(M,M),Q(1,10**12))]
cutoffs=[
 ('G_strict_large_product', [arrow((1,2),(2,0)),arrow((1,2),(1,1),Q(1,10**6)),arrow((2,0),(1,2)),arrow((1,1),(1,2))]+common),
 ('H_strict_large_product', [arrow((1,2),(2,0),Q(1,10**6)),arrow((2,0),(1,1)),arrow((1,1),(1,2))]+common),
 ('Z_strict_large_product', [arrow((1,2),(2,0),Q(1,10**6)),arrow((2,0),(1,2),Q(10**6)),arrow((1,1),(0,2),Q(1,10**6)),arrow((0,2),(1,1))]+common),
]
pure=[
 ('pure_axis_transfer_mixed_loss_large_products',[arrow((3,0),(0,3)),arrow((0,3),(3,0)),arrow((2,1),(1,1),Q(1,10**6)),arrow((2,0),(0,M),10**6),arrow((0,2),(M,0),10**6)]),
 ('extreme_rate_ratios',[arrow((3,0),(0,3),Q(1,10**12)),arrow((0,3),(3,0),10**12),arrow((2,1),(1,1),Q(1,10**12)),arrow((2,0),(0,M),10**12),arrow((0,2),(M,0),10**12)]),
]
controls={
 'diagonal_single_mixed':[arrow((1,2),(0,1)),arrow((0,1),(1,2))],
 'all_w_tiers_zero':[arrow((1,2),(2,0)),arrow((2,0),(1,2)),arrow((0,2),(0,1)),arrow((0,1),(0,2))],
 'mixed_alpha_beta_zero':[arrow((2,1),(2,0)),arrow((2,0),(2,1)),arrow((1,2),(0,2)),arrow((0,2),(1,2))],
 'mixed_beta_zero':[arrow((2,1),(1,1)),arrow((1,1),(2,1)),arrow((1,2),(0,2)),arrow((0,2),(1,2))],
 'mixed_all_total_conservative':[arrow((2,1),(1,2)),arrow((1,2),(2,1)),arrow((2,0),(0,2)),arrow((0,2),(2,0))],
 'pure_all_total_conservative':[arrow((3,0),(0,3)),arrow((0,3),(3,0)),arrow((2,0),(0,2)),arrow((0,2),(2,0))],
 'no_cubic':[arrow((2,0),(0,0)),arrow((0,0),(2,0))],
}
control_results=[]
for name,rs in controls.items():
    assert endotactic(rs)[0]
    if name=='all_w_tiers_zero': assert all(dot(d,(2,1))<=0 for y,d,k in rs if sum(y)>=2)
    if 'total_conservative' in name: assert all(sum(d)==0 for y,d,k in rs)
    control_results.append({'name':name,'full_endotactic':True,'directions':len(directions(rs))})
xu_counter=[arrow((0,0),(1,0)),arrow((1,0),(0,0)),arrow((2,0),(3,0)),arrow((0,3),(0,2))]
assert endotactic(xu_counter)==(False,(1,0))
essential=[(y,d) for y,d,k in xu_counter if sum(d)]
maxdegree=max(sum(y) for y,d in essential)
assert all(sum(d)<0 for y,d in essential if sum(y)==maxdegree)
assert (3,0) not in [y for y,d,k in xu_counter]
out={'method':'Exact Fraction arithmetic; complete finite 2D direction-fan check for named cutoff networks. These diagnostics do not establish universal claims.',
     'cutoff':[cutoff_case(n,r) for n,r in cutoffs],
     'both_pure':[both_pure_case(n,r) for n,r in pure],
     'classification_controls':control_results,
     'xu_example_4_11':{'total_direction_endotactic':True,'full_endotactic':False,'violating_direction':[1,0],'pure_cubic_sources':1,'excluded_from_both_targets':True}}
Path(__file__).with_name('exact_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
