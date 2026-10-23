"""Independent finite diagnostic for the higher-load exact star interface.
Standard library only; no producer imports. The universal proof is PROOF.md.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import json,time,hashlib

Q=4

def path(k):
    return {'n':k+1,'edges':[(i,i+1) for i in range(k)],'ports':(0,k)}

def join(op,g,h):
    # Fresh copies, followed only by the declared endpoint identifications.
    n=g['n']+h['n']; parent=list(range(n))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):parent[find(j)]=find(i)
    a,b=g['ports']; c,d=(g['n']+v for v in h['ports'])
    if op=='S':union(b,c);ports=(a,d)
    elif op=='P':union(a,c);union(b,d);ports=(a,b)
    else:raise ValueError(op)
    roots=sorted({find(i) for i in range(n)}); ids={v:i for i,v in enumerate(roots)}
    cv=lambda i:ids[find(i)]
    ee=[tuple(sorted((cv(u),cv(v)))) for u,v in g['edges']]
    ee += [tuple(sorted((cv(g['n']+u),cv(g['n']+v)))) for u,v in h['edges']]
    assert len(set(ee))==len(ee) and all(u!=v for u,v in ee)
    out={'n':len(roots),'edges':sorted(ee),'ports':tuple(cv(v) for v in ports)}
    assert tuple(sorted(out['ports'])) not in out['edges']
    assert max(map(len,adjacency(out)))<=4
    return out

def adjacency(g):
    aa=[[] for _ in range(g['n'])]
    for u,v in g['edges']:aa[u].append(v);aa[v].append(u)
    return aa

def signature(g,col):
    aa=adjacency(g);out=[]
    for v in g['ports']:
        nn=tuple(sum(col[u]==c for u in aa[v]) for c in range(Q))
        ff=tuple(int(any(col[u]==c and any(w!=v and col[w]==col[v] for w in aa[u]) for u in aa[v])) for c in range(Q))
        out.append((col[v],nn,ff))
    return tuple(out)

def is_star(g,col):
    aa=adjacency(g)
    if any(col[u]==col[v] for u,v in g['edges']):return False
    for u,v in g['edges']:
        if any(w!=v and col[w]==col[v] for w in aa[u]) and any(w!=u and col[w]==col[u] for w in aa[v]):return False
    return True

def enumerate_states(g):
    aa=adjacency(g);order=sorted(range(g['n']),key=lambda v:-len(aa[v]))
    col=[-1]*g['n']; states=set(); proper=star=0
    def rec(i):
        nonlocal proper,star
        if i==len(order):
            proper+=1
            if is_star(g,col):star+=1;states.add(signature(g,col))
            return
        v=order[i]
        for c in range(Q):
            if any(col[u]==c for u in aa[v]):continue
            col[v]=c;rec(i+1)
        col[v]=-1
    rec(0)
    return states,proper,star

def merge(a,b):
    if a[0]!=b[0]:return None
    nn=tuple(x+y for x,y in zip(a[1],b[1])); ff=tuple(int(x or y) for x,y in zip(a[2],b[2]))
    if sum(nn)>4:return None
    if any(n>=2 and f for n,f in zip(nn,ff)):return None
    return (a[0],nn,ff)

def compose(op,a,b):
    if op=='S':
        return (a[0],b[1]) if merge(a[1],b[0]) is not None else None
    l=merge(a[0],b[0]);r=merge(a[1],b[1])
    return (l,r) if l is not None and r is not None else None

def main():
    start=time.perf_counter()
    p2,p3=path(2),path(3)
    c4=join('P',p2,p2)
    u21=join('S',c4,p2)
    u12=join('S',p2,c4)
    cases=[('series_path2_path2','S',p2,p2),('parallel_path2_path2','P',p2,p2),
      ('series_cycle4_path2_load21','S',c4,p2),('series_cycle4_cycle4_degree4_join','S',c4,c4),
      ('parallel_cycle4_cycle4_load44','P',c4,c4),('parallel_load21_path3','P',u21,p3),
      ('parallel_load21_load12','P',u21,u12)]
    cache={}; records=[]
    def states(g):
        key=(g['n'],tuple(g['edges']),g['ports'])
        if key not in cache:cache[key]=enumerate_states(g)
        return cache[key]
    for name,op,g,h in cases:
        t=time.perf_counter();out=join(op,g,h)
        sg=states(g)[0];sh=states(h)[0]
        predicted={w for a in sg for b in sh if (w:=compose(op,a,b)) is not None}
        actual,proper,star=states(out)
        assert predicted==actual,(name,len(predicted),len(actual))
        records.append({'name':name,'operation':op,'n':out['n'],'m':len(out['edges']),
          'degrees':[len(adjacency(out)[v]) for v in out['ports']],
          'child_labeled_states':[len(sg),len(sh)],'parent_labeled_states':len(actual),
          'parent_proper_colorings':proper,'parent_star_colorings':star,
          'exact_state_set_equality':True,'seconds':time.perf_counter()-t})
    res={'schema':'astra-cycle8-independent-higher-load-interface/v1','q':Q,'cases':records,
      'total_body_seconds':time.perf_counter()-start,'scope':'Finite implementation diagnostic; all-size exactness is proved in PROOF.md.'}
    dest=Path(__file__).with_name('RESULT.json');dest.write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps(res,indent=2))
if __name__=='__main__':main()
