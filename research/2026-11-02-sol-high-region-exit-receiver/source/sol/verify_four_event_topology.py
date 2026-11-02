#!/usr/bin/env python3
"""Exact source-word topology independent of all positive rates/large axes."""
from pathlib import Path
import json
from four_nc_axis_kernel import raw_list,f_values
from verify_high_anchor_work import ff

P=Path(__file__).resolve().parent

def main():
    root=(100,0,0,100,0,0);raw=raw_list((1,1,1,1),(1,1,1,1),2,1)
    todo=[(root,())];positive=[];normal_prefix=[];levels=[]
    for depth in range(4):
        out=[]
        for x,word in todo:
            ready=min(x[1:3])>=2 or min(x[4:6])>=2
            if ready:
                assert depth==3 and word in ((0,1,2),(4,5,6))
                normal_prefix.append({'word':word,'state_offset':[v-z for v,z in zip(x,root)]})
                continue
            for j,(s,u,kappa) in enumerate(raw[:8]):
                if not ff(x,s):continue
                z=tuple(v-a+b for v,a,b in zip(x,s,u));newword=word+(j,)
                if depth==3:
                    f=f_values(z);delta=(f[0]-100,f[1]-100)
                    assert min(delta)>=0
                    if any(delta):positive.append({'word':newword,'normalized_anchor_delta':delta,
                                                  'hidden_endpoint':[z[j] for j in (1,2,4,5)]})
                out.append((z,newword))
        levels.append({'noncore_depth':depth+1,'ordinary_source_words':len(out)})
        todo=out
    assert len(normal_prefix)==2
    expected={(0,0,1,1),(0,1,0,1),(0,1,1,0),(4,4,5,5),(4,5,4,5),(4,5,5,4)}
    assert {tuple(v['word']) for v in positive}==expected
    result={'clean_three_event_prefixes':normal_prefix,'all_positive_ordinary_four_event_words':positive,
            'levels':levels,'scope':'Feasible topology and normalized-anchor increments hold for every axis count>=8 and every positive raw rate. This is not the stochastic sign proof.'}
    (P/'results/four_event_topology.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
