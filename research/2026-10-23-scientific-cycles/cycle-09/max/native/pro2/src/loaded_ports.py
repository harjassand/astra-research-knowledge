"""Exact star-color interfaces for nonadjacent, disjoint two-terminal modules.

State = (left color, right color, left counts, left flag mask,
         right counts, right flag mask).  The counts have q=4 entries.
This module is a producer, independently challenged in verification/port_lemma.
"""
from functools import lru_cache
from itertools import permutations

Q=4
PERMS=tuple(permutations(range(Q)))

def transform(s,p):
    a,b,n,f,m,g=s
    nn=[0]*Q;mm=[0]*Q;ff=gg=0
    for c in range(Q):
        nn[p[c]]=n[c];mm[p[c]]=m[c]
        if f>>c&1:ff|=1<<p[c]
        if g>>c&1:gg|=1<<p[c]
    return (p[a],p[b],tuple(nn),ff,tuple(mm),gg)

@lru_cache(None)
def canonical(s):
    # Only permutations mapping the first terminal to zero can minimize.
    return min(transform(s,p) for p in PERMS if p[s[0]]==0)

@lru_cache(None)
def orbit(s):
    return tuple(sorted({transform(s,p) for p in PERMS}))

def degrees(s):return sum(s[2]),sum(s[4])

def valid_port(a,n,f):
    return (len(n)==Q and n[a]==0 and not(f>>a&1)
            and 1<=sum(n)<=4 and all(type(k) is int and 0<=k<=4 for k in n)
            and all(not(f>>c&1) or n[c]==1 for c in range(Q)))

def valid(s):
    a,b,n,f,m,g=s
    return valid_port(a,n,f) and valid_port(b,m,g)

def merge(n,f,m,g):
    z=tuple(x+y for x,y in zip(n,m));h=f|g
    if sum(z)>4 or any(z[c]>=2 and (h>>c&1) for c in range(Q)):return None
    return z,h

def series(s,t):
    a,b,n,f,m,g=s;aa,bb,nn,ff,mm,gg=t
    if b!=aa or merge(m,g,nn,ff) is None:return None
    return (a,bb,n,f,mm,gg)

def parallel(s,t):
    a,b,n,f,m,g=s;aa,bb,nn,ff,mm,gg=t
    if (a,b)!=(aa,bb):return None
    l=merge(n,f,nn,ff);r=merge(m,g,mm,gg)
    if l is None or r is None:return None
    return (a,b,l[0],l[1],r[0],r[1])

def extend(s,side,color):
    a,b,n,f,m,g=s
    if side=='R':
        out=extend((b,a,m,g,n,f),'L',color)
        return None if out is None else (out[1],out[0],out[4],out[5],out[2],out[3])
    if side!='L':raise ValueError('side')
    if color==a or sum(n)>3 or (f>>color&1):return None
    z=[0]*Q;z[a]=1
    return (color,b,tuple(z),(1<<a) if n[color] else 0,m,g)

def path2():
    out=set()
    for a in range(Q):
        for b in range(Q):
            for c in range(Q):
                if c in (a,b):continue
                n=tuple(int(i==c) for i in range(Q));f=(1<<c) if a==b else 0
                out.add(canonical((a,b,n,f,n,f)))
    return frozenset(out)

@lru_cache(None)
def expanded(states):
    return tuple(sorted({v for s in states for v in orbit(s)}))

def apply(kind,left,right=None,with_witness=False):
    """Complete canonical parent states, optionally labeled child witnesses.
    Fixing the first child's state up to a global permutation loses no output.
    """
    out={}
    if kind in ('L','R'):
        for s in sorted(left):
            for c in range(Q):
                u=extend(s,kind,c)
                if u is not None:
                    z=canonical(u)
                    if z not in out:
                        p=next(p for p in PERMS if transform(u,p)==z)
                        out[z]=(transform(s,p),p[c])
    else:
        fun=series if kind=='S' else parallel
        bykey={}
        for t in expanded(right):
            key=t[0] if kind=='S' else t[:2]
            bykey.setdefault(key,[]).append(t)
        for s in sorted(left):
            key=s[1] if kind=='S' else s[:2]
            for t in bykey.get(key,[]):
                u=fun(s,t)
                if u is not None:
                    z=canonical(u)
                    if z not in out:
                        p=next(p for p in PERMS if transform(u,p)==z)
                        out[z]=(transform(s,p),transform(t,p))
    return out if with_witness else frozenset(out)

def serialize(s):
    return [s[0],s[1],list(s[2]),s[3],list(s[4]),s[5]]

def deserialize(s):
    return (s[0],s[1],tuple(s[2]),s[3],tuple(s[4]),s[5])

def admissible(kind,d,e=None):
    if kind in ('L','R'):return d[0 if kind=='L' else 1]<=3
    if kind=='S':return d[1]+e[0]<=4
    return d[0]+e[0]<=4 and d[1]+e[1]<=4

def output_degree(kind,d,e=None):
    if kind=='L':return 1,d[1]
    if kind=='R':return d[0],1
    if kind=='S':return d[0],e[1]
    return d[0]+e[0],d[1]+e[1]
