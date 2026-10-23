"""New actual marked-degree-three normalization tests; no inherited closure replay."""
from pathlib import Path
from collections import Counter
import argparse,sys,json,time,resource,hashlib

HERE=Path(__file__).resolve().parent

def theta(lengths):
    edges=[];n=2
    for ell in lengths:
        old=0
        for _ in range(ell-1):edges.append((old,n));old=n;n+=1
        edges.append((old,1))
    return n,edges

def adjacent_high_degree():
    # Two a-b path2 branches and a-x--(three x-y path2 branches)--y-z-b.
    edges=[(0,4),(4,1),(0,5),(5,1),(0,2),(3,6),(6,1)]
    for w in (7,8,9):edges.extend([(2,w),(w,3)])
    return 10,edges

def actual_check(g):
    n=g['n'];edges=g['edges'];cs=g['colors'];mark=g['mark']
    adj=[set() for _ in range(n)]
    for u,v in edges:
        assert u!=v and cs[u]!=cs[v];adj[u].add(v);adj[v].add(u)
    # Enumerate simple P4s instead of using the producer's multiplicity test.
    p4_count=0
    for a in range(n):
        for b in adj[a]:
            for c in adj[b]-{a}:
                for d in adj[c]-{a,b}:
                    p4_count+=1
                    assert len({cs[a],cs[b],cs[c],cs[d]})>=3
    counts=Counter(cs[v] for v in adj[mark])
    assert len(adj[mark])==3 and len(counts)<=2
    missing=sorted(set(range(4))-{cs[mark]}-set(counts))
    assert missing==g['profile']['missing_neighbor_colors'] and missing
    assert [counts.get(c,0) for c in range(4)]==g['profile']['neighbor_color_multiplicities']
    # Every channel missing from the atom may be the color of a parent vertex.
    # The newly attached edge is the ONLY action-support addition considered here.
    extensions=[]
    for c in missing:
        ext=cs+[c];ee=edges+[(mark,n)];aa=adj+[set()]
        aa=[set(x) for x in aa];aa[mark].add(n);aa[n].add(mark)
        for a in range(n+1):
            for b in aa[a]:
                for d in aa[b]-{a}:
                    for e in aa[d]-{a,b}:assert len({ext[a],ext[b],ext[d],ext[e]})>=3
        extensions.append(dict(parent_color=c,root_color=cs[mark],new_pair_component_vertices=[mark,n],star_preserved=True))
    return dict(status='PASS',simple_p4_walks=p4_count,missing_channels=missing,leaf_extensions=extensions)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-dir',required=True,type=Path);args=ap.parse_args()
    sys.path.insert(0,str(args.source_dir/'src'));sys.path.insert(0,str(HERE/'src'))
    from degree3_atom import Degree3AtomOracle
    start,cpu=time.perf_counter(),time.process_time()
    bundle=Degree3AtomOracle(args.source_dir/'sources/loaded_star_certificate.json',HERE/'results/DEGREE3_PROJECTION.json')
    load=time.perf_counter()-start
    cases=[]
    for lengths in [(2,2,2),(2,3,7)]:
        n,es=theta(lengths)
        cases.extend([dict(name='theta_'+str(lengths)+'_left',n=n,edges=es,mark=0,neighbor=2),
                      dict(name='theta_'+str(lengths)+'_right',n=n,edges=es,mark=1,neighbor=es[-1][0])])
    n,es=adjacent_high_degree()
    cases.extend([dict(name='root3_neighbor4',n=n,edges=es,mark=0,neighbor=2),
                  dict(name='opposite_root3_neighbor2',n=n,edges=es,mark=1,neighbor=6)])
    records=[]
    for case in cases:
        g=bundle.color(case['n'],case['edges'],case['mark'],case['neighbor'])
        assert sorted(tuple(sorted(e)) for e in case['edges'])==g['edges']
        records.append(dict(input=case,result=g,independent_actual_check=actual_check(g)))
    result=dict(schema='astra-degree3-native-diagnostic/v1',cases=records,count=len(records),status='PASS',fixed_source_load_wall_seconds=load,
        wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        scope='Six NEW actual degree-three root constructions and original-support/direct-P4 checks; not old closure or a global composition claim.',
        excludes='JSON serialization, interpreter startup, source reading/authoring/inference/review/integration; initial exploratory projection was unmeasured.')
    (HERE/'results/NATIVE_DIAGNOSTIC.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
    print(json.dumps([dict(name=r['input']['name'],family=r['result']['root_family'],profile=r['result']['profile']) for r in records],indent=2))

if __name__=='__main__':main()
