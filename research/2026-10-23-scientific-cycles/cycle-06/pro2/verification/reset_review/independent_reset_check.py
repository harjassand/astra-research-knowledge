#!/usr/bin/env python3
"""Small independent diagnostic of the new network-color boundary recurrences.

No producer module, numerical solver, or prior scientific fixture is used.
All arithmetic is integer. The all-size arguments are in REVIEW.md.
"""
from itertools import combinations
from pathlib import Path
import json
import time
import resource


def leaf():
    return dict(n=3, edges=[(0,1),(1,2)], colors=[0,2,1], s=0, t=2)


def clone_into(child, mapping, colors, edges, start, end=None):
    relabel={0:start}
    relabel={child['s']:start}
    if end is not None:
        relabel[child['t']]=end
    for u in range(child['n']):
        if u not in relabel:
            relabel[u]=len(colors)
            colors.append(mapping[child['colors'][u]])
        else:
            assert colors[relabel[u]]==mapping[child['colors'][u]]
    edges.extend(tuple(sorted((relabel[u],relabel[v]))) for u,v in child['edges'])
    return relabel[child['t']]


def parallel(children):
    assert 2<=len(children)<=3
    colors=[0,1,2,1]
    edges=[(0,1),(2,3)]
    for child in children:
        clone_into(child, {0:1,1:2,2:0}, colors, edges, 1, 2)
    return dict(n=len(colors),edges=edges,colors=colors,s=0,t=3)


def series(children, even=False):
    assert len(children)==2 if even else len(children)%2==1
    colors=[0]
    edges=[]
    end=0
    for i,child in enumerate(children):
        if even:
            a,b=((0,2),(2,1))[i]
            c=3-a-b
        else:
            a,b=((0,1) if i%2==0 else (1,0))
            c=2
        end=clone_into(child,{0:a,1:b,2:c},colors,edges,end)
    return dict(n=len(colors),edges=edges,colors=colors,s=0,t=end)


def inspect(net):
    n,es,cs=net['n'],net['edges'],net['colors']
    assert len(es)==len(set(es))
    adj=[[] for _ in range(n)]
    for u,v in es:
        assert 0<=u<v<n and cs[u]!=cs[v]
        adj[u].append(v);adj[v].append(u)
    assert len(adj[net['s']])==len(adj[net['t']])==1
    assert (cs[net['s']],cs[net['t']])==(0,1)
    components={}
    maximum=1
    for pair in combinations(range(3),2):
        todo={v for v in range(n) if cs[v] in pair}
        at={}
        while todo:
            start=min(todo); seen={start}; stack=[start]; todo.remove(start)
            while stack:
                v=stack.pop()
                for u in adj[v]:
                    if cs[u] in pair and u not in seen:
                        seen.add(u);todo.remove(u);stack.append(u)
            edge_count=sum(1 for u,v in es if u in seen and v in seen)
            assert edge_count==len(seen)-1
            assert not {net['s'],net['t']}<=seen
            maximum=max(maximum,len(seen))
            for v in seen:at[v]=len(seen)
        components[pair]=at
    return dict(n=n,m=len(es),maximum_degree=max(map(len,adj)),
                maximum_component=maximum,
                profile=[components[0,1][net['s']],components[0,2][net['s']],
                         components[0,1][net['t']],components[1,2][net['t']]],
                proper=True,acyclic=True,no_terminal_transmission=True)


def main():
    wall,cpu=time.perf_counter(),time.process_time()
    p1=parallel([leaf(),leaf(),leaf()])
    p2=parallel([p1,p1,p1])
    odd=series([leaf(),p2,leaf()])
    bad=leaf()
    for _ in range(3):
        module=series([bad,leaf()],even=True)
        bad=parallel([module,module])
    nets={'two_level_ternary_parallel':p2,'odd_series_with_leaf_at_left':odd,
          'even_series_failure_h3':bad}
    result={name:inspect(net) for name,net in nets.items()}
    assert result['two_level_ternary_parallel']['maximum_component']==13
    assert result['two_level_ternary_parallel']['profile']==[2,1,1,2]
    assert result['odd_series_with_leaf_at_left']['maximum_component']==13
    assert result['odd_series_with_leaf_at_left']['profile']==[1,2,1,2]
    assert result['even_series_failure_h3']['profile'][0]==8
    assert result['even_series_failure_h3']['n']==52
    assert result['even_series_failure_h3']['m']==58
    assert result['even_series_failure_h3']['maximum_degree']==3
    result={'status':'PASS','producer_imported':False,'cases':result,
            'inputs':nets,'body_wall_seconds':time.perf_counter()-wall,
            'body_cpu_seconds':time.process_time()-cpu,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            'scope':'Three new exact boundary-profile diagnostics; not an all-size proof or application benchmark.'}
    out=Path(__file__).with_name('RESULT.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='inputs'},indent=2))

if __name__=='__main__':main()
