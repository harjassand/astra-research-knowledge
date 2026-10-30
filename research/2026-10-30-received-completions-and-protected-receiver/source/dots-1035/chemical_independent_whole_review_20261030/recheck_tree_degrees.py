"""Independent finite-head certificate via maximum-weight directed spanning trees.

Unlike the supplied positive-Schur code, this generates every edge from reaction
complexes, makes absorbing labels restart the queried state at rate one, and uses
the positive Markov-chain tree formula. Tree degrees are computed by the exact
integer Chu-Liu/Edmonds contraction algorithm; no floating-point algebra is used.
"""
import json
from pathlib import Path

ROOT = Path('producer-workspace/chemical_joint_global_candidate_20261030')
OUT = Path(__file__).parent

def h(b):
    if b < 4:
        return b
    q, j = divmod(b-4, 3)
    return 3+j+2*q

def g(n):
    q, j = divmod(n, 3)
    return 4*q+j

# Ordered coordinates A,C,B; each pair is an actual source and target complex.
complexes = [(0,0,0), (1,0,1), (3,0,4), (0,3,4), (1,2,4), (2,1,4)]
reactions = [(complexes[0], complexes[1]), (complexes[1], complexes[2]),
             (complexes[2], complexes[0])]
chain = [complexes[i] for i in (3,4,5,2)]
for u,v in zip(chain, chain[1:]):
    reactions += [(u,v), (v,u)]

def put(edges, u, v, d):
    if u != v:
        edges[u,v] = max(edges.get((u,v), -10**9), d)

def max_tree_degree(nodes, edges, root):
    """Degree of a directed in-tree toward root, or None if none exists."""
    ids = {u:i for i,u in enumerate(nodes)}
    # Reverse edges, so the standard rooted out-arborescence algorithm applies.
    es = [(ids[v],ids[u],w) for (u,v),w in edges.items() if u != root]
    n, r, answer = len(nodes), ids[root], 0
    while True:
        incoming = [None]*n
        previous = [-1]*n
        for u,v,w in es:
            if u != v and v != r and (incoming[v] is None or w > incoming[v]):
                incoming[v], previous[v] = w,u
        incoming[r] = 0
        if any(w is None for w in incoming):
            return None
        answer += sum(incoming)
        component = [-1]*n
        visited = [-1]*n
        count = 0
        for start in range(n):
            v = start
            while visited[v] != start and component[v] < 0 and v != r:
                visited[v] = start
                v = previous[v]
            if v != r and component[v] < 0:
                u = previous[v]
                component[v] = count
                while u != v:
                    component[u] = count
                    u = previous[u]
                count += 1
        if count == 0:
            return answer
        for v in range(n):
            if component[v] < 0:
                component[v] = count
                count += 1
        es = [(component[u],component[v],w-incoming[v])
              for u,v,w in es if component[u] != component[v]]
        r, n = component[r], count

LABELS = ['up','down','safe']

def first_graph():
    states = list(range(13))
    edges = {}
    for b in states:
        for y,yp in reactions[:3]:
            if b < y[2]:
                continue
            db = yp[2]-y[2]
            dn = yp[0]+yp[1]-y[0]-y[1]
            bb = b+db
            delta = dn-h(bb)+h(b)
            assert delta in (-1,0,1)
            target = ('up' if delta==1 else 'down' if delta==-1
                      else 'safe' if bb>12 else bb)
            put(edges,b,target,y[0]+y[1])
    return states,edges

def second_graph():
    states = [(a,n-a) for n in range(9) for a in range(n+1)]
    edges = {}
    for a,c in states:
        for y,yp in reactions:
            if a<y[0] or c<y[1]:
                continue
            aa,cc = a+yp[0]-y[0],c+yp[1]-y[1]
            delta = yp[2]-y[2]-g(aa+cc)+g(a+c)
            assert delta in (-1,0,1)
            target = ('up' if delta==1 else 'down' if delta==-1
                      else 'safe' if aa+cc>8 else (aa,cc))
            put(edges,(a,c),target,y[2])
    return states,edges

def certify(states,edges):
    results = {}
    for start in states:
        augmented = dict(edges)
        for label in LABELS:
            put(augmented,label,start,0)
        tree = {label:max_tree_degree(states+LABELS,augmented,label)
                for label in LABELS}
        den = max(v for v in tree.values() if v is not None)
        results['s'+str(start)] = {
            label:None if tree[label] is None else tree[label]-den
            for label in ('up','safe')}
    return results

if __name__ == '__main__':
    reports = {}
    for name,build,filename,key,K in [
        ('r_head',first_graph,'FIRST_RESIDUAL_ALL_EXIT_DEGREES.json','up_degrees',12),
        ('s_head',second_graph,'COMPOSITION_HEAD_EXIT_DEGREES.json','degrees',8)]:
        result = certify(*build())
        supplied = next(x[key] for x in json.loads((ROOT/'checks'/filename).read_text()) if x['K']==K)
        assert result == supplied, (name,result,supplied)
        reports[name] = {'method':'maximum-weight directed spanning trees',
                         'all_entries_match':True,'states':len(result),
                         'max_up':max(v['up'] for v in result.values() if v['up'] is not None),
                         'max_tail':max(v['safe'] for v in result.values() if v['safe'] is not None),
                         'degrees':result}
    (OUT/'INDEPENDENT_TREE_DEGREES.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a!='degrees'} for k,v in reports.items()},indent=2))
