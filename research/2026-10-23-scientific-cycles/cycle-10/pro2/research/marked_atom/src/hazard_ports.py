"""Lossless loaded-port occupancy quotient and monotone guarantee algebra.

Actual terminal degree is retained. Actual per-color multiplicities live in
the realizing coloring and are checked there. Only cross-child occupancy
collisions can create a new repeated-color incident edge at a valid join.
State=(a,b,dL,NL,FL,dR,NR,FR); masks use the actual four-color labels.
"""
from functools import lru_cache
from itertools import permutations
from collections import defaultdict
Q=4
PERMS=tuple(permutations(range(Q)))

def perm_mask(m,p):return sum(1<<p[c] for c in range(Q) if m>>c&1)

def transform(s,p):
    a,b,d,n,f,e,m,g=s
    return (p[a] if a>=0 else -1,p[b] if b>=0 else -1,d,perm_mask(n,p),perm_mask(f,p),e,perm_mask(m,p),perm_mask(g,p))

def project(s):
    a,b,d,n,f,e,m,g=s
    if d==4:a,n,f=-1,0,0
    if e==4:b,m,g=-1,0,0
    return a,b,d,n,f,e,m,g

@lru_cache(None)
def canonical(s):
    s=project(s);a=s[0] if s[0]>=0 else s[1]
    return min(transform(s,p) for p in PERMS if a<0 or p[a]==0)

@lru_cache(None)
def orbit(s):return tuple(sorted({transform(s,p) for p in PERMS}))

@lru_cache(512)
def expanded(states):return tuple(sorted({t for s in states for t in orbit(s)}))

def degrees(s):return s[2],s[5]

def merge(d,n,f,e,m,g):
    if d+e>4 or (n&m&(f|g)):return None
    return d+e,n|m,f|g

def series(s,t):
    a,b,d,n,f,e,m,g=s;aa,bb,dd,nn,ff,ee,mm,gg=t
    if b!=aa or merge(e,m,g,dd,nn,ff) is None:return None
    return a,bb,d,n,f,ee,mm,gg

def parallel(s,t):
    a,b,d,n,f,e,m,g=s;aa,bb,dd,nn,ff,ee,mm,gg=t
    if (a,b)!=(aa,bb):return None
    l=merge(d,n,f,dd,nn,ff);r=merge(e,m,g,ee,mm,gg)
    if l is None or r is None:return None
    return a,b,l[0],l[1],l[2],r[0],r[1],r[2]

def reverse(s):return s[1],s[0],s[5],s[6],s[7],s[2],s[3],s[4]

def extend(s,side,color):
    if side=='R':
        u=extend(reverse(s),'L',color)
        return None if u is None else reverse(u)
    a,b,d,n,f,e,m,g=s
    if d>3 or color==a or f>>color&1:return None
    return color,b,1,1<<a,(1<<a) if n>>color&1 else 0,e,m,g

def path2():
    out=set()
    for a in range(Q):
        for b in range(Q):
            for c in range(Q):
                if c not in (a,b):out.add(canonical((a,b,1,1<<c,(1<<c) if a==b else 0,1,1<<c,(1<<c) if a==b else 0)))
    return frozenset(out)

def apply(kind,left,right=None,with_witness=False):
    out={}
    if kind in ('L','R'):
        for s in sorted(left):
            for c in range(Q):
                u=extend(s,kind,c)
                if u is None:continue
                z=canonical(u)
                if z not in out:
                    p=next(p for p in PERMS if project(transform(u,p))==z)
                    out[z]=(transform(s,p),p[c])
    else:
        fun=series if kind=='S' else parallel;groups=defaultdict(list)
        for t in expanded(right):groups[t[0] if kind=='S' else t[:2]].append(t)
        for s in sorted(left):
            for t in groups[s[1] if kind=='S' else s[:2]]:
                u=fun(s,t)
                if u is None:continue
                z=canonical(u)
                if z not in out:
                    p=next(p for p in PERMS if project(transform(u,p))==z)
                    out[z]=(transform(s,p),transform(t,p))
    return out if with_witness else frozenset(out)

def base(s):return s[0],s[1],s[2],s[5]
def hazard(s):return s[3]|(s[4]<<4)|(s[6]<<8)|(s[7]<<12)
def below(s,t):return base(s)==base(t) and hazard(s)&hazard(t)==hazard(s)

@lru_cache(128)
def groups(states):
    out=defaultdict(list)
    for s in expanded(states):out[base(s)].append(s)
    return dict(out)

def reduce(states):
    gr=defaultdict(set)
    for s in states:
        for t in orbit(s):gr[base(t)].add(t)
    out=set()
    for ss in gr.values():
        keep=[]
        for s in sorted(ss,key=lambda t:(hazard(t).bit_count(),hazard(t))):
            h=hazard(s)
            if not any(k&h==k for k in keep):keep.append(h);out.add(canonical(s))
    return frozenset(out)

@lru_cache(512)
def covers(realizers,targets):
    gr=groups(realizers)
    return all(any(below(t,s) for t in gr.get(base(s),())) for s in targets)

def covering_witness(realizers,target):
    return next(s for s in groups(realizers).get(base(target),()) if below(s,target))

def serialize(s):return list(s)
def deserialize(s):return tuple(s)

def admissible(kind,d,e=None):
    if kind in ('L','R'):return d[0 if kind=='L' else 1]<=3
    if kind=='S':return d[1]+e[0]<=4
    return d[0]+e[0]<=4 and d[1]+e[1]<=4

def output_degree(kind,d,e=None):
    if kind=='L':return 1,d[1]
    if kind=='R':return d[0],1
    if kind=='S':return d[0],e[1]
    return d[0]+e[0],d[1]+e[1]
