"""Exact adversary for local unflagged entries without an outgoing reset."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,resource,time
from coordinate_decoder import prepare,cut_witness,action,norm_sq
from block_reset_recovery import prepare_recovery
from marked_atom import prepare_marked_certificate

ROOT=Path(__file__).resolve().parents[1]


def main():
    start,cpu=time.perf_counter(),time.process_time()
    b=8; n=1; r=0; colors=[0]; edges=[]; blocks=[]
    for i in range(b):
        u,v,w=n,n+1,n+2;n+=3
        c=colors[r]; colors.extend([1-c,2,3])
        es=[tuple(sorted(e)) for e in [(r,u),(u,v),(v,w),(w,r)]]
        edges.extend(es);blocks.append(dict(vertices=[r,u,v,w],edges=es,colors=[c,1-c,2,3]))
        r=u
    edges.sort()
    native=dict(name='unflagged_entry_without_message_C4_chain',n=n,edges=edges,
                literal_bad_colors=colors,block_count=b,blocks=blocks,
                scope='Counterexample to local admission without mandatory outgoing reset, not all four-column designs.')
    # Every literal local coloring uses four different colors, hence is star
    # with two distinct root neighbors and zero flags. The common parent/
    # child channel is the intended alternating 0/1 channel.
    for i,block in enumerate(blocks):
        assert len(set(block['colors']))==4
        if i:
            pc=blocks[i-1]['colors'];cc=block['colors']
            assert {pc[0],pc[2]}.intersection({cc[1],cc[3]})=={cc[1]}
    plan=prepare(n,edges,colors,4)
    comp=next(i for i,c in enumerate(plan['components']) if tuple(c['pair'])==(0,1))
    assert len(plan['components'][comp]['order'])==b+1
    witness=cut_witness(plan,comp)
    assert witness['inverse_lower_sq']==F(20,9)
    assert witness['action_norm_sq']==F(9,20)
    nativepath=ROOT/'inputs/no_message_C4_chain.json'
    nativepath.write_text(json.dumps(native,indent=2)+'\n')
    bundle=prepare_marked_certificate(ROOT/'sources/loaded_star_certificate.json',
                                      ROOT/'sources/marked_root_projection.json')
    form,design,goodplan=prepare_recovery(n,edges,bundle)
    good_actions=action(n,4,design['colors'],witness['diagonal'],witness['edge_values'])
    result=dict(input='inputs/no_message_C4_chain.json',input_sha256=hashlib.sha256(nativepath.read_bytes()).hexdigest(),
                bad_colors=colors,bad_pair=[0,1],b=b,n=n,m=len(edges),
                a=witness['a'],d=witness['b'],cut=list(witness['edge']),
                inverse_lower_sq=str(witness['inverse_lower_sq']),
                bad_action_norm_sq=str(witness['action_norm_sq']),
                witness=dict(diagonal=[str(x) for x in witness['diagonal']],
                    edges=[dict(edge=list(e),value=str(v)) for e,v in sorted(witness['edge_values'].items())],
                    full_original_actions=[[str(x) for x in row] for row in witness['action']]),
                complete_rule_colors=design['colors'],complete_rule_design=design,
                complete_rule_largest_component=max(len(c['order']) for c in goodplan['components']),
                same_D_complete_rule_action_norm_sq=str(norm_sq(good_actions)),
                same_D_complete_rule_actions=[[str(x) for x in row] for row in good_actions],
                all_size_formula='a=floor((b+1)/2), d=ceil((b+1)/2), rho^2>=a*d/(b+1)',
                costs=dict(wall_seconds_before_serialization=time.perf_counter()-start,
                           cpu_seconds_before_serialization=time.process_time()-cpu))
    out=ROOT/'results/NO_MESSAGE_FAILURE.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    receipt=dict(wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
                 peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                 includes_input_and_result_serialization=True,
                 result_bytes=out.stat().st_size,result_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                 n=n,m=len(edges),inverse_lower_sq=result['inverse_lower_sq'],
                 bad_action_norm_sq=result['bad_action_norm_sq'],
                 complete_rule_largest_component=result['complete_rule_largest_component'])
    (ROOT/'results/NO_MESSAGE_COST.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
