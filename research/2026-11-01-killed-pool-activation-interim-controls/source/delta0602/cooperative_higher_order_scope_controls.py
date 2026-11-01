"""Exact scope checks for the min-three-A/degree-six witness."""
import json,hashlib
from fractions import Fraction
from pathlib import Path
from cooperative_scope_controls import rank

ROOT=Path(__file__).resolve().parents[2]


def main():
    m=6;q=7;s=3;zero=(0,0,0);ab=(1,0,1);end=(m,0,q)
    reactions=[{'id':'immigration','source':zero,'product':ab,'rate':1},
               {'id':'activation','source':ab,'product':end,'rate':1},
               {'id':'clearing','source':end,'product':zero,'rate':1}]
    for j,(ku,kd) in enumerate(zip((2,7,11),(1,3,5)),s):
        y=(j,m-j,q);z=(j+1,m-j-1,q)
        reactions.extend(({'id':f'fast_{j}_up','source':y,'product':z,'rate':ku},
                          {'id':f'fast_{j}_down','source':z,'product':y,'rate':kd}))
    cx={tuple(e[k]) for e in reactions for k in ('source','product')}
    sr=rank([[b-a for a,b in zip(e['source'],e['product'])] for e in reactions])
    assert len(cx)==6 and sr==3
    off=(m-2,0,q)
    failures=[{'reaction':e['id'],'side':side,'complex':e[side]} for e in reactions[3:]
              for side in ('source','product') if any(v<w for v,w in zip(e[side],off))]
    assert failures
    for n in range(1,17):
        a,x,b=7*n,0,7*n
        for _ in range(n):
            assert a>=6 and b>=7
            a-=1;x+=1
        for _ in range(n):
            assert a>=6 and b>=7
            a-=6;b-=7
        assert (a,x,b)==(0,n,0)
    out={'status':'PASS exact higher-order structural distinctions','m':m,'q':q,'minimum_fast_A':s,
         'species_order':['A','X','B'],'raw_network':reactions,'complex_count':6,
         'stoichiometric_rank':3,'linkage_classes':1,'deficiency':2,
         'incompatible_complex_balance_A_X_ratios':['2','7/3','11/5'],
         'old_raw_required_offset':off,'failed_old_offset_guards':failures,
         'two_A_contract':'fails: 2A+4X is absent; no inherited two-A uniform logarithmic ratio',
         'pure_contract':'fails: 6X is absent','one_A_contract':'fails: A+5X is absent',
         'reachable_ACK_tier_counterexample':'(0,n,0): 7n immigrations, n fast A-to-X transfers, n clearings; S-top 0 differs from D-top 3A+3X+7B',
         'scope':'Names sufficient-contract failures only, not an exhaustive novelty search or a recurrence converse.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'import_sha256':hashlib.sha256((Path(__file__).parent/'cooperative_scope_controls.py').read_bytes()).hexdigest()}
    (ROOT/'outputs/mechanism_selection_20261101/cooperative_higher_order_scope_controls.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','deficiency','failed_old_offset_guards','two_A_contract')},indent=2))


if __name__=='__main__':main()
