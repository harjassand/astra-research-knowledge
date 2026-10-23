"""Exact color-pair connectivity and vertex-mass profiles for a two-vertex join.

Inputs must agree on boundary colors and have no common vertices outside0,1.
This module propagates actual masses. It does not assert a uniform bound.
"""
from itertools import combinations


class BichromaticCycle(ValueError):
    pass


def profile(vertices, edges, colors, q=4):
    vertices,edges=set(vertices),list(edges)
    assert 0 in vertices and 1 in vertices
    if any(colors[u]==colors[v] for u,v in edges):
        raise ValueError("improper coloring")
    answer={}
    for pair in combinations(range(q),2):
        unused={v for v in vertices if colors[v] in pair}
        adj={v:[] for v in unused}
        for u,v in edges:
            if u in unused and v in unused:
                adj[u].append(v);adj[v].append(u)
        boundary_comps={};closed=0
        while unused:
            s=next(iter(unused));unused.remove(s);seen={s};stack=[s];degree=0
            while stack:
                u=stack.pop();degree+=len(adj[u])
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v);unused.remove(v);stack.append(v)
            if degree!=2*(len(seen)-1):
                raise BichromaticCycle(f"cycle in pair{pair}")
            present=tuple(v for v in (0,1) if v in seen)
            if present:
                boundary_comps[present]=len(seen)
            else:
                closed=max(closed,len(seen))
        if (0,1) in boundary_comps:
            mode,masses='connected',[boundary_comps[(0,1)]]
        elif (0,) in boundary_comps and (1,) in boundary_comps:
            mode,masses='apart',[boundary_comps[(0,)],boundary_comps[(1,)]]
        elif (0,) in boundary_comps:
            mode,masses='u',[boundary_comps[(0,)]]
        elif (1,) in boundary_comps:
            mode,masses='v',[boundary_comps[(1,)]]
        else:
            mode,masses='none',[]
        answer[''.join(map(str,pair))]={'mode':mode,'masses':masses,'closed_max':closed}
    return answer


def join(left,right):
    """Parallel join across the same nonadjacent terminals; exact mass update."""
    if left.keys()!=right.keys():
        raise ValueError("color-pair universes differ")
    answer={}
    for pair in left:
        a,b=left[pair],right[pair];ma,mb=a['mode'],b['mode']
        closed=max(a['closed_max'],b['closed_max'])
        if ma in ('none','u','v'):
            if ma!=mb:
                raise ValueError("boundary color mismatch")
            mode=ma
            masses=[] if ma=='none' else [a['masses'][0]+b['masses'][0]-1]
        elif ma=='connected' and mb=='connected':
            raise BichromaticCycle(f"both pieces transmit pair{pair}")
        elif ma=='apart' and mb=='apart':
            mode,masses='apart',[x+y-1 for x,y in zip(a['masses'],b['masses'])]
        elif {ma,mb}=={'connected','apart'}:
            connected=a if ma=='connected' else b
            apart=b if ma=='connected' else a
            mode,masses='connected',[connected['masses'][0]+sum(apart['masses'])-2]
        else:
            raise ValueError("boundary state mismatch")
        answer[pair]={'mode':mode,'masses':masses,'closed_max':closed}
    return answer


def max_mass(p):
    return max([entry['closed_max'] for entry in p.values()]+
               [m for entry in p.values() for m in entry['masses']])
