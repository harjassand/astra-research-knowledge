"""Classical PEO star coloring and direct-read symmetric recovery.

Implements the established chordal coloring mechanism in Albertson et al.2004,
Thm6.1. The new theorem's matching upper comparator, not a new algorithm.
General nonchordal graphs require a supplied chordal completion/decomposition.
"""
from collections import Counter
import heapq


def prepare(n,edges,t):
    adj=[set() for _ in range(n)]
    for i,j in edges:
        if not(0<=i<j<n):raise ValueError('invalid edge')
        adj[i].add(j);adj[j].add(i)
    label=[0]*n;used=[False]*n;heap=[(0,i) for i in range(n)];order=[]
    heapq.heapify(heap)
    while heap:
        neg,v=heapq.heappop(heap)
        if used[v] or -neg!=label[v]:continue
        used[v]=True;order.append(v)
        for u in adj[v]:
            if not used[u]:label[u]+=1;heapq.heappush(heap,(-label[u],u))
    peo=order[::-1];pos={v:i for i,v in enumerate(peo)}
    later=[{u for u in adj[v] if pos[u]>pos[v]} for v in range(n)]
    for ns in later:
        if len(ns)>t:raise ValueError('width bound failed')
        if any(v not in adj[u] for u in ns for v in ns if u!=v):raise ValueError('not a perfect elimination order')
    K=(t+1)*(t+2)//2;colors=[-1]*n
    for v in reversed(peo):
        forbidden=set(later[v])
        for u in later[v]:forbidden.update(later[u])
        bad={colors[u] for u in forbidden}
        colors[v]=next(c for c in range(K) if c not in bad)
    counts=[Counter(colors[u] for u in adj[v]) for v in range(n)]
    cells=[]
    for i,j in sorted(edges):
        if colors[i]==colors[j]:raise ValueError('not proper')
        if counts[i][colors[j]]==1:cells.append((i,j,i,colors[j]))
        elif counts[j][colors[i]]==1:cells.append((i,j,j,colors[i]))
        else:raise ValueError('not a star coloring')
    selected=[(i,colors[i]) for i in range(n)]+[(v,c) for i,j,v,c in cells]
    if len(set(selected))!=len(selected):raise ValueError('reused selected cell')
    return {'n':n,'q':max(colors,default=-1)+1,'colors':colors,'edge_cells':cells,'peo':peo,'cap':K}


def recover(plan,Y):
    if len(Y)!=plan['n'] or any(len(r)!=plan['q'] for r in Y):raise ValueError('wrong action shape')
    D={(i,i):Y[i][c] for i,c in enumerate(plan['colors'])}
    for i,j,v,c in plan['edge_cells']:D[i,j]=Y[v][c]
    return D
