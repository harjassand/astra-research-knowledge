"""New edge-closure projection of the fixed H8 certificate, not its closure search."""
from pathlib import Path
import argparse,hashlib,json,time,resource

EXPECTED='63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525'

def project(source):
    rows=[]
    for family in source['families']:
        if family['degree'][0]!=2 or not 1<=family['degree'][1]<=3:
            continue
        options=[]
        for ti,sig in enumerate(family['targets']):
            a,b,dl,nl,fl,dr,nr,fr=sig
            if a==b or fl>>b&1 or fr>>a&1 or ((nl>>b&1) and (nr>>a&1)):
                continue
            neighbors=nl|(1<<b)
            flags=fl|((1<<b) if nr>>a&1 else 0)
            if neighbors.bit_count()>2:
                continue
            missing=next(c for c in range(4) if c!=a and not(neighbors>>c&1))
            options.append((neighbors.bit_count(),flags.bit_count(),ti,missing,neighbors,flags,sig))
        assert options,('empty degree-three edge closure',family['id'])
        _,_,ti,missing,neighbors,flags,sig=min(options)
        rows.append(dict(family=family['id'],degree=family['degree'],target_index=ti,
            inherited_target=sig,restored_root_degree=3,root_neighbor_upper_mask=neighbors,
            root_far_flag_upper_mask=flags,missing_color=missing,
            admissible_target_count=len(options)))
    assert len(rows)==18
    return rows

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('certificate',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args()
    start,cpu=time.perf_counter(),time.process_time()
    raw=args.certificate.read_bytes();assert hashlib.sha256(raw).hexdigest()==EXPECTED
    rows=project(json.loads(raw))
    result=dict(schema='astra-degree3-edge-closure/v1',source_sha256=EXPECTED,rows=rows,
        cases=len(rows),all_nonempty=True,guarantee='Every H8 family of degree (2,d), d in 1..3, permits restoration of the original terminal edge to a star-four graph with a missing neighbor color at its degree-three left port.',
        wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        cost_scope='New projection including source read/parse, excluding JSON serialization, inference, proof and authoring; no old closure rerun.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
