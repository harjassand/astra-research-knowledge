"""Direct independent 17-vertex star-three counterexample check.

Uses only this independent review's graph and transition routines, never root
producer code. Direct assignment enumeration and exact terminal-state DP agree.
"""
from pathlib import Path
import hashlib
import json
import resource
import time
from check_port_interface import path, series, parallel, actual_states, series_states, parallel_states


def main():
    t0=time.perf_counter(); cpu=time.process_time()
    L=path(2); A=series(L,L); C=parallel([L,L]); B=parallel([L,A,C]); G=parallel([A,B])
    assert (G['n'],len(G['edges']))==(17,20)
    t=time.perf_counter()
    direct,counts=actual_states(G,palette=3)
    direct_seconds=time.perf_counter()-t
    assert not direct
    t=time.perf_counter()
    ls,leaf_counts=actual_states(L,palette=3)
    ast=series_states(ls,ls)
    cst=parallel_states([ls,ls],palette=3)
    bst=parallel_states([ls,ast,cst],palette=3)
    gst=parallel_states([ast,bst],palette=3)
    dp_seconds=time.perf_counter()-t
    assert gst==direct==set()
    assert len(ls)>0 and len(ast)>0 and len(cst)>0 and len(bst)>0
    degree=[0]*G['n']
    for u,v in G['edges']: degree[u]+=1;degree[v]+=1
    assert max(degree)==4
    result={'status':'PASS','graph':G,'degree':degree,
            'expression':'L=path2; A=S2(L,L); C=P2(L,L); B=P3(L,A,C); G=P2(A,B)',
            'direct_enumeration':{'palette':3,**counts,'attainable_signatures':len(direct),
                                  'wall_seconds':direct_seconds,'symmetry_reduction':'none; all labeled proper three-colorings enumerated'},
            'independent_state_DP':{'state_counts':{'L':len(ls),'A':len(ast),'C':len(cst),'B':len(bst),'G':len(gst)},'wall_seconds':dp_seconds},
            'scope':'No star-three vertex coloring exists on this exact graph. With the separately verified star-four construction this gives star chromatic number4. It is not an arbitrary-real three-query or acyclic-three obstruction.',
            'cost':{'wall_seconds':time.perf_counter()-t0,'cpu_seconds':time.process_time()-cpu,
                    'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                    'excludes':'process startup, authoring/proof review, final receipt serialization'}}
    here=Path(__file__).resolve().parent
    (here/'THREE_STAR_OBSTRUCTION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
