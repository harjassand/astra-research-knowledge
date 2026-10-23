#!/usr/bin/env python3
"""Receive the new boundary extension into full-support recovery.

This evaluates the actual original operator, not a reduced-action surrogate.
It does not repeat the local boundary transition experiment.
"""
from pathlib import Path
import sys,json,time,resource,hashlib
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'experiments')]
from cut_balance import prepare, summary
from cut_balance_operations import noise_case


def main():
    wall=time.perf_counter(); cpu=time.process_time()
    source=ROOT/'research/structure/RESULT.json'
    raw=source.read_bytes(); fixture=json.loads(raw)['fixture']
    colors_map=dict(fixture['colors']); vertices=fixture['vertices']
    assert vertices==list(range(len(vertices)))
    colors=[colors_map[v] for v in vertices]
    rp={v:i for i,v in enumerate(fixture['reduced_vertices'])}
    red_colors=dict(fixture['reduced_colors'])
    reduced=prepare(len(rp),[(rp[u],rp[v]) for u,v in fixture['reduced_edges']],
                    [red_colors[v] for v in fixture['reduced_vertices']],4)
    original,case=noise_case(len(vertices),fixture['edges'],colors,4)
    assert original['gamma']<=max(65*reduced['gamma'],F(64))
    old=set(rp)
    # Verify the receiving-use attachment obligations directly on this input.
    root_mass={}; detached_sizes=[]; attachment_sizes=[]
    edge_set=set(map(tuple,fixture['edges']))
    red_edges=set(map(tuple,fixture['reduced_edges']))
    for comp in original['components']:
        p=comp['pair']; vs=set(comp['order']); retained=old & vs
        adj={v:[] for v in vs}
        for v in comp['order'][1:]:
            u=comp['parent'][v]
            if tuple(sorted((u,v))) not in red_edges:
                adj[u].append(v); adj[v].append(u)
        seen=set()
        for start in vs:
            if start in seen: continue
            piece={start}; seen.add(start); todo=[start]
            for u in todo:
                for v in adj[u]:
                    if v not in seen: seen.add(v); piece.add(v); todo.append(v)
            ports=piece & old
            assert len(ports)<=1
            if ports:
                root=next(iter(ports)); count=len(piece)-1
                root_mass[p,root]=root_mass.get((p,root),0)+count
                attachment_sizes.append(count)
            else: detached_sizes.append(len(piece))
    A=max(root_mass.values(),default=0); B=max(detached_sizes,default=0)
    transfer=max((1+A)*reduced['gamma'],F(A),F(B,4))
    assert original['gamma']<=transfer
    result={'status':'PASS','source_relative':'research/structure/RESULT.json',
            'source_bytes':len(raw),'source_sha256':hashlib.sha256(raw).hexdigest(),
            'reduced_plan':summary(reduced),'original_operation':case,
            'attachment_check':{'maximum_added_vertices_per_old_vertex_and_pair':A,
                                'maximum_detached_tree_size':B,
                                'certified_gamma_upper':str(transfer),
                                'actual_gamma':str(original['gamma']),
                                'no_attachment_meets_two_old_vertices_after_old_edges_removed':True},
            'scope':'New local strip extension received into full original-support operator reconstruction; reduced coloring supplied, not solved generically.',
            'costs':{'body_wall_seconds':time.perf_counter()-wall,
                     'body_cpu_seconds':time.process_time()-cpu,
                     'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                     'executions':1,'discovery_and_authoring':'unmetered; additional'}}
    out=ROOT/'results/received_strip_operation.json'
    saved=(json.dumps(result,indent=2)+'\n').encode(); out.write_bytes(saved)
    print(json.dumps({'status':'PASS','reduced_plan':summary(reduced),
                      'original_plan':summary(original),
                      'attachment_check':result['attachment_check'],
                      'costs':result['costs'],'fixture_bytes':len(saved),
                      'fixture_sha256':hashlib.sha256(saved).hexdigest()},indent=2))


if __name__=='__main__': main()
