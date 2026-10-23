"""Exact small input certificates for the grammar-scope theorem.
No producer import, graph package, optimization or claimed all-size enumeration.
"""
from pathlib import Path
import hashlib, json, resource, time

def graph_A(length):
    assert type(length) is int and length >= 2
    edges=[(0,3),(3,1),(0,4),(4,1),(0,5),(5,2),(0,6),(6,2)]
    path=[1]+list(range(7,length+6))+[2]
    edges += list(zip(path,path[1:]))
    bags=[[0,1,2],[0,1,3],[0,1,4],[0,2,5],[0,2,6]]
    tree=[(0,i) for i in range(1,5)]
    internal=path[1:-1]
    bags.append([1,2,internal[0]])
    tree.append((0,5))
    for i in range(1,len(internal)):
        bags.append([2,internal[i-1],internal[i]])
        tree.append((len(bags)-2,len(bags)-1))
    return {'name':'A_'+str(length),'n':length+6,'edges':[sorted(e) for e in edges],
            'width_two_bags':bags,'bag_tree_edges':tree,
            'colors':[0,1,2,2,2,1,1,0] if length==2 else None}

def graph_K24():
    return {'name':'K_2_4','n':6,'edges':[[v,w] for v in (0,1) for w in range(2,6)],
            'width_two_bags':[[0,1,v] for v in range(2,6)],
            'bag_tree_edges':[[0,i] for i in range(1,4)]}

def adjacency(n, edges):
    a=[set() for _ in range(n)]
    for u,v in edges:
        assert u!=v and v not in a[u]
        a[u].add(v);a[v].add(u)
    return a

def components(a, removed=()):
    forbidden=set(removed);seen=set(forbidden);out=[]
    for root in range(len(a)):
        if root in seen: continue
        q=[root];seen.add(root)
        for v in q:
            for w in sorted(a[v]):
                if w not in seen:
                    seen.add(w);q.append(w)
        out.append(q)
    return out

def cycles(a):
    found=set()
    for s in range(len(a)):
        stack=[(s,[s],{s})]
        while stack:
            u,p,seen=stack.pop()
            for v in a[u]:
                if v==s and len(p)>=3:
                    pp=tuple(p);rr=(p[0],)+tuple(reversed(p[1:]))
                    found.add(min(pp,rr))
                elif v>s and v not in seen:
                    stack.append((v,p+[v],seen|{v}))
    return sorted(found)

def validate_decomposition(g):
    bags=[set(b) for b in g['width_two_bags']]
    tree=adjacency(len(bags),g['bag_tree_edges'])
    assert len(g['bag_tree_edges'])==len(bags)-1 and len(components(tree))==1
    assert max(map(len,bags))<=3
    for u,v in g['edges']: assert any(u in b and v in b for b in bags)
    for v in range(g['n']):
        ids={i for i,b in enumerate(bags) if v in b}
        assert ids
        root=min(ids);seen={root};q=[root]
        for x in q:
            for y in tree[x]:
                if y in ids and y not in seen: seen.add(y);q.append(y)
        assert seen==ids

def balanced_ports(a):
    admitted=[]
    for u in range(len(a)):
        for v in range(u+1,len(a)):
            if len(a[u]) not in (2,3) or len(a[v])!=len(a[u]) or v in a[u]: continue
            comps=components(a,(u,v))
            if len(comps)!=len(a[u]): continue
            if all(len(a[u]&set(c))==len(a[v]&set(c))==1 for c in comps):
                admitted.append([u,v])
    return admitted

def check(g):
    n=g['n'];a=adjacency(n,g['edges']);degree=list(map(len,a))
    assert len(components(a))==1
    assert max(degree)<=4
    assert all(len(components(a,(v,)))==1 for v in range(n))
    for u,v in g['edges']: assert len(components(a,(u,v)))==1
    cs=cycles(a)
    for cyc in cs:
        assert len(cyc)>=4
        k=len(cyc)
        for i in range(k):
            for j in range(i+1,k):
                if j-i in (1,k-1): continue
                assert cyc[j] not in a[cyc[i]]
    validate_decomposition(g)
    if g.get('colors') is not None:
        c=g['colors'];assert all(c[u]!=c[v] for u,v in g['edges'])
        for x in range(3):
            for y in range(x+1,3):
                induced=[set(w for w in a[v] if c[w] in (x,y)) if c[v] in (x,y) else set() for v in range(n)]
                for comp in components(induced):
                    real=[v for v in comp if c[v] in (x,y)]
                    if not real: continue
                    assert sum(len(induced[v]) for v in real)==2*(len(real)-1)
                    assert sum(len(induced[v])>1 for v in real)<=1
    return {'name':g['name'],'n':n,'m':len(g['edges']),'degrees':degree,
            'degree_four_count':degree.count(4),'simple_cycle_count':len(cs),
            'cycles':cs,'two_connected':True,'clique_cutset_free':True,
            'chordless':True,'triangle_free':True,'width_two_decomposition_checked':True,
            'balanced_port_candidates':balanced_ports(a),
            'star_three_checked':g.get('colors') is not None}

def main():
    start=time.perf_counter();cpu=time.process_time()
    inputs=[graph_A(2),graph_K24()]
    results=[check(g) for g in inputs]
    assert results[0]['degree_four_count']==1
    assert results[1]['balanced_port_candidates']==[]
    out={'status':'PASS','inputs':inputs,'results':results,
         'scope':'Two actual exact structural inputs. The all-L exclusion is the mathematical parity proof, not finite testing.',
         'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
         'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
         'excluded_costs':['process startup','authoring','proof discovery','source reading','review','output serialization']}
    p=Path(__file__).with_name('RESULT.json');p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'wall_seconds':out['wall_seconds'],'cpu_seconds':out['cpu_seconds'],
                      'results':[{k:v for k,v in r.items() if k!='cycles'} for r in results]}))
if __name__=='__main__':main()

