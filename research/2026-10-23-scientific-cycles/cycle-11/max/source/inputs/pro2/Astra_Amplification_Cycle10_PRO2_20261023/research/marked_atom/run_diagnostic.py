"""New marked-normalizer diagnostic.  No inherited closure or suite is run."""
from pathlib import Path
import argparse, hashlib, json, resource, sys, time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'src'))
from marked_atom import prepare_marked_certificate, color_marked_atom


def paths_between(lengths):
    es = []; paths = []; nxt = 2
    for length in lengths:
        ids = list(range(nxt, nxt+length-1)); nxt += length-1
        path = [0]+ids+[1]; paths.append(path)
        es.extend(tuple(sorted(e)) for e in zip(path, path[1:]))
    return nxt, sorted(es), paths


def a_l(length):
    # Hubs a=0,b=1,c=2; two paths2 a-b, two paths2 a-c, long path b-c.
    es = []; nxt = 3; paths = []
    for s, t, ell in [(0,1,2),(0,1,2),(0,2,2),(0,2,2),(1,2,length)]:
        ids = list(range(nxt, nxt+ell-1)); nxt += ell-1
        path = [s]+ids+[t]; paths.append(path)
        es.extend(tuple(sorted(e)) for e in zip(path, path[1:]))
    return nxt, sorted(es), paths


def independent_check(g):
    n, es, colors, root = g['n'], g['edges'], g['colors'], g['mark']
    adj = [set() for _ in range(n)]
    for u,v in es:
        assert colors[u] != colors[v]
        adj[u].add(v);adj[v].add(u)
    # Direct enumeration of ordered simple 4-vertex paths, not producer masks.
    for v in range(n):
        for u in adj[v]:
            for w in adj[v]-{u}:
                for z in adj[w]-{u,v}:
                    assert not (colors[u] == colors[w] and colors[v] == colors[z])
    assert len(adj[root]) == 2
    ns = {colors[v] for v in adj[root]}
    fs = {colors[v] for v in adj[root] if any(w != root and colors[w] == colors[root] for w in adj[v])}
    assert len(ns) == 2 and len(fs) <= 1
    assert ns == set(g['root_neighbors']) and fs == set(g['root_flags'])
    return dict(proper=True, all_simple_P4_nonbichromatic=True,
                distinct_root_neighbors=True, actual_root_flag_count=len(fs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', required=True)
    ap.add_argument('--projection', required=True)
    args = ap.parse_args()
    start, cpu = time.perf_counter(), time.process_time()
    bundle = prepare_marked_certificate(args.certificate, args.projection)
    load_seconds = time.perf_counter()-start
    cases = [dict(name='triangle_mark2', n=3, edges=[(0,1),(0,2),(1,2)], mark=2)]
    cases.append(dict(name='cycle7_mark4', n=7,
                      edges=sorted(tuple(sorted((i,(i+1)%7))) for i in range(7)), mark=4))
    n, es, ps = paths_between([2,3,4,5])
    for name, mark in [('short_branch', ps[0][1]), ('long_branch_middle', ps[3][2])]:
        cases.append(dict(name='theta_2345_'+name, n=n, edges=es, mark=mark))
    n, es, ps = a_l(5)
    for name, mark in [('parallel_middle',ps[0][1]), ('long_connector_middle',ps[4][2])]:
        cases.append(dict(name='A5_'+name,n=n,edges=es,mark=mark))
    records=[]
    for case in cases:
        t=time.perf_counter()
        g=color_marked_atom(case['n'],case['edges'],case['mark'],bundle)
        g['name']=case['name']; g['input']=case
        g['independent_direct_P4_check']=independent_check(g)
        g['wall_seconds']=time.perf_counter()-t
        records.append(g)
    out=dict(schema='astra-cycle10-marked-adapter-diagnostic/v1',status='PASS',
             scope='Six NEW specified-root normalizer realizations, not inherited closure replay.',
             cases=records, certificate_load_wall_seconds=load_seconds,
             wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
             peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
             source_sha256=hashlib.sha256((ROOT/'src/marked_atom.py').read_bytes()).hexdigest())
    (ROOT/'results/DIAGNOSTIC.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
    print(json.dumps([dict(name=g['name'],n=g['n'],m=len(g['edges']),family=g['root_family'],
                          profile=g['profile'],siblings=g['native_normal_form'].get('preparation',{}).get('parallel_siblings'))
                      for g in records],indent=2))


if __name__=='__main__':
    main()
