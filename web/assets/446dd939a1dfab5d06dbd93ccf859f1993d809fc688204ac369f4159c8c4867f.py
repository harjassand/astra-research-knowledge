"""Explicit positive rational weighted-to-unweighted perfect-matching reduction.

No FPRAS is implemented here. Supplying an FPRAS for simple unweighted general
graphs makes this reduction usable with that counter. The exact counter below
is only a small-instance diagnostic.
"""
from fractions import Fraction
from functools import lru_cache
from math import lcm


def path_count_dag(weight: int):
    """A simple DAG with exactly `weight` source-to-target paths, O(log weight)."""
    if not isinstance(weight,int) or weight<1:
        raise ValueError('Weight must be a positive integer')
    source=0; current=1; edges=[(source,current)]; size=2
    for bit in bin(weight)[3:]:
        a,b,target=size,size+1,size+2; size+=3
        edges.extend([(current,a),(current,b),(a,target),(b,target)])
        if bit=='1': edges.append((source,target))
        current=target
    return size,edges,source,current


def edge_gadget(weight: int):
    """Ports 0,1: both used => weight completions; neither used => one."""
    n,dag,s,t=path_count_dag(weight)
    edges=[]
    left=lambda v: 2+2*v
    right=lambda v: 3+2*v
    for v in range(n): edges.append((left(v),right(v)))
    for i,j in dag: edges.append((left(i),right(j)))
    edges.extend([(0,right(s)),(1,left(t))])
    return 2+2*n,edges


def weighted_to_unweighted(weights):
    """Return a simple graph and D: Z_weighted=Z_graph/D^(n/2)."""
    A=[[Fraction(w) for w in row] for row in weights]; n=len(A)
    if n%2 or any(len(row)!=n for row in A):
        raise ValueError('Input must be an even-order square matrix')
    if any(A[i][j]!=A[j][i] or A[i][j]<0 for i in range(n) for j in range(n)):
        raise ValueError('Weights must be symmetric and nonnegative')
    denominator=1
    for i in range(n):
        for j in range(i): denominator=lcm(denominator,A[i][j].denominator)
    size=n; output=[]
    for i in range(n):
        for j in range(i):
            if not A[i][j]: continue
            w=A[i][j]*denominator
            gsize,gedges=edge_gadget(int(w))
            def vertex(v): return i if v==0 else j if v==1 else size+v-2
            output.extend((vertex(a),vertex(b)) for a,b in gedges)
            size+=gsize-2
    return size,output,denominator


def exact_count(n,edges,deleted=()):
    adjacency=[0]*n
    for a,b in edges:
        if a==b: raise ValueError('Self-edges are not allowed')
        adjacency[a]|=1<<b; adjacency[b]|=1<<a
    @lru_cache(None)
    def recurse(mask):
        if not mask: return 1
        if mask.bit_count()%2: return 0
        active=[i for i in range(n) if (mask>>i)&1]
        i=min(active,key=lambda v:(adjacency[v]&mask).bit_count())
        neighbors=adjacency[i]&mask
        value=0
        while neighbors:
            bit=neighbors&-neighbors; neighbors-=bit
            value+=recurse(mask^(1<<i)^bit)
        return value
    mask=(1<<n)-1
    for v in deleted: mask&=~(1<<v)
    return recurse(mask)
