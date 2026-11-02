#!/usr/bin/env python3
"""Exact complete killing-output check for the new receiver mismatch."""
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'astra-sol-subgeometric-synthesis-20261102'))
from verify_normal_cell import cell,Y
from verify_high_anchor_work import psi

def main():
    rows=[];count=0
    for n in (2,10,100):
        keys,xs,edges,kills,mu,adj=cell((n,n,n,n));minimum=None;local=0
        for key,x,row in zip(keys,xs,kills):
            i,j,k=key
            assert psi(x,20)==n+(0,3,2,1)[i]+(0,3,2,1)[j]
            for kind,rate,delta,block,source in row:
                out=list(x);off=3*block
                for q in range(3):out[off+q]+=Y[(source+1)%4][q]-Y[source][q]
                assert min(out)>=0
                gap=psi(out,20)-n;assert gap>=3
                minimum=gap if minimum is None else min(minimum,gap);local+=1
        count+=local;rows.append({'residual_even_count':n,'normal_states':len(keys),
                                 'complete_genuine_killing_outputs_checked':local,'minimum_work_increase':minimum})
    result={'exact_outputs_checked':count,'cases':rows,
            'scope':'All physical killing outputs in each finite cell; the all-even-count proof is LOW_ANCHOR_RECEIVER_FRONTIER.md. This refutes this stop/receiver composition, not recurrence.'}
    (P/'results/low_receiver_failure.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
