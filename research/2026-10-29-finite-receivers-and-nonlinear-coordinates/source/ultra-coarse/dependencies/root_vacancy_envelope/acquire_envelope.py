"""Exact native-graph extrema given ONLY total vacancy count.

Ordinary finite-width transfer DP, not a new graph algorithm or a physical
measurement. Every edge comes from C's parsed pinned native O2 catalog.
"""
from pathlib import Path
import hashlib,itertools,json,time

HERE=Path(__file__).resolve().parent
INPUT=HERE.parent/'c_intervention_operation'/'PAIR_GRAPH.json'

def acquire(graph):
    M=graph['sites'];assert M==32
    edges=[tuple(sorted(e['ends'])) for e in graph['edges']]
    assert len(set(edges))==len(edges)==64
    assert all(0<=a<b<M for a,b in edges)
    assert all(sum(v in e for e in edges)==4 for v in range(M))
    rates={e['rate'] for e in graph['edges']};assert len(rates)==1
    rate=rates.pop();assert rate==graph['common_pair_rate']>0
    # The map is VERIFIED against the native list, not assumed from a label.
    expected={tuple(sorted((x+8*y,(x+1)%8+8*y))) for y in range(4) for x in range(8)}
    expected|={tuple(sorted((x+8*y,x+8*((y+1)%4)))) for y in range(4) for x in range(8)}
    assert set(edges)==expected
    slices=[[x+8*y for y in range(4)] for x in range(8)]
    gm=[[sum((1<<v) for y,v in enumerate(ss) if m>>y&1) for m in range(16)] for ss in slices]
    count=[m.bit_count() for m in range(16)]
    inside=[];between=[]
    for x in range(8):
        ee=[e for e in edges if e[0]%8==e[1]%8==x]
        inside.append([sum(bool(mask>>a&1 and mask>>b&1) for a,b in ee) for mask in gm[x]])
        nxt=(x+1)%8
        ee=[e for e in edges if {e[0]%8,e[1]%8}=={x,nxt}]
        assert len(ee)==4
        between.append([[sum(bool((a|b)>>u&1 and (a|b)>>v&1) for u,v in ee)
                         for b in gm[nxt]] for a in gm[x]])
    minimum=[10**9]*(M+1);maximum=[-1]*(M+1)
    minwit=[None]*(M+1);maxwit=[None]*(M+1)
    transitions=0
    for first in range(16):
        # key=(last slice mask,total v); value=mincost,minwit,maxcost,maxwit
        dp={(first,count[first]):(inside[0][first],gm[0][first],inside[0][first],gm[0][first])}
        for x in range(1,8):
            out={}
            for (last,v),(lo,lw,hi,hw) in dp.items():
                for new in range(16):
                    key=(new,v+count[new]);add=inside[x][new]+between[x-1][last][new]
                    nl,nh=lo+add,hi+add;nw_l,nw_h=lw|gm[x][new],hw|gm[x][new]
                    if key not in out:out[key]=(nl,nw_l,nh,nw_h)
                    else:
                        a,aw,b,bw=out[key]
                        if (nl,nw_l)<(a,aw):a,aw=nl,nw_l
                        if nh>b or (nh==b and nw_h<bw):b,bw=nh,nw_h
                        out[key]=(a,aw,b,bw)
                    transitions+=1
            dp=out
        for (last,v),(lo,lw,hi,hw) in dp.items():
            close=between[7][last][first];lo+=close;hi+=close
            if lo<minimum[v] or (lo==minimum[v] and lw<minwit[v]):minimum[v],minwit[v]=lo,lw
            if hi>maximum[v] or (hi==maximum[v] and hw<maxwit[v]):maximum[v],maxwit[v]=hi,hw
    return dict(sites=M,edges=edges,common_pair_rate=rate,
                min_empty_edges=minimum,max_empty_edges=maximum,
                min_witness_masks=minwit,max_witness_masks=maxwit,
                transitions=transitions)

def verify(out):
    M=out['sites'];edges=out['edges'];mn=out['min_empty_edges'];mx=out['max_empty_edges']
    score=lambda mask:sum(bool(mask>>a&1 and mask>>b&1) for a,b in edges)
    for v in range(M+1):
        lo,hi=out['min_witness_masks'][v],out['max_witness_masks'][v]
        assert lo.bit_count()==hi.bit_count()==v
        assert score(lo)==mn[v] and score(hi)==mx[v]
        assert max(0,4*v-2*M)<=mn[v]<=mx[v]<=2*v
        assert mn[v]==4*v-2*M+mn[M-v]
        assert mx[v]==4*v-2*M+mx[M-v]
    checked=0
    for v in range(5):
        low,high=10**9,-1
        for ss in itertools.combinations(range(M),v):
            mask=sum(1<<i for i in ss);s=score(mask)
            low=min(low,s);high=max(high,s);checked+=1
        assert low==mn[v] and high==mx[v]
    return dict(native_direct_subsets_checked=checked,vacancy_counts_directly_enumerated=[0,1,2,3,4],
                all_66_extreme_witnesses_checked=True,complement_identity=True)

def main():
    start=time.perf_counter();raw=INPUT.read_bytes();g=json.loads(raw)
    out=acquire(g);dp_done=time.perf_counter()
    check=verify(out);end=time.perf_counter()
    out.update(status='EXACT INTEGER FRONTIER DP; NATIVE GRAPH ONLY',
       input_file=str(INPUT.resolve()),input_sha256=hashlib.sha256(raw).hexdigest(),
       source_model_sha256=g['source_model_sha256'],
       comparison='ordinary degree4 envelope max(0,4v-64) <= E_empty <= 2v',
       acquisition_seconds=dp_done-start,verification_seconds=end-dp_done,
       checks=check,
       scope='Extrema for every configuration of the exact32-site graph given only totalv. Multiply by supplied common O2 rate for activity. No dynamics, physical detector, rates or confidence intervals acquired.',
       source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'ENVELOPE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['edges','min_witness_masks','max_witness_masks']},indent=2))

if __name__=='__main__':main()
