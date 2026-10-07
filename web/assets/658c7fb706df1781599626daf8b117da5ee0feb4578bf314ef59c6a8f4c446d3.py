"""Exact hard-projected BCS norms by bounded-width Grassmann elimination.

Standard library, rational real/imaginary pairs, no floating point arithmetic.
Public functions: counts(F, allowed, order), width(F, order), min_degree_order(F).
allowed[i] is a subset of {'0','u','d'} physical local occupations.
F contains rational-complex values represented by (Fraction, Fraction).
"""
from fractions import Fraction as Q
from itertools import combinations
import json
import random
import time
from pathlib import Path

ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))

def qc(a=0, b=0):
    return (Q(a), Q(b))

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def neg(a):
    return (-a[0], -a[1])

def mul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])

def conj(a):
    return (a[0], -a[1])

def div(a, b):
    d=b[0]*b[0]+b[1]*b[1]
    return ((a[0]*b[0]+a[1]*b[1])/d,
            (a[1]*b[0]-a[0]*b[1])/d)

def abs2(a):
    return a[0]*a[0]+a[1]*a[1]

def put(p, key, value):
    if value == ZERO:
        return
    v=add(p.get(key, ZERO), value)
    if v == ZERO:
        p.pop(key, None)
    else:
        p[key]=v

def wedge_sign(a, b):
    """Sign to sort all generators of a followed by those of b."""
    parity=0
    aa=a
    while aa:
        bit=aa & -aa
        parity ^= (b & (bit-1)).bit_count() & 1
        aa ^= bit
    return -1 if parity else 1

def product(p, q, stats=None):
    out={}
    for (a, ka), ca in p.items():
        for (b, kb), cb in q.items():
            if a & b:
                continue
            c=mul(ca, cb)
            if wedge_sign(a, b) < 0:
                c=neg(c)
            put(out, (a|b, ka+kb), c)
    if stats is not None:
        stats['products'] += 1
        stats['max_terms'] = max(stats['max_terms'], len(out))
    return out

def linear_edge(a, b, c):
    """1 + c theta_a theta_b, input order retained exactly."""
    if c == ZERO:
        return {(0, 0): ONE}
    if a > b:
        c=neg(c)
    return {(0, 0): ONE, ((1<<a)|(1<<b), 0): c}

def support(F):
    n=len(F)
    adj=[set() for _ in range(n)]
    for i in range(n):
        for j in range(i):
            if F[i][j] != ZERO or F[j][i] != ZERO:
                adj[i].add(j)
                adj[j].add(i)
    return adj

def width(F, order):
    n=len(F)
    if sorted(order) != list(range(n)):
        raise ValueError('order must be a permutation of the sites')
    adj=support(F)
    live=set(range(n))
    w=0
    for v in order:
        ns=adj[v] & live
        w=max(w, len(ns))
        for a, b in combinations(ns, 2):
            adj[a].add(b)
            adj[b].add(a)
        live.remove(v)
    return w

def min_degree_order(F):
    """Acquired heuristic order; no optimal-treewidth promise is asserted."""
    adj=support(F)
    live=set(range(len(F)))
    out=[]
    while live:
        v=min(live, key=lambda u:(len(adj[u]&live), u))
        ns=adj[v]&live
        for a, b in combinations(ns, 2):
            adj[a].add(b)
            adj[b].add(a)
        live.remove(v)
        out.append(v)
    return out

def counts(F, allowed=None, order=None, stats=None):
    n=len(F)
    if any(len(r)!=n for r in F):
        raise ValueError('F must be square')
    if allowed is None:
        allowed=[{'0','u','d'} for _ in range(n)]
    if len(allowed)!=n or any(set(s)-{'0','u','d'} for s in allowed):
        raise ValueError('invalid physical local occupation table')
    if order is None:
        order=min_degree_order(F)
    w=width(F, order)
    if stats is None:
        stats={}
    stats.update({'products':0,'max_terms':0,'width':w,'order':list(order)})
    factors=[]
    # Four generators per site: bar-u,u,bar-d,d, in that order.
    for i in range(n):
        A=3<<(4*i)
        B=12<<(4*i)
        p={}
        if '0' in allowed[i]: p[(A|B, 0)]=ONE
        if 'u' in allowed[i]: p[(B, 1)]=ONE
        if 'd' in allowed[i]: p[(A, 0)]=ONE
        factors.append(({i}, p))
    # Diagonal F is irrelevant under hard projection and is omitted.
    for i in range(n):
        for j in range(n):
            if i==j or F[i][j]==ZERO:
                continue
            e1=linear_edge(4*i, 4*j+3, F[i][j])
            e2=linear_edge(4*j+2, 4*i+1, neg(conj(F[i][j])))
            factors.append(({i,j}, product(e1, e2, stats)))
    for i in order:
        bucket=[]
        rem=[]
        for scope, p in factors:
            (bucket if i in scope else rem).append((scope,p))
        bucket.sort(key=lambda f:len(f[1]))
        p={(0,0):ONE}
        scope=set()
        for sc, q in bucket:
            scope |= sc
            p=product(p,q,stats)
        mask=15<<(4*i)
        out={}
        # Removing a complete four-generator site block has even sign.
        for (a,k),c in p.items():
            if a & mask == mask:
                put(out,(a^mask,k),c)
        scope.discard(i)
        factors=rem+[(scope,out)]
    p={(0,0):ONE}
    for scope,q in factors:
        assert not scope
        p=product(p,q,stats)
    ans=[Q(0) for _ in range(n//2+1)]
    for (a,k),c in p.items():
        assert a==0 and c[1]==0 and c[0]>=0 and k<=n//2
        ans[k] += c[0]
    return ans

def determinant(A):
    A=[list(r) for r in A]
    r=len(A)
    d=ONE
    for j in range(r):
        p=next((i for i in range(j,r) if A[i][j]!=ZERO),None)
        if p is None: return ZERO
        if p!=j:
            A[p],A[j]=A[j],A[p]
            d=neg(d)
        pivot=A[j][j]
        d=mul(d,pivot)
        for i in range(j+1,r):
            a=div(A[i][j],pivot)
            for k in range(j+1,r):
                A[i][k]=add(A[i][k],neg(mul(a,A[j][k])))
    return d

def brute_counts(F,allowed=None):
    n=len(F)
    if allowed is None: allowed=[{'0','u','d'} for _ in range(n)]
    out=[Q(0) for _ in range(n//2+1)]
    for k in range(n//2+1):
        for I in combinations(range(n),k):
            Is=set(I)
            for J in combinations([i for i in range(n) if i not in Is],k):
                Js=set(J)
                if any(('u' if i in Is else 'd' if i in Js else '0')
                       not in allowed[i] for i in range(n)):
                    continue
                out[k] += abs2(determinant([[F[i][j] for j in J] for i in I]))
    return out

def sample(F, k=None, epsilon=Q(1,1000), rng=None, order=None):
    """Finite-random-bit approximate Born self-reduction; no rejection.

    k=None samples the grandcanonical norm at fugacity one. Otherwise use
    exactly the requested canonical sector. Error bound: TV <= epsilon.
    The exact width-dependent counter is called at most 3n+1 times.
    """
    n=len(F)
    if not 0 < epsilon <= 1:
        raise ValueError('epsilon must be in (0,1]')
    if k is not None and not 0 <= k <= n//2:
        raise ValueError('canonical pair count is outside its physical range')
    if rng is None:
        rng=random.SystemRandom()
    if order is None:
        order=min_degree_order(F)
    allowed=[{'0','u','d'} for _ in range(n)]
    def mass(table):
        c=counts(F,table,order)
        return sum(c) if k is None else c[k]
    z=mass(allowed)
    if z==0:
        raise ValueError('requested sector has exact zero norm')
    bits=0
    D=1
    while D < 2*max(1,n)/epsilon:
        bits += 1
        D *= 2
    state=[]
    trace=[]
    for i in range(n):
        ws=[]
        for local in ('0','u','d'):
            allowed[i]={local}
            ws.append(mass(allowed))
        assert sum(ws)==z
        cum=Q(0)
        bounds=[0]
        for a in ws[:-1]:
            cum += a
            bounds.append((D*cum/z).numerator // (D*cum/z).denominator)
        bounds.append(D)
        r=rng.getrandbits(bits)
        branch=next(j for j in range(3) if bounds[j] <= r < bounds[j+1])
        local=('0','u','d')[branch]
        assert ws[branch]>0
        allowed[i]={local}
        state.append(local)
        trace.append({'site':i,'weights':[str(x) for x in ws],
                      'dyadic_bounds':bounds,'branch':local})
        z=ws[branch]
    if k is not None:
        assert state.count('u')==state.count('d')==k
    return {'occupation':state,'pair_count':state.count('u'),
            'bits_per_site':bits,'random_bits':n*bits,
            'TV_bound':str(Q(2*n,D)),'trace':trace}

def test():
    rng=random.Random(6190301)
    t0=time.monotonic()
    cases=[]
    for n in range(1,6):
        for rep in range(4):
            F=[[qc() for j in range(n)] for i in range(n)]
            for i in range(n):
                for j in range(n):
                    if rng.randrange(4)!=0:
                        F[i][j]=qc(Q(rng.randrange(-2,3),rng.randrange(1,4)),
                                   Q(rng.randrange(-1,2),rng.randrange(1,4)))
            cases.append(F)
    # Connected nonbipartite, nonmonomial, unbounded-component example.
    for n in (5,7):
        F=[[qc() for _ in range(n)] for _ in range(n)]
        for v in range(0,n-2,2):
            for i,j in combinations((v,v+1,v+2),2):
                F[i][j]=qc(Q(2,3),Q(1,2))
                F[j][i]=qc(Q(-1,3),Q(1,4))
        cases.append(F)
    count_checks=0
    prefix_checks=0
    rows=[]
    for F in cases:
        n=len(F)
        st={}
        a=counts(F,stats=st)
        assert a==brute_counts(F)
        count_checks += 1
        # Several arbitrary elimination orders catch Grassmann sign issues.
        for rep in range(2):
            order=list(range(n))
            rng.shuffle(order)
            assert counts(F,order=order)==a
            count_checks += 1
        for rep in range(3):
            allowed=[]
            for i in range(n):
                s={x for x in ('0','u','d') if rng.randrange(3)}
                allowed.append(s)
            assert counts(F,allowed)==brute_counts(F,allowed)
            prefix_checks += 1
        rows.append({'n':n,'stats':st,'counts':[str(x) for x in a]})
    # A chain of 15 triangles: rank and connected component grow with n.
    n=31
    F=[[qc() for _ in range(n)] for _ in range(n)]
    for v in range(0,n-2,2):
        for i,j in combinations((v,v+1,v+2),2):
            F[i][j]=qc(1)
            F[j][i]=qc(-1)
    st={}
    t1=time.monotonic()
    a=counts(F,stats=st)
    assert st['width']==2
    assert a[0]==1 and a[1]==90
    # This skew pair matrix has odd n, but no bipartite support premise.
    long={'n':n,'stats':st,'counts':[str(x) for x in a],
          'wall_seconds':time.monotonic()-t1}
    sam=sample(F,k=15,epsilon=Q(1,1000),rng=rng)
    result={'status':'PASS','exact_arithmetic':'Fraction real and imaginary',
            'direct_count_checks':count_checks,'prefix_checks':prefix_checks,
            'cases':rows,'connected_triangle_chain':long,'canonical_sample':sam,
            'wall_seconds':time.monotonic()-t0}
    path=Path(__file__).with_name('grassmann_checks.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases',)},indent=2))

if __name__=='__main__': test()
