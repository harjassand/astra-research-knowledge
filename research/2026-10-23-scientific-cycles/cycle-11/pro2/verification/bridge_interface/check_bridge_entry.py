"""Exact new omitted-entry-reset witness; standard library, no producer imports."""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,resource,time

ROOT=Path(__file__).resolve().parent

def components(n,edges,colors):
    buckets=defaultdict(list)
    for u,v in edges:
        assert colors[u]!=colors[v]
        buckets[tuple(sorted((colors[u],colors[v])))].append((u,v))
    out=[]
    for pair,es in sorted(buckets.items()):
        adj=defaultdict(list)
        for u,v in es:adj[u].append(v);adj[v].append(u)
        seen=set()
        for root in sorted(adj):
            if root in seen:continue
            walk=[root];seen.add(root)
            for v in walk:
                for w in adj[v]:
                    if w not in seen:seen.add(w);walk.append(w)
            count=sum(len(adj[v]) for v in walk)//2
            assert count==len(walk)-1
            out.append(dict(pair=pair,vertices=sorted(walk),edges=count))
    return out

def main():
    t=time.perf_counter();cpu=time.process_time();k=9;n=3*k
    edges=[]
    for i in range(k):
        a,b,c=3*i,3*i+1,3*i+2
        edges.extend([(a,b),(a,c),(b,c)])
        if i:edges.append((3*(i-1),a))
    edges=sorted(edges);degrees=[0]*n
    for u,v in edges:degrees[u]+=1;degrees[v]+=1
    assert max(degrees)==4 and len(edges)==4*k-1
    bad=[];good=[]
    for i in range(k):
        bad.extend([i%2,2,3])
        root=i%3
        other=[2,3] if i==0 else [c for c in range(4) if c not in [root,(i-1)%3]]
        good.extend([root]+other)
        if i:
            assert bad[3*(i-1)] not in bad[3*i+1:3*i+3]
            assert good[3*(i-1)] not in good[3*i+1:3*i+3]
        if i>=2:assert good[3*i]!=good[3*(i-2)]
    cb=components(n,edges,bad);cg=components(n,edges,good)
    assert max(len(c['vertices']) for c in cb)==k
    assert max(len(c['vertices']) for c in cg)==3
    a=k//2;d=k-a;div=[F(1,a) if i<a else F(-1,d) for i in range(k)]
    weights={e:F(0) for e in edges};prefix=F(0)
    for i in range(k-1):
        prefix+=div[i]
        weights[(3*i,3*(i+1))]=(-1)**i*prefix
    cut=(3*(a-1),3*a);assert abs(weights[cut])==1
    Y=[[F(0) for _ in range(4)] for _ in range(n)]
    for (u,v),w in weights.items():Y[u][bad[v]]+=w;Y[v][bad[u]]+=w
    norm=sum(x*x for row in Y for x in row)
    assert norm==F(1,a)+F(1,d)==F(9,20)
    native=dict(name='triangle_bridge_chain_9',n=n,edges=edges,
                blocks=[dict(vertices=[3*i,3*i+1,3*i+2],entry=3*i) for i in range(k)],
                bad_colors=bad,complete_rule_colors=good)
    report=dict(status='PASS',scope='New rule counterexample and same-support repair; no arbitrary-real lower.',
                n=n,m=len(edges),maximum_degree=max(degrees),bad_components=cb,
                repaired_components=cg,cut=dict(edge=cut,sizes=[a,d],coefficient=str(weights[cut])),
                diagonal=['0']*n,edge_coefficients=[[u,v,str(w)] for (u,v),w in sorted(weights.items())],
                full_original_action=[[str(x) for x in row] for row in Y],
                action_frobenius_squared=str(norm),inverse_squared_lower=str(1/norm))
    (ROOT/'triangle_bridge_chain_9.json').write_text(json.dumps(native,indent=2)+'\n')
    (ROOT/'BRIDGE_ENTRY_DIAGNOSTIC.json').write_text(json.dumps(report,indent=2)+'\n')
    costs=dict(wall_seconds=time.perf_counter()-t,cpu_seconds=time.process_time()-cpu,
               peak_process_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
               includes='Input construction, both color-component checks, exact full-action witness and scientific JSON serialization.',
               excludes='Final cost receipt serialization; source reading, proof discovery, inference, authoring and integration are unknown.',
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT/'COSTS.json').write_text(json.dumps(costs,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',n=n,m=len(edges),bad_max_component=k,repaired_max_component=3,
                         norm_squared=str(norm),costs=costs),indent=2))

if __name__=='__main__':main()
