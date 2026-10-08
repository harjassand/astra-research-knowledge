"""Exact finite checks of algebra and cutoff jumps, not theorem certification."""
from fractions import Fraction as F
from math import ceil
import json


def ff(n, m):
    out = 1
    for j in range(m):
        out *= max(n-j, 0)
    return out


def delta(src, target):
    return tuple(t-s for s, t in zip(src, target))


def agg(reactions, source):
    return tuple(sum(k*delta(s,t)[i] for s,t,k in reactions if s==source)
                 for i in (0,1))


def value(a,b,p,q,r,K):
    return p*a*a+q*b*b+2*r*b*max(a-K,0)


truncated_cases = [
    [((1,2),(1,1),F(1)),((2,0),(1,2),F(1)),
     ((1,1),(2,1),F(1)),((0,2),(1,2),F(1))],
    [((1,2),(2,0),F(1)),((2,0),(1,1),F(1)),
     ((1,1),(2,1),F(1)),((0,2),(1,2),F(1))],
    [((1,2),(2,0),F(1)),((2,0),(1,2),F(1)),
     ((1,1),(0,2),F(1)),((0,2),(1,2),F(1))],
]
cutoff_checks = 0
for index, reactions in enumerate(truncated_cases):
    v=agg(reactions,(1,2)); h=agg(reactions,(2,0)); z=agg(reactions,(1,1))
    G=2*v[0]+v[1]; H=2*h[0]+h[1]; Z=2*z[0]+z[1]
    if index==0:
        d=min(F(1),-G/(2*(max(v[0],0)+1)))
        p,q,r=2+d,F(1),F(1)
    elif index==1:
        p,q,r=F(2),F(1),F(1)
    else:
        e=min(F(1),-Z/(2*(h[1]+max(z[1],0)+1)))
        p,q,r=F(4),1+e,F(2)
    CA=p*v[0]+r*v[1]; HA=p*h[0]+r*h[1]
    HB=r*h[0]+q*h[1]; ZA=p*z[0]+r*z[1]; ZB=r*z[0]+q*z[1]
    assert r<2*q
    if index==0: assert CA<0 and HA<=0
    if index==1: assert CA==0 and HA<0
    if index==2: assert CA==HA==0 and HB+ZA<0 and ZB<0
    kappa=sum(k*(q*(-delta(s,t)[1])-r*max(delta(s,t)[0],0))
              for s,t,k in reactions if s==(1,2))
    assert kappa>0
    D=max(abs(delta(s,t)[0]) for s,t,k in reactions)
    TB=2*sum(k*max(q*delta(s,t)[1]+r*delta(s,t)[0],0)
             for s,t,k in reactions if s==(0,2))
    K=D+ceil(TB/kappa)+2
    for a in range(K+D+6):
        cubic_b_coefficient=F(0)
        for s,t,k in reactions:
            da,db=delta(s,t)
            df=max(a+da-K,0)-max(a-K,0)
            if s==(1,2): cubic_b_coefficient+=k*(q*db+r*df)
            if s==(0,2) and a<=K-D: assert df==0 and q*db+r*df<=0
            if a>K-D: assert TB<=kappa*a
            for b in range(28):
                if a<s[0] or b<s[1]: continue
                direct=value(a+da,b+db,p,q,r,K)-value(a,b,p,q,r,K)
                exact=(2*p*a*da+p*da*da+2*b*(q*db+r*df)
                       +q*db*db+2*r*db*max(a+da-K,0))
                assert direct==exact
                if a>=K+D:
                    linear=(2*a*(p*da+r*db)+2*b*(r*da+q*db)
                            +p*da*da+q*db*db+2*r*da*db-2*r*K*db)
                    assert exact==linear
                cutoff_checks+=1
        if a>=1: assert cubic_b_coefficient<=-kappa

# All aggregate degeneracies in the first mixed-source theorem.
mixed_cases=[((-1,1),(1,-2)),((0,-1),(1,-1)),
             ((-1,1),(-1,0)),((0,-1),(-1,0)),((-1,-1),(-1,-1))]
mixed_checks=0
for u0,v0 in mixed_cases:
    u=tuple(map(F,u0)); v=tuple(map(F,v0)); alpha=-u[0]; beta=-v[1]
    if alpha>0 and beta>0:
        p,q=alpha,beta
        eta=beta*(alpha-u[1])+alpha*(beta-v[0])
    elif alpha==0:
        p,q=F(1),(max(v[0],0)+1)/(-u[1]); eta=F(1)
    else:
        p,q=(max(u[1],0)+1)/(-v[0]),F(1); eta=F(1)
    assert p>0 and q>0 and eta>0
    for a in range(20):
        for b in range(20):
            Q=p*u[0]*a*a+(q*u[1]+p*v[0])*a*b+q*v[1]*b*b
            assert Q<=-eta*a*b
            mixed_checks+=1

# Explicit angular constants in the both-pure-source theorem.
pure=[((3,0),(-1,1),F(1)),((0,3),(1,-1),F(1,1000)),
      ((2,1),(-1,0),F(1,10**6))]
S=sum(k*(abs(da)+abs(db)) for y,(da,db),k in pure)
alpha=min(F(1),F(1,1000)); dh=8*S; HH=2*S
d=min(F(1,4),alpha/dh)
ell0=F(1,10**6)*d**3
e=min(F(1),ell0/(HH+1)); c=min(ell0,e*alpha)
angular_checks=0
for t in [F(i,100) for i in range(101)]+[d/2,d,1-d,1-d/2]:
    fa=sum(k*(1-t)**y[0]*t**y[1]*vec[0] for y,vec,k in pure)
    fb=sum(k*(1-t)**y[0]*t**y[1]*vec[1] for y,vec,k in pure)
    ell=-(fa+fb); hh=2*((1-t)*fa+t*fb)
    assert ell>=0
    if t<=d or t>=1-d: assert hh<=-alpha
    else: assert ell>=ell0
    assert -2*ell+e*hh<=-c
    angular_checks+=1

print(json.dumps({"status":"PASS","arithmetic":"exact rational",
                  "cutoff_jump_checks":cutoff_checks,
                  "mixed_weight_checks":mixed_checks,
                  "angular_constant_checks":angular_checks,
                  "scope":"Finite algebra, cutoff strip and selected bounds only"},indent=2))
