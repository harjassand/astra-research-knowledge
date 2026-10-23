"""Create the exact native inputs; no decomposition is supplied to receiver."""
from pathlib import Path
import json,time,resource,hashlib
ROOT=Path(__file__).resolve().parents[1]

def main():
    start,cpu=time.perf_counter(),time.process_time()
    source=ROOT/'research/root_diagnostic/INPUTS.json'
    g=json.loads(source.read_text())['graphs'][2]
    inputs=[dict(name='native_K24_obstruction_16',n=g['n'],edges=g['edges'],
                 provenance=dict(source='research/root_diagnostic/INPUTS.json',
                                 sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                 graph_index=2),
                 purpose='The SAME original support excluding every star-four coloring; native four-action and five-action receiving control.')]
    # p3 branching and unequal k exercise the parameterized native branch.
    # Recipe parents None,0,0,1; attachments at root middles0,1 and block1
    # middle1. Each occurrence has fresh hubs and fresh nonshared middles.
    p=3;ks=[4,5,4,5];parents=[None,0,0,1];parent_slots=[None,0,1,1]
    blocks=[];es=[];n=0
    for i,(k,pa,slot) in enumerate(zip(ks,parents,parent_slots)):
        hs=list(range(n,n+p));n+=p
        mid=[] if pa is None else [blocks[pa]['middles'][slot]]
        while len(mid)<k:
            mid.append(n);n+=1
        blocks.append(dict(hubs=hs,middles=mid))
        es.extend(sorted((h,v)) for h in hs for v in mid)
    assert n==27 and len(es)==54
    inputs.append(dict(name='native_p3_unequal_branch_27',n=n,edges=sorted(es),
                       provenance=dict(recipe='p=3;k=(4,5,4,5);parents=(None,0,0,1);parent_slots=(None,0,1,1)',
                                       source='src/make_inputs.py'),
                       purpose='New p=3, unequal-block, branching/depth receiving branch; not a graph-size sweep or a chordless claim.'))
    records=[]
    for inp in inputs:
        raw=(json.dumps(inp,indent=2)+'\n').encode()
        out=ROOT/'inputs'/f"{inp['name']}.json";out.write_bytes(raw)
        records.append(dict(file=out.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    result=dict(records=records,wall_seconds=time.perf_counter()-start,
                cpu_seconds=time.process_time()-cpu,
                peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
    (ROOT/'results/INPUT_CONSTRUCTION_COSTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
