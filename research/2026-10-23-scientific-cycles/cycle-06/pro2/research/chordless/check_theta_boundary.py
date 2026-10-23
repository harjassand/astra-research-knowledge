"""Bounded exact tests of the new theta interface and induction obstruction."""
import argparse
import itertools
import json
import resource
import time
from pathlib import Path
from theta_boundary import (BoundaryObstruction, extend_theta, theta_graph,
                            free_three_color_theta, cap_induction_witness)


def analyze(vertices, edges, colors, q=4):
    if any(colors[u] == colors[v] for u,v in edges):
        return {"proper":False,"acyclic":False}
    records=[]; acyclic=True
    for pair in itertools.combinations(range(q),2):
        selected={v for v in vertices if colors[v] in pair}
        adj={v:[] for v in selected}
        for u,v in edges:
            if u in selected and v in selected:
                adj[u].append(v);adj[v].append(u)
        while selected:
            s=next(iter(selected)); selected.remove(s);seen={s};stack=[s];degree=0
            while stack:
                u=stack.pop();degree+=len(adj[u])
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v);selected.remove(v);stack.append(v)
            tree=degree==2*(len(seen)-1)
            acyclic &= tree
            records.append({"pair":pair,"vertices":sorted(seen),"is_tree":tree})
    return {"proper":True,"acyclic":acyclic,"max_component":max(len(t['vertices']) for t in records),
            "terminal_connections":[t['pair'] for t in records if 0 in t['vertices'] and 1 in t['vertices']],
            "components":records}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'))
    args=parser.parse_args()
    wall,cpu=time.perf_counter(),time.process_time()
    lengths_cases=[(2,2),(2,3),(3,7),(2,2,2),(2,2,5),(2,4,7),(3,5,8),
                   (2,2,2,2),(2,2,2,13),(2,2,5,9),(2,4,7,10),(3,4,9,17)]
    cases=[];full=[];accepted=blocked=0
    for lengths in lengths_cases:
        for a,b in itertools.product(range(4),repeat=2):
            should_block=a==b and sum(l==2 for l in lengths)==4
            try:
                obj=extend_theta(lengths,(a,b))
            except BoundaryObstruction:
                assert should_block
                blocked+=1;cases.append({"lengths":lengths,"terminal_colors":[a,b],"status":"exact_obstruction"})
                continue
            assert not should_block
            colors=dict(obj['colors'])
            result=analyze(obj['vertices'],obj['edges'],colors)
            assert result['proper'] and result['acyclic']
            assert result['max_component']<=obj['component_bound']
            expected={tuple(sorted((a,c))) for c in obj['transmitting_channels']}
            assert set(map(tuple,result['terminal_connections']))==expected
            accepted+=1
            cases.append({"lengths":lengths,"terminal_colors":[a,b],"status":"PASS",
                          "max_component":result['max_component'],"bound":obj['component_bound'],
                          "terminal_connections":result['terminal_connections']})
            if (lengths,(a,b)) in [((2,2,2,13),(0,0)),((3,4,9,17),(0,1)),((2,2,5,9),(2,2))]:
                obj['analysis']=result;full.append(obj)
    brute=[]
    for r in (2,3,4):
        vertices,edges,paths=theta_graph([2]*r)
        mids=[p[1] for p in paths]
        for a,b in [(0,0),(0,1)]:
            count=0
            for assignment in itertools.product(range(4),repeat=r):
                colors={0:a,1:b};colors.update(zip(mids,assignment))
                check=analyze(vertices,edges,colors)
                count+=bool(check['proper'] and check['acyclic'])
            expected=(6 if r in (2,3) else 0) if a==b else 2**r
            assert count==expected
            brute.append({"branches":r,"terminal_colors":[a,b],"exact_valid_assignments":count})
    comparators=[]
    for lengths in lengths_cases:
        obj=free_three_color_theta(lengths)
        check=analyze(obj['vertices'],obj['edges'],dict(obj['colors']),q=3)
        assert check['proper'] and check['acyclic'] and not check['terminal_connections']
        assert check['max_component']<=obj['component_bound']
        comparators.append({"lengths":lengths,"max_component":check['max_component'],"bound":obj['component_bound']})
    caps=[]
    for k in (2,6,17,64):
        obj=cap_induction_witness(k);colors=dict(obj['old_colors']);z=obj['deleted_vertex']
        before=analyze(range(2*k),obj['old_edges'],colors)
        assert before['acyclic'] and before['max_component']==k
        for c in (2,3):
            after=analyze(obj['vertices'],obj['edges'],colors|{z:c})
            assert after['proper'] and after['acyclic'] and after['max_component']==k+1
        bx,by=obj['boundary_edge']
        assert z not in (bx,by) and all(tuple(sorted((z,w))) not in obj['edges'] for w in (bx,by))
        caps.append(obj)
    report={"status":"PASS","accepted_four_color_extensions":accepted,
            "blocked_endpoint_states":blocked,"all_boundary_cases":cases,
            "selected_complete_fixtures":full,"short_branch_exhaustive_counts":brute,
            "free_three_color_comparator":comparators,"cap_induction_witnesses":caps,
            "body_wall_seconds":time.perf_counter()-wall,"body_cpu_seconds":time.process_time()-cpu,
            "maxrss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            "scope":"exact finite diagnostics; all-size proofs are in PROOF.md"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['all_boundary_cases','selected_complete_fixtures',
          'short_branch_exhaustive_counts','free_three_color_comparator','cap_induction_witnesses']},indent=2))


if __name__=='__main__':
    main()
