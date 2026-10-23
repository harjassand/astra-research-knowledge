"""Four rational queries on genuine 2-trees of maximum degree four.

This is a bounded subclass operation, not a decoder for all partial 2-trees.
Input is an actual 2-tree construction starting with triangle 0,1,2.
All arithmetic is exact Fraction arithmetic; PROOF.md supplies the all-size bound.
"""
from fractions import Fraction as F


def inverse(a):
    n = len(a)
    b = [[F(x) for x in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        p = next((i for i in range(j, n) if b[i][j]), None)
        if p is None:
            raise ValueError('singular local matrix')
        b[j], b[p] = b[p], b[j]
        pivot = b[j][j]
        b[j] = [x / pivot for x in b[j]]
        for i in range(n):
            if i != j:
                pivot = b[i][j]
                b[i] = [x - pivot * y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def eta(a, b):
    assert a != b
    return 1 if (b-a) % 3 == 1 else -1


def prepare(parents):
    n = 3 + len(parents)
    adj = [set() for _ in range(n)]
    for a, b in ((0, 1), (1, 2), (0, 2)):
        adj[a].add(b); adj[b].add(a)
    for v, pair in enumerate(parents, 3):
        a, b = pair
        if not (0 <= a < b < v and b in adj[a]):
            raise ValueError('not a 2-tree construction')
        adj[v].update((a,b)); adj[a].add(v); adj[b].add(v)
    if max(map(len, adj)) > 4:
        raise ValueError('maximum degree exceeds four')
    edges = [(i,j) for i in range(n) for j in sorted(adj[i]) if i<j]
    book = next(((a,b) for a,b in edges if len(adj[a] & adj[b]) == 3), None)
    if book is not None:
        assert n == 5
        colors = [2]*n
        colors[book[0]], colors[book[1]] = 0, 1
        X = [[F(c==j) for j in range(4)] for c in colors]
        return {'n':n,'adj':adj,'edges':edges,'book':book,'colors':colors,'X':X}

    oldadj = [set() for _ in range(n)]
    for a,b in ((0,1),(1,2),(0,2)):
        oldadj[a].add(b);oldadj[b].add(a)
    colors = [0,1,2]+[-1]*(n-3)
    signs = [1]*n
    for v,(a,b) in enumerate(parents,3):
        thirds = oldadj[a] & oldadj[b]
        assert len(thirds)==1
        w = next(iter(thirds))
        colors[v] = 3-colors[a]-colors[b]
        assert colors[v] == colors[w]
        signs[v] = -signs[w]
        oldadj[v].update((a,b));oldadj[a].add(v);oldadj[b].add(v)
    X = [[F(c==j,2) for j in range(3)]+[F(s,2)] for c,s in zip(colors,signs)]
    maps, gram_traces, cache = [], [], {}
    for v in range(n):
        indices = [v] + sorted(adj[v], key=lambda w:(colors[w],signs[w],w))
        rows = [X[w] for w in indices]
        key = tuple(tuple(row) for row in rows)
        if key not in cache:
            if len(rows)<=4:
                inv = inverse(multiply(rows,transpose(rows)))
                P = multiply(inv,rows)
            else:
                inv = inverse(multiply(transpose(rows),rows))
                P = multiply(rows,inv)
            tr = sum(inv[i][i] for i in range(len(inv)))
            assert tr <= 16  # exact local inverse bound <=4
            cache[key] = (P,tr)
        P,tr = cache[key]
        maps.append((indices,P));gram_traces.append(tr)
    high = {v for v in range(n) if len(adj[v])==4}
    anchors = {}
    for v in high:
        lows = sorted(adj[v]-high)
        if lows:
            anchors[v] = ('edge', lows[0])
        else:
            u,w = next((u,w) for u in sorted(adj[v]) for w in sorted(adj[v])
                       if u<w and w in adj[u])
            anchors[v] = ('triangle',u,w)
    return {'n':n,'adj':adj,'edges':edges,'book':None,'colors':colors,
            'signs':signs,'X':X,'maps':maps,'high':high,'anchors':anchors,
            'gram_traces':gram_traces,'distinct_local_maps':len(cache)}


def recover(plan,Y):
    n, colors, adj = plan['n'],plan['colors'],plan['adj']
    assert len(Y)==n and all(len(row)==4 for row in Y)
    if plan['book'] is not None:
        D = {(v,v):Y[v][colors[v]] for v in range(n)}
        for a,b in plan['edges']:
            if sum(colors[w]==colors[b] for w in adj[a])==1:
                D[a,b] = Y[a][colors[b]]
            else:
                assert sum(colors[w]==colors[a] for w in adj[b])==1
                D[a,b] = Y[b][colors[a]]
        return D
    signs = plan['signs']
    rows=[]
    for v,(indices,P) in enumerate(plan['maps']):
        rows.append({w:sum(a*b for a,b in zip(p,Y[v])) for w,p in zip(indices,P)})
    def g(v,w):
        return eta(colors[v],colors[w])*signs[v]*signs[w]*(rows[w][v]-rows[v][w])
    rho={}
    for v,a in plan['anchors'].items():
        if a[0]=='edge':z=g(v,a[1])
        else:
            u,w=a[1:]
            z=(g(v,u)+g(v,w)-g(u,w))/2
        rho[v]=signs[v]*z
    out={(v,v):rows[v][v] for v in range(n)}
    for v,w in plan['edges']:
        a=rows[v][w]+rho.get(v,0)*eta(colors[v],colors[w])*signs[w]
        b=rows[w][v]+rho.get(w,0)*eta(colors[w],colors[v])*signs[v]
        out[v,w]=(a+b)/2
    return out


def action(plan,D):
    Y=[[F(0) for _ in range(4)] for _ in range(plan['n'])]
    for (v,w),a in D.items():
        for j in range(4):
            Y[v][j]+=a*plan['X'][w][j]
            if v!=w:Y[w][j]+=a*plan['X'][v][j]
    return Y
